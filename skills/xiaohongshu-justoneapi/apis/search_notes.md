# 接口：小红书笔记搜索 (V3)

按关键词搜索小红书笔记，适用于话题发现、内容分析、竞品监控、舆情追踪等场景。

## ⚠️ 稳定性警告：该接口较不稳定

调用代码**必须**实现充分的重试机制：

- **HTTP 状态码非 200**：视为请求失败，须重试
- **HTTP 200 但 `code` 非 0**：视为业务失败，须重试（不可恢复的错误码除外）
- 建议重试上限设为 **5 次**，每次间隔递增（2s、4s、6s、8s、10s）
- `code=302`（速率限制）时等待时间应更长（5s、10s、15s……）

不可重试的错误码（客户端侧无法修复）：`100`、`303`、`400`、`600`、`601`

## 请求

```
GET https://api.justoneapi.com/api/xiaohongshu/search-note/v3
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `keyword` | ✅ | string | — | 搜索关键词 |
| `page` | ❌ | integer | `1` | 页码，用于翻页，每页约 20 条 |
| `sort` | ❌ | string | `general` | 排序方式，见下表 |
| `noteType` | ❌ | string | `_0` | 笔记类型过滤，见下表 |

#### `sort` 可选值

| 值 | 含义 |
|----|------|
| `general` | 综合（默认） |
| `popularity_descending` | 热门 |
| `time_descending` | 最新 |

#### `noteType` 可选值

| 值 | 含义 |
|----|------|
| `_0` | 全部类型（默认） |
| `_1` | 仅视频 |
| `_2` | 仅普通图文 |

### 翻页限制

> 调用方**必须**设置最大翻页数上限，不允许无限翻页：
> - 翻页过多会快速消耗每日配额（触发 `code=303`）
> - 大量快速请求会触发速率限制（触发 `code=302`）
> - 建议上限 ≤ 50 页；页数越多，遇到不稳定失败的概率越高

## 响应

### 结构

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "model_type": "note",
        "note": {
          "id": "笔记 ID",
          "type": "normal | video",
          "title": "笔记标题（可能为空）",
          "desc": "笔记正文",
          "abstract_show": "摘要（title 为空时用作替代）",
          "timestamp": 1750039714,
          "liked_count": 85,
          "comments_count": 106,
          "collected_count": 9,
          "shared_count": 8,
          "xsec_token": "YBo...",
          "user": {
            "userid": "用户内部 ID",
            "nickname": "昵称",
            "red_id": "小红书号",
            "images": "头像 URL"
          },
          "images_list": [
            {
              "url": "封面缩略图 URL（可能为空，备用 url_size_large）",
              "url_size_large": "大图 URL",
              "width": 1910,
              "height": 2560
            }
          ]
        }
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 业务状态码，`0` 为成功，见主文档错误码表 |
| `data.items` | array | 当页结果列表 |
| `items[].model_type` | string | 条目类型，只处理值为 `"note"` 的条目 |
| `items[].note.id` | string | 笔记唯一 ID |
| `items[].note.type` | string | `normal`（图文）/ `video`（视频） |
| `items[].note.title` | string | 标题，可能为空，空时取 `abstract_show` |
| `items[].note.desc` | string | 笔记正文 |
| `items[].note.timestamp` | integer | 发布时间，Unix 时间戳（秒） |
| `items[].note.liked_count` | integer | 点赞数 |
| `items[].note.comments_count` | integer | 评论数 |
| `items[].note.collected_count` | integer | 收藏数 |
| `items[].note.shared_count` | integer | 分享数 |
| `items[].note.user.userid` | string | 作者内部用户 ID（可用于 get_user_posts 接口） |
| `items[].note.user.nickname` | string | 作者昵称 |
| `items[].note.user.red_id` | string | 作者小红书号 |
| `items[].note.images_list[0].url` | string | 封面缩略图，`url` 为空时取 `url_size_large` |

### 分页

- 递增 `page` 翻页，每页约 20 条结果
- `data.items` 返回空数组时表示已到末页
- **调用方须自行设置最大翻页数**（见上方翻页限制）
