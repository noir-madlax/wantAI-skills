# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "requests",
# ]
# ///
#
# xhs_search_users.py —— 小红书用户搜索，结果落地为 CSV
# 用法：uv run search_users.py <keyword> [max_pages]
# 示例：uv run search_users.py 美妆博主 5

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

# ── API 调用 ─────────────────────────────────────────────────
BASE_URL    = "https://api.justoneapi.com"
ENDPOINT    = "/api/xiaohongshu/search-user/v2"
TIMEOUT     = 60
RETRY_MAX   = 3
RETRY_CODES = {301}

ERROR_MESSAGES = {
    100: "Token 无效或已失效，请检查 token",
    302: "超出速率限制，请稍后重试",
    303: "超出每日配额，今日无法继续采集",
    400: "参数错误，请检查 keyword 是否为空",
    500: "JustOneAPI 服务器内部错误，请稍后重试",
    600: "当前 token 无此接口权限",
    601: "余额不足，请前往 JustOneAPI 充值",
}

def fetch_page(token, keyword, page):
    """获取单页数据，自动重试 code=301 的瞬时失败。"""
    url    = f"{BASE_URL}{ENDPOINT}"
    params = {"token": token, "keyword": keyword, "page": page}

    for attempt in range(1, RETRY_MAX + 1):
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        body = resp.json()
        code = body.get("code")

        if code == 0:
            return body["data"]["users"]

        if code in RETRY_CODES and attempt < RETRY_MAX:
            print(f"  code={code}，第 {attempt} 次重试（2s 后）...")
            time.sleep(2)
            continue

        raise RuntimeError(ERROR_MESSAGES.get(code, f"未知错误 code={code}"))

    raise RuntimeError(f"code=301 采集失败，已重试 {RETRY_MAX} 次")

# ── CSV 写入 ─────────────────────────────────────────────────
CSV_COLUMNS = [
    "id", "name", "red_id", "desc", "sub_title",
    "red_official_verified", "red_official_verify_type",
    "image", "link",
]

def write_csv(users, filepath, write_header):
    with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(users)

# ── 主流程 ───────────────────────────────────────────────────
def crawl(keyword, max_pages=None, output_dir: Path = Path(".")):
    token    = load_token()
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"xhs_users_{keyword}_{ts}.csv"
    total    = 0

    for page in range(1, (max_pages or 9999) + 1):
        print(f"采集第 {page} 页...", end=" ", flush=True)
        users = fetch_page(token, keyword, page)

        if not users:
            print("已到末页。")
            break

        write_csv(users, filepath, write_header=(page == 1))
        total += len(users)
        print(f"{len(users)} 条（累计 {total} 条）")

        if max_pages and page >= max_pages:
            break
        time.sleep(1.5)  # 控制频率，避免触发 302

    print(f"\n✅ 完成，共 {total} 条 → {filepath}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="小红书用户搜索")
    ap.add_argument("keyword", help="搜索关键词")
    ap.add_argument("max_pages", nargs="?", type=int, help="最大采集页数")
    ap.add_argument("--output-dir", default="search_logs", help="输出目录（默认 search_logs）")
    args = ap.parse_args()
    crawl(args.keyword, args.max_pages, Path(args.output_dir))
