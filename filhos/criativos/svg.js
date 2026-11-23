// Ícones de linha (dourados) usados nos criativos, nas capas dos vídeos e nas imagens da Kiwify (Novena pelos Filhos)
window.SVG = (function () {
  function raios(cx, cy, c1, cor) { var r = ""; for (var i = 0; i < 36; i++) { var a = i * Math.PI / 18, c2 = i % 2 ? c1 + 24 : c1 + 16;
    r += '<line x1="' + (cx + c1 * Math.cos(a)).toFixed(1) + '" y1="' + (cy + c1 * Math.sin(a)).toFixed(1) + '" x2="' + (cx + c2 * Math.cos(a)).toFixed(1) + '" y2="' + (cy + c2 * Math.sin(a)).toFixed(1) + '" stroke="' + cor + '" stroke-width="' + (i % 2 ? 1.2 : .7) + '" opacity=".55"/>'; } return r; }
  function caixa(tam, vb, corpo) { return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 ' + vb + ' ' + vb + '" fill="none" stroke-linecap="round" stroke-linejoin="round">' + corpo + '</svg>'; }
  var S = {
    manto: function (tam, cor, comRaios) { cor = cor || "#C9A052"; var e = "";
      for (var i = 0; i < 12; i++) { var b = (200 + i * 140 / 11) * Math.PI / 180; e += '<circle cx="' + (75 + 40 * Math.cos(b)).toFixed(1) + '" cy="' + (62 + 40 * Math.sin(b)).toFixed(1) + '" r="2.6" fill="' + cor + '"/>'; }
      return caixa(tam, 150, (comRaios === false ? "" : raios(75, 80, 50, cor)) + e + '<g stroke="' + cor + '"><path d="M75 44 C60 58 52 86 44 120 Q75 128 106 120 C98 86 90 58 75 44 Z" stroke-width="4"/>'
        + '<circle cx="75" cy="58" r="8" stroke-width="3.5"/><path d="M75 76 v30 M65 86 h20" stroke-width="3.5"/></g>'); },
    vela: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 110, '<g stroke="' + cor + '" stroke-width="3"><path d="M55 14c6 9 9 15 9 20a9 9 0 0 1-18 0c0-5 3-11 9-20z"/><path d="M42 50h26v46H42z"/><path d="M55 44v6"/><path d="M34 96h42"/></g>'); },
    livro: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M60 34c-10-8-26-10-40-8v62c14-2 30 0 40 8 10-8 26-10 40-8V26c-14-2-30 0-40 8z"/><path d="M60 34v62"/><path d="M60 14v12M54 20h12"/></g>'); },
    chama: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M60 16c12 18 22 28 22 46a22 22 0 0 1-44 0c0-10 6-18 10-24 2 8 6 12 10 12-4-12-2-24 2-34z"/><path d="M40 100h40"/><path d="M48 110h24"/></g>'); },
    asas: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3"><circle cx="60" cy="30" r="9"/><path d="M60 44v40"/><path d="M58 50C44 36 22 34 12 40c10 4 16 12 20 22 6-6 16-8 26-6"/>'
        + '<path d="M62 50c14-14 36-16 46-10-10 4-16 12-20 22-6-6-16-8-26-6"/><path d="M48 84h24l-4 22H52z"/><ellipse cx="60" cy="16" rx="12" ry="3.5"/></g>'); },
    coracao: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M60 98C34 80 18 64 18 46a20 20 0 0 1 42-10 20 20 0 0 1 42 10c0 18-16 34-42 52z"/><path d="M60 50v28M48 62h24"/></g>'); },
    casa: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M20 58L60 24l40 34"/><path d="M30 50v46h60V50"/><path d="M52 96V72h16v24"/><path d="M60 8v10M55 13h10"/><path d="M6 108c30-8 78-8 108 0"/></g>'); },
    estrela: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M60 14l11 28 30 2-23 19 8 29-26-16-26 16 8-29-23-19 30-2z"/><path d="M60 100v14"/></g>'); },
    folha: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M60 110V46"/><path d="M60 76c-16-2-26-12-28-28 16 2 26 12 28 28z"/>'
        + '<path d="M60 64c16-2 26-12 28-28-16 2-26 12-28 28z"/><path d="M60 46c-7-9-7-22 0-32 7 10 7 23 0 32z"/><path d="M44 110h32"/></g>'); },
    pomba: function (tam, cor) { cor = cor || "#C9A052";
      return caixa(tam, 120, '<g stroke="' + cor + '" stroke-width="3.2"><path d="M18 70c18 2 30-6 38-18 8-12 20-18 34-16l12-8-4 14c2 22-14 40-38 44-14 2-30-4-42-16z"/>'
        + '<path d="M56 52c-6-14-18-22-34-22 4 14 14 22 28 26"/><circle cx="86" cy="40" r="1.8" fill="' + cor + '"/><path d="M40 96l-8 10M52 96l-4 12"/></g>'); },
    rosario: function (tam, cor) { cor = cor || "#C9A052"; var c = "";
      for (var a = 0; a < 360; a += 18) { if (a > 75 && a < 105) continue; var r = a * Math.PI / 180; c += '<circle cx="' + (55 + 34 * Math.cos(r)).toFixed(1) + '" cy="' + (44 + 30 * Math.sin(r)).toFixed(1) + '" r="3.2" fill="' + cor + '"/>'; }
      return caixa(tam, 110, c + '<path d="M55 74 v10 M55 88 v16 M48 94 h14" stroke="' + cor + '" stroke-width="3"/>'); },
    pinta: function () {
      document.querySelectorAll("[data-svg]").forEach(function (el) {
        var p = el.getAttribute("data-svg").split(","); el.innerHTML = S[p[0]](+p[1], p[2] || undefined, p[3] === "0" ? false : undefined);
      });
    }
  };
  return S;
})();
