# 小红书 Xiaohongshu —— 品牌官方撰写规则（模块化）

产出装配为 `SaveContent` 工具 `content` 入参中的四个模块：`meta` / `caption` / `hashtags` / `images`。

## `meta`

- `title`：**必填**，≤ 20 字；含品牌视角 hook（数字 / 场景 / 问题 / 反转 / 新品信息），避免标题党
- `language`：默认 `zh-CN`
- `cta`：一句明确下一步动作（收藏 / 评论 / 了解产品 / 进主页查看）；不要把合规披露塞进这里
- `mentions`：品牌官方号或合作方 @handle（若 Brief 指定）
- `location`：可留空

## `caption`

- `body`：**必填**，400–900 字；2–3 行一段，口语但保持品牌可信度
  - 段落顺序建议：场景痛点 → 品牌观点 → 产品/服务卖点 → 使用场景 → CTA
  - 首段前 2 行就要有代入钩子
  - 严禁绝对化用语：最 / 第一 / 100% / 根治 / 立刻见效 等
  - 医疗、功效、化妆品：不承诺疗效，不使用未验证数据
- `variants`（可选）：若用户要 A/B，主版放 `body`，备选版放 `{label, body}`
- `tone_notes`：内部语气备忘，一两句即可

## `hashtags`

- `items`：3–10 个，**不带 `#` 前缀**，由渲染端拼接
  - 必含：品牌词 × 1 + 品类词 × 1 + 人群/场景词 × 1
  - 剩余名额给长尾词（节点词、场景词、问题词）
- `placement`：`"inline"`（正文末尾）
- `max`：10

## `images`

- `style`：整组图的视觉总纲，一段 2–4 句话，覆盖色调 / 光线 / 氛围 / 场景类型 / 拍摄感 / 文字叠加风格，并遵循品牌 `visual_guidelines`
- `aspect_ratio`：默认 `"3:4"`
- `items`：**4–8 张**，顺序即图序
  - 第 1 张必为 `"cover"`，带大字标题叠加，文案与 `meta.title` 对齐
  - 中间为 `"content"`，承载卖点、场景、细节、使用演示或对比
  - 最后一张可为 `"closing"`，承载 CTA 或总结
  - `prompt`：必须包含主体 + 场景 + 构图 + 光线 + 色调 + 风格；如有文字叠加需写清文案与字体风格
  - `alt`：一句中文描述

## 自检清单

- `meta.title` ≤ 20 字且不夸大？
- `caption.body` 是否只引用 Brief / 产品矩阵中的事实？
- 是否避开品牌护栏 forbidden_terms？
- `hashtags.items` 是否覆盖品牌 × 品类 × 人群/场景？
- `images.items[0].role == "cover"` 且 prompt 写清封面字？
