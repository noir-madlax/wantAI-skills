---
name: youtube-justoneapi
description: 当用户需要爬取或采集 YouTube 数据时触发，包括：抓取频道（Channel）下的全部视频列表、视频元数据（标题、描述、播放量、点赞数、时长、封面等）、视频评论与子评论（回复）等场景。常见用途：博主/频道监控、内容矩阵分析、舆情分析、评论情感分析、KOL 调研。通过 JustOneAPI 调用 YouTube 接口获取数据。
---

# YouTube 数据采集 —— JustOneAPI

使用 JustOneAPI 调用 YouTube 接口抓取数据。

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

## 接口目录

根据用户意图，按需读取对应文件，**不要自行重写脚本**。

| 用户意图 | 接口定义 | 脚本 |
|----------|----------|------|
| 抓取频道全部视频 / 内容矩阵分析 / 频道监控 | `apis/get_channel_videos.md` | `scripts/get_channel_videos.py` |
| 抓取视频评论 + 子评论 / 舆情分析 / 情感分析 | `apis/get_video_comments.md` | `scripts/get_video_comments.py` |

## 翻页机制

- **频道视频**、**顶层评论**：使用响应根的 `data.continuation_token` 作为下一页的 `continuationToken` 参数。
- **子评论**：来源为顶层评论中的 `reply_continuation_token`，传给 `video-sub-comment-list/v1` 的 `continuationToken`；后续翻页继续使用该接口返回的 `data.continuation_token`。
- **comment_id 命名约定**：子评论 `comment_id` 形如 `<父评论id>.<子id>`，可由此还原父子关系。

## 运行方式

所有脚本统一使用 `uv run` 执行，无需手动安装依赖：

```bash
# 安装 uv（若尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 直接运行，uv 自动处理依赖
uv run scripts/get_channel_videos.py <channel_id> [--output-dir DIR] [--max-pages N]
uv run scripts/get_video_comments.py <video_id> [--output-dir DIR] [--no-replies] [--max-top N]

# 示例
uv run scripts/get_channel_videos.py UCxxxxxxxxxxxxxxxx --output-dir ./output
uv run scripts/get_channel_videos.py UCxxxxxxxxxxxxxxxx --output-dir ./output --max-pages 5
uv run scripts/get_video_comments.py 1uu4E8xtY7M --output-dir ./output
uv run scripts/get_video_comments.py 1uu4E8xtY7M --no-replies            # 仅抓顶层评论
uv run scripts/get_video_comments.py 1uu4E8xtY7M --max-top 100           # 顶层评论达到 100 条即停止翻页
```

## 输出与断点续传

- **CSV 输出**（追加写入，跨次去重）：
  - `get_channel_videos.py` → `<output-dir>/yt_videos.csv`
  - `get_video_comments.py` → `<output-dir>/yt_comments.csv`
- **进度文件**（中断后再次执行同一命令即自动续传）：
  - `<output-dir>/.yt_videos_progress.json`
  - `<output-dir>/.yt_comments_progress.json`（含 `stage`：`top` → `sub` 两阶段）
- **失败兜底**：后端 upsert 失败的条目落到 `yt_videos_failed.jsonl` / `yt_comments_failed.jsonl`，不影响 CSV 与本地进度。

## 后端入库

每页抓到的新数据会先调用 GoodGame 后端接口批量 upsert，再写入 CSV：

| 数据 | 接口 | 业务唯一键 |
|------|------|------------|
| 频道视频 | `POST /api/skill/youtube/videos/upsert` | `(channel_id, video_id)` |
| 视频评论 | `POST /api/skill/youtube/comments/upsert` | `comment_id` |

请求体格式：`{ "trace_id": "...", "items": [...] }`，后端按唯一键 `ON CONFLICT` 更新。
