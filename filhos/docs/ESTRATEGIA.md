# Novena pelos Filhos: a linha de raciocínio

*Produto novo do Meu Santo Protetor. Feito em 23/11/2026. Sem chave, senha nem dado de cliente.*

## 1. O pedido

- Mais um produto religioso, **por uns R$ 85**, usando o que o Carlos já sabe fazer: **vídeo com IA e voz narrada**.
- Para vender em tráfego pago, com as regras de sempre (sem promessa, sem escassez falsa, sem atributo pessoal na copy).

## 2. A ideia

> **Todo filho nasce no dia de um santo.**

É o gancho que já vendeu mais de mil devocionários, apontado para a intenção mais forte desse público: **rezar pelos filhos e pelos netos**. A pessoa escreve o nome e o aniversário de cada filho (ou neto), vê **de graça** o santo do dia de cada um e recebe a oferta de uma **novena em vídeo**, com um livro feito com o nome e o santo de cada um.

**Por que R$ 87 é crível aqui** (e R$ 87 em vez de R$ 85: segue o padrão 37 · 47 · 97 da marca; a diferença de R$ 2 não muda a decisão e dá para trocar na Kiwify e no `config.js` se preferir R$ 85):
- é o único produto da marca **com vídeos**: 9 vídeos narrados, um por dia, que a pessoa assiste e reza junto. Isso parece um "retiro em casa", não um PDF;
- o livro é **para a família toda** (até 6 filhos e netos, cada um com o seu santo e a sua oração);
- tem **acompanhamento**: a página da novena marca os dias rezados, e chega um lembrete de manhã nos 9 dias.

| Critério | Como a ideia se sai |
|---|---|
| **Público** | O mesmo do Meu Santo: mulheres católicas de 35 a 65 anos, mães e avós. "Por quem mais reza" é quase sempre pelos filhos. |
| **Emoção** | Amor, cuidado e esperança. Toca em dores (filho longe, vício, doença), mas a novena é sobre entregar e confiar, não sobre medo. |
| **Ticket** | R$ 87 + bumps de R$ 19,90 e R$ 14,90 + upsell de R$ 37. |
| **Escada** | No 9º dia, o e-mail convida para a Consagração a Jesus por Maria (R$ 37, já existe). |
| **Risco** | Médio-baixo. Os temas sensíveis (vício, depressão, filho que faleceu) têm texto próprio e os avisos de ajuda (CVV 188, CAPS, Al-Anon, Nar-Anon, Amor-Exigente, Disque 100). |
| **Evergreen** | Não depende de data. Datas reais podem virar prazo verdadeiro (seção 7). |

**Ideias que considerei e deixei de lado:**
- **Consagração a Nossa Senhora em vídeo:** o manual sugere, mas o produto de R$ 37 já existe. Vender uma versão de R$ 87 do mesmo tema confunde quem já comprou.
- **Rezo por Quem Partiu** (o santo do dia em que a pessoa faleceu): forte, mas mexe com luto, e R$ 87 por um produto de luto tem cara de aproveitamento. Aqui, quem perdeu um filho pode incluí-lo na novena com uma oração própria, sem que o produto seja "sobre" isso.
- **Advento ou Natal:** só vende por 3 semanas e não daria tempo de gravar os vídeos.
- **33 vídeos diários (uma consagração inteira em vídeo):** custaria mais do que o dobro de créditos da ElevenLabs e semanas de edição. Nove vídeos curtos cabem no que o Carlos já faz.

## 3. O produto

**Novena pelos Filhos (em vídeo)**, R$ 87:
1. **9 vídeos narrados** (3 a 4 min cada), com a voz do Jorge: abertura, leitura (só a referência), reflexão, o momento em que a pessoa diz o nome de cada filho, a oração do dia, um gesto, Pai-Nosso, Ave-Maria e Glória. Os temas: os filhos que Deus me confiou · a oração que não desiste · a fé que passa de geração em geração · proteção e anjos da guarda · saúde do corpo, da mente e do coração · o filho que está longe · trabalho, estudos e o futuro · paz em casa e união entre irmãos · debaixo do manto de Maria (consagração).
2. **O livro da novena em PDF** (~29 páginas, A4) com o nome de cada um: carta, como rezar (com o link dos vídeos), **o santo de cada um** (texto da IA), **a oração de cada um** (IA), Santa Mônica (história verificada e o que ela ensina), os 9 dias, o Ato de Consagração com os nomes e o **certificado** para imprimir, como dar a bênção, 15 orações para cada situação, as orações de sempre, o quadro com os nomes e a palavra final com os contatos de ajuda.
3. **A página da novena** (`novena.html`): os 9 vídeos, a oração do dia já com os nomes embaixo do vídeo, a marcação dos dias rezados, os santos de cada um e os downloads.
4. **Lembrete por e-mail** de manhã, do 2º ao 9º dia (com link para parar).

**A IA escreve só 3 campos:** a carta, o texto do santo e a oração de cada pessoa, e a intenção da novena. Tudo o mais é texto fixo, revisado contra as regras. **Se a IA falhar, o livro sai igual, com texto padrão.** Os textos são escritos uma vez por quiz e reaproveitados nos bumps e no upsell.

**Order bumps** (acima de R$ 10):
- **Terço pelos Filhos (em vídeo)**, R$ 19,90: um terço meditado com os mistérios gozosos (a infância de Jesus), cada mistério oferecido pelos filhos, e o roteiro em PDF com os nomes. *Só ligue quando o vídeo estiver pronto.*
- **30 Bênçãos para Mandar aos Filhos**, R$ 14,90: 30 mensagens curtas para cada filho, já com o nome e no gênero certo. Na página da novena, cada uma tem botão de **copiar** e de **mandar no WhatsApp**.

**Upsell de 1 clique** (página de obrigado): **Um Livro para Cada Filho**, R$ 37. Um PDF para cada filho ou neto vivo, para a mãe mandar pelo WhatsApp ou imprimir: capa com o nome, o santo do dia do nascimento, "a oração que sua mãe reza por você", uma oração para ele mesmo (por idade), a bênção e um santinho para recortar. Não precisa de formulário (usa o quiz) nem de IA extra. Bônus de marca: cada livro que a mãe repassa leva "Meu Santo Protetor (meusantoprotetor.online)" para dentro da casa dos filhos.

## 4. O funil

```
Anúncio (curiosidade ou produto) → filhos.meusantoprotetor.online
  → quiz de 1 minuto: quem reza (mãe, avó, pai, avô) · seu nome · filhos e netos (nome, filho/filha/neto/neta, data, ano opcional, "já partiu") · até 3 pedidos · algo mais (opcional)
  → revelação grátis: o santinho de cada um, "Santo Antônio, rogai por Pedro"
  → oferta: VSL (Carlos) · capa com os nomes · o que vem · os 9 dias · páginas de exemplo · R$ 87 · garantia · FAQ
  → Kiwify (sck = o pedido do quiz) + 2 bumps
  → obrigado.html: upsell Um Livro para Cada Filho (1 clique) → "a sua novena está pronta" → novena.html
  → e-mail com o link e o PDF + 8 lembretes diários
```

Os dados vêm **antes** da compra (no quiz) e vão no `sck`, como no casamento: nada de formulário depois do pagamento. A página de dados é só a reserva para quem compra pelo link direto do checkout.

## 5. Números de referência

Taxa da Kiwify: ~8,99% + R$ 2,49 (contando os R$ 2,49 em cada item, como no casamento, para ficar do lado seguro).

| Item | Preço | Líquido |
|---|---|---|
| Novena pelos Filhos | R$ 87,00 | **~R$ 76,70** |
| Terço pelos Filhos | R$ 19,90 | ~R$ 15,60 |
| 30 Bênçãos | R$ 14,90 | ~R$ 11,10 |
| Um Livro para Cada Filho (upsell) | R$ 37,00 | ~R$ 31,20 |

- **Empate só com a novena: cada venda pode custar até ~R$ 76.** Para empatar no líquido, o ROAS que o Meta mostra (sobre o valor bruto da novena) precisa ficar em **~1,13**.
- Se 25% levarem o terço, 30% as bênçãos e 10% o upsell (chute razoável, a confirmar), cada comprador deixa **~R$ 87 líquidos**, e o empate sobe para **~R$ 87 por venda**.
- **Custo da IA:** ~US$ 0,06 a 0,12 por compra com o Claude Opus 5.5 (depende de quantos filhos). Para gastar menos: `FILHOS_MODELO=claude-sonnet-5-5`.
- **Custo da ElevenLabs:** uma vez só, uns 23 mil créditos (contados nos roteiros), mais margem para regravar.
- **E-mails:** até 9 por comprador (entrega + 8 lembretes). Com 30 vendas por dia, são ~270 e-mails por dia na Resend (o plano Pro aguenta com folga).

**Comparação honesta com a Família (R$ 47, com VSL):** a Novena custa quase o dobro, então a taxa de compra vai ser menor. O que segura o preço é o quiz (a pessoa já viu o santo de cada filho e se envolveu) e a VSL. Se, depois de umas 300 revelações, menos de 2% clicarem em comprar, o primeiro teste é **o preço (R$ 67)**, sem mudar mais nada ao mesmo tempo.

## 6. Anúncios

- **2 conjuntos** com verba de verdade (US$ 15 a 20 por dia cada), criativos testados dentro do conjunto:
  - **Conjunto A (curiosidade):** E1 qual destes, E2 pergunte em casa, E3 datas, E5 Santa Mônica, E8 conversa (cena), V1 calendário, V2 velas, e os narrados A1, A2 e A3.
  - **Conjunto B (produto):** E4 velas com nomes, E6 produto e preço, E7 os 9 dias, E9 quadro, V3 por dentro, os narrados A4 e A5 e os cortes da VSL.
- Desligue o criativo que gastou US$ 10 a 15 sem compra. Compare os conjuntos pelo custo por compra depois de uns US$ 40.
- **Não** rode a Família e a Novena no mesmo conjunto: são públicos parecidos. Dê à Novena uma campanha própria e compare o custo por compra de cada uma.
- **Sem atributo pessoal na copy:** nada de "Você é mãe?", "Seu filho está longe de Deus?".

## 7. Prazos verdadeiros que podem entrar mais tarde

O 9º dia da novena é a consagração a Nossa Senhora. Dá para casar o fim da novena com uma festa real, sempre com a data em que o prazo sai do ar:

| Para terminar no dia… | Comece até… | O prazo sai do ar em… |
|---|---|---|
| **24/12** (véspera de Natal) | 16/12/2026 | 17/12/2026 |
| **2/2/2027** (Apresentação do Senhor, Nossa Senhora das Candeias) | 25/1/2027 | 26/1/2027 |
| **11/2/2027** (Nossa Senhora de Lourdes) | 3/2/2027 | 4/2/2027 |
| **9/5/2027** (Dia das Mães) | 1/5/2027 | 2/5/2027 |
| **27/8/2027** (Santa Mônica) | 19/8/2027 | 20/8/2027 |

Nove dias, contando o dia em que começa. **Nada disso entra agora**: primeiro, a versão sem prazo precisa provar que vende.

## 8. O que conferir no primeiro teste (honestidade sobre o que não deu para testar daqui)

1. **Os vídeos.** Nada aqui substitui assistir aos 9 vídeos do começo ao fim no celular.
2. **O texto da IA de verdade.** Os testes rodaram com o texto padrão (sem chave da API aqui). Rode `filhos.py teste SEU_EMAIL ia` na VPS e leia o PDF.
3. **Como a Kiwify manda os bumps e o upsell.** O servidor aceita bumps no mesmo aviso ou em avisos separados, e o upsell sem `sck` (usa o quiz da compra recente do mesmo e-mail). Confira com `filhos.py buscar EMAIL` depois da primeira compra.
4. **O script do upsell de 1 clique** (`UPSELL_SCRIPT`): segue o padrão da Kiwify, mas confira com o código que o "Gerador de upsell" gerar.
5. **A tabela de santos da VPS.** Os testes usaram uma tabela de mentira. Rode `filhos.py santo 13 6` e `filhos.py santo 25 12`.
6. **O gerador de PDF da VPS.** `filhos.py diagnostico` mostra qual funciona. O livro foi testado com o Chromium e com o WeasyPrint.
7. **O suporte por IA (`suporte_ia.py`) não conhece este produto** (nem o casamento). Se uma cliente responder "não recebi", use `filhos.py buscar EMAIL` e o link da página da novena que ele mostra.
