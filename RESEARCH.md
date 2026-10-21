# Research

Done on 21 October 2026, before building. Two parts: the current Zeka D-Services site, then the local service landing pages that convert best.

## 1. The current site (zekadservices.ch)

A Duda template made by localsearch.ch in 2023: Accueil, À propos, Les prestations, Contact, Mentions légales.

- **Content we kept:** the company story (three brothers, 6 to 10 years of experience each), the address and phone number, the four activities, and the service details from "Les étapes de notre travail". Those details include on-site evaluation, their own vehicles, a storage partner, packing material, heat pumps and solar thermal.
- **Problems:**
  - Template leftovers on every page ("Slide title", "Write your caption here", "Titre de la diapositive", "Button").
  - No form above the fold and no WhatsApp.
  - A single "Appelez-nous !" button.
  - Mismatched photos: a cleaning bucket on the moving card, a vacuum on the sanitaire card.
- **Colours:** buttons `#1480BA` (rgb 20,128,186) and logo wordmark `#3980BA`.
- **Not used on the new site** (they are listed in TODO-CONFIRM.md instead): founding date, second phone number, opening hours, languages spoken, the Genève & Vaud zone, and the Implenia / Losinger Marazzi and Ad Hoc SA references.

## 2. Benchmark

We reviewed 15 pages: 11 from Geneva and Lausanne, plus Roto-Rooter (US), Pimlico Plumbers (UK), Fantastic Services end of tenancy (UK) and a Brisbane bond-cleaning page (AU).

The Geneva and Lausanne pages were:
- plombier-urgence-geneve.ch, sosplomberie.ch, swissbatplomberie.ch, hugodubois.ch
- chauffagegeneve.ch
- maxiclean.ch, fiditi.ch, fly-demenagement.ch, idnettoyage.ch, nettoyage-fin-bail.ch
- dio-net.ch

## Patterns reused, and why

| Pattern | Seen on | Why it converts | Where it is on our site |
|---|---|---|---|
| Headline that repeats the search, problem first | PUG, sosplomberie | The visitor sees their own query and the answer in one line, which also helps Ads Quality Score | One H1 per landing page ("Plombier à Genève, intervention rapide") |
| Call button and quote button side by side in the hero | all top plumbers | Urgent visitors call. Others want something they can do without talking to anyone | Both in every hero; call first on plumbing and heating |
| Pre-filled WhatsApp message per service | chauffagegeneve, PUG, dio-net | The lowest-friction contact in Switzerland, and the message arrives already labelled | Every WhatsApp link carries a message written for that service |
| Ask for photos as part of the quote | swissbat, dio-net, fiditi, Fantastic | Lets them quote without a visit and sort the request before going out | Photo note in the form, "Envoyer une photo" buttons, FAQ |
| Short form with the problem chosen first | swissbat (but 10 fields), sosplomberie (6 required) | Every extra required field loses leads | 2 steps. Step 1 is taps only; step 2 has 2 required fields |
| Problem chips | swissbat dropdown, hugodubois service cards | Tapping is quicker than typing and tells the company what to bring | "Votre problème ?" chips in the plumbing and heating heroes |
| Pick the number of rooms | fiditi | A small first step that leads into the form | "Votre logement ?" chips in the fin de bail hero (without prices) |
| Room-by-room checklist | Fantastic, maxiclean | People compare quotes line by line, and the list answers "is the oven included?" without a phone call | "Ce qui est inclus" on every landing page |
| Talk to régies and insurance | PUG (régie billing), swissbat (insurers) | In Geneva the régie or the insurer is often involved | FAQ "Je suis locataire…", band tips about photos for the régie |
| Moving + cleaning in one offer | fly-demenagement | It fits a multiservice company: one date, one contact | Combo block on the home, fin de bail and moving pages |
| Process in 3 steps | sosplomberie, chauffagegeneve | Answers "what happens after I click?" | "Comment ça se passe", numbered |
| Practical advice before the call | none of the Geneva sites do this well | It is genuinely helpful, and nothing like it appears on competing sites | "En attendant notre arrivée" and "Avant d'appeler" bands |
| Mobile call bar, sticky header phone | most plumbers | The phone is always one tap away | Appeler · WhatsApp · Devis bar, hidden over the form |

## Anti-patterns avoided

- **Figures that contradict each other** (118 vs 500+ reviews, 30 min vs 1 h, "7j/7" vs posted hours). We publish no figures we can't back up.
- **Recycled or unverifiable testimonials and ratings.** The review section exists but stays hidden until real Google reviews are added.
- **Vanity numbers** ("99,6 % de réussite", "100 % garantie") and **unsourced guarantees.** The guarantee wording is waiting on the owner (see TODO-CONFIRM.md).
- **Long lists of commune links** on an Ads landing page. Communes are shown as plain labels next to a map, not as SEO link farms.
- **No phone number on a fin de bail page** (maxiclean). Ours is in the header, hero, mobile bar, every section's CTAs and the footer.
