// Ícones de linha (dourados) usados nos criativos e nas imagens da Kiwify
window.SVG = {
  aneis: function (tam, cor, raios) {
    cor = cor || "#C9A052"; var r = "";
    if (raios !== false) for (var i = 0; i < 36; i++) { var a = i * Math.PI / 18, c1 = 44, c2 = i % 2 ? 72 : 64;
      r += '<line x1="' + (75 + c1 * Math.cos(a)).toFixed(1) + '" y1="' + (82 + c1 * Math.sin(a)).toFixed(1) + '" x2="' + (75 + c2 * Math.cos(a)).toFixed(1) + '" y2="' + (82 + c2 * Math.sin(a)).toFixed(1) + '" stroke-width="' + (i % 2 ? 1.2 : .7) + '" opacity=".6"/>'; }
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 150 150"><g stroke="' + cor + '" fill="none">' + r
      + '<circle cx="62" cy="90" r="22" stroke-width="5"/><circle cx="88" cy="90" r="22" stroke-width="5"/><path d="M75 30 v32 M64 41 h22" stroke-width="4.5" stroke-linecap="round"/></g></svg>';
  },
  lirio: function (tam, cor) { cor = cor || "#C9A052";
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 120 120" fill="none" stroke="' + cor + '" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
      + '<path d="M60 108V58"/><path d="M60 58c-4-14-4-28 0-40 4 12 4 26 0 40z"/><path d="M60 60c-10-6-22-6-30 2 10 2 20 2 30-2z"/><path d="M60 60c10-6 22-6 30 2-10 2-20 2-30-2z"/>'
      + '<path d="M60 84c-8-2-14-8-16-14 8 0 14 4 16 14z"/><path d="M60 92c8-2 14-8 16-14-8 0-14 4-16 14z"/></svg>'; },
  rosa: function (tam, cor) { cor = cor || "#C9A052";
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 120 120" fill="none" stroke="' + cor + '" stroke-width="3.2" stroke-linecap="round">'
      + '<path d="M60 26c-14 0-24 10-24 22 0 13 11 22 24 22s24-9 24-22c0-12-10-22-24-22z"/><path d="M60 36c-7 0-12 5-12 11 0 7 6 11 12 11s12-4 12-11"/><path d="M60 44c-3 0-5 2-5 4"/>'
      + '<path d="M60 70v34"/><path d="M60 86c-9-2-16-8-18-16 8 0 16 5 18 16z"/><path d="M60 80c8-2 14-8 16-15-8 0-14 5-16 15z"/></svg>'; },
  coroa: function (tam, cor) { cor = cor || "#C9A052";
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 120 120" fill="none" stroke="' + cor + '" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'
      + '<path d="M28 52l12 14 20-26 20 26 12-14-6 30H34z"/><path d="M34 90h52"/><circle cx="60" cy="34" r="4"/><circle cx="28" cy="48" r="3.5"/><circle cx="92" cy="48" r="3.5"/>'
      + '<path d="M60 92v18M52 100h16"/></svg>'; },
  vela: function (tam, cor) { cor = cor || "#C9A052";
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 110 110" fill="none" stroke="' + cor + '" stroke-width="3" stroke-linecap="round">'
      + '<path d="M55 14c6 9 9 15 9 20a9 9 0 0 1-18 0c0-5 3-11 9-20z"/><path d="M42 50h26v46H42z"/><path d="M55 44v6"/><path d="M34 96h42"/></svg>'; },
  casal: function (tam, cor) { cor = cor || "#C9A052";  // duas mãos com alianças, estilizadas
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 120 120" fill="none" stroke="' + cor + '" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
      + '<path d="M20 78c10-4 18-12 24-22 4-6 10-6 12 0l2 6"/><path d="M100 78c-10-4-18-12-24-22-4-6-10-6-12 0l-2 6"/><path d="M40 92c8 6 32 6 40 0"/>'
      + '<circle cx="52" cy="70" r="6"/><circle cx="68" cy="70" r="6"/><path d="M60 20v18M52 28h16"/></svg>'; },
  pinta: function () {
    document.querySelectorAll("[data-svg]").forEach(function (el) {
      var p = el.getAttribute("data-svg").split(","); el.innerHTML = SVG[p[0]](+p[1], p[2] || undefined, p[3] === "0" ? false : undefined);
    });
  }
};
