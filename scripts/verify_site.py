import os
import re
import urllib.request
import threading
import http.server
import socketserver
import time
from pathlib import Path
from html.parser import HTMLParser

ROOT_DIR = Path(__file__).resolve().parent.parent

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.anchors = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if "id" in attr_dict:
            self.ids.append(attr_dict["id"])
        if tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])
        if tag == "img" and "src" in attr_dict:
            self.images.append(attr_dict["src"])

def verify_site():
    print("=== STARTING PORTFOLIO VERIFICATION ===")
    errors = []
    
    html_files = [
        "index.html",
        "fuse-blast.html",
        "upulse.html",
        "unreleased-rd.html",
        "mtg-counter.html",
        "can-transceiver.html",
        "robotics.html",
        "toolkit.html",
        "onewheel.html"
    ]
    
    # 1. Verify existence of HTML files
    for h in html_files:
        p = ROOT_DIR / h
        if not p.exists():
            errors.append(f"Missing HTML file: {h}")
        else:
            print(f"[OK] HTML File Present: {h} ({p.stat().st_size} bytes)")

    # 2. Parse links, images, and anchors in each HTML file
    for h in html_files:
        p = ROOT_DIR / h
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8")
        parser = LinkExtractor()
        parser.feed(content)

        # Check images
        for img_src in parser.images:
            if not img_src or img_src.startswith("http"):
                continue
            img_path = ROOT_DIR / img_src
            if not img_path.exists():
                errors.append(f"In {h}: Broken image link '{img_src}'")
            else:
                if not img_src.endswith(".webp") and not img_src.endswith(".svg"):
                    errors.append(f"In {h}: Image is not WebP: '{img_src}'")

        # Check internal links
        for href in parser.links:
            if href.startswith("http") or href.startswith("mailto:"):
                continue
            if href.startswith("#"):
                # Anchor link in same file
                target_id = href[1:]
                if target_id not in parser.ids:
                    errors.append(f"In {h}: Broken anchor '{href}' (ID #{target_id} not found in file)")
            elif "#" in href:
                target_file, target_id = href.split("#", 1)
                t_path = ROOT_DIR / target_file
                if not t_path.exists():
                    errors.append(f"In {h}: Broken target file '{target_file}' in href '{href}'")
                else:
                    t_content = t_path.read_text(encoding="utf-8")
                    t_parser = LinkExtractor()
                    t_parser.feed(t_content)
                    if target_id not in t_parser.ids:
                        errors.append(f"In {h}: Broken anchor ID '{target_id}' in '{href}'")
            else:
                target_path = ROOT_DIR / href
                if not target_path.exists():
                    errors.append(f"In {h}: Broken link '{href}'")

    # 3. Check 3D model
    glb_path = ROOT_DIR / "assets" / "models" / "mtg-counter.glb"
    if not glb_path.exists():
        errors.append("3D GLB model missing: assets/models/mtg-counter.glb")
    else:
        print(f"[OK] 3D Model Present: assets/models/mtg-counter.glb ({glb_path.stat().st_size / 1024:.1f} KB)")

    # 4. Check CSS & JS
    css_path = ROOT_DIR / "assets" / "css" / "style.css"
    js_path = ROOT_DIR / "assets" / "js" / "main.js"
    if not css_path.exists():
        errors.append("CSS file missing: assets/css/style.css")
    else:
        print(f"[OK] Stylesheet Present: assets/css/style.css ({css_path.stat().st_size} bytes)")
    if not js_path.exists():
        errors.append("JS file missing: assets/js/main.js")
    else:
        print(f"[OK] Script Present: assets/js/main.js ({js_path.stat().st_size} bytes)")

    # 5. Check HTTP Server Responses
    PORT = 8089
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT_DIR), **kwargs)
        def log_message(self, format, *args):
            pass

    httpd = socketserver.TCPServer(("", PORT), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    test_urls = [
        f"http://localhost:{PORT}/index.html",
        f"http://localhost:{PORT}/fuse-blast.html",
        f"http://localhost:{PORT}/upulse.html",
        f"http://localhost:{PORT}/unreleased-rd.html",
        f"http://localhost:{PORT}/mtg-counter.html",
        f"http://localhost:{PORT}/can-transceiver.html",
        f"http://localhost:{PORT}/robotics.html",
        f"http://localhost:{PORT}/toolkit.html",
        f"http://localhost:{PORT}/assets/css/style.css",
        f"http://localhost:{PORT}/assets/js/main.js",
        f"http://localhost:{PORT}/assets/models/mtg-counter.glb",
        f"http://localhost:{PORT}/assets/models/onewheel.glb",
        f"http://localhost:{PORT}/assets/img/fuse-blast-hero.webp",
        f"http://localhost:{PORT}/assets/img/upulse-hero.webp",
        f"http://localhost:{PORT}/assets/img/mtg-counter-loop.webp",
        f"http://localhost:{PORT}/assets/img/mtg-explode.webp",
        f"http://localhost:{PORT}/assets/img/mtg-lifecounter-hero.webp",
        f"http://localhost:{PORT}/assets/img/can-board.webp",
        f"http://localhost:{PORT}/assets/img/can-circuit.webp",
        f"http://localhost:{PORT}/assets/img/can-schematic.webp",
        f"http://localhost:{PORT}/assets/img/robot-2025.webp",
        f"http://localhost:{PORT}/assets/img/onewheel.webp",
        f"http://localhost:{PORT}/assets/docs/CanHack_Schematic.pdf",
    ]

    for url in test_urls:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req) as resp:
                if resp.status != 200:
                    errors.append(f"HTTP GET {url} failed with status {resp.status}")
                else:
                    print(f"[OK] HTTP 200: {url.split('/')[-1]}")
        except Exception as ex:
            errors.append(f"HTTP GET {url} threw exception: {ex}")

    httpd.shutdown()

    print("\n=== VERIFICATION SUMMARY ===")
    if not errors:
        print("SUCCESS: 0 errors found! All pages, anchors, images, docs, scripts, and HTTP endpoints verified.")
        return 0
    else:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(f" - {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(verify_site())
