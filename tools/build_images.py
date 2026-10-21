#!/usr/bin/env python3
"""Converts the stock originals in _src/stock-raw/ into responsive AVIF + WebP files in img/stock/
and writes tools/images.json (widths + ratio) for build.py. Needs Pillow >= 11 with AVIF.

    python3 tools/build_images.py
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "stock-raw"
OUT = ROOT / "img" / "stock"
OUT.mkdir(parents=True, exist_ok=True)
WIDTHS = [480, 800, 1200, 1600]

manifest = {}
total = 0
for src in sorted(SRC.glob("*.jpg")):
    key = src.stem
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    ws = [w for w in WIDTHS if w <= im.width] or [im.width]
    for w in ws:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(OUT / f"{key}-{w}.webp", "WEBP", quality=70, method=6)
        r.save(OUT / f"{key}-{w}.avif", "AVIF", quality=52, speed=4)
        total += (OUT / f"{key}-{w}.webp").stat().st_size + (OUT / f"{key}-{w}.avif").stat().st_size
    manifest[f"stock/{key}"] = {"w": ws, "ratio": [im.width, im.height]}
    print(f"{key:28s} {im.width}x{im.height}  {(OUT / f'{key}-800.webp').stat().st_size // 1024 if 800 in ws else '-'} KB @800 webp")

(ROOT / "tools" / "images.json").write_text(json.dumps(manifest, indent=1))
print(f"total {total // 1024} KB")
