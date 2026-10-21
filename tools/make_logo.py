"""Builds the SVG logo (wordmark as outlined paths, so it needs no font) and the favicons.
Run with a Python that has fontTools: python3 tools/make_logo.py"""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
NAVY, BLUE = "#0D2236", "#1480BA"

def outline(text, wght, size, x0, baseline, track=0.0):
    f = instantiateVariableFont(TTFont(ROOT / "fonts/archivo-latin.woff2"), {"wght": wght})
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    x = x0
    for ch in text:
        gn = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, x, baseline))
        gs[gn].draw(tp)
        x += hmtx[gn][0] * s + track * size
    return pen.getCommands(), x

# mark: navy tile, white Z whose bottom stroke is a water line in Zeka blue
MARK = (f'<rect x="0" y="0" width="44" height="44" rx="7" fill="{NAVY}"/>'
        '<path d="M12.5 13h19L13 30.2" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="square" stroke-linejoin="miter"/>'
        f'<path d="M11.5 31.6c3.4 0 3.4-2.4 6.8-2.4s3.4 2.4 6.8 2.4 3.4-2.4 6.8-2.4" fill="none" stroke="#5FB4E6" stroke-width="3.2" stroke-linecap="round"/>')

zeka, x1 = outline("Zeka", 760, 27, 56, 30.5, -0.01)
dsv, x2 = outline("D-Services", 560, 27, x1 + 6, 30.5, -0.005)
W = round(x2 + 2)

def logo(word1=NAVY, word2=BLUE, mark=MARK):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 44" width="{W}" height="44" role="img" aria-label="Zeka D-Services">'
            f'{mark}<path fill="{word1}" d="{zeka}"/><path fill="{word2}" d="{dsv}"/></svg>')

(ROOT / "img/brand/logo.svg").write_text(logo())
(ROOT / "img/brand/logo-white.svg").write_text(logo("#FFFFFF", "#9FC9E6", MARK.replace(f'fill="{NAVY}"', 'fill="#FFFFFF" fill-opacity=".08" stroke="#FFFFFF" stroke-opacity=".35"')))
(ROOT / "img/brand/mark.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44">{MARK}</svg>')
(ROOT / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44">{MARK}</svg>')
print("logo width", W)
