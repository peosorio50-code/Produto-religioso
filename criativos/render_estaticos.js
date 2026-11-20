// Fotografa cada .peca de estaticos.html em PNG (criativos 4:5 e imagens da Kiwify).
// Uso: node criativos/render_estaticos.js   (saída em kit/criativos e kit/kiwify)
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const raiz = path.resolve(__dirname, '..');
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1300, height: 1400 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, 'estaticos.html')); await pg.waitForTimeout(800);
  await pg.evaluate(() => document.fonts.ready);
  const ids = await pg.$$eval('.peca', els => els.map(e => e.id));
  for (const id of ids) {
    const dir = path.join(raiz, 'kit', id.startsWith('k-') ? 'kiwify' : 'criativos'); fs.mkdirSync(dir, { recursive: true });
    const nome = id.startsWith('k-') ? id.slice(2) : id;
    await (await pg.$('#' + id)).screenshot({ path: path.join(dir, nome + '.png') });
    console.log('ok', nome);
  }
  await b.close();
})();
