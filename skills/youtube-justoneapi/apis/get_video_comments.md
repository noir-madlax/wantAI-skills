# 接口：YouTube 视频评论 (V1)

获取 YouTube 视频评论数据，包含**顶层评论**与**子评论（回复）**两个接口；二者通常配套使用：先翻顶层评论，再对带 `reply_continuation_token` 的评论拉取回复。适用于评论采集、舆情/情感分析、社区监控等场景。

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

## 1. 顶层评论

### 请求

```
GET https://api.justoneapi.com/api/youtube/get-video-comment/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `videoId` | ✅ | string | — | YouTube 视频 ID |
| `continuationToken` | ❌ | string | — | 翻页游标；**首页不传**，后续传上一页响应的 `data.continuation_token` |

### 响应

```json
{
  "code": 0,
  "data": {
    "comments": [
      {
        "comment_id": "UgxL4F9SiL-Zmhepp9N4AaABAg",
        "content": "评论文本",
        "published_time": "2天前",
        "reply_level": 0,
        "like_count": "258",
        "like_count_a11y": "258 次赞",
        "reply_count": "13",
        "reply_count_a11y": "13 条回复",
        "reply_count_text": "13 条回复",
        "author": {
          "channel_id": "UCglR8_mzhc1UVRSf8bfScMg",
          "display_name": "@danieldiiworkout",
          "channel_url": "https://www.youtube.com/@danieldiiworkout",
          "avatar_url": "https://yt3.ggpht.com/...",
          "avatar_thumbnails": [ {"url": "...", "width": 88, "height": 88} ],
          "is_verified": false,
          "is_creator": false,
          "is_artist": false
        },
        "creator_thumbnail_url": null,
        "reply_continuation_token": "Eg0SCzF1dTRFOHh0WTdN..."
      }
    ],
    "continuation_token": "Eg0SCzF1dTRFOHh0WTdNGAYy..."
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `comments[].comment_id` | 评论 ID |
| `comments[].reply_level` | `0`=顶层 / `1`=子评论 |
| `comments[].like_count` / `reply_count` | 字符串数字，需正则转 `int` |
| `comments[].author.channel_id` | 评论作者频道 ID（即作者 ID） |
| `comments[].author.is_creator` | 是否视频作者本人 |
| `comments[].reply_continuation_token` | 拉取该评论子评论的游标；**为空表示该评论无回复**，无需调用子评论接口 |
| `data.continuation_token` | 下一页顶层评论游标；为空/null 表示已到末页 |

## 2. 子评论（回复）

### 请求

```
GET https://api.justoneapi.com/api/youtube/get-video-sub-comment/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `videoId` | ✅ | string | — | 视频 ID（与顶层评论同一视频） |
| `commentId` | ✅ | string | — | 顶层评论 `comment_id` |
| `continuationToken` | ✅ | string | — | **首页**传顶层评论的 `reply_continuation_token`；后续翻页传本接口响应的 `data.continuation_token` |

### 响应

```json
{
  "code": 0,
  "data": {
    "comments": [
      {
        "comment_id": "UgxL4F9SiL-Zmhepp9N4AaABAg.AWM9lxQblrsAWMFsatzLqx",
        "content": "Thanks bro",
        "published_time": "2天前",
        "reply_level": 1,
        "like_count": "3",
        "reply_count": "0",
        "author": { "channel_id": "UCyMpWsfILAAYBxMPKOlfpdw", "display_name": "@awesomereviews1561", "...": "..." },
        "creator_thumbnail_url": null
      }
    ],
    "continuation_token": null
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `comments[].comment_id` | 形如 `<父评论id>.<子id>`，可由此还原父子关系 |
| `comments[].reply_level` | 固定为 `1` |
| `data.continuation_token` | 下一页子评论游标；为空/null 表示该顶层评论的回复已拉完 |

> ⚠️ YouTube 评论只有两层（顶层 + 回复）。子评论之间的「@回复」关系不在响应里直接给出，仅通过 `comment_id` 的前缀可以确定其所属顶层评论。

## 分页

两个接口分页方式一致：

1. 首页：顶层评论不传 `continuationToken`；子评论首页用顶层评论的 `reply_continuation_token`
2. 翻页：取响应中 `data.continuation_token` 作为下一次请求的 `continuationToken`
3. 终止条件：`data.continuation_token` 为空/null，或 `data.comments` 为空

## 配套用法

1. 调用「顶层评论」翻完所有页
2. 收集本页中 `reply_continuation_token` 非空且 `reply_count > 0` 的评论
3. 对每条评论用其 `reply_continuation_token` 调用「子评论」翻完所有页（`commentId` 传顶层评论 ID）
4. 入库映射：
   - **顶层评论**：`is_sub=0`，`parent_comment_id=NULL`，`root_comment_id = 自身 comment_id`
   - **子评论**：`is_sub=1`，`parent_comment_id = comment_id` 中 `.` 之前部分，`root_comment_id = 顶层评论 id`
