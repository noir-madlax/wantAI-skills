# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_user_posts.py —— 抓取小红书用户笔记列表，每页先 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_user_posts.py <user_id> [user_id2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N]
# 示例：uv run get_user_posts.py 5b33a8556b58b74911b89949 --output-dir ./output --since 2025-01-01

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
API_URL     = "https://api.justoneapi.com/api/xiaohongshu/get-user-note-list/v4"
TIMEOUT     = 60
RETRY_MAX   = 3
RETRY_SLEEP = 2.0
PAGE_SLEEP  = 0.5
_CST = timezone(timedelta(hours=8))

CSV_COLUMNS = [
    "user_id", "note_id", "create_time", "create_time_fmt",
    "title", "desc", "type", "sticky",
    "author_userid", "author_nickname",
    "likes", "comments_count", "collected_count", "share_count",
    "cover_url", "raw_json",
]

# ── 后端上传配置 ──────────────────────────────────────────────
BACKEND_URL    = "https://www.goodgame.monster/api/skill/xiaohongshu/notes/upsert"
UPLOAD_TIMEOUT = 30

# CSV 列名 → 后端 schema 字段名（含义相同，名称不同）
UPLOAD_FIELD_MAP = {
    "note_id":         "note_id",
    "create_time":     "timestamp",
    "create_time_fmt": "timestamp_fmt",
    "title":           "title",
    "desc":            "description",
    "type":            "type",
    "author_userid":   "author_userid",
    "author_nickname": "author_nickname",
    "likes":           "liked_count",
    "comments_count":  "comments_count",
    "collected_count": "collected_count",
    "share_count":     "shared_count",
    "cover_url":       "cover_url",
    "raw_json":        "raw_data",
}
INT_FIELDS = {"timestamp", "liked_count", "comments_count", "collected_count", "shared_count"}

# ── 工具函数 ──────────────────────────────────────────────────
def fmt_cst(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)

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
    return out

def load_seen(csv_file: Path) -> set:
    if not (csv_file.exists() and csv_file.stat().st_size > 0):
        return set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        return {r["note_id"] for r in csv.DictReader(f) if r.get("note_id")}

def load_progress(pfile: Path) -> dict:
    return json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {}

def save_progress(pfile: Path, data: dict):
    pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── API 调用 ──────────────────────────────────────────────────
def fetch_page(token: str, user_id: str, last_cursor: str = "") -> dict | None:
    params = {"token": token, "userId": user_id}
    if last_cursor:
        params["lastCursor"] = last_cursor
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(API_URL, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            if body.get("code") == 0:
                return body.get("data", {})
            code = body.get("code")
            if code == 301 and attempt < RETRY_MAX:
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
    items = [it for it in items if it.get("note_id")]
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
def fetch_user(ctx: Ctx, user_id: str) -> bool:
    with ctx.prog_lock:
        state = ctx.progress.get(user_id, {})
    cursor = state.get("cursor", "")
    page   = state.get("page", 1)
    total  = state.get("total", 0)
    tag    = user_id[:20]
    if cursor:
        print(f"[{tag}] 断点续传 第{page}页 cursor={cursor}")
    else:
        print(f"[{tag}] 开始抓取")

    while True:
        data = fetch_page(ctx.token, user_id, cursor)
        if data is None:
            print(f"[{tag}] 请求失败，中止（下次续传）")
            return False
        notes = data.get("notes") or []
        if not notes:
            print(f"[{tag}] 无更多数据，完成")
            break

        rows, hit_cutoff = [], False
        for note in notes:
            ct = note.get("create_time", 0)
            if ctx.since_ts and ct and int(ct) < ctx.since_ts:
                hit_cutoff = True
                continue
            u = note.get("user") or {}
            imgs = note.get("images_list") or []
            rows.append({
                "user_id": user_id,
                "note_id": note.get("id", ""),
                "create_time": ct,
                "create_time_fmt": fmt_cst(ct) if ct else "",
                "title": note.get("title", "") or note.get("display_title", ""),
                "desc": note.get("desc", ""),
                "type": note.get("type", ""),
                "sticky": note.get("sticky", False),
                "author_userid": u.get("userid", ""),
                "author_nickname": u.get("nickname", ""),
                "likes": note.get("likes", ""),
                "comments_count": note.get("comments_count", ""),
                "collected_count": note.get("collected_count", ""),
                "share_count": note.get("share_count", ""),
                "cover_url": imgs[0].get("url", "") if imgs else "",
                "raw_json": note,  # 内存中保留 dict，写 CSV 时再 dumps
            })

        next_cursor = notes[-1].get("cursor", "") if notes else ""
        has_more    = data.get("has_more", False)

        # 1) 锁内：去重，标记已见
        with ctx.csv_lock:
            new = [r for r in rows if r["note_id"] not in ctx.seen_ids]
            for r in new:
                ctx.seen_ids.add(r["note_id"])

        # 2) 锁外：先上传，再写 CSV（顺序：upload → csv）
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
        with ctx.prog_lock:
            if has_more and next_cursor and not hit_cutoff:
                ctx.progress[user_id] = {"cursor": next_cursor, "page": page, "total": total}
            else:
                ctx.progress.pop(user_id, None)
            save_progress(ctx.pfile, ctx.progress)

        if hit_cutoff or not has_more or not next_cursor:
            break
        cursor = next_cursor
        time.sleep(PAGE_SLEEP)

    print(f"[{tag}] 完成 共{total}条")
    return True

# ── 主流程 ─────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取小红书用户笔记列表")
    ap.add_argument("user_ids", nargs="+", help="小红书 userId，可传多个")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--since", help="只采集此日期之后的笔记，格式 YYYY-MM-DD（CST）")
    ap.add_argument("--workers", type=int, default=3, help="并发线程数（默认 3）")
    args = ap.parse_args()

    token = load_token()
    since_ts = None
    if args.since:
        d = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=_CST)
        since_ts = int(d.timestamp())

    out_dir  = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file    = out_dir / "xhs_posts.csv"
    pfile       = out_dir / ".xhs_posts_progress.json"
    failed_path = out_dir / "xhs_posts_failed.jsonl"
    trace_id    = f"xhs_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    progress    = load_progress(pfile)
    seen_ids    = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    print(
        f"用户数: {len(args.user_ids)}  并发: {args.workers}  输出: {csv_file}"
    )
    if since_ts:
        print(f"只采集 {args.since} 之后的笔记")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not file_exists:
            writer.writeheader()

        ctx = Ctx(
            token=token, since_ts=since_ts,
            writer=writer, fp=f,
            csv_lock=threading.Lock(), seen_ids=seen_ids,
            progress=progress, pfile=pfile, prog_lock=threading.Lock(),
            trace_id=trace_id, failed_path=failed_path, failed_lock=threading.Lock(),
        )

        def run(uid: str):
            ok = fetch_user(ctx, uid)
            if ok:
                with ctx.prog_lock:
                    ctx.progress.pop(uid, None)
                    save_progress(ctx.pfile, ctx.progress)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for fut in as_completed({pool.submit(run, uid): uid for uid in args.user_ids}):
                if fut.exception():
                    print(f"[error] {fut.exception()}")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()

