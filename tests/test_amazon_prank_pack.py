#!/usr/bin/env python3
"""
Verification tests for the Amazon prank pack.

These drive the real shipped HTML/content sources (not re-implemented copies)
and assert the acceptance criteria for titles, chapter themes, reviews, and
exported screenshot assets.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SCREENSHOTS = ROOT / "screenshots"
SHARE = ROOT / "share"


class TestShippedContent(unittest.TestCase):
    def test_product_metadata_exact_title_author(self):
        data = json.loads((CONTENT / "product.json").read_text(encoding="utf-8"))
        self.assertEqual(data["title"], "Road to 7.0 Pickleball")
        self.assertEqual(data["author"], "Quang Duong")
        self.assertGreaterEqual(data["rating"], 4.5)
        self.assertGreater(data["ratingCount"], 100)

    def test_chapter_excerpt_title_and_themes(self):
        text = (CONTENT / "chapter-excerpt.md").read_text(encoding="utf-8")
        self.assertIn("Bruce Lee's 1 inch punch", text)
        self.assertIn("Road to 7.0 Pickleball", text)
        # Theme (a) little backswing
        self.assertTrue(
            re.search(r"little backswing|minimal backswing|no backswing|short preparation", text, re.I)
        )
        # Theme (b) core engagement / power
        self.assertTrue(re.search(r"\bcore\b", text, re.I))
        self.assertTrue(re.search(r"power", text, re.I))
        # Theme (c) Bruce Lee + pros / related sports
        self.assertTrue(re.search(r"Bruce Lee|one-inch punch|1 inch punch", text, re.I))
        self.assertTrue(
            re.search(r"tennis|table tennis|squash|martial arts|PPA|MLP", text, re.I)
        )

    def test_reviews_pro_praise_and_stars(self):
        reviews = json.loads((CONTENT / "reviews.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(reviews), 4)
        for r in reviews:
            self.assertEqual(r["stars"], 5)
            self.assertIn("Verified Purchase", r["badge"])
            self.assertTrue(r["title"].strip())
            self.assertTrue(r["body"].strip())
            self.assertTrue(r.get("proNote"))
        # At least one review mentions the chapter / core idea
        joined = " ".join(r["body"] + " " + r["title"] for r in reviews)
        self.assertTrue(
            re.search(r"Bruce Lee|1 inch|backswing|core", joined, re.I),
            "reviews should praise the chapter philosophy",
        )


class TestShippedHtml(unittest.TestCase):
    def _html(self, name: str) -> str:
        path = ROOT / name
        self.assertTrue(path.exists(), f"missing {path}")
        return path.read_text(encoding="utf-8")

    def test_product_html_contains_exact_strings(self):
        html = self._html("product.html")
        self.assertIn("Road to 7.0 Pickleball", html)
        self.assertIn("Quang Duong", html)
        self.assertIn("Bruce Lee's 1 inch punch", html)
        self.assertIn("Customer reviews", html)
        self.assertIn("Add to Cart", html)
        self.assertIn("Look inside", html)
        self.assertIn("amazon", html.lower())

    def test_look_inside_chapter_html(self):
        html = self._html("look-inside.html")
        self.assertIn("Bruce Lee's 1 inch punch", html)
        self.assertIn("Road to 7.0 Pickleball", html)
        self.assertIn("Quang Duong", html)
        self.assertIn("little backswing", html.lower())
        self.assertIn("core", html.lower())
        self.assertIn("one-inch punch", html.lower())
        self.assertTrue(re.search(r"tennis|table tennis|squash", html, re.I))

    def test_reviews_html_pro_bylines(self):
        html = self._html("reviews.html")
        self.assertIn("Customer reviews", html)
        self.assertIn("4.9 out of 5", html)
        self.assertIn("Verified Purchase", html)
        # Pro-style bylines from reviews.json
        self.assertIn("Jordan Blake", html)
        self.assertIn("Marcus Hale", html)
        self.assertIn("Elena Voss", html)
        self.assertTrue(re.search(r"PPA|MLP|coach|DUPR", html))


class TestScreenshotAssets(unittest.TestCase):
    REQUIRED = [
        "01-product-page.png",
        "03-look-inside-chapter.png",
        "04-reviews.png",
        "05-cover-detail.png",
        "06-mobile-product.png",
        "08-cover-standalone.jpg",
    ]

    def test_at_least_three_distinct_screenshots(self):
        existing = [SCREENSHOTS / n for n in self.REQUIRED if (SCREENSHOTS / n).exists()]
        self.assertGreaterEqual(len(existing), 3)
        for p in existing:
            self.assertGreater(p.stat().st_size, 50_000, f"{p.name} too small")

    def test_cover_asset_exists(self):
        cover = ROOT / "assets" / "cover.jpg"
        self.assertTrue(cover.exists())
        self.assertGreater(cover.stat().st_size, 50_000)

    def test_share_pack_ready(self):
        if not SHARE.exists():
            self.skipTest("share/ not built yet")
        files = list(SHARE.glob("*"))
        self.assertGreaterEqual(len(files), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
