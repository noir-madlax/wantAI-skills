# 接口：Facebook 主页帖子列表

获取指定 Facebook 主页（Page / Profile）公开发布的全部帖子，支持游标翻页，适用于内容分析、品牌/竞品监控、KOL 内容采集等场景。

## 请求

```
GET https://facebook-scraper3.p.rapidapi.com/profile/posts
```

### Headers

| Header | 必填 | 说明 |
|--------|:----:|------|
| `x-rapidapi-key` | ✅ | RapidAPI Key，对应环境变量 `RAPIDAPI_KEY` |
| `x-rapidapi-host` | ✅ | 固定值 `facebook-scraper3.p.rapidapi.com` |

### Query 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `profile_id` | ✅ | string | — | Facebook 主页数字 ID（如 `100078792651602`） |
| `cursor` | ❌ | string | — | 翻页游标；**首页不传**，后续页取上一页响应中的 `cursor` 字段 |

## 响应

### 结构

```json
{
  "results": [
    {
      "post_id": "923954776907602",
      "type": "post",
      "url": "https://www.facebook.com/BYDGlobal/posts/pfbid0xxx",
      "timestamp": 1775208113,
      "message": "帖子正文（含 #标签）",
      "message_rich": "帖子富文本",
      "comments_count": 0,
      "reactions_count": 5,
      "reshare_count": 1,
      "reactions": {
        "like": 5, "love": 0, "care": 0,
        "haha": 0, "wow": 0, "sad": 0, "angry": 0
      },
      "author": {
        "id": "100078792651602",
        "name": "BYD Global",
        "url": "https://www.facebook.com/BYDGlobal",
        "profile_picture_url": "https://..."
      },
      "image": {
        "uri": "https://...image.jpg",
        "id": "923954753574271",
        "width": 526,
        "height": 7074
      },
      "video": "https://www.facebook.com/reel/1314020283976225/",
      "video_files": {
        "video_sd_file": "https://....mp4",
        "video_hd_file": "https://....mp4"
      },
      "video_thumbnail": "https://...thumb.jpg",
      "album_preview": null,
      "external_url": null,
      "attached_event": null,
      "attached_post": null,
      "attached_post_url": null,
      "comments_id": "923954776907602",
      "shares_id": "923954776907602"
    }
  ],
  "cursor": "<下一页 cursor，缺失或为空表示已到末页>"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `results` | array | 当页帖子列表 |
| `cursor` | string | **翻页游标**，原样作为下一页 `cursor` 入参；**缺失或为空表示已到末页** |
| `post_id` | string | 帖子唯一 ID（用作去重键） |
| `type` | string | `post` / `reel` / `video` 等 |
| `url` | string | 帖子在 Facebook 的可访问 URL |
| `timestamp` | integer | 发布时间，Unix 时间戳（秒） |
| `message` | string | 帖子正文 |
| `message_rich` | string | 帖子富文本（含格式化标记） |
| `reactions_count` | integer | 总互动数 |
| `comments_count` | integer | 评论数 |
| `reshare_count` | integer | 转发数 |
| `reactions.{like,love,care,haha,wow,sad,angry}` | integer | 七种 reaction 各自的计数 |
| `author.id` | string | 作者主页数字 ID |
| `author.name` | string | 作者主页显示名 |
| `author.url` | string | 作者主页 URL |
| `image.uri` | string | 图片 URL（图文帖） |
| `image.id` | string | 图片 ID |
| `video` | string | 视频 / Reel 的页面 URL |
| `video_files.video_sd_file` | string | 视频 SD 直链 |
| `video_files.video_hd_file` | string | 视频 HD 直链 |
| `video_thumbnail` | string | 视频封面图 URL |

> 其余 `album_preview` / `external_url` / `attached_event` / `attached_post` / `attached_post_url` / `comments_id` / `shares_id` 等字段当前未单独建列，完整原始体保留在 `raw_data` 中。

### 分页规则

1. **首页**：不传 `cursor`
2. **翻页**：取响应中根级 `cursor` 字段，原样作为下一次请求的 `cursor` 参数
3. **终止条件**：`results` 为空数组，或响应未返回 `cursor`

### 失败信号

> ⚠️ RapidAPI **没有 JustOneAPI 风格的业务 `code` 字段**，只能依靠 HTTP 状态码 + 响应体形态判断成败。

| 信号 | 处理策略 |
|------|----------|
| HTTP 200 + 含 `results` 数组 | 视为成功 |
| HTTP 200 + 缺少 `results` 字段 | 自动重试，最多 5 次 |
| HTTP 401 / 403 | 立即终止，提示检查 `RAPIDAPI_KEY` 是否有效 / 已订阅该 API |
| HTTP 429 | 触发速率限制，等待后重试 |
| HTTP 5xx / 网络异常 | 自动重试 |

### ID 获取方式

`profile_id` 为 Facebook 主页内部数字 ID，并非 URL 中的用户名 / vanity name。常用获取方法：

1. 浏览器打开主页，查看页面源代码，搜索 `entity_id` / `pageID` / `userID` 字段
2. 使用如 "Find my Facebook ID" 等浏览器插件直接读取
3. 调用 Facebook Graph API（需另外鉴权）查询
