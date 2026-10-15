# Christopher Johnson Portfolio Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, responsive, dark industrial-themed multi-page engineering portfolio website for Christopher Johnson (Mechanical Design Engineer) optimized for GitHub Pages with WebP media, interactive 3D CAD viewer, and easily editable semantic HTML.

**Architecture:** A static multi-page site composed of `index.html` (Hero, sticky category anchor nav with scroll-spy, 7 project preview cards) and 7 deep-dive project detail pages (`fuse-blast.html`, `upulse.html`, `unreleased-rd.html`, `mtg-counter.html`, `can-transceiver.html`, `robotics.html`, `toolkit.html`). Shared modular styles in `assets/css/style.css`, shared interactivity and Three.js 3D viewer with part-visibility toggles in `assets/js/main.js`, and all media converted to optimized `.webp` in `assets/img/`.

**Tech Stack:** HTML5 (Semantic & Commented), Modern CSS3 (CSS Variables, Flexbox/Grid, Glassmorphic effects), Vanilla JavaScript (ES6+), Three.js (WebGL 3D Viewer with OrbitControls), Python (Pillow / conversion tools).

**Spec:** [docs/superpowers/specs/2026-08-30-portfolio-website-design.md](file:///c:/Users/penguins/Documents/Gemini/Portfolio/docs/superpowers/specs/2026-08-30-portfolio-website-design.md)

## Global Constraints
- Target platform: GitHub Pages (100% static, zero build step required).
- All image and animation media must be optimized `.webp` format for fast loading and low bandwidth.
- Plaintext content must be structured in semantic HTML `<p>`, `<li>`, `<h3>` with clear `<!-- EDIT: ... -->` comment blocks.
- Frequent git commits after each task.

---

### Task 1: Media Conversion & Asset Pipeline Setup

**Files:**
- Create: `scripts/convert_media.py`
- Create: `scripts/convert_step.py`
- Create: `assets/img/*`
- Create: `assets/docs/*`
- Create: `assets/models/*`

**Interfaces:**
- Produces: Optimized `.webp` images in `assets/img/`, PDF documents in `assets/docs/`, and 3D `.glb` model in `assets/models/`.

- [ ] **Step 1: Write media conversion script**
Create `scripts/convert_media.py` to:
1. Ensure Pillow / imageio is installed.
2. Convert all image files in `Resources/` (`Fuse-Blast.webp`, `uPulse.jpg`, `CanTransceiverFundamentalCircuit.PNG`, `CAN Transceiver.png`, `MTG ExplodeView.PNG`, `MTG LifeCounters.jpg`, `Robot2018-2026.jpg`, `Onewheel_Homemade.jpg`) to standardized WebP files in `assets/img/`.
3. Extract and convert `MTG Counter.mp4` into a 3-second looping animated `.webp` (`assets/img/mtg-counter-loop.webp`).
4. Generate SVG/WebP for Formlabs butterfly branding (`assets/img/formlabs-butterfly.webp` / `.svg`).
5. Copy `ChrisJohnsonResume.docx.pdf` and `Patent_Real.pdf` to `assets/docs/`.

- [ ] **Step 2: Run media conversion script**
Run: `python scripts/convert_media.py`
Expected: All webp and doc assets created in `assets/img/` and `assets/docs/`.

- [ ] **Step 3: Setup STEP 3D model conversion**
Create `scripts/convert_step.py` to convert `MTG Life Counter.step` into `assets/models/mtg-counter.glb` with named mesh parts. Run and verify `assets/models/mtg-counter.glb` is generated.

- [ ] **Step 4: Commit assets and conversion scripts**
```bash
git add scripts/ assets/
git commit -m "feat(assets): add media conversion pipeline and generate webp assets"
```

---

### Task 2: Core Dark Industrial CSS Design System

**Files:**
- Create: `assets/css/style.css`

**Interfaces:**
- Consumes: CSS Variables & Design tokens.
- Produces: Complete styling for index and detail pages, navbar, hero, cards, galleries, buttons, typography, and 3D viewer container.

- [ ] **Step 1: Write `assets/css/style.css`**
Implement:
1. Color variables: Background `#0B0F17`, Surface `#131D2E`, Elevated `#0F1726ee`, Border `#24334A`, Primary Cyan `#00D2FF`, Secondary Amber `#FF6B00`, Text `#F8FAFC`, Muted `#94A3B8`.
2. Typography: Inter / system sans font family, JetBrains Mono for specs/tags.
3. Sticky navigation header with glassmorphism blur and active indicator underline.
4. Hero layout with clean grid, typography hierarchy, and CTA buttons.
5. Section project cards: High-contrast split layout (Summary/tags left, WebP visual right) with smooth hover zoom.
6. Case study layout: Overview banner, grid metrics, problem/solution breakdown, technical callout cards, photo gallery with hover zoom.
7. 3D Model viewer container: WebGL canvas wrapper, loading spinner, and floating part toggle pill buttons.
8. Image lightbox modal styles.
9. Fully responsive media queries for desktop, tablet, and mobile.

- [ ] **Step 2: Verify CSS validity and structure**
Ensure syntax is clean, variables are unified, and no broken rules exist.

- [ ] **Step 3: Commit CSS stylesheet**
```bash
git add assets/css/style.css
git commit -m "feat(css): implement Dark Industrial styling system and responsive layouts"
```

---

### Task 3: Core Interactive JavaScript & 3D WebGL Viewer

**Files:**
- Create: `assets/js/main.js`

**Interfaces:**
- Produces: Navigation scroll-spy, smooth anchor scrolling, image lightbox modal, and Three.js 3D CAD viewer with individual part show/hide toggles.

- [ ] **Step 1: Write `assets/js/main.js`**
Implement:
1. Smooth anchor scrolling for category navigation.
2. Scroll-Spy: Highlights active category anchor in sticky navbar based on scroll position (`IntersectionObserver`).
3. Mobile navbar toggle handling.
4. Lightbox Modal: Intercepts gallery image clicks to display high-res image modal with caption and keyboard navigation (Esc to close).
5. Interactive 3D Model Viewer (`initCadViewer(containerId, modelUrl)`):
   - Initializes Three.js Scene, PerspectiveCamera, WebGLRenderer, and OrbitControls.
   - Adds studio lighting (Key, Fill, Ambient, Rim lights).
   - Loads `.glb` model via `GLTFLoader`.
   - Inspects meshes, collects distinct part nodes, and creates interactive toggle chips in `#cad-parts-list`.
   - Clicking a part chip toggles `mesh.visible` and toggles active button state.
   - Adds reset view and auto-rotate controls.

- [ ] **Step 2: Verify JS functionality**
Ensure zero errors on load and graceful degradation if WebGL is unsupported.

- [ ] **Step 3: Commit JavaScript**
```bash
git add assets/js/main.js
git commit -m "feat(js): implement scroll-spy, lightbox modal, and 3D CAD viewer with part toggles"
```

---

### Task 4: Main Landing Page (`index.html`)

**Files:**
- Create: `index.html`

**Interfaces:**
- Consumes: `assets/css/style.css`, `assets/js/main.js`, `assets/img/*.webp`.
- Produces: Landing page with Hero, Sticky Nav, and 7 top-to-bottom project showcase cards.

- [ ] **Step 1: Write `index.html`**
Include:
1. Meta tags, viewport, fonts, stylesheet links.
2. Hero section:
   - Christopher Johnson
   - Mechanical Design Engineer
   - Editable 1-sentence hook: `<!-- EDIT: Hook Sentence -->`
   - CTA buttons: `Explore Projects ↓` and `Download Resume 📄`.
3. Sticky Anchor Navigation:
   - `Mass Manufacturing` (`#mass-manufacturing`)
   - `Mechatronics` (`#mechatronics`)
   - `Leadership` (`#leadership`)
   - `Toolkit & Homelab` (`#toolkit-homelab`)
4. 7 Showcase Cards with WebP previews:
   - Section 1: Formlabs: Fuse Blast (`fuse-blast.html`)
   - Section 2: uPulse Turnaround (`upulse.html`)
   - Section 3: Unreleased Product R&D (`unreleased-rd.html`)
   - Section 4: MTG Life Counter (`mtg-counter.html`)
   - Section 5: CAN Bus Transceiver (`can-transceiver.html`)
   - Section 6: FIRST Robotics Team 4909 (`robotics.html`)
   - Section 7: The Toolkit & Homelab (`toolkit.html`)
5. Footer with direct social/contact links (LinkedIn, GitHub, Email, Resume).

- [ ] **Step 2: Verify landing page layout and navigation**
Check anchor links scroll smoothly to matching categories and card links go to respective pages.

- [ ] **Step 3: Commit `index.html`**
```bash
git add index.html
git commit -m "feat(page): create main landing page with hero, sticky anchor nav, and 7 project showcases"
```

---

### Task 5: Project Detail Pages — Mass Manufacturing & R&D

**Files:**
- Create: `fuse-blast.html`
- Create: `upulse.html`
- Create: `unreleased-rd.html`

**Interfaces:**
- Consumes: `assets/css/style.css`, `assets/js/main.js`, `assets/img/`, `assets/docs/`.
- Produces: Deep-dive case studies for Fuse Blast, uPulse, and Unreleased R&D.

- [ ] **Step 1: Write `fuse-blast.html`**
Detail case study covering:
- Hopper subsystem design and sheet metal DFM.
- Robotic seam welding and structural integrity.
- Global vendor sourcing, tooling trials, and quality control.
- Die-casting DFM (draft angles, wall thickness, parting lines, machining tolerances).
- Photo gallery with high-res WebP visuals and edit comment guides.

- [ ] **Step 2: Write `upulse.html`**
Detail case study covering:
- The rescue mission narrative: taking over an unverified subsystem.
- Liquid level sensing redevelopment and signal consistency.
- New pressure gradient technology.
- Prominent Patent Feature Card: Patent [EP4739424A1](https://patents.google.com/patent/EP4739424A1/en) with direct link and download link to `assets/docs/Patent_Real.pdf`.
- Photo gallery and technical diagrams.

- [ ] **Step 3: Write `unreleased-rd.html`**
Detail case study covering:
- NDA-compliant R&D narrative highlighting trust with future confidential architectures.
- Optical pathway alignment, precision mounting, and thermal drift prevention.
- Custom airflow handling, aerodynamic CFD validation, and particle control.
- Formlabs butterfly branding visual and clear edit placeholders.

- [ ] **Step 4: Commit mass manufacturing & R&D pages**
```bash
git add fuse-blast.html upulse.html unreleased-rd.html
git commit -m "feat(pages): create detail case studies for Fuse Blast, uPulse, and Unreleased R&D"
```

---

### Task 6: Project Detail Pages — Mechatronics & Firmware

**Files:**
- Create: `mtg-counter.html`
- Create: `can-transceiver.html`

**Interfaces:**
- Consumes: Three.js CDN / `assets/js/main.js`, `assets/models/mtg-counter.glb`, `assets/img/mtg-counter-loop.webp`, `assets/img/can-*.webp`.
- Produces: Deep-dive case studies for MTG Life Counter and CAN Bus Transceiver.

- [ ] **Step 1: Write `mtg-counter.html`**
Include:
- 3-second looping animated WebP hero demonstrating mechanism in action.
- Interactive 3D CAD Viewer container (`#cad-viewer`) with part visibility toggles for Housing, Dials, Planetary Carrier, Ring Gear, and Pinions.
- Exploded CAD view breakdown (`assets/img/mtg-explode.webp`).
- Gearbox engineering challenge: module sizing, custom tooth profiles to prevent jamming, backlash minimization, and detent feel.
- Manufacturing & assembly: 3D printing tolerances, snap fits, and tactile feedback.

- [ ] **Step 2: Write `can-transceiver.html`**
Include:
- Electronics & PCB design: custom circuit schematic breakdown (`assets/img/can-schematic.webp`, `assets/img/can-circuit.webp`).
- Transceiver selection, bus termination, and EMI / signal integrity.
- ESP32 hardware integration and pinout architecture.
- AI-assisted firmware development workflow (prompt engineering for register-level drivers and CAN message filtering).
- Hardware validation and oscilloscope capture analysis.

- [ ] **Step 3: Commit mechatronics & firmware pages**
```bash
git add mtg-counter.html can-transceiver.html
git commit -m "feat(pages): create detail case studies for MTG Life Counter and CAN Bus Transceiver"
```

---

### Task 7: Project Detail Pages — Leadership, Homelab & Resume

**Files:**
- Create: `robotics.html`
- Create: `toolkit.html`

**Interfaces:**
- Consumes: `assets/img/robot-*.webp`, `assets/img/onewheel.webp`, `assets/docs/ChrisJohnsonResume.docx.pdf`.
- Produces: FIRST Robotics Team 4909 mentorship page and Toolkit/Homelab page with resume download.

- [ ] **Step 1: Write `robotics.html`**
Include:
- FIRST Robotics Team 4909 (Billerica, MA) mentorship philosophy.
- Mechanical coaching: CAD standards, drivetrain design, intake/shooter mechanisms, rapid prototyping.
- World Championship runs and regional accolades.
- Interactive Photo Gallery covering robots from 2018 to 2026 with lightbox zoom.

- [ ] **Step 2: Write `toolkit.html`**
Include:
- Homelab & Systems literacy: Raspberry Pi home cluster, Plex media server, custom VLANs & network routing.
- DIY Hardware Projects: Custom Onewheel mechatronics build with motor controller and battery pack design.
- Comprehensive Technical Skills Matrix (CAD, DFM, FEA, Rapid Prototyping, Embedded Firmware, Lab Equipment).
- Contact section (Email, LinkedIn, GitHub).
- High-visibility `Download Resume (PDF)` button linking to `assets/docs/ChrisJohnsonResume.docx.pdf`.

- [ ] **Step 3: Commit leadership & toolkit pages**
```bash
git add robotics.html toolkit.html
git commit -m "feat(pages): create detail pages for FIRST Robotics Team 4909 and Toolkit/Homelab"
```

---

### Task 8: End-to-End Testing, Polish & Verification

**Files:**
- Test all pages: `index.html`, `fuse-blast.html`, `upulse.html`, `unreleased-rd.html`, `mtg-counter.html`, `can-transceiver.html`, `robotics.html`, `toolkit.html`.

- [ ] **Step 1: Run local static server**
Run: `python -m http.server 8080`

- [ ] **Step 2: Verify page links, anchors, and responsive views**
Verify:
1. All anchor links scroll smoothly to target sections on `index.html`.
2. All card links navigate to the correct detail page.
3. All detail page back links return to `index.html`.
4. Lightbox works on all gallery images.
5. 3D CAD viewer renders and toggles individual parts properly.
6. All images load quickly as WebP with no 404s.
7. Resume download link delivers `ChrisJohnsonResume.docx.pdf`.

- [ ] **Step 3: Final Git Commit and Status Check**
Ensure git working tree is clean and all files are committed.
