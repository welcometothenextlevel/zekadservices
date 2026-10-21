/* Zeka D-Services · site behaviour (vanilla JS, no dependencies).
   Settings live in js/config.js, reviews in js/reviews.js. */
(function () {
  "use strict";
  var C = window.ZEKA || {};
  var doc = document;
  var html = doc.documentElement;
  var ROOT = html.getAttribute("data-root") || "";
  var PAGE_SERVICE = doc.body.getAttribute("data-service") || "general";
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  function store(k, v) {
    try {
      if (v === undefined) return window.sessionStorage.getItem(k);
      if (v === null) return window.sessionStorage.removeItem(k);
      window.sessionStorage.setItem(k, v);
    } catch (e) { return null; }
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- 1. keep phone / WhatsApp / e-mail in sync with config.js ---------- */
  var BUILT_TEL = "tel:+41786395066", BUILT_WA = "41786395066";
  if (C.PHONE_E164 && "tel:" + C.PHONE_E164 !== BUILT_TEL) {
    $$('a[href^="tel:"]').forEach(function (a) { a.setAttribute("href", "tel:" + C.PHONE_E164); });
    $$("[data-phone]").forEach(function (el) { el.textContent = C.PHONE_DISPLAY; });
  }
  if (C.WHATSAPP && C.WHATSAPP !== BUILT_WA) {
    $$('a[href*="wa.me/' + BUILT_WA + '"]').forEach(function (a) {
      a.setAttribute("href", a.getAttribute("href").replace("wa.me/" + BUILT_WA, "wa.me/" + C.WHATSAPP));
    });
  }
  $$("[data-email]").forEach(function (el) {
    if (!C.EMAIL) return;
    el.textContent = C.EMAIL;
    if (el.tagName === "A") el.setAttribute("href", "mailto:" + C.EMAIL);
  });

  /* ---------- 2. tracking: dataLayer always, Google Ads only if configured ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  var ADS = C.GOOGLE_ADS_ID || "";
  var LABELS = C.CONVERSION_LABELS || {};
  if (ADS) {
    var gs = doc.createElement("script");
    gs.async = true;
    gs.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ADS);
    doc.head.appendChild(gs);
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", ADS);
  }
  var CONVERSION_FOR = { call_click: "call", whatsapp_click: "whatsapp", merci_view: "lead" };
  function track(ev, params) {
    params = params || {};
    var o = { event: ev, page_service: PAGE_SERVICE };
    for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k) && k !== "convert") o[k] = params[k];
    window.dataLayer.push(o);
    if (ADS) {
      gtag("event", ev, o);
      var label = LABELS[CONVERSION_FOR[ev]];
      if (label && params.convert !== false) gtag("event", "conversion", { send_to: ADS + "/" + label });
    }
  }
  window.zekaTrack = track;

  /* ---------- 3. keep gclid / UTM for the whole visit ---------- */
  var ATTR = ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
  var attr = {};
  try { attr = JSON.parse(store("zeka_attr") || "{}") || {}; } catch (e) { attr = {}; }
  try {
    var qs = new URLSearchParams(window.location.search), changed = false;
    ATTR.forEach(function (k) { var v = qs.get(k); if (v) { attr[k] = v.slice(0, 200); changed = true; } });
    if (!attr.landing_page) { attr.landing_page = window.location.pathname; changed = true; }
    if (changed) store("zeka_attr", JSON.stringify(attr));
  } catch (e) { /* old browser: no attribution */ }
  function fillAttr(form) {
    ATTR.concat(["landing_page"]).forEach(function (k) {
      var i = form.querySelector('input[name="' + k + '"]');
      if (i && attr[k]) i.value = attr[k];
    });
  }

  /* ---------- 4. click events on every call / WhatsApp / quote link ---------- */
  function serviceOf(el) {
    var s = el.closest("[data-service]");
    return (s && s.getAttribute("data-service")) || PAGE_SERVICE;
  }
  doc.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";
    var p = { service: serviceOf(a), placement: a.getAttribute("data-loc") || "" };
    if (href.indexOf("tel:") === 0) track("call_click", p);
    else if (href.indexOf("wa.me/") > -1) track("whatsapp_click", p);
    else if (href === "#devis") {
      track("quote_cta_click", p);
      var target = doc.getElementById("devis");
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
        var t = $(".qf-title", target);
        if (t) setTimeout(function () { t.focus({ preventScroll: true }); }, reduced ? 0 : 450);
        if (history.replaceState) history.replaceState(null, "", "#devis");
      }
    }
  });

  /* ---------- 5. forms ---------- */
  var MSG = {
    service: "Choisissez le service qui vous intéresse.",
    nom: "Indiquez votre nom.",
    telephone: "Indiquez un numéro de téléphone valide, par exemple 078 123 45 67.",
    email: "Cette adresse e-mail ne semble pas complète.",
    fail: "L'envoi n'a pas fonctionné. Appelez-nous au " + (C.PHONE_DISPLAY || "078 639 50 66") + " ou écrivez-nous sur WhatsApp, nous vous répondons directement."
  };
  function setErr(input, msg) {
    var f = input.closest(".field");
    var el = f && f.querySelector(".err");
    input.setAttribute("aria-invalid", msg ? "true" : "false");
    if (el) el.textContent = msg || "";
    return !msg;
  }
  function checkField(input) {
    var v = (input.value || "").trim();
    switch (input.name) {
      case "nom": return setErr(input, v.length >= 2 ? "" : MSG.nom);
      case "telephone":
        var digits = v.replace(/\D/g, "");
        return setErr(input, digits.length >= 9 && digits.length <= 15 ? "" : MSG.telephone);
      case "email": return setErr(input, !v || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? "" : MSG.email);
    }
    return true;
  }
  function selectedService(form) {
    var r = form.querySelector('input[name="service"]:checked');
    if (r) return r.value;
    var s = form.querySelector('select[name="service"]');
    return s ? s.value : "";
  }

  function setupForm(form) {
    fillAttr(form);
    var steps = $$(".qf-step", form);
    var stepLabel = $(".qf-steplabel b", form);
    var status = $(".qf-status", form);
    var s1err = $(".qf-step1-err", form);

    function show(n, focus) {
      form.setAttribute("data-step", n);
      steps.forEach(function (s) { s.hidden = +s.getAttribute("data-step") !== n; });
      if (stepLabel) stepLabel.textContent = n;
      if (focus) {
        var first = $('.qf-step[data-step="' + n + '"] input:not([type=hidden]), .qf-step[data-step="' + n + '"] legend', form);
        if (first && first.tagName === "INPUT" && first.type !== "radio") first.focus();
      }
    }
    form.zekaShow = show;

    function conditional() {
      var v = selectedService(form);
      $$(".qf-cond", form).forEach(function (el) {
        el.hidden = el.getAttribute("data-for").split("|").indexOf(v) < 0;
      });
    }
    form.zekaConditional = conditional;
    form.addEventListener("change", function (e) {
      if (e.target.name === "service") {
        conditional();
        if (s1err) s1err.textContent = "";
      }
    });
    conditional();

    var next = $(".qf-next", form);
    if (next) next.addEventListener("click", function () {
      if (!selectedService(form)) {
        if (s1err) s1err.textContent = MSG.service;
        var c = $('input[name="service"]', form);
        if (c) c.focus();
        return;
      }
      track("form_step2", { service: selectedService(form) });
      show(2, true);
    });
    var back = $(".qf-back", form);
    if (back) back.addEventListener("click", function () { show(1); var c = $('input[name="service"]:checked', form); if (c) c.focus(); });

    $$("input[name=nom], input[name=telephone], input[name=email]", form).forEach(function (i) {
      i.addEventListener("blur", function () { if (i.value.trim() || i.getAttribute("aria-invalid") === "true") checkField(i); });
      i.addEventListener("input", function () { if (i.getAttribute("aria-invalid") === "true") checkField(i); });
    });

    $$('input[type="date"]', form).forEach(function (d) {
      try { d.min = new Date().toISOString().slice(0, 10); } catch (e) {}
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.classList.contains("qf") && !selectedService(form)) { show(1); if (s1err) s1err.textContent = MSG.service; return; }
      var ok = true, firstBad = null;
      $$("input[name=nom], input[name=telephone], input[name=email]", form).forEach(function (i) {
        if (!checkField(i)) { ok = false; firstBad = firstBad || i; }
      });
      if (!ok) { firstBad.focus(); return; }

      var data = {};
      new FormData(form).forEach(function (v, k) {
        if (typeof v === "string" && v.trim() !== "") data[k] = v.trim();
      });
      var service = data.service || "Demande de rappel";
      if (data._honey) { window.location.href = ROOT + "merci/"; return; }
      data._subject = "Nouvelle demande · " + service + " · " + (data.localite || "localité non précisée");
      data._template = "table";
      data._captcha = "false";
      if (data.email) data._replyto = data.email;
      data.page = window.location.pathname;

      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.setAttribute("aria-busy", "true"); }
      if (status) { status.className = "qf-status"; status.textContent = "Envoi en cours…"; }

      fetch((C.FORM_ENDPOINT || "https://formsubmit.co/ajax/") + C.EMAIL, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; });
      }).then(function (res) {
        if (!(res.ok && (res.j.success === true || res.j.success === "true"))) throw new Error(res.j.message || "send");
        track("generate_lead", { service: service, form: form.id, localite: data.localite || "" });
        store("zeka_lead", JSON.stringify({ service: service, t: Date.now() }));
        if (status) status.textContent = "Merci, votre demande est envoyée.";
        setTimeout(function () { window.location.href = ROOT + "merci/"; }, 250);
      }).catch(function () {
        track("form_error", { service: service, form: form.id });
        if (status) {
          status.className = "qf-status is-err";
          status.textContent = MSG.fail;
        }
        if (btn) { btn.disabled = false; btn.removeAttribute("aria-busy"); }
      });
    });
  }
  $$("form.qf, form.cb").forEach(setupForm);

  /* ---------- 6. "Votre problème" chips and room-count shortcuts ---------- */
  var qf = doc.getElementById("quote-form");
  function pick(form, name, value) {
    var r = form.querySelector('input[name="' + name + '"][value="' + value + '"]');
    if (r) { r.checked = true; r.dispatchEvent(new Event("change", { bubbles: true })); }
  }
  var panel = doc.getElementById("pb-panel");
  $$("[data-problem]").forEach(function (b) {
    b.addEventListener("click", function () {
      var problem = b.getAttribute("data-problem");
      var svc = b.getAttribute("data-svc");
      $$("[data-problem]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      if (qf) {
        pick(qf, "service", svc);
        if (b.hasAttribute("data-urgent")) pick(qf, "urgent", "Oui");
        var hidden = qf.querySelector('input[name="probleme"]');
        if (hidden) hidden.value = problem;
        var msg = qf.querySelector('textarea[name="message"]');
        if (msg) {
          msg.value = msg.value.replace(/^Problème : [^\n]*\n?/, "");
          msg.value = "Problème : " + problem + "\n" + msg.value;
        }
      }
      if (panel) {
        $(".pb-what", panel).textContent = problem;
        panel.hidden = false;
      }
      track("problem_select", { problem: problem, service: svc });
    });
  });
  var pbGo = doc.getElementById("pb-continue");
  if (pbGo && qf) pbGo.addEventListener("click", function () {
    qf.zekaShow(2);
    doc.getElementById("devis").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    setTimeout(function () { var n = qf.querySelector('input[name="nom"]'); if (n) n.focus({ preventScroll: true }); }, reduced ? 0 : 450);
  });
  $$("[data-rooms]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!qf) return;
      pick(qf, "service", "Fin de bail");
      pick(qf, "pieces", b.getAttribute("data-rooms"));
      qf.zekaShow(1);
      track("rooms_select", { rooms: b.getAttribute("data-rooms"), service: "Fin de bail" });
      doc.getElementById("devis").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      setTimeout(function () { var d = qf.querySelector('input[name="date"]'); if (d) d.focus({ preventScroll: true }); }, reduced ? 0 : 450);
    });
  });

  /* ---------- 7. mobile contact bar: hidden while a form is on screen ---------- */
  var bar = $(".mbar");
  if (bar && "IntersectionObserver" in window) {
    var onScreen = [];
    var typing = false;
    var fab = $(".wa-float");
    var sync = function () {
      var hide = onScreen.length > 0 || typing;
      bar.classList.toggle("is-hidden", hide);
      if (fab) fab.classList.toggle("is-hidden", hide);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var i = onScreen.indexOf(en.target);
        if (en.isIntersecting && i < 0) onScreen.push(en.target);
        if (!en.isIntersecting && i > -1) onScreen.splice(i, 1);
      });
      sync();
    }, { threshold: 0.12 });
    $$("form.qf, form.cb").forEach(function (f) {
      io.observe(f);
      f.addEventListener("focusin", function () { typing = true; sync(); });
      f.addEventListener("focusout", function () { typing = false; setTimeout(sync, 50); });
    });
  }

  /* ---------- 8. hero video: desktop, fast connection, motion allowed ---------- */
  var v = $(".hero-media video");
  if (v) {
    var wide = window.matchMedia("(min-width: 960px)");
    var conn = navigator.connection || {};
    var slow = conn.saveData || /(^|-)(2g|3g)$/.test(conn.effectiveType || "");
    var start = function () {
      if (!wide.matches || reduced || slow || v.getAttribute("data-on")) return;
      v.setAttribute("data-on", "1");
      $$("source[data-src]", v).forEach(function (s) { s.src = s.getAttribute("data-src"); });
      v.addEventListener("playing", function () { v.classList.add("on"); });
      v.load();
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    };
    if (doc.readyState === "complete") setTimeout(start, 400);
    else window.addEventListener("load", function () { setTimeout(start, 400); });
    if (wide.addEventListener) wide.addEventListener("change", start);
  }

  /* ---------- 10. thank-you page ---------- */
  if (html.getAttribute("data-page") === "merci") {
    var lead = null;
    try { lead = JSON.parse(store("zeka_lead") || "null"); } catch (e) { lead = null; }
    track("merci_view", { service: lead ? lead.service : "", from_form: !!lead, convert: !!lead });
    if (lead) store("zeka_lead", null);
  }
})();
