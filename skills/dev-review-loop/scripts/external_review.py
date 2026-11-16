#!/usr/bin/env python3
"""Run one read-only external code review round through the Antigravity CLI (agy).

Two subcommands:

  check   Verify everything the loop depends on is installed. Exit 2 if not.
  run     Ask a fresh agy conversation to run /code-review against the uncommitted
          diff, verify the run really completed, and save the report.

Exit codes (the caller branches on these, so keep them stable):

  0  ok
  2  a dependency is missing                     -> tell the user what to install, stop
  3  the review did not complete                 -> NOT "zero findings"; see stderr
  4  the reviewer changed the worktree           -> stop, show the user what changed
  5  precondition not met (nothing to review...) -> fix the precondition, rerun

Standard library only, so it runs with a bare `python3`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_MODEL = "gemini-4-carbon-high"
REQUIRED_SKILLS = ("code-review", "setup-matt-pocock-skills")
SKILL_INSTALL_HINT = "npx skills add mattpocock/skills --skill={name}"

# agy cannot prompt for permission in headless mode: any command outside this
# list is auto-denied, and a single denial ends the whole turn with an empty
# response. Wildcards such as command(*) are rejected by agy itself, so the
# list is explicit. Every entry is read-only: `git branch` is spelled out per
# flag because the bare prefix would also allow `git branch -D`.
ALLOWED_COMMANDS = [
    "git diff",
    "git log",
    "git show",
    "git status",
    "git grep",
    "git blame",
    "git rev-parse",
    "git rev-list",
    "git merge-base",
    "git ls-files",
    "git ls-tree",
    "git cat-file",
    "git describe",
    "git shortlog",
    "git branch --show-current",
    "git branch --list",
    "git branch -a",
    "git branch -r",
]
ALLOWED_SUMMARY = "diff、log、show、status、grep、blame、rev-parse、rev-list、merge-base、ls-files、ls-tree、cat-file、describe、shortlog，以及 branch 的 --show-current / --list / -a / -r"

PROMPT = """/code-review {fixed}

补充输入与约束：
- 审查对象是**尚未提交**的改动：基准点 `{fixed}` 到当前工作区。不要用 `git diff {fixed}...HEAD`，它看不到未提交内容。已跟踪文件的改动用 `git diff {fixed}` 查看；新增文件用 `git ls-files --others --exclude-standard` 列出后直接读取，它们同样属于本次改动。
- 规格来源：{spec_line}
- 全程只读：不修改、不创建、不删除任何文件，不提交，不切换分支。
- 只做静态审查：可用的终端命令仅限 git 的这些只读子命令：{allowed}。其余一律用读文件和搜索工具，不要用 cat / grep / find / ls 等 shell 命令。不要运行类型检查、lint、测试、构建或任何 npm / npx / node / python 命令，这些由开发方负责；其他命令会被拒绝并导致整次审查作废。
- 无人值守：不要向用户提问；信息不足时写明你的假设后继续。
- 只报告问题，不写肯定性评语；某一类没有问题就写“无”。
- 用中文输出。最终回复只包含审查报告：`## Standards`（分“硬性违规”/“判断项”）、`## Spec`（分“a 缺失”/“b 多做”/“c 不一致”），每条给出文件路径与行号、依据（引用标准或规格原文）和问题说明；最后一行是单行总结。"""


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def find_skill(name: str, repo: Path) -> Path | None:
    roots = [
        repo / ".claude" / "skills",
        repo / ".agents" / "skills",
        Path.home() / ".claude" / "skills",
        Path.home() / ".agents" / "skills",
    ]
    for root in roots:
        candidate = root / name / "SKILL.md"
        if candidate.is_file():
            return candidate.resolve()
    return None


def find_agy() -> str | None:
    found = shutil.which("agy")
    if found:
        return found
    fallback = Path.home() / ".gemini" / "bin" / "agy"
    return str(fallback) if fallback.is_file() and os.access(fallback, os.X_OK) else None


def agy_models(agy: str) -> list[str] | None:
    """Model ids agy can use right now, or None when the call fails (not signed in, offline)."""
    try:
        out = subprocess.run(
            [agy, "models"], capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if out.returncode != 0:
        return None
    ids = [line.split("\t")[0].strip() for line in out.stdout.splitlines() if "\t" in line]
    return ids or None


def cmd_check(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    missing: list[str] = []
    report: dict[str, object] = {"skills": {}, "reviewer": {}}

    for name in REQUIRED_SKILLS:
        path = find_skill(name, repo)
        report["skills"][name] = str(path) if path else None  # type: ignore[index]
        if not path:
            missing.append(f"缺少 skill `{name}`。安装：{SKILL_INSTALL_HINT.format(name=name)}")

    agy = find_agy()
    report["reviewer"] = {"cli": "agy", "path": agy, "model": args.model}
    if not agy:
        hint = "未找到 Antigravity 命令行 `agy`（查过 PATH 和 ~/.gemini/bin/agy）。请安装并登录后重试。"
        if shutil.which("cursor-agent"):
            hint += " 检测到 `cursor-agent`，但本 skill 目前只适配并实测过 `agy`。"
        missing.append(hint)
    else:
        models = agy_models(agy)
        if models is None:
            missing.append("`agy models` 调用失败：可能未登录或网络不通。请在终端运行一次 `agy` 完成登录。")
        elif args.model not in models:
            missing.append(
                f"`agy` 没有模型 `{args.model}`。可用模型：{', '.join(models)}。用 --model 指定其一。"
            )

    report["ok"] = not missing
    report["missing"] = missing
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if missing:
        eprint("依赖检查未通过：")
        for item in missing:
            eprint(f"  - {item}")
        return 2
    return 0


def untracked(repo: Path) -> list[str]:
    out = git("ls-files", "--others", "--exclude-standard", "-z", cwd=repo)
    return [f for f in out.split("\0") if f]


def snapshot(repo: Path) -> dict[str, str]:
    """State the reviewer must not change. The changes under review are uncommitted,
    so `git status` alone is not enough: an already-modified file stays `M` even if
    the reviewer edits it again. Fingerprint the content as well."""
    digest = hashlib.sha256()
    digest.update(subprocess.run(["git", "diff", "HEAD", "--binary"], cwd=repo,
                                 capture_output=True, check=True).stdout)
    for name in untracked(repo):
        path = repo / name
        digest.update(name.encode() + b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
    return {
        "head": git("rev-parse", "HEAD", cwd=repo),
        "branch": git("branch", "--show-current", cwd=repo),
        "status": git("status", "--porcelain", cwd=repo),
        "content": digest.hexdigest(),
    }


def parse_stream(path: Path) -> dict[str, object]:
    """Pull the final result and any failed commands out of agy's stream-json output."""
    result: dict[str, object] | None = None
    failed: list[dict[str, str]] = []
    tools: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = event.get("event")
        if kind == "result":
            result = event.get("result") or {}
        elif kind == "step_update":
            step = event.get("step_update") or {}
            if step.get("step_type") != "tool" or step.get("state") not in ("DONE", "ERROR"):
                continue
            name = step.get("tool_name", "?")
            tools[name] = tools.get(name, 0) + 1
            info = step.get("tool_info") or {}
            if step.get("state") == "ERROR" and name == "run_command":
                failed.append(
                    {
                        "command": (info.get("parameters") or {}).get("CommandLine", ""),
                        "error": ((info.get("error") or {}).get("message") or "")[:300],
                    }
                )
    return {"result": result, "failed_commands": failed, "tools": tools}


def cmd_run(args: argparse.Namespace) -> int:
    repo = Path(git("rev-parse", "--show-toplevel")).resolve()

    agy = find_agy()
    if not agy:
        eprint("未找到 `agy`。先运行 `external_review.py check`。")
        return 2

    # --- preconditions -----------------------------------------------------
    try:
        git("rev-parse", "--verify", "--quiet", f"{args.base}^{{commit}}", cwd=repo)
    except subprocess.CalledProcessError:
        eprint(f"基准点 `{args.base}` 无法解析。")
        return 5
    before = snapshot(repo)
    fixed = git("merge-base", args.base, "HEAD", cwd=repo)
    if git("diff", "--stat", fixed, cwd=repo) == "" and not untracked(repo):
        eprint(f"相对 `{args.base}` 没有任何改动（已提交和未提交的都没有）。")
        return 5
    if args.spec:
        if not (repo / args.spec).exists() and not Path(args.spec).exists():
            eprint(f"规格文件不存在：{args.spec}")
            return 5
        spec_line = f"用户传入的路径 `{args.spec}`" + (f"（{args.spec_note}）" if args.spec_note else "")
    elif args.no_spec:
        spec_line = "无。按 code-review 的约定跳过 Spec 轴，并在报告的 `## Spec` 下注明“无规格，已跳过”。"
    else:
        eprint("必须给 --spec <路径>，或显式 --no-spec。无头模式下审查者无法向人询问规格在哪。")
        return 5

    # --- output location ---------------------------------------------------
    if args.out:
        out_dir = Path(args.out).resolve()
    else:
        git_path = Path(git("rev-parse", "--git-path", "dev-review-loop", cwd=repo))
        if not git_path.is_absolute():
            git_path = repo / git_path
        out_dir = git_path / re.sub(r"[^A-Za-z0-9._-]+", "-", before["branch"] or "detached")
    out_dir.mkdir(parents=True, exist_ok=True)
    round_no = args.round or (len(list(out_dir.glob("round-*.md"))) + 1)
    stream_path = out_dir / f"round-{round_no}.ndjson"
    err_path = out_dir / f"round-{round_no}.stderr.txt"
    report_path = out_dir / f"round-{round_no}.md"

    # --- run the reviewer --------------------------------------------------
    prompt = PROMPT.format(base=args.base, fixed=fixed, spec_line=spec_line, allowed=ALLOWED_SUMMARY)
    settings = {"permissions": {"allow": [f"command({c})" for c in ALLOWED_COMMANDS]}}
    command = [
        agy,
        "-p", prompt,
        "--settings", json.dumps(settings),
        "--mode", "plan",
        "--model", args.model,
        "--output-format", "stream-json",
        "--print-timeout", f"{args.timeout}s",
    ]
    started = time.time()
    try:
        with stream_path.open("w", encoding="utf-8") as out, err_path.open("w", encoding="utf-8") as err:
            proc = subprocess.run(
                command, cwd=repo, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                timeout=args.timeout + 120,
            )
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        exit_code = -1
    elapsed = round(time.time() - started, 1)

    # --- did the reviewer leave the worktree alone? ------------------------
    after = snapshot(repo)
    if after != before:
        eprint("审查者改动了 worktree，本轮结果作废。前后对比：")
        for key in before:
            if before[key] != after[key]:
                eprint(f"  {key}: {before[key]!r} -> {after[key]!r}")
        return 4

    # --- did the review actually complete? ---------------------------------
    # agy reports status SUCCESS and exit code 0 even when a denied command
    # ended the turn with no output, so neither can be trusted on its own.
    parsed = parse_stream(stream_path)
    result = parsed["result"] or {}
    response = (result.get("response") or "").strip()  # type: ignore[union-attr]
    denied = result.get("denied_actions") or []  # type: ignore[union-attr]
    problems: list[str] = []
    if exit_code != 0:
        problems.append("agy 超时" if exit_code == -1 else f"agy 退出码 {exit_code}")
    if not parsed["result"]:
        problems.append("输出里没有最终结果事件")
    if denied:
        problems.append(f"有操作被权限拒绝：{json.dumps(denied, ensure_ascii=False)}")
    if not response:
        problems.append("审查正文为空")
    elif "## Standards" not in response or "## Spec" not in response:
        problems.append("审查正文缺少 `## Standards` 或 `## Spec` 小节")
    if problems:
        eprint("审查没有完成，不能当作“零发现”：")
        for item in problems:
            eprint(f"  - {item}")
        for failed in parsed["failed_commands"]:  # type: ignore[union-attr]
            eprint(f"  被拒或失败的命令：{failed['command']}  ({failed['error']})")
        eprint(f"  原始输出：{stream_path}\n  stderr：{err_path}")
        return 3

    usage = result.get("usage") or {}  # type: ignore[union-attr]
    header = "\n".join(
        [
            f"<!-- dev-review-loop round {round_no}",
            f"reviewer: agy / {args.model}",
            f"conversation_id: {result.get('conversation_id')}",  # type: ignore[union-attr]
            f"base: {args.base} (fixed point {fixed})",
            f"head: {before['head']}",
            f"branch: {before['branch']}",
            f"spec: {args.spec or '(none)'}",
            f"duration_seconds: {elapsed}",
            f"total_tokens: {usage.get('total_tokens')}",
            f"tools: {json.dumps(parsed['tools'], ensure_ascii=False)}",
            "-->",
            "",
        ]
    )
    report_path.write_text(header + response + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "round": round_no,
                "report": str(report_path),
                "out_dir": str(out_dir),
                "head": before["head"],
                "model": args.model,
                "duration_seconds": elapsed,
                "total_tokens": usage.get("total_tokens"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="verify dependencies; exit 2 when something is missing")
    check.add_argument("--repo", default=".", help="repository to look for project-level skills in")
    check.add_argument("--model", default=DEFAULT_MODEL)
    check.set_defaults(func=cmd_check)

    run = sub.add_parser("run", help="run one review round in the current worktree")
    run.add_argument("--base", default="HEAD", help="fixed point; the review covers everything from its merge-base with HEAD to the working tree (default: HEAD, i.e. only uncommitted changes)")
    run.add_argument("--spec", help="path to the spec the change implements")
    run.add_argument("--spec-note", help="which part of the spec applies, e.g. '第三批 3c 一节'")
    run.add_argument("--no-spec", action="store_true", help="there is no spec; skip the Spec axis")
    run.add_argument("--model", default=DEFAULT_MODEL)
    run.add_argument("--round", type=int, help="round number (default: next free one)")
    run.add_argument("--out", help="output directory (default: inside .git, never tracked)")
    run.add_argument("--timeout", type=int, default=1800, help="seconds to wait for the reviewer")
    run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
