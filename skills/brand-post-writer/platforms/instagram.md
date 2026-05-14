# Instagram —— Brand-Owned Draft Format

This platform outputs a **Markdown draft directly in the conversation**. Do NOT call `SaveContent`.

## Draft Structure

Return the draft in the following format, using the exact section headers below:

---

### Caption

Write the full post caption here.

- **Length**: 120–450 words
- **Opening**: The first 125 characters MUST carry the hook — this is the "above the fold" preview users see before tapping "more"
- **Voice**: Brand-owned, authoritative yet approachable; NOT influencer diary or personal experience
- **Structure**: Short paragraphs separated by line breaks; use emoji sparingly and only if consistent with brand tone
- **CTA**: Place near the end — Save / Share / Comment / DM / Link in bio
- **Disclosures**: Include required disclosures from Brief or guardrails where applicable
- **Language**: Default English; follow Brief if it specifies another market language

### Hashtags

List hashtags on a single line, each prefixed with `#`.

- **Count**: 5–15
- **Must include**: at least 1 brand term + 1 category term + 1 audience/scenario term
- **Placement note**: Recommend first comment placement; inline is acceptable for short captions

### 配图建议 / Visual Suggestions

Describe the visual direction and each image:

**整体风格 / Overall Style**: 2–4 sentences covering color palette, lighting, composition, lifestyle mood, production quality, and how it connects to brand visual guidelines.

**推荐比例 / Aspect Ratio**: `1:1` for feed, `4:5` for carousel, `9:16` for Reels/Story (choose based on Brief context)

**图片列表 / Image List**: Describe each image (single image or 3–10 carousel):

1. **封面 / Cover**: [Subject, scene, composition, lighting, color, style. Specify overlay text if any.]
2. **内容图 / Content**: [Product detail, use case, scene, or proof point.]
3. **收尾图 / Closing** (optional): [CTA card, summary, or brand sign-off.]

Each image description should include: subject, scene, composition, lighting, color palette, and style — specific enough for an image generation tool.

---

## Checklist (internal, do not output)

- Does the first 125 characters contain the hook?
- Is the voice clearly brand-owned rather than KOL personal voice?
- Are product claims grounded in `BRAND_PRODUCTS` or the Brief?
- Are guardrails and forbidden terms respected?
- Does the visual direction follow `BRAND_CORE.visual_guidelines`?
