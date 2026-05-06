# 接口：YouTube 频道视频列表 (V1)

获取指定 YouTube 频道发布的视频列表，支持游标翻页，适用于频道监控、内容矩阵分析、KOL 调研等场景。

## 请求

```
GET https://api.justoneapi.com/api/youtube/get-channel-videos/v1
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `channelId` | ✅ | string | — | YouTube 频道 ID（形如 `UCxxxxxxxxxxxxxxxx`） |
| `continuationToken` | ❌ | string | — | 翻页游标；**首页不传**，后续传上一页响应的 `data.continuation_token` |

## 响应

### 结构

```json
{
  "code": 0,
  "data": {
    "videos": [
      {
        "video_id": "1uu4E8xtY7M",
        "title": "The FASTEST Way to Lose Love Handles",
        "description": "Love handles won't disappear from side bends...",
        "url": "https://www.youtube.com/watch?v=1uu4E8xtY7M",
        "playback_url": "https://rr3---sn-n4v7sns7.googlevideo.com/initplayback?...",
        "duration": "10:57",
        "duration_accessibility": "10分钟57秒钟",
        "thumbnail": "https://i.ytimg.com/vi/1uu4E8xtY7M/hqdefault.jpg?...",
        "thumbnails": [ {"url": "...", "width": 168, "height": 94}, ... ],
        "moving_thumbnail": "https://i.ytimg.com/an_webp/1uu4E8xtY7M/mqdefault_6s.webp?...",
        "published_time": "2天前",
        "view_count": "135,254次观看",
        "short_view_count": "13万次观看",
        "is_live": false,
        "is_verified": true
      }
    ],
    "continuation_token": "4qmFsgLZCRIYVUNl..."
  }
}
```

### 关键字段

| 字段 | 说明 |
|------|------|
| `data.videos[].video_id` | 视频 ID（用于后续拉评论） |
| `data.videos[].duration` | 时长字符串，如 `10:57`；`duration_accessibility` 为本地化文本 |
| `data.videos[].view_count` | 播放量文本，如 `135,254次观看`；非纯数字，需正则提取 |
| `data.videos[].published_time` | 发布时间相对文本，如 `2天前` / `1个月前`，**非时间戳** |
| `data.videos[].is_live` / `is_verified` | 是否直播 / 是否认证 |
| `data.continuation_token` | 下一页 `continuationToken` 取值；为空/null 表示已到末页 |

> ⚠️ **响应里不包含 `channel_id`**。脚本在写库时由请求参数 `channelId` 回填到每一行。

## 分页

1. 首页：不传 `continuationToken`
2. 翻页：取响应中 `data.continuation_token` 作为下一次请求的 `continuationToken`
3. 终止条件：`data.continuation_token` 为空 / null，或 `data.videos` 为空

## 入库映射

- 业务唯一键：`(channel_id, video_id)`
- 数值字段（`view_count` / `like_count`）入库时由脚本统一去掉非数字字符再转 `int`
- 原始 JSON 整条存入 `raw_data` 字段以便回溯
