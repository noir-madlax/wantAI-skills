# Facebook —— Brand-Owned Draft Format

This platform outputs a **Markdown draft directly in the conversation**. Do NOT call `SaveContent`.

## Draft Structure

Return the draft in the following format, using the exact section headers below:

---

### Caption

Write the full post caption here. Choose one format based on the Brief:

**Short Engagement Post** (80–180 words):
- Hook question or bold statement as the opening sentence
- 1–2 short paragraphs delivering value or story
- End with a CTA question that encourages comments

**Story / Long-Form Post** (250–600 words):
- Clear narrative arc: hook → context → insight → product tie-in → CTA
- Short paragraphs with blank lines for readability
- The opening sentence must be a genuine hook, not a generic intro

**General rules**:
- Brand-owned voice: credible, useful, and conversational
- Put external links on their own line at the end if the Brief provides one
- Language: default English; follow Brief if it specifies another market

### Hashtags

List hashtags on a single line, each prefixed with `#`.

- **Count**: 1–3 only — Facebook penalizes hashtag overuse
- **Placement**: Inline at the end of the caption

### 配图建议 / Visual Suggestions

Describe the visual direction and each image:

**整体风格 / Overall Style**: 2–4 sentences covering color, lighting, realness vs. design polish, typography, and how it connects to brand visual guidelines.

**推荐比例 / Aspect Ratio**: `1:1` for standard feed, `1.91:1` for horizontal link-preview style

**图片列表 / Image List**: 1–3 images:

1. **封面 / Cover**: [Subject, scene, composition, lighting, color palette, style. Specify text-card copy if any.]
2. **内容图 / Content** (optional): [Scene, product detail, or comparison shot.]
3. **收尾图 / Closing** (optional): [CTA card or brand sign-off.]

Each image description should include: subject, scene, composition, lighting, color palette, and style — specific enough for an image generation tool.

---

## Checklist (internal, do not output)

- Is the first sentence a real hook?
- Is `CTA` concrete and comment-friendly?
- Are product claims grounded in `BRAND_PRODUCTS` or the Brief?
- Are hashtags capped at 3?
- Are guardrails and forbidden terms respected?
