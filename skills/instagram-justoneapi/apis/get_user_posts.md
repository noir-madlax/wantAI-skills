# 接口：Instagram 用户发布帖子 (V1)

获取指定用户发布的全部帖子，支持游标翻页，适用于内容分析、KOL 监控、竞品研究等场景。

## 请求

```
GET https://api.justoneapi.com/api/instagram/get-user-posts/v1
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `username` | ✅ | string | — | Instagram 用户名（不带 `@`） |
| `paginationToken` | ❌ | string | — | 翻页游标；**首页不传**，后续页取上一页响应的 `next_pagination_token` 字段 |

## 响应

### 结构（字段以实际响应为准；以下为常见字段示意）

```json
{
  "code": 0,
  "data": {
    "next_pagination_token": "xxx",
    "more_available": true,
    "posts": [
      {
        "code": "C1abc23XYZ",
        "id": "3123456789012345678_1234567",
        "pk": "3123456789012345678",
        "media_type": 1,
        "product_type": "feed",
        "caption": { "text": "正文内容" },
        "taken_at": 1735689600,
        "like_count": 1234,
        "comment_count": 56,
        "play_count": null,
        "view_count": null,
        "thumbnail_url": "https://...",
        "video_url": "https://...",
        "user": {
          "pk": "1234567",
          "username": "nasa",
          "full_name": "NASA"
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
| `data.next_pagination_token` | string | 下一页 `paginationToken` 取值 |
| `data.more_available` | boolean | `true` 表示还有下一页 |
| `data.posts` | array | 当页帖子列表 |
| `posts[].code` | string | 帖子 shortcode（业务主键，URL 用） |
| `posts[].pk` / `posts[].id` | string | 帖子数字 media id（评论回复接口必填） |
| `posts[].media_type` | integer | `1`=图片，`2`=视频，`8`=carousel（多图） |
| `posts[].product_type` | string | `feed` / `clips`（reels）/ `igtv` 等 |
| `posts[].caption.text` | string | 正文内容 |
| `posts[].taken_at` | integer | 发布时间，Unix 时间戳（秒） |
| `posts[].like_count` | integer | 点赞数 |
| `posts[].comment_count` | integer | 评论数 |
| `posts[].play_count` | integer\|null | 视频播放数（无则 NULL） |
| `posts[].view_count` | integer\|null | reels 观看数 |
| `posts[].thumbnail_url` | string | 封面图 URL |
| `posts[].video_url` | string | 视频 URL（若有） |
| `posts[].user.pk` | string | 作者数字 ID |
| `posts[].user.username` | string | 作者用户名 |
| `posts[].user.full_name` | string | 作者展示名 |

> ⚠️ 字段名兼容：脚本中已对 `posts` / `items` / `data` 列表节点、`pk` / `id` / `media_id` 数字 ID、`next_pagination_token` / `pagination_token` / `next_max_id` 翻页游标做了多名称兜底。

### 分页

1. 首页：不传 `paginationToken`
2. 翻页：取响应中 `data.next_pagination_token`，作为下一次请求的 `paginationToken`
3. 终止条件：`data.more_available` 为 `false`，或 `next_pagination_token` 为空，或 `data.posts` 为空数组
