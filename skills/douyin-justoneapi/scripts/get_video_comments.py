# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_video_comments.py —— 抓取抖音视频评论（顶层 + 回复），每页 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_video_comments.py <aweme_id> [aweme_id2 ...] [--output-dir DIR] [--max-top N] [--no-replies]
# 示例：uv run get_video_comments.py 7300000000000000000 --output-dir ./output
# 断点续爬：进度写入 .douyin_video_comments_progress.json，CSV 固定文件名追加；中断后再次运行同命令即可续传

import argparse, csv, json, os, sys, time
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests

# ── Token ─────────────────────────────────────────────────────
def load_token():
    for d in [Path.cwd(), *Path.cwd().parents]:
        p = d / ".env"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                for k in ("JUSTONEAPI_TOKEN", "JUST_ONE_API_TOKEN"):
                    if line.startswith(f"{k}=") and (v := line.split("=", 1)[1].strip()):
                        return v
    v = os.environ.get("JUSTONEAPI_TOKEN") or os.environ.get("JUST_ONE_API_TOKEN")
    if v:
        return v
    sys.exit("❌ 未找到 JustOneAPI Token，请在 .env 中配置：\n  JUSTONEAPI_TOKEN=your_token")

# ── 常量 ──────────────────────────────────────────────────────
BASE_URL       = "https://api.justoneapi.com"
TOP_ENDPOINT   = "/api/douyin/get-video-comment/v1"
SUB_ENDPOINT   = "/api/douyin/get-video-sub-comment/v1"
TIMEOUT        = 60
RETRY_MAX      = 3
RETRY_SLEEP    = 2.0
PAGE_SLEEP     = 0.5
NO_RETRY_CODES = {100, 303, 400, 600, 601}
_CST = timezone(timedelta(hours=8))

CSV_COLUMNS = [
    "aweme_id", "comment_id", "parent_comment_id", "root_comment_id", "is_sub",
    "content", "digg_count", "reply_count", "ip_label",
    "user_uid", "user_sec_uid", "user_short_id", "user_nickname", "user_avatar",
    "comment_time", "comment_time_fmt", "raw_data",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/douyin/video-comments/upsert"
UPLOAD_TIMEOUT = 30

UPLOAD_FIELDS = {
    "aweme_id", "comment_id", "parent_comment_id", "root_comment_id", "is_sub",
    "content", "digg_count", "reply_count", "ip_label",
    "user_uid", "user_sec_uid", "user_short_id", "user_nickname", "user_avatar",
    "comment_time", "raw_data",
}
INT_FIELDS = {"is_sub", "digg_count", "reply_count"}

# ── 工具函数 ──────────────────────────────────────────────────
def fmt_cst(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""

def to_iso_cst(ts) -> Optional[str]:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).isoformat()
    except Exception:
        return None

def _safe_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def _code_eq(code, target: int) -> bool:
    try:
        return int(code) == target
    except (TypeError, ValueError):
        return str(code) == str(target)

def _pick(d, *keys, default=None):
    for k in keys:
        if d is None:
            break
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return default

def _first_url(node) -> str:
    if not isinstance(node, dict):
        return ""
    urls = node.get("url_list") or node.get("urlList") or []
    if isinstance(urls, list) and urls:
        return urls[0] or ""
    return node.get("url", "") or ""

# ── 进度与去重 ────────────────────────────────────────────────
def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_seen(csv_file: Path) -> set:
    """从已存在 CSV 中加载 (aweme_id, comment_id) 复合键集合，用于跨次去重。"""
    if not (csv_file.exists() and csv_file.stat().st_size > 0):
        return set()
    seen = set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            aid, cid = r.get("aweme_id"), r.get("comment_id")
            if aid and cid:
                seen.add((aid, cid))
    return seen

# ── 上下文 ────────────────────────────────────────────────────
@dataclass
class Ctx:
    token: str
    include_replies: bool
    writer: csv.DictWriter
    fp: object
    seen: set
    progress: dict
    pfile: Path
    trace_id: str
    failed_path: Path
    max_top: Optional[int] = None

# ── API 调用 ──────────────────────────────────────────────────
def _request(token: str, endpoint: str, params: dict) -> Optional[dict]:
    """通用单次请求 + 重试。成功返回 data，失败返回 None。"""
    p = {"token": token, **params}
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(f"{BASE_URL}{endpoint}", params=p, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            code = body.get("code")
            if _code_eq(code, 0):
                return body.get("data") or {}
            if any(_code_eq(code, c) for c in NO_RETRY_CODES):
                print(f"  [error] 不可重试 code={code}")
                return None
            print(f"  [warn] code={code} (attempt {attempt})")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP)
    return None

def fetch_top_page(token, aweme_id: str, page: int) -> Optional[dict]:
    return _request(token, TOP_ENDPOINT, {"awemeId": aweme_id, "page": page})

def fetch_sub_page(token, comment_id: str, page: int) -> Optional[dict]:
    return _request(token, SUB_ENDPOINT, {"commentId": comment_id, "page": page})

# ── 数据转换 ──────────────────────────────────────────────────
def comment_to_row(c: dict, aweme_id: str, *,
                   is_sub: int,
                   parent_comment_id: Optional[str],
                   root_comment_id: str) -> dict:
    user = c.get("user") or {}
    ts   = _safe_int(_pick(c, "create_time", "createTime"))
    cid  = str(_pick(c, "cid", "comment_id", "id") or "")
    return {
        "aweme_id":           aweme_id or str(_pick(c, "aweme_id", "awemeId") or ""),
        "comment_id":         cid,
        "parent_comment_id":  parent_comment_id or "",
        "root_comment_id":    root_comment_id,
        "is_sub":             is_sub,
        "content":            _pick(c, "text", "content") or "",
        "digg_count":         _safe_int(_pick(c, "digg_count", "like_count")),
        "reply_count":        _safe_int(_pick(c, "reply_comment_total", "reply_count", "sub_comment_count")) if not is_sub else None,
        "ip_label":           _pick(c, "ip_label", "ipLabel") or "",
        "user_uid":           str(_pick(user, "uid", "id") or ""),
        "user_sec_uid":       _pick(user, "sec_uid", "secUid") or "",
        "user_short_id":      str(_pick(user, "short_id", "unique_id") or ""),
        "user_nickname":      _pick(user, "nickname", "name") or "",
        "user_avatar":        _first_url(_pick(user, "avatar_thumb", "avatar_larger", "avatar_medium", default={})),
        "comment_time":       to_iso_cst(ts) if ts else "",
        "comment_time_fmt":   fmt_cst(ts) if ts else "",
        "raw_data":           c,
    }

def row_to_upload(row: dict) -> dict:
    """row → 后端 schema：剔除空值，类型修正。"""
    out = {}
    for k in UPLOAD_FIELDS:
        v = row.get(k)
        if v in ("", None):
            continue
        if isinstance(v, (list, dict)) and not v and k != "raw_data":
            continue
        if k in INT_FIELDS:
            v = _safe_int(v)
            if v is None:
                continue
        out[k] = v
    return out

def write_csv(rows: list, fp, writer):
    for r in rows:
        out = {**r, "raw_data": json.dumps(r.get("raw_data") or {}, ensure_ascii=False)}
        writer.writerow(out)
    fp.flush()

# ── 后端上传 ──────────────────────────────────────────────────
def upload_to_backend(rows: list, trace_id: str, failed_path: Path) -> bool:
    items = [row_to_upload(r) for r in rows]
    items = [it for it in items
             if it.get("aweme_id") and it.get("comment_id")
             and it.get("root_comment_id") and it.get("raw_data")]
    if not items:
        return True
    try:
        resp = requests.post(BACKEND_URL,
                             json={"trace_id": trace_id, "items": items},
                             timeout=UPLOAD_TIMEOUT)
        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if resp.status_code == 200 and body.get("code") == 0:
            print(f"    ↑ 上传 {body.get('data', {}).get('count', 0)} 条")
            return True
        print(f"    ⚠️ 上传失败 HTTP={resp.status_code} body={body}")
    except Exception as e:
        print(f"    ⚠️ 上传异常: {e}")
    with open(failed_path, "a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, default=str) + "\n")
    return False

def _persist(rows: list, ctx: Ctx) -> int:
    """对 rows 按 (aweme_id, comment_id) 去重 → 上传后端 → 写 CSV。返回新增条数。"""
    new = []
    for r in rows:
        key = (r["aweme_id"], r["comment_id"])
        if not key[1] or key in ctx.seen:
            continue
        ctx.seen.add(key)
        new.append(r)
    if not new:
        return 0
    upload_to_backend(new, ctx.trace_id, ctx.failed_path)
    write_csv(new, ctx.fp, ctx.writer)
    return len(new)

# ── 单视频抓取（支持断点续传）────────────────────────────────
def fetch_video(ctx: Ctx, aweme_id: str) -> bool:
    """抓取单个视频的评论。成功完整返回 True，中途失败返回 False（进度已保存）。"""
    state       = ctx.progress.get(aweme_id, {})
    stage       = state.get("stage", "top")
    total       = state.get("total", 0)
    sub_targets = list(state.get("sub_targets", []))         # [[cid, expected_count], ...]
    tag         = aweme_id[:24]

    # ───── 阶段 1：顶层评论 ─────
    if stage == "top":
        page = state.get("top_page", 1)
        session_top = 0
        if page > 1:
            limit_msg = f"，本次上限 {ctx.max_top}" if ctx.max_top else ""
            print(f"\n[{tag}] 断点续传 顶层第{page}页{limit_msg}")
        else:
            limit_msg = f"（本次上限 {ctx.max_top}）" if ctx.max_top else ""
            print(f"\n[{tag}] 开始抓取顶层评论{limit_msg}")

        reached_limit = False
        while not reached_limit:
            data = fetch_top_page(ctx.token, aweme_id, page)
            if data is None:
                print(f"[{tag}] 顶层第{page}页失败，已保存进度，下次续传")
                ctx.progress[aweme_id] = {
                    "stage": "top", "top_page": page,
                    "total": total, "sub_targets": sub_targets,
                }
                save_progress(ctx.pfile, ctx.progress)
                return False
            comments = data.get("comments") or []
            if not comments:
                break

            rows = []
            for c in comments:
                cid = str(_pick(c, "cid", "comment_id", "id") or "")
                if not cid:
                    continue
                rows.append(comment_to_row(c, aweme_id, is_sub=0,
                                           parent_comment_id=None, root_comment_id=cid))
                child_cnt = _safe_int(_pick(c, "reply_comment_total", "reply_count", "sub_comment_count")) or 0
                if ctx.include_replies and child_cnt > 0:
                    sub_targets.append([cid, child_cnt])
                session_top += 1
                if ctx.max_top and session_top >= ctx.max_top:
                    reached_limit = True
                    break

            added = _persist(rows, ctx)
            total += added
            print(f"[{tag}] 顶层第{page}页 评论{len(comments)}条 新增{added}条 累计{total}（本次顶层{session_top}）")

            page += 1
            has_more = bool(_safe_int(data.get("has_more")) or 0) if isinstance(data.get("has_more"), (int, str)) else bool(data.get("has_more"))

            if reached_limit:
                print(f"[{tag}] 已达本次顶层上限 {ctx.max_top}，停止翻页（下次运行可继续）")
                if has_more:
                    ctx.progress[aweme_id] = {
                        "stage": "top", "top_page": page,
                        "total": total, "sub_targets": sub_targets,
                    }
                    save_progress(ctx.pfile, ctx.progress)
                    return True
                break

            if has_more:
                ctx.progress[aweme_id] = {
                    "stage": "top", "top_page": page,
                    "total": total, "sub_targets": sub_targets,
                }
                save_progress(ctx.pfile, ctx.progress)
                time.sleep(PAGE_SLEEP)
            else:
                break

        # 顶层完成 → 切换到子评论阶段
        stage = "sub"
        ctx.progress[aweme_id] = {
            "stage": "sub", "total": total,
            "sub_targets": sub_targets, "sub_page": 1,
        }
        save_progress(ctx.pfile, ctx.progress)

    # ───── 阶段 2：子评论 ─────
    if stage == "sub" and ctx.include_replies and sub_targets:
        print(f"[{tag}] 待拉取 {len(sub_targets)} 条评论的回复")
        sub_page = state.get("sub_page", 1) if state.get("stage") == "sub" else 1

        while sub_targets:
            cid, expected = sub_targets[0]
            sub_total = 0
            while True:
                data = fetch_sub_page(ctx.token, cid, sub_page)
                if data is None:
                    print(f"[{tag}] 评论{cid} 子第{sub_page}页失败，已保存进度，下次续传")
                    ctx.progress[aweme_id] = {
                        "stage": "sub", "total": total,
                        "sub_targets": sub_targets, "sub_page": sub_page,
                    }
                    save_progress(ctx.pfile, ctx.progress)
                    return False
                comments = data.get("comments") or []
                if not comments:
                    break

                rows = []
                for c in comments:
                    parent_raw = str(_pick(c, "reply_to_reply_id", "parent_comment_id") or "")
                    parent_id = parent_raw if parent_raw and parent_raw != "0" else cid
                    rows.append(comment_to_row(c, aweme_id, is_sub=1,
                                               parent_comment_id=parent_id,
                                               root_comment_id=cid))
                added = _persist(rows, ctx)
                sub_total += added
                total += added

                has_more = bool(_safe_int(data.get("has_more")) or 0) if isinstance(data.get("has_more"), (int, str)) else bool(data.get("has_more"))
                if not has_more:
                    break
                sub_page += 1
                ctx.progress[aweme_id] = {
                    "stage": "sub", "total": total,
                    "sub_targets": sub_targets, "sub_page": sub_page,
                }
                save_progress(ctx.pfile, ctx.progress)
                time.sleep(PAGE_SLEEP)

            print(f"[{tag}] 评论{cid} 子评论新增{sub_total}条（预期{expected}）")
            sub_targets.pop(0)
            sub_page = 1
            ctx.progress[aweme_id] = {
                "stage": "sub", "total": total,
                "sub_targets": sub_targets, "sub_page": 1,
            }
            save_progress(ctx.pfile, ctx.progress)

    # 完成：清理进度
    ctx.progress.pop(aweme_id, None)
    save_progress(ctx.pfile, ctx.progress)
    print(f"[{tag}] ✅ 完成 共{total}条")
    return True

# ── 主流程 ────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取抖音视频评论（顶层 + 回复，支持断点续爬）")
    ap.add_argument("aweme_ids", nargs="+", help="抖音视频 aweme_id，可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--no-replies", action="store_true",
                    help="只采集顶层评论，不拉取每条评论的回复")
    ap.add_argument("--max-top", type=int, default=None,
                    help="本次运行最多新增的顶层评论数（达到后停止翻新顶层；子评论仍会拉完）")
    args = ap.parse_args()

    token       = load_token()
    out_dir     = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file    = out_dir / "douyin_video_comments.csv"
    pfile       = out_dir / ".douyin_video_comments_progress.json"
    failed_path = out_dir / "douyin_video_comments_failed.jsonl"
    trace_id    = f"douyin_video_comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    progress    = load_progress(pfile)
    seen        = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(f"视频数: {len(args.aweme_ids)}  输出: {csv_file}"
          f"{f' | 本次顶层上限: {args.max_top}' if args.max_top else ''}"
          f"{' | 回复: 关闭' if args.no_replies else ''}")
    if progress:
        in_prog = [aid for aid in args.aweme_ids if aid in progress]
        if in_prog:
            print(f"检测到 {len(in_prog)} 个未完成视频，将从断点续传")
    if seen:
        print(f"已存在 CSV {len(seen)} 条评论记录，将自动去重")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            token=token,
            include_replies=not args.no_replies,
            writer=writer, fp=f, seen=seen,
            progress=progress, pfile=pfile,
            trace_id=trace_id, failed_path=failed_path,
            max_top=args.max_top,
        )

        for aid in args.aweme_ids:
            try:
                fetch_video(ctx, aid)
            except KeyboardInterrupt:
                print(f"\n⚠️ 已中断，进度已保存到 {pfile}，下次同命令续传")
                sys.exit(130)
            except Exception as e:
                print(f"[error] 视频 {aid} 异常: {e}（进度保留，下次续传）")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()
