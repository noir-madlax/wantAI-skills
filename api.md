---
title: "小红书笔记搜索 API (V3)"
description: "获取小红书（RedNote）笔记搜索数据，包括摘要、作者和媒体，用于话题发现。"
---

# 小红书笔记搜索 API (V3)

<ApiTester 
  method="GET" 
  path="/api/xiaohongshu/search-note/v3" 
  summary="笔记搜索 (V3)" 
  openapiDefinitionUrl="https://docs.justoneapi.com/openapi/xiaohongshu-rednote/note-search-v3-zh.json" 
  :parameters='[{"name":"token","in":"query","description":"此 API 服务的访问令牌。","required":true,"schema":{"type":"string"}},{"name":"keyword","in":"query","description":"搜索关键词。","required":true,"schema":{"type":"string"}},{"name":"page","in":"query","description":"用于分页的页码。","required":false,"schema":{"type":"integer","format":"int32","default":1}},{"name":"sort","in":"query","description":"结果集的排序方式。\n\n可用值：\n- `general`：综合\n- `popularity_descending`：热门\n- `time_descending`：最新","required":false,"schema":{"type":"string","default":"general","description":"Xiaohongshu Search Note Sort","enum":["general","popularity_descending","time_descending"]}},{"name":"noteType","in":"query","description":"笔记类型过滤器。\n\n可用值：\n- `_0`: 通用\n- `_1`: 视频\n- `_2`: 普通","required":false,"schema":{"type":"string","default":"_0","description":"Xiaohongshu Search Note Type","enum":["_0","_1","_2"]}}]' 
  :requestBody='null'
  :responseExample='null'
/>

<ApiHealthSection api="/api/xiaohongshu/search-note/v3" />

获取小红书（RedNote）笔记搜索数据，包括摘要、作者和媒体，用于话题发现。

## 请求参数

<div class="api-doc-table api-doc-table--params">

| 参数名 | 位置 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `token` | query | `string` | 是 | - | 此 API 服务的访问令牌。 |
| `keyword` | query | `string` | 是 | - | 搜索关键词。 |
| `page` | query | `integer` | 否 | `1` | 用于分页的页码。 |
| `sort` | query | `string` | 否 | `general` | 结果集的排序方式。<br><br>可用值：<br>- `general`：综合<br>- `popularity_descending`：热门<br>- `time_descending`：最新 |
| `noteType` | query | `string` | 否 | `_0` | 笔记类型过滤器。<br><br>可用值：<br>- `_0`: 通用<br>- `_1`: 视频<br>- `_2`: 普通 |

</div>

## 代码示例

::: tip 💡 环境说明
默认请使用 `https://api.justoneapi.com`（`prod-global`）。一般来说，`api.justoneapi.com` 在全球访问速度都正常；如果中国大陆地区用户感觉慢，可以将代码中的基地址切换为 `http://47.117.133.51:30015`（`prod-cn`）。
:::

::: code-group

```bash [🐚 cURL]
curl -X GET "https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE"
```

```text [🤖 AI 提示词]
我想使用 Just One API 提供的“笔记搜索 (V3)”接口。
接口地址: https://api.justoneapi.com/api/xiaohongshu/search-note/v3
HTTP 方法: GET
身份验证: 在 URL 后添加查询参数“?token=您的API密钥”。
OpenAPI 定义: https://docs.justoneapi.com/openapi/xiaohongshu-rednote/note-search-v3-zh.json

请求参数说明:
- token (query): 此 API 服务的访问令牌。 (必填)
- keyword (query): 搜索关键词。 (必填)
- page (query): 用于分页的页码。
- sort (query): 结果集的排序方式。

可用值：
- `general`：综合
- `popularity_descending`：热门
- `time_descending`：最新
- noteType (query): 笔记类型过滤器。

可用值：
- `_0`: 通用
- `_1`: 视频
- `_2`: 普通

返回格式: JSON

响应处理与错误码：
1. 需通过返回体中的 "code" 字段判断业务结果（code 为 0 表示成功）。
2. 超时建议：建议将请求超时时间设置为至少 60 秒。
3. 业务码说明：
   - 0: 成功
   - 100: Token 无效或已失效
   - 301: 采集失败，请重试
   - 302: 超出速率限制
   - 303: 超出每日配额
   - 400: 参数错误
   - 500: 内部服务器错误
   - 600: 权限不足
   - 601: 余额不足

请帮我用我擅长的编程语言写一个脚本来调用这个接口，并处理返回结果。
```

```python [🐍 Python]
import requests

url = "https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE"
response = requests.get(url)
print(response.json())
```

```js [🌐 JavaScript]
const response = await fetch("https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE", {
  method: "GET"
});
const data = await response.json();
console.log(data);
```

```java [☕ Java]
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE"))
            .method("GET", HttpRequest.BodyPublishers.noBody())
            .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

```go [🐹 Go]
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	client := &http.Client{}
	url := "https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE"
	req, _ := http.NewRequest("GET", url, nil)
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))
}
```

```php [🐘 PHP]
<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://api.justoneapi.com/api/xiaohongshu/search-note/v3?token=YOUR_API_KEY&keyword=VALUE");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
$response = curl_exec($ch);
curl_close($ch);
echo $response;
```

:::

<div style="text-align: right; margin-top: -20px; margin-bottom: 20px;">
<a href="/openapi/xiaohongshu-rednote/note-search-v3-zh.json" target="_blank" style="font-size: 12px; color: var(--vp-c-text-3); text-decoration: none; opacity: 0.8;">[OpenAPI 定义 (JSON)]</a>
</div>

## 响应结果

```
{
  "code": 0,
  "data": {
    "show_single_col": false,
    "is_broad_query": true,
    "search_dqa_new_page_exp": 1,
    "strategy_info": {
      "query_can_guide_to_feed": true,
      "query_average_impression_count": 19
    },
    "dqa_authorized_user_by_shared": false,
    "can_cut": false,
    "cur_cut_number": 0,
    "search_request_id": "eb568d726ace1b15",
    "request_dqa": 0,
    "items": [
      {
        "model_type": "note",
        "note": {
          "id": "684f7ca200000000230145a1",
          "result_from": "",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "xsec_token": "YBoBdzKHwufHtvN4aZ8PKXQl4zWjKAZJXBwUalfga8aZQ=",
          "liked": false,
          "user": {
            "red_id": "417866368",
            "show_red_official_verify_icon": false,
            "userid": "5c1c9f650000000007021ee0",
            "track_duration": 0,
            "red_official_verified": false,
            "followed": false,
            "nickname": "不赶香信",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31l5dvi012g0g5n0sjtihs7n0kkaoeig?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0
          },
          "has_music": false,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAc7OoFJSGdRlYhciNwPeO/a3J86YQRU7SQESFrU9Fmlrz4REJgUnJQv9ov1aIm9JbBqME7uUF+FI4DtVVRTNwQVXVzRIHo0i9",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-06-16",
              "text_en": "2025-06-16",
              "style": 0
            }
          ],
          "abstract_show": "有偿找个骑车搭子一个月8000-15000💰…#机车跑山 #女骑 #摩托车",
          "type": "normal",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "85"
          },
          "niced": false,
          "collected": false,
          "extract_text_enabled": 0,
          "desc": "有偿找个骑车搭子一个月8000-15000💰 一个人骑车真的太无聊了，所以想找一个陪骑， 一个月大概8000左右可商议",
          "timestamp": 1750039714,
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "nice_count": 0,
          "collected_count": 9,
          "comments_count": 106,
          "liked_count": 85,
          "images_list": [
            {
              "width": 1910,
              "url": "https://sns-na-i8.xhscdn.com/1040g00831ip70f1q0u1g5n0sjtihs7n0v6mvobg?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=f666b39e73410fa8a6ed96ab5e519884&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831ip70f1q0u1g5n0sjtihs7n0v6mvobg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=f666b39e73410fa8a6ed96ab5e519884&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831ip70f1q0u1g5n0sjtihs7n0v6mvobg",
              "need_load_original_image": false,
              "fileid": "1040g00831ip70f1q0u1g5n0sjtihs7n0v6mvobg",
              "height": 2560
            },
            {
              "original": "",
              "trace_id": "1040g00831ip70f1q0u005n0sjtihs7n0vul0q30",
              "need_load_original_image": false,
              "fileid": "1040g00831ip70f1q0u005n0sjtihs7n0vul0q30",
              "height": 1367,
              "width": 1025,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831ip70f1q0u005n0sjtihs7n0vul0q30?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=9312158bee0ba2f9e8d910674df304ab&t=69d8fcb3&origin=1"
            },
            {
              "trace_id": "1040g00831ip70f1q0u105n0sjtihs7n0kuiss70",
              "need_load_original_image": false,
              "fileid": "1040g00831ip70f1q0u105n0sjtihs7n0kuiss70",
              "height": 2560,
              "width": 1916,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831ip70f1q0u105n0sjtihs7n0kuiss70?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=627701ca03abe65e63c497fabd3bac2c&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831ip70f1q0u0g5n0sjtihs7n0u47bv2o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4086381da13768d37fe0906ff81279f5&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831ip70f1q0u0g5n0sjtihs7n0u47bv2o",
              "need_load_original_image": false,
              "fileid": "1040g00831ip70f1q0u0g5n0sjtihs7n0u47bv2o",
              "height": 2560,
              "width": 1912,
              "url": ""
            }
          ],
          "last_update_time": 1750040076,
          "note_attributes": [],
          "shared_count": 8,
          "debug_info_str": "",
          "widgets_context": "{\"flags\":{},\"author_id\":\"5c1c9f650000000007021ee0\",\"author_name\":\"不赶香信\"}",
          "update_time": 1758817821000
        }
      },
      {
        "model_type": "note",
        "note": {
          "nice_count": 0,
          "niced": false,
          "comments_count": 97,
          "has_music": false,
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAoxqFryjIGmGWaiqmNTroIN1BvpWg9IaDjkb1a04ibP0DRt5Z6anZJdfjkXbAFcEQ7qc/it7u4mdU/hrsWrjhHWPXoUH1ylBv",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "03-08",
              "text_en": "03-08"
            }
          ],
          "user": {
            "show_red_official_verify_icon": false,
            "track_duration": 0,
            "followed": false,
            "red_id": "95494672245",
            "nickname": "一起看日出",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31ikoul3ogi4g5plfhn1nc7357dm45d8?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "red_official_verified": false,
            "userid": "66af8dc3000000001d021c65"
          },
          "abstract_show": "本田 Nwt150…#爱机车爱生活爱骑行 #踏板摩托车 #本田nwt150",
          "desc": "今天去店里看了 试驾了一下，整体感觉还不错 ，标准款和高配 我感觉没有必要上高配的。 试驾了一下 整体挺平稳 刹车也灵敏",
          "advanced_widgets_groups": {
            "groups": [
              {
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ],
                "mode": 1
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"66af8dc3000000001d021c65\",\"author_name\":\"一起看日出\"}",
          "extract_text_enabled": 0,
          "collected_count": 36,
          "liked": false,
          "id": "69ad120c00000000230385f5",
          "xsec_token": "YB-l0dmRGESW5kiguB0UfxKyf9ykCKjFNLuJ75Pt4aG9s=",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "95"
          },
          "collected": false,
          "update_time": 1772950072000,
          "debug_info_str": "",
          "note_attributes": [],
          "result_from": "",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "timestamp": 1772950028,
          "type": "normal",
          "images_list": [
            {
              "trace_id": "notes_pre_post/1040g3k831temhu4558dg5plfhn1nc735aan1d30",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831temhu4558dg5plfhn1nc735aan1d30",
              "height": 2710,
              "width": 2138,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831temhu4558dg5plfhn1nc735aan1d30?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=d377cac6d92e5205624b79e34ba98497&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831temhu4558dg5plfhn1nc735aan1d30?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d377cac6d92e5205624b79e34ba98497&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031temhu5k566g5plfhn1nc7355kbqq9o",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031temhu5k566g5plfhn1nc7355kbqq9o",
              "height": 1920,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031temhu5k566g5plfhn1nc7355kbqq9o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4150b10645a9821823de0c9e0bfbe5fa&t=69d8fcb3&origin=1"
            }
          ],
          "last_update_time": 0,
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "shared_count": 50,
          "title": "本田 Nwt150",
          "liked_count": 95
        }
      },
      {
        "model_type": "note",
        "note": {
          "id": "69b96c65000000001b00153c",
          "last_update_time": 0,
          "shared_count": 4,
          "update_time": 1773759636000,
          "has_music": false,
          "timestamp": 1773759589,
          "widgets_context": "{\"flags\":{},\"author_id\":\"5b61984a4eacab10be27141b\",\"author_name\":\"屁屁软\"}",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "65"
          },
          "desc": "黑骑500从25年5月29号骑到今年3月12号，不到一年，出了黑骑950，马上黑骑600也要上市了，骑腻了换了赛",
          "cover_image_index": 0,
          "note_attributes": [],
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "collected": false,
          "liked": false,
          "type": "normal",
          "user": {
            "red_id": "QHC0822",
            "nickname": "屁屁软",
            "track_duration": 0,
            "userid": "5b61984a4eacab10be27141b",
            "followed": false,
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31a32aiurni004a7uerc4k50rbnaikto?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false
          },
          "debug_info_str": "",
          "nice_count": 0,
          "collected_count": 9,
          "title": "终于还是巡航换仿赛了",
          "images_list": [
            {
              "need_load_original_image": false,
              "width": 4284,
              "url": "https://sns-na-i8.xhscdn.com/note_pre_post_uhdr/1040g3r831tqof7u4mo704a7uerc4k50r4992amo?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=dbc206b69dca68da1190150d84158ba4&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "note_pre_post_uhdr/1040g3r831tqof7u4mo704a7uerc4k50r4992amo",
              "live_photo": {
                "media": {
                  "video_id": 137845130041427490,
                  "video": {
                    "biz_id": "281960326896555324",
                    "duration": 3,
                    "hdr_type": 0,
                    "drm_type": 0,
                    "bound": [
                      {
                        "y": 0,
                        "w": 1920,
                        "h": 1440,
                        "x": 0
                      }
                    ],
                    "opaque1": {
                      "domestic": "0",
                      "livephoto_flag": "1",
                      "amend_mobile": "60",
                      "weakNetUserFlag": "1",
                      "amend": "8"
                    },
                    "width": 1440,
                    "biz_name": 10,
                    "height": 1920,
                    "stream_types": [
                      66,
                      198
                    ]
                  },
                  "stream": {
                    "av1": [],
                    "h264": [],
                    "h265": [
                      {
                        "audio_codec": "aac",
                        "rotate": 0,
                        "sr": 0,
                        "volume": 0,
                        "fps": 29,
                        "video_codec": "hevc",
                        "stream_type": 66,
                        "avg_bitrate": 2302070,
                        "audio_channels": 2,
                        "default_stream": 1,
                        "ssim": 0,
                        "quality_type": "FHD",
                        "format": "mp4",
                        "master_url": "http://sns-video-zl.xhscdn.com/stream/1/10/66/01e9b96a5a23061a010050019cfc4fabf4_66.mp4",
                        "psnr": 39.18199920654297,
                        "stream_desc": "livephoto_r256_1080p_66_andr",
                        "size": 652637,
                        "backup_urls": [
                          "http://sns-bak-v8.xhscdn.com/stream/1/10/66/01e9b96a5a23061a010050019cfc4fabf4_66.mp4",
                          "http://sns-bak-v10.xhscdn.com/stream/1/10/66/01e9b96a5a23061a010050019cfc4fabf4_66.mp4"
                        ],
                        "hdrType": 0,
                        "vmaf": -1,
                        "opaque1": {
                          "didLoudnorm": "false",
                          "pcdn_supplier": "",
                          "amend": "0",
                          "has_soundtrack": "1",
                          "use_pcdn": "0",
                          "pcdn_302_flag": "false",
                          "device_score": "0"
                        },
                        "width": 1080,
                        "duration": 2268,
                        "audio_duration": 2266,
                        "audio_bitrate": 59664,
                        "weight": 66,
                        "height": 1440,
                        "video_bitrate": 2230830,
                        "video_duration": 2267
                      },
                      {
                        "opaque1": {
                          "min_long_side": "1920",
                          "has_soundtrack": "0",
                          "pcdn_302_flag": "false",
                          "min_short_side": "1080",
                          "didLoudnorm": "false",
                          "pcdn_supplier": "",
                          "amend": "100",
                          "use_pcdn": "0",
                          "device_score": "700",
                          "is_livephoto_2k": "1"
                        },
                        "stream_desc": "R265_MP4_2K_198_ANDR_exp",
                        "fps": 29,
                        "master_url": "http://sns-video-zl.xhscdn.com/stream/1/10/198/01e9b96a5a23061a010050019cfc4fcc48_198.mp4",
                        "backup_urls": [
                          "http://sns-bak-v8.xhscdn.com/stream/1/10/198/01e9b96a5a23061a010050019cfc4fcc48_198.mp4",
                          "http://sns-bak-v10.xhscdn.com/stream/1/10/198/01e9b96a5a23061a010050019cfc4fcc48_198.mp4"
                        ],
                        "vmaf": -1,
                        "psnr": 40.0880012512207,
                        "default_stream": 0,
                        "duration": 2267,
                        "video_codec": "hevc",
                        "audio_channels": 2,
                        "weight": 80,
                        "hdrType": 0,
                        "rotate": 0,
                        "format": "mp4",
                        "size": 840015,
                        "volume": 0,
                        "avg_bitrate": 2964322,
                        "audio_bitrate": 59664,
                        "sr": 0,
                        "ssim": 0,
                        "quality_type": "2K",
                        "video_bitrate": 2913955,
                        "video_duration": 2250,
                        "audio_codec": "aac",
                        "stream_type": 198,
                        "width": 1440,
                        "height": 1920,
                        "audio_duration": 2266
                      }
                    ],
                    "h266": []
                  },
                  "userLevel": 0
                }
              },
              "live_photo_file_id": "livephoto_pre_post/1040g3jo31tqoeubnnu004a7uerc4k50rghdbo78",
              "fileid": "note_pre_post_uhdr/1040g3r831tqof7u4mo704a7uerc4k50r4992amo",
              "height": 5712,
              "url_size_large": "https://sns-na-i8.xhscdn.com/note_pre_post_uhdr/1040g3r831tqof7u4mo704a7uerc4k50r4992amo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=dbc206b69dca68da1190150d84158ba4&t=69d8fcb3&origin=1"
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/note_pre_post_uhdr/1040g3r831tqof7u4mo7g4a7uerc4k50rpbeq2h8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4ed32d97661732c88fc40516ea8bd36e&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "note_pre_post_uhdr/1040g3r831tqof7u4mo7g4a7uerc4k50rpbeq2h8",
              "need_load_original_image": false,
              "fileid": "note_pre_post_uhdr/1040g3r831tqof7u4mo7g4a7uerc4k50rpbeq2h8",
              "height": 5712,
              "width": 4284
            }
          ],
          "geo_info": {
            "distance": ""
          },
          "niced": false,
          "comments_count": 88,
          "xsec_token": "YBPldWS8xM3gd2Aqtb18Viac5ZhGrHE-4Hf2-rbUxp36g=",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "result_from": "",
          "extract_text_enabled": 0,
          "liked_count": 65,
          "corner_tag_info": [
            {
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RA9XjK4L5QdajGhBYyQEFvhyk3MQPLQCMkG6i1FB+s++3SY7NznH/hn3syJn/zgoPSTzixlvnOUTyiMbM7tl+JFerMGkwwQsW8",
              "text_en": ""
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "03-17",
              "text_en": "03-17",
              "style": 0
            }
          ]
        }
      },
      {
        "model_type": "note",
        "note": {
          "user": {
            "red_official_verified": false,
            "userid": "5c63f11d000000001202e6b3",
            "track_duration": 0,
            "followed": false,
            "nickname": "骑慢车的小张",
            "show_red_official_verify_icon": false,
            "red_id": "222626397",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1000g2jo2llva9j0im0005n33u4eklpljgkjgvb0?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0
          },
          "debug_info_str": "",
          "collected": false,
          "liked": false,
          "niced": false,
          "comments_count": 112,
          "widgets_context": "{\"flags\":{},\"author_id\":\"5c63f11d000000001202e6b3\",\"author_name\":\"骑慢车的小张\"}",
          "shared_count": 12,
          "nice_count": 0,
          "id": "69c1443e000000001f0017d4",
          "liked_count": 33,
          "last_update_time": 0,
          "note_attributes": [],
          "advanced_widgets_groups": {
            "groups": [
              {
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ],
                "mode": 1
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "update_time": 1774273641000,
          "tag_info": {
            "type": "",
            "title": ""
          },
          "timestamp": 1774273598,
          "cover_image_index": 0,
          "interaction_area": {
            "status": false,
            "text": "33",
            "type": 1
          },
          "corner_tag_info": [
            {
              "text": "RAx/ETTNLopO9CDGBrqsi9sb8lKEPbSmCh9eVykhkVSTPUJkmZVuKpzfeJNClH+fxkH6mz4uPJmyjeO/wNzU+8gQGlxe6e2dJZ",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": ""
            },
            {
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "03-23",
              "text_en": "03-23"
            }
          ],
          "desc": "24年春风clc450双座 个人一手仅行驶1000公里 全车无伤 全车车衣 改装手机支架 双缸450cc TFT液晶仪表",
          "type": "normal",
          "geo_info": {
            "distance": ""
          },
          "collected_count": 8,
          "has_music": false,
          "result_from": "",
          "xsec_token": "YBNrmjAzfbWhNsYBFUMgYAyvzAtN96W2d4a7FnsqD9gSg=",
          "title": "听说小红薯出车快！春风clc450",
          "images_list": [
            {
              "height": 1920,
              "width": 1440,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q005n33u4eklpljgcdg9pg?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=e5937cf7945db140d29fd7ddfdce0779&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q005n33u4eklpljgcdg9pg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e5937cf7945db140d29fd7ddfdce0779&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q005n33u4eklpljgcdg9pg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q005n33u4eklpljgcdg9pg"
            },
            {
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q0g5n33u4eklpljuhft600?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=a5366f5beabf754b8f5b5ba8303d047c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q0g5n33u4eklpljuhft600",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q0g5n33u4eklpljuhft600"
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q105n33u4eklpljkqa9ha0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e58bbb8e551c90723e2c09c27a44609d&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q105n33u4eklpljkqa9ha0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q105n33u4eklpljkqa9ha0",
              "height": 1920,
              "width": 1440
            },
            {
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q1g5n33u4eklplj3ir3fg8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=7160121db9ec43fe64153f5cc89b3286&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q1g5n33u4eklplj3ir3fg8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q1g5n33u4eklplj3ir3fg8",
              "height": 1920
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q205n33u4eklpljd2ki8ro?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=806260fc130edcc6a4781bdcbacafe2f&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q205n33u4eklpljd2ki8ro",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q205n33u4eklpljd2ki8ro",
              "height": 1920,
              "width": 1440
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831u2dq23n7q2g5n33u4eklpljmi6k0lo",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831u2dq23n7q2g5n33u4eklpljmi6k0lo",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831u2dq23n7q2g5n33u4eklpljmi6k0lo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=0f563f3949a4ab06de963baf3cd48985&t=69d8fcb3&origin=1"
            }
          ],
          "extract_text_enabled": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "liked_count": 117,
          "has_music": false,
          "update_time": 1773047468000,
          "collected_count": 44,
          "liked": false,
          "result_from": "",
          "corner_tag_info": [
            {
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RAsOn3OXOXMwNp7HyhnYQV9DzbjgNgLeu56M8gF1svr0jeuPqHeA+lz+h7BJw+b0hxe0eF7BsnDO6+A1u/nAguLVtexIf4mWo6",
              "text_en": ""
            },
            {
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "03-09",
              "text_en": "03-09",
              "style": 0,
              "location": 5
            }
          ],
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "117"
          },
          "desc": "提车提车！也是有小摩托的人了，在小拉和铃木之间反复横跳最后选了铃木，越看越喜欢[派对R] 超级好骑！！！目前还差一个尾箱",
          "last_update_time": 0,
          "widgets_context": "{\"flags\":{},\"author_id\":\"5a8636714eacab1947ed9f9e\",\"author_name\":\"绾绾爱存钱\"}",
          "xsec_token": "YB60GFEvoRMx6iplhWccTJQ-vRwNumccGJB8TTDDzJDDI=",
          "images_list": [
            {
              "width": 4284,
              "url": "https://sns-na-i8.xhscdn.com/notes_uhdr/1040g3qo31tg53df7m8604a1g2gr737su76e8ioo?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=8db082c8baf18a9b8b93d03d93657ace&t=69d8fcb3&origin=1",
              "trace_id": "notes_uhdr/1040g3qo31tg53df7m8604a1g2gr737su76e8ioo",
              "live_photo": {
                "media": {
                  "video_id": 137833189532047340,
                  "video": {
                    "biz_id": "281948377693667655",
                    "opaque1": {
                      "amend_mobile": "60",
                      "weakNetUserFlag": "1",
                      "amend": "8",
                      "domestic": "0",
                      "livephoto_flag": "1"
                    },
                    "bound": [
                      {
                        "h": 1440,
                        "x": 0,
                        "y": 0,
                        "w": 1920
                      }
                    ],
                    "width": 1440,
                    "height": 1920,
                    "biz_name": 10,
                    "duration": 3,
                    "hdr_type": 0,
                    "drm_type": 0,
                    "stream_types": [
                      66,
                      198
                    ]
                  },
                  "stream": {
                    "h264": [],
                    "h265": [
                      {
                        "vmaf": -1,
                        "psnr": 40.715999603271484,
                        "stream_type": 66,
                        "height": 1440,
                        "volume": 0,
                        "video_duration": 2100,
                        "audio_channels": 2,
                        "backup_urls": [
                          "http://sns-bak-v8.xhscdn.com/stream/1/10/66/01e9ae8e3c5117f2010050019cd1dbd443_66.mp4",
                          "http://sns-bak-v10.xhscdn.com/stream/1/10/66/01e9ae8e3c5117f2010050019cd1dbd443_66.mp4"
                        ],
                        "stream_desc": "livephoto_r256_1080p_66_andr",
                        "opaque1": {
                          "didLoudnorm": "false",
                          "pcdn_supplier": "",
                          "amend": "0",
                          "has_soundtrack": "1",
                          "use_pcdn": "0",
                          "pcdn_302_flag": "false",
                          "device_score": "0"
                        },
                        "fps": 29,
                        "video_codec": "hevc",
                        "audio_duration": 2100,
                        "format": "mp4",
                        "duration": 2101,
                        "size": 512695,
                        "quality_type": "FHD",
                        "video_bitrate": 1880040,
                        "audio_bitrate": 59738,
                        "width": 1080,
                        "ssim": 0,
                        "default_stream": 1,
                        "audio_codec": "aac",
                        "hdrType": 0,
                        "sr": 0,
                        "avg_bitrate": 1952194,
                        "rotate": 0,
                        "master_url": "http://sns-video-zl.xhscdn.com/stream/1/10/66/01e9ae8e3c5117f2010050019cd1dbd443_66.mp4",
                        "weight": 66
                      },
                      {
                        "size": 659967,
                        "volume": 0,
                        "audio_duration": 2100,
                        "hdrType": 0,
                        "audio_codec": "aac",
                        "rotate": 0,
                        "backup_urls": [
                          "http://sns-bak-v8.xhscdn.com/stream/1/10/198/01e9ae8e3c5117f2010050019cd1dc24c7_198.mp4",
                          "http://sns-bak-v10.xhscdn.com/stream/1/10/198/01e9ae8e3c5117f2010050019cd1dc24c7_198.mp4"
                        ],
                        "psnr": 41.23400115966797,
                        "stream_desc": "R265_MP4_2K_198_ANDR_exp",
                        "duration": 2101,
                        "weight": 80,
                        "audio_bitrate": 59738,
                        "opaque1": {
                          "pcdn_supplier": "",
                          "device_score": "700",
                          "amend": "100",
                          "has_soundtrack": "0",
                          "use_pcdn": "0",
                          "pcdn_302_flag": "false",
                          "min_short_side": "1080",
                          "min_long_side": "1920",
                          "is_livephoto_2k": "1",
                          "didLoudnorm": "false"
                        },
                        "stream_type": 198,
                        "width": 1440,
                        "master_url": "http://sns-video-zl.xhscdn.com/stream/1/10/198/01e9ae8e3c5117f2010050019cd1dc24c7_198.mp4",
                        "ssim": 0,
                        "sr": 0,
                        "format": "mp4",
                        "audio_channels": 2,
                        "default_stream": 0,
                        "quality_type": "2K",
                        "video_duration": 2083,
                        "vmaf": -1,
                        "height": 1920,
                        "avg_bitrate": 2512963,
                        "fps": 29,
                        "video_codec": "hevc",
                        "video_bitrate": 2461132
                      }
                    ],
                    "h266": [],
                    "av1": []
                  },
                  "userLevel": 0
                }
              },
              "live_photo_file_id": "livephoto/1040g39831tg4m2b3lm704a1g2gr737su30mvlto",
              "fileid": "notes_uhdr/1040g3qo31tg53df7m8604a1g2gr737su76e8ioo",
              "height": 5712,
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_uhdr/1040g3qo31tg53df7m8604a1g2gr737su76e8ioo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=8db082c8baf18a9b8b93d03d93657ace&t=69d8fcb3&origin=1",
              "original": "",
              "need_load_original_image": false
            },
            {
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_uhdr/1040g3qo31tg53df7m85g4a1g2gr737su96vjqo8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=029193c01db42f6fec3e887edb1a5c9d&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_uhdr/1040g3qo31tg53df7m85g4a1g2gr737su96vjqo8",
              "need_load_original_image": false,
              "fileid": "notes_uhdr/1040g3qo31tg53df7m85g4a1g2gr737su96vjqo8",
              "height": 4032
            },
            {
              "original": "",
              "trace_id": "notes_uhdr/1040g3qo31tg53df7m86g4a1g2gr737su2bg0iso",
              "need_load_original_image": false,
              "fileid": "notes_uhdr/1040g3qo31tg53df7m86g4a1g2gr737su2bg0iso",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_uhdr/1040g3qo31tg53df7m86g4a1g2gr737su2bg0iso?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=570fbe388a0ca3976fbc73a2abed34f3&t=69d8fcb3&origin=1"
            }
          ],
          "note_attributes": [],
          "id": "69ae8e41000000001b01c147",
          "debug_info_str": "",
          "geo_info": {
            "distance": ""
          },
          "nice_count": 0,
          "niced": false,
          "comments_count": 152,
          "title": "铃木us125 提车啦",
          "type": "normal",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "cover_image_index": 0,
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "shared_count": 52,
          "user": {
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "followed": false,
            "red_id": "264442638",
            "userid": "5a8636714eacab1947ed9f9e",
            "track_duration": 0,
            "nickname": "绾绾爱存钱",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31qllhb6t7o0g4a1g2gr737sur97i7to?imageView2/2/w/80/format/jpg"
          },
          "timestamp": 1773047361,
          "collected": false,
          "extract_text_enabled": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "liked_count": 1920,
          "has_music": false,
          "widgets_context": "{\"flags\":{\"music\":true},\"author_id\":\"60927a41000000000100341c\",\"author_name\":\"骑不快的小张\"}",
          "update_time": 1753862598000,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "result_from": "",
          "collected_count": 432,
          "collected": false,
          "comments_count": 93,
          "type": "normal",
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RA3giGWCPAdAcMPXDwFJNpSTmutkCiJWFHSKoADaC5HPiSIuF+ovXYGo5X6rWbglWS5IJfS/Ds6jsRfARBx8VOqzoAxbCZlyNw",
              "text_en": "",
              "style": 0
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-07-30",
              "text_en": "2025-07-30",
              "style": 0
            },
            {
              "location": 0,
              "style": 0,
              "poi_id": "42303031363137535948"
            }
          ],
          "nice_count": 0,
          "niced": false,
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "xsec_token": "YB3-0yCBm9fJ3HrH94s1a40feojW804WMFe51nUlKf2G0=",
          "desc": "有没有一起溜车的友友 天津哪都去系列 #rs",
          "last_update_time": 0,
          "debug_info_str": "",
          "note_attributes": [],
          "liked": false,
          "user": {
            "followed": false,
            "red_id": "1146972356",
            "nickname": "骑不快的小张",
            "userid": "60927a41000000000100341c",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31kmat53n3q005o4if90g8d0sf6c2k7o?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "track_duration": 0
          },
          "extract_text_enabled": 0,
          "shared_count": 407,
          "id": "6889d16b0000000025024169",
          "title": "再装逼 我就蹦烂你男朋友的450sr",
          "images_list": [
            {
              "fileid": "notes_pre_post/1040g3k031ki8tio23q305o4if90g8d0s94j2pj8",
              "height": 2560,
              "width": 1920,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q305o4if90g8d0s94j2pj8?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=eeff303cabd6719d310ddda2d07ea79a&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q305o4if90g8d0s94j2pj8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=eeff303cabd6719d310ddda2d07ea79a&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ki8tio23q305o4if90g8d0s94j2pj8",
              "need_load_original_image": false
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q3g5o4if90g8d0ssb8hfv0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=fdd70dd6949dfac78c8e04353798a944&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ki8tio23q3g5o4if90g8d0ssb8hfv0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ki8tio23q3g5o4if90g8d0ssb8hfv0",
              "height": 2560,
              "width": 1920,
              "url": ""
            },
            {
              "trace_id": "notes_pre_post/1040g3k031ki8tio23q405o4if90g8d0sv05j6h0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ki8tio23q405o4if90g8d0sv05j6h0",
              "height": 2560,
              "width": 1920,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q405o4if90g8d0sv05j6h0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1b3c1541c55905441a908954d616d940&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "height": 2254,
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31ki8phn3k8e05o4if90g8d0schlksk0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=ce4d551e33b2c1ceef28b757e2a90fb4&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31ki8phn3k8e05o4if90g8d0schlksk0",
              "need_load_original_image": false,
              "fileid": "1040g2sg31ki8phn3k8e05o4if90g8d0schlksk0"
            },
            {
              "fileid": "notes_pre_post/1040g3k031ki8tio23q4g5o4if90g8d0scaolfh8",
              "height": 2560,
              "width": 1920,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q4g5o4if90g8d0scaolfh8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=509a51b80cd5bd9863b4bb335ddf6569&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ki8tio23q4g5o4if90g8d0scaolfh8",
              "need_load_original_image": false
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ki8tio23q505o4if90g8d0sqjtd3cg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ki8tio23q505o4if90g8d0sqjtd3cg",
              "height": 2560,
              "width": 1920,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ki8tio23q505o4if90g8d0sqjtd3cg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=8db97c8b87869d4627a65621cbb5aebc&t=69d8fcb3&origin=1"
            }
          ],
          "timestamp": 1753862507,
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "interaction_area": {
            "status": false,
            "text": "1920",
            "type": 1
          }
        }
      },
      {
        "model_type": "note",
        "note": {
          "user": {
            "followed": false,
            "red_id": "9502793133",
            "nickname": "蛋",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo319490vrc4u605o7lqha859sjthm1hi0?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "userid": "60f5d454000000002002a793",
            "track_duration": 0
          },
          "debug_info_str": "",
          "liked": false,
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "919"
          },
          "extract_text_enabled": 0,
          "collected_count": 320,
          "type": "normal",
          "images_list": [
            {
              "trace_id": "notes_pre_post/1040g3k831ihhnk0s08k05o7lqha859sj4tug30o",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831ihhnk0s08k05o7lqha859sj4tug30o",
              "height": 1440,
              "width": 1080,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831ihhnk0s08k05o7lqha859sj4tug30o?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=fea534eb49b8f9e4402254adda36288b&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831ihhnk0s08k05o7lqha859sj4tug30o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=fea534eb49b8f9e4402254adda36288b&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "fileid": "notes_pre_post/1040g3k831ihhnk0s08jg5o7lqha859sjfbgjnqg",
              "height": 1440,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831ihhnk0s08jg5o7lqha859sjfbgjnqg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=c028f08e3c363dea28072346df3c220c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831ihhnk0s08jg5o7lqha859sjfbgjnqg",
              "need_load_original_image": false
            },
            {
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831ihhnk0s08hg5o7lqha859sj7eq1fq8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=2c55974631379b7d65c2ae27ec6a54ef&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831ihhnk0s08hg5o7lqha859sj7eq1fq8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831ihhnk0s08hg5o7lqha859sj7eq1fq8",
              "height": 1440
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831ihhnk0s08ig5o7lqha859sjhnatph0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=b94b0b7c4df0697bb0ca3bc048e1becf&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831ihhnk0s08ig5o7lqha859sjhnatph0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831ihhnk0s08ig5o7lqha859sjhnatph0",
              "height": 2844,
              "width": 1260
            }
          ],
          "has_music": false,
          "timestamp": 1749518634,
          "corner_tag_info": [
            {
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RAE+CPFm14R+PsOoO3k7MP07ZIAZdJ6qw2S0z5N3M8MnWXxmLllczJOCWXE9g7+hJZBEChHV0k/RY4C4b69c1da6juZ8G6wttW",
              "text_en": ""
            },
            {
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-06-10",
              "text_en": "2025-06-10"
            }
          ],
          "collected": false,
          "last_update_time": 0,
          "niced": false,
          "cover_image_index": 0,
          "result_from": "",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"60f5d454000000002002a793\",\"author_name\":\"蛋\"}",
          "id": "6847892a0000000012002aa4",
          "title": "决赛圈！女生新手第一辆选哪个啊啊啊",
          "geo_info": {
            "distance": ""
          },
          "note_attributes": [],
          "comments_count": 577,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "nice_count": 0,
          "update_time": 1749518678000,
          "xsec_token": "YBqNLb0kJN9tbcRkLRkz5MP-ZAc_sgrU7XAuYCiXTeXsk=",
          "desc": "目前周围人都说gsx比较好 本人身高160，不知道座高能不能调 还有到底是买新的还是二手！ #决赛圈  #帮忙选一下",
          "liked_count": 919,
          "shared_count": 112
        }
      },
      {
        "model_type": "note",
        "note": {
          "liked": false,
          "timestamp": 1752226393,
          "collected_count": 141,
          "id": "6870da59000000002203c9c1",
          "title": "风是自由的你也是",
          "video_info_v2": {
            "media": {
              "user_level": 0,
              "video_id": 137483870248500130,
              "video": {
                "biz_name": 110,
                "biz_id": "281599059818170817",
                "bound": [
                  {
                    "w": 0,
                    "h": 0,
                    "x": 0,
                    "y": 0
                  }
                ],
                "opaque1": {
                  "bottomAvgLuma": "132",
                  "amend": "8",
                  "videoLanguage": "[\"zh-CN\"]",
                  "topAvgLuma": "93",
                  "audioLevInfo": "{\"audio_quality_level\":\"F\",\"mos_overall\":2.0112,\"version\":\"3.0\"}",
                  "hasHumanVoice": "true",
                  "amend_4k": "25",
                  "weakNetUserFlag": "1",
                  "amend_mobile": "40",
                  "domestic": "0",
                  "loudnorm": "{\"lra\":0.7,\"htp\":0.15,\"hldn\":-4.18,\"ldn\":-4.18,\"thr\":-14.18}",
                  "amend_2k": "25",
                  "audioClsInfo": "{\"music_ratio\":0.6892724180921803,\"freesound_ratio\":0.0160295911184228,\"speech_ratio\":0.09001231935729724}",
                  "isSupportSubtitle": "true",
                  "rightAvgLuma": "107"
                },
                "duration": 9,
                "md5": "07aef3250aaf4a3270647bef25e4545f",
                "hdr_type": 2,
                "drm_type": 0,
                "stream_types": [
                  258,
                  114,
                  22
                ],
                "width": 1080,
                "height": 1920
              },
              "stream": {
                "h264": [
                  {
                    "video_bitrate": 3868078,
                    "video_duration": 8366,
                    "weight": 49,
                    "fps": 30,
                    "opaque1": {
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": "",
                      "use_pcdn": "0"
                    },
                    "ssim": 0,
                    "default_stream": 0,
                    "audio_channels": 2,
                    "rotate": 0,
                    "volume": 0,
                    "audio_duration": 8335,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/79/110/258/01e870da0081fb9f4f03700197f8d5a22c_258.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/79/110/258/01e870da0081fb9f4f03700197f8d5a22c_258.mp4"
                    ],
                    "quality_type": "HD",
                    "sr": 0,
                    "hdr_type": 0,
                    "vmaf": -1,
                    "stream_desc": "X264_MP4",
                    "avg_bitrate": 3932326,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/79/110/258/01e870da0081fb9f4f03700197f8d5a22c_258.mp4",
                    "format": "mp4",
                    "size": 4112722,
                    "video_codec": "h264",
                    "duration": 8367,
                    "audio_codec": "aac",
                    "audio_bitrate": 56780,
                    "psnr": 0,
                    "stream_type": 258,
                    "width": 720,
                    "height": 1280
                  }
                ],
                "h265": [
                  {
                    "audio_bitrate": 129783,
                    "audio_duration": 8335,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/79/110/114/01e870da0081fb9f4f03700197f8d5758a_114.mp4",
                    "ssim": 0,
                    "opaque1": {
                      "didLoudnorm": "false",
                      "roiWeight": "71.9066",
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.0E-5\",\"mvmaf\":\"88.98969\"}",
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false"
                    },
                    "format": "mp4",
                    "audio_codec": "aac",
                    "audio_channels": 2,
                    "rotate": 0,
                    "hdr_type": 0,
                    "sr": 0,
                    "default_stream": 1,
                    "video_codec": "hevc",
                    "vmaf": -1,
                    "width": 720,
                    "video_duration": 8300,
                    "duration": 8336,
                    "size": 1918348,
                    "fps": 59,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/79/110/114/01e870da0081fb9f4f03700197f8d5758a_114.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/79/110/114/01e870da0081fb9f4f03700197f8d5758a_114.mp4"
                    ],
                    "stream_desc": "R265_MP4_720P_114_android",
                    "volume": 0,
                    "quality_type": "HD",
                    "stream_type": 114,
                    "psnr": 39.73099899291992,
                    "video_bitrate": 1708309,
                    "weight": 50,
                    "height": 1280,
                    "avg_bitrate": 1841024
                  },
                  {
                    "fps": 60,
                    "video_codec": "hevc",
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/79/110/22/01e870da0081fb9f0103700397f8d6ee6f_22.mp4",
                    "stream_type": 22,
                    "height": 1920,
                    "duration": 8336,
                    "avg_bitrate": 4471701,
                    "vmaf": -1,
                    "sr": 0,
                    "audio_duration": 8335,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/79/110/22/01e870da0081fb9f0103700397f8d6ee6f_22.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/79/110/22/01e870da0081fb9f0103700397f8d6ee6f_22.mp4"
                    ],
                    "ssim": 0,
                    "quality_type": "HD",
                    "width": 1080,
                    "video_duration": 8316,
                    "audio_bitrate": 129783,
                    "format": "mp4",
                    "size": 4659513,
                    "audio_codec": "aac",
                    "default_stream": 1,
                    "video_bitrate": 4341672,
                    "psnr": 0,
                    "stream_desc": "HDR_R265_MP4_22_ANDROID_multi",
                    "volume": 0,
                    "weight": 100,
                    "audio_channels": 2,
                    "rotate": 0,
                    "hdr_type": 2,
                    "opaque1": {
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    }
                  }
                ],
                "h266": [],
                "av1": []
              }
            },
            "image": {
              "thumbnail": "https://sns-na-i8.xhscdn.com/110/0/01e870da0081fb9f00100000000197f8d55adb_0.webp?imageView2/2/w/5000/h/5000/format/heif/q/56&redImage/frame/0&ap=5&sc=SRH_ORG&sign=4eb86d1415b6812be73d54c20217ed9f&t=69d8fcb3&origin=1",
              "thumbnail_dim": "https://sns-na-i8.xhscdn.com/110/0/01e870da0081fb9f00100000000197f8d55adb_0.webp?imageView2/2/w/720/h/720/format/heif/q/46|imageMogr2/strip&redImage/frame/0&ap=5&sc=SRH_SPRT&sign=4eb86d1415b6812be73d54c20217ed9f&t=69d8fcb3&origin=1"
            },
            "capa": {
              "is_user_select": false,
              "is_upload": false,
              "duration": 8,
              "frame_ts": 0
            },
            "consumer": {
              "can_super_resolution": false
            }
          },
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAYfE8P59f67o91lvud0h0DdBIOoCN3b4Bv/bqmqmctpa7S7IBU9/3lATj6+EB1eFjoeWfGyrEI++sC9/Lc1xj9Oxgqa5z3uif",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "text_en": "2025-07-11",
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-07-11"
            }
          ],
          "user": {
            "red_id": "63807619447",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "userid": "66f7b6f5000000001d020fa0",
            "track_duration": 0,
            "followed": false,
            "nickname": "阿林爱玩机车",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31jpsoqlrio005pnnmrqnc3t0nvm6ca8?imageView2/2/w/80/format/jpg",
            "red_official_verified": false
          },
          "images_list": [
            {
              "need_load_original_image": false,
              "fileid": "1040g00831jprelau32104b2fb395e3n196582v0",
              "height": 1920,
              "width": 1080,
              "url": "https://sns-na-i8.xhscdn.com/1040g00831jprelau32104b2fb395e3n196582v0?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=58a0372c17d24a97e32ff37e10197013&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831jprelau32104b2fb395e3n196582v0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=58a0372c17d24a97e32ff37e10197013&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831jprelau32104b2fb395e3n196582v0"
            }
          ],
          "last_update_time": 0,
          "geo_info": {
            "distance": ""
          },
          "update_time": 1752226468000,
          "xsec_token": "YB7RwkGd581S9EHoptsvHeyTs_asZxlmWKhhE1rJXKvtc=",
          "type": "video",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "has_music": false,
          "debug_info_str": "",
          "widgets_context": "{\"video\":true,\"origin_video_key\":\"pre_post/1040g2t031jprelatiom04b2fb395e3n1ktlc0d8\",\"flags\":{\"sound_track\":true},\"author_id\":\"66f7b6f5000000001d020fa0\",\"author_name\":\"阿林爱玩机车\",\"video_duration\":8}",
          "cover_image_index": 0,
          "result_from": "",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "note_collection",
                  "cooperate_binds",
                  "rec_next_infos",
                  "video_marks",
                  "product_review",
                  "related_search",
                  "video_goods_cards",
                  "cooperate_comment_component",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "video_recommend_tag",
                  "buyable_goods_card_v2",
                  "cooperate_search_component",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "related_recommend",
                  "next_note_guide",
                  "widgets_ndb",
                  "pgy_bbc_exp",
                  "brand_max_trailer",
                  "super_activity",
                  "note_nice_guide",
                  "pin_search_highlights",
                  "widgets_enhance",
                  "packed_goods",
                  "packed_buyable_goods",
                  "widgets_ncb",
                  "note_nice_compound",
                  "live_shooting_flag",
                  "widgets_nbb",
                  "poi_declare",
                  "async_group"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "guide_post",
                  "video_foot_bar",
                  "follow_guide",
                  "share_to_msg",
                  "note_share_prompt_v1",
                  "note_share_prompt_v2",
                  "group_share",
                  "share_guide_bubble",
                  "goods_enhance_component",
                  "guide_navigator",
                  "sync_group"
                ]
              }
            ]
          },
          "nice_count": 0,
          "note_attributes": [],
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "462"
          },
          "shared_count": 10,
          "comments_count": 21,
          "liked_count": 462,
          "collected": false,
          "niced": false,
          "desc": "有没有人跟我一样宣泄方式就是一个人骑车#赛600rs  #日常溜车  #机车男孩  #摩托车骑行  #男生穿搭  #追求",
          "extract_text_enabled": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "liked": false,
          "debug_info_str": "",
          "nice_count": 0,
          "collected_count": 342,
          "comments_count": 42,
          "timestamp": 1744612805,
          "geo_info": {
            "distance": ""
          },
          "corner_tag_info": [
            {
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RAfAlT6G8rSdNk2I7yzKzeW2ysNizCbZ64+IsH+YHub/GJwX1AOnrrKvNL738C940TXSToPqZn0LDJZlKidQ507YGCAYwi5JQk",
              "text_en": "",
              "style": 0,
              "location": -1
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-04-14",
              "text_en": "2025-04-14",
              "style": 0
            }
          ],
          "interaction_area": {
            "status": false,
            "text": "1102",
            "type": 1
          },
          "liked_count": 1102,
          "type": "normal",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"5a16276b4eacab5188ff5af0\",\"author_name\":\"西橙崽子\"}",
          "extract_text_enabled": 0,
          "shared_count": 169,
          "id": "67fcadc5000000001d005bdd",
          "title": "开启星耀黑模式",
          "images_list": [
            {
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghs7049vphtjmmmngts6g5o8",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs7049vphtjmmmngts6g5o8",
              "height": 1799,
              "width": 1440,
              "url": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs7049vphtjmmmngts6g5o8?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=835c066879036aa3a078bbe86f1060c8&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs7049vphtjmmmngts6g5o8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=835c066879036aa3a078bbe86f1060c8&t=69d8fcb3&origin=1"
            },
            {
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs7g49vphtjmmmngbd8l8i0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=69c87451e1e23ee5f43b82ff530fc3ce&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghs7g49vphtjmmmngbd8l8i0",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs7g49vphtjmmmngbd8l8i0",
              "height": 1800
            },
            {
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghs8049vphtjmmmngvt6va88",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs8049vphtjmmmngvt6va88",
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs8049vphtjmmmngvt6va88?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=79a3c2d07ad13769b7935d85a87a60a9&t=69d8fcb3&origin=1"
            },
            {
              "trace_id": "1040g2sg31g8eeh3ghs8g49vphtjmmmngns68j38",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs8g49vphtjmmmngns68j38",
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs8g49vphtjmmmngns68j38?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=3f183267c16af8e771e1e219382f611e&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs9049vphtjmmmngtf6h5t8",
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs9049vphtjmmmngtf6h5t8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=f9f3eb3af955197b473a9cc15be89f44&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghs9049vphtjmmmngtf6h5t8"
            },
            {
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghs9g49vphtjmmmng6vauhvg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e6bc95fc3045a35dcc5f9f260cede01f&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghs9g49vphtjmmmng6vauhvg",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghs9g49vphtjmmmng6vauhvg"
            },
            {
              "height": 1799,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghsa049vphtjmmmngu52h55g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1497e6e6ba2d1eb4bb03a5511f9e61d2&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghsa049vphtjmmmngu52h55g",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghsa049vphtjmmmngu52h55g"
            },
            {
              "fileid": "1040g2sg31g8eeh3ghsag49vphtjmmmng3fosn5g",
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghsag49vphtjmmmng3fosn5g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=fcf652b44af20d6df326b6073743fb38&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghsag49vphtjmmmng3fosn5g",
              "need_load_original_image": false
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghsb049vphtjmmmngj9nd2lg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=18cb4319951e0b1eadfa8317b9f68b87&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghsb049vphtjmmmngj9nd2lg",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghsb049vphtjmmmngj9nd2lg",
              "height": 1799,
              "width": 1440
            },
            {
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghsbg49vphtjmmmng9lp9tp8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=90fcc80b3f2642177f10853cbdc30817&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghsbg49vphtjmmmng9lp9tp8",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghsbg49vphtjmmmng9lp9tp8",
              "height": 1799
            },
            {
              "original": "",
              "trace_id": "1040g2sg31g8eeh3ghsc049vphtjmmmngks0fd70",
              "need_load_original_image": false,
              "fileid": "1040g2sg31g8eeh3ghsc049vphtjmmmngks0fd70",
              "height": 1800,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31g8eeh3ghsc049vphtjmmmngks0fd70?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=c8c867a00790f2ffb1bb52f7182c5577&t=69d8fcb3&origin=1"
            }
          ],
          "has_music": false,
          "niced": false,
          "xsec_token": "YBFRt1ee8UvjerTMtnmCATky0XPiW6kjq-l-ZetcJDVEI=",
          "desc": "碳纤维造就非凡差异 from:andoni #骑行  #摩托车  #改装车  #机车  #宝马  #仿赛",
          "result_from": "",
          "note_attributes": [],
          "collected": false,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "cover_image_index": 0,
          "update_time": 1744612851000,
          "user": {
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31av5m33ene0049vphtjmmmngtnbtbo0?imageView2/2/w/80/format/jpg",
            "red_official_verified": false,
            "userid": "5a16276b4eacab5188ff5af0",
            "followed": false,
            "red_id": "274655817",
            "nickname": "西橙崽子",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "track_duration": 0
          },
          "last_update_time": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "title": "第一天见他的样子",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "liked": false,
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RAIl1NXZbpBzsIXG4TDYk/DbaU8nxcS0LcBKrOeqpBC64GJX3vWQP7IUGHf2hxllH/c8slL4J3JbkmhMIUxSpJZDuOCyb24T0Y",
              "text_en": "",
              "style": 0
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2024-08-21",
              "text_en": "2024-08-21",
              "style": 0
            }
          ],
          "collected": false,
          "extract_text_enabled": 0,
          "nice_count": 0,
          "niced": false,
          "user": {
            "track_duration": 0,
            "followed": false,
            "red_id": "630297394",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "userid": "5a98496111be10577acbf34c",
            "nickname": "kk",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo315u1p7hi0q004a30ar4m3sqco7s95hg?imageView2/2/w/80/format/jpg"
          },
          "tag_info": {
            "title": "",
            "type": ""
          },
          "last_update_time": 0,
          "debug_info_str": "",
          "interaction_area": {
            "text": "386",
            "type": 1,
            "status": false
          },
          "collected_count": 82,
          "has_music": false,
          "liked_count": 386,
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "update_time": 1724177015000,
          "id": "66c4da52000000001d014ccd",
          "images_list": [
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g008316ntsk64gs004a30ar4m3sqcem3qte0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=8ab2352ccb1c104296af5e62ab2dfeb9&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g008316ntsk64gs004a30ar4m3sqcem3qte0",
              "need_load_original_image": false,
              "fileid": "1040g008316ntsk64gs004a30ar4m3sqcem3qte0",
              "height": 2560,
              "width": 1920,
              "url": "https://sns-na-i8.xhscdn.com/1040g008316ntsk64gs004a30ar4m3sqcem3qte0?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=8ab2352ccb1c104296af5e62ab2dfeb9&t=69d8fcb3&origin=1"
            },
            {
              "trace_id": "1040g008316ntsk64gs0g4a30ar4m3sqcpm5oc58",
              "need_load_original_image": false,
              "fileid": "1040g008316ntsk64gs0g4a30ar4m3sqcpm5oc58",
              "height": 2560,
              "width": 1920,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g008316ntsk64gs0g4a30ar4m3sqcpm5oc58?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4d07ed031d20160e14a9226273b440e5&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "height": 2560,
              "width": 1920,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g008316ntsk64gs104a30ar4m3sqcnosv6qo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4457ab57e6933c15ea5561074508b580&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g008316ntsk64gs104a30ar4m3sqcnosv6qo",
              "need_load_original_image": false,
              "fileid": "1040g008316ntsk64gs104a30ar4m3sqcnosv6qo"
            }
          ],
          "note_attributes": [],
          "shared_count": 35,
          "comments_count": 34,
          "desc": "这玩意儿谁研究的呢？#摩托车  #爱车  #仿赛  #每个男人都有一个机车梦  #杜卡迪  #薯队长  #日常骑行",
          "timestamp": 1724176978,
          "result_from": "",
          "xsec_token": "YBmLdEJmEwKMlQHcUg1Zt2RwlLWIuAH_CWxnJaaWfPT-o=",
          "type": "normal",
          "widgets_context": "{\"flags\":{\"filter\":true},\"author_id\":\"5a98496111be10577acbf34c\",\"author_name\":\"kk\"}"
        }
      },
      {
        "model_type": "note",
        "note": {
          "liked": false,
          "title": "🏍️",
          "has_music": false,
          "geo_info": {
            "distance": ""
          },
          "result_from": "",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "68"
          },
          "comments_count": 0,
          "id": "67d19d500000000029015f83",
          "liked_count": 68,
          "images_list": [
            {
              "need_load_original_image": false,
              "fileid": "1040g00831eucmaeplu005pj14lbgue7cmqosjh0",
              "height": 1440,
              "width": 1080,
              "url": "https://sns-na-i8.xhscdn.com/1040g00831eucmaeplu005pj14lbgue7cmqosjh0?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=74d94189bcfff9ac105d5a017d01fa34&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831eucmaeplu005pj14lbgue7cmqosjh0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=74d94189bcfff9ac105d5a017d01fa34&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831eucmaeplu005pj14lbgue7cmqosjh0"
            }
          ],
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "note_collection",
                  "cooperate_binds",
                  "rec_next_infos",
                  "video_marks",
                  "product_review",
                  "related_search",
                  "video_goods_cards",
                  "cooperate_comment_component",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "video_recommend_tag",
                  "buyable_goods_card_v2",
                  "cooperate_search_component",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "related_recommend",
                  "next_note_guide",
                  "widgets_ndb",
                  "pgy_bbc_exp",
                  "brand_max_trailer",
                  "super_activity",
                  "note_nice_guide",
                  "pin_search_highlights",
                  "widgets_enhance",
                  "packed_goods",
                  "packed_buyable_goods",
                  "widgets_ncb",
                  "note_nice_compound",
                  "live_shooting_flag",
                  "widgets_nbb",
                  "poi_declare",
                  "async_group"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "guide_post",
                  "video_foot_bar",
                  "follow_guide",
                  "share_to_msg",
                  "note_share_prompt_v1",
                  "note_share_prompt_v2",
                  "group_share",
                  "share_guide_bubble",
                  "goods_enhance_component",
                  "guide_navigator",
                  "sync_group"
                ]
              }
            ]
          },
          "collected": false,
          "shared_count": 0,
          "debug_info_str": "",
          "nice_count": 0,
          "niced": false,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "timestamp": 1741790544,
          "cover_image_index": 0,
          "widgets_context": "{\"video\":true,\"origin_video_key\":\"pre_post/1040g0cg31eucffn2lsf05pj14lbgue7c4qrim1o\",\"flags\":{\"sound_track\":true},\"author_id\":\"6661255700000000030338ec\",\"author_name\":\"zhi sheng\",\"video_duration\":17}",
          "collected_count": 21,
          "desc": "#摩托车  #夜骑  #新山  #ninja250  #ninja",
          "type": "video",
          "user": {
            "followed": false,
            "red_id": "26532882829",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31er69t29lu005pj14lbgue7c9ustsa0?imageView2/2/w/80/format/jpg",
            "userid": "6661255700000000030338ec",
            "track_duration": 0,
            "nickname": "zhi sheng",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false
          },
          "video_info_v2": {
            "media": {
              "video_id": 137308785044951790,
              "video": {
                "biz_name": 110,
                "hdr_type": 0,
                "drm_type": 0,
                "stream_types": [
                  258,
                  49,
                  85,
                  76,
                  77
                ],
                "opaque1": {
                  "audioClsInfo": "{\"music_ratio\":0.9971378936955986,\"freesound_ratio\":0.0,\"speech_ratio\":0.018889523818573336}",
                  "loudnorm": "{\"lra\":2.3,\"htp\":-3.11,\"hldn\":-13.43,\"ldn\":-13.68,\"thr\":-23.7}",
                  "amend": "8",
                  "hasHumanVoice": "true",
                  "audioLevInfo": "{\"audio_quality_level\":\"E\",\"mos_overall\":3.9392,\"version\":\"3.0\"}",
                  "amend_4k": "25",
                  "amend_2k": "25",
                  "videoLanguage": "[\"zh-CN\"]",
                  "amend_mobile": "40",
                  "weakNetUserFlag": "1",
                  "domestic": "0",
                  "isSupportSubtitle": "true"
                },
                "height": 1934,
                "biz_id": "281423975327031171",
                "duration": 18,
                "md5": "21925975f14d7273e1170d3b261f1bef",
                "bound": [
                  {
                    "h": 0,
                    "x": 0,
                    "y": 0,
                    "w": 0
                  }
                ],
                "width": 1088
              },
              "stream": {
                "h265": [
                  {
                    "avg_bitrate": 643259,
                    "opaque1": {
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "87.14172789753607",
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.0E-5\",\"mvmaf\":\"92.19519789753608\"}",
                      "use_pcdn": "1"
                    },
                    "height": 1280,
                    "hdr_type": 0,
                    "format": "mp4",
                    "fps": 50,
                    "psnr": 43.564998626708984,
                    "volume": 0,
                    "ssim": 0,
                    "video_bitrate": 505347,
                    "audio_duration": 17691,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/49/01e7d19ccd2512f401037003958c37901a_49.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/49/01e7d19ccd2512f401037003958c37901a_49.mp4"
                    ],
                    "default_stream": 1,
                    "width": 720,
                    "duration": 17700,
                    "video_duration": 17700,
                    "audio_codec": "aac",
                    "rotate": 0,
                    "weight": 47,
                    "stream_type": 49,
                    "audio_bitrate": 129018,
                    "audio_channels": 2,
                    "vmaf": -1,
                    "sr": 0,
                    "stream_desc": "R265_MP4_720P_49_ANDROID",
                    "size": 1423212,
                    "video_codec": "hevc",
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/49/01e7d19ccd2512f401037003958c37901a_49.mp4",
                    "quality_type": "HD"
                  },
                  {
                    "width": 1080,
                    "video_bitrate": 885068,
                    "audio_channels": 2,
                    "stream_type": 85,
                    "height": 1920,
                    "rotate": 0,
                    "vmaf": -1,
                    "sr": 0,
                    "stream_desc": "R265_MP4_1080P_85_and_low",
                    "default_stream": 0,
                    "audio_bitrate": 129018,
                    "size": 2263341,
                    "volume": 0,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/85/01e7d19ccd2512f401037001958ad02165_85.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/85/01e7d19ccd2512f401037001958ad02165_85.mp4"
                    ],
                    "psnr": 44.03799819946289,
                    "quality_type": "FHD",
                    "video_duration": 17700,
                    "audio_codec": "aac",
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/85/01e7d19ccd2512f401037001958ad02165_85.mp4",
                    "weight": 48,
                    "duration": 17700,
                    "avg_bitrate": 1022978,
                    "opaque1": {
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.0E-5\",\"mvmaf\":\"92.87314523847164\"}",
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "84.02246523847164"
                    },
                    "format": "mp4",
                    "fps": 50,
                    "video_codec": "hevc",
                    "audio_duration": 17691,
                    "hdr_type": 0,
                    "ssim": 0
                  },
                  {
                    "default_stream": 0,
                    "format": "mp4",
                    "fps": 50,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/76/01e7d19ccd2512f401037003958b1dc565_76.mp4",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/76/01e7d19ccd2512f401037003958b1dc565_76.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/76/01e7d19ccd2512f401037003958b1dc565_76.mp4"
                    ],
                    "video_codec": "hevc",
                    "audio_channels": 2,
                    "stream_desc": "R265_MP4_2K4K_76_ANDR_prediction",
                    "avg_bitrate": 2006946,
                    "ssim": 0,
                    "stream_type": 76,
                    "video_duration": 17700,
                    "audio_duration": 17677,
                    "duration": 17700,
                    "size": 4440370,
                    "audio_codec": "aac",
                    "audio_bitrate": 56493,
                    "hdr_type": 0,
                    "height": 2560,
                    "rotate": 0,
                    "vmaf": -1,
                    "weight": 49,
                    "width": 1440,
                    "video_bitrate": 1941573,
                    "quality_type": "2K",
                    "volume": 0,
                    "psnr": 46.78799819946289,
                    "sr": 0,
                    "opaque1": {
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.0E-5\",\"mvmaf\":\"94.62991403109376\"}",
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "75.21418403109377",
                      "pcdn_supplier": ""
                    }
                  },
                  {
                    "duration": 17700,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/77/01e7d19ccd2512f401037003958b1e4d48_77.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/77/01e7d19ccd2512f401037003958b1e4d48_77.mp4"
                    ],
                    "rotate": 0,
                    "audio_bitrate": 56493,
                    "audio_duration": 17677,
                    "height": 3840,
                    "hdr_type": 0,
                    "vmaf": -1,
                    "default_stream": 0,
                    "width": 2160,
                    "video_duration": 17700,
                    "sr": 0,
                    "weight": 50,
                    "opaque1": {
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.0E-5\",\"mvmaf\":\"96.73149561937501\"}",
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "65.544775619375"
                    },
                    "audio_codec": "aac",
                    "ssim": 0,
                    "quality_type": "4K",
                    "stream_type": 77,
                    "psnr": 48.08100128173828,
                    "size": 7044698,
                    "avg_bitrate": 3184044,
                    "video_bitrate": 3118672,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/77/01e7d19ccd2512f401037003958b1e4d48_77.mp4",
                    "stream_desc": "R265_MP4_2K4K_77_ANDR_xf",
                    "format": "mp4",
                    "video_codec": "hevc",
                    "audio_channels": 2,
                    "volume": 0,
                    "fps": 50
                  }
                ],
                "h266": [],
                "av1": [],
                "h264": [
                  {
                    "stream_desc": "X264_MP4",
                    "avg_bitrate": 1112536,
                    "audio_channels": 2,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/258/01e7d19ccd2512f401037001958aced249_258.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/258/01e7d19ccd2512f401037001958aced249_258.mp4"
                    ],
                    "vmaf": -1,
                    "size": 2461487,
                    "fps": 50,
                    "video_bitrate": 1047477,
                    "audio_codec": "aac",
                    "audio_duration": 17691,
                    "stream_type": 258,
                    "volume": 0,
                    "video_codec": "h264",
                    "quality_type": "HD",
                    "sr": 0,
                    "default_stream": 0,
                    "format": "mp4",
                    "duration": 17700,
                    "video_duration": 17700,
                    "audio_bitrate": 56445,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/258/01e7d19ccd2512f401037001958aced249_258.mp4",
                    "psnr": 0,
                    "opaque1": {
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    },
                    "height": 1280,
                    "hdr_type": 0,
                    "width": 720,
                    "rotate": 0,
                    "ssim": 0,
                    "weight": 46
                  }
                ]
              },
              "user_level": 0
            },
            "image": {
              "thumbnail": "https://sns-na-i8.xhscdn.com/110/0/01e7d19ccd2512f4001000000001958acf863d_0.webp?imageView2/2/w/5000/h/5000/format/heif/q/56&redImage/frame/0&ap=5&sc=SRH_ORG&sign=419563cd82a9f54a8af8436136a9e73c&t=69d8fcb3&origin=1",
              "thumbnail_dim": "https://sns-na-i8.xhscdn.com/110/0/01e7d19ccd2512f4001000000001958acf863d_0.webp?imageView2/2/w/720/h/720/format/heif/q/46|imageMogr2/strip&redImage/frame/0&ap=5&sc=SRH_SPRT&sign=419563cd82a9f54a8af8436136a9e73c&t=69d8fcb3&origin=1",
              "first_frame": "https://sns-na-i8.xhscdn.com/110/0/01e7d19ccd2512f4001000000001958acea5cc_0.jpg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d9f92d411e90aba0b8641fd32654af38&t=69d8fcb3&origin=1"
            },
            "capa": {
              "frame_ts": 0,
              "is_user_select": false,
              "is_upload": false,
              "duration": 17
            },
            "consumer": {
              "can_super_resolution": false
            }
          },
          "last_update_time": 0,
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RA8jEN8jS+59WLJl5eA6taV4WFmU9X+Eas8XIbx+uHoU4hT/d8pixlVZ41Zw8J1XUxX0Jz7TDcJE2RUE+ICNakMqziQy03Tfpq",
              "text_en": "",
              "style": 0
            },
            {
              "text_en": "2025-03-12",
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-03-12"
            }
          ],
          "extract_text_enabled": 0,
          "note_attributes": [],
          "update_time": 1741790599000,
          "xsec_token": "YBUUn5rqNh2DL28U4pNNdRezTSqs5TvqeGfalR5AmVohA="
        }
      },
      {
        "model_type": "note",
        "note": {
          "images_list": [
            {
              "original": "",
              "need_load_original_image": false,
              "live_photo_file_id": "livephoto_pre_post/1040g3jg31fdgk02r70005negof9g9bp50lm9rcg",
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6705negof9g9bp5lieqs50",
              "width": 3024,
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6705negof9g9bp5lieqs50?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=2ea60950ebe7cb7631dace42562b5bad&t=69d8fcb3&origin=1",
              "live_photo": {
                "media": {
                  "video_id": 137325814022161920,
                  "video": {
                    "hdr_type": 0,
                    "bound": [
                      {
                        "y": 0,
                        "w": 1920,
                        "h": 1440,
                        "x": 0
                      }
                    ],
                    "opaque1": {
                      "domestic": "0",
                      "livephoto_flag": "1",
                      "amend_mobile": "60",
                      "weakNetUserFlag": "1",
                      "amend": "8"
                    },
                    "stream_types": [
                      66
                    ],
                    "width": 1440,
                    "height": 1920,
                    "biz_name": 10,
                    "biz_id": "281441003074261296",
                    "duration": 2,
                    "drm_type": 0
                  },
                  "stream": {
                    "h264": [],
                    "h265": [
                      {
                        "duration": 1911,
                        "audio_channels": 2,
                        "token": "",
                        "stream_desc": "livephoto_r256_1080p_66_andr",
                        "audio_bitrate": 60037,
                        "hdrType": 0,
                        "ssim": 0,
                        "weight": 66,
                        "default_stream": 1,
                        "width": 1080,
                        "volume": 0,
                        "rotate": 0,
                        "backup_urls": [
                          "http://sns-bak-v8.xhscdn.com/stream/1/10/66/01e7e119ab4845fb0100500395c74d4cf5_66.mp4",
                          "http://sns-bak-v10.xhscdn.com/stream/1/10/66/01e7e119ab4845fb0100500395c74d4cf5_66.mp4"
                        ],
                        "quality_type": "FHD",
                        "sr": 0,
                        "fps": 29,
                        "video_duration": 1910,
                        "master_url": "http://sns-video-zl.xhscdn.com/stream/1/10/66/01e7e119ab4845fb0100500395c74d4cf5_66.mp4",
                        "opaque1": {
                          "pcdn_302_flag": "false",
                          "device_score": "0",
                          "didLoudnorm": "false",
                          "pcdn_supplier": "",
                          "amend": "0",
                          "has_soundtrack": "1",
                          "use_pcdn": "0"
                        },
                        "video_codec": "hevc",
                        "psnr": 39.387001037597656,
                        "size": 244243,
                        "avg_bitrate": 1022472,
                        "audio_duration": 1910,
                        "vmaf": -1,
                        "stream_type": 66,
                        "format": "mp4",
                        "height": 1440,
                        "video_bitrate": 948417,
                        "audio_codec": "aac"
                      }
                    ],
                    "h266": [],
                    "av1": []
                  },
                  "userLevel": 0
                }
              },
              "height": 4032,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6705negof9g9bp5lieqs50?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=2ea60950ebe7cb7631dace42562b5bad&t=69d8fcb3&origin=1",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6705negof9g9bp5lieqs50"
            },
            {
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n67g5negof9g9bp57ttlh88",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n67g5negof9g9bp57ttlh88?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1ff35f656dc9e7d97c47fdd20bb0b862&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n67g5negof9g9bp57ttlh88",
              "need_load_original_image": false
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6805negof9g9bp5b1anjoo",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6805negof9g9bp5b1anjoo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=c775431544930e68343f3f2ff791bced&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6805negof9g9bp5b1anjoo"
            },
            {
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n68g5negof9g9bp57a26ido",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n68g5negof9g9bp57a26ido?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=93e58d62a38acc630f11ed53e34007e7&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n68g5negof9g9bp57a26ido",
              "need_load_original_image": false
            },
            {
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6905negof9g9bp53d678n8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=14342713372f4072b4d49ea42bec3e94&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6905negof9g9bp53d678n8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6905negof9g9bp53d678n8"
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n69g5negof9g9bp5tjd0a68",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n69g5negof9g9bp5tjd0a68?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=880329a7cb5325ce2a8e1b5c9dd179fc&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n69g5negof9g9bp5tjd0a68"
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6a05negof9g9bp5uva25bo",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6a05negof9g9bp5uva25bo",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6a05negof9g9bp5uva25bo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1f27fde978345a76d97948b2f37d2f6e&t=69d8fcb3&origin=1"
            },
            {
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6ag5negof9g9bp58fak29o",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6ag5negof9g9bp58fak29o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4ce21b995faf1bc91f5a93ba0c296479&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6ag5negof9g9bp58fak29o",
              "need_load_original_image": false
            },
            {
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6b05negof9g9bp5h1f0jv8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=50f88fef6d3789b4b4b0a94c9c927e0e&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6b05negof9g9bp5h1f0jv8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6b05negof9g9bp5h1f0jv8",
              "height": 4032
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6bg5negof9g9bp5vh2m1pg",
              "height": 5712,
              "width": 4284,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6bg5negof9g9bp5vh2m1pg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=a93393f5759de5218c32b2b644fe4824&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6bg5negof9g9bp5vh2m1pg"
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6c05negof9g9bp5sa4qh7g",
              "height": 5712,
              "width": 4284,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6c05negof9g9bp5sa4qh7g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=3f3a52ea5e3d09b9b067485d2ef4ba19&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6c05negof9g9bp5sa4qh7g"
            },
            {
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6cg5negof9g9bp546nhk2g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4afced7c94a863db01e0debe7fb6fa0a&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6cg5negof9g9bp546nhk2g",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6cg5negof9g9bp546nhk2g"
            },
            {
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6d05negof9g9bp5i6s87m0",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6d05negof9g9bp5i6s87m0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=ef4dd880bbedf3aa2ff8ffdaa9f68c49&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6d05negof9g9bp5i6s87m0",
              "need_load_original_image": false
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031fdgjtj3n6dg5negof9g9bp57nudatg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=516b1dcbee61df3fd1aebff26b040ca3&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031fdgjtj3n6dg5negof9g9bp57nudatg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031fdgjtj3n6dg5negof9g9bp57nudatg",
              "height": 4032,
              "width": 3024,
              "url": ""
            },
            {
              "trace_id": "notes_pre_post/1040g3k831fdgk7i9n0705negof9g9bp50kuima0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831fdgk7i9n0705negof9g9bp50kuima0",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831fdgk7i9n0705negof9g9bp50kuima0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=867e520e5a15871d5acac07311bb957b&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831fdgk7i9n07g5negof9g9bp5e5jb4u0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d74e7a2ff42c8a01b46918ed6240973f&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831fdgk7i9n07g5negof9g9bp5e5jb4u0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831fdgk7i9n07g5negof9g9bp5e5jb4u0",
              "height": 4032,
              "width": 3024,
              "url": ""
            },
            {
              "trace_id": "notes_pre_post/1040g3k831fdgk7i9n0805negof9g9bp51oue18g",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831fdgk7i9n0805negof9g9bp51oue18g",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831fdgk7i9n0805negof9g9bp51oue18g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=b5dfec4b517a10b245b45090a6fa63b7&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831fdgk7i9n08g5negof9g9bp5r7btgt8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831fdgk7i9n08g5negof9g9bp5r7btgt8",
              "height": 4032,
              "width": 3024,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831fdgk7i9n08g5negof9g9bp5r7btgt8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=9c97c98330d5b00ee5d08468202b284d&t=69d8fcb3&origin=1"
            }
          ],
          "timestamp": 1742805477,
          "debug_info_str": "",
          "result_from": "",
          "widgets_context": "{\"flags\":{},\"author_id\":\"5dd0c3d3000000000100af25\",\"author_name\":\"两米\"}",
          "shared_count": 72,
          "liked": false,
          "desc": "地表最凶街车进化！首付**5737元全包落地**，引擎未响，肾上腺素已炸裂—— 🔥 208匹猛兽出笼，碳纤维刀锋劈开拥",
          "type": "normal",
          "id": "67e119e5000000001e009130",
          "nice_count": 0,
          "collected_count": 25,
          "extract_text_enabled": 0,
          "niced": false,
          "xsec_token": "YBRSrKeXhkZcOE8O9x0GMZ6OxjFQqB58CjJxCCATaruQM=",
          "title": "【杜卡迪街霸V4S｜5000首付撕破街头】",
          "geo_info": {
            "distance": ""
          },
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "105"
          },
          "liked_count": 105,
          "update_time": 1742805528000,
          "comments_count": 21,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "corner_tag_info": [
            {
              "text": "RARi6kL92Ey+lXUGLyk+98XsjApsrFLR4Ab2hr4tCPOK6CNJtxkUj8AdXiS3ePwPZCi1aiTl8sYaxOgufMXcMfJS25bAdDYTC5",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": ""
            },
            {
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-03-24",
              "text_en": "2025-03-24",
              "style": 0,
              "location": 5
            }
          ],
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "last_update_time": 0,
          "note_attributes": [],
          "collected": false,
          "user": {
            "followed": false,
            "nickname": "两米",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31l0s51f2jq005negof9g9bp5f1pgqkg?imageView2/2/w/80/format/jpg",
            "userid": "5dd0c3d3000000000100af25",
            "red_id": "Spaceflight06",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "track_duration": 0
          },
          "has_music": false,
          "cover_image_index": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "id": "695e0ea3000000002103f2ce",
          "type": "normal",
          "debug_info_str": "",
          "shared_count": 88,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "has_music": false,
          "note_attributes": [],
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "492"
          },
          "last_update_time": 1767789326,
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "xsec_token": "YBxebYFY7MTLKbsl1iRi8hmv24G6Ht91urMhiXvTtgXJM=",
          "collected_count": 87,
          "liked_count": 492,
          "cover_image_index": 0,
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RA6UykgQhg42sm2cJzljp/5Tp8MZHrZEdupkOFeT0eKzLaKbiVx67QDtDLfSlSFKbiqqh3nyx2qBS6LRCL72OsRxCTK/n807ZU",
              "text_en": "",
              "style": 0
            },
            {
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "01-07",
              "text_en": "01-07"
            }
          ],
          "update_time": 1768615283000,
          "liked": false,
          "desc": "杜卡迪V4S,别弄错了，那时候花了32万，车贩子就别考虑了，诚心买的就看车在说话，看公里数，别那别的车比",
          "geo_info": {
            "distance": ""
          },
          "niced": false,
          "comments_count": 359,
          "collected": false,
          "extract_text_enabled": 0,
          "nice_count": 0,
          "result_from": "",
          "widgets_context": "{\"flags\":{},\"author_id\":\"6118c9b2000000000100574f\",\"author_name\":\"绿光森林\"}",
          "title": "不骑了谁要，22年11月，540公里，一直放着",
          "user": {
            "followed": false,
            "nickname": "绿光森林",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo30pbios513u005o8op6p08lqfqiavavg?imageView2/2/w/80/format/jpg",
            "userid": "6118c9b2000000000100574f",
            "red_id": "2745505625",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "track_duration": 0
          },
          "images_list": [
            {
              "trace_id": "notes_pre_post/1040g3k031r1hgg6d7g6g5o8op6p08lqft13ccmg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031r1hgg6d7g6g5o8op6p08lqft13ccmg",
              "height": 4096,
              "width": 3072,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031r1hgg6d7g6g5o8op6p08lqft13ccmg?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=ca7efcf5480ffce4abfba89049523e85&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031r1hgg6d7g6g5o8op6p08lqft13ccmg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=ca7efcf5480ffce4abfba89049523e85&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031r1hgg6d7g605o8op6p08lqfcr16518",
              "height": 4096,
              "width": 3072,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031r1hgg6d7g605o8op6p08lqfcr16518?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=687b467d71dbe5956c421cc299242fb3&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031r1hgg6d7g605o8op6p08lqfcr16518"
            },
            {
              "width": 3072,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031r1hgg6d7g505o8op6p08lqfoae3afg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=5e6d742e5f4dbc9e5b6bc9e6a67ef10c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031r1hgg6d7g505o8op6p08lqfoae3afg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031r1hgg6d7g505o8op6p08lqfoae3afg",
              "height": 4096
            }
          ],
          "timestamp": 1767771811
        }
      },
      {
        "model_type": "note",
        "note": {
          "note_attributes": [],
          "widgets_context": "{\"video\":true,\"origin_video_key\":\"pre_post/1040g0cg31oujf2ut1as05p3ctso3698f87eht2o\",\"flags\":{\"sound_track\":true},\"author_id\":\"646cef30000000000c03250f\",\"author_name\":\"奶茶姐姐\",\"video_duration\":11}",
          "collected_count": 599,
          "tag_info": {
            "type": "",
            "title": ""
          },
          "last_update_time": 0,
          "user": {
            "red_official_verify_type": 0,
            "userid": "646cef30000000000c03250f",
            "track_duration": 0,
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31j9aaesk32005p3ctso3698f2imsf38?imageView2/2/w/80/format/jpg",
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "followed": false,
            "red_id": "8974001631",
            "nickname": "奶茶姐姐"
          },
          "result_from": "",
          "advanced_widgets_groups": {
            "groups": [
              {
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "note_collection",
                  "cooperate_binds",
                  "rec_next_infos",
                  "video_marks",
                  "product_review",
                  "related_search",
                  "video_goods_cards",
                  "cooperate_comment_component",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "video_recommend_tag",
                  "buyable_goods_card_v2",
                  "cooperate_search_component",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "related_recommend",
                  "next_note_guide",
                  "widgets_ndb",
                  "pgy_bbc_exp",
                  "brand_max_trailer",
                  "super_activity",
                  "note_nice_guide",
                  "pin_search_highlights",
                  "widgets_enhance",
                  "packed_goods",
                  "packed_buyable_goods",
                  "widgets_ncb",
                  "note_nice_compound",
                  "live_shooting_flag",
                  "widgets_nbb",
                  "poi_declare",
                  "async_group"
                ],
                "mode": 1
              },
              {
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "guide_post",
                  "video_foot_bar",
                  "follow_guide",
                  "share_to_msg",
                  "note_share_prompt_v1",
                  "note_share_prompt_v2",
                  "group_share",
                  "share_guide_bubble",
                  "goods_enhance_component",
                  "guide_navigator",
                  "sync_group"
                ],
                "mode": 0
              }
            ]
          },
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "2755"
          },
          "collected": false,
          "niced": false,
          "update_time": 1763279713000,
          "xsec_token": "YBs1hBPYe6OlfpvRoOtNcKUL7_ktnXDWk04mgEgQm5oMU=",
          "has_music": false,
          "type": "video",
          "video_info_v2": {
            "media": {
              "video_id": 137669313677251470,
              "video": {
                "stream_types": [
                  258,
                  178,
                  108,
                  77,
                  22,
                  91,
                  93,
                  224,
                  225,
                  226
                ],
                "height": 3840,
                "biz_id": "281784502858299205",
                "duration": 12,
                "md5": "34c199ca8f65034ca1a5302f2f7ccc74",
                "hdr_type": 1,
                "drm_type": 0,
                "biz_name": 110,
                "bound": [
                  {
                    "y": 0,
                    "w": 0,
                    "h": 0,
                    "x": 0
                  }
                ],
                "opaque1": {
                  "rightAvgLuma": "122",
                  "hasHumanVoice": "true",
                  "isSupportSubtitle": "true",
                  "videoLanguage": "[\"zh-CN\"]",
                  "audioClsInfo": "{\"music_ratio\":0.9999999161777103,\"freesound_ratio\":0.0,\"speech_ratio\":0.0}",
                  "amend_mobile": "40",
                  "audioLevInfo": "{\"audio_quality_level\":\"G+\",\"mos_overall\":3.6573,\"version\":\"3.0\"}",
                  "topAvgLuma": "89",
                  "domestic": "0",
                  "amend": "8",
                  "loudnorm": "{\"lra\":0.7,\"htp\":0.69,\"hldn\":-7.18,\"ldn\":-7.01,\"thr\":-17.01}",
                  "amend_2k": "25",
                  "amend_4k": "25",
                  "weakNetUserFlag": "1",
                  "bottomAvgLuma": "129"
                },
                "width": 2160
              },
              "stream": {
                "h265": [
                  {
                    "video_bitrate": 1751895,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/178/01e91982ea345394010370019a8c39cf02_178.mp4",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/178/01e91982ea345394010370019a8c39cf02_178.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/178/01e91982ea345394010370019a8c39cf02_178.mp4"
                    ],
                    "hdr_type": 0,
                    "stream_desc": "R265_MP4_720P_178_ANDROID",
                    "default_stream": 1,
                    "rotate": 0,
                    "opaque1": {
                      "roiWeight": "78.61486256859375",
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.5E-6\",\"mvmaf\":\"81.24270506859375\"}",
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false"
                    },
                    "volume": 0,
                    "quality_type": "HD",
                    "video_codec": "hevc",
                    "vmaf": -1,
                    "psnr": 39.887001037597656,
                    "ssim": 0,
                    "sr": 0,
                    "width": 720,
                    "duration": 11967,
                    "audio_bitrate": 117216,
                    "stream_type": 178,
                    "video_duration": 11966,
                    "audio_duration": 11946,
                    "audio_channels": 2,
                    "weight": 48,
                    "format": "mp4",
                    "height": 1280,
                    "size": 2816890,
                    "avg_bitrate": 1883105,
                    "fps": 60,
                    "audio_codec": "aac"
                  },
                  {
                    "volume": 0,
                    "fps": 60,
                    "video_duration": 11966,
                    "rotate": 0,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/108/01e91982ea345394010370019a8c2d24bc_108.mp4",
                    "weight": 49,
                    "default_stream": 0,
                    "audio_bitrate": 128233,
                    "hdr_type": 0,
                    "ssim": 0,
                    "audio_duration": 11959,
                    "quality_type": "2K",
                    "sr": 0,
                    "opaque1": {
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "86.035109844375",
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.5E-6\",\"mvmaf\":\"93.182329344375\"}"
                    },
                    "format": "mp4",
                    "size": 7333746,
                    "avg_bitrate": 4902646,
                    "audio_codec": "aac",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/108/01e91982ea345394010370019a8c2d24bc_108.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/108/01e91982ea345394010370019a8c2d24bc_108.mp4"
                    ],
                    "vmaf": -1,
                    "stream_type": 108,
                    "width": 1440,
                    "video_bitrate": 4764813,
                    "height": 2560,
                    "audio_channels": 2,
                    "stream_desc": "R265_MP4_2K4K_108_ANDR_xf",
                    "duration": 11967,
                    "video_codec": "hevc",
                    "psnr": 41.45399856567383
                  },
                  {
                    "height": 3840,
                    "fps": 60,
                    "rotate": 0,
                    "stream_desc": "R265_MP4_2K4K_77_ANDR_xf",
                    "avg_bitrate": 7827585,
                    "video_codec": "hevc",
                    "video_duration": 11966,
                    "sr": 0,
                    "volume": 0,
                    "hdr_type": 0,
                    "vmaf": -1,
                    "stream_type": 77,
                    "format": "mp4",
                    "duration": 11967,
                    "size": 11709090,
                    "audio_bitrate": 129259,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/77/01e91982ea345394010370019a8baac421_77.mp4",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/77/01e91982ea345394010370019a8baac421_77.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/77/01e91982ea345394010370019a8baac421_77.mp4"
                    ],
                    "weight": 50,
                    "default_stream": 0,
                    "ssim": 0,
                    "audio_codec": "aac",
                    "audio_duration": 11956,
                    "psnr": 43.16400146484375,
                    "width": 2160,
                    "audio_channels": 2,
                    "quality_type": "4K",
                    "video_bitrate": 7688833,
                    "opaque1": {
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "roiWeight": "80.694516594375",
                      "pcdn_supplier": "",
                      "roi_info": "{\"alpha\":\"1.0\",\"gamma\":\"0.0\",\"lambda\":\"1.5E-6\",\"mvmaf\":\"92.227766094375\"}",
                      "use_pcdn": "0"
                    }
                  },
                  {
                    "opaque1": {
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    },
                    "quality_type": "HD",
                    "sr": 0,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/22/01e91982ea345394010370019a8baac775_22.mp4",
                    "volume": 0,
                    "audio_duration": 11956,
                    "format": "mp4",
                    "height": 1920,
                    "size": 6786346,
                    "vmaf": -1,
                    "ssim": 0,
                    "stream_desc": "HDR_R265_MP4_22_ANDROID_multi",
                    "width": 1080,
                    "default_stream": 1,
                    "audio_channels": 2,
                    "audio_bitrate": 129259,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/22/01e91982ea345394010370019a8baac775_22.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/22/01e91982ea345394010370019a8baac775_22.mp4"
                    ],
                    "hdr_type": 2,
                    "psnr": 0,
                    "avg_bitrate": 4536706,
                    "video_duration": 11966,
                    "audio_codec": "aac",
                    "rotate": 0,
                    "stream_type": 22,
                    "fps": 60,
                    "video_bitrate": 4397860,
                    "weight": 100,
                    "duration": 11967,
                    "video_codec": "hevc"
                  },
                  {
                    "avg_bitrate": 5859847,
                    "fps": 60,
                    "audio_duration": 11956,
                    "hdr_type": 2,
                    "opaque1": {
                      "pcdn_supplier": "",
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false"
                    },
                    "stream_type": 91,
                    "video_bitrate": 5721039,
                    "audio_bitrate": 129259,
                    "audio_channels": 2,
                    "quality_type": "QHD",
                    "width": 1440,
                    "weight": 110,
                    "video_duration": 11966,
                    "audio_codec": "aac",
                    "default_stream": 0,
                    "format": "mp4",
                    "height": 2560,
                    "psnr": 0,
                    "ssim": 0,
                    "stream_desc": "HDR_R265_MP4_91_ANDROID_multi",
                    "video_codec": "hevc",
                    "sr": 0,
                    "duration": 11967,
                    "size": 8765600,
                    "volume": 0,
                    "rotate": 0,
                    "vmaf": -1,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/91/01e91982ea345394010370019a8ba95421_91.mp4",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/91/01e91982ea345394010370019a8ba95421_91.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/91/01e91982ea345394010370019a8ba95421_91.mp4"
                    ]
                  },
                  {
                    "audio_bitrate": 129259,
                    "audio_duration": 11956,
                    "ssim": 0,
                    "stream_desc": "HDR_R265_MP4_93_ANDROID_multi",
                    "video_codec": "hevc",
                    "audio_codec": "aac",
                    "rotate": 0,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/93/01e91982ea345394010370019a8baa87f7_93.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/93/01e91982ea345394010370019a8baa87f7_93.mp4"
                    ],
                    "default_stream": 0,
                    "volume": 0,
                    "audio_channels": 2,
                    "vmaf": -1,
                    "video_duration": 11966,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/93/01e91982ea345394010370019a8baa87f7_93.mp4",
                    "sr": 0,
                    "psnr": 0,
                    "opaque1": {
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    },
                    "size": 13561549,
                    "fps": 60,
                    "video_bitrate": 8927245,
                    "format": "mp4",
                    "height": 3840,
                    "weight": 120,
                    "avg_bitrate": 9065964,
                    "hdr_type": 2,
                    "quality_type": "UHD",
                    "stream_type": 93,
                    "width": 2160,
                    "duration": 11967
                  },
                  {
                    "fps": 60,
                    "video_bitrate": 4864620,
                    "audio_channels": 2,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/224/01e91982ea345394010370019a8baac666_224.mp4",
                    "weight": 130,
                    "quality_type": "HD",
                    "duration": 11957,
                    "volume": 0,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/224/01e91982ea345394010370019a8baac666_224.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/224/01e91982ea345394010370019a8baac666_224.mp4"
                    ],
                    "height": 1920,
                    "avg_bitrate": 5000808,
                    "size": 7474334,
                    "video_duration": 11950,
                    "vmaf": -1,
                    "psnr": 0,
                    "default_stream": 1,
                    "width": 1080,
                    "audio_bitrate": 129259,
                    "ssim": 0,
                    "format": "mp4",
                    "rotate": 0,
                    "sr": 0,
                    "stream_desc": "HDR_Dolby_R265_MP4_224_ANDROID_all",
                    "video_codec": "hevc",
                    "audio_duration": 11956,
                    "hdr_type": 1,
                    "stream_type": 224,
                    "opaque1": {
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    },
                    "audio_codec": "aac"
                  },
                  {
                    "avg_bitrate": 6068593,
                    "vmaf": -1,
                    "psnr": 0,
                    "format": "mp4",
                    "audio_duration": 11956,
                    "ssim": 0,
                    "default_stream": 0,
                    "audio_codec": "aac",
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/225/01e91982ea345394010370019a8baa0179_225.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/225/01e91982ea345394010370019a8baa0179_225.mp4"
                    ],
                    "video_duration": 11950,
                    "audio_channels": 2,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/225/01e91982ea345394010370019a8baa0179_225.mp4",
                    "quality_type": "QHD",
                    "stream_desc": "HDR_Dolby_R265_MP4_225_ANDROID_all",
                    "height": 2560,
                    "duration": 11957,
                    "fps": 60,
                    "rotate": 0,
                    "audio_bitrate": 129259,
                    "width": 1440,
                    "video_codec": "hevc",
                    "video_bitrate": 5933031,
                    "weight": 140,
                    "stream_type": 225,
                    "size": 9070272,
                    "volume": 0,
                    "hdr_type": 1,
                    "sr": 0,
                    "opaque1": {
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": "",
                      "use_pcdn": "1"
                    }
                  },
                  {
                    "width": 2160,
                    "avg_bitrate": 9266081,
                    "sr": 0,
                    "stream_type": 226,
                    "vmaf": -1,
                    "format": "mp4",
                    "height": 3840,
                    "duration": 11957,
                    "volume": 0,
                    "fps": 60,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/226/01e91982ea345394010370019a8bac8534_226.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/226/01e91982ea345394010370019a8bac8534_226.mp4"
                    ],
                    "quality_type": "UHD",
                    "opaque1": {
                      "use_pcdn": "1",
                      "pcdn_302_flag": "false",
                      "didLoudnorm": "false",
                      "pcdn_supplier": ""
                    },
                    "default_stream": 0,
                    "video_codec": "hevc",
                    "stream_desc": "HDR_Dolby_R265_MP4_226_ANDROID_all",
                    "size": 13849317,
                    "video_bitrate": 9132392,
                    "audio_duration": 11956,
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/226/01e91982ea345394010370019a8bac8534_226.mp4",
                    "video_duration": 11950,
                    "audio_bitrate": 129259,
                    "hdr_type": 1,
                    "psnr": 0,
                    "ssim": 0,
                    "audio_codec": "aac",
                    "audio_channels": 2,
                    "rotate": 0,
                    "weight": 150
                  }
                ],
                "h266": [],
                "av1": [],
                "h264": [
                  {
                    "master_url": "http://sns-video-zl.xhscdn.com/stream/1/110/258/01e91982ea345394010370019a8ba8e353_258.mp4",
                    "quality_type": "HD",
                    "height": 1280,
                    "backup_urls": [
                      "http://sns-bak-v8.xhscdn.com/stream/1/110/258/01e91982ea345394010370019a8ba8e353_258.mp4",
                      "http://sns-bak-v10.xhscdn.com/stream/1/110/258/01e91982ea345394010370019a8ba8e353_258.mp4"
                    ],
                    "opaque1": {
                      "didLoudnorm": "false",
                      "pcdn_supplier": "",
                      "use_pcdn": "0",
                      "pcdn_302_flag": "false"
                    },
                    "avg_bitrate": 4189053,
                    "fps": 30,
                    "width": 720,
                    "psnr": 0,
                    "video_bitrate": 4124499,
                    "audio_duration": 11956,
                    "stream_type": 258,
                    "default_stream": 0,
                    "volume": 0,
                    "audio_bitrate": 56852,
                    "rotate": 0,
                    "hdr_type": 0,
                    "vmaf": -1,
                    "weight": 47,
                    "stream_desc": "X264_MP4",
                    "size": 6283580,
                    "video_codec": "h264",
                    "video_duration": 12000,
                    "audio_codec": "aac",
                    "sr": 0,
                    "format": "mp4",
                    "audio_channels": 2,
                    "ssim": 0,
                    "duration": 12000
                  }
                ]
              },
              "user_level": 0
            },
            "image": {
              "first_frame": "https://sns-na-i8.xhscdn.com/110/0/01e91982ea3453940010000000019a8ba86ec4_0.jpg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=938012a4212c885d0cc545893f682c66&t=69d8fcb3&origin=1",
              "thumbnail": "https://sns-na-i8.xhscdn.com/frame/110/0/01e91982ea3453940010000000019a8ba9e185_0.webp?imageView2/2/w/5000/h/5000/format/heif/q/56&redImage/frame/0&ap=5&sc=SRH_ORG&sign=83c33b880dc6c63754dde0e4fbdb919b&t=69d8fcb3&origin=1",
              "thumbnail_dim": "https://sns-na-i8.xhscdn.com/frame/110/0/01e91982ea3453940010000000019a8ba9e185_0.webp?imageView2/2/w/720/h/720/format/heif/q/46|imageMogr2/strip&redImage/frame/0&ap=5&sc=SRH_SPRT&sign=83c33b880dc6c63754dde0e4fbdb919b&t=69d8fcb3&origin=1"
            },
            "capa": {
              "is_upload": false,
              "duration": 11,
              "frame_ts": 0,
              "is_user_select": false
            },
            "consumer": {
              "can_super_resolution": false
            }
          },
          "liked_count": 2755,
          "debug_info_str": "",
          "corner_tag_info": [
            {
              "text": "RAW0j03ATNdB7QoeoW3ndzgu0S1vVBKWoqiBx0KXRHUaXuxTHjby2yYega7aWfEkuG1lv/QUJYeNb5qPpinr7yKVNPJp6tX1ea",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": ""
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-11-16",
              "text_en": "2025-11-16",
              "style": 0
            }
          ],
          "nice_count": 0,
          "images_list": [
            {
              "original": "",
              "trace_id": "1040g2sg31oujf2ut1ge05p3ctso3698f4kfp4fg",
              "need_load_original_image": false,
              "fileid": "1040g2sg31oujf2ut1ge05p3ctso3698f4kfp4fg",
              "height": 1920,
              "width": 1440,
              "url": "https://sns-na-i8.xhscdn.com/1040g2sg31oujf2ut1ge05p3ctso3698f4kfp4fg?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=1f90279978f9871b0ccdfd6874d110f8&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31oujf2ut1ge05p3ctso3698f4kfp4fg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1f90279978f9871b0ccdfd6874d110f8&t=69d8fcb3&origin=1"
            }
          ],
          "desc": "如果你也喜欢机车 那我们就是朋友 #机车梦",
          "timestamp": 1763279660,
          "liked": false,
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "extract_text_enabled": 0,
          "shared_count": 133,
          "comments_count": 60,
          "id": "6919832c0000000005003745"
        }
      },
      {
        "model_type": "note",
        "note": {
          "cover_image_index": 0,
          "note_attributes": [],
          "tag_info": {
            "title": "",
            "type": ""
          },
          "last_update_time": 0,
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RADyfMqjbedfoMkzC8WOSonmzJntblKwZIUNkLj9cfSy6djY0Za7EzTqFrvAjdoX4MdmUuwjgLRoXcRK2SDyvCkcQ6DHDRIcWX",
              "text_en": "",
              "style": 0
            },
            {
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "02-26",
              "text_en": "02-26"
            }
          ],
          "shared_count": 79,
          "nice_count": 0,
          "liked_count": 403,
          "user": {
            "red_id": "339065003",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31ejap8c1h6005no473b0btgi65agve0?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "track_duration": 0,
            "followed": false,
            "nickname": "珍妮佛梁是Car迷",
            "red_official_verified": false,
            "userid": "5f0438d6000000000101f612"
          },
          "update_time": 1773427812000,
          "desc": "赛道用本田，飙车用铃木，泡妞用雅马哈，玩命用川崎。让你感受飞机般的速度。上车之前你的命已经不属于你，一切与你无关，一档破",
          "type": "normal",
          "result_from": "",
          "images_list": [
            {
              "trace_id": "1040g00831t1tvkqq5c005no473b0btgiei2e7k0",
              "need_load_original_image": false,
              "fileid": "1040g00831t1tvkqq5c005no473b0btgiei2e7k0",
              "height": 1555,
              "width": 1170,
              "url": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c005no473b0btgiei2e7k0?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=0ca1338afb8021cc89c1df2dedce87fe&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c005no473b0btgiei2e7k0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=0ca1338afb8021cc89c1df2dedce87fe&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "fileid": "1040g00831t1tvkqq5c0g5no473b0btgij1umdq8",
              "height": 1555,
              "width": 1170,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c0g5no473b0btgij1umdq8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d526b3ad44b10a2a952f70ad3d890908&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831t1tvkqq5c0g5no473b0btgij1umdq8",
              "need_load_original_image": false
            },
            {
              "original": "",
              "trace_id": "1040g00831t1tvkqq5c105no473b0btgi4p193m8",
              "need_load_original_image": false,
              "fileid": "1040g00831t1tvkqq5c105no473b0btgi4p193m8",
              "height": 1545,
              "width": 1170,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c105no473b0btgi4p193m8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=9e772705b13cfe302cd161f1a1107041&t=69d8fcb3&origin=1"
            },
            {
              "fileid": "1040g00831t1tvkqq5c1g5no473b0btgirog517o",
              "height": 1617,
              "width": 1170,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c1g5no473b0btgirog517o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=94e2be71404e0ad35734c0b320334c8c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831t1tvkqq5c1g5no473b0btgirog517o",
              "need_load_original_image": false
            },
            {
              "original": "",
              "trace_id": "1040g00831t1tvkqq5c205no473b0btgi17ugk30",
              "need_load_original_image": false,
              "fileid": "1040g00831t1tvkqq5c205no473b0btgi17ugk30",
              "height": 1549,
              "width": 1170,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831t1tvkqq5c205no473b0btgi17ugk30?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=995d3938739d975625d83ac49277014e&t=69d8fcb3&origin=1"
            }
          ],
          "has_music": false,
          "title": "青春没有售价，疯狂就在当下。",
          "xsec_token": "YBn3Qkw8b0gcWJl6QF8WVQ-1bV8dG1QhopnEEqg7KLAQg=",
          "niced": false,
          "geo_info": {
            "distance": ""
          },
          "extract_text_enabled": 0,
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "403"
          },
          "comments_count": 22,
          "timestamp": 1772092905,
          "debug_info_str": "",
          "advanced_widgets_groups": {
            "groups": [
              {
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ],
                "mode": 1
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"5f0438d6000000000101f612\",\"author_name\":\"珍妮佛梁是Car迷\"}",
          "collected": false,
          "collected_count": 170,
          "liked": false,
          "id": "699ffde9000000002203b615"
        }
      },
      {
        "model_type": "note",
        "note": {
          "desc": "整车大保养油水刚换 安全行驶两万公里 成色细节漂亮 三套版花 带三者保险 全款十万多一点点",
          "images_list": [
            {
              "fileid": "notes_pre_post/1040g3k031thhgnunme705pq03o7n39kjgre9fto",
              "height": 1920,
              "width": 1440,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme705pq03o7n39kjgre9fto?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=e7dcf56a20ec6718fdd1c1a2abbd249b&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme705pq03o7n39kjgre9fto?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e7dcf56a20ec6718fdd1c1a2abbd249b&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunme705pq03o7n39kjgre9fto",
              "need_load_original_image": false
            },
            {
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme7g5pq03o7n39kj7ee5us8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4fa519f9768282a1de0c263165fab3ad&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunme7g5pq03o7n39kj7ee5us8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunme7g5pq03o7n39kj7ee5us8",
              "height": 1080
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme805pq03o7n39kjacc1n68?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=c6efddcc961e7d1a729844b8fa21428d&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunme805pq03o7n39kjacc1n68",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunme805pq03o7n39kjacc1n68",
              "height": 1920,
              "width": 1440,
              "url": ""
            },
            {
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunme8g5pq03o7n39kjom47kvg",
              "height": 1080,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme8g5pq03o7n39kjom47kvg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=84ad6d0ab49c9caf73857481a2c19d0c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunme8g5pq03o7n39kjom47kvg"
            },
            {
              "trace_id": "notes_pre_post/1040g3k031thhgnunme905pq03o7n39kja9tvfuo",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunme905pq03o7n39kja9tvfuo",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme905pq03o7n39kja9tvfuo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=98b794de12516a3f756235f7f65472f7&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunme9g5pq03o7n39kj1cdrav0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=7dbc3eac9ee592e4e23a58b3c41592b9&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunme9g5pq03o7n39kj1cdrav0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunme9g5pq03o7n39kj1cdrav0",
              "height": 1920
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunmea05pq03o7n39kjsp6uj6o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=7f7e09335b57e8a29961ec753b912695&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunmea05pq03o7n39kjsp6uj6o",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunmea05pq03o7n39kjsp6uj6o",
              "height": 1920,
              "width": 1440,
              "url": ""
            },
            {
              "fileid": "notes_pre_post/1040g3k031thhgnunmeag5pq03o7n39kjnrgqqf8",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunmeag5pq03o7n39kjnrgqqf8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=44e3c1681543642a6fc2725443c0f4c6&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunmeag5pq03o7n39kjnrgqqf8",
              "need_load_original_image": false
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031thhgnunmeb05pq03o7n39kjkh70t9g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=bdbff563bfd0fa5986a444c3a5a55d08&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031thhgnunmeb05pq03o7n39kjkh70t9g",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031thhgnunmeb05pq03o7n39kjkh70t9g",
              "height": 1920,
              "width": 1440,
              "url": ""
            }
          ],
          "debug_info_str": "",
          "extract_text_enabled": 0,
          "update_time": 1773140876000,
          "id": "69affa4f000000002202132c",
          "title": "亏本出宝马s1000rr",
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "xsec_token": "YBaDSJ5LzEk6X4RDCEle9O18TN-wBKwn0BHiVkdnaRFfI=",
          "type": "normal",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "timestamp": 1773140559,
          "note_attributes": [],
          "user": {
            "userid": "67401e0f000000001c01a693",
            "nickname": "摩托公爵",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31s7rp2thl6005pq03o7n39kjj760v2g?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "followed": false,
            "red_id": "95418551730",
            "red_official_verified": false,
            "track_duration": 0
          },
          "has_music": false,
          "widgets_context": "{\"flags\":{},\"author_id\":\"67401e0f000000001c01a693\",\"author_name\":\"摩托公爵\"}",
          "interaction_area": {
            "text": "5",
            "type": 1,
            "status": false
          },
          "collected": false,
          "nice_count": 0,
          "niced": false,
          "comments_count": 7,
          "liked_count": 5,
          "result_from": "",
          "corner_tag_info": [
            {
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RA3RRsukMahbwMUqnXBSz6GV59bdXgwMRMMK3SE/kZKdQX9j9VYzlEXm7a/58lhi2ST2AHSn9TFZiTSrPRD4314JEHa9V5hrIh",
              "text_en": ""
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "03-10",
              "text_en": "03-10",
              "style": 0
            }
          ],
          "shared_count": 1,
          "collected_count": 4,
          "last_update_time": 1773140837,
          "liked": false
        }
      },
      {
        "model_type": "note",
        "note": {
          "debug_info_str": "",
          "geo_info": {
            "distance": ""
          },
          "extract_text_enabled": 0,
          "collected_count": 732,
          "liked": false,
          "title": "每天了解一台车：闪 300 AMT 🏍️",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "cover_image_index": 0,
          "nice_count": 0,
          "images_list": [
            {
              "height": 1562,
              "width": 1171,
              "url": "https://sns-na-i8.xhscdn.com/spectrum/1040g34o31fstdqsr0c0g5nui2kb08ve5iqj8u70?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=4589e25d769e4c1fbf7a48d741622364&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g34o31fstdqsr0c0g5nui2kb08ve5iqj8u70?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4589e25d769e4c1fbf7a48d741622364&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g34o31fstdqsr0c0g5nui2kb08ve5iqj8u70",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g34o31fstdqsr0c0g5nui2kb08ve5iqj8u70"
            },
            {
              "trace_id": "spectrum/1040g0k031fstegk47i005nui2kb08ve5mcd51lo",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstegk47i005nui2kb08ve5mcd51lo",
              "height": 1402,
              "width": 1051,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstegk47i005nui2kb08ve5mcd51lo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=ff295b74de99fef456bd9468cc973d5d&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "trace_id": "spectrum/1040g0k031fstfug67i005nui2kb08ve525ku9t0",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstfug67i005nui2kb08ve525ku9t0",
              "height": 1510,
              "width": 1132,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstfug67i005nui2kb08ve525ku9t0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d74ff34e0162ac55bfb3ef953f2b5973&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "original": "",
              "trace_id": "spectrum/1040g34o31fstf6sl7e0g5nui2kb08ve5vjmkiro",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g34o31fstf6sl7e0g5nui2kb08ve5vjmkiro",
              "height": 1537,
              "width": 1153,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g34o31fstf6sl7e0g5nui2kb08ve5vjmkiro?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=d051987773fcc04f7d3f1feda81fc017&t=69d8fcb3&origin=1"
            },
            {
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstdcshnk005nui2kb08ve5d5n59f8",
              "height": 1720,
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstdcshnk005nui2kb08ve5d5n59f8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=b60d1507c5792fe21ac0b8cf070edeba&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g0k031fstdcshnk005nui2kb08ve5d5n59f8"
            },
            {
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstdkg0ge005nui2kb08ve5nac7558",
              "height": 1720,
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstdkg0ge005nui2kb08ve5nac7558?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=6e9d2537902d4d23d629d5805d88efb2&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g0k031fstdkg0ge005nui2kb08ve5nac7558"
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstepuu0c005nui2kb08ve5sjo106g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=cb11dc3c1fe7ce3b6a8952a79c4e0cea&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g0k031fstepuu0c005nui2kb08ve5sjo106g",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstepuu0c005nui2kb08ve5sjo106g",
              "height": 1720,
              "width": 1290
            },
            {
              "height": 1720,
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstdh3k0e005nui2kb08ve51aeqjvg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=306d00c5541ce3133511c74508ee8de5&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g0k031fstdh3k0e005nui2kb08ve51aeqjvg",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstdh3k0e005nui2kb08ve51aeqjvg"
            },
            {
              "width": 1037,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g34o31fstffea7k0g5nui2kb08ve5ui166to?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=874c8da464cbfa182d622720f88092e9&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g34o31fstffea7k0g5nui2kb08ve5ui166to",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g34o31fstffea7k0g5nui2kb08ve5ui166to",
              "height": 1383
            },
            {
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g0k031fstevrhni005nui2kb08ve5cukotvo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=db8b3ff5d5f637e6f63f427ee4087036&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g0k031fstevrhni005nui2kb08ve5cukotvo",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g0k031fstevrhni005nui2kb08ve5cukotvo",
              "height": 1720
            },
            {
              "height": 1720,
              "width": 1290,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/spectrum/1040g34o31fstfnvgni0g5nui2kb08ve54cmip90?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e967225867bb28663e91fa695294b181&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "spectrum/1040g34o31fstfnvgni0g5nui2kb08ve54cmip90",
              "need_load_original_image": false,
              "fileid": "spectrum/1040g34o31fstfnvgni0g5nui2kb08ve54cmip90"
            }
          ],
          "result_from": "",
          "collected": false,
          "timestamp": 1743850204,
          "note_attributes": [],
          "update_time": 1743850204000,
          "xsec_token": "YBiV3nNha2c-iLYU56R8YV42_ReGsxFPTY7Otbhl1GypY=",
          "liked_count": 1666,
          "last_update_time": 0,
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAqVS17t0vyxWM+CnG7Sxs+o2imjnNABkGziivGW3CAykwxE2/jdqKFY65dmSm044yYiyyEcpjw4690HX8IfmD3iw1W2aAhJsK",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "text_en": "2025-04-05",
              "style": 0,
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-04-05"
            }
          ],
          "id": "67f0f477000000001d03a23d",
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"5fd215160000000001007dc5\",\"author_name\":\"压根不懂车\"}",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "1666"
          },
          "comments_count": 178,
          "desc": "🌟钱江闪300AMT版深度测评 | 参数解析+优缺点+适合谁买？看完再冲！🌟 作为国产巡航初次搭载AMT系统的车型",
          "type": "normal",
          "user": {
            "track_duration": 0,
            "red_id": "A01094922",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31di2gteq0c005nui2kb08ve5ufonjuo?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "followed": false,
            "nickname": "压根不懂车",
            "userid": "5fd215160000000001007dc5"
          },
          "has_music": false,
          "shared_count": 1214,
          "niced": false
        }
      },
      {
        "note": {
          "timestamp": 1762528455,
          "result_from": "",
          "update_time": 1762528715000,
          "comments_count": 307,
          "xsec_token": "YB0ac6yTJ_gV0Ww60kElIT4MQfHJRvfzK572QCNpUgMw4=",
          "title": "98年👧🏻 全款2万➕拿下人生第一辆摩托🏍️",
          "user": {
            "followed": false,
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "userid": "5b80a6883be3260001870967",
            "track_duration": 0,
            "red_id": "LLHHNN",
            "nickname": "Kkoo.",
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1000g2jo2obllo64ju0004ajdq0j8g2b75d03ilo?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0
          },
          "tag_info": {
            "title": "",
            "type": ""
          },
          "images_list": [
            {
              "height": 2912,
              "width": 2160,
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog64g4ajdq0j8g2b7fcp2mmo?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=589b8b3edaad40f80486f810be9dcda1&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog64g4ajdq0j8g2b7fcp2mmo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=589b8b3edaad40f80486f810be9dcda1&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog64g4ajdq0j8g2b7fcp2mmo",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog64g4ajdq0j8g2b7fcp2mmo"
            },
            {
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog6004ajdq0j8g2b7qn5qp18?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=07f7e42815c83b0d53a3167da8f9ff97&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog6004ajdq0j8g2b7qn5qp18",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog6004ajdq0j8g2b7qn5qp18"
            },
            {
              "fileid": "notes_pre_post/1040g3k031ojd1tmog60g4ajdq0j8g2b7m39m570",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog60g4ajdq0j8g2b7m39m570?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=a949c9abba9ee3bb952bb45c29f7de77&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog60g4ajdq0j8g2b7m39m570",
              "need_load_original_image": false
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog6104ajdq0j8g2b7q5oo960",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog6104ajdq0j8g2b7q5oo960",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog6104ajdq0j8g2b7q5oo960?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=1926dabbdc1e2eb01950a85eaa29b3d4&t=69d8fcb3&origin=1"
            },
            {
              "fileid": "notes_pre_post/1040g3k031ojd1tmog61g4ajdq0j8g2b7g0lq6lg",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog61g4ajdq0j8g2b7g0lq6lg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4ab930ca16e956031f168264798df6b5&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog61g4ajdq0j8g2b7g0lq6lg",
              "need_load_original_image": false
            },
            {
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog6204ajdq0j8g2b7bj05758",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog6204ajdq0j8g2b7bj05758",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog6204ajdq0j8g2b7bj05758?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=546b51db7c6bfd6b58223e08ac19b137&t=69d8fcb3&origin=1"
            },
            {
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog62g4ajdq0j8g2b7ev6p1fo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=528c173447d7b96779b2e2cf1190731c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog62g4ajdq0j8g2b7ev6p1fo",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog62g4ajdq0j8g2b7ev6p1fo",
              "height": 2880
            },
            {
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog6304ajdq0j8g2b7apsetm0",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog6304ajdq0j8g2b7apsetm0",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog6304ajdq0j8g2b7apsetm0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=c1e566643e72f3b30645f7d6ca8f2f63&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog63g4ajdq0j8g2b75a0q7v8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog63g4ajdq0j8g2b75a0q7v8",
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog63g4ajdq0j8g2b75a0q7v8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=a8701c552f0d63e29b68a204e5c330a3&t=69d8fcb3&origin=1",
              "original": ""
            },
            {
              "height": 2880,
              "width": 2160,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k031ojd1tmog6404ajdq0j8g2b7aockap8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=46123df94d0a5b00e74514d6df6a44ce&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k031ojd1tmog6404ajdq0j8g2b7aockap8",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k031ojd1tmog6404ajdq0j8g2b7aockap8"
            }
          ],
          "widgets_context": "{\"flags\":{},\"author_id\":\"5b80a6883be3260001870967\",\"author_name\":\"Kkoo.\"}",
          "id": "690e0cc70000000003010fe4",
          "shared_count": 573,
          "collected_count": 864,
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "1865"
          },
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAUxlRzrvpa29ubzu2PGTnk5IZDEjeCkI63lu1U2i5XIJwFe7xhD26xnimR6VLViYlvX/yPs8NUyG+uan5k/+XTxSYI4Pbicn7",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "location": 5,
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-11-07",
              "text_en": "2025-11-07",
              "style": 0
            }
          ],
          "collected": false,
          "extract_text_enabled": 0,
          "nice_count": 0,
          "desc": "27岁 先买车 再考驾照😎 今天全款拿下一辆自己的摩托车🏍️ 一开始纠结 奔达拿破仑or春风CLC450 试驾之后",
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "liked_count": 1865,
          "note_attributes": [],
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "liked": false,
          "niced": false,
          "debug_info_str": "",
          "type": "normal",
          "has_music": false,
          "last_update_time": 1762528676
        },
        "model_type": "note"
      },
      {
        "model_type": "note",
        "note": {
          "desc": "银色+已改灯，22年（包括）之后的车，过户次数少 这条件苛刻不？ 或者川崎Z400 #二手摩托车  #爱机车爱生活爱骑行",
          "has_music": false,
          "last_update_time": 1769579960,
          "update_time": 1769580000000,
          "xsec_token": "YB-moa00blUSwc-LeWw08YtRPODyTSw0p4c1AThB3sZcU=",
          "type": "normal",
          "user": {
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31ru8nid520705q161k6ji77o21tltpg?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "show_red_official_verify_icon": false,
            "followed": false,
            "nickname": "霱謩",
            "userid": "68260d0d000000000e011cf8",
            "track_duration": 0,
            "red_id": "95046411913",
            "red_official_verified": false
          },
          "cover_image_index": 0,
          "geo_info": {
            "distance": ""
          },
          "widgets_context": "{\"flags\":{},\"author_id\":\"68260d0d000000000e011cf8\",\"author_name\":\"霱謩\"}",
          "id": "697981c0000000000b00a645",
          "corner_tag_info": [
            {
              "icon": "",
              "text": "RAfO0lIAgKKifmJoqGKrOZReLn3B2E7n3oYC2WL0wOW9+kv/nrEZOjxK5EOk8ZSeGdUX0eLWM+XklV7flqzMCwn7V+15Rm8fkh",
              "text_en": "",
              "style": 0,
              "location": -1,
              "type": "ubt_sig_token"
            },
            {
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "01-28",
              "text_en": "01-28",
              "style": 0,
              "location": 5
            }
          ],
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "100"
          },
          "collected_count": 39,
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "collected": false,
          "liked_count": 100,
          "debug_info_str": "",
          "comments_count": 221,
          "tag_info": {
            "title": "",
            "type": ""
          },
          "images_list": [
            {
              "url": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831rsav9gpi2005q161k6ji77odt0emhg?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=ca74988017bf54b62d58a65882348770&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831rsav9gpi2005q161k6ji77odt0emhg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=ca74988017bf54b62d58a65882348770&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831rsav9gpi2005q161k6ji77odt0emhg",
              "need_load_original_image": false,
              "fileid": "notes_pre_post/1040g3k831rsav9gpi2005q161k6ji77odt0emhg",
              "height": 1741,
              "width": 1320
            },
            {
              "fileid": "notes_pre_post/1040g3k831rsav9gpi2105q161k6ji77orp2qio8",
              "height": 979,
              "width": 1112,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831rsav9gpi2105q161k6ji77orp2qio8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=2dc22ba24aad797405017d916e82bd32&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831rsav9gpi2105q161k6ji77orp2qio8",
              "need_load_original_image": false
            },
            {
              "fileid": "notes_pre_post/1040g3k831rsav9gpi20g5q161k6ji77o5i7874g",
              "height": 975,
              "width": 1320,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/notes_pre_post/1040g3k831rsav9gpi20g5q161k6ji77o5i7874g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=58895a659f7b744f9b09d21d19d1263e&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "notes_pre_post/1040g3k831rsav9gpi20g5q161k6ji77o5i7874g",
              "need_load_original_image": false
            }
          ],
          "timestamp": 1769570752,
          "result_from": "",
          "note_attributes": [],
          "extract_text_enabled": 0,
          "title": "预算1.5，能收到一台cb400f吗",
          "niced": false,
          "liked": false,
          "shared_count": 19,
          "nice_count": 0
        }
      },
      {
        "model_type": "note",
        "note": {
          "id": "677a295e0000000009014ca7",
          "geo_info": {
            "distance": ""
          },
          "advanced_widgets_groups": {
            "groups": [
              {
                "mode": 1,
                "fetch_types": [
                  "guos_test",
                  "note_next_step",
                  "second_jump_bar",
                  "cooperate_binds",
                  "note_collection",
                  "rec_next_infos",
                  "image_stickers",
                  "image_filters",
                  "product_review",
                  "related_search",
                  "cooperate_comment_component",
                  "image_goods_cards",
                  "ads_goods_cards",
                  "ads_comment_component",
                  "goods_card_v2",
                  "image_template",
                  "buyable_goods_card_v2",
                  "ads_engage_bar",
                  "challenge_card",
                  "cooperate_engage_bar",
                  "guide_post",
                  "pgy_comment_component",
                  "pgy_engage_bar",
                  "bar_below_image",
                  "aigc_collection",
                  "co_produce",
                  "widgets_ndb",
                  "next_note_guide",
                  "pgy_bbc_exp",
                  "async_group",
                  "super_activity",
                  "widgets_enhance",
                  "music_player",
                  "soundtrack_player"
                ]
              },
              {
                "mode": 0,
                "fetch_types": [
                  "guos_test",
                  "vote_stickers",
                  "bullet_comment_lead",
                  "note_search_box",
                  "interact_pk",
                  "interact_vote",
                  "guide_heuristic",
                  "share_to_msg",
                  "follow_guide",
                  "note_share_prompt_v1",
                  "sync_group",
                  "group_share",
                  "share_guide_bubble",
                  "widgets_share",
                  "guide_navigator"
                ]
              }
            ]
          },
          "collected": false,
          "user": {
            "show_red_official_verify_icon": false,
            "red_official_verified": false,
            "followed": false,
            "images": "https://sns-avatar-qc.xhscdn.com/avatar/1040g2jo31c7pr1hk100040snaaf5e669pojblag?imageView2/2/w/80/format/jpg",
            "red_official_verify_type": 0,
            "userid": "558e9e57538c253e39fa18c9",
            "track_duration": 0,
            "red_id": "603913870",
            "nickname": "Kobe Bryant"
          },
          "has_music": false,
          "comments_count": 2,
          "niced": false,
          "note_attributes": [],
          "extract_text_enabled": 0,
          "shared_count": 2,
          "nice_count": 0,
          "collected_count": 11,
          "cover_image_index": 0,
          "result_from": "",
          "widgets_context": "{\"flags\":{\"music\":true},\"author_id\":\"558e9e57538c253e39fa18c9\",\"author_name\":\"Kobe Bryant\"}",
          "update_time": 1736059270000,
          "liked_count": 37,
          "debug_info_str": "",
          "interaction_area": {
            "type": 1,
            "status": false,
            "text": "37"
          },
          "type": "normal",
          "timestamp": 1736059230,
          "title": "杜卡迪街霸V4 红绿灯",
          "images_list": [
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s0040snaaf5e669n25nloo",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s0040snaaf5e669n25nloo",
              "height": 1350,
              "width": 1080,
              "url": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s0040snaaf5e669n25nloo?imageView2/2/w/576/format/heif/q/58|imageMogr2/strip&redImage/frame/0/enhance/4&ap=5&sc=SRH_PRV&sign=dba4cce7d65fc548defff23a03b6450d&t=69d8fcb3&origin=1",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s0040snaaf5e669n25nloo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=dba4cce7d65fc548defff23a03b6450d&t=69d8fcb3&origin=1"
            },
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s0g40snaaf5e6692uvautg",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s0g40snaaf5e6692uvautg",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s0g40snaaf5e6692uvautg?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=16fcb5e95539ef584c1df45acc614dba&t=69d8fcb3&origin=1"
            },
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s1040snaaf5e6697ceanro",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s1040snaaf5e6697ceanro",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s1040snaaf5e6697ceanro?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e8a9d0d3502c802165de50494d63985d&t=69d8fcb3&origin=1"
            },
            {
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s1g40snaaf5e6698bbvsj8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=44a009a2251c772c5940ac4c2823ceaa&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s1g40snaaf5e6698bbvsj8",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s1g40snaaf5e6698bbvsj8",
              "height": 1350
            },
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s2040snaaf5e669vkuk6u0",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s2040snaaf5e669vkuk6u0",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s2040snaaf5e669vkuk6u0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=6c4155781247ca51183bb22b7e2b2623&t=69d8fcb3&origin=1"
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s2g40snaaf5e669edtlim0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=22c6f9d1dbd2adf557535ab544d163c6&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s2g40snaaf5e669edtlim0",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s2g40snaaf5e669edtlim0",
              "height": 1350,
              "width": 1080
            },
            {
              "height": 1349,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s3040snaaf5e669eib3s9g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=4b8b010287cac79465e8dcb0a6f18cd9&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s3040snaaf5e669eib3s9g",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s3040snaaf5e669eib3s9g"
            },
            {
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s3g40snaaf5e669599o8c8",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s3g40snaaf5e669599o8c8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=8774e95bbcd4003d2b862c829b7963b1&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s3g40snaaf5e669599o8c8"
            },
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s4040snaaf5e669c25bt7o",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s4040snaaf5e669c25bt7o",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s4040snaaf5e669c25bt7o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=866255a43a5e5b17495df7abbd1ec936&t=69d8fcb3&origin=1"
            },
            {
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s4g40snaaf5e669kcumk1g",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s4g40snaaf5e669kcumk1g",
              "height": 1350,
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s4g40snaaf5e669kcumk1g?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=cdbd859c7b77205984bfed7a1dbcf9c3&t=69d8fcb3&origin=1"
            },
            {
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s5040snaaf5e669tdeees8?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=f5a798092b8d160df139a07c4d71ef08&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s5040snaaf5e669tdeees8",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s5040snaaf5e669tdeees8",
              "height": 1350
            },
            {
              "width": 1080,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s5g40snaaf5e669nvgen6o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=38ce71ceec32ff873f2e94573aab00e0&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s5g40snaaf5e669nvgen6o",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s5g40snaaf5e669nvgen6o",
              "height": 1350
            },
            {
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s6040snaaf5e669q3kb0e0?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=b48ea7bed4c2cb4576ec47454b76b18c&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s6040snaaf5e669q3kb0e0",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s6040snaaf5e669q3kb0e0",
              "height": 1920,
              "width": 1440,
              "url": ""
            },
            {
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g00831c8vpc3s0s6g40snaaf5e669v1rfjto?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=e5587b0c59351414a7c30cd6502edded&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g00831c8vpc3s0s6g40snaaf5e669v1rfjto",
              "need_load_original_image": false,
              "fileid": "1040g00831c8vpc3s0s6g40snaaf5e669v1rfjto",
              "height": 1920,
              "width": 1440
            },
            {
              "need_load_original_image": false,
              "fileid": "1040g2sg31c8vpc4mh07040snaaf5e66999m1soo",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31c8vpc4mh07040snaaf5e66999m1soo?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=a69ce6fa77d2729b468972702b542e8b&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31c8vpc4mh07040snaaf5e66999m1soo"
            },
            {
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31c8vpc4mh07g40snaaf5e6692303mno?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=7c79357be69fc45d155883cf35ac22e4&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31c8vpc4mh07g40snaaf5e6692303mno",
              "need_load_original_image": false,
              "fileid": "1040g2sg31c8vpc4mh07g40snaaf5e6692303mno"
            },
            {
              "need_load_original_image": false,
              "fileid": "1040g2sg31c8vpc4mh08040snaaf5e669cu41h2o",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31c8vpc4mh08040snaaf5e669cu41h2o?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=5fe52cb3b88d092399a185a79a6ce12d&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31c8vpc4mh08040snaaf5e669cu41h2o"
            },
            {
              "need_load_original_image": false,
              "fileid": "1040g2sg31c8vpc4mh08g40snaaf5e669lqskmao",
              "height": 1920,
              "width": 1440,
              "url": "",
              "url_size_large": "https://sns-na-i8.xhscdn.com/1040g2sg31c8vpc4mh08g40snaaf5e669lqskmao?imageView2/2/w/1440/format/heif/q/45&redImage/frame/0&ap=5&sc=SRH_DTL&sign=66a0d4147528ce4e12d0cb7149e2752d&t=69d8fcb3&origin=1",
              "original": "",
              "trace_id": "1040g2sg31c8vpc4mh08g40snaaf5e669lqskmao"
            }
          ],
          "corner_tag_info": [
            {
              "location": -1,
              "type": "ubt_sig_token",
              "icon": "",
              "text": "RASbQqiwPEIwuPM8ZeFy20C0HU8mI6BSEQgTy0GRjNKvBUvTX6WB4zEMhDa4VFNia++MNULpTkhf0v5d0HZHiBjwelKZRFQJCK",
              "text_en": "",
              "style": 0
            },
            {
              "type": "publish_time",
              "icon": "http://picasso-static.xiaohongshu.com/fe-platform/e9b67af62f67d9d6cfac936f96ad10a85fdb868e.png",
              "text": "2025-01-05",
              "text_en": "2025-01-05",
              "style": 0,
              "location": 5
            }
          ],
          "xsec_token": "YBjINaRn84LOK5V-1QlODdej3vCItgMDK__1hJ7xKKlQg=",
          "liked": false,
          "desc": "诗意浓#摩托车  #每个男人都有一个机车梦  #趁年轻骑仿赛  #机车梦  #爱机车爱生活爱骑行  跨上蛮牛意气生，杜卡",
          "tag_info": {
            "title": "",
            "type": ""
          },
          "last_update_time": 0
        }
      }
    ],
    "query_debug_info": {
      "is_forbidden": false
    },
    "search_pull_down_opt_exp": 1,
    "service_status": "{\"filter\":\"not_required\",\"note\":\"success\",\"onebox\":\"not_required\",\"cost\":{\"all\":711,\"zone\":\"rcsh1\"}}",
    "query_type": 0,
    "query_intent": {
      "low_supply_intent": false,
      "goodsIntent": 3,
      "search_ask_intent": true
    },
    "request_dqa_instant": false,
    "ai_mode_enable": false
  },
  "message": null,
  "recordTime": "2026-04-10T21:35:58.418526694"
}
```