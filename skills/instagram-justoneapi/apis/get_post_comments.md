# 接口：Instagram 帖子评论 (V1)

获取 Instagram 帖子评论数据，包含**顶层评论**与**评论回复**两个接口；二者通常配套使用：先翻顶层评论，再对 `child_comment_count > 0` 的评论拉取回复。适用于评论采集、舆情/情感分析、社区互动等场景。

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

> ⚠️ Instagram 帖子有两种 ID：
> - `code`（shortcode，11 位字符串） —— **顶层评论接口必填**
> - `media_id`（数字 ID，长串数字，又名 `pk`） —— **评论回复接口必填**
> 评论列表的响应里通常会带 `media_id`，脚本会自动提取并复用。

## 1. 顶层评论

### 请求

```
GET https://api.justoneapi.com/api/instagram/get-post-comments/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `code` | ✅ | string | — | Instagram 帖子 shortcode |
| `minId` | ❌ | string | — | 翻页游标；**首页不传**，后续传上一页响应的 `next_min_id` |
| `sortOrder` | ❌ | string | `newest` | 排序：`newest`（最新）/ `popular`（热门） |

### 响应（字段以实际响应为准；常见结构如下）

```json
{
  "code": 0,
  "data": {
    "next_min_id": "{...}",
    "has_more_comments": true,
    "comment_count": 808,
    "comments": [
      {
        "pk": "17900000000000000",
        "media_id": "3123456789012345678",
        "text": "评论文本",
        "created_at": 1735660800,
        "comment_like_count": 12,
        "child_comment_count": 3,
        "user": {
          "pk": "1234567",
          "username": "demo_user",
          "full_name": "Demo",
          "profile_pic_url": "https://...",
          "is_verified": false
        }
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `data.has_more_comments` | 是否还有下一页 |
| `data.next_min_id` | 下一页 `minId` 取值（字符串原样回传） |
| `comments[].pk` / `comments[].id` | 评论 ID |
| `comments[].media_id` | 所属帖子的数字 media id（用于评论回复接口） |
| `comments[].text` | 评论内容 |
| `comments[].created_at` | 发布时间，Unix 时间戳（秒） |
| `comments[].child_comment_count` | 该评论下的回复数；>0 时调用「评论回复」接口拉取 |
| `comments[].comment_like_count` / `like_count` | 点赞数 |
| `comments[].user` | 评论者基本信息 |

## 2. 评论回复（子评论）

### 请求

```
GET https://api.justoneapi.com/api/instagram/get-comment-replies/v1
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `mediaId` | ✅ | string | — | 帖子数字 media id（不是 shortcode） |
| `commentId` | ✅ | string | — | 父评论 ID（顶层评论的 `pk`） |
| `minId` | ❌ | string | — | 翻页游标；首页不传，后续传上一页响应的 `next_min_child_cursor` |

### 响应

```json
{
  "code": 0,
  "data": {
    "next_min_child_cursor": "xxx",
    "has_more_comments": true,
    "comments": [
      {
        "pk": "17900000000000001",
        "media_id": "3123456789012345678",
        "parent_comment_id": "17900000000000000",
        "text": "回复内容",
        "created_at": 1735661000,
        "comment_like_count": 1,
        "user": { "pk": "...", "username": "...", "full_name": "...", "profile_pic_url": "...", "is_verified": false }
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `data.next_min_child_cursor` | 下一页 `minId` 取值 |
| `comments[].parent_comment_id` | 该回复直接回复的评论 ID（可能是顶层，也可能是另一条回复） |

> ⚠️ Instagram 评论结构上视为两层（楼 + 楼中楼）。`parent_comment_id` 不一定等于顶层评论 ID；写入存储时区分 `parent_comment_id`（直接被回复）与 `root_comment_id`（所属顶层）。

## 分页

两个接口分页方式一致：

1. 首页：不传 `minId`
2. 翻页：取响应的 `next_min_id`（顶层）/ `next_min_child_cursor`（回复）作为下一次的 `minId`
3. 终止条件：`has_more_comments = false`、游标为空、或 `comments` 为空

## 配套用法

1. 调用「顶层评论」翻完所有页（同时记录每条评论的 `media_id` 与 `child_comment_count`）
2. 收集 `child_comment_count > 0` 的评论 ID
3. 对每个评论 ID 调用「评论回复」翻完所有页（`commentId` 传顶层评论 ID，`mediaId` 传该帖子的数字 ID）
4. 入库映射：
   - **顶层评论**：`is_sub=0`，`parent_comment_id=NULL`，`root_comment_id = 自身 id`
   - **子评论**：`is_sub=1`，`parent_comment_id = 接口返回的 parent_comment_id`，`root_comment_id = 顶层评论 id`
