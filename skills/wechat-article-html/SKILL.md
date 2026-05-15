---
name: wechat-article-html
description: Generate WeChat Official Account article HTML files that can be opened locally and copied as rich text into the WeChat editor. Use when the user asks to create, modify, package, or publish a `wechat-editor-fragment.html` style HTML article, needs SVG/GIF/image longform layouts for WeChat, needs a “复制使用” button, or needs HTML that copies rendered rich text instead of source code.
---

# WeChat Article HTML

## Goal

Create local HTML files for WeChat Official Account publishing. The file should render the article preview in a browser and include a local-only “复制使用” helper that copies the article wrapper as rich text (`text/html`) into the clipboard.

## Core Rules

- Require user-provided assets for real images, GIFs, logos, and product visuals. Do not invent final campaign assets unless the user explicitly asks for placeholders.
- Let the user specify visual style. Do not enforce a fixed aesthetic.
- Keep copied article content inside one wrapper, usually `<section data-goodgame-wechat-article>...</section>`.
- Keep the copy helper UI and `<script>` outside that wrapper so they are not copied into WeChat.
- Use inline styles for the article content. Avoid external CSS, frameworks, custom fonts, and JavaScript inside the copied article.
- Prefer WeChat-friendly tags: `section`, `p`, `span`, `img`, and inline `svg` with simple SMIL animation when needed.
- For GIFs, use `<img>` with both `src` and `data-src` when a WeChat CDN URL is available.
- For local assets, use relative paths for local preview, then remind the user that final publishing usually requires uploading images/GIFs to WeChat and replacing `src`/`data-src` with WeChat CDN URLs.
- For horizontal swipe rows, use pure CSS such as `overflow-x:auto`, `white-space:nowrap`, and optional `scroll-snap-type:x mandatory`; do not add swipe JavaScript.

## Standard File Shape

Generate one self-copying HTML file unless the user requests a different package:

```html
<!-- Local helper: open this file in a browser, click copy, paste into WeChat editor. -->
<div data-copy-helper>
  <a href="javascript:;" id="copy-editor-html">复制使用</a>
  <div data-copy-status style="display:none;">已复制富文本</div>
</div>

<section data-goodgame-wechat-article>
  <!-- WeChat article content goes here. Inline styles only. -->
</section>

<script>
  /* Copy helper goes here. */
</script>
```

## Required Copy Helper Logic

Use this 135-editor-style copy approach. It writes rendered HTML into the clipboard as `text/html`, writes readable fallback text as `text/plain`, then falls back to selecting the article node and calling `execCommand('copy')`.

```html
<script>
  (function () {
    var article = document.querySelector('[data-goodgame-wechat-article]');
    var copyButton = document.querySelector('#copy-editor-html');
    var status = document.querySelector('[data-copy-status]');
    var resetTimer = null;

    function setHelperText(text, isError) {
      if (!status) return;
      status.textContent = text;
      status.style.display = 'block';
      status.style.background = isError ? 'rgba(190,56,46,.94)' : 'rgba(24,33,42,.92)';
      clearTimeout(resetTimer);
      resetTimer = setTimeout(function () {
        status.style.display = 'none';
        status.textContent = '已复制富文本';
        status.style.background = 'rgba(24,33,42,.92)';
      }, 2600);
    }

    function copyByClipboardEvent(html, plainText) {
      var didSetClipboard = false;

      function handleCopy(event) {
        if (!event.clipboardData) return;
        event.clipboardData.setData('text/html', html);
        event.clipboardData.setData('text/plain', plainText);
        event.preventDefault();
        didSetClipboard = true;
      }

      document.addEventListener('copy', handleCopy);
      try {
        if (document.queryCommandSupported && !document.queryCommandSupported('copy')) {
          return false;
        }
        var ok = document.execCommand('copy');
        return didSetClipboard || ok;
      } finally {
        document.removeEventListener('copy', handleCopy);
      }
    }

    function fallbackCopyBySelection() {
      var range = document.createRange();
      var selection = window.getSelection();
      range.selectNode(article);
      selection.removeAllRanges();
      selection.addRange(range);
      var ok = document.execCommand('copy');
      selection.removeAllRanges();
      return ok;
    }

    function copyRichText() {
      if (!article) {
        setHelperText('没有找到可复制的文章内容。', true);
        return;
      }

      var html = article.outerHTML;
      var plainText = article.innerText || '公众号富文本已复制。请在微信编辑器正文区粘贴。';

      try {
        if (copyByClipboardEvent(html, plainText)) {
          setHelperText('已复制富文本。现在去微信编辑器正文区粘贴即可。', false);
          return;
        }
      } catch (error) {
        // Some browsers block scripted clipboard writes; use selection copy below.
      }

      try {
        if (fallbackCopyBySelection()) {
          setHelperText('已通过选区方式复制富文本。现在去微信编辑器正文区粘贴即可。', false);
        } else {
          setHelperText('复制失败：浏览器拦截了剪贴板权限。请换 Chrome/Safari 打开后再点一次。', true);
        }
      } catch (error) {
        setHelperText('复制失败：浏览器拦截了剪贴板权限。请换 Chrome/Safari 打开后再点一次。', true);
      }
    }

    if (copyButton) {
      copyButton.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        copyRichText();
      });
    }
  })();
</script>
```

## Article Patterns

### Image Or GIF Block

```html
<section style="margin:0;padding:0;line-height:0;font-size:0;">
  <img src="ASSET_URL" data-src="ASSET_URL" alt="" style="display:block;margin:0 auto;width:100%;height:auto;line-height:0;vertical-align:top;">
</section>
```

### Horizontal Snap Swipe Row

```html
<section style="margin:0;padding:0 0 0 34px;max-width:100%;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;white-space:nowrap;line-height:0;font-size:0;">
  <section style="display:inline-block;margin:0 14px 0 0;padding:0;width:78%;max-width:620px;vertical-align:top;line-height:0;font-size:0;scroll-snap-align:start;scroll-snap-stop:always;">
    <img src="ASSET_URL" data-src="ASSET_URL" alt="" style="display:block;width:100%;height:auto;border-radius:10px;line-height:0;vertical-align:top;">
  </section>
</section>
```

### Inline SVG Animation

Use inline SVG for decorative or layout-safe animation that does not depend on external scripts:

```html
<svg xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;height:auto;line-height:0;" viewBox="0 0 1080 600">
  <rect width="1080" height="600" fill="#18212a"></rect>
  <circle cx="540" cy="300" r="72" fill="#ffffff" opacity=".8">
    <animate attributeName="opacity" values=".35;1;.35" dur="1.6s" repeatCount="indefinite"></animate>
  </circle>
</svg>
```

## Workflow

1. Confirm or infer the target output path. Default to a package folder and `wechat-editor-fragment.html` when the user is working on a WeChat publishing package.
2. Collect the user-provided asset paths or URLs. If required assets are missing, ask for them or use clearly labeled placeholders only when the user allows it.
3. Build the article inside the wrapper with inline styles and WeChat-friendly HTML.
4. Add the local copy helper outside the wrapper using the required copy helper logic.
5. Validate the generated file:
   - Check the file contains exactly one article wrapper.
   - Parse all `<script>` blocks with `new Function(scriptText)` or equivalent.
   - Check local asset paths exist when they are referenced.
   - Check the copy helper copies `article.outerHTML`, not the full page.
6. Tell the user how to use it: open the file locally, click “复制使用”, paste into the WeChat editor body, then preview on phone.

## Publishing Notes

- Pasting raw HTML into the WeChat editor usually shows code. The user should use the local “复制使用” button or a third-party editor that supports rich HTML import.
- Local images may not survive WeChat paste. For final publishing, upload images/GIFs to WeChat first, then replace local image paths with WeChat CDN URLs.
- WeChat may strip unsupported tags or CSS. After pasting, always use WeChat preview, especially for SVG animation, GIF playback, and horizontal swipe rows.
