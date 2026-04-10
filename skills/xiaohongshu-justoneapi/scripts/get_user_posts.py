# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_user_posts.py —— 抓取小红书用户笔记列表，支持多用户、断点续传、时间过滤
# 用法：uv run get_user_posts.py <user_id> [user_id2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N]
# 示例：uv run get_user_posts.py 5b33a8556b58b74911b89949 --output-dir ./output --since 2025-01-01

import argparse, csv, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
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

# ── 工具函数 ──────────────────────────────────────────────────
def fmt_cst(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)

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

# ── 单用户抓取 ────────────────────────────────────────────────
def fetch_user(
    token: str, user_id: str, since_ts: int | None,
    writer: csv.DictWriter, f,
    csv_lock: threading.Lock, seen_ids: set,
    progress: dict, pfile: Path, prog_lock: threading.Lock,
) -> bool:
    with prog_lock:
        state = progress.get(user_id, {})
    cursor = state.get("cursor", "")
    page   = state.get("page", 1)
    total  = state.get("total", 0)
    tag    = user_id[:20]
    if cursor:
        print(f"[{tag}] 断点续传 第{page}页 cursor={cursor}")
    else:
        print(f"[{tag}] 开始抓取")

    while True:
        data = fetch_page(token, user_id, cursor)
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
            if since_ts and ct and int(ct) < since_ts:
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
                "raw_json": json.dumps(note, ensure_ascii=False),
            })

        next_cursor = notes[-1].get("cursor", "") if notes else ""
        has_more    = data.get("has_more", False)

        with csv_lock:
            new = [r for r in rows if r["note_id"] not in seen_ids]
            for r in new:
                seen_ids.add(r["note_id"])
            writer.writerows(new)
            f.flush()
        total += len(new)
        print(f"[{tag}] 第{page}页 新增{len(new)}条 累计{total}条")

        page += 1
        with prog_lock:
            if has_more and next_cursor and not hit_cutoff:
                progress[user_id] = {"cursor": next_cursor, "page": page, "total": total}
            else:
                progress.pop(user_id, None)
            save_progress(pfile, progress)

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
    ap.add_argument("--output-dir", default=".", help="输出目录（默认当前目录）")
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
    csv_file = out_dir / "xhs_posts.csv"
    pfile    = out_dir / ".xhs_posts_progress.json"
    progress = load_progress(pfile)
    seen_ids = load_seen(csv_file)
    file_exists = csv_file.exists() and csv_file.stat().st_size > 0

    csv_lock  = threading.Lock()
    prog_lock = threading.Lock()

    print(f"用户数: {len(args.user_ids)}  并发: {args.workers}  输出: {csv_file}")
    if since_ts:
        print(f"只采集 {args.since} 之后的笔记")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not file_exists:
            writer.writeheader()

        def run(uid: str):
            ok = fetch_user(
                token, uid, since_ts, writer, f,
                csv_lock, seen_ids, progress, pfile, prog_lock,
            )
            if ok:
                with prog_lock:
                    progress.pop(uid, None)
                    save_progress(pfile, progress)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for fut in as_completed({pool.submit(run, uid): uid for uid in args.user_ids}):
                if fut.exception():
                    print(f"[error] {fut.exception()}")

    print(f"\n✅ 完成 → {csv_file}")

if __name__ == "__main__":
    main()

