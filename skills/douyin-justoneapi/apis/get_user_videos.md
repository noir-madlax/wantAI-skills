# 接口：抖音用户发布视频 (V3)

获取指定抖音用户发布的全部视频，支持游标翻页，适用于账号监控、KOL 内容分析、竞品研究等场景。

## 请求

```
GET https://api.justoneapi.com/api/douyin/get-user-video-list/v3
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `secUid` | ✅ | string | — | 抖音用户的加密 ID（`sec_uid`），形如 `MS4wLjABAAAA...` |
| `maxCursor` | ❌ | integer | `0` | 翻页游标；**首页传 0**，后续传上一页响应的 `max_cursor` |

> ⚠️ 部分用户的最新视频可能无法访问（接口本身限制）。

## 响应

### 结构（字段以实际响应为准；以下为常见字段示意）

```json
{
  "code": 0,
  "data": {
    "max_cursor": 1735000000000,
    "has_more": true,
    "aweme_list": [
      {
        "aweme_id": "7300000000000000000",
        "desc": "视频文案",
        "create_time": 1735689600,
        "duration": 45000,
        "aweme_type": 0,
        "is_top": 0,
        "share_url": "https://www.iesdouyin.com/share/video/...",
        "video": {
          "duration": 45000,
          "cover": { "url_list": ["https://..."] },
          "play_addr": { "url_list": ["https://..."] }
        },
        "statistics": {
          "aweme_id": "7300000000000000000",
          "digg_count": 12345,
          "comment_count": 678,
          "share_count": 90,
          "collect_count": 100,
          "play_count": 500000
        },
        "author": {
          "uid": "1234567890",
          "sec_uid": "MS4wLjABAAAA...",
          "short_id": "12345",
          "nickname": "示例作者",
          "avatar_thumb": { "url_list": ["https://..."] }
        }
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 业务状态码，`0` 为成功，见错误码表 |
| `data.max_cursor` | integer | 下一页 `maxCursor` 取值（毫秒级时间戳形态游标） |
| `data.has_more` | boolean | `true` 表示还有下一页 |
| `data.aweme_list` | array | 当页视频列表 |
| `aweme_list[].aweme_id` | string | 视频唯一 ID（业务主键） |
| `aweme_list[].desc` | string | 视频文案 |
| `aweme_list[].create_time` | integer | 发布时间，Unix 时间戳（秒） |
| `aweme_list[].duration` / `video.duration` | integer | 时长（毫秒） |
| `aweme_list[].aweme_type` | integer | 媒体类型（图文 / 视频 / 直播回放等） |
| `aweme_list[].is_top` | integer | 是否置顶 (0/1) |
| `aweme_list[].share_url` | string | 分享链接 |
| `aweme_list[].video.cover.url_list[0]` | string | 封面图 URL |
| `aweme_list[].video.play_addr.url_list[0]` | string | 视频播放 URL |
| `aweme_list[].statistics.digg_count` | integer | 点赞数 |
| `aweme_list[].statistics.comment_count` | integer | 评论数 |
| `aweme_list[].statistics.share_count` | integer | 分享数 |
| `aweme_list[].statistics.collect_count` | integer | 收藏数 |
| `aweme_list[].statistics.play_count` | integer | 播放数 |
| `aweme_list[].author.uid` | string | 作者数字 UID |
| `aweme_list[].author.sec_uid` | string | 作者加密 ID |
| `aweme_list[].author.short_id` | string | 作者抖音号 |
| `aweme_list[].author.nickname` | string | 作者昵称 |
| `aweme_list[].author.avatar_thumb.url_list[0]` | string | 作者头像 URL |

> ⚠️ 字段名兜底：脚本中已对 `aweme_list` / `videos` / `items`、`max_cursor` / `cursor`、`has_more` / `more_available` 等做了多名称兜底。

### 分页

1. 首页：`maxCursor=0`（或不传，接口默认 0）
2. 翻页：取响应中 `data.max_cursor` 作为下一次请求的 `maxCursor`
3. 终止条件：`data.has_more` 为 `false`，或 `max_cursor` 为 0/空，或 `aweme_list` 为空数组
