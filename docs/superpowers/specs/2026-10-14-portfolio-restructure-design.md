# Portfolio Restructure: Design Spec

**Date:** 2026-10-14
**Status:** Approved in conversation; awaiting written-spec review

## Goal

A hiring manager skimming the homepage for under a minute, without clicking anything, gets an accurate picture of who Christopher is and what he's best at, then clicks into the projects that matter to them. Nothing reads as AI-generated, and every label, number, and blurb is consistent.

## Positioning

- **Lead identity:** Mechanical Design Engineer. Most target roles are mechanical design; the strongest evidence is products taken to production.
- **Differentiator:** robotics and mechatronics (gear trains, a balancing board, a CAN board, 14 years of FIRST). This must read as real engineering, not a hobby afterthought.
- **No resume download anywhere.** Resumes are tailored per job; the site is fixed. Contact is by email and LinkedIn.

## Homepage

### Hero

- Round headshot (cropped from `Resources/Headshot_ChrisJohnson.jpg`, head and shoulders, cropped above the boutonniere), beside the text block.
- Name: "Christopher Johnson". Headline: "Mechanical Design Engineer".
- Pitch line (one sentence, plain): "I design hardware that ships, and I build robots because I can't stop." Final wording is confirmed with Christopher in the text review doc before commit.
- Buttons: **Email** (`mailto:c.johnson.career@gmail.com`) and **LinkedIn** (`https://www.linkedin.com/in/ChrisJohnson4909`).
- Removed: "Mech Eng" badge next to the name (header and hero), "Download PDF Resume" button. The "Explore Projects" button stays.
- Published image file gets a neutral name: `assets/img/headshot.webp`.

### Header (all pages)

- Brand: "Christopher Johnson" only (no badge).
- Homepage nav, matching section headings exactly: **Professional Work · Robotics & Builds · Side Projects · Contact**.
- The "Resume" button becomes a plain **Contact** link to `index.html#contact`.

### Sections and cards

Section headings use one style: plain words, no number, no `//` prefix.

| # | Section | Card title | Context tag | Page |
|---|---|---|---|---|
| 01 | Professional Work | Fuse Blast | Formlabs | `fuse-blast.html` |
| 02 | Professional Work | uPulse | Formulatrix | `upulse.html` |
| 03 | Professional Work | Next-Generation Printer | Formlabs (NDA) | `unreleased-rd.html` |
| 04 | Robotics & Builds | MTG Life Counter | Personal | `mtg-counter.html` |
| 05 | Robotics & Builds | DIY Onewheel | Personal | `onewheel.html` |
| 06 | Robotics & Builds | CAN Bus Fault Isolator | FIRST Robotics | `can-transceiver.html` |
| 07 | Robotics & Builds | FIRST Robotics | FIRST Robotics | `robotics.html` |
| 08 | Side Projects | Raspberry Pi Home Server | Personal | `toolkit.html` |

**Card anatomy (identical on every card, nothing else):**

1. Number (`01`–`08`) and one context tag from the table.
2. Title.
3. One-line tagline.
4. Two-to-three-line description.
5. One button: "View project →".
6. Image.

**Removed from every card:** all skill pills; all image overlay badges ("Interactive 3D Available", "Fuse-Blast", "Under NDA", "Personal Build", "Robots 2018–2026", "Hardware & Code", "Side Projects", uPulse's empty badge). Descriptions do not mention the 3D viewers.

Card taglines and descriptions are re-checked against each page's current content so every blurb matches what the page shows. The Pi card's description drops "Plus my skills and resume."

### Skills strip

A compact three-column block after Side Projects, no card styling. Content from the current Toolkit page:

- **CAD:** SolidWorks, Onshape
- **Manufacturing:** Die casting, sheet metal, injection molding, CNC machining, GD&T, 3D printing (SLA, FDM, SLS), shop tools (manual mill and lathe, drill press, band saw)
- **Electronics & Code:** ESP32, Arduino, Raspberry Pi, C/C++, Python, Git, Linux, AI tools

### Contact (`#contact`)

A short closing section: one sentence inviting contact, plus the Email and LinkedIn buttons.

### Footer

- Keep: name, Email, LinkedIn, project links in the 01–08 order.
- Remove: "Built for GitHub Pages • Optimized WebP Media", the generic bio line, "Download PDF Resume".
- Copyright line becomes just "© 2026 Christopher Johnson" (drop "All rights reserved").

## Subpages

- **Header:** remove "Download Resume"; add the plain Contact link.
- **Breadcrumbs and "Back to" links:** use the new section names and anchors ("← Back to Professional Work", "← Back to Robotics & Builds", "← Back to Side Projects").
- **Prev/next chain:** Fuse Blast → uPulse → Next-Gen Printer → MTG → Onewheel → CAN → FIRST → Pi Server → "Back to overview". Header nav links and bottom buttons both follow it.
- **Figure numbers match card numbers:** Fuse Blast 1.x, uPulse 2.x, MTG 4.x (unchanged), Onewheel 6.x → 5.x, CAN 5.x → 6.x. Pages without figures are unchanged.
- **`toolkit.html` becomes "Raspberry Pi Home Server":** remove the resume card and the skills section; keep the three stories (smart scale, TV-aware lamp, over-the-air TV); add the dashboard screenshot (`assets/img/pi-server-hub.webp`) as the page image. File name unchanged so links don't break.

## Filler sweep

A final pass over all nine pages for leftover marketing phrases, mismatched labels, stale `<title>` and meta descriptions, and duplicated or inconsistent nav items. Every change from the sweep is listed for Christopher to veto.

## Testing

- `scripts/verify_site.py` passes (update its asset list for any added/removed files).
- Each page checked in the browser at desktop width and at 375 px with no horizontal scroll.
- Click through the prev/next chain from 01 to 08 and back to the overview.
- Both 3D viewers still load.
- Homepage text extracted and read top to bottom to confirm every card follows the anatomy and every blurb matches its page.

## Out of scope

- Visual redesign of the theme (colors, fonts, card styling beyond removing pills and badges).
- New project content beyond what's already written.
- Deployment to GitHub Pages.
