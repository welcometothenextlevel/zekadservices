# Assets

## Images from the current site (`img/original/`)

We downloaded every image from zekadservices.ch and opened each one. **None of them is a real company photo.** They are all stock or clip-art.

| File | What it shows | Verdict |
|---|---|---|
| `logo.png`, `zds-0.png`, `fb-logo.jpg` | The old logo: 3D clip-art figures carrying a house into a van, plus a cartoon cleaner, above the name "Zeka D-Services" in blue `#3980BA` | **Not reused.** At 175 px it is too small for a header. The cleaner figure carries a visible stock watermark, so it is unlicensed clip-art. We redrew the logo as `img/brand/logo.svg`: the same name and blue, plus a navy "Z" mark whose base stroke is a water line. |
| `zds-2.jpg` | Hand turning a thermostatic radiator valve | Stock from the Duda/localsearch library (licence tied to that site) |
| `zds-3.jpg`, `zds-9.jpg` | Two movers unloading a box truck; truck full of boxes | Same library |
| `zds-4.jpg` | Bucket of cleaning products (used on the old *moving* card) | Same library, wrong service |
| `zds-5.jpg` | Vacuum on a building site (used on the old *sanitaire* card) | Same library, wrong service |
| `zds-6.jpg`, `zds-7.jpg`, `zds-8.jpg`, `zds-11.jpg` | Cleaning a wall, steam-cleaning a sofa, wiping a hob, spraying a counter | Same library |
| `zds-10.jpg` | Heating engineer at a radiator | Same library |
| `zds-12.jpg`, `zds-13.jpg` | Brush on purple wood; brush on a colour fan | Same library |
| `pexels-7859953.jpg` | Hands on a boiler circulator pump | **Pexels, free licence. Reused** as `stock/chaudiere-pompe` (heating page) |
| `pexels-159045.jpg` | Paint samples and colour fan on a plan | **Pexels, free licence. Reused** as `stock/nuancier` (renovation page) |

The `zds-*` files came with the localsearch/Duda template and we cannot confirm a licence that covers a new site. We kept them in `img/original/` for reference only, and the new pages do not use them.

## New stock (`img/stock/`, `video/`)

There are 37 photos and 2 videos, all from Pexels or Unsplash under free licences. Every file was downloaded locally and opened. We rejected anything AI-looking, watermarked, branded or off-topic, for example a branded "ECO CLEAN" bathroom shot, a "MOVING COMPANY" van and render-like luxury bathrooms. We chose European-looking interiors: parquet, panel radiators, wall-hung WCs. Sources and authors are in CREDITS.md and on `mentions-legales/#credits`.

Each photo is exported as AVIF + WebP at 480, 800, 1200 and 1600 px with Pillow (`tools/build_images.py`), and served with `srcset`/`sizes` and explicit width/height.

Videos: two 10-second loops, muted, H.264 MP4 + VP9 WebM, 1280 px, 0.3 to 1.1 MB each, each with a poster image.
- **Sanitaire hero:** a hand closing the valve under a sink.
- **Nettoyage hero:** a professional mopping a floor.

They only load on screens of 960 px and wider, on a fast connection, and when reduced motion is off. Otherwise the poster stays.

## Brand

| Token | Hex | Use |
|---|---|---|
| Zeka blue | `#1480BA` | Structure: icons, rules, progress bar, ticks (from the old site's buttons) |
| Blue (text) | `#0B6496` | Links (5.8:1 on the off-white) |
| Navy | `#0D2236` | Authority: hero, header buttons, footer (14.7:1 with the off-white) |
| Orange | `#C84B0C` | **Call buttons only** (white text 4.7:1) |
| WhatsApp green | `#157A45` | WhatsApp buttons (white text 5.4:1) |
| Off-white | `#F7F4EE` / `#EEE8DD` | Warm backgrounds |
| Ink / muted | `#15202B` / `#56616C` | Body text (muted 5.8:1) |

Every text and button pair passes WCAG AA, and Lighthouse accessibility scores 100.

Fonts: Archivo (headings, semi-condensed 87.5 %) and Source Sans 3 (body, 18 px, line-height 1.55), self-hosted.

Signature details, used sparingly:
- a thin water line above section titles on the plumbing and heating pages (also the base of the logo mark)
- a small sparkle on the cleaning pages and as the cleaning checklist bullet
