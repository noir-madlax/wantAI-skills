# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "requests",
# ]
# ///
#
# search_notes.py —— 小红书笔记搜索，结果落地为 CSV
# 用法：uv run search_notes.py <keyword> <max_pages> [--sort SORT] [--note-type TYPE] [--output-dir DIR]
# 示例：uv run search_notes.py 美妆 10 --sort popularity_descending --note-type _1 --output-dir ./output

import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# ── Token 加载 ──────────────────────────────────────────────
def find_env_token():
    """从当前目录向上逐级查找 .env，直到根目录。"""
    for directory in [Path.cwd(), *Path.cwd().parents]:
        env_path = directory / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                for key in ("JUSTONEAPI_TOKEN", "JUST_ONE_API_TOKEN"):
                    if line.startswith(f"{key}="):
                        token = line.split("=", 1)[1].strip()
                        if token:
                            return token
    return None

def load_token():
    """优先级：.env 文件 → 环境变量，均未找到则报错退出。"""
    token = find_env_token()
    if token:
        return token
    token = os.environ.get("JUSTONEAPI_TOKEN") or os.environ.get("JUST_ONE_API_TOKEN")
    if token:
        return token
    raise RuntimeError(
        "未找到 JustOneAPI Token，请在 .env 文件中添加：\n"
        "  JUSTONEAPI_TOKEN=your_token_here"
    )

# ── API 常量 ─────────────────────────────────────────────────
BASE_URL    = "https://api.justoneapi.com"
ENDPOINT    = "/api/xiaohongshu/search-note/v3"
TIMEOUT     = 60
RETRY_MAX   = 5       # 接口不稳定，重试次数高于其他接口
PAGE_SLEEP  = 1.5     # 翻页间隔，避免触发 302

# 不可重试的错误码（客户端侧无法修复）
NO_RETRY_CODES = {100, 303, 400, 600, 601}

ERROR_MESSAGES = {
    100: "Token 无效或已失效，请检查 token",
    302: "超出速率限制，请降低请求频率",
    303: "超出每日配额，今日无法继续采集",
    400: "参数错误，请检查关键词等参数",
    500: "JustOneAPI 服务器内部错误",
    600: "当前 token 无此接口权限",
    601: "余额不足，请前往 JustOneAPI 充值",
}

SORT_CHOICES = {
    "general":              "综合",
    "popularity_descending": "热门",
    "time_descending":      "最新",
}

NOTE_TYPE_CHOICES = {
    "_0": "全部类型",
    "_1": "仅视频",
    "_2": "仅普通图文",
}

# ── API 调用 ─────────────────────────────────────────────────
def fetch_page(token: str, keyword: str, page: int, sort: str, note_type: str) -> list:
    """
    获取单页笔记列表。

    重试策略（该接口不稳定，比其他接口更激进）：
      - HTTP 状态码非 200 → 重试
      - HTTP 200 但 code 非 0 → 重试（NO_RETRY_CODES 除外，直接抛错）
      - 网络异常 → 重试
    每次重试间隔递增（attempt * 2s），code=302 时等待更长（attempt * 5s）。
    最多重试 RETRY_MAX 次。
    """
    url    = f"{BASE_URL}{ENDPOINT}"
    params = {
        "token":    token,
        "keyword":  keyword,
        "page":     page,
        "sort":     sort,
        "noteType": note_type,
    }

    for attempt in range(1, RETRY_MAX + 1):
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)

            # HTTP 非 200 → 重试
            if resp.status_code != 200:
                wait = attempt * 2
                print(f"  HTTP {resp.status_code}，第 {attempt}/{RETRY_MAX} 次重试（{wait}s 后）...")
                if attempt < RETRY_MAX:
                    time.sleep(wait)
                continue

            body = resp.json()
            code = body.get("code")

            if code == 0:
                items = body.get("data", {}).get("items", [])
                return [
                    item["note"]
                    for item in items
                    if item.get("model_type") == "note" and "note" in item
                ]

            # 不可重试的错误码，立即报错
            if code in NO_RETRY_CODES:
                raise RuntimeError(ERROR_MESSAGES.get(code, f"错误 code={code}，不可重试"))

            # 其他非 0 code（301/302/500 等）→ 重试，等待递增
            wait = attempt * 5 if code == 302 else attempt * 2
            print(f"  code={code}，第 {attempt}/{RETRY_MAX} 次重试（{wait}s 后）...")
            if attempt < RETRY_MAX:
                time.sleep(wait)

        except RuntimeError:
            raise
        except Exception as e:
            wait = attempt * 2
            print(f"  请求异常: {e}，第 {attempt}/{RETRY_MAX} 次重试（{wait}s 后）...")
            if attempt < RETRY_MAX:
                time.sleep(wait)

    raise RuntimeError(f"接口持续失败，已重试 {RETRY_MAX} 次，请稍后再试")

# ── CSV 写入 ─────────────────────────────────────────────────
CSV_COLUMNS = [
    "note_id", "type", "timestamp", "timestamp_fmt",
    "title", "desc",
    "author_userid", "author_nickname", "author_red_id",
    "liked_count", "comments_count", "collected_count", "shared_count",
    "cover_url",
]

def note_to_row(note: dict) -> dict:
    user = note.get("user") or {}
    imgs = note.get("images_list") or []
    ts   = note.get("timestamp", 0)
    cover = next(
        (img.get("url") or img.get("url_size_large", "") for img in imgs if img),
        "",
    )
    return {
        "note_id":         note.get("id", ""),
        "type":            note.get("type", ""),
        "timestamp":       ts,
        "timestamp_fmt":   datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S") if ts else "",
        "title":           note.get("title") or note.get("abstract_show", ""),
        "desc":            note.get("desc", ""),
        "author_userid":   user.get("userid", ""),
        "author_nickname": user.get("nickname", ""),
        "author_red_id":   user.get("red_id", ""),
        "liked_count":     note.get("liked_count", ""),
        "comments_count":  note.get("comments_count", ""),
        "collected_count": note.get("collected_count", ""),
        "shared_count":    note.get("shared_count", ""),
        "cover_url":       cover,
    }

def write_csv(rows: list, filepath: Path, write_header: bool):
    with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(rows)

# ── 主流程 ───────────────────────────────────────────────────
def crawl(keyword: str, max_pages: int, sort: str, note_type: str, output_dir: Path):
    token    = load_token()
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"xhs_notes_{keyword}_{sort}_{ts}.csv"
    total    = 0

    print(
        f"关键词: {keyword} | 排序: {SORT_CHOICES[sort]} "
        f"| 类型: {NOTE_TYPE_CHOICES[note_type]} | 最多: {max_pages} 页"
    )

    for page in range(1, max_pages + 1):
        print(f"采集第 {page}/{max_pages} 页...", end=" ", flush=True)
        notes = fetch_page(token, keyword, page, sort, note_type)

        if not notes:
            print("已到末页。")
            break

        rows = [note_to_row(n) for n in notes]
        write_csv(rows, filepath, write_header=(page == 1))
        total += len(rows)
        print(f"{len(rows)} 条（累计 {total} 条）")

        if page < max_pages:
            time.sleep(PAGE_SLEEP)

    print(f"\n✅ 完成，共 {total} 条 → {filepath}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="小红书笔记搜索")
    ap.add_argument("keyword",   help="搜索关键词")
    ap.add_argument("max_pages", type=int,
                    help="最大采集页数（必填，建议不超过 50 页以节省配额）")
    ap.add_argument(
        "--sort",
        choices=list(SORT_CHOICES.keys()),
        default="general",
        metavar="SORT",
        help="排序：general（综合，默认）| popularity_descending（热门）| time_descending（最新）",
    )
    ap.add_argument(
        "--note-type",
        choices=list(NOTE_TYPE_CHOICES.keys()),
        default="_0",
        dest="note_type",
        metavar="TYPE",
        help="笔记类型：_0（全部，默认）| _1（仅视频）| _2（仅图文）",
    )
    ap.add_argument("--output-dir", default="search_logs",
                    help="输出目录（默认 search_logs）")
    args = ap.parse_args()

    try:
        crawl(args.keyword, args.max_pages, args.sort, args.note_type, Path(args.output_dir))
    except RuntimeError as e:
        sys.exit(f"❌ {e}")
