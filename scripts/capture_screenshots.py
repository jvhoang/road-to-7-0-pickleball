#!/usr/bin/env python3
"""Capture Amazon mock screenshots via Chrome headless + local HTTP server."""

from __future__ import annotations

import http.server
import os
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"
CHROME = os.environ.get(
    "CHROME_PATH",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)

SHOTS = [
    {
        "name": "01-product-page.png",
        "path": "/product.html",
        "width": 1440,
        "height": 1100,
    },
    {
        "name": "02-product-page-full.png",
        "path": "/product.html",
        "width": 1440,
        "height": 2800,
    },
    {
        "name": "03-look-inside-chapter.png",
        "path": "/look-inside.html",
        "width": 1200,
        "height": 4200,
    },
    {
        "name": "04-reviews.png",
        "path": "/reviews.html",
        "width": 1440,
        "height": 3400,
    },
    {
        "name": "05-cover-detail.png",
        "path": "/cover-detail.html",
        "width": 1440,
        "height": 900,
    },
    {
        "name": "06-mobile-product.png",
        "path": "/mobile-product.html",
        "width": 390,
        "height": 1800,
    },
    {
        "name": "07-cover-only.png",
        "path": "/cover-detail.html",
        "width": 900,
        "height": 1100,
    },
]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):  # noqa: A003
        pass


def start_server():
    # Bind ephemeral port
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def capture(port: int, shot: dict) -> None:
    out_path = OUT / shot["name"]
    url = f"http://127.0.0.1:{port}{shot['path']}"
    args = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--force-device-scale-factor=2",
        f"--window-size={shot['width']},{shot['height']}",
        f"--screenshot={out_path}",
        url,
    ]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(
            f"Chrome failed for {shot['name']}: {result.stderr[:500]}"
        )
    if not out_path.exists() or out_path.stat().st_size < 1000:
        raise RuntimeError(f"Screenshot missing or too small: {out_path}")
    print(f"OK {shot['name']} ({out_path.stat().st_size} bytes)")


def main() -> int:
    if not Path(CHROME).exists():
        print(f"Chrome not found: {CHROME}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    httpd, port = start_server()
    print(f"Serving {ROOT} on http://127.0.0.1:{port}")
    time.sleep(0.3)
    try:
        for shot in SHOTS:
            capture(port, shot)
    finally:
        httpd.shutdown()
    print(f"All screenshots written to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
