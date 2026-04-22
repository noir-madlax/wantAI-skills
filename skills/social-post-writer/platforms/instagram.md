# Instagram —— 撰写规则（模块化）

产出装配为 `SaveContent` 工具 `content` 入参中的四个模块：`meta` / `caption` / `hashtags` / `images`。

## `meta`

- `title`：**留空**（IG 没有独立标题字段）
- `language`：默认 `en`；若 KOL `audience_signals` 指明其他主要市场语言则按之
- `cta`：**只选一项**——Save / Share / Comment / DM / Link in bio；放 `caption.body` 尾、hashtags 之前
- `mentions`：品牌 `@handle`；合作帖按 Paid Partnership 规范
- `location`：可按 Brief 场景填

## `caption`

- `body`：**必填**，150–500 字为宜
  - **首 125 字 = Hook**：折叠前必须完整表达核心钩子
  - 短句分行，emoji 适度，每 1–2 行一段
  - 合作/返佣帖：正文内加 `#ad` 或 `#sponsored`，并按 Brief 合规项披露
  - CTA 一行，放正文末尾、hashtags 之前
- `variants`（可选）：若用户要 A/B，`body` 放稳版（叙事型 + 情绪收束 CTA），`variants` 放钩子版（首句悬念/反常识）
- `tone_notes`：一两句内部语气备忘

## `hashtags`

- `items`：5–15 个，**不带 `#` 前缀**；混合 **高热 / 中等 / 长尾**；品牌词 + 品类词 + 受众词各 ≥ 1
- `placement`：
  - `"first_comment"`（**推荐**，保持 caption 干净）
  - `"inline"`（放正文末尾也可）
- `max`：15

## `images`

IG 以视觉驱动；封面决定 feed 停留。

- `style`：一段 2–4 句话，覆盖 **色调 / 光线 / 构图美学 / 生活方式调性 / 拍摄质感（胶片 / 极简 / 高饱和 等）**；风格要与 KOL feed 的视觉一致性吻合
- `aspect_ratio`：默认 `"1:1"`（feed 方图）；竖图轮播用 `"4:5"`；Reels 封面用 `"9:16"`
- `items`：**单图或 3–10 张轮播**；顺序即轮播顺序
  - `role`：
    - 第 1 张必为 `"cover"`（停留钩子，构图要有视觉焦点，必要时有文字叠加）
    - 中间为 `"content"`（产品/场景/细节/使用过程/数据图）
    - 最后一张可为 `"closing"`（CTA 图 / 收束 / 合照，可省略）
  - `prompt`：可中英文；必须包含 **主体 + 场景 + 构图 + 光线 + 色调 + 风格**；若含文字叠加，写清文案与字体风格
  - `alt`：英文一句话（无障碍 + SEO）

## 自检清单

- `caption.body` 首 125 字是否已完整承载 hook？
- CTA 是否单一明确？
- `hashtags.placement` 是否和 caption 长度匹配（长 caption 建议 `first_comment`）？
- 合作披露是否已在 `caption.body` 内显式出现？
- `images.items[0].role == "cover"` 且风格与 KOL feed 一致？
