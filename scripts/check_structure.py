"""Structural rules from docs/superpowers/specs/2026-10-14-portfolio-restructure-design.md.

Prints one [FAIL] line per violation and exits 1, or prints
ALL STRUCTURE CHECKS PASSED and exits 0.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "index.html", "fuse-blast.html", "upulse.html", "unreleased-rd.html",
    "mtg-counter.html", "onewheel.html", "can-transceiver.html",
    "robotics.html", "toolkit.html",
]

CARDS = [
    ("01", "Formlabs", "Fuse Blast"),
    ("02", "Formulatrix", "uPulse"),
    ("03", "Formlabs", "Next-Generation Printer"),
    ("04", "Personal", "MTG Life Counter"),
    ("05", "Personal", "DIY Onewheel"),
    ("06", "FIRST Robotics", "CAN Bus Fault Isolator"),
    ("07", "FIRST Robotics", "FIRST Robotics"),
    ("08", "Personal", "Raspberry Pi Home Server"),
]

NAV = ["Professional Work", "Robotics & Builds", "Side Projects", "Contact"]
SECTION_IDS = ["professional-work", "robotics-builds", "side-projects", "skills", "contact"]
CHAIN = ["fuse-blast.html", "upulse.html", "unreleased-rd.html", "mtg-counter.html",
         "onewheel.html", "can-transceiver.html", "robotics.html", "toolkit.html", "index.html"]
OLD_ANCHORS = ["#mass-production", "#mechatronics", "#leadership", "#toolkit-homelab"]
EMAIL = "mailto:c.johnson.career@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/ChrisJohnson4909"
BUTTON = "View project →"

failures = []


def fail(rule, msg):
    failures.append(f"[FAIL] {rule}: {msg}")


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def text(fragment):
    """Visible text of an HTML fragment, whitespace-collapsed."""
    t = re.sub(r"<[^>]+>", " ", fragment)
    t = t.replace("&amp;", "&").replace("&rarr;", "→")
    return re.sub(r"\s+", " ", t).strip()


def no_resume_links():
    for p in PAGES:
        s = read(p)
        for bad in ("ChrisJohnsonResume", "Download Resume", "Download PDF Resume"):
            if bad in s:
                fail("no_resume_links", f"{p} contains '{bad}'")


def no_footer_boilerplate():
    for p in PAGES:
        s = read(p)
        for bad in ("Built for GitHub Pages", "Optimized WebP Media", "All rights reserved"):
            if bad in s:
                fail("no_footer_boilerplate", f"{p} contains '{bad}'")


def homepage_nav():
    s = read("index.html")
    m = re.search(r'<ul class="nav-links" id="nav-links">(.*?)</ul>', s, re.S)
    if not m:
        fail("homepage_nav", "nav list not found")
        return
    labels = [text(a) for a in re.findall(r"<a[^>]*>(.*?)</a>", m.group(1), re.S)]
    header = re.search(r'<header class="site-header">(.*?)</header>', s, re.S).group(1)
    actions = re.search(r'<div class="nav-actions">(.*?)</div>', header, re.S)
    extra = [text(a) for a in re.findall(r"<a[^>]*>(.*?)</a>", actions.group(1), re.S)] if actions else []
    got = labels + extra
    if got != NAV:
        fail("homepage_nav", f"nav labels {got} != {NAV}")


def homepage_sections():
    s = read("index.html")
    ids = re.findall(r'<section[^>]*\sid="([^"]+)"', s)
    ordered = [i for i in ids if i in SECTION_IDS]
    if ordered != SECTION_IDS:
        fail("homepage_sections", f"section ids {ordered} != {SECTION_IDS}")
    for h in re.findall(r'<h2 class="category-heading">(.*?)</h2>', s, re.S):
        t = text(h)
        if "//" in t or re.match(r"^\d", t):
            fail("homepage_sections", f"heading has number or // : '{t}'")


def homepage_cards():
    s = read("index.html")
    cards = re.findall(r'<article class="project-card">(.*?)</article>', s, re.S)
    if len(cards) != len(CARDS):
        fail("homepage_cards", f"{len(cards)} cards, expected {len(CARDS)}")
    for card, (num, tag, title) in zip(cards, CARDS):
        n = re.search(r'<span class="project-number">(.*?)</span>', card, re.S)
        g = re.search(r'<span class="project-tag">(.*?)</span>', card, re.S)
        t = re.search(r'<h3 class="project-title">(.*?)</h3>', card, re.S)
        got = (text(n.group(1)) if n else None, text(g.group(1)) if g else None, text(t.group(1)) if t else None)
        if got != (num, tag, title):
            fail("homepage_cards", f"card {got} != {(num, tag, title)}")
        buttons = [text(b) for b in re.findall(r'<a [^>]*class="btn[^"]*"[^>]*>(.*?)</a>', card, re.S)]
        if buttons != [BUTTON]:
            fail("homepage_cards", f"card {num} buttons {buttons} != ['{BUTTON}']")
    for bad in ("skill-pill", "media-badge"):
        count = sum(c.count(bad) for c in cards)
        if count:
            fail("homepage_cards", f"{count} '{bad}' elements on cards")


def no_old_anchors():
    for p in PAGES:
        s = read(p)
        for a in OLD_ANCHORS:
            if f'"{a}"' in s or f'index.html{a}"' in s or f'id="{a[1:]}"' in s:
                fail("no_old_anchors", f"{p} still uses {a}")


def next_chain():
    for here, nxt in zip(CHAIN[:-1], CHAIN[1:]):
        s = read(here)
        bottom = re.findall(r'<a href="([^"#]+)[^"]*" class="btn btn-primary">', s)
        if not bottom or bottom[-1] != nxt:
            fail("next_chain", f"{here} bottom next -> {bottom[-1] if bottom else None}, expected {nxt}")


def figure_numbers():
    for page, prefix, wrong in (("onewheel.html", "5.", "6."), ("can-transceiver.html", "6.", "5.")):
        figs = re.findall(r"Fig (\d+\.\d+)", read(page))
        if not figs or any(not f.startswith(prefix) for f in figs):
            fail("figure_numbers", f"{page} figures {sorted(set(figs))}, expected all {prefix}x")


def contact_links():
    s = read("index.html")
    for link in (EMAIL, LINKEDIN):
        if link not in s:
            fail("contact_links", f"index.html missing {link}")


SECTION_OF = {
    "fuse-blast.html": "professional-work", "upulse.html": "professional-work",
    "unreleased-rd.html": "professional-work", "mtg-counter.html": "robotics-builds",
    "onewheel.html": "robotics-builds", "can-transceiver.html": "robotics-builds",
    "robotics.html": "robotics-builds", "toolkit.html": "side-projects",
}


def prev_chain():
    for i, here in enumerate(CHAIN[:-1]):
        s = read(here)
        bottom = re.findall(r'<a href="([^"]+)" class="btn btn-secondary">', s)
        want = CHAIN[i - 1] if i > 0 else f"index.html#{SECTION_OF[here]}"
        if not bottom or bottom[-1] != want:
            fail("prev_chain", f"{here} bottom previous -> {bottom[-1] if bottom else None}, expected {want}")


def header_links():
    for i, here in enumerate(CHAIN[:-1]):
        s = read(here)
        m = re.search(r'<ul class="nav-links" id="nav-links">(.*?)</ul>', s, re.S)
        got = re.findall(r'<a href="([^"]+)"', m.group(1)) if m else None
        want = [f"index.html#{SECTION_OF[here]}"] + ([CHAIN[i - 1]] if i > 0 else []) + [CHAIN[i + 1]]
        if got != want:
            fail("header_links", f"{here} header links {got} != {want}")


def no_resume_file():
    if (ROOT / "assets/docs/ChrisJohnsonResume.docx.pdf").exists():
        fail("no_resume_file", "assets/docs/ChrisJohnsonResume.docx.pdf is still published")


CHECKS = [no_resume_links, no_footer_boilerplate, homepage_nav, homepage_sections,
          homepage_cards, no_old_anchors, next_chain, prev_chain, header_links,
          figure_numbers, contact_links, no_resume_file]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for check in CHECKS:
        check()
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print("ALL STRUCTURE CHECKS PASSED")
