/* O Santo do Nosso Casamento — funções comuns às páginas (não precisa editar; a configuração fica no config.js) */
(function () {
  var C = window.CFG || {};
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var BODAS = { 1: "Bodas de Papel", 5: "Bodas de Madeira", 10: "Bodas de Estanho", 15: "Bodas de Cristal", 20: "Bodas de Porcelana",
                25: "Bodas de Prata", 30: "Bodas de Pérola", 50: "Bodas de Ouro", 60: "Bodas de Diamante" };

  function ls(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  function sessao() {
    var s = ls("cas_sessao");
    if (!s) { s = Math.random().toString(36).slice(2) + Date.now().toString(36); ls("cas_sessao", s); }
    return s.slice(0, 40);
  }
  // UTMs e src: guarda a primeira origem da visita (o anúncio) para mandar ao checkout
  function origem() {
    var q = new URLSearchParams(location.search), o = {}, tem = false;
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "src", "fbclid"].forEach(function (k) {
      if (q.get(k)) { o[k] = q.get(k).slice(0, 200); tem = true; }
    });
    if (tem) { ls("cas_origem", JSON.stringify(o)); return o; }
    try { return JSON.parse(ls("cas_origem") || "{}"); } catch (e) { return {}; }
  }
  var ORIGEM = origem();

  // contador próprio do servidor (o Meta descarta eventos personalizados de sites na categoria Religião)
  var contados = {};
  function conta(ev) {
    if (contados[ev]) return; contados[ev] = 1;
    try {
      var body = JSON.stringify({ s: sessao(), e: ev, p: "casamento", src: (ORIGEM.utm_source || ORIGEM.src || "").slice(0, 40) });
      if (navigator.sendBeacon) navigator.sendBeacon(C.API + "/api/evento", new Blob([body], { type: "text/plain" }));
      else fetch(C.API + "/api/evento", { method: "POST", body: body, keepalive: true });
    } catch (e) {}
  }
  function track(ev, padrao, dados) {
    conta(ev);
    try { if (padrao && window.fbq) fbq("track", padrao, dados || {}); } catch (e) {}
  }

  function api(caminho, opcoes, ms) {
    var ctl = window.AbortController ? new AbortController() : null;
    var t = setTimeout(function () { if (ctl) ctl.abort(); }, ms || 12000);
    opcoes = opcoes || {};
    if (ctl) opcoes.signal = ctl.signal;
    if (opcoes.body && typeof opcoes.body !== "string") {
      opcoes.body = JSON.stringify(opcoes.body); opcoes.headers = { "Content-Type": "application/json" }; opcoes.method = opcoes.method || "POST";
    }
    return fetch(C.API + caminho, opcoes).then(function (r) {
      clearTimeout(t);
      return r.json().catch(function () { return {}; }).then(function (j) { j._status = r.status; return j; });
    }, function (e) { clearTimeout(t); throw e; });
  }

  function pixel() {
    if (!C.PIXEL) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    fbq("init", C.PIXEL); fbq("track", "PageView");
  }

  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function primeiro(n) { n = String(n || "").trim().split(/\s+/)[0] || ""; return n ? n.charAt(0).toUpperCase() + n.slice(1).toLowerCase() : ""; }
  function dataPt(d, m, a) { return d + " de " + MESES[m - 1] + (a ? " de " + a : ""); }
  function dd(n) { return (n < 10 ? "0" : "") + n; }

  window.CAS = { C: C, MESES: MESES, BODAS: BODAS, ls: ls, sessao: sessao, ORIGEM: ORIGEM, conta: conta, track: track, api: api,
                 pixel: pixel, esc: esc, primeiro: primeiro, dataPt: dataPt, dd: dd };
})();
