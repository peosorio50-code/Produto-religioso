# O Santo do Nosso Casamento (Meu Santo Protetor)

> **Todo casamento acontece no dia de um santo.** O quiz descobre, de graça, o santo do dia em que o casal disse sim, e oferece o livro de orações do casal em PDF, feito com o nome dos dois (R$ 37 + 2 bumps + upsell da Família).

| Pasta | O que tem |
|---|---|
| `docs/ESTRATEGIA.md` | A linha de raciocínio: por que este produto, preço, funil, números e riscos |
| `docs/COMO-SUBIR.md` | Passo a passo para a Kiwify, a VPS, o Cloudflare, o teste e os anúncios (com o terminal de cada comando) |
| `docs/TEXTOS-KIWIFY-E-ANUNCIOS.md` | Nomes, preços, descrições, bumps, upsell, legenda e lista de criativos |
| `docs/GUIA-CLAUDE-CASAMENTO.md` | Guia técnico para o Claude que for mexer no produto |
| `servidor/` | O que vai para `/opt/mapadaalma`: `casamento.py`, `casamento_conteudo.py`, `casamento_pdf.py`, `casamento_fontes/` e o `servidor.py` (v19 + 4 ganchos) |
| `site/` | O site estático para o Cloudflare Pages (configuração em `site/config.js`) |
| `criativos/` | O código dos criativos e das imagens (HTML + Playwright + ffmpeg) |
| `kit/` | As saídas: `kiwify/` (imagem e banners), `criativos/` (8 estáticos 4:5 e 3 vídeos 9:16) e `exemplos/` (PDFs de exemplo) |
| `testes/` | Teste ponta a ponta do servidor (45 conferências) |
| `entregas/` | Os zips prontos para subir e a skill `skill-produto-digital.zip` |

As fontes dos PDFs e dos criativos (Cormorant Garamond, Cinzel, Great Vibes e Outfit) são do Google Fonts, com licença SIL Open Font License.
