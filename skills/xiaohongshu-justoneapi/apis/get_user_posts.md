# 接口：小红书用户笔记列表 (V4)

获取指定用户发布的全部笔记，支持游标翻页，适用于内容分析、竞品监控、KOL 内容采集等场景。

## 请求

```
GET https://api.justoneapi.com/api/xiaohongshu/get-user-note-list/v4
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `userId` | ✅ | string | — | 小红书用户 ID（非小红书号，是内部 userId） |
| `lastCursor` | ❌ | string | — | 翻页游标；**首页不传**，后续页取上一页最后一条 note 的 `cursor` 字段 |

## 响应

### 结构

```json
{
  "code": 0,
  "data": {
    "has_more": true,
    "notes": [
      {
        "id": "笔记 ID",
        "cursor": "翻页游标（取该字段传给下一页 lastCursor）",
        "title": "笔记标题",
        "display_title": "展示标题（title 为空时使用）",
        "desc": "笔记正文",
        "type": "normal | video",
        "sticky": false,
        "create_time": 1735689600,
        "likes": 1234,
        "comments_count": 56,
        "collected_count": 789,
        "share_count": 12,
        "images_list": [
          { "url": "封面图 URL" }
        ],
        "user": {
          "userid": "作者用户 ID",
          "nickname": "作者昵称"
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
| `data.has_more` | boolean | `true` 表示还有下一页 |
| `data.notes` | array | 当页笔记列表 |
| `id` | string | 笔记唯一 ID |
| `cursor` | string | **翻页游标**，取最后一条 note 的此字段作为下一页 `lastCursor` |
| `title` / `display_title` | string | 笔记标题，优先取 `title`，为空则取 `display_title` |
| `desc` | string | 笔记正文 |
| `type` | string | `normal`（图文）/ `video`（视频） |
| `sticky` | boolean | 是否置顶 |
| `create_time` | integer | 发布时间，Unix 时间戳（秒） |
| `likes` | integer | 点赞数 |
| `comments_count` | integer | 评论数 |
| `collected_count` | integer | 收藏数 |
| `share_count` | integer | 分享数 |
| `images_list[0].url` | string | 封面图 URL |
| `user.userid` | string | 作者用户 ID |
| `user.nickname` | string | 作者昵称 |

### 分页

1. 首页：不传 `lastCursor`
2. 翻页：取响应中 **最后一条** note 的 `cursor` 字段，作为下一次请求的 `lastCursor`
3. 终止条件：`data.has_more` 为 `false`，或 `data.notes` 为空数组
