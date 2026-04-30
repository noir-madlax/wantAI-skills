---
name: facebook-rapidapi
description: 当用户需要爬取或采集 Facebook 主页（Page / Profile）公开帖子数据时触发，包括：抓取指定主页发布的帖子（内容分析、KOL 监控、品牌/竞品研究）、统计互动数据（reactions / comments / shares）、获取 Reels 视频信息等场景。通过 RapidAPI 的 facebook-scraper3 接口获取数据。
---

# Facebook 数据采集 —— RapidAPI

使用 RapidAPI 上的 `facebook-scraper3` 服务调用 Facebook 接口抓取主页帖子。

> **渠道说明**：本 skill 不是 JustOneAPI，鉴权方式与 `*-justoneapi` 系列不同 —— 通过 HTTP Header 传递 `x-rapidapi-key`，环境变量名为 `RAPIDAPI_KEY`。

## 前置：获取 RapidAPI Key

所有接口均通过 HTTP Header `x-rapidapi-key` 鉴权。按以下优先级获取：

1. 从当前目录向上逐级查找 `.env` 文件，匹配 `RAPIDAPI_KEY` 或 `RAPIDAPI_API_KEY`
2. 读取系统环境变量 `RAPIDAPI_KEY` 或 `RAPIDAPI_API_KEY`
3. 均未找到则报错退出，提示用户在 `.env` 中添加 key

生成代码时 key 须从环境变量读取，不要硬编码：

```
RAPIDAPI_KEY=your_rapidapi_key_here
```

## 错误处理（HTTP 状态码 + 响应体）

> ⚠️ RapidAPI 没有 JustOneAPI 风格的业务 `code` 字段，**仅靠 HTTP 状态码 + 响应体是否含 `results` 字段** 判断成败。

| 信号 | 含义 | 处理策略 |
|------|------|----------|
| HTTP 200 + 响应含 `results` 数组 | 成功 | 正常处理 |
| HTTP 200 + 响应缺少 `results` | 数据异常 | 自动重试，最多 5 次 |
| HTTP 401 / 403 | RapidAPI Key 无效或未订阅该 API | 立即终止，提示检查 `RAPIDAPI_KEY` |
| HTTP 429 | 触发速率限制 | 等待后重试 |
| HTTP 5xx / 网络异常 | 服务端 / 网络故障 | 自动重试 |

## Facebook ID 速查

| 名称 | 形态 | 说明 |
|------|------|------|
| `profile_id` | 长数字字符串，如 `100078792651602` | 主页内部数字 ID，本接口的**必填入参** |
| `post_id` | 长数字字符串，如 `923954776907602` | 帖子原生 ID，作为去重 / 唯一键 |

`profile_id` 可在主页 URL 源码中查找（搜索 `pageID` / `entity_id`），或用浏览器插件如 "Find my Facebook ID" 拿到。

## 接口目录

根据用户意图，按需读取对应文件，**不要自行重写脚本**。

| 用户意图 | 接口定义 | 脚本 |
|----------|----------|------|
| 抓取主页发布的帖子 / Reels / 内容分析 / 互动统计 | `apis/get_profile_posts.md` | `scripts/get_profile_posts.py` |

## 运行方式

所有脚本统一使用 `uv run` 执行，无需手动安装依赖：

```bash
# 安装 uv（若尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 抓取一个或多个主页（profile_id 可传多个）
uv run scripts/get_profile_posts.py <profile_id> [profile_id2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N] [--max-pages N]

# 示例：抓取 BYD Global 主页 2025-01-01 之后的帖子
uv run scripts/get_profile_posts.py 100078792651602 --output-dir ./output --since 2025-01-01

# 示例：并发抓取多个主页，每个主页最多翻 3 页
uv run scripts/get_profile_posts.py 100078792651602 100064959991036 --output-dir ./output --workers 3 --max-pages 3
```

## 数据落地

每个脚本运行后会在 `--output-dir` 下生成：

| 文件 | 说明 |
|------|------|
| `fb_posts.csv` | 主数据文件（追加写入，自动跨次去重） |
| `.fb_posts_progress.json` | 断点进度（中途失败/中断后再次运行同命令即可续传） |
| `fb_posts_failed.jsonl` | 后端 upsert 失败的整页 payload，便于事后补传 |

每页数据**先 upsert 到 GoodGame 后端**（接口见下表），再写入 CSV。后端 upsert 失败不会中断流程，相应数据会落到 `*_failed.jsonl`。

| 数据类型 | 后端 upsert 接口 |
|----------|------------------|
| 帖子 | `POST https://www.goodgame.monster/api/skill/fb/posts/upsert` |
