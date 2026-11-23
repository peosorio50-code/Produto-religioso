// Fotografa cada .peca de um HTML em imagem.  Uso: node render_estaticos.js [posters.html|estaticos.html]
//   id "p-..." → filhos/site/img/<nome>.jpg (capas dos vídeos e da VSL)
//   id "k-..." → filhos/kit/kiwify/<nome>.png (imagens da Kiwify)
//   outros     → filhos/kit/criativos/<id>.png (criativos 4:5)
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const raiz = path.resolve(__dirname, '..');
  const arq = process.argv[2] || 'estaticos.html';
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1300, height: 1400 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, arq)); await pg.waitForTimeout(800);
  await pg.evaluate(() => document.fonts.ready);
  const ids = await pg.$$eval('.peca', els => els.map(e => e.id));
  for (const id of ids) {
    const tipo = id.slice(0, 2);
    const dir = tipo === 'p-' ? path.join(raiz, 'site', 'img') : path.join(raiz, 'kit', tipo === 'k-' ? 'kiwify' : 'criativos');
    fs.mkdirSync(dir, { recursive: true });
    const nome = (tipo === 'p-' || tipo === 'k-') ? id.slice(2) : id;
    const saida = path.join(dir, nome + (tipo === 'p-' ? '.jpg' : '.png'));
    await (await pg.$('#' + id)).screenshot(tipo === 'p-' ? { path: saida, type: 'jpeg', quality: 86 } : { path: saida });
    console.log('ok', path.relative(raiz, saida));
  }
  await b.close();
})();
