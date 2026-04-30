# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_user_posts.py —— 抓取 Instagram 用户发布的帖子，每页先 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_user_posts.py <username> [username2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]
# 示例：uv run get_user_posts.py nasa natgeo --output-dir ./output --since 2025-01-01

import argparse, csv, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
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
API_URL     = "https://api.justoneapi.com/api/instagram/get-user-posts/v1"
TIMEOUT     = 60
RETRY_MAX   = 3
RETRY_SLEEP = 2.0
PAGE_SLEEP  = 0.5
_CST = timezone(timedelta(hours=8))

CSV_COLUMNS = [
    "username", "code", "media_id", "media_type", "product_type",
    "caption", "taken_at", "taken_at_fmt",
    "like_count", "comment_count", "play_count", "view_count",
    "owner_id", "owner_username", "owner_full_name",
    "thumbnail_url", "video_url", "raw_json",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/ig/posts/upsert"
UPLOAD_TIMEOUT = 30

# CSV 列名 → 后端 schema 字段名（含义相同）
UPLOAD_FIELD_MAP = {
    "username":        "username",
    "code":            "code",
    "media_id":        "media_id",
    "media_type":      "media_type",
    "product_type":    "product_type",
    "caption":         "caption",
    "taken_at":        "taken_at",
    "taken_at_fmt":    "taken_at_fmt",
    "like_count":      "like_count",
    "comment_count":   "comment_count",
    "play_count":      "play_count",
    "view_count":      "view_count",
    "owner_id":        "owner_id",
    "owner_username":  "owner_username",
    "owner_full_name": "owner_full_name",
    "thumbnail_url":   "thumbnail_url",
    "video_url":       "video_url",
    "raw_json":        "raw_data",
}
INT_FIELDS = {"media_type", "taken_at", "like_count", "comment_count", "play_count", "view_count"}

# ── 工具函数 ──────────────────────────────────────────────────
def fmt_cst(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""

def _safe_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def _code_eq(code, target: int) -> bool:
    """JustOneAPI 各接口 code 有时是 int 有时是 str，统一比较。"""
    try:
        return int(code) == target
    except (TypeError, ValueError):
        return str(code) == str(target)

def _pick(d: dict, *keys, default=None):
    """从 dict 中按候选键名顺序取第一个非空值。"""
    for k in keys:
        if d is None:
            break
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return default

def _extract_caption(post: dict) -> str:
    cap = post.get("caption")
    if isinstance(cap, dict):
        return cap.get("text", "") or ""
    if isinstance(cap, str):
        return cap
    return ""

def _extract_thumb(post: dict) -> str:
    """兼容 thumbnail_url / display_url / image_versions2.candidates[0].url。"""
    v = _pick(post, "thumbnail_url", "display_url", "image_url")
    if v:
        return v
    iv = post.get("image_versions2") or {}
    cands = iv.get("candidates") if isinstance(iv, dict) else None
    if cands and isinstance(cands, list):
        return (cands[0] or {}).get("url", "") or ""
    iv2 = post.get("image_versions") or {}
    items = iv2.get("items") if isinstance(iv2, dict) else None
    if items and isinstance(items, list):
        return (items[0] or {}).get("url", "") or ""
    return ""

def _extract_video(post: dict) -> str:
    v = _pick(post, "video_url")
    if v:
        return v
    vs = post.get("video_versions")
    if isinstance(vs, list) and vs:
        return (vs[0] or {}).get("url", "") or ""
    return ""

def to_upload_item(row: dict) -> dict:
    """CSV 行 → 后端 schema item：字段映射 + 类型转换 + 空值剔除。"""
    out = {}
    for src, dst in UPLOAD_FIELD_MAP.items():
        v = row.get(src)
        if v in ("", None):
            continue
        if dst in INT_FIELDS:
            v = _safe_int(v)
            if v is None:
                continue
        out[dst] = v
    return out

def load_seen(csv_file: Path) -> set:
    if not (csv_file.exists() and csv_file.stat().st_size > 0):
        return set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        return {r["code"] for r in csv.DictReader(f) if r.get("code")}

def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── API 调用 ──────────────────────────────────────────────────
def fetch_page(token: str, username: str, pagination_token: str = "") -> Optional[dict]:
    params = {"token": token, "username": username}
    if pagination_token:
        params["paginationToken"] = pagination_token
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(API_URL, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            if _code_eq(body.get("code"), 0):
                return body.get("data") or {}
            code = body.get("code")
            if _code_eq(code, 301) and attempt < RETRY_MAX:
                time.sleep(RETRY_SLEEP)
                continue
            print(f"  [warn] code={code} (attempt {attempt})")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP)
    return None

# ── 上下文 ────────────────────────────────────────────────────
@dataclass
class Ctx:
    token: str
    since_ts: Optional[int]
    max_pages: Optional[int]
    writer: csv.DictWriter
    fp: object
    csv_lock: threading.Lock
    seen_codes: set
    progress: dict
    pfile: Path
    prog_lock: threading.Lock
    trace_id: str
    failed_path: Path
    failed_lock: threading.Lock

# ── 后端上传 ──────────────────────────────────────────────────
def upload_to_backend(rows: list, ctx: Ctx) -> bool:
    """单页上传，失败则把整页落到 *_failed.jsonl，跳过继续。"""
    items = [to_upload_item(r) for r in rows]
    items = [it for it in items if it.get("code") and it.get("username")]
    if not items:
        return True
    try:
        resp = requests.post(
            BACKEND_URL,
            json={"trace_id": ctx.trace_id, "items": items},
            timeout=UPLOAD_TIMEOUT,
        )
        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if resp.status_code == 200 and body.get("code") == 0:
            print(f"  ↑ 上传到后端 {body.get('data', {}).get('count', 0)} 条")
            return True
        print(f"  ⚠️ 上传到后端失败 HTTP={resp.status_code} body={body}")
    except Exception as e:
        print(f"  ⚠️ 上传到后端异常: {e}")

    with ctx.failed_lock, open(ctx.failed_path, "a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, default=str) + "\n")
    return False

# ── 单用户抓取 ────────────────────────────────────────────────
def fetch_user(ctx: Ctx, username: str) -> bool:
    with ctx.prog_lock:
        state = ctx.progress.get(username, {})
    cursor = state.get("cursor", "")
    page   = state.get("page", 1)
    total  = state.get("total", 0)
    tag    = username[:24]
    if cursor:
        print(f"[{tag}] 断点续传 第{page}页")
    else:
        print(f"[{tag}] 开始抓取")

    session_pages = 0
    while True:
        data = fetch_page(ctx.token, username, cursor)
        if data is None:
            print(f"[{tag}] 请求失败，中止（下次续传）")
            return False
        # IG 实际响应是 body.data.data.items，多包了一层
        inner = data.get("data") if isinstance(data.get("data"), dict) else data
        posts = _pick(inner, "items", "posts", default=[]) or []
        if not posts:
            print(f"[{tag}] 无更多数据，完成")
            break

        rows, hit_cutoff = [], False
        for post in posts:
            ts = _safe_int(_pick(post, "taken_at", "device_timestamp", "created_at"))
            if ctx.since_ts and ts and ts < ctx.since_ts:
                hit_cutoff = True
                continue
            user = post.get("user") or post.get("owner") or {}
            code = _pick(post, "code", "shortcode", "short_code") or ""
            mid  = _pick(post, "media_id", "pk", "id")
            if isinstance(mid, str) and "_" in mid:
                mid = mid.split("_", 1)[0]   # "3123_1234567" → "3123"
            rows.append({
                "username": username,
                "code": code,
                "media_id": str(mid) if mid is not None else "",
                "media_type": _safe_int(post.get("media_type")),
                "product_type": post.get("product_type", "") or "",
                "caption": _extract_caption(post),
                "taken_at": ts if ts is not None else "",
                "taken_at_fmt": fmt_cst(ts) if ts else "",
                "like_count": _safe_int(_pick(post, "like_count", "likes")),
                "comment_count": _safe_int(_pick(post, "comment_count", "comments_count")),
                "play_count": _safe_int(post.get("play_count")),
                "view_count": _safe_int(_pick(post, "view_count", "ig_play_count", "play_count")),
                "owner_id": str(_pick(user, "pk", "id", "userid") or ""),
                "owner_username": _pick(user, "username") or "",
                "owner_full_name": _pick(user, "full_name", "fullname") or "",
                "thumbnail_url": _extract_thumb(post),
                "video_url": _extract_video(post),
                "raw_json": post,  # 内存中保留 dict，写 CSV 时再 dumps
            })

        # pagination_token 通常在外层 data 上；兼容内层放置
        next_cursor = (_pick(data, "pagination_token", "next_pagination_token", "next_max_id", "next_min_id")
                       or _pick(inner, "pagination_token", "next_pagination_token")
                       or "")
        more = data.get("more_available")
        has_more = bool(next_cursor) if more is None else bool(more)

        # 1) 锁内：去重，标记已见
        with ctx.csv_lock:
            new = [r for r in rows if r["code"] and r["code"] not in ctx.seen_codes]
            for r in new:
                ctx.seen_codes.add(r["code"])

        # 2) 锁外：先上传，再写 CSV
        if new:
            upload_to_backend(new, ctx)
            with ctx.csv_lock:
                for r in new:
                    csv_row = {**r, "raw_json": json.dumps(r["raw_json"], ensure_ascii=False)}
                    ctx.writer.writerow(csv_row)
                ctx.fp.flush()

        total += len(new)
        print(f"[{tag}] 第{page}页 新增{len(new)}条 累计{total}条")

        page += 1
        session_pages += 1
        with ctx.prog_lock:
            if has_more and next_cursor and not hit_cutoff:
                ctx.progress[username] = {"cursor": next_cursor, "page": page, "total": total}
            else:
                ctx.progress.pop(username, None)
            save_progress(ctx.pfile, ctx.progress)

        if hit_cutoff or not has_more or not next_cursor:
            break
        if ctx.max_pages and session_pages >= ctx.max_pages:
            print(f"[{tag}] 已达本次上限 {ctx.max_pages} 页，停止（下次运行可继续）")
            return True
        cursor = next_cursor
        time.sleep(PAGE_SLEEP)

    print(f"[{tag}] 完成 共{total}条")
    return True

# ── 主流程 ─────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取 Instagram 用户发布的帖子")
    ap.add_argument("usernames", nargs="+", help="Instagram 用户名（不带 @），可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--since", help="只采集此日期之后的帖子，格式 YYYY-MM-DD（CST）")
    ap.add_argument("--workers", type=int, default=3, help="并发线程数（默认 3）")
    ap.add_argument("--max-pages", type=int, default=None,
                    help="本次运行每个用户最多翻页数（不传则翻完）")
    args = ap.parse_args()

    token = load_token()
    since_ts = None
    if args.since:
        d = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=_CST)
        since_ts = int(d.timestamp())

    out_dir  = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file    = out_dir / "ig_posts.csv"
    pfile       = out_dir / ".ig_posts_progress.json"
    failed_path = out_dir / "ig_posts_failed.jsonl"
    trace_id    = f"ig_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    progress    = load_progress(pfile)
    seen_codes  = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(f"用户数: {len(args.usernames)}  并发: {args.workers}  输出: {csv_file}")
    if since_ts:
        print(f"只采集 {args.since} 之后的帖子")
    if args.max_pages:
        print(f"本次每用户最多翻 {args.max_pages} 页")
    if seen_codes:
        print(f"已存在 CSV {len(seen_codes)} 条记录，将自动去重")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            token=token, since_ts=since_ts, max_pages=args.max_pages,
            writer=writer, fp=f,
            csv_lock=threading.Lock(), seen_codes=seen_codes,
            progress=progress, pfile=pfile, prog_lock=threading.Lock(),
            trace_id=trace_id, failed_path=failed_path, failed_lock=threading.Lock(),
        )

        def run(name: str):
            ok = fetch_user(ctx, name)
            if ok:
                with ctx.prog_lock:
                    if name in ctx.progress and not ctx.progress[name].get("cursor"):
                        ctx.progress.pop(name, None)
                        save_progress(ctx.pfile, ctx.progress)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for fut in as_completed({pool.submit(run, n): n for n in args.usernames}):
                if fut.exception():
                    print(f"[error] {fut.exception()}")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()

