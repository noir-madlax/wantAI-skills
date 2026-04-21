---
name: social-post-writer
description: 根据营销 Brief 与 KOL 人设生成小红书 / Instagram / Facebook 的可发布帖子文案。当用户需要写社媒帖子、种草文案、KOL 投放内容、多平台改写、品牌/产品推广帖子时触发。
arguments:
  - kol_id
  - brief_id
  - platforms
preload:
  - name: KOL_PERSONA_CORE
    loader: kol_persona_core
    args: { kol_id: "$kol_id" }
  - name: BRIEF_FULL
    loader: brief_full
    args: { brief_id: "$brief_id" }
  - name: PLATFORM_RULES
    loader: read_skill_files
    args:
      path_template: "platforms/{item}.md"
      items: "$platforms"
      default_items: "xiaohongshu,instagram,facebook"
      separator: "\n\n---\n\n"
---

# 社媒帖子撰写(小红书 / IG / FB)

根据 Brief 与 KOL 人设,为指定平台生成可直接发布的帖子文案。

## Context(执行器已注入)

以下两块由后端在 Skill 激活时从数据库取出并注入,视为**权威输入**;不要质疑其准确性,也不要要求用户重新提供这些字段。若某块明显为空或字段缺失,按"工作流程-步骤 1"处理。

### KOL 人设
{{KOL_PERSONA_CORE}}

### Brief
{{BRIEF_FULL}}

### 本次生成平台
`$platforms` —— 取值为 `xiaohongshu` / `instagram` / `facebook` 的子集(逗号分隔);未指定时默认三个平台全出。

## 通用规则(所有平台)

1. 贴合 KOL 的 `positioning` / `tone_tags` / `voice`,**第一人称**写作;避免"官方口径"
2. 只使用 Brief 明示的卖点与事实;不承诺未列出的功效 / 数据
3. 严格遵守 KOL 的 `no_go_list` 与 Brief 的合规要求;涉及医疗、功效、绝对化用词自行合规化
4. 不贬低竞品;广告 / 合作关系按平台规定披露(如 IG `#ad`、小红书蒲公英报备提示)
5. 每个平台默认给 **2 版** 供选择(版本 A 偏稳、版本 B 偏钩子/反转)
6. 输出必标注字符数;同一批内容不要跨平台照搬,按平台规则改写

## 平台规则（本次目标平台）

以下内容由执行器根据 `$platforms` 自动注入对应 `platforms/*.md`；未列出的平台不会出现在这里。每个平台块包含：结构 / 话题 / 合规 / 版本 A-B 差异 / 输出字段模板。

{{PLATFORM_RULES}}

## 工作流程

1. **核对 Context**：确认 `KOL_PERSONA_CORE` / `BRIEF_FULL` / `PLATFORM_RULES` 三块均已注入且关键字段齐全（如 Brief 的 `core_message` / 卖点，KOL 的 `tone_tags` / `voice`）。若明显缺失，**列出缺失项向用户确认**，不要编造；用户明示"按你理解补"后，再生成并在"备注"中标注【假设】
2. **抽取要点**：从 Brief 萃取 3 条最能撑起核心卖点的支撑点；从 KOL `voice` / `content_preference` 抽取 2–3 个语言特征（口头禅 / 句式 / 惯用表达）
3. **按平台生成**：对 `$platforms` 的每个平台，依据"平台规则"段中该平台的"输出字段"模板各给 2 版（A 稳 / B 钩子）
4. **自检**：每版对照 KOL `no_go_list`、Brief 合规项与该平台规则做一次回扫，违规直接改写

## 收尾

所有平台输出完成后，附**一段** 3–5 行的 `改写说明`：为什么这样切入、版本 A / B 差异、哪些点基于【假设】。
