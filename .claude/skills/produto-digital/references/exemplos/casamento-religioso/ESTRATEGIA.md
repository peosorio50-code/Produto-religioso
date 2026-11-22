# O Santo do Nosso Casamento: a linha de raciocínio

*Produto novo do Meu Santo Protetor. Feito em 20/11/2026. Sem chave, senha nem dado de cliente.*

## 1. O que o manual pedia

- **Subir o ticket.** Com ROAS em torno de 1, o devocionário de R$ 19 só empata. O objetivo é vender de R$ 37 a R$ 97.
- **Reaproveitar o que já foi validado.** O gancho *"Todo mundo nasce no dia de um santo. Descubra o seu."* passou de mil vendas. A mecânica é: a pessoa digita uma data, vê o santo de graça e recebe a oferta de um material feito com o nome dela.
- **Sem nada que exija mentir:** sem escassez falsa, sem depoimento inventado, sem promessa de graça.

## 2. A ideia: o mesmo gancho, numa data nova

> **Todo casamento acontece no dia de um santo.**

É verdade (todo dia do calendário da Igreja recorda um santo ou celebra uma festa), é curioso, quase ninguém sabe a resposta e dá para descobrir em 1 minuto. É o gancho vencedor aplicado a uma data com muito mais carga emocional do que o aniversário: **o dia do sim**.

Por que casamento e não outra data:

| Critério | Por que ajuda |
|---|---|
| **Público** | É o mesmo do Meu Santo: mulheres católicas de 35 a 65 anos, mães e avós. A maioria é casada há 10 a 40 anos. |
| **Emoção positiva** | Gratidão, memória e família. Rezar pelo casamento e pelo marido é uma devoção muito comum (Santa Rita e Santa Mônica são as santas disso). |
| **Presente** | Bodas e aniversário de casamento dos pais e dos padrinhos. A data existe o ano todo, então o produto não depende de época. |
| **Ticket** | São duas pessoas e um livro mais rico, com quadro para emoldurar. R$ 37 é crível: o dobro do devocionário, abaixo da Família (R$ 47). |
| **Escada** | Depois do casal, a oferta natural é "e o santo de cada pessoa da casa?", que é a Família (já existe). |
| **Risco** | Baixo. Não toca em doença, luto nem dinheiro, e não promete nada. |

**Ideias que considerei e deixei para depois:**
- **Advento 2026** (começa em 29/11, uma data real): só vende por 3 semanas e disputa espaço com o Natal da Família.
- **"Rezo por quem partiu"** (o santo do dia em que a pessoa faleceu, com a lembrança de 7º dia): é forte, mas mexe com o luto e pede muito mais cuidado na copy e no atendimento. É um bom candidato a próximo produto, com a mesma estrutura deste.
- **Consagração a Nossa Senhora com VSL** (sugerida no manual): é um produto que já existe; o que falta é a VSL, não um produto novo.

## 3. O produto

**O Santo do Nosso Casamento: livro de orações do casal (PDF, 19 páginas, A4)**, feito com o nome dos dois:

1. Capa com os nomes, a data e o santo do dia do casamento.
2. Carta ao casal (IA) e, se for presente, a dedicatória de quem deu.
3. **O santo do dia do casamento:** quem foi e o que o exemplo dele diz ao casal (IA, só com fatos seguros). Mais o santo de cada um, se os aniversários forem informados.
4. **A oração do casal** com os dois nomes e os pedidos (IA) + a oração de quem reza pelo cônjuge.
5. Uma página sobre o sacramento. Ela muda se o casal se casou só no civil, sem julgamento.
6. **Novena do casal:** 9 dias, cada um com leitura (só a referência), reflexão e oração.
7. Os santos dos casais: Sagrada Família, São José, Joaquim e Ana, Luís e Zélia Martin, Mônica, Rita e Antônio.
8. Renovação das promessas em casa (o passo a passo e a fala de cada um).
9. Orações para cada momento: briga, falta de dinheiro, doença, a fé do cônjuge, o aniversário, a hora de dormir e os dias difíceis.
10. As orações de sempre e o calendário do casal de 2027.
11. Quadro "Unidos por Deus" para imprimir e emoldurar, e a palavra final ("não somos paróquia").

**A IA escreve só 6 campos.** Todo o resto é texto fixo, revisado contra as regras do manual. Se a IA falhar (sem crédito, fora do ar), o livro sai do mesmo jeito, com texto padrão. **Ninguém fica sem entrega:** essa é a lição de 10 a 12/11, quando 48 compras ficaram paradas.

**Order bumps** (acima de R$ 10, por causa da taxa):
- **30 Dias Rezando pelo Meu Marido** (ou pela minha esposa): R$ 14,90. Um tema, uma oração com o nome e um gesto por dia. Não usa IA.
- **Novena de Santa Rita pelo Casamento**: R$ 12,90. Nove dias com a história dela e o pedido do casal. Não usa IA.

**Upsell na página de obrigado:** *Os Santos Protetores da Sua Família* por R$ 27, só nessa página (o preço normal é R$ 47). É um produto que já existe e o servidor já entrega. Se a compradora informou o próprio aniversário no quiz, o devocionário de bônus sai sem formulário.

## 4. O funil

```
Anúncio (curiosidade ou produto) → casamento.meusantoprotetor.online
  → quiz de 1 minuto: para quem é · nomes · data do casamento · na Igreja? · pedidos · aniversários (opcional) · algo mais (opcional)
  → revelação grátis: "Vocês se casaram no dia de Santo Antônio" + "Santo Antônio, rogai por Ana e por José" + anos de casados
  → oferta: capa com os nomes, o que vem no livro, páginas de exemplo, R$ 37, garantia, FAQ
  → Kiwify (sck = o pedido do quiz) + 2 bumps
  → obrigado.html: upsell da Família (1 clique) → livro pronto para baixar na própria página + e-mail com o PDF
```

**A mudança mais importante em relação ao Meu Santo:** os dados são pedidos **antes** da compra (no quiz) e vão para a Kiwify no `sck`. O livro é gerado assim que o pagamento é aprovado, **sem formulário depois da compra**. Isso ataca de frente o maior problema do manual: as 187 compras paradas em `aguardando_dados`. A página de dados existe só para quem compra pelo link direto do checkout, sem passar pelo quiz.

## 5. Números de referência

- **Líquido por venda** (taxa da Kiwify de ~8,99% + R$ 2,49, a mesma conta que dá ~R$ 40 nos R$ 47 da Família):
  - livro sozinho: ~R$ 31;
  - com o bump de R$ 14,90: ~R$ 42;
  - com os dois bumps: ~R$ 51.
- **Empate:** cada venda pode custar **até ~R$ 31**, sem contar os bumps e o upsell. Para empatar no líquido, o ROAS que o Meta mostra precisa ficar em ~1,2.
- **Custo da IA:** ~US$ 0,05 por livro com o Claude Opus 5.5. Para gastar menos, troque para o Sonnet com `CASAMENTO_MODELO=claude-sonnet-5-5`.

## 6. Anúncios (as regras do manual valem aqui)

- **2 conjuntos** com verba de verdade (US$ 15 a 20 por dia cada), com os criativos testados dentro do conjunto:
  - **Conjunto A (curiosidade e participação):** E1 qual destes, E2 pergunte em casa, E3 datas, E4 vela, E7 conversa, V1 calendário e V2 vela.
  - **Conjunto B (produto e presente):** E5 produto e preço, E6 presente de bodas, E8 quadro e V3 o livro por dentro.
- Desligue o criativo que gastou US$ 10 a 15 sem compra. Compare os conjuntos pelo custo por compra depois de uns US$ 40.
- **Mude uma coisa por vez.** Antes de mexer em criativo por queda de vendas, confira o checkout e o rastreamento.
- **Sem atributo pessoal na copy** ("Você é católica?", "Seu casamento está em crise?"). A copy fala do dia, do santo e do livro.
- **Datas reais que podem virar prazo verdadeiro mais tarde:**
  - **Santo Antônio (13/6):** para chegar à festa com os nove dias da novena completos, é preciso começar até **4 de junho** (4/6 a 12/6).
  - **Dia dos Namorados:** 12/6.
  - **Sagrada Família:** 27/12/2026 e 26/12/2027.

## 7. O que conferir no primeiro teste (honestidade sobre o que não deu para testar daqui)

1. **Como a Kiwify manda os bumps.** O servidor aceita os dois jeitos (no mesmo aviso ou em avisos separados) sem duplicar o livro. Confira com `casamento.py buscar EMAIL` depois da primeira compra.
2. **O código do upsell de 1 clique.** O endereço do script (`UPSELL_SCRIPT` no `config.js`) segue o padrão da Kiwify, mas confira com o código que o "Gerador de upsell" gerar.
3. **A tabela de santos da VPS.** Os testes usaram uma tabela de mentira. Rode `casamento.py santo 25 12` e `casamento.py santo 13 6` para ver os nomes reais. Os dias de festa do Senhor (Natal, Batismo...) são reconhecidos pelo nome e trocam a invocação por "Santa Maria, Mãe de Deus, rogai por nós".
4. **O gerador de PDF da VPS.** O `casamento.py diagnostico` mostra se é o Playwright, o WeasyPrint ou o Chromium. O livro foi testado com o Chromium e com o WeasyPrint.
5. **O suporte por IA (`suporte_ia.py`) não conhece este produto.** Se uma cliente responder "não recebi", ele não vai achar a compra na tabela `compras`. Peça ao Claude que acrescente uma consulta à tabela `casamento_compras` (o arquivo não estava no kit que recebi). Enquanto isso, use `casamento.py buscar EMAIL`.
