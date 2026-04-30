# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_user_videos.py —— 抓取抖音用户发布的视频，每页先 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_user_videos.py <sec_uid> [sec_uid2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]
# 示例：uv run get_user_videos.py MS4wLjABAAAA_demo --output-dir ./output --since 2025-01-01

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
API_URL     = "https://api.justoneapi.com/api/douyin/get-user-video-list/v3"
TIMEOUT     = 60
RETRY_MAX   = 3
RETRY_SLEEP = 2.0
PAGE_SLEEP  = 0.5
_CST = timezone(timedelta(hours=8))

CSV_COLUMNS = [
    "sec_uid", "aweme_id", "short_id", "media_type", "is_top",
    "description", "create_time", "create_time_fmt", "duration_ms",
    "cover_url", "play_url", "share_url",
    "digg_count", "comment_count", "share_count", "collect_count", "play_count",
    "author_uid", "author_sec_uid", "author_short_id", "author_nickname", "author_avatar",
    "raw_json",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/douyin/videos/upsert"
UPLOAD_TIMEOUT = 30

# CSV 列名 → 后端 schema 字段名（含义相同）
UPLOAD_FIELD_MAP = {
    "sec_uid":         "sec_uid",
    "aweme_id":        "aweme_id",
    "short_id":        "short_id",
    "media_type":      "media_type",
    "is_top":          "is_top",
    "description":     "description",
    "create_time":     "create_time",   # ISO 8601 字符串
    "duration_ms":     "duration_ms",
    "cover_url":       "cover_url",
    "play_url":        "play_url",
    "share_url":       "share_url",
    "digg_count":      "digg_count",
    "comment_count":   "comment_count",
    "share_count":     "share_count",
    "collect_count":   "collect_count",
    "play_count":      "play_count",
    "author_uid":      "author_uid",
    "author_sec_uid":  "author_sec_uid",
    "author_short_id": "author_short_id",
    "author_nickname": "author_nickname",
    "author_avatar":   "author_avatar",
    "raw_json":        "raw_data",
}
INT_FIELDS = {
    "media_type", "is_top", "duration_ms",
    "digg_count", "comment_count", "share_count", "collect_count", "play_count",
}

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
    """JustOneAPI 各接口 code 有时是 int 有时是 str，统一比较。"""
    try:
        return int(code) == target
    except (TypeError, ValueError):
        return str(code) == str(target)

def _pick(d, *keys, default=None):
    """从 dict 中按候选键名顺序取第一个非空值。"""
    for k in keys:
        if d is None:
            break
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return default

def _first_url(node) -> str:
    """抖音常见结构 {"url_list": ["...", "..."]}，取第一个 URL。"""
    if not isinstance(node, dict):
        return ""
    urls = node.get("url_list") or node.get("urlList") or []
    if isinstance(urls, list) and urls:
        return urls[0] or ""
    return node.get("url", "") or ""

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
        return {r["aweme_id"] for r in csv.DictReader(f) if r.get("aweme_id")}

def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── API 调用 ──────────────────────────────────────────────────
def fetch_page(token: str, sec_uid: str, max_cursor: int = 0) -> Optional[dict]:
    params = {"token": token, "secUid": sec_uid, "maxCursor": int(max_cursor or 0)}
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
    items = [it for it in items if it.get("aweme_id") and it.get("sec_uid") and it.get("raw_data")]
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

# ── 数据转换 ──────────────────────────────────────────────────
def aweme_to_row(a: dict, sec_uid: str) -> dict:
    video  = a.get("video") or {}
    stats  = a.get("statistics") or {}
    author = a.get("author") or {}
    ts     = _safe_int(_pick(a, "create_time", "createTime"))
    duration = _safe_int(_pick(a, "duration") or _pick(video, "duration"))
    return {
        "sec_uid":         sec_uid,
        "aweme_id":        str(_pick(a, "aweme_id", "awemeId", "id") or ""),
        "short_id":        str(_pick(a, "short_id") or ""),
        "media_type":      _safe_int(_pick(a, "aweme_type", "media_type")),
        "is_top":          _safe_int(_pick(a, "is_top")),
        "description":     _pick(a, "desc", "description", "text") or "",
        "create_time":     to_iso_cst(ts) or "",
        "create_time_fmt": fmt_cst(ts) if ts else "",
        "duration_ms":     duration,
        "cover_url":       _first_url(_pick(video, "cover", "origin_cover", "dynamic_cover", default={})),
        "play_url":        _first_url(_pick(video, "play_addr", "playAddr", "download_addr", default={})),
        "share_url":       _pick(a, "share_url", "shareUrl") or "",
        "digg_count":      _safe_int(_pick(stats, "digg_count", "like_count")),
        "comment_count":   _safe_int(_pick(stats, "comment_count")),
        "share_count":     _safe_int(_pick(stats, "share_count")),
        "collect_count":   _safe_int(_pick(stats, "collect_count")),
        "play_count":      _safe_int(_pick(stats, "play_count")),
        "author_uid":      str(_pick(author, "uid", "id") or ""),
        "author_sec_uid":  _pick(author, "sec_uid", "secUid") or "",
        "author_short_id": str(_pick(author, "short_id", "unique_id") or ""),
        "author_nickname": _pick(author, "nickname", "name") or "",
        "author_avatar":   _first_url(_pick(author, "avatar_thumb", "avatar_larger", "avatar_medium", default={})),
        "raw_json":        a,
    }

# ── 单用户抓取 ────────────────────────────────────────────────
def fetch_user(ctx: Ctx, sec_uid: str) -> bool:
    with ctx.prog_lock:
        state = ctx.progress.get(sec_uid, {})
    cursor = int(state.get("cursor", 0) or 0)
    page   = state.get("page", 1)
    total  = state.get("total", 0)
    tag    = sec_uid[:24]
    if cursor:
        print(f"[{tag}] 断点续传 第{page}页 cursor={cursor}")
    else:
        print(f"[{tag}] 开始抓取")

    session_pages = 0
    while True:
        data = fetch_page(ctx.token, sec_uid, cursor)
        if data is None:
            print(f"[{tag}] 请求失败，中止（下次续传）")
            return False
        # 列表节点字段名兜底
        awemes = _pick(data, "aweme_list", "awemes", "videos", "items", default=[]) or []
        if not awemes:
            print(f"[{tag}] 无更多数据，完成")
            break

        rows, hit_cutoff = [], False
        for a in awemes:
            ts = _safe_int(_pick(a, "create_time", "createTime"))
            if ctx.since_ts and ts and ts < ctx.since_ts:
                hit_cutoff = True
                continue
            rows.append(aweme_to_row(a, sec_uid))

        next_cursor = _safe_int(_pick(data, "max_cursor", "maxCursor", "cursor")) or 0
        more = data.get("has_more")
        has_more = bool(next_cursor) if more is None else bool(more)

        # 1) 锁内：去重，标记已见
        with ctx.csv_lock:
            new = [r for r in rows if r["aweme_id"] and r["aweme_id"] not in ctx.seen_ids]
            for r in new:
                ctx.seen_ids.add(r["aweme_id"])

        # 2) 锁外：先上传，再写 CSV
        if new:
            upload_to_backend(new, ctx)
            with ctx.csv_lock:
                for r in new:
                    csv_row = {**r, "raw_json": json.dumps(r["raw_json"], ensure_ascii=False)}
                    ctx.writer.writerow(csv_row)
                ctx.fp.flush()

        total += len(new)
        print(f"[{tag}] 第{page}页 视频{len(awemes)}条 新增{len(new)}条 累计{total}条")

        page += 1
        session_pages += 1
        with ctx.prog_lock:
            if has_more and next_cursor and not hit_cutoff:
                ctx.progress[sec_uid] = {"cursor": next_cursor, "page": page, "total": total}
            else:
                ctx.progress.pop(sec_uid, None)
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
    ap = argparse.ArgumentParser(description="抓取抖音用户发布的视频")
    ap.add_argument("sec_uids", nargs="+", help="抖音用户 sec_uid（形如 MS4wLjABAAAA...），可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--since", help="只采集此日期之后的视频，格式 YYYY-MM-DD（CST）")
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
    csv_file    = out_dir / "douyin_videos.csv"
    pfile       = out_dir / ".douyin_videos_progress.json"
    failed_path = out_dir / "douyin_videos_failed.jsonl"
    trace_id    = f"douyin_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    progress    = load_progress(pfile)
    seen_ids    = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(f"用户数: {len(args.sec_uids)}  并发: {args.workers}  输出: {csv_file}")
    if since_ts:
        print(f"只采集 {args.since} 之后的视频")
    if args.max_pages:
        print(f"本次每用户最多翻 {args.max_pages} 页")
    if seen_ids:
        print(f"已存在 CSV {len(seen_ids)} 条记录，将自动去重")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            token=token, since_ts=since_ts, max_pages=args.max_pages,
            writer=writer, fp=f,
            csv_lock=threading.Lock(), seen_ids=seen_ids,
            progress=progress, pfile=pfile, prog_lock=threading.Lock(),
            trace_id=trace_id, failed_path=failed_path, failed_lock=threading.Lock(),
        )

        def run(sec_uid: str):
            ok = fetch_user(ctx, sec_uid)
            if ok:
                with ctx.prog_lock:
                    if sec_uid in ctx.progress and not ctx.progress[sec_uid].get("cursor"):
                        ctx.progress.pop(sec_uid, None)
                        save_progress(ctx.pfile, ctx.progress)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for fut in as_completed({pool.submit(run, s): s for s in args.sec_uids}):
                if fut.exception():
                    print(f"[error] {fut.exception()}")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()
