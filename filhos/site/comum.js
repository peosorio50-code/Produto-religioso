/* Novena pelos Filhos — funções comuns às páginas (não precisa editar; a configuração fica no config.js) */
(function () {
  var C = window.CFG || {};
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];

  function ls(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  function sessao() {
    var s = ls("fil_sessao");
    if (!s) { s = Math.random().toString(36).slice(2) + Date.now().toString(36); ls("fil_sessao", s); }
    return s.slice(0, 40);
  }
  // UTMs e src: guarda a primeira origem da visita (o anúncio) para mandar ao checkout
  function origem() {
    var q = new URLSearchParams(location.search), o = {}, tem = false;
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "src", "fbclid"].forEach(function (k) {
      if (q.get(k)) { o[k] = q.get(k).slice(0, 200); tem = true; }
    });
    if (tem) { ls("fil_origem", JSON.stringify(o)); return o; }
    try { return JSON.parse(ls("fil_origem") || "{}"); } catch (e) { return {}; }
  }
  var ORIGEM = origem();

  // contador próprio do servidor (o Meta descarta eventos personalizados de sites na categoria Religião)
  var contados = {};
  function conta(ev) {
    if (contados[ev]) return; contados[ev] = 1;
    try {
      var body = JSON.stringify({ s: sessao(), e: ev, p: "filhos", src: (ORIGEM.utm_source || ORIGEM.src || "").slice(0, 40) });
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
  function lista(n) { n = n.filter(Boolean); return n.length < 2 ? (n[0] || "") : n.slice(0, -1).join(", ") + " e " + n[n.length - 1]; }
  function dataValida(d, m, a) { var x = new Date(a || 2000, m - 1, d); return d && m && x.getDate() === +d && x.getMonth() === m - 1; }

  // ---------- editor de filhos e netos (quiz e página de dados) ----------
  var MAX = 6;
  var RELS = [["filho", "Filho"], ["filha", "Filha"], ["neto", "Neto"], ["neta", "Neta"]];
  function selDia(cls, v) { var h = '<select class="' + cls + '"><option value="">Dia</option>'; for (var d = 1; d <= 31; d++) h += '<option' + (+v === d ? " selected" : "") + '>' + d + '</option>'; return h + '</select>'; }
  function selMes(cls, v) { return '<select class="' + cls + '"><option value="">Mês</option>' + MESES.map(function (m, i) { return '<option value="' + (i + 1) + '"' + (+v === i + 1 ? " selected" : "") + '>' + m + '</option>'; }).join("") + '</select>'; }
  function relPadrao(papel) { return papel === "avo_f" || papel === "avo_m" ? "neto" : "filho"; }

  function Editor(el, papel, pessoas) {
    var self = this; this.el = el; this.papel = papel;
    this.p = (pessoas && pessoas.length ? pessoas : [{ nome: "", rel: relPadrao(papel), dia: "", mes: "", ano: "", partiu: false }]).map(function (x) { return Object.assign({}, x); });
    this.ler = function () {
      Array.prototype.forEach.call(el.querySelectorAll(".pessoa"), function (c, i) {
        var p = self.p[i]; if (!p) return;
        p.nome = c.querySelector(".f-nome").value.trim(); p.dia = +c.querySelector(".f-dia").value || ""; p.mes = +c.querySelector(".f-mes").value || "";
        p.ano = c.querySelector(".f-ano").value.trim(); p.partiu = c.querySelector(".f-partiu").checked;
      });
    };
    this.render = function () {
      el.innerHTML = this.p.map(function (p, i) {
        return '<div class="pessoa"><h4>' + (i + 1) + 'º</h4>' + (self.p.length > 1 ? '<button type="button" class="tirar" data-i="' + i + '">tirar</button>' : "")
          + '<div class="campo"><input type="text" class="f-nome" maxlength="40" autocomplete="off" placeholder="Primeiro nome" value="' + esc(p.nome) + '"></div>'
          + '<div class="rel">' + RELS.map(function (r) { return '<button type="button" data-i="' + i + '" data-r="' + r[0] + '" class="' + (p.rel === r[0] ? "sel" : "") + '">' + r[1] + '</button>'; }).join("") + '</div>'
          + '<div class="rotulo">Data de nascimento (o ano é opcional)</div>'
          + '<div class="nasc">' + selDia("f-dia", p.dia) + selMes("f-mes", p.mes) + '<input type="tel" inputmode="numeric" class="f-ano" maxlength="4" placeholder="Ano" value="' + esc(p.ano) + '"></div>'
          + '<label class="partiu"><input type="checkbox" class="f-partiu"' + (p.partiu ? " checked" : "") + '> Já partiu para junto de Deus</label></div>';
      }).join("") + (this.p.length < MAX ? '<button type="button" class="mais" id="ed-mais">+ Adicionar mais um</button>' : "");
      Array.prototype.forEach.call(el.querySelectorAll(".rel button"), function (b) {
        b.onclick = function () { self.ler(); self.p[+b.getAttribute("data-i")].rel = b.getAttribute("data-r"); self.render(); };
      });
      Array.prototype.forEach.call(el.querySelectorAll(".tirar"), function (b) {
        b.onclick = function () { self.ler(); self.p.splice(+b.getAttribute("data-i"), 1); self.render(); };
      });
      var m = el.querySelector("#ed-mais");
      if (m) m.onclick = function () {
        self.ler(); var ult = self.p[self.p.length - 1] || {};
        self.p.push({ nome: "", rel: ult.rel || relPadrao(self.papel), dia: "", mes: "", ano: "", partiu: false }); self.render();
        var ns = el.querySelectorAll(".f-nome"); ns[ns.length - 1].focus();
      };
    };
    this.valida = function () {
      this.ler(); var hoje = new Date();
      for (var i = 0; i < this.p.length; i++) {
        var p = this.p[i], q = (i + 1) + "º";
        if (p.nome.length < 2) return "Escreva o nome do " + q + ".";
        if (!p.dia || !p.mes || !dataValida(p.dia, p.mes)) return "Confira o dia e o mês em que " + primeiro(p.nome) + " nasceu.";
        if (p.ano !== "") {
          var a = +p.ano;
          if (!a || a < 1920 || String(p.ano).length !== 4 || !dataValida(p.dia, p.mes, a) || new Date(a, p.mes - 1, p.dia) > hoje) return "Confira o ano em que " + primeiro(p.nome) + " nasceu (4 números) ou deixe em branco.";
        }
      }
      return "";
    };
    this.dados = function () {
      return this.p.map(function (p) { var o = { nome: p.nome, rel: p.rel, dia: +p.dia, mes: +p.mes, partiu: !!p.partiu }; if (p.ano !== "") o.ano = +p.ano; return o; });
    };
    this.render();
  }

  window.FIL = { C: C, MESES: MESES, ls: ls, sessao: sessao, ORIGEM: ORIGEM, conta: conta, track: track, api: api, pixel: pixel, esc: esc,
                 primeiro: primeiro, dataPt: dataPt, dd: dd, lista: lista, dataValida: dataValida, Editor: Editor, MAX: MAX };
})();
