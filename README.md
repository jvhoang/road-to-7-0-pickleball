# Road to 7.0 Pickleball

**by Quang Duong**

[**Open the free Look Inside sample →**](https://jvhoang.github.io/road-to-7-0-pickleball/)

Featured chapter: **Bruce Lee's 1 inch punch** — the core habit of minimal backswing and core-driven power.

## Pages

| Page | Link |
|------|------|
| Look Inside (chapter sample) | [index.html](index.html) / [look-inside.html](look-inside.html) |
| Amazon-style product page | [product.html](product.html) |
| Customer reviews | [reviews.html](reviews.html) |
| Cover detail | [cover-detail.html](cover-detail.html) |
| Mobile product view | [mobile-product.html](mobile-product.html) |

## Share images

Ready-to-send screenshots are in [`share/`](share/).

## Source

- Chapter copy: `content/chapter-excerpt.md`
- Product metadata: `content/product.json`
- Reviews: `content/reviews.json`
- Cover art: `assets/cover.jpg`

```bash
# Local preview
open index.html

# Regenerate screenshots (Playwright Chromium)
python3 scripts/capture_playwright.py

# Tests
python3 -m unittest tests/test_amazon_prank_pack.py -v
```
