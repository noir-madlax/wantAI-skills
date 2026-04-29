# 接口：小红书笔记评论 (V2)

获取小红书笔记评论数据，包含**顶层评论**与**评论回复**两个接口；二者通常配套使用：先翻顶层评论，再对 `sub_comment_count > 0` 的评论拉取回复。适用于评论采集、舆情/情感分析、社区监控等场景。

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

## 1. 顶层评论

### 请求

```
GET https://api.justoneapi.com/api/xiaohongshu/get-note-comment/v2
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `noteId` | ✅ | string | — | 小红书笔记 ID |
| `lastCursor` | ❌ | string | — | 翻页游标；**首页不传**，后续传上一页响应的 `data.cursor` |
| `sort` | ❌ | string | `latest` | 排序：`latest`（最新）/ `normal`（默认排序） |

### 响应

```json
{
  "code": 0,
  "data": {
    "has_more": true,
    "cursor": "69f0a04d0000000028037c6d",
    "comment_count": 808,
    "comment_count_l1": 590,
    "comments": [
      {
        "id": "69f1545a0000000027028a00",
        "note_id": "69ea1edc0000000020013001",
        "content": "评论文本",
        "time": 1777423450,
        "like_count": 0,
        "sub_comment_count": 0,
        "comment_type": 0,
        "status": 0,
        "ip_location": "北京",
        "user": { "userid": "...", "nickname": "...", "red_id": "...", "images": "..." },
        "pictures": [ {"url": "...", "origin_url": "..."} ],
        "sub_comments": []
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `data.has_more` | 是否还有下一页 |
| `data.cursor` | 下一页 `lastCursor` 取值（字符串，原样回传） |
| `comments[].id` | 评论 ID |
| `comments[].time` | 评论发布时间，Unix 时间戳（秒） |
| `comments[].sub_comment_count` | 该评论下的回复数；>0 时需调用「评论回复」接口拉取 |
| `comments[].sub_comments` | 内联回复列表，**通常为空**（接口默认不展开），需走下方接口 |
| `comments[].comment_type` | `0`=文本，`2`=图片评论（带 `pictures`） |
| `comments[].ip_location` | IP 属地（如 `北京` / `美国` / `广东`） |

## 2. 评论回复（子评论）

### 请求

```
GET https://api.justoneapi.com/api/xiaohongshu/get-note-sub-comment/v2
```

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `noteId` | ✅ | string | — | 小红书笔记 ID |
| `commentId` | ✅ | string | — | 顶层评论 ID（上方接口返回的 `comments[].id`） |
| `lastCursor` | ❌ | string | — | 翻页游标；首页不传 |

### 响应

```json
{
  "code": 0,
  "data": {
    "has_more": true,
    "cursor": "下一页 lastCursor",
    "comments": [
      {
        "id": "65bf659700000000080142ec",
        "note_id": "65bf5360000000002c03f684",
        "content": "回复内容",
        "time": 1707042199,
        "like_count": 43,
        "user": { "userid": "...", "nickname": "...", "red_id": "...", "images": "..." },
        "target_comment": {
          "id": "65bf6392000000000800b405",
          "user": { "userid": "...", "nickname": "..." }
        }
      }
    ]
  }
}
```

#### 关键字段

| 字段 | 说明 |
|------|------|
| `comments[].target_comment.id` | 该回复直接回复的评论 ID（可能是顶层评论，也可能是另一条回复） |
| `comments[].target_comment.user` | 被回复用户基本信息 |

> ⚠️ 小红书评论只有两层（楼 + 楼中楼）。`target_comment` 不一定是顶层评论；写入存储时需区分 `parent_comment_id`（直接被回复的评论）与 `root_comment_id`（所属顶层评论 id）。

## 分页

两个接口分页方式一致：

1. 首页：不传 `lastCursor`
2. 翻页：取响应中 `data.cursor` 作为下一次请求的 `lastCursor`
3. 终止条件：`data.has_more = false` 或 `data.comments` 为空

## 配套用法

1. 调用「顶层评论」翻完所有页
2. 收集本页中 `sub_comment_count > 0` 的评论 ID
3. 对每个评论 ID 调用「评论回复」翻完所有页（用 `commentId` 传顶层评论 ID）
4. 入库映射：
   - **顶层评论**：`is_sub=0`，`parent_comment_id=NULL`，`root_comment_id = 自身 id`
   - **子评论**：`is_sub=1`，`parent_comment_id = target_comment.id`，`root_comment_id = 顶层评论 id`
