# Textos prontos: Kiwify e anúncios

## 1. Produto principal

- **Nome na Kiwify (exato):** `O Santo do Nosso Casamento`
  - O servidor reconhece a venda pelo trecho **"santo do nosso casamento"**. Se mudar o nome na Kiwify, mude também `CASAMENTO_PRODUTO` no `.env`, senão a venda não é entregue.
  - Não coloque no nome "livro de orações", "devocionário", "2027" nem "consagração": são trechos que o servidor usa para outros produtos.
- **Preço:** R$ 37,00 · pagamento único · Pix e cartão · garantia de 7 dias
- **Imagem do produto:** `kit/kiwify/produto.png` (1000×1000)
- **Checkout:**
  - cores `#F8F3EE` (fundo) e `#17295A` (botões);
  - banner de computador: `kit/kiwify/banner-computador.png` (1200×400);
  - banner de celular: `kit/kiwify/banner-celular.png` (1080×540).
- **Página de obrigado (redirecionamento depois da compra):** `https://casamento.meusantoprotetor.online/obrigado.html`

**Descrição (copiar e colar):**

> O Santo do Nosso Casamento é um livro de orações em PDF feito para o casal, com o nome dos dois.
>
> Todo dia do ano a Igreja recorda um santo ou celebra uma festa. O livro começa pelo santo do dia em que vocês se casaram: quem ele foi e o que o exemplo dele ensina ao casamento de vocês.
>
> Vem junto:
> • a oração do casal, escrita com o nome dos dois e com o que você contou;
> • o santo de cada um (se você informar os aniversários);
> • a novena do casal: 9 dias para rezarem juntos;
> • a renovação das promessas para fazer em casa no aniversário de casamento;
> • orações para cada momento: depois de uma briga, quando falta dinheiro, na doença, pela fé do marido ou da esposa, antes de dormir e nos dias difíceis;
> • os santos dos casais: Sagrada Família, São José, Santa Rita, Santa Mônica, São Luís e Santa Zélia;
> • o calendário do casal de 2027;
> • o quadro "Unidos por Deus" com os nomes de vocês, para imprimir e emoldurar.
>
> Entrega: o PDF chega no seu e-mail em poucos minutos depois da confirmação do pagamento.
>
> Material devocional católico do Meu Santo Protetor. Não somos uma paróquia: nada substitui a missa, os sacramentos e a orientação do padre.

## 2. Order bumps

São dois produtos separados na Kiwify, adicionados como order bump no checkout do principal.

### Bump 1

- **Nome na Kiwify (exato):** `30 Dias Rezando pelo Meu Marido`
- **Preço:** R$ 14,90
- **Imagem:** `kit/kiwify/bump-30-dias.png`
- **Título no checkout:** Sim! Quero também os 30 Dias Rezando pelo Meu Marido (ou pela minha esposa)
- **Descrição:** Um tema, uma oração com o nome dele e um gesto simples para cada um dos 30 dias: a fé, o trabalho, a saúde, a paciência, o perdão… Chega junto com o livro, no mesmo e-mail.

### Bump 2

- **Nome na Kiwify (exato):** `Novena de Santa Rita pelo Casamento`
- **Preço:** R$ 12,90
- **Imagem:** `kit/kiwify/bump-santa-rita.png`
- **Título no checkout:** Sim! Quero também a Novena de Santa Rita pelo Casamento
- **Descrição:** Nove dias com a santa das causas impossíveis, que conheceu de perto um casamento difícil. A história de cada dia, a oração com o nome do casal e o seu pedido.

> Se mudar o nome de um bump na Kiwify, mude também `CASAMENTO_BUMP_MARIDO` ou `CASAMENTO_BUMP_RITA` no `.env`.

## 3. Upsell de 1 clique (página de obrigado)

- **Produto:** o que já existe, **Os Santos Protetores da Sua Família + Devocionário de Bônus**. Crie uma oferta nova nele por **R$ 27** (o nome da oferta pode ser "Upsell casamento").
  - O servidor entrega pelo nome do produto, que já é reconhecido (fluxo da Família, com o devocionário de bônus).
- Na Kiwify, no "Gerador de upsell" dessa oferta:
  - **Ao aceitar / ao recusar:** deixe em "área de membros". A página define o destino, como nas outras ofertas.
  - Do código gerado, copie o trecho depois de `kiwify-upsell-trigger-` e cole em `UPSELL_ID` no `site/config.js`.
  - Confira se o `<script src="...">` do código é igual ao `UPSELL_SCRIPT` do `config.js`.
  - O link do checkout da oferta vai em `CHECKOUT_UPSELL`: é a reserva para quem pagou no Pix.

## 4. Anúncios (Meta)

**Legenda única (copiar e colar):**

> Todo casamento acontece no dia de um santo. 💍✝
>
> Na Igreja, cada dia do ano recorda um santo ou celebra uma festa. O dia em que vocês disseram sim também tem o seu.
>
> Descubra de graça, em 1 minuto: digite a data do casamento e veja qual santo a Igreja recordava naquele dia.
>
> Se quiser, leve o livro de orações do casal, feito com o nome de vocês dois: a história do santo, a oração do casal, a novena de 9 dias e um quadro para emoldurar. Também é um presente bonito de bodas. 🙏
>
> 👉 Toque em Saiba mais.

- **Título:** Descubra o santo do dia do seu casamento
- **Descrição:** Grátis · 1 minuto
- **Botão:** Saiba mais
- **Link:**
  ```
  https://casamento.meusantoprotetor.online/?utm_source=facebook&utm_medium=pago&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
  ```

**Criativos** (`kit/criativos/`):

| Arquivo | Formato | Conjunto | Ideia |
|---|---|---|---|
| `e1-qual-destes.png` | 4:5 | A | "Qual destes é o santo do seu casamento?" (A/B/C, como o campeão do devocionário) |
| `e2-pergunte-em-casa.png` | 4:5 | A | "Em que dia de santo vocês se casaram?" (no formato do "pergunte à sua mãe") |
| `e3-datas.png` | 4:5 | A | Datas reais e o santo de cada uma, terminando em "E o dia de vocês?" |
| `e4-vela.png` | 4:5 | A | Vela: "Desde o dia do seu sim, um santo reza pelo seu casamento" |
| `e7-conversa.png` | 4:5 | A | Conversa de WhatsApp com a mãe, em formato de cena (não é depoimento de cliente) |
| `v1-calendario.mp4` | 9:16, 13 s | A | As folhas do calendário passam com o santo de cada dia |
| `v2-vela.mp4` | 9:16, 12 s | A | Vela e alianças com a frase em três partes |
| `e5-produto-preco.png` | 4:5 | B | O livro, o que vem nele e o preço |
| `e6-presente-bodas.png` | 4:5 | B | Presente de bodas (traz o aviso "imagem ilustrativa") |
| `e8-quadro.png` | 4:5 | B | O quadro emoldurado |
| `v3-livro.mp4` | 9:16, 14 s | B | As páginas do livro por dentro, terminando com o preço |

- Os vídeos não têm áudio: escolha a música na biblioteca do Meta.
- As páginas mostradas nos criativos são de um livro de exemplo ("Ana e José"), e os criativos dizem isso.
- **Não use** escassez nem prazo que não seja verdadeiro, depoimento inventado ou "de/por" falso.
- **Prazo verdadeiro para usar em maio e junho:** "Para chegar à festa de Santo Antônio (13/6) com os nove dias da novena do casal completos, comece até 4 de junho." (4/6 a 12/6 são os nove dias, e a festa é no dia seguinte, como no prazo do Natal do manual.) Esse prazo **sai do ar no dia 5/6**.
