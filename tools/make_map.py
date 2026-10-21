#!/usr/bin/env python3
"""Draws the illustrated map of the canton of Geneva (tools/map.svg, inlined by build.py).
Boundary and lake from OpenStreetMap (Nominatim, ODbL), town points geocoded the same way."""
import json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
canton = json.load(open(ROOT / "_src/canton.json"))[0]["geojson"]
lake = json.load(open(ROOT / "_src/lake.json"))[0]["geojson"]
towns = json.load(open(ROOT / "_src/towns.json"))
LON0, LAT0, LON1, LAT1 = 5.94, 46.375, 6.325, 46.118
K = 1900
C = math.cos(math.radians(46.22))
def P(lon, lat):
    return ((lon - LON0) * C * K, (LAT0 - lat) * K)
W, H = P(LON1, LAT1)
def ring(pts, step=1):
    out = []
    for i, (lon, lat) in enumerate(pts):
        if i % step and i != len(pts) - 1:
            continue
        x, y = P(lon, lat)
        out.append(f"{x:.1f} {y:.1f}")
    return "M" + "L".join(out) + "Z"
cpath = "".join(ring(poly[0]) for poly in canton["coordinates"])
lcoords = lake["coordinates"] if lake["type"] == "Polygon" else lake["coordinates"][0]
# keep only lake points near the canton window to keep the path short
lpath = ring([p for p in lcoords[0]], 1)

# label placement tuned by hand: (dx, dy, anchor)
LABELS = {
    "Genève": (-9, -8, "end"), "Chêne-Bourg": (16, 6, "start"), "Chêne-Bougeries": (14, -10, "start"),
    "Thônex": (10, 19, "start"), "Carouge GE": (8, 17, "start"), "Lancy": (-7, -8, "end"), "Onex": (-8, 15, "end"),
    "Vernier": (-10, 4, "end"), "Meyrin": (-10, -6, "end"), "Plan-les-Ouates": (-8, 15, "end"),
    "Versoix": (-10, 4, "end"), "Cologny": (-10, -5, "end"), "Vandœuvres": (10, -7, "start"),
}
dots, labels = [], []
for name, (lat, lon) in towns.items():
    x, y = P(lon, lat)
    dx, dy, a = LABELS[name]
    shown = name.replace(" GE", "")
    base = name == "Chêne-Bourg"
    if base:
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" class="m-ring"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" class="m-base"/>')
        labels.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{a}" class="m-lab m-lab-base">{shown}</text>')
    else:
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" class="m-dot"/>')
        labels.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{a}" class="m-lab">{shown}</text>')

svg = (f'<svg class="map" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-labelledby="map-t">'
       '<title id="map-t">Carte du canton de Genève avec les communes où nous intervenons, depuis Chêne-Bourg</title>'
       f'<defs><clipPath id="m-clip"><path d="{cpath}"/></clipPath></defs>'
       f'<path d="{cpath}" class="m-canton"/>'
       f'<path d="{lpath}" class="m-lake" clip-path="url(#m-clip)"/>'
       f'<path d="{cpath}" class="m-edge"/>'
       f'<text x="{P(6.172,46.262)[0]:.0f}" y="{P(6.172,46.262)[1]:.0f}" class="m-water">Léman</text>'
       + "".join(dots) + "".join(labels) + '</svg>')
(ROOT / "tools/map.svg").write_text(svg)
print(len(svg), "bytes", f"{W:.0f}x{H:.0f}")
