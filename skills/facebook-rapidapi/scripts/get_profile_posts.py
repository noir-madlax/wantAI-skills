# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_profile_posts.py —— 抓取 Facebook 主页帖子，每页先 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_profile_posts.py <profile_id> [profile_id2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]
# 示例：uv run get_profile_posts.py 100078792651602 --output-dir ./output --since 2025-01-01

import argparse, csv, json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import requests

# ── RapidAPI Key ──────────────────────────────────────────────
def load_rapidapi_key():
    for d in [Path.cwd(), *Path.cwd().parents]:
        p = d / ".env"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                for k in ("RAPIDAPI_API_KEY",):
                    if line.startswith(f"{k}=") and (v := line.split("=", 1)[1].strip()):
                        return v
    v = os.environ.get("RAPIDAPI_KEY") or os.environ.get("RAPIDAPI_API_KEY")
    if v:
        return v
    sys.exit("❌ 未找到 RapidAPI Key，请在 .env 中配置：\n  RAPIDAPI_KEY=your_rapidapi_key")

# ── 常量 ──────────────────────────────────────────────────────
API_URL     = "https://facebook-scraper3.p.rapidapi.com/profile/posts"
API_HOST    = "facebook-scraper3.p.rapidapi.com"
TIMEOUT     = 60
RETRY_MAX   = 5
RETRY_SLEEP = 1.0
PAGE_SLEEP  = 0.1
_CST = timezone(timedelta(hours=8))
HASHTAG_RE = re.compile(r"#[\w\u4e00-\u9fff]+")

CSV_COLUMNS = [
    # 基础
    "profile_id", "post_id", "type", "url",
    "timestamp", "timestamp_fmt",
    "message", "message_rich", "hashtags",
    # 互动
    "reactions_count", "comments_count", "reshare_count",
    "reaction_like", "reaction_love", "reaction_care",
    "reaction_haha", "reaction_wow", "reaction_sad", "reaction_angry",
    # 作者
    "author_id", "author_name", "author_url",
    # 媒体
    "image_uri", "image_id",
    "video_url", "video_sd_file", "video_hd_file", "video_thumbnail",
    # 原始
    "raw_json",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/fb/posts/upsert"
UPLOAD_TIMEOUT = 30

# CSV 列名 → 后端 schema 字段名（除 raw_json → raw_data 外完全一致）
UPLOAD_FIELD_MAP = {c: c for c in CSV_COLUMNS if c != "raw_json"}
UPLOAD_FIELD_MAP["raw_json"] = "raw_data"

INT_FIELDS = {
    "timestamp",
    "reactions_count", "comments_count", "reshare_count",
    "reaction_like", "reaction_love", "reaction_care",
    "reaction_haha", "reaction_wow", "reaction_sad", "reaction_angry",
}

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
    # raw_data 是后端必填，缺失则整条丢弃
    if "raw_data" not in out:
        return {}
    return out

def load_seen(csv_file: Path) -> set:
    if not (csv_file.exists() and csv_file.stat().st_size > 0):
        return set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        return {r["post_id"] for r in csv.DictReader(f) if r.get("post_id")}

def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── API 调用 ──────────────────────────────────────────────────
def fetch_page(rapidapi_key: str, profile_id: str, cursor: str = "") -> Optional[dict]:
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": rapidapi_key,
    }
    params = {"profile_id": profile_id}
    if cursor:
        params["cursor"] = cursor

    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(API_URL, headers=headers, params=params, timeout=TIMEOUT)
            if r.status_code in (401, 403):
                print(f"  [error] HTTP {r.status_code}：RapidAPI 鉴权失败，请检查 RAPIDAPI_KEY")
                return None
            if r.status_code == 429:
                print(f"  [warn] HTTP 429 速率限制 (attempt {attempt})")
            else:
                r.raise_for_status()
                body = r.json()
                if "results" in body:
                    return body
                print(f"  [warn] 响应缺少 results 字段 (attempt {attempt}): {body}")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP)
    return None


# ── 上下文 ────────────────────────────────────────────────────
@dataclass
class Ctx:
    rapidapi_key: str
    since_ts: Optional[int]
    max_pages: Optional[int]
    writer: csv.DictWriter
    fp: object
    csv_lock: threading.Lock
    seen_ids: set
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
    items = [it for it in items if it.get("post_id") and it.get("profile_id")]
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

# ── 单主页抓取 ────────────────────────────────────────────────
def fetch_profile(ctx: Ctx, profile_id: str) -> bool:
    with ctx.prog_lock:
        state = ctx.progress.get(profile_id, {})
    cursor = state.get("cursor", "")
    page   = state.get("page", 1)
    total  = state.get("total", 0)
    tag    = profile_id[:24]
    if cursor:
        print(f"[{tag}] 断点续传 第{page}页")
    else:
        print(f"[{tag}] 开始抓取")

    session_pages = 0
    while True:
        body = fetch_page(ctx.rapidapi_key, profile_id, cursor)
        if body is None:
            print(f"[{tag}] 请求失败，中止（下次续传）")
            return False
        items = body.get("results") or []
        if not items:
            print(f"[{tag}] 无更多数据，完成")
            break

        rows, hit_cutoff = [], False
        for item in items:
            ts = _safe_int(item.get("timestamp"))
            if ctx.since_ts and ts and ts < ctx.since_ts:
                hit_cutoff = True
                continue
            author     = item.get("author") or {}
            reactions  = item.get("reactions") or {}
            image      = item.get("image") or {}
            video_files = item.get("video_files") or {}
            message    = item.get("message") or ""
            rows.append({
                "profile_id":      profile_id,
                "post_id":         item.get("post_id", "") or "",
                "type":            item.get("type", "") or "",
                "url":             item.get("url", "") or "",
                "timestamp":       ts if ts is not None else "",
                "timestamp_fmt":   fmt_cst(ts) if ts else "",
                "message":         message,
                "message_rich":    item.get("message_rich") or "",
                "hashtags":        " ".join(HASHTAG_RE.findall(message)),
                "reactions_count": _safe_int(item.get("reactions_count")),
                "comments_count":  _safe_int(item.get("comments_count")),
                "reshare_count":   _safe_int(item.get("reshare_count")),
                "reaction_like":   _safe_int(reactions.get("like")),
                "reaction_love":   _safe_int(reactions.get("love")),
                "reaction_care":   _safe_int(reactions.get("care")),
                "reaction_haha":   _safe_int(reactions.get("haha")),
                "reaction_wow":    _safe_int(reactions.get("wow")),
                "reaction_sad":    _safe_int(reactions.get("sad")),
                "reaction_angry":  _safe_int(reactions.get("angry")),
                "author_id":       str(author.get("id") or ""),
                "author_name":     author.get("name") or "",
                "author_url":      author.get("url") or "",
                "image_uri":       image.get("uri") or "",
                "image_id":        str(image.get("id") or ""),
                "video_url":       item.get("video") or "",
                "video_sd_file":   (video_files or {}).get("video_sd_file") or "",
                "video_hd_file":   (video_files or {}).get("video_hd_file") or "",
                "video_thumbnail": item.get("video_thumbnail") or "",
                "raw_json":        item,
            })

        next_cursor = body.get("cursor") or ""
        has_more = bool(next_cursor)

        with ctx.csv_lock:
            new = [r for r in rows if r["post_id"] and r["post_id"] not in ctx.seen_ids]
            for r in new:
                ctx.seen_ids.add(r["post_id"])

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
            if has_more and not hit_cutoff:
                ctx.progress[profile_id] = {"cursor": next_cursor, "page": page, "total": total}
            else:
                ctx.progress.pop(profile_id, None)
            save_progress(ctx.pfile, ctx.progress)

        if hit_cutoff or not has_more:
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
    ap = argparse.ArgumentParser(description="抓取 Facebook 主页发布的帖子（RapidAPI facebook-scraper3）")
    ap.add_argument("profile_ids", nargs="+", help="Facebook 主页数字 profile_id，可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--since", help="只采集此日期之后的帖子，格式 YYYY-MM-DD（CST）")
    ap.add_argument("--workers", type=int, default=3, help="并发线程数（默认 3）")
    ap.add_argument("--max-pages", type=int, default=None,
                    help="本次运行每个主页最多翻页数（不传则翻完）")
    args = ap.parse_args()

    rapidapi_key = load_rapidapi_key()
    since_ts = None
    if args.since:
        d = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=_CST)
        since_ts = int(d.timestamp())

    out_dir  = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file    = out_dir / "fb_posts.csv"
    pfile       = out_dir / ".fb_posts_progress.json"
    failed_path = out_dir / "fb_posts_failed.jsonl"
    trace_id    = f"fb_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    progress    = load_progress(pfile)
    seen_ids    = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(f"主页数: {len(args.profile_ids)}  并发: {args.workers}  输出: {csv_file}")
    if since_ts:
        print(f"只采集 {args.since} 之后的帖子")
    if args.max_pages:
        print(f"本次每主页最多翻 {args.max_pages} 页")
    if seen_ids:
        print(f"已存在 CSV {len(seen_ids)} 条记录，将自动去重")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            rapidapi_key=rapidapi_key, since_ts=since_ts, max_pages=args.max_pages,
            writer=writer, fp=f,
            csv_lock=threading.Lock(), seen_ids=seen_ids,
            progress=progress, pfile=pfile, prog_lock=threading.Lock(),
            trace_id=trace_id, failed_path=failed_path, failed_lock=threading.Lock(),
        )

        def run(pid: str):
            ok = fetch_profile(ctx, pid)
            if ok:
                with ctx.prog_lock:
                    if pid in ctx.progress and not ctx.progress[pid].get("cursor"):
                        ctx.progress.pop(pid, None)
                        save_progress(ctx.pfile, ctx.progress)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for fut in as_completed({pool.submit(run, p): p for p in args.profile_ids}):
                if fut.exception():
                    print(f"[error] {fut.exception()}")

    print(f"\n✅ 完成 → {csv_file}")


if __name__ == "__main__":
    main()
