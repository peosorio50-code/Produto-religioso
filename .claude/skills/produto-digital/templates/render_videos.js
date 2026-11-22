// Gera os vídeos 9:16 de videos.html quadro a quadro (24 fps) e monta com o ffmpeg. Sem áudio: use uma música da biblioteca do Meta.
// Uso: node criativos/render_videos.js [pasta-temporaria]   (saída em kit/criativos/*.mp4)
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs'); const { execFileSync } = require('child_process');
const FPS = 24;
(async () => {
  const raiz = path.resolve(__dirname, '..'); const tmp = process.argv[2] || fs.mkdtempSync(path.join(require('os').tmpdir(), 'vid-'));
  const saida = path.join(raiz, 'kit', 'criativos'); fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, 'videos.html')); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
  const ids = await pg.evaluate(() => Object.keys(VIDEOS));
  for (const id of ids) {
    const dir = path.join(tmp, id); fs.mkdirSync(dir, { recursive: true });
    const dur = await pg.evaluate(i => { mostra(i); return VIDEOS[i].dur; }, id);
    const el = await pg.$('#' + id);
    for (let n = 0; n < dur * FPS; n++) {
      await pg.evaluate(([i, t]) => VIDEOS[i].f(t), [id, n / FPS]);
      await el.screenshot({ path: path.join(dir, String(n).padStart(4, '0') + '.png') });
    }
    const mp4 = path.join(saida, id + '.mp4');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                            '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', mp4]);
    console.log('ok', id, dur + 's');
  }
  await b.close();
})();
