# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# get_video_comments.py —— 抓取 YouTube 视频评论（顶层 + 子评论），upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run get_video_comments.py <video_id> [--output-dir DIR] [--no-replies] [--max-top N]
# 示例：uv run get_video_comments.py 1uu4E8xtY7M --output-dir ./output
# 断点续爬：进度写入 .yt_comments_progress.json，中断后再次运行同命令即可续传

import argparse, csv, json, os, re, sys, time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

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
    if v: return v
    sys.exit("❌ 未找到 JustOneAPI Token，请在 .env 中配置：\n  JUSTONEAPI_TOKEN=your_token")

# ── 常量 ──────────────────────────────────────────────────────
BASE_URL       = "https://api.justoneapi.com"
TOP_ENDPOINT   = "/api/youtube/get-video-comment/v1"
SUB_ENDPOINT   = "/api/youtube/get-video-sub-comment/v1"
BACKEND_URL    = "https://www.goodgame.monster/api/skill/youtube/comments/upsert"
TIMEOUT        = 60
RETRY_MAX      = 3
RETRY_SLEEP    = 2.0
PAGE_SLEEP     = 0.5
NO_RETRY_CODES = {100, 303, 400, 600, 601}

CSV_COLUMNS = [
    "comment_id", "video_id", "is_sub", "parent_comment_id", "root_comment_id",
    "content", "published_time_text",
    "like_count_text", "like_count", "reply_count", "reply_continuation_token",
    "author_name", "author_id", "author_thumbnail",
    "is_creator", "creator_thumbnail_url", "raw_data",
]

# ── 工具 ──────────────────────────────────────────────────────
def _safe_int(v):
    if v is None: return None
    if isinstance(v, int): return v
    try: return int(re.sub(r"[^\d]", "", str(v)) or "0") or None
    except: return None

def load_progress(pfile): return json.loads(pfile.read_text("utf-8")) if pfile.exists() else {}
def save_progress(pfile, data): pfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

def load_seen(csv_file):
    if not (csv_file.exists() and csv_file.stat().st_size > 0): return set()
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        return {r["comment_id"] for r in csv.DictReader(f) if r.get("comment_id")}

# ── API 调用 ──────────────────────────────────────────────────
def _request(token, endpoint, params):
    p = {"token": token, **params}
    for attempt in range(1, RETRY_MAX + 1):
        try:
            r = requests.get(f"{BASE_URL}{endpoint}", params=p, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            code = body.get("code")
            if code == 0: return body.get("data") or {}
            if code in NO_RETRY_CODES:
                print(f"  [error] 不可重试 code={code}")
                return None
            print(f"  [warn] code={code} (attempt {attempt})")
        except Exception as e:
            print(f"  [error] {e} (attempt {attempt})")
        if attempt < RETRY_MAX: time.sleep(RETRY_SLEEP)
    return None

# ── 数据转换 ──────────────────────────────────────────────────
def comment_to_row(c, video_id, is_sub, parent_comment_id, root_comment_id):
    cid = c.get("comment_id", "")
    return {
        "comment_id":             cid,
        "video_id":               video_id,
        "is_sub":                 is_sub,
        "parent_comment_id":      parent_comment_id,
        "root_comment_id":        root_comment_id or cid,
        "content":                c.get("content"),
        "published_time_text":    c.get("published_time_text"),
        "like_count_text":        c.get("like_count_text"),
        "like_count":             _safe_int(c.get("like_count")),
        "reply_count":            _safe_int(c.get("reply_count")),
        "reply_continuation_token": c.get("reply_continuation_token"),
        "author_name":            c.get("author_name"),
        "author_id":              c.get("author_id"),
        "author_thumbnail":       c.get("author_thumbnail"),
        "is_creator":             c.get("is_creator", False),
        "creator_thumbnail_url":  c.get("creator_thumbnail_url"),
        "raw_data":               c,
    }

# ── 后端上传 ──────────────────────────────────────────────────
def upload_to_backend(rows, trace_id, failed_path):
    items = [{k: v for k, v in r.items()
              if k != "raw_data" and v not in (None, "", [])} | {"raw_data": r.get("raw_data")}
             for r in rows if r.get("comment_id")]
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
        for it in items: f.write(json.dumps(it, ensure_ascii=False, default=str) + "\n")
    return False

def write_csv(rows, f, writer):
    for r in rows:
        writer.writerow({**r, "raw_data": json.dumps(r.get("raw_data") or {}, ensure_ascii=False)})
    f.flush()

# ── 主流程 ────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="抓取 YouTube 视频评论（顶层+子评论，支持断点续爬）")
    ap.add_argument("video_id", help="YouTube 视频 ID")
    ap.add_argument("--output-dir", default="search_logs")
    ap.add_argument("--no-replies", action="store_true", help="只抓顶层评论")
    ap.add_argument("--max-top", type=int, default=0, help="最多抓取顶层评论数（0=不限）")
    args = ap.parse_args()

    token     = load_token()
    out_dir   = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file  = out_dir / "yt_comments.csv"
    pfile     = out_dir / ".yt_comments_progress.json"
    failed    = out_dir / "yt_comments_failed.jsonl"
    trace_id  = f"yt_comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    progress = load_progress(pfile)
    seen     = load_seen(csv_file)
    state    = progress.get(args.video_id, {})

    file_exists = csv_file.exists() and csv_file.stat().st_size > 0
    print(f"视频: {args.video_id}  输出: {csv_file}{' | 回复: 关闭' if args.no_replies else ''}")

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if not file_exists: writer.writeheader()

        # ─── 阶段1: 顶层评论 ───
        stage       = state.get("stage", "top")
        token_cur   = state.get("top_token") if stage == "top" else None
        page        = state.get("top_page", 1) if stage == "top" else 1
        total       = state.get("total", 0)
        sub_targets = list(state.get("sub_targets", []))  # [[comment_id, reply_token], ...]
        session_top = 0

        if stage == "top":
            print(f"开始抓取顶层评论...")
            reached_limit = False
            while not reached_limit:
                params = {"videoId": args.video_id}
                if token_cur: params["continuationToken"] = token_cur
                data = _request(token, TOP_ENDPOINT, params)
                if data is None:
                    print(f"[顶层第{page}页] 请求失败，保存进度")
                    progress[args.video_id] = {"stage": "top", "top_token": token_cur,
                        "top_page": page, "total": total, "sub_targets": sub_targets}
                    save_progress(pfile, progress)
                    return

                comments = data.get("comments") or []
                if not comments: break

                new_rows = []
                for c in comments:
                    cid = c.get("comment_id", "")
                    if not cid or cid in seen: continue
                    seen.add(cid)
                    row = comment_to_row(c, args.video_id, 0, None, cid)
                    new_rows.append(row)
                    rct = c.get("reply_continuation_token")
                    if not args.no_replies and rct and _safe_int(c.get("reply_count")):
                        sub_targets.append([cid, rct])
                    session_top += 1
                    if args.max_top and session_top >= args.max_top:
                        reached_limit = True; break

                if new_rows:
                    upload_to_backend(new_rows, trace_id, failed)
                    write_csv(new_rows, f, writer)
                    total += len(new_rows)

                print(f"[顶层第{page}页] {len(comments)}条 新增{len(new_rows)}条 累计{total}")
                token_cur = data.get("continuation_token")
                page += 1
                progress[args.video_id] = {"stage": "top", "top_token": token_cur,
                    "top_page": page, "total": total, "sub_targets": sub_targets}
                save_progress(pfile, progress)
                if not token_cur or reached_limit: break
                time.sleep(PAGE_SLEEP)

            stage = "sub"

        # ─── 阶段2: 子评论 ───
        if stage == "sub" and not args.no_replies and sub_targets:
            print(f"待拉取 {len(sub_targets)} 条评论的回复")
            while sub_targets:
                root_id, reply_token = sub_targets[0][0], sub_targets[0][1]
                sub_token = reply_token
                sub_page  = 1
                sub_total = 0
                while True:
                    params = {"videoId": args.video_id, "commentId": root_id}
                    if sub_token: params["continuationToken"] = sub_token
                    data = _request(token, SUB_ENDPOINT, params)
                    if data is None:
                        print(f"[子评论 {root_id} 第{sub_page}页] 失败，保存进度")
                        progress[args.video_id] = {"stage": "sub", "total": total,
                            "sub_targets": sub_targets}
                        save_progress(pfile, progress)
                        return

                    comments = data.get("comments") or []
                    if not comments: break

                    new_rows = []
                    for c in comments:
                        cid = c.get("comment_id", "")
                        if not cid or cid in seen: continue
                        seen.add(cid)
                        # comment_id 格式 parent.child，parent 即 root
                        parent_id = cid.split(".")[0] if "." in cid else root_id
                        new_rows.append(comment_to_row(c, args.video_id, 1, parent_id, root_id))

                    if new_rows:
                        upload_to_backend(new_rows, trace_id, failed)
                        write_csv(new_rows, f, writer)
                        total += len(new_rows)
                        sub_total += len(new_rows)

                    sub_token = data.get("continuation_token")
                    sub_page += 1
                    if not sub_token: break
                    time.sleep(PAGE_SLEEP)

                print(f"[子评论 {root_id}] 新增{sub_total}条")
                sub_targets.pop(0)
                progress[args.video_id] = {"stage": "sub", "total": total, "sub_targets": sub_targets}
                save_progress(pfile, progress)

    progress.pop(args.video_id, None)
    save_progress(pfile, progress)
    print(f"\n✅ 完成 → {csv_file}  共{total}条")

if __name__ == "__main__":
    main()
