#!/usr/bin/env python3
"""Capture Amazon mock screenshots with Playwright."""

from __future__ import annotations

import http.server
import socketserver
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"

SHOTS = [
    {
        "name": "01-product-page.png",
        "path": "/product.html",
        "width": 1440,
        "height": 1100,
        "full_page": False,
    },
    {
        "name": "02-product-page-full.png",
        "path": "/product.html",
        "width": 1440,
        "height": 900,
        "full_page": True,
    },
    {
        "name": "03-look-inside-chapter.png",
        "path": "/look-inside.html",
        "width": 1200,
        "height": 900,
        "full_page": True,
    },
    {
        "name": "04-reviews.png",
        "path": "/reviews.html",
        "width": 1440,
        "height": 900,
        "full_page": True,
    },
    {
        "name": "05-cover-detail.png",
        "path": "/cover-detail.html",
        "width": 1440,
        "height": 900,
        "full_page": False,
    },
    {
        "name": "06-mobile-product.png",
        "path": "/mobile-product.html",
        "width": 390,
        "height": 844,
        "full_page": True,
    },
    {
        "name": "07-cover-hero.png",
        "path": "/cover-detail.html",
        "width": 1000,
        "height": 1100,
        "full_page": False,
    },
]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):  # noqa: A003
        pass


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    time.sleep(0.2)
    base = f"http://127.0.0.1:{port}"
    print(f"Serving on {base}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for shot in SHOTS:
            page = browser.new_page(
                viewport={"width": shot["width"], "height": shot["height"]},
                device_scale_factor=2,
            )
            url = base + shot["path"]
            page.goto(url, wait_until="networkidle")
            # small settle for fonts/images
            page.wait_for_timeout(400)
            out = OUT / shot["name"]
            page.screenshot(path=str(out), full_page=shot["full_page"])
            page.close()
            size = out.stat().st_size
            print(f"OK {shot['name']} ({size} bytes)")
        browser.close()

    httpd.shutdown()
    print(f"All screenshots written to {OUT}")


if __name__ == "__main__":
    main()
