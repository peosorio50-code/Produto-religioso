# Novena pelos Filhos (Meu Santo Protetor)

> **Todo filho nasce no dia de um santo.** O quiz descobre, de graça, o santo do dia em que cada filho ou neto nasceu, e oferece a novena em vídeo: 9 vídeos narrados e um livro em PDF com o nome e o santo de cada um (R$ 87 + 2 bumps + upsell "Um Livro para Cada Filho").

| Pasta | O que tem |
|---|---|
| `roteiros/` | **Para o Carlos:** o que falta gravar (VSL, 9 vídeos da novena, terço, anúncios narrados), com o texto para a ElevenLabs e a direção de imagem. Comece pelo `00-LEIA-PRIMEIRO-CARLOS.md` |
| `docs/ESTRATEGIA.md` | Por que este produto, preço, funil, números, prazos verdadeiros possíveis e riscos |
| `docs/COMO-SUBIR.md` | Kiwify → VPS → Cloudflare → teste → anúncios, com o terminal de cada comando |
| `docs/TEXTOS-KIWIFY-E-ANUNCIOS.md` | Nomes exatos, preços, descrições, bumps, upsell, legenda e lista de criativos |
| `docs/GUIA-CLAUDE-FILHOS.md` | Guia técnico para o Claude que for mexer no produto |
| `site/` | O site estático para o Cloudflare Pages (configuração em `site/config.js`; vídeos em `site/videos/`) |
| `criativos/` | O código dos criativos, das capas dos vídeos e das imagens da Kiwify (HTML + Playwright + ffmpeg) |
| `kit/` | As saídas: `kiwify/`, `criativos/` (9 estáticos 4:5 e 3 vídeos 9:16) e `exemplos/` (PDFs de exemplo) |

O servidor fica em `../servidor/` (`filhos.py`, `filhos_conteudo.py`, `filhos_pdf.py`, `filhos_fontes/` e o `servidor.py` v21), e o teste em `../testes/teste_filhos.py` (60 conferências).

O pacote para o Carlos é um zip só: `../entregas/novena-pelos-filhos.zip` (monte de novo com `bash filhos/montar_zip.sh`, na raiz do repositório).
