/* Customer reviews, copied word for word from the Google Business Profile.
   tools/build.py reads this file and writes the reviews into every page (no JavaScript needed to see them).
   After editing: run `python3 tools/build.py`. Keep strict JSON between "=" and ";" (double quotes, no trailing commas).
   Only real reviews. Name = first name + initial, as a privacy courtesy.
   An empty ZEKA_REVIEWS list hides the review section and the rating badges. */
window.ZEKA_GOOGLE = {
  "rating": 5.0,
  "count": 3,
  "url": "https://search.google.com/local/reviews?placeid=ChIJo5cPZFFvjEcRMiAn7vbA4j0",
  "maps": "https://maps.google.com/?cid=4459338747840241714"
};
window.ZEKA_REVIEWS = [
  {
    "name": "Mati M.",
    "rating": 5,
    "service": "Déménagement et fin de bail",
    "text": "Nous avons utiliser leurs services pour déménagement et nettoyages de fin de bail. Le service était très professionnel, satisfaisant et agréable. Nous recommandons chaudement !"
  },
  {
    "name": "Thomas C.",
    "rating": 5,
    "service": "",
    "text": "Poli, à l'heure, super efficace, allez-y les yeux fermés. Ca fait plaisir de rencontrer des gens aussi pro !"
  },
  {
    "name": "Eric V.",
    "rating": 5,
    "service": "",
    "text": "Ponctuels, rapport qualité-prix excellent, travaux parfaitement exécutés"
  }
];
