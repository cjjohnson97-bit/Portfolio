import os
import shutil
from pathlib import Path
from PIL import Image
import imageio.v3 as iio
import fitz  # PyMuPDF

ROOT_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = ROOT_DIR / "Resources"
IMG_DIR = ROOT_DIR / "assets" / "img"
DOCS_DIR = ROOT_DIR / "assets" / "docs"

IMG_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

def convert_image(src_path: Path, dest_name: str, max_size=(1920, 1920), quality=85):
    dest_path = IMG_DIR / f"{dest_name}.webp"
    with Image.open(src_path) as img:
        img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(dest_path, "WEBP", quality=quality, method=6)
    print(f"Converted {src_path.name} -> {dest_path.name} ({dest_path.stat().st_size / 1024:.1f} KB)")

def convert_pdf_page(pdf_path: Path, dest_name: str, page_num=0, dpi=200):
    dest_path = IMG_DIR / f"{dest_name}.webp"
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    img.save(dest_path, "WEBP", quality=85, method=6)
    doc.close()
    print(f"Rendered {pdf_path.name} [p{page_num}] -> {dest_path.name} ({dest_path.stat().st_size / 1024:.1f} KB)")

def convert_video_to_animated_webp(video_path: Path, dest_name: str, duration_sec=3.5, target_fps=15, max_width=640):
    dest_path = IMG_DIR / f"{dest_name}.webp"
    print(f"Converting video {video_path.name} to animated WebP...")
    
    # Read video frames
    frames = []
    fps = None
    try:
        meta = iio.immeta(video_path, plugin="pyav")
        fps = meta.get("fps", 30)
    except Exception:
        fps = 30
        
    step = max(1, int(fps / target_fps))
    max_frames = int(duration_sec * target_fps)
    
    count = 0
    collected = 0
    for frame in iio.imiter(video_path):
        if count % step == 0:
            pil_img = Image.fromarray(frame)
            w, h = pil_img.size
            if w > max_width:
                new_h = int(h * (max_width / w))
                pil_img = pil_img.resize((max_width, new_h), Image.Resampling.LANCZOS)
            frames.append(pil_img)
            collected += 1
            if collected >= max_frames:
                break
        count += 1

    if frames:
        duration_per_frame = int(1000 / target_fps)
        frames[0].save(
            dest_path,
            "WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration_per_frame,
            loop=0,
            quality=80,
            method=4
        )
        print(f"Created animated WebP: {dest_path.name} ({dest_path.stat().st_size / 1024:.1f} KB, {len(frames)} frames)")

def main():
    # 1. Standard Images
    image_mappings = {
        "Fuse-Blast.webp": "fuse-blast-hero",
        "uPulse.jpg": "upulse-hero",
        "CanTransceiverFundamentalCircuit.PNG": "can-circuit",
        "MTG ExplodeView.PNG": "mtg-explode",
        "MTG LifeCounters.jpg": "mtg-lifecounters",
        "2018-GEMS.PNG": "robot-2018",
        "2019-gems.jpeg": "robot-2019",
        "Robot2022.jpg": "robot-2022",
        "Robot2023.jpg": "robot-2023",
        "Robot2024.jpg": "robot-2024",
        "Robot2025.JPG": "robot-2025",
        "Robot2026.jpg": "robot-2026",
        "Onewheel_Homemade.jpg": "onewheel"
    }

    for src_file, dest_name in image_mappings.items():
        src_path = RESOURCES_DIR / src_file
        if src_path.exists():
            convert_image(src_path, dest_name)
        else:
            print(f"Warning: {src_file} not found in Resources")

    # 2. PDF Previews
    can_pdf = RESOURCES_DIR / "CanHack_Schematic.pdf"
    if can_pdf.exists():
        convert_pdf_page(can_pdf, "can-schematic", page_num=0)

    # 3. Animated WebP from MP4
    mp4_path = RESOURCES_DIR / "MTG Counter.mp4"
    if mp4_path.exists():
        convert_video_to_animated_webp(mp4_path, "mtg-counter-loop", duration_sec=3.0, target_fps=15, max_width=640)

    # 4. Copy PDFs to docs
    for doc in ["CanHack_Schematic.pdf"]:
        src_doc = RESOURCES_DIR / doc
        if src_doc.exists():
            dest_doc = DOCS_DIR / doc
            shutil.copy2(src_doc, dest_doc)
            print(f"Copied doc {doc} -> {dest_doc.name}")

if __name__ == "__main__":
    main()
