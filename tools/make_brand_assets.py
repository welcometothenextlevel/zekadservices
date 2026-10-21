#!/usr/bin/env python3
"""Renders the raster brand assets with headless Chrome + Pillow:
favicon.ico, apple-touch-icon.png, icon-512.png, img/brand/logo.png and img/og-share.jpg."""
import subprocess, tempfile
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
U = ROOT.as_uri()

def shot(html, w, h, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ROOT / "_src") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    f"--window-size={w},{h}", "--force-device-scale-factor=1", f"--screenshot={out}", Path(f.name).as_uri()],
                   capture_output=True)
    Path(f.name).unlink()

mark = (ROOT / "img/brand/mark.svg").read_text()
shot(f'<body style="margin:0;background:#0D2236">{mark.replace("<svg ", "<svg width=512 height=512 ")}</body>', 512, 512, ROOT / "_src/icon-512.png")
im = Image.open(ROOT / "_src/icon-512.png").convert("RGBA")
im.save(ROOT / "icon-512.png")
im.resize((180, 180), Image.LANCZOS).save(ROOT / "apple-touch-icon.png")
im.resize((192, 192), Image.LANCZOS).save(ROOT / "icon-192.png")
im.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

logo = (ROOT / "img/brand/logo.svg").read_text().replace('width="244" height="44"', 'width="732" height="132"')
shot(f'<body style="margin:0;background:#fff;padding:34px">{logo}</body>', 800, 200, ROOT / "_src/logo.png")
Image.open(ROOT / "_src/logo.png").convert("RGB").save(ROOT / "img/brand/logo.png", optimize=True)

og = f"""<html><head><style>
@font-face{{font-family:A;src:url({U}/fonts/archivo-latin.woff2)}}@font-face{{font-family:S;src:url({U}/fonts/source-sans-3-latin.woff2)}}
body{{margin:0;width:1200px;height:630px;display:grid;grid-template-columns:640px 560px;background:#0D2236;font-family:S}}
.l{{padding:64px 56px;display:flex;flex-direction:column;justify-content:space-between;color:#fff}}
h1{{font:700 54px/1.05 A;letter-spacing:-.02em;margin:28px 0 18px}}p{{font-size:26px;color:#C9D8E4;margin:0}}
.t{{font:700 34px A;color:#fff}}.t span{{display:inline-block;background:#C84B0C;padding:10px 20px;border-radius:6px}}
.r{{background:url({U}/img/stock/plombier-evier-1200.webp) center/cover}}
</style></head><body><div class="l"><div>{(ROOT / "img/brand/logo-white.svg").read_text().replace('width="244" height="44"', 'width="366" height="66"')}
<h1>Sanitaire, chauffage, nettoyage et déménagement à Genève</h1><p>Entreprise familiale à Chêne-Bourg · Devis gratuit</p></div>
<div class="t"><span>078 639 50 66</span></div></div><div class="r"></div></body></html>"""
shot(og, 1200, 630, ROOT / "_src/og.png")
Image.open(ROOT / "_src/og.png").convert("RGB").save(ROOT / "img/og-share.jpg", quality=84, optimize=True, progressive=True)
print("ok")
