# Design Specification: Christopher Johnson Portfolio Website

**Date:** 2026-08-30  
**Author:** Christopher Johnson / Antigravity  
**Status:** Approved  
**Target Platform:** GitHub Pages (`github.io`)

---

## 1. Overview & Objectives

Create a high-performance, responsive, and visually modern engineering portfolio website for **Christopher Johnson**, **Mechanical Design Engineer**. The site emphasizes mass manufacturing, precision mechanisms, mechatronics, firmware, robotics mentorship, and full-stack hardware/software capabilities.

### Key Constraints & Requirements
1. **GitHub Pages Optimized**: Pure static HTML/CSS/JavaScript with zero build step dependencies.
2. **File Size & Performance**: All images and animated videos converted to lightweight modern `.webp` format for sub-second page loads.
3. **Easy Plaintext Editing**: Semantic, well-structured HTML markup with clear edit comments (`<!-- EDIT: ... -->`) enabling direct, non-technical copy editing in any text editor without token overhead.
4. **Read Top-to-Bottom Structure**: A single-page flow on `index.html` featuring a hero section, sticky category anchor navigation with scroll-spy, and 7 project showcase cards.
5. **Multi-Page Deep Dives**: Each showcase card links to a dedicated, high-detail project page (`fuse-blast.html`, `upulse.html`, `unreleased-rd.html`, `mtg-counter.html`, `can-transceiver.html`, `robotics.html`, `toolkit.html`).
6. **Interactive 3D CAD Viewer**: An interactive WebGL/Three.js 3D viewer on the MTG Life Counter page supporting 360° orbit/zoom and individual part show/hide toggles.
7. **Git History**: Early and frequent commits tracking every phase of creation.

---

## 2. Information Architecture & Navigation

### 2.1 Landing Page (`index.html`)
* **Hero Section**:
  * Name: `Christopher Johnson`
  * Subtitle: `Mechanical Design Engineer`
  * Hook: *"Designing precision mechanisms, robotics, and mass-manufactured hardware from first principles to high-volume production."*
  * Quick Actions: `[ Explore Projects ↓ ]` & `[ Download Resume 📄 ]`
* **Sticky Category Anchor Nav**:
  * `Mass Manufacturing` → Formlabs Fuse Blast, uPulse Turnaround, Unreleased R&D
  * `Mechatronics` → MTG Life Counter, CAN Bus Transceiver
  * `Leadership` → FIRST Robotics Team 4909
  * `Toolkit & Homelab` → Homelab, Tech Stack & Resume
* **7 Top-to-Bottom Showcase Cards**:
  * Card 1: **Formlabs: Fuse Blast** (Mass Manufacturing, Hopper, Welding, Global Sourcing, Die-Casting DFM)
  * Card 2: **uPulse Turnaround** (Liquid Level Sense, Pressure Gradient Tech, EP4739424A1 Patent)
  * Card 3: **Unreleased Product R&D** (Optics & Air Handling Design, NDA-compliant, Formlabs Butterfly badge)
  * Card 4: **MTG Life Counter** (Mechatronics, 3-Second Looping WebP, Exploded CAD View, Planetary Gearbox)
  * Card 5: **CAN Bus Transceiver** (Custom PCB Circuit, ESP32 Integration, AI-Assisted Firmware)
  * Card 6: **FIRST Robotics Team 4909** (Leadership, Mentorship, World Championships robot gallery 2018–2026)
  * Card 7: **The Toolkit & Homelab** (Raspberry Pi, Plex, Custom Networking, DIY Onewheel, Contact & Resume Download)

### 2.2 Deep-Dive Project Pages
* `fuse-blast.html` — Detailed mass manufacturing case study, sheet metal & robotic welding, global vendor management, die-cast DFM tooling.
* `upulse.html` — The rescue mission, liquid level sensing redevelopment, pressure gradient mechanics, patent callout with PDF link.
* `unreleased-rd.html` — Confidential R&D ownership, optical pathways, precision air handling, thermal management.
* `mtg-counter.html` — Mechatronic life counter, 3D interactive viewer with part toggles, looping animation, exploded view, gear tooth geometry & backlash analysis.
* `can-transceiver.html` — Custom schematic design, signal integrity, ESP32 firmware, transceiver hardware validation.
* `robotics.html` — FRC Team 4909 mentorship philosophy, mechanism engineering, season-by-season robot showcase.
* `toolkit.html` — Homelab architecture, networking, embedded toolchain, DIY projects (Onewheel), full skills breakdown, direct resume download.

---

## 3. Visual Design System (Dark Industrial)

* **Color Palette**:
  * Background Main: `#0B0F17` (Deep Dark Slate)
  * Card / Container Surface: `#131D2E` (Technical Blue-Gray)
  * Elevated Elements & Header: `#0F1726ee` with glassmorphic `backdrop-filter: blur(12px)`
  * Primary Accent: `#00D2FF` (Precision Electric Cyan)
  * Secondary Accent: `#FF6B00` / `#F59E0B` (Industrial Amber / Formlabs Orange)
  * Border Lines: `#24334A`
  * Typography: `#F8FAFC` (Headings/Body), `#94A3B8` (Subtext/Captions)
* **Typography**:
  * Headings & Body: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, sans-serif.
  * Code, Specs, Metadata: `JetBrains Mono`, `Consolas`, `Fira Code`, monospace.
* **UI Components**:
  * Responsive cards with hover elevation and subtle accent glows.
  * Sticky navigation header with scroll-spy progress indication.
  * Lightbox modal for clicking and inspecting full-size gallery photos.
  * Interactive 3D Canvas with OrbitControls and Part Visibility Toggle chips.

---

## 4. Media & Asset Pipeline

* **Python Conversion Script (`scripts/convert_media.py`)**:
  * Converts all JPG, PNG, and camera photos in `Resources/` to optimized `.webp` format in `assets/img/`.
  * Trims and encodes `MTG Counter.mp4` into a lightweight, looping animated `.webp`.
  * Copies `ChrisJohnsonResume.docx.pdf` and `Patent_Real.pdf` to `assets/docs/`.
  * Converts `MTG Life Counter.step` to an optimized `.glb` 3D model asset for Three.js web rendering.

---

## 5. Technical Implementation & Verification Plan

1. **Media Processing**: Execute `scripts/convert_media.py` and verify all webp assets generated with high quality and minimal footprint.
2. **Core Styling**: Build `assets/css/style.css` covering mobile, tablet, and desktop viewports.
3. **Core Interactivity**: Build `assets/js/main.js` (smooth anchor scrolling, sticky nav scrollspy, image lightbox modal, and Three.js 3D viewer with part toggles).
4. **Page Construction**:
   * Build `index.html` with all 7 top-to-bottom project preview sections.
   * Build all 7 project detail HTML pages with clean structure and editable comment guides.
5. **Local Web Server Verification**: Serve locally via `python -m http.server` and test all links, anchors, responsive layouts, 3D interactions, and media rendering.
6. **Git Version Control**: Initialize git repo and commit each milestone cleanly with descriptive messages.
