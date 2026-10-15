# Portfolio Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the static portfolio so the homepage reads as one consistent story (three sections, cards 01–08, one card anatomy, contact instead of resume) and every subpage follows the same order and labels.

**Architecture:** Plain static HTML/CSS/JS served from the repo root (GitHub Pages). A new `scripts/check_structure.py` encodes the spec's structural rules as assertions and is the "test" each task makes pass; `scripts/verify_site.py` (existing) keeps catching broken links, anchors, and non-WebP images.

**Tech Stack:** HTML, CSS (`assets/css/style.css`), vanilla JS (`assets/js/main.js`), Python 3 + Pillow for checks and image prep.

**Spec:** `docs/superpowers/specs/2026-10-14-portfolio-restructure-design.md`

## Global Constraints

- Card order and tags exactly as the spec table: 01 Fuse Blast (Formlabs), 02 uPulse (Formulatrix), 03 Next-Generation Printer (Formlabs (NDA)), 04 MTG Life Counter (Personal), 05 DIY Onewheel (Personal), 06 CAN Bus Fault Isolator (FIRST Robotics), 07 FIRST Robotics (FIRST Robotics), 08 Raspberry Pi Home Server (Personal).
- Section names, nav labels, and breadcrumb names: "Professional Work", "Robotics & Builds", "Side Projects", "Contact". Section headings carry no number and no `//`.
- Section ids: `professional-work`, `robotics-builds`, `side-projects`, `skills`, `contact` (each a `<section id>` so the existing scroll-spy in `main.js` picks them up).
- Email `c.johnson.career@gmail.com`; LinkedIn `https://www.linkedin.com/in/ChrisJohnson4909`.
- No "Download Resume"/"Download PDF Resume" anywhere; no `ChrisJohnsonResume` link anywhere in HTML.
- No skill pills (`skill-pill`) and no image badges (`media-badge`) on homepage cards. Every card button reads exactly "View project →".
- All images WebP; the headshot is `assets/img/headshot.webp`.
- Only facts already on the site or approved in conversation; no new claims (see memory "no invented portfolio content").
- Pitch line wording is approved by Christopher in chat before it is committed.

## Review Focus

- **Phone width (375 px):** hero with the new round photo and two contact buttons must not cause horizontal scroll; photo stacks above text. Pinned in Task 3 (browser check).
- **Old anchors still linked from subpages:** `#mass-production`, `#mechatronics`, `#leadership`, `#toolkit-homelab` must be gone from every page; `verify_site.py` must report zero broken anchors. Pinned in Task 4 (check_structure asserts none of the old anchors appear).
- **Mobile nav menu:** the hamburger menu on the homepage must still open and list the four new nav items. Pinned in Task 3 (browser check at 375 px).
- **Scroll-spy highlighting:** nav highlight must track the new sections. Pinned in Task 3 (browser check: scroll to Robotics & Builds, its nav link gets `active`).
- **Both 3D viewers after the page edits:** MTG and Onewheel viewers still load. Pinned in Task 6 (browser check).

---

### Task 1: Structure check script

**Files:**
- Create: `scripts/check_structure.py`

**Interfaces:**
- Produces: `python scripts/check_structure.py` → prints one `[FAIL] <rule>` line per violation and exits 1, or prints `ALL STRUCTURE CHECKS PASSED` and exits 0. Later tasks run it as their test.

- [ ] **Step 1: Write the checks** as plain functions over the HTML files in `verify_site.py`'s `html_files` list (read as text; `html.parser` or regex is fine):
  - `no_resume_links`: no file contains `ChrisJohnsonResume` or `Download Resume` or `Download PDF Resume`.
  - `no_footer_boilerplate`: no file contains `Built for GitHub Pages` or `Optimized WebP Media` or `All rights reserved`.
  - `homepage_nav`: index.html header nav link texts are exactly `["Professional Work", "Robotics & Builds", "Side Projects", "Contact"]`.
  - `homepage_sections`: index.html has `<section id=...>` for all five ids in Global Constraints, in that order; section headings contain no `//` and no leading digits.
  - `homepage_cards`: `.project-card` elements in order have numbers `01`…`08`, tags and titles exactly as the Global Constraints list, button text exactly `View project →`, zero `skill-pill`, zero `media-badge`.
  - `no_old_anchors`: no file contains `#mass-production`, `#mechatronics`, `#leadership`, or `#toolkit-homelab`.
  - `next_chain`: each subpage's bottom "Next" button links to the next page in card order (`fuse-blast → upulse → unreleased-rd → mtg-counter → onewheel → can-transceiver → robotics → toolkit`), and `toolkit.html`'s goes to `index.html`.
  - `figure_numbers`: `onewheel.html` figures are `Fig 5.x`, `can-transceiver.html` figures are `Fig 6.x`.
  - `contact_links`: index.html contains the exact mailto and LinkedIn URLs from Global Constraints.

- [ ] **Step 2: Run it to confirm it fails on the current site**

Run: `python scripts/check_structure.py`
Expected: exit 1 with FAIL lines for every rule above.

- [ ] **Step 3: Commit**

```bash
git add scripts/check_structure.py
git commit -m "test: add structure checks for portfolio restructure"
```

### Task 2: Pitch line (human gate)

**Files:** none

- [ ] **Step 1:** Discuss the hero pitch line with Christopher in chat (2–4 options, plain words, one sentence, true to the site). Do not start Task 3's hero copy until he picks one.
- [ ] **Step 2:** Record the chosen sentence verbatim in this plan's Task 3 Step 3 before implementing.

### Task 3: Homepage hero, header, and nav

**Files:**
- Create: `assets/img/headshot.webp` (from `Resources/Headshot_ChrisJohnson.jpg`)
- Modify: `index.html` (header, hero), `assets/css/style.css` (hero photo layout)

**Interfaces:**
- Consumes: pitch line from Task 2.
- Produces: header markup pattern reused by Task 5: brand = "Christopher Johnson" only; nav ends with a plain `Contact` link to `index.html#contact` (on index: `#contact`).

- [ ] **Step 1:** Crop the headshot square around head and shoulders, cutting above the boutonniere; resize to 600×600; save `assets/img/headshot.webp` (quality 85). Look at the result before using it.
- [ ] **Step 2:** Header: remove the `brand-badge`; nav links become the four Global Constraints labels pointing at `#professional-work`, `#robotics-builds`, `#side-projects`, `#contact`; replace the Resume button with the Contact link.
- [ ] **Step 3:** Hero: round photo beside the text block; name, "Mechanical Design Engineer", pitch line "I take hardware from first prototype to production, and I build robots because I can't stop."; buttons "Explore Projects ↓" (to `#professional-work`), "Email" (mailto), "LinkedIn" (new tab). Remove "Download PDF Resume". At ≤768 px the photo stacks above the text.
- [ ] **Step 4: Verify** in the browser at desktop and 375 px: no horizontal scroll, photo stacks on phone, hamburger opens with the four items; scrolling to Robotics & Builds marks its nav link `active` (after Task 4 adds the section).
- [ ] **Step 5: Commit** `feat(home): new hero with headshot and contact links`

### Task 4: Homepage sections, cards, skills, contact, footer

**Files:**
- Modify: `index.html`, `assets/css/style.css` (skills strip, contact section)

**Interfaces:**
- Consumes: section ids from Global Constraints.
- Produces: `#skills` and `#contact` sections; card order used by Task 5's prev/next chain.

- [ ] **Step 1:** Rebuild the project area as three `<section id>` blocks with plain headings "Professional Work", "Robotics & Builds", "Side Projects", cards in the Global Constraints order and anatomy (number, tag, title, tagline, description, "View project →", image). Delete all `skill-pill` and `media-badge` elements. Pi card: title "Raspberry Pi Home Server", description without "Plus my skills and resume". Re-read each card blurb against its page and fix any mismatch (list fixes in the commit message).
- [ ] **Step 2:** Add `<section id="skills">` with the three columns and exact lists from the spec.
- [ ] **Step 3:** Add `<section id="contact">`: one sentence inviting contact plus Email and LinkedIn buttons.
- [ ] **Step 4:** Footer: name, Email, LinkedIn, project links in 01–08 order, "© 2026 Christopher Johnson". Remove the bio line, resume button, "Built for GitHub Pages…", "All rights reserved".
- [ ] **Step 5: Run** `python scripts/check_structure.py` → homepage rules (`homepage_nav`, `homepage_sections`, `homepage_cards`, `contact_links`, `no_footer_boilerplate` for index) pass.
- [ ] **Step 6: Commit** `feat(home): three sections, consistent cards, skills and contact`

### Task 5: Subpage headers, breadcrumbs, and prev/next chain

**Files:**
- Modify: `fuse-blast.html`, `upulse.html`, `unreleased-rd.html`, `mtg-counter.html`, `onewheel.html`, `can-transceiver.html`, `robotics.html`, `toolkit.html`

**Interfaces:**
- Consumes: header pattern from Task 3; card order from Task 4.

- [ ] **Step 1:** Every subpage header: remove `brand-badge` and the "Download Resume" button; add the Contact link (`index.html#contact`).
- [ ] **Step 2:** Breadcrumbs and "← Back to Overview" links point to the page's new section anchor with its name ("← Back to Professional Work" for 01–03, "← Back to Robotics & Builds" for 04–07, "← Back to Side Projects" for 08).
- [ ] **Step 3:** Header prev/next nav links and bottom buttons follow the card order; first page's previous is the overview, `toolkit.html`'s next is "Back to overview" (`index.html`).
- [ ] **Step 4: Run** `python scripts/check_structure.py` → `no_resume_links`, `no_old_anchors`, `next_chain` pass; `python scripts/verify_site.py` → 0 errors.
- [ ] **Step 5: Commit** `feat(pages): consistent headers, breadcrumbs, and page order`

### Task 6: Figure numbers and the Pi Home Server page

**Files:**
- Modify: `onewheel.html` (Fig 6.x → 5.x), `can-transceiver.html` (Fig 5.x → 6.x), `toolkit.html`, `scripts/verify_site.py` (asset list if changed)

- [ ] **Step 1:** Renumber figures (captions and any "See Fig" references).
- [ ] **Step 2:** `toolkit.html`: title/meta/H1 "Raspberry Pi Home Server"; remove the resume card and the Skills & Tools section and the resume spec-grid item; keep the three stories; add `assets/img/pi-server-hub.webp` as the page image (gallery item with caption).
- [ ] **Step 3: Run** `python scripts/check_structure.py` → `figure_numbers` passes; `verify_site.py` → 0 errors.
- [ ] **Step 4: Verify** both 3D viewers (MTG, Onewheel) still load in the browser.
- [ ] **Step 5: Commit** `feat(pages): renumber figures; Pi Home Server page`

### Task 7: Filler sweep

**Files:** any of the nine HTML pages

- [ ] **Step 1:** Read every page's extracted text plus `<title>` and meta description; fix leftover marketing phrasing, mismatched labels, stale titles (e.g. anything still saying "Turnaround", "Toolkit & Homelab", "Unreleased R&D" where the visible name differs), duplicated nav items.
- [ ] **Step 2:** List every change for Christopher to veto.
- [ ] **Step 3: Run** both scripts → `ALL STRUCTURE CHECKS PASSED` and `SUCCESS: 0 errors`.
- [ ] **Step 4: Verify** each page at desktop and 375 px (no horizontal scroll) and click the prev/next chain 01→08→overview.
- [ ] **Step 5: Commit** `chore: filler sweep across all pages`
