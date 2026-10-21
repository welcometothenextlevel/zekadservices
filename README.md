# Zeka D-Services · website

Conversion website for Zeka D-Services, a family multiservice company in Chêne-Bourg (Geneva). It covers sanitaire & chauffage, nettoyage, déménagement, and rénovation & peinture, and it is built to receive Google Ads traffic.

**Live:** https://welcometothenextlevel.github.io/zekadservices/

| Page | URL |
|---|---|
| Home | https://welcometothenextlevel.github.io/zekadservices/ |
| Plombier | https://welcometothenextlevel.github.io/zekadservices/plombier-geneve/ |
| Chauffagiste | https://welcometothenextlevel.github.io/zekadservices/chauffagiste-geneve/ |
| Nettoyage | https://welcometothenextlevel.github.io/zekadservices/nettoyage-geneve/ |
| Fin de bail | https://welcometothenextlevel.github.io/zekadservices/nettoyage-fin-de-bail-geneve/ |
| Déménagement | https://welcometothenextlevel.github.io/zekadservices/demenagement-geneve/ |
| Rénovation et peinture | https://welcometothenextlevel.github.io/zekadservices/renovation-peinture-geneve/ |
| Thank-you (conversion) | https://welcometothenextlevel.github.io/zekadservices/merci/ |

The site is static HTML, CSS and vanilla JS: no framework, no build step to run it. Every path is relative, so it works in the GitHub Pages subfolder and on its own domain.

## Change the phone, WhatsApp, e-mail or form address

Everything is in **`js/config.js`**:

```js
PHONE_DISPLAY: "078 639 50 66",
PHONE_E164: "+41786395066",
WHATSAPP: "41786395066",
EMAIL: "zeka.ge.services@gmail.com",   // shown on the site AND receives every request
```

The pages update themselves from this file in the browser. For a new phone number, also change `PHONE`, `TEL` and `WA_NUM` at the top of `tools/build.py` and run the build, so the static HTML (what Google sees) matches.

### FormSubmit activation (once)

Requests are sent with FormSubmit's AJAX API to the `EMAIL` above. **The first submission does not arrive.** Instead, FormSubmit sends an activation e-mail to that address. Click "Activate form" in that e-mail once, and every later request is delivered as a table:

- the subject reads `Nouvelle demande · [service] · [localité]`
- the request also carries the gclid and UTM parameters

Do this again if you change the e-mail. If sending fails, visitors see the phone number and WhatsApp instead.

## Reviews and socials

The 3 Google reviews (5,0) live in **`js/reviews.js`**. `tools/build.py` writes them into every page, so they show without JavaScript and Google can read them. They appear in three places:
- a rating badge under the hero buttons
- the first item of the trust bar
- an "Avis clients" section right after the "Ce qui est inclus" list

To add or change a review, copy it word for word from Google into the list, update `rating` and `count`, then run `python3 tools/build.py`:

```js
window.ZEKA_GOOGLE = { "rating": 5.0, "count": 4, "url": "https://search.google.com/local/reviews?placeid=ChIJo5cPZFFvjEcRMiAn7vbA4j0", "maps": "https://maps.google.com/?cid=4459338747840241714" };
window.ZEKA_REVIEWS = [ { "name": "Prénom N.", "rating": 5, "service": "", "text": "Texte exact de l'avis." } ];
```

The file must stay strict JSON between `=` and `;`: double quotes and no trailing commas. An empty list hides every review element.

Link for asking happy customers to leave a review (send it on WhatsApp after a job): https://search.google.com/local/writereview?placeid=ChIJo5cPZFFvjEcRMiAn7vbA4j0

Facebook (`FACEBOOK` in `tools/build.py`) and Google appear as icons in the footer and in `sameAs` in the JSON-LD.

## Google Ads

In **`js/config.js`**:

```js
GOOGLE_ADS_ID: "AW-1234567890",
CONVERSION_LABELS: { lead: "AbC...", call: "DeF...", whatsapp: "GhI..." }
```

While `GOOGLE_ADS_ID` is empty, gtag is not loaded at all. These events are always pushed to `window.dataLayer`, so Google Tag Manager can use them too:

| Event | When | Ads conversion label |
|---|---|---|
| `call_click` | any tap on a phone link | `call` |
| `whatsapp_click` | any WhatsApp link | `whatsapp` |
| `generate_lead` | form sent successfully (just before the redirect) | none |
| `merci_view` | `merci/` page view. Converts only after a real submission, not on a reload | `lead` |
| `quote_cta_click`, `problem_select`, `rooms_select`, `form_step2`, `form_error` | micro-steps, useful for optimisation | none |

Every event carries:
- `service`: the `data-service` of the CTA, for example `plombier`, `fin-de-bail` or `demenagement-nettoyage`
- `placement`: for example `hero`, `header`, `mobile-bar` or `final`
- `page_service`

The `gclid`, `gbraid`, `wbraid` and `utm_*` parameters of the landing URL are kept for the visit in sessionStorage, and sent with every form.

## Edit the content

All pages are generated from **`tools/build.py`** (texts, FAQ, checklists, JSON-LD) and **`tools/site.css`** (the styles):

```
python3 tools/build.py          # writes every index.html, 404.html, css/site.css, sitemap.xml, robots.txt
python3 tools/build_images.py   # _src/stock-raw/*.jpg (originals, kept outside git) → img/stock/*.avif + *.webp
python3 tools/make_map.py       # canton map (tools/map.svg)
python3 tools/check_links.py https://welcometothenextlevel.github.io/zekadservices/   # every internal link and asset must answer 200
```

`tools/build.py` inlines the critical CSS (everything above the `CRITICAL END` marker in `tools/site.css`) into each page and writes the rest to `css/site.css`. Edit the source files, not the generated ones. Bump `V` in `tools/build.py` after a CSS or JS change to bust caches.

## Test locally

Serve the **parent** folder so the `/zekadservices/` subfolder behaves like GitHub Pages:

```
cd ..  &&  python3 -m http.server 4237
# open http://localhost:4237/zekadservices/
```

## Files

- `RESEARCH.md`: benchmark of Geneva and international landing pages, and the patterns reused
- `ASSETS.md`: old-site images (real vs stock), palette, fonts
- `CREDITS.md`: author and source of every photo, the videos and the map data
- `TODO-CONFIRM.md`: everything that needs the owner's confirmation before it can go on the site
