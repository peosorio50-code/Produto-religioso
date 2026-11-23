# Textos prontos: Kiwify e anúncios

## 1. Produto principal

- **Nome na Kiwify (exato):** `Novena pelos Filhos (em vídeo)`
  - O servidor reconhece a venda pelo trecho **"novena pelos filhos"**. Se mudar o nome na Kiwify, mude também `FILHOS_PRODUTO` no `.env`, senão a venda não é entregue.
  - Não coloque no nome "livro de orações", "devocionário", "2027", "consagração", "biblioteca", "terço diário" nem "rezo por você": são trechos que o servidor usa para outros produtos.
- **Preço:** R$ 87,00 · pagamento único · Pix e cartão · garantia de 7 dias
- **Imagem do produto:** `kiwify/produto.png` (1000×1000)
- **Checkout:**
  - cores `#F8F3EE` (fundo) e `#17295A` (botões);
  - banner de computador: `kiwify/banner-computador.png` (1200×400);
  - banner de celular: `kiwify/banner-celular.png` (1080×540).
- **Página de obrigado (redirecionamento depois da compra):** `https://filhos.meusantoprotetor.online/obrigado.html`

**Descrição (copiar e colar):**

> A Novena pelos Filhos são nove dias para rezar por cada filho e cada neto, pelo nome.
>
> Todo dia do ano a Igreja recorda um santo ou celebra uma festa. A novena começa pelo santo do dia em que cada um nasceu, e acompanha você durante nove dias, com Santa Mônica, a mãe que rezou anos pelo filho, e com Nossa Senhora.
>
> Você recebe:
> • 9 vídeos narrados, um por dia, de poucos minutos: você aperta o play, reza junto e diz o nome de cada um;
> • o livro da novena em PDF, com o nome e o santo do dia de nascimento de cada filho ou neto;
> • uma oração para cada um, escrita pelo nome;
> • a história de Santa Mônica e o que ela ensina a quem reza pelos filhos;
> • a consagração a Nossa Senhora no nono dia, com certificado para imprimir;
> • como dar a bênção, e orações para cada situação (quando sai de casa, numa prova, na doença, na tristeza, no vício, longe da fé, sem trabalho);
> • um quadro com os nomes para emoldurar;
> • um lembrete de manhã no seu e-mail durante os nove dias.
>
> Entrega: logo depois da confirmação do pagamento, a página da sua novena abre com os vídeos e o livro, e o link chega no seu e-mail.
>
> Material devocional católico do Meu Santo Protetor. Não somos uma paróquia: nada substitui a missa, os sacramentos e a orientação do padre.

## 2. Order bumps

São dois produtos separados na Kiwify, adicionados como order bump no checkout do principal.

### Bump 1 (só depois que o vídeo do terço estiver no ar)

- **Nome na Kiwify (exato):** `Terço pelos Filhos (em vídeo)`
- **Preço:** R$ 19,90
- **Imagem:** `kiwify/bump-terco.png`
- **Título no checkout:** Sim! Quero também o Terço pelos Filhos em vídeo
- **Descrição:** Um terço meditado com os mistérios gozosos, a infância de Jesus, com cada mistério oferecido pelo nome dos seus filhos e netos. O vídeo reza junto com você, e o roteiro em PDF vem com os nomes.

### Bump 2

- **Nome na Kiwify (exato):** `30 Bênçãos para Mandar aos Filhos`
- **Preço:** R$ 14,90
- **Imagem:** `kiwify/bump-bencaos.png`
- **Título no checkout:** Sim! Quero também as 30 Bênçãos para Mandar aos Filhos
- **Descrição:** 30 mensagens curtas de bênção, uma por dia, já com o nome de cada filho ou neto, para mandar pelo WhatsApp com um toque. Chegam junto com a novena.

> Se mudar o nome de um bump na Kiwify, mude também `FILHOS_BUMP_TERCO` ou `FILHOS_BUMP_BENCAOS` no `.env`.

## 3. Upsell de 1 clique (página de obrigado)

- **Produto novo na Kiwify (nome exato):** `Um Livro para Cada Filho`, R$ 37,00, garantia de 7 dias, imagem `kiwify/upsell-livros.png`.
  - O servidor reconhece pelo trecho **"livro para cada filho"** (`FILHOS_UPSELL` no `.env`).
  - Este produto **só é vendido na página de obrigado**. Não use o link dele em anúncio nem em e-mail: a página diz "só nesta página", e isso tem que continuar verdade.
- **Descrição (Kiwify):**
  > Um livro em PDF para cada filho ou neto, com o nome na capa, o santo do dia em que nasceu, a oração que você reza por ele, uma oração para ele mesmo rezar, uma bênção e um santinho para recortar. Para mandar pelo WhatsApp ou imprimir e entregar em mãos. Feito com os nomes que você informou na Novena pelos Filhos.
- **Gerador de upsell** desse produto:
  - **Ao aceitar / ao recusar:** deixe em "área de membros". A página define o destino, como nas outras ofertas.
  - Do código gerado, copie o trecho depois de `kiwify-upsell-trigger-` e cole em `UPSELL_ID` no `site/config.js`.
  - Confira se o `<script src="...">` do código é igual ao `UPSELL_SCRIPT` do `config.js`.
  - O link do checkout desse produto vai em `CHECKOUT_UPSELL`: é a reserva para quem pagou no Pix (a página acrescenta o `sck` sozinha, para o servidor achar os nomes).

## 4. Anúncios (Meta)

**Legenda única (copiar e colar):**

> Todo filho nasce no dia de um santo. 🕯️
>
> Na Igreja, cada dia do ano recorda um santo ou celebra uma festa. O dia em que cada filho (ou neto) nasceu também tem o seu.
>
> Descubra de graça, em 1 minuto: escreva o nome e o aniversário de cada um e veja na hora o santo que a Igreja recorda naquele dia.
>
> Se quiser, reze a Novena pelos Filhos: 9 dias, com um vídeo curto por dia, para entregar cada um a Deus pelo nome, com Santa Mônica e Nossa Senhora. 🙏
>
> 👉 Toque em Saiba mais.

- **Título:** Descubra o santo do dia de cada filho
- **Descrição:** Grátis · 1 minuto
- **Botão:** Saiba mais
- **Link:**
  ```
  https://filhos.meusantoprotetor.online/?utm_source=facebook&utm_medium=pago&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
  ```

**Criativos** (`criativos/`):

| Arquivo | Formato | Conjunto | Ideia |
|---|---|---|---|
| `e1-qual-destes.png` | 4:5 | A | "Qual destes é o santo do seu filho?" (A/B/C, como o campeão do devocionário) |
| `e2-pergunte-em-casa.png` | 4:5 | A | "Pergunte em casa: em que dia de santo cada um nasceu?" |
| `e3-datas.png` | 4:5 | A | Datas reais e o santo de cada uma, terminando em "E no dia em que cada filho seu nasceu?" |
| `e5-santa-monica.png` | 4:5 | A | A frase do bispo a Santa Mônica, com a fonte (Confissões, III, 12) |
| `e8-conversa.png` | 4:5 | A | Conversa no grupo da família, como **cena** (etiqueta "cena ilustrativa") |
| `v1-calendario.mp4` | 9:16, 13 s | A | Folhas do calendário com o santo de cada dia |
| `v2-velas.mp4` | 9:16, 13 s | A | Três velas acendendo, cada uma com um nome |
| `e4-velas.png` | 4:5 | B | "Uma vela. Um nome. Nove dias." |
| `e6-produto-preco.png` | 4:5 | B | O livro, o vídeo, o que vem e o preço |
| `e7-nove-dias.png` | 4:5 | B | As capas dos 9 dias |
| `e9-quadro.png` | 4:5 | B | O quadro com os nomes emoldurado |
| `v3-por-dentro.mp4` | 9:16, 14 s | B | O vídeo do dia e as páginas do livro, terminando com o preço |
| *narrados do Carlos* | 9:16 | A e B | Roteiros em `roteiros/04-ANUNCIOS-NARRADOS.md` |

- Os vídeos mudos não têm áudio: escolha a música na biblioteca do Meta.
- As páginas mostradas são de um livro de exemplo ("Pedro, Ana e Lucas"), e os criativos dizem isso.
- **Não use** escassez nem prazo que não seja verdadeiro, depoimento inventado ou "de/por" falso. Os prazos verdadeiros possíveis (com a data em que saem do ar) estão no `ESTRATEGIA.md`, seção 7.
