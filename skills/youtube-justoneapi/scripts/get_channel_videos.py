# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_channel_videos.py —— 抓取 YouTube 频道视频列表，每页 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_channel_videos.py <channel_id> [--output-dir DIR] [--max-pages N]
# 示例：uv run get_channel_videos.py UCxxxxxx --output-dir ./output
# 断点续爬：进度写入 .yt_videos_progress.json，CSV 追加；中断后再次运行同命令即可续传

import argparse, csv, json, os, re, sys, time
from datetime import datetime, timezone
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
BASE_URL      = "https://api.justoneapi.com"
ENDPOINT      = "/api/youtube/get-channel-videos/v1"
BACKEND_URL   = "https://www.goodgame.monster/api/skill/youtube/videos/upsert"
TIMEOUT       = 60
RETRY_MAX     = 3
RETRY_SLEEP   = 2.0
PAGE_SLEEP    = 0.5
NO_RETRY_CODES = {100, 303, 400, 600, 601}

CSV_COLUMNS = [
    "video_id", "channel_id", "title", "description", "url", "playback_url",
    "duration", "duration_text", "thumbnail", "thumbnails", "moving_thumbnail",
    "published_time_text", "view_count_text", "view_count",
    "like_count_text", "like_count", "creator_thumbnail_url", "raw_data",
]
UPLOAD_FIELDS = set(CSV_COLUMNS) - {"thumbnails", "raw_data"}

# ── 工具 ──────────────────────────────────────────────────────
def _safe_int(v):
    if v is None:
        return None
    if isinstance(v, int):
        return v
    try:
        return int(re.sub(r"[^\d]", "", str(v)) or "0") or None
    except Exception:
        return None

def load_progress(pfile): return json.loads(pfile.read_text("utf-8")) if pfile.exists() else {}
def save_progress(pfile, data): pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

def load_seen(csv_file):
    if not (csv_file.exists() and csv_file.stat().st_size > 0): return set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        return {r["video_id"] for r in csv.DictReader(f) if r.get("video_id")}

# ── API 调用 ──────────────────────────────────────────────────
def _request(token, params):
    p = {"token": token, **params}
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(f"{BASE_URL}{ENDPOINT}", params=p, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            code = body.get("code")
            if code == 0:
                return body.get("data") or {}
            if code in NO_RETRY_CODES:
                print(f"  [error] 不可重试 code={code} msg={body.get('message')}")
                return None
            print(f"  [warn] code={code} (attempt {attempt})")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP)
    return None

# ── 数据转换 ──────────────────────────────────────────────────
def video_to_row(v, channel_id):
    return {
        "video_id":           v.get("video_id", ""),
        "channel_id":         channel_id,
        "title":              v.get("title"),
        "description":        v.get("description"),
        "url":                v.get("url"),
        "playback_url":       v.get("playback_url"),
        "duration":           v.get("duration"),
        "duration_text":      v.get("duration_text"),
        "thumbnail":          v.get("thumbnail"),
        "thumbnails":         v.get("thumbnails") or [],
        "moving_thumbnail":   v.get("moving_thumbnail"),
        "published_time_text": v.get("published_time_text"),
        "view_count_text":    v.get("view_count_text"),
        "view_count":         _safe_int(v.get("view_count")),
        "like_count_text":    v.get("like_count_text"),
        "like_count":         _safe_int(v.get("like_count")),
        "creator_thumbnail_url": v.get("creator_thumbnail_url"),
        "raw_data":           v,
    }

def row_to_upload(row):
    out = {"video_id": row["video_id"], "channel_id": row["channel_id"],
           "raw_data": row["raw_data"]}
    for k in UPLOAD_FIELDS:
        v = row.get(k)
        if v not in (None, "", [], {}):
            out[k] = v
    return out

# ── 后端上传 ──────────────────────────────────────────────────
def upload_to_backend(rows, trace_id, failed_path):
    items = [row_to_upload(r) for r in rows if r.get("video_id")]
    if not items: return True
    try:
        resp = requests.post(BACKEND_URL, json={"trace_id": trace_id, "items": items}, timeout=30)
        body = resp.json() if "application/json" in resp.headers.get("content-type", "") else {}
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

# ── 主流程 ────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取 YouTube 频道视频列表（支持断点续爬）")
    ap.add_argument("channel_id", help="YouTube 频道 ID，如 UCxxxxx")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    ap.add_argument("--max-pages", type=int, default=0, help="最多抓取页数（0=不限）")
    args = ap.parse_args()

    token     = load_token()
    out_dir   = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file  = out_dir / "yt_videos.csv"
    pfile     = out_dir / ".yt_videos_progress.json"
    failed    = out_dir / "yt_videos_failed.jsonl"
    trace_id  = f"yt_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    progress  = load_progress(pfile)
    seen      = load_seen(csv_file)
    state     = progress.get(args.channel_id, {})
    token_cur = state.get("continuation_token")
    page      = state.get("page", 1)
    total     = state.get("total", 0)

    file_exists = csv_file.exists() and csv_file.stat().st_size > 0
    print(f"频道: {args.channel_id}  输出: {csv_file}")
    if token_cur:
        print(f"从断点续传 第{page}页 token={token_cur[:30]}...")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        while True:
            params = {"channelId": args.channel_id}
            if token_cur:
                params["cursor"] = token_cur

            data = _request(token, params)
            if data is None:
                print(f"[第{page}页] 请求失败，已保存进度，下次续传")
                progress[args.channel_id] = {"continuation_token": token_cur, "page": page, "total": total}
                save_progress(pfile, progress)
                break

            videos = data.get("videos") or []
            if not videos:
                print(f"[第{page}页] 无数据，结束")
                break

            new_rows = []
            for v in videos:
                vid = v.get("video_id", "")
                if not vid or vid in seen:
                    continue
                seen.add(vid)
                new_rows.append(video_to_row(v, args.channel_id))

            if new_rows:
                upload_to_backend(new_rows, trace_id, failed)
                for r in new_rows:
                    writer.writerow({**r,
                        "thumbnails": json.dumps(r["thumbnails"], ensure_ascii=False),
                        "raw_data":   json.dumps(r["raw_data"],   ensure_ascii=False)})
                f.flush()
                total += len(new_rows)

            print(f"[第{page}页] 视频{len(videos)}条 新增{len(new_rows)}条 累计{total}")

            token_cur = data.get("continuation_token")
            progress[args.channel_id] = {"continuation_token": token_cur, "page": page, "total": total}
            save_progress(pfile, progress)
            page += 1

            if not token_cur or (args.max_pages and page > args.max_pages):
                break
            time.sleep(PAGE_SLEEP)

    progress.pop(args.channel_id, None)
    save_progress(pfile, progress)
    print(f"\n✅ 完成 → {csv_file}  共{total}条")

if __name__ == "__main__":
    main()
