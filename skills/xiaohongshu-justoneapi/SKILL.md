---
name: xiaohongshu-justoneapi
description: 当用户需要爬取或采集小红书（RedNote）数据时触发，包括：搜索用户/博主、发现 KOL/达人、研究账号信息等场景。通过 JustOneAPI 调用小红书接口获取数据。
---

# 小红书数据采集 —— JustOneAPI

使用 JustOneAPI 调用小红书接口抓取数据。

## 前置：获取 Token

所有接口均通过 query 参数 `token` 鉴权。若用户未提供，先向其索取 JustOneAPI 访问令牌。

## 接口：用户搜索 (V2)

按关键词搜索小红书用户，适用于达人发现、账号研究、竞品分析等场景。

**请求**

```
GET https://api.justoneapi.com/api/xiaohongshu/search-user/v2
```

| 参数 | 必填 | 类型 | 默认值 | 说明 |
|------|:----:|------|:------:|------|
| `token` | ✅ | string | — | JustOneAPI 访问令牌 |
| `keyword` | ✅ | string | — | 搜索关键词 |
| `page` | ❌ | integer | `1` | 页码，用于翻页 |

> 中国大陆访问慢时，将 base URL 替换为 `http://47.117.133.51:30015`。

**响应结构**

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

**关键字段说明**

- `data.users`：当页用户列表，每页约 20 条
- `red_official_verified`：是否官方认证（蓝 V）
- `red_official_verify_type`：认证类型（`0` = 未认证）
- `link`：用户主页深链

**分页采集**

递增 `page` 翻页；当 `data.users` 返回空数组时，表示已到末页。

## 错误处理

> ⚠️ `code` 在**响应体**中，不是 HTTP 状态码。HTTP 200 也须检查 `code`。

| `code` | 含义 | 处理策略 |
|:------:|------|----------|
| `0` | 成功 | 正常处理 |
| `100` | Token 无效或已失效 | 提示用户检查 token |
| `301` | 采集失败 | **自动重试**，间隔 2-3 秒，最多 3 次 |
| `302` | 超出速率限制 | 降低请求频率，等待后重试 |
| `303` | 超出每日配额 | 告知用户当日配额已用尽 |
| `400` | 参数错误 | 检查必填参数是否缺失或格式有误 |
| `500` | 服务器内部错误 | 稍后重试，持续则反馈 JustOneAPI |
| `600` | 权限不足 | 告知用户当前 token 无此接口权限 |
| `601` | 余额不足 | 告知用户需在 JustOneAPI 充值 |

## 编写代码的注意事项

1. `token` 始终通过 **query 参数**传递，不要放入 Header
2. 请求超时设置 **≥ 60 秒**，采集响应可能较慢
3. `code: 301` 属正常瞬时失败，须实现**重试逻辑**
4. 批量翻页时建议每次请求间隔 1-2 秒，避免触发 `302`
5. 使用用户偏好的语言生成代码；未指明时优先使用 Python
