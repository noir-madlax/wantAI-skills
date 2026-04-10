# 接口：小红书用户搜索 (V2)

按关键词搜索小红书用户，适用于达人发现、账号研究、竞品分析等场景。

## 请求

```
GET https://api.justoneapi.com/api/xiaohongshu/search-user/v2
```

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`

### 参数

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌，通过 query 参数传递 |
| `keyword` | ✅ | string | — | 搜索关键词 |
| `page` | ❌ | integer | `1` | 页码，用于翻页 |

## 响应

### 结构

```json
{
  "code": 0,
  "data": {
    "users": [
      {
        "id": "68b016570000000018028e20",
        "name": "昵称",
        "red_id": "小红书号",
        "image": "头像 URL",
        "desc": "简介（通常含小红书号）",
        "sub_title": "子标题",
        "link": "xhsdiscover://1/user/user.<id>",
        "red_official_verified": false,
        "red_official_verify_type": 0,
        "followed": false,
        "self": false
      }
    ],
    "filters": []
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 业务状态码，`0` 为成功，见错误码表 |
| `data.users` | array | 当页用户列表，每页约 20 条 |
| `id` | string | 用户唯一 ID |
| `name` | string | 昵称 |
| `red_id` | string | 小红书号 |
| `desc` | string | 简介（通常含小红书号） |
| `sub_title` | string | 子标题 |
| `image` | string | 头像 URL |
| `link` | string | 主页深链，格式 `xhsdiscover://1/user/user.<id>` |
| `red_official_verified` | boolean | 是否蓝 V 认证 |
| `red_official_verify_type` | integer | 认证类型（`0` = 未认证） |

### 分页

递增 `page` 翻页；`data.users` 返回空数组时表示已到末页。
