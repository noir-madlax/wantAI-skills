---
name: douyin-justoneapi
description: 当用户需要爬取或采集抖音（Douyin）数据时触发，包括：抓取指定用户发布的视频（账号监控、KOL 内容分析、竞品研究），采集视频评论与评论回复（舆情、情感分析、互动研究）等场景。通过 JustOneAPI 调用抖音接口获取数据，每页先 upsert 到 GoodGame 后端再落 CSV。
---

# 抖音数据采集 —— JustOneAPI

使用 JustOneAPI 调用抖音接口抓取数据。

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

## 抖音 ID 速查

抖音同一对象有多种 ID，调用不同接口时要分清楚：

| 名称 | 形态 | 说明 / 用途 |
|------|------|------|
| `sec_uid` | 长串字母数字（以 `MS4w` 开头） | 用户加密 ID；**用户发布视频接口必填** |
| `aweme_id` | 19 位数字 | 视频唯一 ID；视频 URL `douyin.com/video/{aweme_id}` 用的就是它；**视频评论接口必填** |
| `cid` / `comment_id` | 长数字 | 评论 ID；**评论回复接口必填** |

> 评论回复接口本身只需 `commentId`，但脚本会同时把 `aweme_id` 透传给后端 upsert（评论表的复合唯一键是 `(aweme_id, comment_id)`）。

## 接口目录

根据用户意图，按需读取对应文件，**不要自行重写脚本**。

| 用户意图 | 接口定义 | 脚本 |
|----------|----------|------|
| 抓取用户发布的视频 / 账号监控 / KOL 内容分析 / 竞品研究 | `apis/get_user_videos.md` | `scripts/get_user_videos.py` |
| 抓取视频评论 / 评论回复 / 舆情分析 / 情感分析 | `apis/get_video_comments.md` | `scripts/get_video_comments.py` |

## 运行方式

所有脚本统一使用 `uv run` 执行，无需手动安装依赖：

```bash
# 安装 uv（若尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 直接运行，uv 自动处理依赖
uv run scripts/get_user_videos.py <sec_uid> [sec_uid2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]
uv run scripts/get_video_comments.py <aweme_id> [aweme_id2 ...] [--output-dir DIR] [--max-top N] [--no-replies]

# 示例：抓取某 KOL 的发布视频，2025-01-01 之后
uv run scripts/get_user_videos.py MS4wLjABAAAA_demo --output-dir ./output --since 2025-01-01

# 示例：抓取单个视频的全部评论与回复
uv run scripts/get_video_comments.py 7300000000000000000 --output-dir ./output

# 示例：仅抓顶层评论，本次最多 200 条
uv run scripts/get_video_comments.py 7300000000000000000 --max-top 200 --no-replies
```

## 数据落地

每个脚本运行后会在 `--output-dir` 下生成：

| 文件 | 说明 |
|------|------|
| `douyin_videos.csv` / `douyin_video_comments.csv` | 主数据文件（追加写入，自动跨次去重） |
| `.douyin_*_progress.json` | 断点进度（中途失败/中断后再次运行同命令即可续传） |
| `douyin_*_failed.jsonl` | 后端 upsert 失败的整页 payload，便于事后补传 |

每页数据**先 upsert 到 GoodGame 后端**（接口见下表），再写入 CSV。后端 upsert 失败不会中断流程，相应数据会落到 `*_failed.jsonl`。

| 数据类型 | 后端 upsert 接口 |
|----------|------------------|
| 视频 | `POST https://www.goodgame.monster/api/skill/douyin/videos/upsert` |
| 评论 | `POST https://www.goodgame.monster/api/skill/douyin/video-comments/upsert` |
