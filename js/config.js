/* Zeka D-Services · site settings.
   Change a value here and the whole site follows (links, form, tracking).
   After changing the phone number, also run `python3 tools/build.py` so the
   static HTML (what Google and visitors without JavaScript see) matches. */
window.ZEKA = {
  // Contact
  PHONE_DISPLAY: "078 639 50 66",
  PHONE_E164: "+41786395066",          // used for tel: links
  WHATSAPP: "41786395066",             // wa.me number, digits only, no +
  EMAIL: "zeka.ge.services@gmail.com", // shown on the site AND receives the quote requests

  // Form delivery (FormSubmit AJAX). The first real submission sends an activation
  // e-mail to EMAIL: click the link once, then every request arrives in that inbox.
  FORM_ENDPOINT: "https://formsubmit.co/ajax/",

  // Google Ads. Leave empty to load nothing. Example: "AW-1234567890"
  GOOGLE_ADS_ID: "",
  // Conversion labels from Google Ads (Objectifs > Conversions). Example: "AbCdEfGhIjKlMnOp"
  CONVERSION_LABELS: {
    lead: "",      // fired once on the merci/ page after a quote request
    call: "",      // fired on every tap on a phone number
    whatsapp: ""   // fired on every WhatsApp click
  }
};
