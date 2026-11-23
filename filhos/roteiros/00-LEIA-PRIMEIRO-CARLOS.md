# Carlos, leia primeiro: o que falta para a Novena pelos Filhos ir ao ar

O servidor, o site, o livro em PDF, as imagens da Kiwify, os criativos estáticos e 3 vídeos mudos **já estão prontos e testados**. O que falta é com você:

1. **Gravar e montar os vídeos narrados** (esta pasta).
2. **Subir** na Kiwify, na VPS e no Cloudflare (o passo a passo está em `docs/COMO-SUBIR.md`, com o terminal de cada comando).

> **Onde está cada coisa:** as imagens citadas nos roteiros como `site/img/...` (capas dos dias, capa da VSL, páginas de exemplo do livro) estão na pasta `roteiros/capas-dos-videos/` do `kit-filhos.zip`, e também na pasta `img/` do `site-santo-filhos.zip`. Os vídeos mudos citados nos anúncios (`v1-calendario.mp4`...) estão em `criativos/` do kit.

## Os vídeos, em ordem de prioridade

| # | Vídeo | Roteiro | Duração | Formato | Arquivo | Precisa estar pronto antes de… |
|---|---|---|---|---|---|---|
| 1 | **Os 9 vídeos da novena** (o produto) | `02-NOVENA-9-VIDEOS.md` | 3 a 4 min cada | 4:5, 720×900 | `site/videos/dia1.mp4` … `dia9.mp4` | **ligar a venda** |
| 2 | **VSL** da página de vendas | `01-VSL.md` | ~4 min | 4:5, 720×900, até 22 MB | `site/videos/vsl.mp4` | ligar os anúncios (dá para testar sem, mas a R$ 87 a VSL faz falta) |
| 3 | **Terço pelos Filhos** (order bump) | `03-TERCO.md` | 20 a 25 min | 4:5; YouTube não listado | link no `config.js` | ligar o bump do terço na Kiwify |
| 4 | **Anúncios narrados** 9:16 | `04-ANUNCIOS-NARRADOS.md` | 25 a 60 s | 1080×1920 | para o Gerenciador de Anúncios | — (os estáticos e os 3 vídeos mudos do kit já servem para começar) |
| 5 | Cortes da VSL 9:16 | final do `01-VSL.md` | 45 a 70 s | 1080×1920 | para o Gerenciador | — |

> **Não venda antes dos 9 vídeos estarem no ar.** A página da novena funciona sem eles (mostra a capa do dia e o texto), mas a pessoa pagou R$ 87 por uma novena **em vídeo**. Se faltar um vídeo, é reclamação e reembolso.

## ElevenLabs

- Voz **Jorge – Calm & Warm**, modelo Eleven v4, Stability no meio, Similarity ~75%, sem Auto-tag, MP3 128 kbps (as mesmas das VSLs).
- **Grave um bloco por vez**, e mande antes um bloco de teste (o V01 da VSL ou o DIA-1 Reflexão) para conferir o ritmo. Para oração, o ritmo é **mais lento** que o da VSL.
- Blocos **[COMUM]** são gravados **uma vez** e reaproveitados nos 9 dias e no terço (abertura, momento dos nomes, Pai-Nosso, Ave-Maria, Glória, fecho).
- `[PAUSA 10 s]` é silêncio na edição. Não escreva isso na ElevenLabs.
- **Pronúncia** que costuma dar problema: Loide (**LÓ-i-de**), Eunice (**eu-NÍ-ce**), Jairo (**JA-i-ro**), Óstia, Tagaste, Agostinho. Se sair errado, escreva do jeito que se fala só no texto da ElevenLabs.
- **Conta de créditos** (contada nos roteiros, 1 crédito por caractere): 9 dias ~12,5 mil (com os blocos comuns) · VSL ~3,5 mil · terço ~4,5 mil · anúncios ~2,5 mil. **Total: ~23 mil**, mais uns 30% de margem para regravar o que não ficar bom (~30 mil). Em 17/11 você tinha ~38 mil: confira o saldo antes. Grave a novena primeiro.

## Imagens

- Cada dia indica uma **pintura antiga em domínio público** (procure pelo nome no Wikimedia Commons) para os momentos de santo, de Nossa Senhora e de Jesus. Imagem de IA de santo costuma sair com defeito, e esse público percebe.
- IA para o resto: velas, mãos, terço, Bíblia, estradas, janelas, casa. **Sem rosto nítido** (de costas, desfocado ou só as mãos), para não parecer depoimento de gente real.
- As capas prontas de cada dia estão em `site/img/dia1.jpg` … `dia9.jpg` e `terco.jpg`. A capa da VSL é `site/img/vsl-capa.jpg`.
- Paleta: azul-marinho `#0B1636` / `#17295A` e dourado `#C9A052` / `#E9CF93`. Fontes: Cinzel (títulos) e Cormorant Garamond (texto), as mesmas do livro.

## Arquivos de vídeo para o site

- **4:5, 720×900, H.264, AAC mono 96 kbps, `-movflags +faststart`.** O limite do Cloudflare Pages é **25 MB por arquivo**: mire em 10 a 15 MB para 4 minutos (imagem calma comprime bem). Comando de exemplo no **Mac** (troque os nomes):
  ```
  ffmpeg -i dia1-editado.mov -vf scale=720:900 -c:v libx264 -crf 27 -preset slow -c:a aac -b:a 96k -ac 1 -movflags +faststart dia1.mp4
  ```
- Coloque os arquivos na pasta `videos/` do site e preencha o `config.js`:
  ```
  VSL_SRC: "videos/vsl.mp4",
  VIDEOS: { dia1: "videos/dia1.mp4", dia2: "videos/dia2.mp4", … dia9: "videos/dia9.mp4", terco: "youtube:ID_DO_VIDEO" }
  ```
- Se algum arquivo passar de 25 MB, use YouTube **não listado** e escreva `"youtube:ID"` (o ID é o trecho depois de `watch?v=`).

## Checklist antes de ligar os anúncios

- [ ] 9 vídeos da novena assistidos do começo ao fim (áudio, legenda, nenhuma imagem estranha)
- [ ] VSL no ar e conferida no celular (começa muda, botão de som funciona)
- [ ] Vídeo do terço no ar **ou** o bump do terço desligado na Kiwify
- [ ] Compra de teste no celular até gerar o Pix, e uma compra paga de verdade (depois reembolsar)
- [ ] Página da novena aberta pelo link do e-mail, vídeo do dia 1 tocando
