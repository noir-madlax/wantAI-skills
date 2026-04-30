# 接口：抖音视频评论 (V1)

获取抖音视频评论数据，包含**视频评论**与**评论回复**两个接口；二者通常配套使用：先翻视频顶层评论，再对 `reply_comment_total > 0` 的评论拉取回复。适用于评论采集、舆情/情感分析、互动研究等场景。

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

> ⚠️ 抖音评论分页采用**页码**（`page`，从 1 开始），与小红书 / IG 的游标分页不同。

## 1. 视频评论（顶层）

### 请求

```
GET https://api.justoneapi.com/api/douyin/get-video-comment/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `awemeId` | ✅ | string | — | 视频唯一 ID（`aweme_id`） |
| `page` | ❌ | integer | `1` | 页码（从 1 开始） |

### 响应（字段以实际响应为准；常见结构如下）

```json
{
  "code": 0,
  "data": {
    "has_more": true,
    "total": 808,
    "cursor": 20,
    "comments": [
      {
        "cid": "7300000000000000001",
        "aweme_id": "7300000000000000000",
        "text": "评论文本",
        "create_time": 1735660800,
        "digg_count": 12,
        "reply_comment_total": 3,
        "ip_label": "广东",
        "user": {
          "uid": "1234567890",
          "sec_uid": "MS4wLjABAAAA...",
          "short_id": "12345",
          "nickname": "评论者",
          "avatar_thumb": { "url_list": ["https://..."] }
        }
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `data.has_more` | 是否还有下一页（`1`/`true` 表示还有） |
| `data.total` | 评论总数（仅作展示，分页仍以 `has_more` 为准） |
| `comments[].cid` / `comments[].id` | 评论 ID |
| `comments[].aweme_id` | 所属视频 ID |
| `comments[].text` | 评论内容 |
| `comments[].create_time` | 发布时间，Unix 时间戳（秒） |
| `comments[].digg_count` | 点赞数 |
| `comments[].reply_comment_total` | 该评论下的回复数；>0 时调用「评论回复」接口拉取 |
| `comments[].ip_label` | IP 属地 |
| `comments[].user` | 评论者基本信息 |

## 2. 评论回复（子评论）

### 请求

```
GET https://api.justoneapi.com/api/douyin/get-video-sub-comment/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `commentId` | ✅ | string | — | 顶层评论 ID（`cid`） |
| `page` | ❌ | integer | `1` | 页码（从 1 开始） |

> ⚠️ 此接口本身不传 `awemeId`；写入存储时所属视频 ID 由调用方（脚本）维护。

### 响应

```json
{
  "code": 0,
  "data": {
    "has_more": true,
    "comments": [
      {
        "cid": "7300000000000000002",
        "reply_id": "7300000000000000001",
        "reply_to_reply_id": "0",
        "text": "回复内容",
        "create_time": 1735661000,
        "digg_count": 1,
        "ip_label": "北京",
        "user": { "uid": "...", "sec_uid": "...", "nickname": "...", "avatar_thumb": {"url_list": ["..."]} }
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `comments[].reply_id` | 该回复所属的顶层评论 ID（即调用接口时传入的 `commentId`） |
| `comments[].reply_to_reply_id` | 该回复直接回复的目标评论 ID；为 `"0"` 时表示直接回复顶层 |

> ⚠️ 抖音评论结构上视为两层（楼 + 楼中楼）。`reply_to_reply_id` 不一定等于顶层评论 ID；写入存储时区分 `parent_comment_id`（直接被回复，取自 `reply_to_reply_id`，为 0 时回退到顶层 ID）与 `root_comment_id`（所属顶层）。

## 分页

两个接口均使用页码分页：

1. 首页：`page=1`（或不传，接口默认 1）
2. 翻页：`page` 自增 +1
3. 终止条件：`has_more = false / 0`，或 `comments` 为空数组

## 配套用法

1. 调用「视频评论」翻完所有页（同时记录每条评论的 `cid` 与 `reply_comment_total`）
2. 收集 `reply_comment_total > 0` 的评论 ID
3. 对每个评论 ID 调用「评论回复」翻完所有页（`commentId` 传顶层评论 `cid`）
4. 入库映射：
   - **顶层评论**：`is_sub=0`，`parent_comment_id=NULL`，`root_comment_id = 自身 cid`
   - **子评论**：`is_sub=1`，`parent_comment_id = reply_to_reply_id`（为 `"0"` 时回退到顶层 cid），`root_comment_id = 顶层 cid`
