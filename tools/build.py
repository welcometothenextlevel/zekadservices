#!/usr/bin/env python3
"""Generates every page of the Zeka D-Services site, plus css/site.css, sitemap.xml and robots.txt.

The output is plain static HTML (no build step is needed to *run* the site). This script only
keeps the shared parts (header, quote form, footer, contact bar) identical on every page.
Edit texts here, then run:

    python3 tools/build.py

Every link is relative, so the site works in the GitHub Pages subfolder
(https://<user>.github.io/zekadservices/) and on its own domain without changes.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://welcometothenextlevel.github.io/zekadservices/"  # change when the site moves to zekadservices.ch
V = "3"  # cache-busting version for css/js

IMG = json.loads((ROOT / "tools" / "images.json").read_text())
MAP_SVG = (ROOT / "tools" / "map.svg").read_text()

PHONE = "078 639 50 66"
TEL = "tel:+41786395066"
WA_NUM = "41786395066"
ADDRESS = ("Avenue de Bel-Air 61 ter", "1225", "Chêne-Bourg")
GEO = (46.20198, 6.20005)
TOWNS = ["Genève", "Chêne-Bourg", "Chêne-Bougeries", "Thônex", "Carouge", "Lancy", "Onex", "Vernier",
         "Meyrin", "Plan-les-Ouates", "Versoix", "Cologny", "Vandœuvres"]
SERVICES = ["Sanitaire", "Chauffage", "Nettoyage", "Fin de bail", "Déménagement", "Rénovation / peinture", "Autre"]
ROOMS = ["Studio", "2", "2.5", "3", "3.5", "4", "4.5", "5+"]


def esc(s):
    return html.escape(s, quote=True)


def wa(text):
    q = re.sub(r"[^A-Za-z0-9\-_.~]", lambda m: "".join("%%%02X" % b for b in m.group(0).encode()), text)
    return f"https://wa.me/{WA_NUM}?text={q}"


# ------------------------------------------------------------------ icons
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M6.6 3.8h2.6l1.5 3.9-1.9 1.2a10.6 10.6 0 0 0 5.3 5.3l1.2-1.9 3.9 1.5v2.6a2 2 0 0 1-2.1 2A14.6 14.6 0 0 1 4.6 5.9a2 2 0 0 1 2-2.1z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path stroke="none" fill="currentColor" d="M12.04 2.5a9.43 9.43 0 0 0-8.1 14.24L2.6 21.5l4.88-1.28a9.43 9.43 0 1 0 4.56-17.72zm0 17.26a7.8 7.8 0 0 1-3.98-1.09l-.29-.17-2.9.76.78-2.83-.19-.3a7.82 7.82 0 1 1 6.58 3.63zm4.29-5.86c-.24-.12-1.4-.69-1.61-.77-.22-.08-.38-.12-.54.12-.16.24-.62.77-.76.93-.14.16-.28.18-.52.06-.24-.12-1-.37-1.91-1.18-.7-.63-1.18-1.41-1.32-1.65-.14-.24-.01-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.2-.47-.4-.4-.54-.41h-.46a.89.89 0 0 0-.64.3 2.7 2.7 0 0 0-.84 2c0 1.18.86 2.32.98 2.48.12.16 1.69 2.58 4.1 3.62.57.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.4-.57 1.6-1.13.2-.55.2-1.03.14-1.13-.06-.1-.22-.16-.46-.28z"/></symbol>
<symbol id="i-family" viewBox="0 0 24 24"><circle cx="12" cy="6.4" r="2.6"/><circle cx="5.6" cy="8.4" r="2.1"/><circle cx="18.4" cy="8.4" r="2.1"/><path d="M7.2 20.2c.4-4.1 2.2-6.6 4.8-6.6s4.4 2.5 4.8 6.6"/><path d="M2.4 18.6c.3-3 1.6-4.7 3.4-4.7.9 0 1.6.3 2.2.9M21.6 18.6c-.3-3-1.6-4.7-3.4-4.7-.9 0-1.6.3-2.2.9"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21.2s-6.6-5.7-6.6-11.1a6.6 6.6 0 0 1 13.2 0c0 5.4-6.6 11.1-6.6 11.1z"/><circle cx="12" cy="10.1" r="2.4"/></symbol>
<symbol id="i-doc" viewBox="0 0 24 24"><path d="M6.2 3.4h7.9l4.6 4.6v12.6H6.2z"/><path d="M13.9 3.5v4.7h4.7M9.2 12.4h6.4M9.2 15.9h6.4"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M5.2 5.2h13.6a1.6 1.6 0 0 1 1.6 1.6v8.6a1.6 1.6 0 0 1-1.6 1.6H10l-4.6 3.4V17H5.2a1.6 1.6 0 0 1-1.6-1.6V6.8a1.6 1.6 0 0 1 1.6-1.6z"/><path d="M7.6 9.6h8.8M7.6 12.8h5.4"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M4.8 12.6l4.4 4.3L19.2 7"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4.8 12h14.2M13.4 6.2l5.8 5.8-5.8 5.8"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path d="M6.4 9.2l5.6 5.6 5.6-5.6"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3.4" y="5.4" width="17.2" height="13.2" rx="2"/><path d="M4.2 7.2l7.8 6 7.8-6"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3.4s6.2 6.5 6.2 10.8a6.2 6.2 0 0 1-12.4 0C5.8 9.9 12 3.4 12 3.4z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.6 2.6"/></symbol>
<symbol id="i-flame" viewBox="0 0 24 24"><path d="M12 21c-3.8 0-6.6-2.7-6.6-6.3 0-4.4 4.2-6.5 4.8-11.2 2.9 1.9 4.5 4.6 4.5 7.4.9-.5 1.6-1.6 1.8-2.9 1.4 1.5 2.1 3.5 2.1 5.4 0 4.1-2.8 7.6-6.6 7.6z"/><path d="M12 21c-1.7 0-2.9-1.2-2.9-2.9 0-1.9 1.7-2.9 2.3-4.8 1.6 1 2.9 2.6 2.9 4.5 0 1.9-.8 3.2-2.3 3.2z"/></symbol>
<symbol id="i-radiator" viewBox="0 0 24 24"><rect x="3.6" y="5.2" width="3.4" height="13" rx="1.7"/><rect x="8.6" y="5.2" width="3.4" height="13" rx="1.7"/><rect x="13.6" y="5.2" width="3.4" height="13" rx="1.7"/><path d="M17 9h3.4M5.2 18.2v1.6M15.4 18.2v1.6"/></symbol>
<symbol id="i-boiler" viewBox="0 0 24 24"><rect x="6.2" y="2.8" width="11.6" height="14.4" rx="2"/><circle cx="12" cy="11" r="2.2"/><path d="M9.2 6.2h5.6M9.6 17.2v3.6M14.4 17.2v3.6"/></symbol>
<symbol id="i-wrench" viewBox="0 0 24 24"><path d="M14.6 6.3a1 1 0 0 0 0 1.4l1.7 1.7a1 1 0 0 0 1.4 0l3.4-3.4a5.9 5.9 0 0 1-7.8 7.8l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a5.9 5.9 0 0 1 7.8-7.8z"/></symbol>
<symbol id="i-shower" viewBox="0 0 24 24"><path d="M5 21V7.6a4 4 0 0 1 7.6-1.8"/><path d="M10.2 8.8a4.4 4.4 0 0 1 7.2 0z"/><path d="M11.4 12.2l-.6 1.4M13.8 12.2v1.6M16.2 12.2l.6 1.4M11 16.4l-.6 1.4M14 16.4v1.6M17 16.4l.6 1.4"/></symbol>
<symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 2.8c.7 4.8 2.6 6.7 7.4 7.4-4.8.7-6.7 2.6-7.4 7.4-.7-4.8-2.6-6.7-7.4-7.4 4.8-.7 6.7-2.6 7.4-7.4z"/><path d="M18.6 16.4c.3 1.7 1 2.4 2.6 2.6-1.7.3-2.4 1-2.6 2.6-.3-1.7-1-2.4-2.6-2.6 1.7-.2 2.4-.9 2.6-2.6z"/></symbol>
<symbol id="i-kitchen" viewBox="0 0 24 24"><rect x="4" y="3.4" width="16" height="17.2" rx="1.6"/><path d="M4 8.2h16M7.6 5.8h.01M10.6 5.8h.01"/><rect x="7" y="11.2" width="10" height="6.2" rx="1"/></symbol>
<symbol id="i-bath" viewBox="0 0 24 24"><path d="M3.4 12.4h17.2v2.4a4.2 4.2 0 0 1-4.2 4.2H7.6a4.2 4.2 0 0 1-4.2-4.2z"/><path d="M6 12.4V6.2a2.2 2.2 0 0 1 4.1-1.1M7 19l-.9 1.8M17 19l.9 1.8"/></symbol>
<symbol id="i-window" viewBox="0 0 24 24"><rect x="4.2" y="3.6" width="15.6" height="16.8" rx="1.4"/><path d="M12 3.6v16.8M4.2 12h15.6"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3.8 11.2L12 4.6l8.2 6.6M6.2 9.4v10.4h11.6V9.4M10 19.8v-5h4v5"/></symbol>
<symbol id="i-building" viewBox="0 0 24 24"><path d="M5 20.4V4.6h9.4v15.8M14.4 9.4H19v11M3.4 20.4h17.2"/><path d="M8 8h3.4M8 11.4h3.4M8 14.8h3.4"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24"><path d="M2.8 6.4h11v10H2.8zM13.8 9.6h3.8l2.9 3.2v3.6h-6.7"/><circle cx="6.6" cy="17.6" r="1.9"/><circle cx="16.8" cy="17.6" r="1.9"/></symbol>
<symbol id="i-box" viewBox="0 0 24 24"><path d="M3.6 7.6L12 3.4l8.4 4.2v8.8L12 20.6l-8.4-4.2z"/><path d="M3.6 7.6L12 11.8l8.4-4.2M12 11.8v8.8M7.8 5.5l8.4 4.2"/></symbol>
<symbol id="i-roller" viewBox="0 0 24 24"><rect x="3.6" y="3.4" width="13.2" height="5.2" rx="1.2"/><path d="M16.8 6h2.8v4.8H11.2v3.2"/><rect x="9.8" y="14" width="2.8" height="6.8" rx="1"/></symbol>
<symbol id="i-key" viewBox="0 0 24 24"><circle cx="8" cy="15.6" r="4.2"/><path d="M11 12.6l8.6-8.6M16.2 7.4l2.4 2.4M13.8 9.8l2 2"/></symbol>
<symbol id="i-cal" viewBox="0 0 24 24"><rect x="3.8" y="5.4" width="16.4" height="14.8" rx="2"/><path d="M3.8 10h16.4M8.4 3.4v4M15.6 3.4v4"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><rect x="3.4" y="7" width="17.2" height="12.4" rx="2"/><circle cx="12" cy="13.2" r="3.4"/><path d="M8.6 7l1.6-2.6h3.6L15.4 7"/></symbol>
<symbol id="i-lock" viewBox="0 0 24 24"><rect x="5" y="10.4" width="14" height="10" rx="2"/><path d="M8 10.4V7.8a4 4 0 0 1 8 0v2.6"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-back" viewBox="0 0 24 24"><path d="M19.2 12H5M10.6 6.2L4.8 12l5.8 5.8"/></symbol>
</defs></svg>"""


def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


WLINE = ('<svg class="wline" viewBox="0 0 120 14" aria-hidden="true"><path d="M1 7c7.4 0 7.4-5 14.8-5s7.4 5 14.8 5 '
         '7.4-5 14.8-5 7.4 5 14.8 5 7.4-5 14.8-5 7.4 5 14.8 5 7.4-5 14.8-5 7.4 5 14.8 5"/></svg>')
SPARK = ('<svg class="wline" viewBox="0 0 120 14" aria-hidden="true"><path d="M1 7h74"/>'
         '<path style="fill:currentColor;stroke:none" d="M88 0c.5 4.3 2.2 6 6.5 6.5-4.3.5-6 2.2-6.5 6.5-.5-4.3-2.2-6-6.5-6.5 4.3-.5 6-2.2 6.5-6.5z'
         'M104 3.5c.3 2.3 1.2 3.2 3.5 3.5-2.3.3-3.2 1.2-3.5 3.5-.3-2.3-1.2-3.2-3.5-3.5 2.3-.3 3.2-1.2 3.5-3.5z"/></svg>')


# ------------------------------------------------------------------ images
BLANK = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="


def srcset(rel, key, ext):
    return ", ".join(f"{rel}img/{key}-{w}.{ext} {w}w" for w in IMG[key]["w"])


def pic(rel, key, alt, sizes, eager=False, cls=""):
    info = IMG[key]
    ws = info["w"]
    w0, h0 = info["ratio"]
    big = max(ws)
    h = round(h0 * big / w0)
    mid = min(ws, key=lambda w: abs(w - 800))
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{srcset(rel, key, "avif")}" sizes="{sizes}">'
            f'<img src="{rel}img/{key}-{mid}.webp" srcset="{srcset(rel, key, "webp")}" sizes="{sizes}" '
            f'width="{big}" height="{h}" alt="{esc(alt)}" {load}{c}></picture>')


def desktop_pic(rel, key):
    """Hero image: loaded on screens >= 960px only (hidden on phones, where text is the LCP)."""
    return (f'<picture><source media="(min-width: 960px)" type="image/avif" srcset="{srcset(rel, key, "avif")}" sizes="62vw">'
            f'<source media="(min-width: 960px)" type="image/webp" srcset="{srcset(rel, key, "webp")}" sizes="62vw">'
            f'<img src="{BLANK}" alt="" width="1600" height="1000" fetchpriority="high" decoding="async"></picture>')


def frame(rel, key, alt, sizes, ratio="43", cap=None):
    c = f'<figcaption class="cap">{cap}</figcaption>' if cap else ""
    return f'<figure style="margin:0"><div class="frame frame--{ratio}">{pic(rel, key, alt, sizes)}</div>{c}</figure>'


# ------------------------------------------------------------------ buttons
def b_call(svc, loc, label=None, cls="btn btn-call"):
    label = label or f'Appeler <span class="nw" data-phone>{PHONE}</span>'
    return f'<a class="{cls}" href="{TEL}" data-service="{svc}" data-loc="{loc}">{ic("phone")}<span>{label}</span></a>'


def b_wa(svc, loc, text, label="Écrire sur WhatsApp", cls="btn btn-wa"):
    return (f'<a class="{cls}" href="{wa(text)}" target="_blank" rel="noopener" data-service="{svc}" data-loc="{loc}">'
            f'{ic("wa")}<span>{label}</span></a>')


def b_quote(svc, loc, label="Obtenir mon devis gratuit", cls="btn btn-quote"):
    return f'<a class="{cls}" href="#devis" data-service="{svc}" data-loc="{loc}">{ic("doc")}<span>{label}</span></a>'


def cta_row(svc, loc, watext, quote="Obtenir mon devis", call="Appeler maintenant", wa_label="Écrire sur WhatsApp", order="qcw"):
    parts = {"q": b_quote(svc, loc, quote), "c": b_call(svc, loc, call), "w": b_wa(svc, loc, watext, wa_label)}
    return '<div class="cta-row">' + "".join(parts[k] for k in order) + "</div>"


# ------------------------------------------------------------------ quote form
def chips(name, values, cls="", req=False, checked=None):
    out = []
    for v in values:
        lab = "Studio" if v == "Studio" else (v if name != "pieces" else f"{v}<span class=sr> pièces</span>")
        ch = " checked" if checked == v else ""
        out.append(f'<label class="chip"><input type="radio" name="{name}" value="{esc(v)}"{ch}><span>{lab}</span></label>')
    return f'<div class="chips {cls}">{"".join(out)}</div>'


ATTR_FIELDS = "".join(f'<input type="hidden" name="{k}">' for k in
                      ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "landing_page"])
DATALIST = '<datalist id="towns">' + "".join(f'<option value="{t}">' for t in TOWNS) + "</datalist>"


def quote_form(svc_slug, default=None, watext="Bonjour, je souhaite un devis."):
    return f"""<form class="qf" id="quote-form" novalidate data-step="1" data-service="{svc_slug}" aria-labelledby="qf-title">
<div class="qf-head"><h2 class="qf-title" id="qf-title" tabindex="-1">Devis gratuit</h2><p class="qf-steplabel" aria-live="polite">Étape <b>1</b> sur 2</p></div>
<div class="qf-bar" aria-hidden="true"><span></span></div>
<fieldset class="qf-step" data-step="1">
<legend>Pour quel service&nbsp;?</legend>
{chips("service", SERVICES, checked=default)}
<p class="err qf-step1-err" role="alert"></p>
<div class="qf-cond" data-for="Fin de bail" hidden>
<p class="qf-sub" id="qf-rooms">Taille du logement</p>
<div role="radiogroup" aria-labelledby="qf-rooms">{chips("pieces", ROOMS, "chips--rooms")}</div>
<div class="field" style="margin-top:14px"><label for="qf-date">Date de l’état des lieux <span class="opt">(si connue)</span></label><input id="qf-date" name="date" type="date"></div>
</div>
<div class="qf-cond" data-for="Déménagement" hidden>
<div class="field" style="margin-top:14px"><label for="qf-date2">Date du déménagement <span class="opt">(si connue)</span></label><input id="qf-date2" name="date_demenagement" type="date"></div>
</div>
<div class="qf-cond" data-for="Sanitaire|Chauffage" hidden>
<p class="qf-sub" id="qf-urg">Est-ce urgent&nbsp;?</p>
<div role="radiogroup" aria-labelledby="qf-urg">{chips("urgent", ["Oui", "Non"], "chips--yn")}</div>
</div>
<button type="button" class="btn btn-quote btn-block qf-next" style="margin-top:18px">Continuer{ic("arrow")}</button>
</fieldset>
<fieldset class="qf-step" data-step="2" hidden>
<legend>Vos coordonnées</legend>
<div class="field"><label for="qf-nom">Nom et prénom</label><input id="qf-nom" name="nom" type="text" autocomplete="name" required aria-describedby="qf-nom-e"><span class="err" id="qf-nom-e"></span></div>
<div class="field"><label for="qf-tel">Téléphone</label><input id="qf-tel" name="telephone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="078 123 45 67" aria-describedby="qf-tel-e"><span class="err" id="qf-tel-e"></span></div>
<div class="field"><label for="qf-loc">Localité <span class="opt">(commune)</span></label><input id="qf-loc" name="localite" type="text" list="towns" autocomplete="address-level2" placeholder="Ex. Thônex"></div>
<div class="field"><label for="qf-mail">E-mail <span class="opt">(facultatif)</span></label><input id="qf-mail" name="email" type="email" inputmode="email" autocomplete="email" aria-describedby="qf-mail-e"><span class="err" id="qf-mail-e"></span></div>
<div class="field"><label for="qf-msg">Votre message <span class="opt">(facultatif)</span></label><textarea id="qf-msg" name="message" rows="3" placeholder="Décrivez en quelques mots ce dont vous avez besoin."></textarea></div>
<p class="qf-photo">{ic("camera")}<span>Plus rapide&nbsp;: envoyez une photo sur <a href="{wa(watext)}" target="_blank" rel="noopener" data-service="{svc_slug}" data-loc="form-photo">WhatsApp</a>.</span></p>
<input type="hidden" name="probleme">{ATTR_FIELDS}
<div class="hp" aria-hidden="true"><label>Ne pas remplir ce champ<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
<div class="qf-actions"><button type="button" class="qf-back">{ic("back")}<span class="sr">Retour à l’étape 1</span></button><button type="submit" class="btn btn-quote">Envoyer ma demande</button></div>
<p class="qf-status" role="status" aria-live="polite"></p>
</fieldset>
<p class="qf-reassure">{ic("lock")}Gratuit et sans engagement · Vos données restent confidentielles</p>
{DATALIST}
</form>"""


def callback_form(svc_slug, default):
    opts = "".join(f'<option{" selected" if s == default else ""}>{esc(s)}</option>' for s in SERVICES)
    return f"""<form class="cb" id="callback-form" novalidate data-service="{svc_slug}" aria-labelledby="cb-title">
<h3 class="qf-title" id="cb-title">Être rappelé</h3>
<p class="cb-sub">Laissez votre numéro, nous vous rappelons pour fixer les détails.</p>
<div class="field"><label for="cb-svc">Service</label><select id="cb-svc" name="service">{opts}</select></div>
<div class="field"><label for="cb-nom">Nom</label><input id="cb-nom" name="nom" type="text" autocomplete="name" required aria-describedby="cb-nom-e"><span class="err" id="cb-nom-e"></span></div>
<div class="field"><label for="cb-tel">Téléphone</label><input id="cb-tel" name="telephone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="078 123 45 67" aria-describedby="cb-tel-e"><span class="err" id="cb-tel-e"></span></div>
<input type="hidden" name="type" value="Demande de rappel">{ATTR_FIELDS}
<div class="hp" aria-hidden="true"><label>Ne pas remplir ce champ<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
<button type="submit" class="btn btn-quote btn-block">Me rappeler</button>
<p class="qf-status" role="status" aria-live="polite"></p>
<p class="qf-reassure">{ic("lock")}Gratuit et sans engagement</p>
</form>"""


# ------------------------------------------------------------------ shared blocks
TRUST3 = [("family", "Entreprise familiale, 3 frères"), ("pin", "Tout le canton de Genève"), ("doc", "Devis gratuit")]
TRUSTBAR = [("family", "Entreprise familiale"), ("pin", "Tout Genève"), ("doc", "Devis gratuit"), ("chat", "Appel ou WhatsApp")]


def trust3():
    return '<ul class="trust3">' + "".join(f"<li>{ic(i)}{t}</li>" for i, t in TRUST3) + "</ul>"


def trustbar():
    return '<div class="tbar"><div class="wrap"><ul>' + "".join(f"<li>{ic(i)}{t}</li>" for i, t in TRUSTBAR) + "</ul></div></div>"


PROBLEMS = [("Fuite d’eau", "Sanitaire", True, "drop"), ("WC bouché", "Sanitaire", True, "wrench"),
            ("Plus d’eau chaude", "Sanitaire", True, "shower"), ("Chaudière en panne", "Chauffage", True, "flame"),
            ("Radiateur froid", "Chauffage", False, "radiator"), ("Boiler", "Sanitaire", False, "boiler")]


def problem_chips(svc):
    btns = "".join(
        f'<button type="button" class="pb-chip" data-problem="{esc(p)}" data-svc="{s}"{" data-urgent" if u else ""} aria-pressed="false">{ic(i)}{p}</button>'
        for p, s, u, i in PROBLEMS)
    return f"""<div class="pb"><p class="pb-q" id="pb-q">Votre problème&nbsp;?</p>
<div class="pb-list" role="group" aria-labelledby="pb-q">{btns}</div>
<div class="pb-panel" id="pb-panel" hidden aria-live="polite"><p><b class="pb-what"></b>&nbsp;: c’est noté dans votre demande. Pour aller plus vite, appelez-nous directement.</p>
<div class="btns">{b_call(svc, "problem-panel", "Appeler maintenant")}<button type="button" class="btn btn-light" id="pb-continue">Continuer mon devis{ic("arrow")}</button></div></div></div>"""


def room_chips():
    btns = "".join(f'<button type="button" class="pb-chip" data-rooms="{r}">{"Studio" if r == "Studio" else r + " pièces"}</button>' for r in ROOMS)
    return f'<div class="pb"><p class="pb-q" id="rooms-q">Votre logement&nbsp;?</p><div class="pb-list" role="group" aria-labelledby="rooms-q">{btns}</div></div>'


def hero(p, rel):
    media = ""
    if p.get("video"):
        vkey = p["video"]
        media = (f'<div class="hero-media" aria-hidden="true">{desktop_pic(rel, p["hero_img"])}'
                 f'<video muted playsinline loop preload="none" tabindex="-1">'
                 f'<source data-src="{rel}video/{vkey}.webm" type="video/webm">'
                 f'<source data-src="{rel}video/{vkey}.mp4" type="video/mp4"></video></div>')
    elif p.get("hero_img"):
        media = f'<div class="hero-media" aria-hidden="true">{desktop_pic(rel, p["hero_img"])}</div>'
    svc = p["slug"]
    if p.get("call_first"):
        ctas = b_call(svc, "hero", cls="btn btn-call btn-lg") + b_quote(svc, "hero", "Recevoir mon devis gratuit", "btn btn-quote btn-lg")
    else:
        ctas = b_quote(svc, "hero", "Recevoir mon devis gratuit", "btn btn-quote btn-lg") + b_call(svc, "hero", cls="btn btn-call btn-lg")
    extra = ""
    if p.get("problems"):
        extra = problem_chips(svc)
    elif p.get("rooms"):
        extra = room_chips()
    return f"""<section class="hero" data-service="{svc}">{media}
<div class="hero-in wrap">
<div class="hero-copy">
<h1>{p["h1"]}</h1>
<p class="hero-sub">{p["sub"]}</p>
<div class="hero-ctas">{ctas}</div>
{trust3()}
{extra}
</div>
<div class="hero-form" id="devis">{quote_form(svc, p.get("form_default"), p["wa"])}</div>
</div>
</section>"""


MARKS = {"water": WLINE, "spark": SPARK}


def head_block(mark, title, intro=None, cls="head"):
    m = MARKS.get(mark, "")
    i = f"<p>{intro}</p>" if intro else ""
    return f'<div class="{cls}">{m}<h2>{title}</h2>{i}</div>'


def checklist(groups, spark=False, note=None):
    cl = "check check--spark" if spark else "check"
    out = []
    for icon, title, items in groups:
        lis = "".join(f"<li>{x}</li>" for x in items)
        out.append(f'<div class="group"><h3>{ic(icon)}{title}</h3><ul class="{cl}">{lis}</ul></div>')
    n = f'<p class="groups-note">{note}</p>' if note else ""
    return f'<div class="groups">{"".join(out)}</div>{n}'


def steps_block(svc, mark, watext, title="Comment ça se passe", steps=None, bg="sec"):
    steps = steps or [
        ("Vous appelez ou demandez un devis", "Par téléphone, sur WhatsApp ou avec le formulaire. Une photo nous aide à comprendre votre besoin."),
        ("On vous rappelle et fixe le rendez-vous", "Nous discutons de votre besoin, venons voir sur place si nécessaire et vous remettons un devis gratuit."),
        ("On intervient", "À la date convenue, avec le matériel nécessaire. Une question en cours de route&nbsp;? Vous nous appelez au même numéro."),
    ]
    lis = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    return f"""<section class="{bg}" aria-labelledby="steps-t"><div class="wrap">
<div class="head">{MARKS.get(mark, "")}<h2 id="steps-t">{title}</h2></div>
<ol class="steps">{lis}</ol>
{cta_row(svc, "steps", watext, "Obtenir mon devis", "Appeler maintenant", order="qcw")}
</div></section>"""


def team_block(rel, svc, bg="sec sec--white", short=False):
    more = "" if short else ("<p>Pour un projet qui touche plusieurs métiers, un déménagement suivi du nettoyage ou une salle de bain "
                             "à refaire puis à repeindre, vous avez un seul interlocuteur et un seul devis.</p>")
    return f"""<section class="{bg}" aria-labelledby="team-t"><div class="wrap cols cols--5-7">
<div><div class="team-ph" role="img" aria-label="Emplacement réservé à la photo de l’équipe"><b>Photo de l’équipe</b><small>Emplacement réservé à la photo des trois frères (à fournir)</small></div></div>
<div>
<h2 id="team-t">Trois frères, une seule entreprise</h2>
<p>Zeka D-Services est une entreprise familiale de Chêne-Bourg, fondée par trois frères. Chacun a entre 6 et 10&nbsp;ans d’expérience dans son domaine. Ensemble, ils couvrent le sanitaire, le chauffage, le nettoyage, le déménagement, la rénovation et la peinture.</p>
{more}
<ul class="facts">
<li>{ic("family")}<span><b>Entreprise familiale.</b> Trois frères, chacun avec 6 à 10&nbsp;ans de métier.</span></li>
<li>{ic("doc")}<span><b>Devis gratuit et personnalisé.</b> Nous nous déplaçons pour évaluer le travail sur place quand c’est utile.</span></li>
<li>{ic("pin")}<span><b>Basés à Chêne-Bourg.</b> {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]}.</span></li>
</ul>
</div></div></section>"""


def zone_block(svc, bg="sec sec--sand", title="Partout dans le canton de Genève"):
    towns = "".join(f"<li>{t}</li>" for t in TOWNS) + '<li class="all">Tout le canton de Genève</li>'
    return f"""<section class="{bg}" aria-labelledby="zone-t"><div class="wrap zone">
<div>{MAP_SVG}</div>
<div>
<h2 id="zone-t">{title}</h2>
<p>Nous partons de Chêne-Bourg et nous déplaçons dans toutes les communes du canton, en ville comme à la campagne.</p>
<ul class="towns">{towns}</ul>
<div class="cta-row">{b_call(svc, "zone", "Appeler maintenant")}</div>
</div></div></section>"""


def faq_block(faqs, bg="sec sec--white", title="Questions fréquentes"):
    items = "".join(
        f'<details><summary>{q}{ic("chev")}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs)
    return f"""<section class="{bg}" aria-labelledby="faq-t"><div class="wrap cols cols--4-8">
<div><h2 id="faq-t">{title}</h2><p style="color:var(--muted)">Une autre question&nbsp;? Appelez le <a href="{TEL}" data-loc="faq"><span class="nw" data-phone>{PHONE}</span></a>.</p></div>
<div class="faq">{items}</div>
</div></section>"""


def reviews_block():
    return """<section class="sec sec--sand" id="avis" hidden aria-labelledby="avis-t"><div class="wrap">
<div class="head"><h2 id="avis-t">Avis clients</h2></div>
<div class="revs"></div>
<p style="margin-top:20px"><a class="lnk revs-link" href="#" target="_blank" rel="noopener" hidden>Voir tous les avis sur Google</a></p>
</div></section>"""


def final_cta(p):
    svc = p["slug"]
    return f"""<section class="fcta" aria-labelledby="fcta-t" data-service="{svc}"><div class="wrap fcta-in">
<div>
<h2 id="fcta-t">Votre devis gratuit en quelques minutes</h2>
<p>Appelez-nous, écrivez-nous sur WhatsApp ou laissez votre numéro&nbsp;: nous vous rappelons.</p>
<a class="phone-big" href="{TEL}" data-service="{svc}" data-loc="final-big">{ic("phone")}<span data-phone>{PHONE}</span></a>
<div class="btns">{b_call(svc, "final", "Appeler maintenant")}{b_wa(svc, "final", p["wa"])}</div>
</div>
{callback_form(svc, p.get("form_default") or "Autre")}
</div></section>"""


def gallery(rel, items):
    big, *rest = items
    out = [f'<figure class="g-big"><div class="frame frame--43">{pic(rel, big[0], big[1], "(min-width: 760px) 50vw, 100vw")}</div><figcaption class="cap">{big[2]}</figcaption></figure>']
    for k, alt, cap in rest:
        out.append(f'<figure><div class="frame frame--43">{pic(rel, k, alt, "(min-width: 760px) 25vw, 50vw")}</div><figcaption class="cap">{cap}</figcaption></figure>')
    return f'<div class="gal">{"".join(out)}</div>'


def split(rel, key, alt, body, rev=False, ratio="43"):
    r = " split--rev" if rev else ""
    return f'<div class="split{r}"><div class="split-media"><div class="frame frame--{ratio}">{pic(rel, key, alt, "(min-width: 960px) 50vw, 100vw")}</div></div><div>{body}</div></div>'


def band(rel, key, title, intro, tips, extra=""):
    lis = "".join(f"<li><span>{t}</span></li>" for t in tips)
    return f"""<section class="band" aria-labelledby="band-t"><div class="band-media">{pic(rel, key, "", "100vw")}</div>
<div class="wrap band-in"><h2 id="band-t">{title}</h2><p>{intro}</p><ol class="tips">{lis}</ol>{extra}</div></section>"""


# ------------------------------------------------------------------ header / footer
NAV = [("plombier-geneve/", "Plombier"), ("chauffagiste-geneve/", "Chauffage"), ("nettoyage-geneve/", "Nettoyage"),
       ("nettoyage-fin-de-bail-geneve/", "Fin de bail"), ("demenagement-geneve/", "Déménagement"),
       ("renovation-peinture-geneve/", "Peinture")]


def header(rel, svc, nav=False, quote_href="#devis"):
    n = ""
    if nav:
        n = '<nav class="hd-nav" aria-label="Nos services">' + "".join(f'<a href="{rel}{h}">{t}</a>' for h, t in NAV) + "</nav>"
    return f"""<a class="skip" href="#main">Aller au contenu</a>
<header class="hd" data-service="{svc}"><div class="wrap hd-in">
<a class="hd-logo" href="{rel or './'}"><img src="{rel}img/brand/logo.svg" width="244" height="44" alt="Zeka D-Services, accueil"></a>
{n}<div class="hd-cta">
<a class="btn btn-call hd-phone" href="{TEL}" data-service="{svc}" data-loc="header" aria-label="Appeler le {PHONE}">{ic("phone")}<span class="num" data-phone>{PHONE}</span></a>
<a class="btn btn-quote hd-quote" href="{quote_href}" data-service="{svc}" data-loc="header"><span class="l-long">Devis gratuit</span><span class="l-short">Devis</span></a>
</div></div></header>"""


SERVICE_LINKS = [("plombier-geneve/", "Plombier à Genève"), ("chauffagiste-geneve/", "Chauffagiste à Genève"),
                 ("nettoyage-geneve/", "Entreprise de nettoyage"), ("nettoyage-fin-de-bail-geneve/", "Nettoyage de fin de bail"),
                 ("demenagement-geneve/", "Déménagement"), ("renovation-peinture-geneve/", "Rénovation et peinture")]


def footer(rel):
    svcs = "".join(f'<li><a href="{rel}{h}">{t}</a></li>' for h, t in SERVICE_LINKS)
    return f"""<footer class="ft"><div class="wrap">
<div class="ft-grid">
<div class="ft-brand"><img src="{rel}img/brand/logo-white.svg" width="244" height="44" alt="Zeka D-Services" loading="lazy">
<p>Entreprise familiale multiservice à Chêne-Bourg&nbsp;: sanitaire, chauffage, nettoyage, déménagement, rénovation et peinture dans tout le canton de Genève.</p></div>
<div><h2>Services</h2><ul>{svcs}</ul></div>
<div><h2>Contact</h2><ul class="ft-contact">
<li>{ic("pin")}<address>Zeka D-Services<br>{ADDRESS[0]}<br>{ADDRESS[1]} {ADDRESS[2]}</address></li>
<li>{ic("phone")}<a href="{TEL}" data-loc="footer"><span data-phone>{PHONE}</span></a></li>
<li>{ic("wa")}<a href="{wa("Bonjour, je souhaite un renseignement.")}" target="_blank" rel="noopener" data-loc="footer">WhatsApp</a></li>
<li>{ic("mail")}<a href="#" data-email>E-mail</a></li>
</ul></div>
<div><h2>Informations</h2><ul>
<li><a href="{rel or './'}">Accueil</a></li>
<li><a href="{rel}mentions-legales/">Mentions légales</a></li>
<li><a href="{rel}confidentialite/">Protection des données</a></li>
<li><a href="{rel}mentions-legales/#credits">Crédits photos</a></li>
</ul></div>
</div>
<div class="ft-bottom"><span>© 2026 Zeka D-Services · Chêne-Bourg, Genève</span><ul><li><a href="{rel}mentions-legales/">Mentions légales</a></li><li><a href="{rel}confidentialite/">Confidentialité</a></li></ul></div>
</div></footer>"""


def contact_bar(svc, watext):
    return f"""<nav class="mbar" aria-label="Contact rapide" data-service="{svc}">
<a class="m-call" href="{TEL}" data-loc="mobile-bar">{ic("phone")}Appeler</a>
<a class="m-wa" href="{wa(watext)}" target="_blank" rel="noopener" data-loc="mobile-bar">{ic("wa")}WhatsApp</a>
<a class="m-quote" href="#devis" data-loc="mobile-bar">{ic("doc")}Devis</a>
</nav>
<a class="wa-float" href="{wa(watext)}" target="_blank" rel="noopener" data-service="{svc}" data-loc="float">{ic("wa")}WhatsApp</a>"""


# ------------------------------------------------------------------ head + JSON-LD
SRC_CSS = (ROOT / "tools" / "site.css").read_text()
CRIT, REST = SRC_CSS.split("/* ==== CRITICAL END ==== */")
CRIT = CRIT.split("*/", 1)[1]  # drop the header comment


def minify(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    # keep the space in media queries "and (" and in values like "0 0"
    css = css.replace("and(", "and (")
    return css.strip()


CRIT_MIN = minify(CRIT)
REST_MIN = minify(REST)

BIZ_TYPES = {
    "home": ["HomeAndConstructionBusiness", "Plumber", "HVACBusiness", "MovingCompany", "HousePainter"],
    "plombier": ["Plumber", "HomeAndConstructionBusiness"],
    "chauffagiste": ["HVACBusiness", "HomeAndConstructionBusiness"],
    "nettoyage": ["HomeAndConstructionBusiness"],
    "fin-de-bail": ["HomeAndConstructionBusiness"],
    "demenagement": ["MovingCompany"],
    "renovation": ["HousePainter", "GeneralContractor"],
}


def business(kind):
    return {
        "@type": BIZ_TYPES.get(kind, ["HomeAndConstructionBusiness"]),
        "@id": BASE_URL + "#entreprise",
        "name": "Zeka D-Services",
        "description": "Entreprise familiale multiservice à Chêne-Bourg (Genève) : sanitaire, chauffage, nettoyage, fin de bail, déménagement, rénovation et peinture.",
        "url": BASE_URL,
        "logo": BASE_URL + "img/brand/logo.png",
        "image": BASE_URL + "img/og-share.jpg",
        "telephone": "+41 78 639 50 66",
        "currenciesAccepted": "CHF",
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS[0], "postalCode": ADDRESS[1],
                    "addressLocality": ADDRESS[2], "addressRegion": "GE", "addressCountry": "CH"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "areaServed": [{"@type": "AdministrativeArea", "name": "Canton de Genève"}] +
                      [{"@type": "City", "name": t} for t in TOWNS],
    }


def jsonld(p):
    graph = [business(p["kind"])]
    url = BASE_URL + p["path"]
    if p.get("service_ld"):
        name, stype = p["service_ld"]
        graph.append({"@type": "Service", "name": name, "serviceType": stype, "url": url,
                      "provider": {"@id": BASE_URL + "#entreprise"},
                      "areaServed": {"@type": "AdministrativeArea", "name": "Canton de Genève"},
                      "offers": {"@type": "Offer", "description": "Devis gratuit et sans engagement", "priceCurrency": "CHF"}})
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]})
    if p.get("faqs"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in p["faqs"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace(" ", " ")


def head(p, rel):
    url = BASE_URL + p["path"]
    robots = '<meta name="robots" content="noindex, follow">' if p.get("noindex") else ""
    preload = ""
    if p.get("hero_img"):
        k = p["hero_img"]
        preload = (f'<link rel="preload" as="image" type="image/avif" media="(min-width: 960px)" '
                   f'imagesrcset="{srcset(rel, k, "avif")}" imagesizes="62vw" fetchpriority="high">')
    crit = CRIT_MIN.replace("url(../fonts/", f"url({rel}fonts/")
    ld = f'<script type="application/ld+json">{jsonld(p)}</script>' if not p.get("noindex") else ""
    return f"""<!doctype html>
<html lang="fr-CH" data-root="{rel}" data-page="{p['kind']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:site_name" content="Zeka D-Services">
<meta property="og:title" content="{esc(p.get("og_title", p["title"]))}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}img/og-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0D2236">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{rel}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{rel}apple-touch-icon.png">
<link rel="manifest" href="{rel}site.webmanifest">
<link rel="preload" href="{rel}fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel}fonts/source-sans-3-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<style>{crit}.nw{{white-space:nowrap}}</style>
<link rel="stylesheet" href="{rel}css/site.css?v={V}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{rel}css/site.css?v={V}"></noscript>
{ld}
</head>"""


def scripts(rel):
    return (f'<script src="{rel}js/config.js?v={V}" defer></script>'
            f'<script src="{rel}js/reviews.js?v={V}" defer></script>'
            f'<script src="{rel}js/main.js?v={V}" defer></script>')


# ------------------------------------------------------------------ typography
def typo(doc):
    """French spacing (non-breaking space before : ; ? !) in text only, never inside tags, styles or scripts."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", doc, flags=re.S)
    for i, part in enumerate(parts):
        if i % 2 == 0 and part:
            part = re.sub(r" ([:;])", " \\1", part)
            part = re.sub(r" ([?!])", " \\1", part)
            parts[i] = part
    return "".join(parts)


# ------------------------------------------------------------------ pages
FAQ_PAY = ("Comment se passe le paiement&nbsp;?", "Les modalités de paiement sont précisées dans votre devis. Posez-nous la question au moment du devis si vous avez une préférence.")


def faq_zone(what="Nous intervenons dans tout le canton de Genève"):
    return ("Dans quelles communes intervenez-vous&nbsp;?",
            f"{what}, notamment à Genève, Chêne-Bourg, Chêne-Bougeries, Thônex, Carouge, Lancy, Onex, Vernier, Meyrin, Plan-les-Ouates, Versoix, Cologny et Vandœuvres.")


PAGES = []

# ---------------- HOME
HOME = dict(
    kind="home", slug="general", path="", crumb="Accueil",
    title="Zeka D-Services · Sanitaire, chauffage, nettoyage à Genève · Devis gratuit",
    desc="Entreprise familiale de Chêne-Bourg : sanitaire, chauffage, nettoyage, fin de bail, déménagement et peinture dans tout le canton de Genève. Devis gratuit, appelez le 078 639 50 66.",
    h1="Sanitaire, chauffage et nettoyage à Genève, par une entreprise familiale",
    sub="Trois frères, chacun avec 6 à 10&nbsp;ans de métier. De la fuite d’eau au nettoyage de fin de bail, nous intervenons rapidement dans tout le canton de Genève.",
    hero_img="stock/plombier-evier", wa="Bonjour, je souhaite un devis.",
    faqs=[
        ("Le devis est-il gratuit&nbsp;?", "Oui. Le devis est gratuit et sans engagement, quel que soit le service. Pour un travail plus important, nous nous déplaçons pour évaluer le travail sur place."),
        ("Comment obtenir une intervention rapide&nbsp;?", f"Appelez le {PHONE}. Pour une fuite ou une panne, le téléphone est le plus rapide&nbsp;: nous vous disons tout de suite quand nous pouvons passer."),
        ("Pouvez-vous gérer le déménagement et le nettoyage de fin de bail&nbsp;?", "Oui. Nous déménageons vos affaires puis nettoyons l’ancien logement pour l’état des lieux. Un seul interlocuteur et un seul devis pour tout le départ."),
        ("Travaillez-vous pour les particuliers et les entreprises&nbsp;?", "Oui. Nous intervenons chez les particuliers, en appartement comme en villa, et pour les professionnels&nbsp;: bureaux, surfaces commerciales et immeubles."),
        ("Puis-je envoyer des photos&nbsp;?", "Oui, et c’est souvent le plus simple. Envoyez vos photos sur WhatsApp au 078 639 50 66, avec quelques mots sur votre besoin."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def home_body(p, rel):
    svc = p["slug"]
    acts_major = [
        ("stock/chaudiere-technicien", "Technicien en chauffage réglant une chaudière murale", "Sanitaire et chauffage",
         "Dépannage, réparation et installation, chez vous dans tout le canton.",
         ["Fuites d’eau et WC bouchés", "Boilers et eau chaude", "Chaudières, radiateurs et entretien", "Rénovation de salle de bain"],
         [("plombier-geneve/", "Plombier à Genève"), ("chauffagiste-geneve/", "Chauffagiste à Genève")], "drop"),
        ("stock/nettoyage-sol", "Nettoyage du sol d’un appartement lumineux", "Nettoyage",
         "D’appoint ou régulier, pour les particuliers comme pour les entreprises.",
         ["Fin de bail et état des lieux", "Appartements et villas", "Bureaux et surfaces commerciales", "Immeubles et fins de chantier"],
         [("nettoyage-geneve/", "Entreprise de nettoyage"), ("nettoyage-fin-de-bail-geneve/", "Nettoyage de fin de bail")], "spark"),
    ]
    acts_minor = [
        ("stock/demenagement-cartons", "Déménageur devant une camionnette chargée de cartons", "Déménagement",
         "En Suisse et à l’étranger, avec nos propres véhicules.",
         ["Emballage et déballage", "Démontage et remontage des meubles", "Transport national et international", "Garde-meubles avec un partenaire"],
         [("demenagement-geneve/", "Déménagement à Genève")]),
        ("stock/peinture-rouleau", "Mur repeint au rouleau", "Rénovation et peinture",
         "Pour rafraîchir un appartement ou refaire une salle de bain.",
         ["Murs, plafonds et boiseries", "Plaques de plâtre", "Salles de bain et cuisines", "Remise en peinture avant un départ"],
         [("renovation-peinture-geneve/", "Rénovation et peinture")]),
    ]

    def act(a, minor=False):
        key, alt, t, line, bullets, links = a[:6]
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        lk = "".join(f'<a class="lnk" href="{rel}{h}">{lt}{ic("arrow")}</a>' for h, lt in links)
        sizes = "(min-width: 760px) 260px, 100vw" if minor else "(min-width: 760px) 50vw, 100vw"
        ratio = "43" if minor else "32"
        cl = "check check--spark" if (len(a) > 6 and a[6] == "spark") else "check"
        return (f'<article class="act"><div class="frame frame--{ratio}">{pic(rel, key, alt, sizes)}</div><div>'
                f'<h3><a href="{rel}{links[0][0]}">{t}</a></h3><p>{line}</p><ul class="{cl}">{lis}</ul><div class="act-links">{lk}</div></div></article>')

    combo = f"""<section class="sec" aria-labelledby="combo-t"><div class="wrap">
<div class="combo" data-service="demenagement-nettoyage">
<div class="combo-media"><div class="frame">{pic(rel, "stock/demenagement-camionnette", "Cartons chargés dans une camionnette de déménagement", "(min-width: 960px) 25vw, 50vw")}</div><div class="frame">{pic(rel, "stock/appartement-vide", "Appartement vide et propre, prêt pour l’état des lieux", "(min-width: 960px) 25vw, 50vw")}</div></div>
<div class="combo-body">
<p class="combo-plus">{ic("truck")}Déménagement {ic("plus")} nettoyage de fin de bail {ic("spark")}</p>
<h2 id="combo-t">Une seule équipe pour tout votre départ</h2>
<p>Nous emballons et transportons vos affaires, puis nous nettoyons l’appartement vide pour l’état des lieux. Les dates sont coordonnées, vous n’avez qu’un interlocuteur et qu’un devis.</p>
<ul class="check" style="margin:18px 0 0"><li>Emballage, transport, démontage et remontage</li><li>Nettoyage complet de l’ancien logement, du four aux stores</li><li>Un devis unique, gratuit et sans engagement</li></ul>
<div class="cta-row">{b_wa("demenagement-nettoyage", "combo", "Bonjour, je souhaite un devis pour un déménagement avec nettoyage de fin de bail.", "Devis déménagement + nettoyage")}{b_call("demenagement-nettoyage", "combo", "Appeler maintenant")}</div>
</div></div></div></section>"""

    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="acts-t"><div class="wrap">
{head_block("water", "Quatre métiers, une entreprise familiale", "Sanitaire et chauffage, nettoyage, déménagement, rénovation et peinture&nbsp;: choisissez votre besoin, nous nous occupons du reste.").replace("<h2>", '<h2 id="acts-t">')}
<div class="acts">{"".join(act(a) for a in acts_major)}</div>
<div class="acts--minor">{"".join(act(a, True) for a in acts_minor)}</div>
{cta_row(svc, "activities", p["wa"], "Obtenir mon devis", "Appeler maintenant", "Écrire sur WhatsApp")}
</div></section>
{steps_block(svc, "water", p["wa"])}
{combo}
{team_block(rel, svc)}
{reviews_block()}
{zone_block(svc)}
{faq_block(p["faqs"])}"""


HOME["body"] = home_body
PAGES.append(HOME)

# ---------------- PLOMBIER
PLOMBIER = dict(
    kind="plombier", slug="plombier", path="plombier-geneve/", crumb="Plombier à Genève",
    title="Plombier Genève · Dépannage et devis gratuit · Zeka D-Services",
    desc="Plombier à Genève : fuite d’eau, WC bouché, débouchage, boiler, robinetterie. Entreprise familiale de Chêne-Bourg, intervention dans tout le canton. Appelez le 078 639 50 66.",
    h1="Plombier à Genève, intervention rapide",
    sub="Fuite d’eau, WC bouché, plus d’eau chaude&nbsp;? Entreprise familiale de Chêne-Bourg, nous venons chez vous rapidement, partout dans le canton de Genève.",
    video="sanitaire-hero", hero_img="stock/poster-sanitaire", call_first=True, problems=True, form_default="Sanitaire",
    wa="Bonjour, j’ai besoin d’un plombier. Voici une photo du problème :",
    service_ld=("Plombier à Genève : dépannage sanitaire, fuites, débouchage, boiler", "Plomberie et dépannage sanitaire"),
    faqs=[
        ("Intervenez-vous en urgence&nbsp;?", f"Pour une fuite, un WC bouché ou une panne d’eau chaude, appelez le {PHONE}. Nous vous disons directement quand un plombier peut passer chez vous."),
        ("Intervenez-vous le soir et le week-end&nbsp;?", "Appelez-nous&nbsp;: nous vous indiquons nos disponibilités du moment et le prochain créneau possible."),
        ("Combien coûte un dépannage&nbsp;?", "Le prix dépend du problème et des pièces à changer. Le devis est gratuit et sans engagement. Une photo envoyée sur WhatsApp nous aide à vous répondre plus précisément."),
        ("Faut-il être présent pendant l’intervention&nbsp;?", "Il faut que quelqu’un nous ouvre et nous montre l’installation. Si ce n’est pas possible, indiquez-le dans votre demande et nous trouvons une solution avec vous."),
        ("Je suis locataire&nbsp;: dois-je prévenir ma régie&nbsp;?", "En cas de dégât d’eau, prévenez votre régie et, si besoin, votre assurance. Prenez des photos avant et après&nbsp;: elles servent pour le dossier."),
        ("Remplacez-vous les boilers&nbsp;?", "Oui. Nous contrôlons le boiler, le détartrons ou le remplaçons s’il est en fin de vie, et vous expliquons l’option la plus raisonnable avant de commencer."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def plombier_body(p, rel):
    svc = p["slug"]
    groups = [
        ("drop", "Dépannage", ["Recherche et réparation de fuites", "Débouchage de WC, éviers, lavabos et douches", "Chasse d’eau qui coule ou ne se remplit plus",
                               "Robinet qui goutte, mitigeur défectueux", "Siphons et écoulements lents", "Joints et flexibles à remplacer"]),
        ("boiler", "Boiler et eau chaude", ["Diagnostic quand l’eau chaude ne vient plus", "Détartrage et entretien du boiler", "Remplacement du boiler",
                                            "Groupe de sécurité et raccordements"]),
        ("wrench", "Pose et remplacement", ["WC, lavabos et éviers", "Robinetterie et colonnes de douche", "Meubles de salle de bain",
                                            "Raccordement de lave-linge et lave-vaisselle"]),
        ("bath", "Rénovation", ["Rénovation complète de salle de bain", "Remplacement des appareils sanitaires", "Travaux de cuisine côté eau",
                                "Peinture et finitions par la même entreprise"]),
    ]
    s1 = f"""<h2>Plus d’eau chaude&nbsp;? Souvent le boiler</h2>
<p>Un boiler entartré chauffe mal, fait du bruit ou ne chauffe plus du tout. Nous contrôlons l’appareil et ses raccordements, le détartrons ou le remplaçons s’il est en fin de vie.</p>
<ul class="check"><li>Contrôle de l’appareil et du groupe de sécurité</li><li>Détartrage ou remplacement</li><li>Conseils pour choisir la bonne taille</li></ul>
{cta_row(svc, "split-boiler", "Bonjour, je n’ai plus d’eau chaude. Voici une photo de mon boiler :", wa_label="Envoyer une photo du boiler", order="wc")}"""
    s2 = f"""<h2>Débouchage&nbsp;: WC, évier, douche</h2>
<p>Un écoulement lent annonce souvent un bouchon. Nous débouchons WC, éviers, lavabos et douches, puis contrôlons le siphon et les raccords pour éviter qu’il ne revienne.</p>
{cta_row(svc, "split-debouchage", p["wa"], quote="Demander un devis", order="qc")}"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky">{WLINE}<h2 id="inc-t">Nos interventions sanitaires</h2><p style="color:var(--muted)">Du petit dépannage à la salle de bain complète, chez les particuliers comme dans les bureaux.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/plombier-boiler", "Plombier raccordant un siphon sous un lavabo", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups, note="Vous ne trouvez pas votre problème&nbsp;? Décrivez-le dans le formulaire ou envoyez une photo sur WhatsApp.")}
{cta_row(svc, "checklist", p["wa"], order="cqw")}</div>
</div></section>
{band(rel, "stock/robinet-goutte", "Une fuite&nbsp;? En attendant notre arrivée", "Quatre gestes simples limitent les dégâts.", [
        "<b>Coupez l’eau.</b> Fermez la vanne sous l’appareil qui fuit, ou la vanne générale du logement.",
        "<b>Éloignez l’eau de l’électricité.</b> Si l’eau approche d’une prise ou d’un appareil, coupez le courant au tableau.",
        "<b>Photographiez les dégâts.</b> Les photos servent à votre régie et à votre assurance.",
        "<b>Envoyez-nous une photo sur WhatsApp.</b> Nous voyons tout de suite de quoi il s’agit."],
        f'<div class="cta-row">{b_call(svc, "band", "Appeler maintenant")}{b_wa(svc, "band", p["wa"], "Envoyer une photo")}</div>')}
<section class="sec" aria-label="Boilers et débouchage"><div class="wrap">
{split(rel, "stock/boiler-cle", "Plombier serrant un raccord sur un boiler", s1)}
{split(rel, "stock/plombier-evier", "Plombier intervenant sous un évier", s2, rev=True)}
</div></section>
<section class="sec sec--white" aria-labelledby="gal-t"><div class="wrap">
{head_block("water", "Dans les salles de bain et cuisines de Genève").replace("<h2>", '<h2 id="gal-t">')}
{gallery(rel, [("stock/plombier-salle-de-bain", "Plombier au travail dans une salle de bain", "Réparation et pose d’appareils sanitaires"),
               ("stock/wc-chasse", "Chasse d’eau d’un WC suspendu", "Chasses d’eau et WC"),
               ("stock/raccord-radiateur", "Raccordement de tuyaux à la pince", "Raccords et tuyauterie")])}
</div></section>
{steps_block(svc, "water", p["wa"])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Plombier dans tout le canton de Genève")}"""


PLOMBIER["body"] = plombier_body
PAGES.append(PLOMBIER)

# ---------------- CHAUFFAGISTE
CHAUFF = dict(
    kind="chauffagiste", slug="chauffagiste", path="chauffagiste-geneve/", crumb="Chauffagiste à Genève",
    title="Chauffagiste Genève · Panne de chauffage, chaudière, entretien · Zeka D-Services",
    desc="Chauffagiste à Genève : panne de chauffage, réparation et remplacement de chaudière, radiateurs, entretien, pompe à chaleur. Entreprise familiale, tout le canton. Devis gratuit.",
    h1="Chauffagiste à Genève&nbsp;: panne, réparation, entretien",
    sub="Chaudière en panne, radiateurs froids, entretien à prévoir&nbsp;? Entreprise familiale de Chêne-Bourg, nous intervenons rapidement dans tout le canton de Genève.",
    hero_img="stock/chaudiere-technicien", call_first=True, problems=True, form_default="Chauffage",
    wa="Bonjour, j’ai un problème de chauffage. Voici une photo de ma chaudière :",
    service_ld=("Chauffagiste à Genève : dépannage, réparation et remplacement de chaudière, entretien", "Chauffage"),
    faqs=[
        ("Ma chaudière est en panne&nbsp;: que faire&nbsp;?", f"Notez le code d’erreur affiché, vérifiez le thermostat et le disjoncteur, puis appelez le {PHONE}. Avec ces informations, le diagnostic va plus vite."),
        ("Intervenez-vous le soir et le week-end&nbsp;?", "Appelez-nous&nbsp;: nous vous indiquons nos disponibilités du moment et le prochain créneau possible."),
        ("Faut-il réparer ou remplacer ma chaudière&nbsp;?", "Cela dépend de son âge, de son état et du coût de la réparation. Nous faisons le diagnostic sur place et vous présentons les deux options dans un devis gratuit."),
        ("Installez-vous des pompes à chaleur&nbsp;?", "Oui. Nous posons des pompes à chaleur, des chaudières gaz et mazout et des installations solaires thermiques. Nous évaluons d’abord votre logement avant de vous remettre un devis."),
        ("Pourquoi un radiateur reste-t-il froid&nbsp;?", "Souvent à cause d’air dans le circuit, d’une vanne thermostatique bloquée ou d’une pression trop basse. Nous cherchons la cause et rétablissons la chaleur."),
        ("Je suis locataire&nbsp;: qui appeler&nbsp;?", "Dans un immeuble, le chauffage est souvent géré par la régie. Prévenez-la d’abord. Nous pouvons intervenir à sa demande ou à la vôtre."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def chauff_body(p, rel):
    svc = p["slug"]
    groups = [
        ("flame", "Dépannage", ["Diagnostic de panne de chaudière", "Radiateurs froids ou tièdes", "Pression trop basse, fuites sur le circuit",
                                "Localisation de la panne et remplacement des pièces défectueuses"]),
        ("boiler", "Chaudières", ["Réparation et remplacement de chaudière", "Chaudières gaz et mazout", "Chaudières à combustibles solides",
                                  "Citernes à mazout et raccordements"]),
        ("radiator", "Entretien et régulation", ["Entretien de la chaudière", "Purge et équilibrage des radiateurs", "Thermostats, sondes et capteurs",
                                                 "Vannes thermostatiques"]),
        ("wrench", "Installations", ["Pose de radiateurs et de tuyauterie de chauffage", "Pompes à chaleur", "Installations solaires thermiques",
                                     "Planification des travaux étape par étape"]),
    ]
    s1 = f"""<h2>Radiateurs froids ou tièdes</h2>
<p>Air dans le circuit, vanne thermostatique bloquée, pression trop basse&nbsp;: nous cherchons la cause et rétablissons la chaleur dans chaque pièce.</p>
<ul class="check"><li>Purge et équilibrage</li><li>Contrôle de la pression et des vannes</li><li>Remplacement des têtes thermostatiques</li></ul>
{cta_row(svc, "split-radiateur", p["wa"], order="cq")}"""
    s2 = f"""<h2>Remplacer son chauffage</h2>
<p>Chaudière en fin de vie ou envie de changer d’énergie&nbsp;? Nous posons chaudières gaz et mazout, pompes à chaleur et installations solaires thermiques. Lors de la visite, nous vous expliquons les options et leurs conséquences pour votre logement.</p>
{cta_row(svc, "split-remplacement", p["wa"], quote="Demander une visite et un devis", order="qc")}"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky">{WLINE}<h2 id="inc-t">Nos interventions chauffage</h2><p style="color:var(--muted)">Dépannage, entretien et installation, en appartement, en villa ou dans les bureaux.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/chaudiere-pompe", "Réglage du circulateur d’une chaudière", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups, note="Une chaudière, un code d’erreur&nbsp;? Envoyez-nous une photo sur WhatsApp avec votre demande.")}
{cta_row(svc, "checklist", p["wa"], order="cqw")}</div>
</div></section>
{band(rel, "stock/vanne-thermostatique", "Plus de chauffage&nbsp;? Avant d’appeler", "Trois vérifications rapides. Si le problème reste, appelez-nous avec ces informations&nbsp;: le diagnostic sera plus rapide.", [
        "<b>Le thermostat.</b> Est-il bien réglé, et ses piles sont-elles bonnes&nbsp;?",
        "<b>Le code d’erreur.</b> La chaudière affiche-t-elle un code&nbsp;? Notez-le ou prenez-le en photo.",
        "<b>Le disjoncteur.</b> Le disjoncteur de la chaudière est-il enclenché au tableau électrique&nbsp;?"],
        f'<div class="cta-row">{b_call(svc, "band", "Appeler maintenant")}{b_wa(svc, "band", p["wa"], "Envoyer une photo")}</div>')}
<section class="sec" aria-label="Radiateurs et remplacement"><div class="wrap">
{split(rel, "stock/radiateur", "Radiateur sous une fenêtre dans un appartement", s1)}
{split(rel, "stock/collecteur-chauffage", "Collecteur de chauffage avec manomètre et circulateur", s2, rev=True)}
</div></section>
<section class="sec sec--white" aria-labelledby="gal-t"><div class="wrap">
{head_block("water", "Chaudières, radiateurs, régulation").replace("<h2>", '<h2 id="gal-t">')}
{gallery(rel, [("stock/chaudiere-technicien-2", "Technicien contrôlant une chaudière murale", "Contrôle et réparation de chaudière"),
               ("stock/raccord-radiateur", "Raccordement d’un radiateur", "Pose de radiateurs"),
               ("stock/thermostat", "Réglage d’un thermostat d’ambiance", "Thermostats et régulation")])}
</div></section>
{steps_block(svc, "water", p["wa"])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Chauffagiste dans tout le canton de Genève")}"""


CHAUFF["body"] = chauff_body
PAGES.append(CHAUFF)

# ---------------- NETTOYAGE
NETT = dict(
    kind="nettoyage", slug="nettoyage", path="nettoyage-geneve/", crumb="Entreprise de nettoyage à Genève",
    title="Entreprise de nettoyage Genève · Appartements, bureaux, immeubles · Devis gratuit",
    desc="Entreprise de nettoyage à Genève : appartements, villas, bureaux, immeubles, vitres, fin de chantier. Ponctuel ou régulier. Entreprise familiale de Chêne-Bourg, devis gratuit.",
    h1="Entreprise de nettoyage à Genève, ponctuel ou régulier",
    sub="Appartements, bureaux, immeubles&nbsp;: une entreprise familiale de Chêne-Bourg s’occupe de votre nettoyage, une fois ou chaque semaine, rapidement et partout dans le canton de Genève.",
    video="nettoyage-hero", hero_img="stock/poster-nettoyage", form_default="Nettoyage",
    wa="Bonjour, je souhaite un devis pour un nettoyage.",
    service_ld=("Entreprise de nettoyage à Genève : appartements, bureaux, immeubles", "Nettoyage"),
    faqs=[
        ("Proposez-vous un nettoyage régulier&nbsp;?", "Oui. Nous faisons des nettoyages ponctuels et des contrats réguliers, par exemple chaque semaine pour des bureaux ou des parties communes d’immeuble."),
        ("Venez-vous avec vos produits et votre matériel&nbsp;?", "Oui. Nous choisissons les produits adaptés à chaque surface et venons avec nos machines et notre matériel."),
        ("Pouvez-vous nettoyer en dehors des heures de bureau&nbsp;?", "Dites-nous les horaires qui vous conviennent dans votre demande&nbsp;: nous en tenons compte dans le devis."),
        ("Faites-vous les nettoyages de fin de chantier&nbsp;?", "Oui. Nous retirons poussières et résidus de chantier, nettoyons sols, vitres et sanitaires, et trions les déchets selon les prescriptions."),
        ("Faut-il être présent pendant le nettoyage&nbsp;?", "Pas forcément. Nous convenons ensemble de l’accès au moment du devis&nbsp;: clés, code ou concierge."),
        ("Comment est établi le prix&nbsp;?", "Selon la surface, le type de locaux et la fréquence. Le devis est gratuit et sans engagement."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def nett_body(p, rel):
    svc = p["slug"]
    groups = [
        ("kitchen", "Cuisine", ["Plans de travail, évier et robinetterie", "Façades d’armoires et poignées", "Électroménager à l’extérieur",
                                "Catelles et crédence"]),
        ("bath", "Salle de bain et WC", ["Lavabo, douche, baignoire et WC", "Carrelage et joints", "Miroirs et robinetterie sans traces",
                                         "Détartrage du calcaire"]),
        ("home", "Pièces à vivre", ["Dépoussiérage des meubles et surfaces", "Sols aspirés et lavés, moquettes", "Plinthes, portes, interrupteurs",
                                    "Vitres intérieures"]),
        ("building", "Bureaux et immeubles", ["Postes de travail et salles de réunion", "Coin café, sanitaires et poubelles", "Entrées, cages d’escalier et rampes",
                                              "Tri des déchets selon les prescriptions"]),
    ]
    s1 = f"""<h2>D’appoint ou régulier</h2>
<p>Un grand nettoyage avant une fête ou après des travaux, ou un passage chaque semaine&nbsp;: vous choisissez la fréquence, nous adaptons l’équipe et le matériel.</p>
<ul class="check check--spark"><li>Appartements et villas</li><li>Nettoyages réguliers sur contrat</li><li>Nettoyages de fin de chantier et débarras</li></ul>
{cta_row(svc, "split-frequence", p["wa"], order="qw")}"""
    s2 = f"""<h2>Bureaux et surfaces commerciales</h2>
<p>Des locaux propres pour vos équipes et vos clients. Nous intervenons dans les bureaux, commerces et parties communes d’immeubles, aux horaires qui vous conviennent.</p>
<ul class="check check--spark"><li>Sols, postes de travail, sanitaires</li><li>Machines adaptées aux grandes surfaces</li><li>Locaux remis propres et rangés</li></ul>
{cta_row(svc, "split-bureaux", "Bonjour, je souhaite un devis pour le nettoyage de nos bureaux.", quote="Devis pour vos bureaux", order="qc")}"""
    s3 = f"""<h2>Vitres, stores et cadres</h2>
<p>Les vitres font la différence dans un logement comme dans un commerce. Nous nettoyons vitres, cadres, tablettes et stores, à l’intérieur comme à l’extérieur quand l’accès le permet.</p>
{cta_row(svc, "split-vitres", p["wa"], order="cq")}"""
    finbail = f"""<section class="sec sec--white" aria-labelledby="fdb-t" data-service="fin-de-bail"><div class="wrap">
<div class="combo"><div class="combo-media"><div class="frame">{pic(rel, "stock/calcaire-douche", "Détartrage d’une pomme de douche", "(min-width: 960px) 25vw, 50vw")}</div><div class="frame">{pic(rel, "stock/appartement-vide-2", "Pièce vide aux murs blancs", "(min-width: 960px) 25vw, 50vw")}</div></div>
<div class="combo-body"><p class="combo-plus">{ic("key")}État des lieux</p><h2 id="fdb-t">Vous quittez votre appartement&nbsp;?</h2>
<p>Le nettoyage de fin de bail a ses propres règles&nbsp;: four, hotte, calcaire, stores, armoires dedans et dehors. Tout est détaillé sur notre page dédiée.</p>
<div class="cta-row"><a class="btn btn-quote" href="{rel}nettoyage-fin-de-bail-geneve/" data-loc="nettoyage-to-fdb">Nettoyage de fin de bail{ic("arrow")}</a></div></div></div>
</div></section>"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky">{SPARK}<h2 id="inc-t">Ce qui est inclus</h2><p style="color:var(--muted)">La base de chaque nettoyage. Nous adaptons la liste à vos locaux et à vos demandes.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/nettoyage-evier", "Nettoyage de l’évier et du plan de travail", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups, spark=True, note="Besoin de quelque chose de précis, comme les stores, le four ou les vitres extérieures&nbsp;? Indiquez-le dans votre demande.")}
{cta_row(svc, "checklist", p["wa"], order="qcw")}</div>
</div></section>
<section class="sec" aria-label="Nos formules de nettoyage"><div class="wrap">
{split(rel, "stock/nettoyage-sol", "Nettoyage du sol d’un salon lumineux", s1)}
{split(rel, "stock/nettoyage-bureau", "Aspiration de la moquette d’un bureau", s2, rev=True)}
{split(rel, "stock/vitres-perche", "Nettoyage de fenêtres à la perche", s3)}
</div></section>
{finbail}
{steps_block(svc, "spark", p["wa"])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Nettoyage dans tout le canton de Genève")}"""


NETT["body"] = nett_body
PAGES.append(NETT)

# ---------------- FIN DE BAIL
FDB = dict(
    kind="fin-de-bail", slug="fin-de-bail", path="nettoyage-fin-de-bail-geneve/", crumb="Nettoyage de fin de bail à Genève",
    title="Nettoyage fin de bail Genève · État des lieux · Devis gratuit · Zeka D-Services",
    desc="Nettoyage de fin de bail à Genève pour un état des lieux sans stress : cuisine, four, calcaire, vitres, stores, armoires. Studio à 5.5 pièces, devis gratuit. Entreprise familiale.",
    h1="Nettoyage de fin de bail à Genève, pour un état des lieux sans stress",
    sub="Vous rendez les clés à la régie&nbsp;? Entreprise familiale de Chêne-Bourg, nous nettoyons tout l’appartement, du four aux stores, rapidement et partout dans le canton de Genève.",
    hero_img="stock/appartement-vide", rooms=True, form_default="Fin de bail",
    wa="Bonjour, je souhaite un devis pour un nettoyage de fin de bail.",
    service_ld=("Nettoyage de fin de bail à Genève pour l’état des lieux", "Nettoyage de fin de bail"),
    faqs=[
        ("Combien coûte un nettoyage de fin de bail&nbsp;?", "Le prix dépend du nombre de pièces, de l’état du logement et des extras comme le balcon ou les stores. Indiquez la taille du logement dans le formulaire&nbsp;: le devis est gratuit et sans engagement."),
        ("Que se passe-t-il si la régie demande une retouche&nbsp;?", "Appelez-nous dès l’état des lieux. Les conditions d’un éventuel passage complémentaire sont précisées dans votre devis."),
        ("Quand faut-il réserver&nbsp;?", "Dès que vous connaissez la date de l’état des lieux. Indiquez-la dans votre demande pour que nous planifiions le nettoyage juste avant."),
        ("Le logement doit-il être vide&nbsp;?", "Oui, idéalement entièrement vide. Le nettoyage est plus rapide et plus complet. Si vous déménagez avec nous, nous coordonnons les deux."),
        ("L’eau et l’électricité doivent-elles rester branchées&nbsp;?", "Oui, jusqu’à la fin du nettoyage. Nous en avons besoin pour l’eau chaude, l’éclairage et nos machines."),
        ("Dois-je être présent&nbsp;?", "Pas pendant tout le nettoyage. Nous convenons ensemble de l’accès et de la remise des clés au moment du devis."),
        ("Fournissez-vous les produits&nbsp;?", "Oui. Nous venons avec les produits adaptés, notamment contre le calcaire, et avec notre matériel."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def fdb_body(p, rel):
    svc = p["slug"]
    groups = [
        ("kitchen", "Cuisine", ["Four, plaques et grilles, dedans et dehors", "Frigo et congélateur, joints compris", "Hotte et filtre",
                                "Armoires dedans et dehors, tiroirs", "Évier, robinetterie et catelles"]),
        ("bath", "Salle de bain et WC", ["Calcaire sur robinets, douche et carrelage", "WC, lavabo, baignoire et douche", "Miroirs et armoire de toilette",
                                         "Joints, siphons visibles et bouches d’aération"]),
        ("window", "Fenêtres et stores", ["Vitres et cadres, intérieur et extérieur", "Tablettes et encadrements", "Stores et lamelles",
                                          "Portes-fenêtres du balcon"]),
        ("home", "Pièces, sols et balcon", ["Sols aspirés et lavés, plinthes", "Armoires murales dedans et dehors", "Portes, cadres et poignées",
                                            "Interrupteurs, prises et radiateurs", "Balcon ou terrasse"]),
    ]
    prep = band(rel, "stock/vitres-raclette", "Avant notre passage", "Quelques préparatifs pour un nettoyage efficace et un état des lieux serein.", [
        "<b>Videz entièrement le logement</b>, y compris la cave et le galetas si la régie les contrôle.",
        "<b>Laissez l’eau et l’électricité branchées</b> jusqu’à la fin du nettoyage.",
        "<b>Dégivrez le congélateur</b> la veille de notre passage.",
        "<b>Indiquez-nous la date et l’heure</b> de l’état des lieux dans votre demande."],
        f'<div class="cta-row">{b_quote(svc, "band", "Obtenir mon devis", "btn btn-light")}{b_call(svc, "band", "Appeler maintenant")}</div>')
    combo = f"""<section class="sec" aria-labelledby="combo-t" data-service="demenagement-nettoyage"><div class="wrap">
<div class="combo"><div class="combo-media"><div class="frame">{pic(rel, "stock/demenagement-diable", "Cartons transportés vers une camionnette", "(min-width: 960px) 25vw, 50vw")}</div><div class="frame">{pic(rel, "stock/cuisine-four", "Cuisine propre avec four encastré", "(min-width: 960px) 25vw, 50vw")}</div></div>
<div class="combo-body"><p class="combo-plus">{ic("truck")}Déménagement {ic("plus")} nettoyage {ic("spark")}</p><h2 id="combo-t">Vous déménagez aussi&nbsp;?</h2>
<p>Nous transportons vos affaires puis nettoyons l’ancien logement pour l’état des lieux. Une seule équipe, des dates coordonnées et un seul devis.</p>
<div class="cta-row">{b_wa("demenagement-nettoyage", "combo", "Bonjour, je souhaite un devis pour un déménagement avec nettoyage de fin de bail.", "Devis déménagement + nettoyage")}<a class="btn btn-line" href="{rel}demenagement-geneve/" data-loc="fdb-to-dem">Le déménagement{ic("arrow")}</a></div></div></div>
</div></section>"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky">{SPARK}<h2 id="inc-t">Ce qui est inclus</h2><p style="color:var(--muted)">Les points que la régie contrôle à l’état des lieux, pièce par pièce.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/calcaire-vapeur", "Détartrage du carrelage à la vapeur", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups, spark=True, note="Votre régie a sa propre liste&nbsp;? Envoyez-la-nous avec votre demande, nous la suivons.")}
{cta_row(svc, "checklist", p["wa"], order="qwc")}</div>
</div></section>
{prep}
<section class="sec sec--white" aria-labelledby="gal-t"><div class="wrap">
{head_block("spark", "Là où l’état des lieux se joue", "Calcaire, intérieur du four, poignées et cadres&nbsp;: les détails que l’on remarque en premier.").replace("<h2>", '<h2 id="gal-t">')}
{gallery(rel, [("stock/calcaire-douche", "Détartrage d’une pomme de douche aux gants", "Calcaire dans la douche"),
               ("stock/cuisine-four", "Cuisine propre avec four et hotte", "Four, hotte et plaques"),
               ("stock/poignee-armoire", "Nettoyage d’une poignée d’armoire", "Armoires et poignées")])}
</div></section>
{combo}
{steps_block(svc, "spark", p["wa"], steps=[
        ("Vous demandez un devis", "Indiquez la taille du logement et la date de l’état des lieux. Des photos sur WhatsApp nous aident à estimer le travail."),
        ("On vous rappelle et fixe la date", "Nous confirmons le devis, gratuit et sans engagement, et planifions le nettoyage avant la remise des clés."),
        ("On nettoie, vous rendez les clés", "Nous nettoyons tout le logement selon la liste convenue. Vous arrivez à l’état des lieux l’esprit tranquille.")])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Fin de bail dans tout le canton de Genève")}"""


FDB["body"] = fdb_body
PAGES.append(FDB)

# ---------------- DEMENAGEMENT
DEM = dict(
    kind="demenagement", slug="demenagement", path="demenagement-geneve/", crumb="Déménagement à Genève",
    title="Déménagement Genève · National et international · Devis gratuit · Zeka D-Services",
    desc="Déménagement à Genève, en Suisse et à l’étranger : emballage, transport, démontage et remontage, garde-meubles. Offre déménagement + nettoyage de fin de bail. Devis gratuit.",
    h1="Déménagement à Genève, en Suisse et à l’étranger",
    sub="Emballage, transport, montage&nbsp;: une entreprise familiale de Chêne-Bourg organise votre déménagement de A à Z, et peut aussi nettoyer l’ancien logement pour l’état des lieux.",
    hero_img="stock/demenagement-camionnette", form_default="Déménagement",
    wa="Bonjour, je souhaite un devis pour un déménagement.",
    service_ld=("Déménagement à Genève, national et international", "Déménagement"),
    faqs=[
        ("Comment est calculé le prix du déménagement&nbsp;?", "Nous établissons le devis selon la surface et le volume à déménager, la distance et les services choisis. Le devis est gratuit et sans engagement."),
        ("Fournissez-vous les cartons et le matériel&nbsp;?", "Nous mettons à disposition le matériel nécessaire à l’emballage le jour du déménagement. Pour des cartons à l’avance, précisez-le dans votre demande."),
        ("Faites-vous les déménagements à l’étranger&nbsp;?", "Oui. Nous déménageons partout en Suisse et dans les pays voisins."),
        ("Proposez-vous un garde-meubles&nbsp;?", "Oui, en collaboration avec un espace de stockage partenaire, si vous avez besoin d’entreposer vos meubles entre deux logements."),
        ("Pouvez-vous aussi nettoyer l’ancien logement&nbsp;?", "Oui. C’est notre offre déménagement + nettoyage de fin de bail&nbsp;: une seule équipe, des dates coordonnées et un seul devis."),
        ("Combien de temps à l’avance réserver&nbsp;?", "Le plus tôt possible, surtout pour les fins de mois, qui sont très demandées. Indiquez la date souhaitée dans votre demande."),
        faq_zone("Nous déménageons depuis et vers toutes les communes du canton de Genève"),
        FAQ_PAY,
    ],
)


def dem_body(p, rel):
    svc = p["slug"]
    groups = [
        ("doc", "Avant le jour J", ["Estimation du volume et devis", "Matériel d’emballage fourni le jour du déménagement", "Planification de la date et de l’accès"]),
        ("box", "Emballage et meubles", ["Emballage et déballage soignés", "Démontage des grands meubles", "Remontage dans le nouveau logement"]),
        ("truck", "Transport", ["Nos propres véhicules, adaptés au volume", "Chargement protégé et arrimé", "Sangles, chariots et diables pour la manutention"]),
        ("key", "Et aussi", ["Déménagements en Suisse et dans les pays voisins", "Garde-meubles avec un partenaire", "Nettoyage de fin de bail de l’ancien logement"]),
    ]
    combo = f"""<section class="sec" aria-labelledby="combo-t" data-service="demenagement-nettoyage"><div class="wrap">
<div class="combo"><div class="combo-media"><div class="frame">{pic(rel, "stock/cartons-salon", "Cartons de déménagement dans un salon", "(min-width: 960px) 25vw, 50vw")}</div><div class="frame">{pic(rel, "stock/appartement-vide", "Appartement vide et propre", "(min-width: 960px) 25vw, 50vw")}</div></div>
<div class="combo-body"><p class="combo-plus">{ic("truck")}Déménagement {ic("plus")} nettoyage de fin de bail {ic("spark")}</p><h2 id="combo-t">Une seule équipe pour tout votre départ</h2>
<p>Le jour du déménagement, nous vidons l’appartement. Ensuite, nous le nettoyons pour l’état des lieux&nbsp;: four, calcaire, vitres, stores, armoires. Un interlocuteur, un devis.</p>
<div class="cta-row">{b_wa("demenagement-nettoyage", "combo", "Bonjour, je souhaite un devis pour un déménagement avec nettoyage de fin de bail.", "Devis déménagement + nettoyage")}<a class="btn btn-line" href="{rel}nettoyage-fin-de-bail-geneve/" data-loc="dem-to-fdb">Le nettoyage de fin de bail{ic("arrow")}</a></div></div></div>
</div></section>"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky"><h2 id="inc-t">Ce qui est inclus</h2><p style="color:var(--muted)">Vous choisissez les services dont vous avez besoin, nous les détaillons dans le devis.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/demenagement-cartons", "Déménageur à l’arrière d’une camionnette chargée de cartons", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups)}
{cta_row(svc, "checklist", p["wa"], order="qcw")}</div>
</div></section>
{combo}
<section class="sec sec--white" aria-labelledby="gal-t"><div class="wrap">
{head_block("", "Du premier carton au dernier meuble").replace("<h2>", '<h2 id="gal-t">')}
{gallery(rel, [("stock/demenagement-camionnette", "Chargement de cartons dans une camionnette", "Chargement protégé"),
               ("stock/demenagement-diable", "Transport de cartons au diable", "Manutention au diable"),
               ("stock/cartons-salon", "Préparation des cartons dans un salon", "Emballage")])}
</div></section>
{steps_block(svc, "", p["wa"], steps=[
        ("Vous demandez un devis", "Indiquez la date, les adresses et la taille du logement. Des photos des pièces nous aident à estimer le volume."),
        ("On estime le volume et fixe la date", "Nous évaluons le volume, sur place si nécessaire, et vous remettons un devis gratuit et sans engagement."),
        ("On déménage", "Emballage, démontage, transport et remontage le jour convenu. Si vous le souhaitez, nous nettoyons ensuite l’ancien logement.")])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Déménagements depuis tout le canton de Genève")}"""


DEM["body"] = dem_body
PAGES.append(DEM)

# ---------------- RENOVATION
REN = dict(
    kind="renovation", slug="renovation", path="renovation-peinture-geneve/", crumb="Rénovation et peinture à Genève",
    title="Rénovation et peinture Genève · Appartement, salle de bain · Devis gratuit",
    desc="Rénovation et peinture à Genève : murs, plafonds, boiseries, plaques de plâtre, salle de bain et cuisine. Entreprise familiale de Chêne-Bourg, devis gratuit après visite.",
    h1="Rénovation et peinture à Genève",
    sub="Peinture d’appartement, salle de bain, plâtrerie&nbsp;: une entreprise familiale de Chêne-Bourg rafraîchit votre intérieur, avec une visite rapide et un devis gratuit, partout dans le canton de Genève.",
    hero_img="stock/salle-de-bain-renovee", form_default="Rénovation / peinture",
    wa="Bonjour, je souhaite un devis pour des travaux de rénovation ou de peinture.",
    service_ld=("Rénovation et peinture à Genève : appartement, salle de bain, cuisine", "Rénovation et peinture"),
    faqs=[
        ("Venez-vous voir avant de faire le devis&nbsp;?", "Oui. Nous nous déplaçons pour évaluer le travail sur place, puis vous remettons un devis personnalisé, gratuit et sans engagement."),
        ("Pouvez-vous peindre un logement habité&nbsp;?", "Oui. Nous protégeons les sols et les meubles avant de commencer et laissons les pièces propres en fin de journée."),
        ("Faites-vous aussi le sanitaire de la salle de bain&nbsp;?", "Oui, c’est l’avantage d’une entreprise multiservice&nbsp;: le sanitaire, la rénovation et la peinture sont faits par la même équipe."),
        ("La peinture et les fournitures sont-elles comprises&nbsp;?", "Le matériel et les fournitures sont détaillés dans le devis, pour que vous sachiez exactement ce qui est compris."),
        ("Combien de temps durent les travaux&nbsp;?", "Cela dépend de la surface et de l’état des murs. Nous vous donnons une durée estimée avec le devis."),
        faq_zone(),
        FAQ_PAY,
    ],
)


def ren_body(p, rel):
    svc = p["slug"]
    groups = [
        ("roller", "Peinture", ["Murs et plafonds", "Boiseries&nbsp;: portes, cadres, plinthes", "Sols", "Remise en peinture avant un état des lieux"]),
        ("home", "Préparation et finitions", ["Protection des sols et des meubles", "Rebouchage des trous et fissures", "Ponçage et sous-couche", "Joints et finitions soignées"]),
        ("building", "Plâtrerie", ["Pose de plaques de plâtre", "Cloisons et faux plafonds", "Réparation de surfaces abîmées"]),
        ("bath", "Salle de bain et cuisine", ["Rénovation de salle de bain", "Remplacement des équipements sanitaires", "Rénovation de cuisine",
                                              "Coordination sanitaire, rénovation et peinture"]),
    ]
    s1 = f"""<h2>Une salle de bain refaite par une seule équipe</h2>
<p>Démontage, sanitaire, plâtrerie et peinture&nbsp;: le sanitaire fait partie de nos métiers, vous n’avez donc pas à coordonner plusieurs artisans.</p>
<ul class="check"><li>Remplacement des appareils et de la robinetterie</li><li>Plaques de plâtre et finitions</li><li>Peinture adaptée aux pièces humides</li></ul>
{cta_row(svc, "split-sdb", p["wa"], quote="Demander une visite", order="qw")}"""
    s2 = f"""<h2>Rafraîchir un appartement</h2>
<p>Avant d’emménager, avant de vendre ou avant un état des lieux&nbsp;: nous repeignons murs, plafonds et boiseries proprement, en protégeant tout ce qui doit l’être.</p>
{cta_row(svc, "split-peinture", p["wa"], order="qc")}"""
    return f"""{trustbar()}
<section class="sec sec--white" aria-labelledby="inc-t"><div class="wrap cols cols--4-8">
<div><div class="sticky"><h2 id="inc-t">Nos travaux</h2><p style="color:var(--muted)">Dans les appartements, les villas et les bureaux.</p>
<div class="frame frame--45" style="margin-top:24px">{pic(rel, "stock/peinture-rouleau", "Mur repeint au rouleau", "(min-width: 960px) 30vw, 100vw")}</div></div></div>
<div>{checklist(groups)}
{cta_row(svc, "checklist", p["wa"], order="qcw")}</div>
</div></section>
<section class="sec" aria-label="Salle de bain et peinture"><div class="wrap">
{split(rel, "stock/salle-de-bain-renovee", "Salle de bain rénovée avec douche vitrée", s1)}
{split(rel, "stock/peintre-mur", "Peinture d’un mur au rouleau", s2, rev=True)}
</div></section>
<section class="sec sec--white" aria-labelledby="gal-t"><div class="wrap">
{head_block("", "Préparer, protéger, finir").replace("<h2>", '<h2 id="gal-t">')}
{gallery(rel, [("stock/peintre-facade", "Peintre sur une échelle devant une façade", "Peinture des boiseries et encadrements"),
               ("stock/joints-cuisine", "Finitions et joints dans une cuisine", "Joints et finitions"),
               ("stock/nuancier", "Nuancier de couleurs et échantillons", "Choix des teintes")])}
</div></section>
{steps_block(svc, "", p["wa"], steps=[
        ("Vous nous décrivez le projet", "Par téléphone, sur WhatsApp ou avec le formulaire. Ajoutez des photos des pièces concernées."),
        ("On vient voir et on chiffre", "Nous évaluons le travail sur place et vous remettons un devis gratuit, avec le détail des travaux et des fournitures."),
        ("On réalise les travaux", "Protection, préparation, travaux et finitions, puis nous laissons les pièces propres.")])}
{team_block(rel, svc, short=True)}
{reviews_block()}
{faq_block(p["faqs"], "sec")}
{zone_block(svc, "sec sec--sand", "Rénovation et peinture dans tout le canton")}"""


REN["body"] = ren_body
PAGES.append(REN)


# ------------------------------------------------------------------ assembly
def render(p):
    depth = p["path"].count("/")
    rel = "../" * depth
    body = p["body"](p, rel)
    doc = (head(p, rel) +
           f'\n<body data-service="{p["slug"]}">\n{SPRITE}\n'
           f'{header(rel, p["slug"], nav=(p["kind"] == "home"))}\n'
           f'<main id="main">\n{hero(p, rel)}\n{body}\n{final_cta(p)}\n</main>\n'
           f'{footer(rel)}\n{contact_bar(p["slug"], p["wa"])}\n{scripts(rel)}\n</body>\n</html>\n')
    return typo(doc)


def simple_page(path, kind, title, desc, h1, intro, content, noindex=False, slug="general", wa_text="Bonjour, je souhaite un renseignement."):
    depth = path.count("/")
    rel = "../" * depth
    p = dict(kind=kind, slug=slug, path=path, title=title, desc=desc, noindex=noindex, wa=wa_text)
    quote_href = f"{rel}#devis"
    bar = contact_bar(slug, wa_text).replace('href="#devis"', f'href="{quote_href}"')
    doc = (head(p, rel) +
           f'\n<body data-service="{slug}">\n{SPRITE}\n{header(rel, slug, quote_href=quote_href)}\n'
           f'<main id="main">\n<div class="page-hd"><div class="wrap"><h1>{h1}</h1>{f"<p>{intro}</p>" if intro else ""}</div></div>\n{content}\n</main>\n'
           f'{footer(rel)}\n{bar}\n{scripts(rel)}\n</body>\n</html>\n')
    return typo(doc)


def merci_page():
    rel = "../"
    content = f"""<section class="thanks"><div class="wrap prose">
<div class="tick">{ic("check")}</div>
<h2>Nous vous rappelons</h2>
<p>Votre demande nous est bien parvenue. Nous vous rappelons au numéro indiqué pour en discuter et fixer les détails du devis.</p>
<p><b>C’est urgent&nbsp;?</b> Une fuite, une panne de chauffage&nbsp;: appelez-nous directement, c’est le plus rapide.</p>
<div class="btns">{b_call("merci", "merci", f'Appeler le <span class="nw" data-phone>{PHONE}</span>')}{b_wa("merci", "merci", "Bonjour, je viens d’envoyer une demande de devis. Voici une photo :", "Envoyer une photo sur WhatsApp")}<a class="btn btn-line" href="{rel}">Retour à l’accueil</a></div>
<p style="color:var(--muted)">Vous pouvez aussi nous envoyer des photos sur WhatsApp&nbsp;: elles nous aident à préparer le devis.</p>
</div></section>"""
    return simple_page("merci/", "merci", "Merci, votre demande est envoyée · Zeka D-Services",
                       "Votre demande de devis a bien été envoyée à Zeka D-Services.", "Merci, votre demande est envoyée",
                       None, content, noindex=True, slug="merci")


def credits_html():
    stock = json.loads((ROOT / "tools" / "stock.json").read_text())
    lis = "".join(
        f'<li>{esc(r[5])}&nbsp;: <a href="{esc(r[3])}" rel="nofollow noopener" target="_blank">{esc(r[4])}</a> sur {"Unsplash" if r[1] == "unsplash" else "Pexels"}</li>'
        for r in stock)
    lis += ('<li>Vidéo sanitaire&nbsp;: <a href="https://www.pexels.com/video/7584762/" rel="nofollow noopener" target="_blank">Stepan SK</a> sur Pexels</li>'
            '<li>Vidéo nettoyage&nbsp;: <a href="https://www.pexels.com/video/6195524/" rel="nofollow noopener" target="_blank">Tima Miroshnichenko</a> sur Pexels</li>'
            '<li>Carte du canton&nbsp;: données © <a href="https://www.openstreetmap.org/copyright" rel="nofollow noopener" target="_blank">contributeurs OpenStreetMap</a> (ODbL)</li>')
    return f'<ul class="credit-list">{lis}</ul>'


def legal_page():
    content = f"""<section class="sec sec--white"><div class="wrap prose">
<h2>Éditeur du site</h2>
<p><b>Zeka D-Services</b><br>{ADDRESS[0]}<br>{ADDRESS[1]} {ADDRESS[2]}, Suisse</p>
<p>Téléphone&nbsp;: <a href="{TEL}" data-loc="legal"><span data-phone>{PHONE}</span></a><br>E-mail&nbsp;: <a href="#" data-email>voir la page de contact</a></p>
<h2>Hébergement</h2>
<p>Le site est hébergé par GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, le logo et la mise en page de ce site appartiennent à Zeka D-Services. Toute reproduction sans autorisation écrite est interdite. Les photographies et vidéos proviennent de banques d’images libres de droits (Unsplash et Pexels), dont les auteurs sont cités ci-dessous.</p>
<h2>Responsabilité</h2>
<p>Les informations de ce site sont fournies à titre indicatif. Seul le devis remis par Zeka D-Services fait foi pour le contenu, le prix et les conditions d’une prestation. Les liens vers d’autres sites sont fournis par commodité&nbsp;; nous ne sommes pas responsables de leur contenu.</p>
<h2>Protection des données</h2>
<p>Le traitement des données envoyées par le formulaire est décrit dans notre <a href="../confidentialite/">déclaration de protection des données</a>.</p>
<h2 id="credits">Crédits photos et vidéos</h2>
{credits_html()}
</div></section>"""
    return simple_page("mentions-legales/", "legal", "Mentions légales · Zeka D-Services",
                       "Mentions légales du site de Zeka D-Services, entreprise familiale multiservice à Chêne-Bourg (Genève).",
                       "Mentions légales", None, content)


def privacy_page():
    content = f"""<section class="sec sec--white"><div class="wrap prose">
<p>Cette déclaration explique quelles données personnelles nous traitons lorsque vous utilisez ce site, conformément à la loi fédérale sur la protection des données (LPD, nLPD en vigueur depuis le 1<sup>er</sup> septembre 2023).</p>
<h2>Responsable du traitement</h2>
<p>Zeka D-Services, {ADDRESS[0]}, {ADDRESS[1]} {ADDRESS[2]}, Suisse. Téléphone&nbsp;: <span data-phone>{PHONE}</span>. E-mail&nbsp;: <a href="#" data-email>adresse e-mail</a>.</p>
<h2>Données collectées par les formulaires</h2>
<p>Lorsque vous demandez un devis ou un rappel, nous recevons les informations que vous saisissez&nbsp;: service souhaité, taille du logement, date, urgence, nom, numéro de téléphone, localité, adresse e-mail (facultative) et message. Nous recevons aussi la page d’où vous avez envoyé la demande et, si vous êtes arrivé par une annonce, les paramètres de campagne de l’adresse (par exemple gclid ou utm_source).</p>
<h2>Finalité</h2>
<p>Ces données servent uniquement à répondre à votre demande, à vous recontacter, à établir le devis et, le cas échéant, à réaliser la prestation. Les paramètres de campagne nous permettent de savoir quelles annonces sont utiles. Nous ne vendons pas vos données et ne les utilisons pas pour de la prospection sans votre accord.</p>
<h2>Sous-traitants et transfert à l’étranger</h2>
<ul>
<li><b>FormSubmit</b> (formsubmit.co) transmet le contenu des formulaires à notre adresse e-mail. Le service peut traiter les données hors de Suisse.</li>
<li><b>Google</b> (messagerie e-mail) reçoit et conserve les demandes envoyées à notre adresse. Les données peuvent être traitées hors de Suisse, notamment aux États-Unis.</li>
<li><b>WhatsApp</b> (Meta) traite les messages si vous choisissez de nous écrire par WhatsApp, selon ses propres conditions.</li>
<li><b>GitHub Pages</b> héberge le site et peut enregistrer des données techniques de connexion (adresse IP, navigateur) pour des raisons de sécurité.</li>
<li><b>Google Ads</b>&nbsp;: si la mesure des conversions est activée, Google peut déposer des cookies et traiter des données de navigation pour mesurer l’efficacité de nos annonces. Vous pouvez gérer ces cookies dans les réglages de votre navigateur et dans vos paramètres publicitaires Google.</li>
</ul>
<p>Lorsque des données sont transférées dans un pays sans niveau de protection adéquat, nous nous appuyons sur les garanties contractuelles prévues par ces prestataires.</p>
<h2>Durée de conservation</h2>
<p>Nous conservons vos données le temps nécessaire au traitement de votre demande et à la relation commerciale, puis pendant la durée imposée par les obligations légales, notamment comptables.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander à tout moment l’accès à vos données, leur rectification ou leur effacement, et vous opposer à leur traitement. Écrivez-nous ou appelez-nous aux coordonnées ci-dessus. Vous pouvez aussi vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT).</p>
<h2>Stockage dans votre navigateur</h2>
<p>Le site garde dans votre navigateur, pendant la visite uniquement (sessionStorage), les paramètres de campagne de l’adresse et l’information qu’une demande a été envoyée. Ces données sont effacées à la fermeture de l’onglet.</p>
<p style="color:var(--muted)">Version d’octobre 2026.</p>
</div></section>"""
    return simple_page("confidentialite/", "privacy", "Protection des données · Zeka D-Services",
                       "Déclaration de protection des données (nLPD) du site de Zeka D-Services : formulaires, sous-traitants, durée de conservation et vos droits.",
                       "Protection des données", None, content)


def page_404():
    """GitHub Pages serves 404.html for any missing URL, at any depth, so relative links can't be known
    in advance. A tiny inline script writes a <base> pointing at the site root (the folder that holds
    this site), so every relative link below works from wherever the visitor landed."""
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in SERVICE_LINKS)
    p = dict(kind="404", slug="general", path="404.html", title="Page introuvable · Zeka D-Services",
             desc="Cette page n’existe pas ou a été déplacée.", noindex=True)
    doc = head(p, "")
    base = ("<script>(function(){var p=location.pathname,i=p.indexOf('/zekadservices/');"
            "var b=i>-1?p.slice(0,i+15):'/';document.write('<base href=\"'+b+'\">');})();</script>")
    doc = doc.replace("<meta charset=\"utf-8\">", "<meta charset=\"utf-8\">\n" + base, 1)
    doc += f"""
<body data-service="general">
{SPRITE}
{header("", "general", quote_href="./#devis")}
<main id="main"><div class="page-hd"><div class="wrap"><h1>Cette page n’existe pas</h1><p>Le lien est peut-être ancien. Voici nos services, ou appelez-nous directement.</p></div></div>
<section class="sec sec--white"><div class="wrap prose"><ul class="check">{links}</ul>
<div class="cta-row">{b_call("general", "404", "Appeler maintenant")}<a class="btn btn-line" href="./">Retour à l’accueil</a></div></div></section></main>
{footer("")}
{scripts("")}
</body>
</html>
"""
    return typo(doc)


def main():
    out = []
    for p in PAGES:
        path = ROOT / p["path"] / "index.html" if p["path"] else ROOT / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(p))
        out.append(p["path"])
    for path, html_doc in [("merci/", merci_page()), ("mentions-legales/", legal_page()), ("confidentialite/", privacy_page())]:
        (ROOT / path).mkdir(parents=True, exist_ok=True)
        (ROOT / path / "index.html").write_text(html_doc)
    (ROOT / "404.html").write_text(page_404())
    (ROOT / "css").mkdir(exist_ok=True)
    (ROOT / "css" / "site.css").write_text("/* Generated by tools/build.py from tools/site.css. Edit the source, not this file. */\n" + REST_MIN + "\n")
    indexable = [p["path"] for p in PAGES] + ["mentions-legales/", "confidentialite/"]
    sm = "".join(f"<url><loc>{BASE_URL}{u}</loc><lastmod>2026-10-21</lastmod></url>" for u in indexable)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")
    print("built", len(out) + 4, "pages")


if __name__ == "__main__":
    main()
