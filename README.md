# Road to 7.0 Pickleball — Amazon Prank Pack

Fake-but-glance-legit **Amazon.com** screenshots for the book:

- **Title:** Road to 7.0 Pickleball  
- **Author:** Quang Duong  
- **Featured chapter:** Bruce Lee's 1 inch punch  

Built for a doubles-partner / brother prank. Nothing is published on real Amazon.

## Send these (ready to text)

Use the files in **`share/`** (also under `screenshots/`):

| File | What it is |
|------|------------|
| `01-product-page.png` | Full Amazon product page (cover, price, buy box, ratings) |
| `03-look-inside-chapter.png` | Look Inside sample — chapter **Bruce Lee's 1 inch punch** |
| `04-reviews.png` | Highly praising pro-style customer reviews |
| `05-cover-detail.png` | Cover-focused Amazon product image view |
| `06-mobile-product.png` | Phone-width Amazon listing (great for iMessage) |
| `08-cover-standalone.jpg` | Clean book cover only |

Suggested send order: mobile product → look inside chapter → reviews → cover detail.

## Source / regenerate

```bash
# HTML mocks
open product.html          # desktop product + reviews
open look-inside.html      # chapter excerpt
open reviews.html          # full reviews
open cover-detail.html     # cover zoom
open mobile-product.html   # phone layout

# Re-capture PNGs (needs Playwright Chromium)
python3 scripts/capture_playwright.py

# Verify
python3 -m unittest tests/test_amazon_prank_pack.py -v
```

## Content notes

- Chapter explains **minimal backswing + core power**, ties it to Bruce Lee’s one-inch punch, and references pros + tennis / table tennis / squash / martial arts.
- Reviews use **fictional pro-sounding names** (not real athletes) with PPA/MLP/coach tags so the prank lands without impersonating specific living pros.
- Cover art: `assets/cover.jpg`
