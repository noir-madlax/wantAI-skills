---
name: instagram-justoneapi
description: 当用户需要爬取或采集 Instagram 数据时触发，包括：抓取指定用户发布的帖子（内容分析、KOL 监控、竞品研究），采集帖子评论与评论回复（舆情、情感分析、社区互动）等场景。通过 JustOneAPI 调用 Instagram 接口获取数据。
---

# Instagram 数据采集 —— JustOneAPI

使用 JustOneAPI 调用 Instagram 接口抓取数据。

## 前置：获取 Token

所有接口均通过 query 参数 `token` 鉴权。按以下优先级获取 token：

1. 从当前目录向上逐级查找 `.env` 文件，匹配 `JUSTONEAPI_TOKEN` 或 `JUST_ONE_API_TOKEN`
2. 读取系统环境变量 `JUSTONEAPI_TOKEN` 或 `JUST_ONE_API_TOKEN`
3. 均未找到则报错退出，提示用户在 `.env` 中添加 token

生成代码时，token 应从环境变量读取，不要硬编码到代码中：

```
JUSTONEAPI_TOKEN=your_token_here
```

## 错误码（所有接口通用）

> ⚠️ `code` 在**响应体**中，不是 HTTP 状态码。HTTP 200 也须检查 `code`。

| `code` | 含义 | 处理策略 |
|:------:|------|----------|
| `0` | 成功 | 正常处理 |
| `100` | Token 无效或已失效 | 提示用户检查 token |
| `301` | 采集失败 | **自动重试**，间隔 2-3 秒，最多 3 次 |
| `302` | 超出速率限制 | 降低请求频率，等待后重试 |
| `303` | 超出每日配额 | 告知用户当日配额已用尽 |
| `400` | 参数错误 | 检查必填参数是否缺失或格式有误 |
| `500` | 服务器内部错误 | 稍后重试，持续则反馈 JustOneAPI |
| `600` | 权限不足 | 告知用户当前 token 无此接口权限 |
| `601` | 余额不足 | 告知用户需在 JustOneAPI 充值 |

## Instagram ID 速查

IG 同一条帖子有两种 ID，调用不同接口时要分清楚：

| 名称 | 形态 | 说明 / 用途 |
|------|------|------|
| `code`（shortcode） | 11 位字母数字，如 `C1abc23XYZ` | 帖子 URL `instagram.com/p/{code}/` 用的就是它；**评论列表接口必填** |
| `media_id`（pk / id） | 长数字，如 `3123456789012345678` | 内部数字 ID；**评论回复接口必填** |

评论脚本会优先使用用户传入的 `media_id`，若未传则尝试从评论接口的响应中自动提取（多数情况下 `media_id` 会带在评论数据里）。

## 接口目录

根据用户意图，按需读取对应文件，**不要自行重写脚本**。

| 用户意图 | 接口定义 | 脚本 |
|----------|----------|------|
| 抓取用户发布的帖子 / 内容分析 / KOL 监控 / 竞品研究 | `apis/get_user_posts.md` | `scripts/get_user_posts.py` |
| 抓取帖子评论 / 评论回复 / 舆情分析 / 情感分析 | `apis/get_post_comments.md` | `scripts/get_post_comments.py` |

## 运行方式

所有脚本统一使用 `uv run` 执行，无需手动安装依赖：

```bash
# 安装 uv（若尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 直接运行，uv 自动处理依赖
uv run scripts/get_user_posts.py <username> [username2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]
uv run scripts/get_post_comments.py <code[:media_id]> [code2[:media_id2] ...] [--output-dir DIR] [--sort newest|popular] [--max-top N] [--no-replies]

# 示例：抓取 NASA 与 natgeo 的帖子，2025-01-01 之后
uv run scripts/get_user_posts.py nasa natgeo --output-dir ./output --since 2025-01-01

# 示例：抓取单个帖子的全部评论与回复（自动从评论响应里提取 media_id）
uv run scripts/get_post_comments.py C1abc23XYZ --output-dir ./output

# 示例：手动指定 media_id（推荐，跳过自动探测，更稳）
uv run scripts/get_post_comments.py C1abc23XYZ:3123456789012345678 --output-dir ./output

# 示例：仅抓顶层评论，按热门排序
uv run scripts/get_post_comments.py C1abc23XYZ --sort popular --no-replies

# 示例：本次最多新增 200 条顶层评论后停止翻页
uv run scripts/get_post_comments.py C1abc23XYZ --max-top 200
```

## 数据落地

每个脚本运行后会在 `--output-dir` 下生成：

| 文件 | 说明 |
|------|------|
| `ig_posts.csv` / `ig_post_comments.csv` | 主数据文件（追加写入，自动跨次去重） |
| `.ig_*_progress.json` | 断点进度（中途失败/中断后再次运行同命令即可续传） |
| `ig_*_failed.jsonl` | 后端 upsert 失败的整页 payload，便于事后补传 |

每页数据**先 upsert 到 GoodGame 后端**（接口见下表），再写入 CSV。后端 upsert 失败不会中断流程，相应数据会落到 `*_failed.jsonl`。

| 数据类型 | 后端 upsert 接口 |
|----------|------------------|
| 帖子 | `POST https://www.goodgame.monster/api/skill/ig/posts/upsert` |
| 评论 | `POST https://www.goodgame.monster/api/skill/ig/post-comments/upsert` |
