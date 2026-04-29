# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_note_comments.py —— 抓取小红书笔记评论（顶层 + 回复），每页 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_note_comments.py <note_id> [note_id2 ...] [--output-dir DIR] [--sort latest|normal] [--no-replies] [--no-upload]
# 示例：uv run get_note_comments.py 65bf5360000000002c03f684 --output-dir ./output
# 断点续爬：进度写入 .xhs_comments_progress.json，CSV 固定文件名追加；中断后再次运行同命令即可续传

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
TOP_ENDPOINT   = "/api/xiaohongshu/get-note-comment/v2"
SUB_ENDPOINT   = "/api/xiaohongshu/get-note-sub-comment/v2"
TIMEOUT        = 60
RETRY_MAX      = 3
RETRY_SLEEP    = 2.0
PAGE_SLEEP     = 0.5
NO_RETRY_CODES = {100, 303, 400, 600, 601}
_CST = timezone(timedelta(hours=8))

CSV_COLUMNS = [
    "note_id", "comment_id", "parent_comment_id", "root_comment_id", "is_sub",
    "content", "comment_type",
    "like_count", "sub_comment_count", "status",
    "user_id", "user_nickname", "user_red_id", "user_avatar",
    "target_comment_id", "target_user_id", "target_user_nickname",
    "ip_location",
    "comment_time", "comment_time_fmt",
    "pictures", "raw_data",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/xiaohongshu/note-comments/upsert"
UPLOAD_TIMEOUT = 30

UPLOAD_FIELDS = {
    "note_id", "comment_id", "parent_comment_id", "root_comment_id", "is_sub",
    "content", "comment_type", "pictures",
    "like_count", "sub_comment_count", "status",
    "user_id", "user_nickname", "user_avatar", "user_red_id",
    "target_comment_id", "target_user_id", "target_user_nickname",
    "ip_location",
    "comment_time", "raw_data",
}
INT_FIELDS = {"is_sub", "comment_type", "like_count", "sub_comment_count", "status"}

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

def _extract_cursor(raw) -> str:
    """接口返回的 data.cursor 是形如 '{"cursor":"xxx","index":2,...}' 的 JSON 字符串，
    实际请求 lastCursor 只需要内层那个 id。解析失败则原样返回。"""
    if not raw:
        return ""
    if isinstance(raw, dict):
        return raw.get("cursor", "") or ""
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("{"):
            try:
                return json.loads(s).get("cursor", "") or ""
            except Exception:
                return s
        return s
    return str(raw)

# ── 进度与去重 ────────────────────────────────────────────────
def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_seen(csv_file: Path) -> set:
    """从已存在 CSV 中加载 (note_id, comment_id) 复合键集合，用于跨次去重。"""
    if not (csv_file.exists() and csv_file.stat().st_size > 0):
        return set()
    seen = set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            nid, cid = r.get("note_id"), r.get("comment_id")
            if nid and cid:
                seen.add((nid, cid))
    return seen

# ── 上下文 ────────────────────────────────────────────────────
@dataclass
class Ctx:
    token: str
    sort: str
    include_replies: bool
    no_upload: bool
    writer: csv.DictWriter
    fp: object
    seen: set
    progress: dict
    pfile: Path
    trace_id: str
    failed_path: Path
    max_top: Optional[int] = None  # 顶层评论上限（达到后停止翻页）

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
            if code == 0:
                return body.get("data") or {}
            if code in NO_RETRY_CODES:
                print(f"  [error] 不可重试 code={code}")
                return None
            print(f"  [warn] code={code} (attempt {attempt})")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP)
    return None

def fetch_top_page(token, note_id, last_cursor: str, sort: str) -> Optional[dict]:
    params = {"noteId": note_id, "sort": sort}
    if last_cursor:
        params["lastCursor"] = last_cursor
    return _request(token, TOP_ENDPOINT, params)

def fetch_sub_page(token, note_id, comment_id, last_cursor: str) -> Optional[dict]:
    params = {"noteId": note_id, "commentId": comment_id}
    if last_cursor:
        params["lastCursor"] = last_cursor
    return _request(token, SUB_ENDPOINT, params)

# ── 数据转换 ──────────────────────────────────────────────────
def comment_to_row(c: dict, note_id: str, *,
                   is_sub: int,
                   parent_comment_id: Optional[str],
                   root_comment_id: str) -> dict:
    user        = c.get("user") or {}
    target      = c.get("target_comment") or {}
    target_user = target.get("user") or {}
    ts          = c.get("time")
    return {
        "note_id":              note_id,
        "comment_id":           c.get("id", ""),
        "parent_comment_id":    parent_comment_id or "",
        "root_comment_id":      root_comment_id,
        "is_sub":               is_sub,
        "content":              c.get("content", ""),
        "comment_type":         _safe_int(c.get("comment_type")),
        "like_count":           _safe_int(c.get("like_count")),
        "sub_comment_count":    _safe_int(c.get("sub_comment_count")) if not is_sub else None,
        "status":               _safe_int(c.get("status")),
        "user_id":              user.get("userid", ""),
        "user_nickname":        user.get("nickname", ""),
        "user_red_id":          user.get("red_id", ""),
        "user_avatar":          user.get("images", ""),
        "target_comment_id":    target.get("id", "") if is_sub else "",
        "target_user_id":       target_user.get("userid", "") if is_sub else "",
        "target_user_nickname": target_user.get("nickname", "") if is_sub else "",
        "ip_location":          c.get("ip_location", ""),
        "comment_time":         to_iso_cst(ts) if ts else "",
        "comment_time_fmt":     fmt_cst(ts) if ts else "",
        "pictures":             c.get("pictures") or [],
        "raw_data":             c,
    }

def row_to_upload(row: dict) -> dict:
    """row → 后端 schema：剔除空值/空容器，类型修正。"""
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
        out = {**r,
               "pictures": json.dumps(r.get("pictures") or [], ensure_ascii=False),
               "raw_data": json.dumps(r.get("raw_data") or {}, ensure_ascii=False)}
        writer.writerow(out)
    fp.flush()

# ── 后端上传 ──────────────────────────────────────────────────
def upload_to_backend(rows: list, trace_id: str, failed_path: Path) -> bool:
    """单页上传，失败则把整页落到 *_failed.jsonl，跳过继续。"""
    items = [row_to_upload(r) for r in rows]
    items = [it for it in items if it.get("note_id") and it.get("comment_id") and it.get("raw_data")]
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

# ── 写入与去重 ────────────────────────────────────────────────
def _persist(rows: list, ctx: Ctx) -> int:
    """对 rows 按 (note_id, comment_id) 去重 → 上传后端 → 写 CSV。返回新增条数。"""
    new = []
    for r in rows:
        key = (r["note_id"], r["comment_id"])
        if not key[1] or key in ctx.seen:
            continue
        ctx.seen.add(key)
        new.append(r)
    if not new:
        return 0
    if not ctx.no_upload:
        upload_to_backend(new, ctx.trace_id, ctx.failed_path)
    write_csv(new, ctx.fp, ctx.writer)
    return len(new)

# ── 单笔记抓取（支持断点续传）────────────────────────────────
def fetch_note(ctx: Ctx, note_id: str) -> bool:
    """抓取单个笔记的评论。成功完整返回 True，中途失败返回 False（进度已保存）。"""
    state       = ctx.progress.get(note_id, {})
    stage       = state.get("stage", "top")
    total       = state.get("total", 0)
    sub_targets = list(state.get("sub_targets", []))         # [[cid, expected_count], ...]
    tag         = note_id[:20]

    # ───── 阶段 1：顶层评论 ─────
    if stage == "top":
        cursor = _extract_cursor(state.get("top_cursor", ""))  # 兼容旧 progress 里的完整 JSON 字符串
        page   = state.get("top_page", 1)
        session_top = 0                                        # 本次运行新增的顶层数（与 progress 无关）
        if cursor:
            limit_msg = f"，本次上限 {ctx.max_top}" if ctx.max_top else ""
            print(f"\n[{tag}] 断点续传 顶层第{page}页 cursor={cursor[:30]}...{limit_msg}")
        else:
            limit_msg = f"（本次上限 {ctx.max_top}）" if ctx.max_top else ""
            print(f"\n[{tag}] 开始抓取顶层评论{limit_msg}")

        reached_limit = False
        while not reached_limit:
            data = fetch_top_page(ctx.token, note_id, cursor, ctx.sort)
            if data is None:
                print(f"[{tag}] 顶层第{page}页失败，已保存进度，下次续传")
                ctx.progress[note_id] = {
                    "stage": "top", "top_cursor": cursor, "top_page": page,
                    "total": total, "sub_targets": sub_targets,
                }
                save_progress(ctx.pfile, ctx.progress)
                return False
            comments = data.get("comments") or []
            if not comments:
                break

            rows = []
            for c in comments:
                cid = c.get("id", "")
                rows.append(comment_to_row(c, note_id, is_sub=0,
                                           parent_comment_id=None, root_comment_id=cid))
                for sc in c.get("sub_comments") or []:  # 内联子评论（一般为空，保险处理）
                    rows.append(comment_to_row(sc, note_id, is_sub=1,
                                               parent_comment_id=cid, root_comment_id=cid))
                if ctx.include_replies and (c.get("sub_comment_count") or 0) > 0:
                    sub_targets.append([cid, c.get("sub_comment_count")])
                session_top += 1
                if ctx.max_top and session_top >= ctx.max_top:
                    reached_limit = True
                    break

            added = _persist(rows, ctx)
            total += added
            print(f"[{tag}] 顶层第{page}页 评论{len(comments)}条 新增{added}条 累计{total}（本次顶层{session_top}）")

            page += 1
            has_more = data.get("has_more", False)
            next_cursor = _extract_cursor(data.get("cursor"))

            if reached_limit:
                # 达到本次上限：保留 top 阶段 + 下一页 cursor，下次再跑可继续翻新顶层
                print(f"[{tag}] 已达本次顶层上限 {ctx.max_top}，停止翻页（下次运行可继续）")
                if has_more and next_cursor:
                    ctx.progress[note_id] = {
                        "stage": "top", "top_cursor": next_cursor, "top_page": page,
                        "total": total, "sub_targets": sub_targets,
                    }
                    save_progress(ctx.pfile, ctx.progress)
                    return True
                break

            if has_more and next_cursor:
                cursor = next_cursor
                ctx.progress[note_id] = {
                    "stage": "top", "top_cursor": cursor, "top_page": page,
                    "total": total, "sub_targets": sub_targets,
                }
                save_progress(ctx.pfile, ctx.progress)
                time.sleep(PAGE_SLEEP)
            else:
                break

        # 顶层完成 → 切换到子评论阶段
        stage = "sub"
        ctx.progress[note_id] = {
            "stage": "sub", "total": total,
            "sub_targets": sub_targets, "sub_cursor": "", "sub_page": 1,
        }
        save_progress(ctx.pfile, ctx.progress)

    # ───── 阶段 2：子评论 ─────
    if stage == "sub" and ctx.include_replies and sub_targets:
        print(f"[{tag}] 待拉取 {len(sub_targets)} 条评论的回复")
        sub_cursor = _extract_cursor(state.get("sub_cursor", "")) if state.get("stage") == "sub" else ""
        sub_page   = state.get("sub_page", 1) if state.get("stage") == "sub" else 1

        while sub_targets:
            cid, expected = sub_targets[0]
            sub_total = 0
            while True:
                data = fetch_sub_page(ctx.token, note_id, cid, sub_cursor)
                if data is None:
                    print(f"[{tag}] 评论{cid} 子第{sub_page}页失败，已保存进度，下次续传")
                    ctx.progress[note_id] = {
                        "stage": "sub", "total": total, "sub_targets": sub_targets,
                        "sub_cursor": sub_cursor, "sub_page": sub_page,
                    }
                    save_progress(ctx.pfile, ctx.progress)
                    return False
                comments = data.get("comments") or []
                if not comments:
                    break

                rows = []
                for c in comments:
                    target = c.get("target_comment") or {}
                    parent_id = target.get("id") or cid
                    rows.append(comment_to_row(c, note_id, is_sub=1,
                                               parent_comment_id=parent_id,
                                               root_comment_id=cid))
                added = _persist(rows, ctx)
                sub_total += added
                total += added

                if not data.get("has_more"):
                    break
                sub_cursor = _extract_cursor(data.get("cursor"))
                if not sub_cursor:
                    break
                sub_page += 1
                ctx.progress[note_id] = {
                    "stage": "sub", "total": total, "sub_targets": sub_targets,
                    "sub_cursor": sub_cursor, "sub_page": sub_page,
                }
                save_progress(ctx.pfile, ctx.progress)
                time.sleep(PAGE_SLEEP)

            print(f"[{tag}] 评论{cid} 子评论新增{sub_total}条（预期{expected}）")
            sub_targets.pop(0)
            sub_cursor, sub_page = "", 1
            ctx.progress[note_id] = {
                "stage": "sub", "total": total, "sub_targets": sub_targets,
                "sub_cursor": "", "sub_page": 1,
            }
            save_progress(ctx.pfile, ctx.progress)

    # 完成：清理进度
    ctx.progress.pop(note_id, None)
    save_progress(ctx.pfile, ctx.progress)
    print(f"[{tag}] ✅ 完成 共{total}条")
    return True

# ── 主流程 ────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取小红书笔记评论（顶层 + 回复，支持断点续爬）")
    ap.add_argument("note_ids", nargs="+", help="小红书笔记 ID，可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--sort", choices=["latest", "normal"], default="latest",
                    help="顶层评论排序：latest（最新，默认）| normal（默认排序）")
    ap.add_argument("--no-replies", action="store_true",
                    help="只采集顶层评论，不拉取每条评论的回复")
    ap.add_argument("--no-upload", action="store_true",
                    help="只写本地 CSV，不调用后端 upsert 接口")
    ap.add_argument("--max-top", type=int, default=None,
                    help="本次运行最多新增的顶层评论数（与历史进度无关；达到后停止翻新顶层，但子评论仍会拉完）")
    args = ap.parse_args()

    token       = load_token()
    out_dir     = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file    = out_dir / "xhs_comments.csv"
    pfile       = out_dir / ".xhs_comments_progress.json"
    failed_path = out_dir / "xhs_comments_failed.jsonl"
    trace_id    = f"xhs_comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    progress    = load_progress(pfile)
    seen        = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(f"笔记数: {len(args.note_ids)}  排序: {args.sort}  输出: {csv_file}"
          f"{f' | 本次顶层上限: {args.max_top}' if args.max_top else ''}"
          f"{' | 回复: 关闭' if args.no_replies else ''}"
          f"{' | 上传: 关闭' if args.no_upload else ''}")
    if progress:
        in_prog = [nid for nid in args.note_ids if nid in progress]
        if in_prog:
            print(f"检测到 {len(in_prog)} 个未完成笔记，将从断点续传")
    if seen:
        print(f"已存在 CSV {len(seen)} 条评论记录，将自动去重")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            token=token, sort=args.sort,
            include_replies=not args.no_replies, no_upload=args.no_upload,
            writer=writer, fp=f, seen=seen,
            progress=progress, pfile=pfile,
            trace_id=trace_id, failed_path=failed_path,
            max_top=args.max_top,
        )

        for nid in args.note_ids:
            try:
                fetch_note(ctx, nid)
            except KeyboardInterrupt:
                print(f"\n⚠️ 已中断，进度已保存到 {pfile}，下次同命令续传")
                sys.exit(130)
            except Exception as e:
                print(f"[error] 笔记 {nid} 异常: {e}（进度保留，下次续传）")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()
