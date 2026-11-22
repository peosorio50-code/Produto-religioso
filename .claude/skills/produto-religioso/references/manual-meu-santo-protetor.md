# Meu Santo Protetor: manual completo do negócio católico

*Atualizado em 18/11/2026. Escrito para ser entregue a outro Claude, que vai continuar o trabalho com o sócio do Carlos. Este documento não contém nenhuma chave, senha, token nem dado de cliente: tudo isso fica só no `.env` da VPS e nos painéis (Kiwify, Resend, Anthropic, Meta).*

**Para o Claude que vai ler isto:** este é o contexto de trabalho de um negócio de produtos digitais católicos, vendidos com anúncios no Meta e checkout na Kiwify, entregues por um servidor próprio que gera PDFs personalizados com IA. Leia tudo antes de começar. As seções 2 (regras) e 10 (dinâmica de trabalho) valem para todas as respostas.

---

## 1. Visão geral

**Marca:** Meu Santo Protetor (`meusantoprotetor.online`). Separada de propósito de outras marcas do mesmo servidor: o público católico não pode ver "mapa astral" nem nada esotérico em domínio, e-mail ou página.

**Público:** católicos brasileiros, principalmente mulheres de 35 a 65 anos, mães e avós, que rezam pela família. Chegam por anúncio frio no Facebook e no Instagram.

**Gancho central (validado com mais de mil vendas):** *"Todo mundo nasce no dia de um santo. Descubra o seu."* A pessoa digita o dia e o mês em que nasceu e vê, **de graça**, o santo que a Igreja recorda nesse dia. Depois recebe a oferta de um devocionário feito com o nome dela.

**A lógica de todos os produtos:** material de oração **personalizado com o nome da pessoa** (e da família), gerado por IA dentro de regras doutrinárias rígidas, entregue em PDF no e-mail em poucos minutos.

**Situação financeira assumida:** ROAS em torno de 1 (empate). Ao discutir os produtos, **assuma ROAS 1 ou mais e não peça o gasto de anúncio.** O Carlos avisa quando estiver no lucro. Por isso o objetivo atual é **subir o ticket**: vender produtos de R$ 47 a R$ 97 em vez de depender só do devocionário de R$ 19.

---

## 2. Regras inegociáveis

### Doutrina e conteúdo (estão no código da IA e valem para toda copy)
- Santo **não é adorado**: é honrado e **intercede**. Quem concede as graças é Deus.
- **Nunca** prometer graça, cura, dinheiro, emprego, casamento, nem que "a família vai mudar".
- **Nunca** superstição, corrente, simpatia, milagre inventado, data ou fala inventada sobre um santo.
- Pedido pela saúde de alguém: reza pela pessoa e lembra com delicadeza de buscar também o cuidado médico.
- Sempre deixar claro que **não somos paróquia** e que **nada substitui a missa, os sacramentos ou o padre**.
- A voz da VSL pode *soar* como a de um padre, mas **nunca pode dizer ou insinuar que é padre** ("eu, como sacerdote", "abençoo você"). O narrador é "da equipe do Meu Santo Protetor".
- Nada de vocabulário evangélico nos produtos católicos, e vice-versa.

### Anúncios e vendas (regras do Meta e honestidade)
- **Sem** depoimento inventado, preço "de/por" falso, escassez ou contagem regressiva falsa, "digite amém" ou isca de engajamento.
- **Sem atributo pessoal** na copy: nada de "Você é católica?". O texto fala do produto e da situação, não afirma a religião ou a saúde de quem lê.
- **Prazos só se forem verdadeiros.** Exemplo em uso: "para rezar a novena da família antes do Natal, comece até 16 de dezembro" (9 dias até o dia 25). **A partir de 17/12, esse prazo tem que sair** da página `/familia`, da página `/biblioteca`, da VSL (bloco 08) e dos criativos de Natal.
- O "R$ 133,70 separados" da Biblioteca é verdadeiro: é a soma dos preços avulsos reais.
- Bíblia: quando citar um versículo, usar a **Bíblia Livre** (licença CC BY), com a fonte escrita.
- **Não fazer:** cloaker, domínio ou pixel novo para fugir da classificação do Meta, rodízio de números de WhatsApp, contas falsas em serviços de e-mail, ferramentas de spam baixadas de fórum, disparo para lista comprada ou raspada.

### Segurança e operação
- **Chaves nunca no chat.** A chave da API da Anthropic, as chaves da Resend e da Kiwify e o `ADMIN_CHAVE` ficam **só** em `/opt/mapadaalma/.env`, na VPS. Se precisar trocar uma chave, o comando edita o `.env` direto na VPS.
- **A VPS é compartilhada com outro negócio do Carlos (um bot de WhatsApp).** **Nunca** reiniciar o Docker, nunca rodar `do-release-upgrade`, nunca reiniciar a máquina no meio de entregas. Pode ignorar o aviso "System restart required".
- Arquivos de entrega e zips **nunca** levam o `.env` (use `zip ... -x '.env'`).
- **LGPD:** nada de e-mail, CPF ou telefone de cliente em arquivos de documentação. As planilhas de venda da Kiwify têm dados pessoais: use só para totais e não guarde.
- A VPS **não tem o programa `sqlite3`**. Consultas no banco são feitas com `python3`.

---

## 3. Infraestrutura

| Peça | O que é | Onde |
|---|---|---|
| **Servidor** | FastAPI + SQLite, serviço `mapadaalma` (systemd), porta 8010 | VPS Hostinger, `root@srv2014776` (IP 2.25.252.204), pasta `/opt/mapadaalma` |
| **Banco** | SQLite em `/opt/mapadaalma/dados/mapa.db` | tabelas `clientes`, `compras`, `recuperacao`, `ofertas`, `eventos` |
| **API pública** | `https://api.mapadaalma.online` (via Cloudflare Tunnel `mapadaalma-vps` → `localhost:8010`) | o webhook e as páginas de dados usam esse endereço |
| **Site** | HTML estático no **Cloudflare Pages**, projeto do Meu Santo Protetor | `meusantoprotetor.online` (também responde em `meusantoprotetor.pages.dev`) |
| **IA** | API da Anthropic, modelo padrão `claude-sonnet-5-5` (variável `MAPA_MODELO`) | chave em `ANTHROPIC_API_KEY` no `.env` |
| **E-mail** | Resend, plano **Pro** | remetente `contato@meusantoprotetor.online`; respostas vão para o Gmail do Carlos via Email Routing do Cloudflare |
| **Checkout** | Kiwify | um webhook só para todos os produtos: `/webhook/kiwify/<segredo>` |
| **Pixel** | Meta, ID `1108457205151516` | o Meta classificou os domínios na categoria **"Religião"**: no Brasil ficam em "configuração básica" (veja a seção 8) |
| **Voz das VSLs** | ElevenLabs, voz **"Jorge – Calm & Warm"**, modelo Eleven v4, Stability no meio, Similarity ~75%, sem Auto-tag, MP3 128 kbps | conta do Carlos (tinha ~38 mil créditos em 17/11) |

### A API da Anthropic (a mesma de sempre)
- O servidor usa **a mesma chave da Anthropic que já está no `.env`**. O Claude do sócio não precisa da chave para nada: ele só escreve código e comandos. A chave nunca deve aparecer no chat.
- **Em 10 a 12/11, o crédito acabou e 48 compras pagas ficaram sem entrega.** Gerou reclamação de "golpe". Lição: no console da Anthropic, em **Billing**, deixar a **recarga automática ligada** (por exemplo, recarregar US$ 50 quando o saldo cair abaixo de US$ 20).
- A v14c em diante tem proteção: a compra que falha volta sozinha para a fila a cada 30 min (até 9 tentativas), a chamada tenta de novo quando a API está sobrecarregada (`max_retries=6`), e chega no máximo 1 alerta a cada 30 min no e-mail do admin.

### Terminais (sempre dizer qual)
- **Mac:** `carlosaugusto@macbook`. É de onde os zips saem para a VPS:
  `scp -o ServerAliveInterval=20 ~/Downloads/ARQUIVO.zip root@2.25.252.204:/root/`
- **VPS:** `root@srv2014776`. Instalação padrão de uma atualização:
  `cd /opt/mapadaalma && cp servidor.py backup-servidor-ANTERIOR.py && unzip -o /root/ARQUIVO.zip -d /opt/mapadaalma && chown mapa:mapa ARQUIVOS && systemctl restart mapadaalma && sleep 4 && curl -s localhost:8010/health`
- Sempre usar `-o ServerAliveInterval=20` em `ssh` e `scp`.

---

## 4. Produtos (estado em 18/11/2026)

O servidor identifica o produto pelo **nome na Kiwify**, sem acento e sem diferenciar maiúscula, procurando trechos definidos no `CFG` do `servidor.py` (`PRODUTO_*`, com alternativas separadas por `|`). **Mudar o nome de um produto na Kiwify sem atualizar esses trechos faz a venda não ser entregue.** Isso já aconteceu com outro produto e perdeu 2 vendas.

| Produto (nome na Kiwify) | Preço | SKU | Checkout | Página de vendas | Página de dados/obrigado | Entregável |
|---|---|---|---|---|---|---|
| **Devocionário do Meu Santo Protetor** | R$ 19 (oferta de teste R$ 24,90: `C4d1i87`) | `santo` | `D68zu9g` | `/` (quiz A), `/b` (página B, **a que mais vende**), `/a24`, `/qb` | `/dados` | PDF de ~15 págs: o santo do dia em que nasceu, história, 3 virtudes, oração com nome e pedido, novena de 9 dias, orações de sempre, proteção do lar, santinho e papel de parede |
| **Calendário de Fé 2027** | R$ 10,90 (bump do devocionário) | `santo_cal` | — | — | `/dados` | 12 meses com as festas de 2027, o dia do santo marcado, intenção e oração por mês |
| **Os Santos Protetores da Sua Família + Devocionário de Bônus** (antigo "Livro de Orações da Família") | R$ 47 | `livro_familia` (+ `santo` de bônus) | `GJSYLJP` | `/familia` (com VSL) | `/dados-familia`; obrigado → `/oferta-completa` | Até 8 pessoas: santo, história, oração pelo nome, aniversário, santinhos para recortar, novena da família, Natal em família (presépio e bênção da ceia), consagração do lar, calendário da família 2027. **Bônus:** o devocionário de quem comprou |
| **Consagração a Jesus por Maria em 33 dias** | R$ 37 (oferta de R$ 27 para upsell antigo) | `consagracao` | `ZdbeE6m` | `/consagracao` | `/dados-consagracao` | Os 33 dias de São Luís de Montfort, meditação diária, Ato de Consagração com o nome, certificado |
| **Rezo por Você** (orações por quem está doente) | R$ 19,90 | `enfermo` | `fjiM4ZV` | `/enfermo` | `/dados-enfermo` | Novena de São Rafael, bênção de cabeceira, oração para cada momento do tratamento |
| ↳ **Santo Protetor de Quem Eu Amo** | R$ 12,90 (bump do Rezo) | `enfermo_santo` | — | — | `/dados-enfermo` | o santo da pessoa doente |
| ↳ **Cartões de Fé** | R$ 10,90 (bump do Rezo) | `enfermo_cartoes` | — | — | `/dados-enfermo` | 30 imagens de oração |
| **Biblioteca da Família Católica: 5 Livros de Oração para a Sua Casa** | R$ 97 público · R$ 77 cliente · **R$ 37 "completa"** | `biblioteca` → libera `santo`, `livro_familia`, `consagracao`, `enfermo`, `santo_cal` | 97: `4Rt3Bma` · 77: `2pkNTSq` · 37: `hyPTemQ` | `/biblioteca` (com VSL) | `/dados`; upsell 77 em `/oferta-biblioteca` | Os 5 livros. **O servidor entrega só os que a pessoa ainda não tem** |

Todos os checkouts ficam em `https://pay.kiwify.com.br/<código>`.

**Padrões da Kiwify:** checkout com fundo `#F8F3EE` e botões `#17295A`; garantia de 7 dias; bumps sempre acima de R$ 10 (abaixo disso a taxa da Kiwify é maior); webhook com a mesma URL e os mesmos eventos (compra aprovada, recusada, Pix/boleto gerado, carrinho abandonado e reembolso). Cada webhook tem um token, e o `.env` aceita vários: `KIWIFY_TOKEN=tok1,tok2,...`.

**Upsell de 1 clique (Kiwify, "Gerador de upsell"):** os campos "Ao aceitar" e "Ao recusar" só oferecem "área de membros" ou "outra upsell". Deixe em área de membros, porque a página do upsell define o destino. O código gerado traz um ID (o trecho depois de `kiwify-upsell-trigger-`), que vai no `UPSELL_ID` da página. O link do checkout da mesma oferta vai no `CHECKOUT_UPSELL`, como reserva para quando o 1 clique não funciona (quem pagou com Pix não tem 1 clique).

---

## 5. Os funis

### 5.1 Devocionário (R$ 19): o que paga as contas
1. Anúncio → **página B** (`/b`). A B vendeu o dobro da A (78 contra 38 vendas no mesmo período).
2. **Quiz:** nome, dia e mês de nascimento, por quem mais reza, como está o coração e um pedido (opcional).
3. **Revelação grátis:** o santinho, o nome do santo, "Você nasceu em…", o padroado e o "rogai por nós".
4. **Versão de 16/11 da B:**
   - santinho menor e uma seta "Veja o que preparamos para você ↓";
   - logo abaixo, **a capa do devocionário com o nome da pessoa e o santo dela**, a lista do que vem e o botão **"Quero o devocionário de [santo]"**, com "Feito para [nome] · R$ 19 · pagamento único" e a garantia embaixo;
   - na oferta, **o pedido que a pessoa escreveu aparece dentro da novena**.
5. Checkout da Kiwify, com o bump do Calendário (R$ 10,90). **O bump do livro da família foi tirado.**
6. **Página de obrigado** = `/oferta-biblioteca`: upsell da Biblioteca por R$ 77 com 1 clique (ID `2pkNTSq`). Aceitando ou recusando, a pessoa vai para `/dados`.
7. `/dados` → a pessoa confirma o e-mail e a data → a IA gera → o PDF chega no e-mail.

**Números de referência:**
- De 9 a 13/11, eram **33 a 41 devocionários por dia**. Caiu para 24 (14/11), 15 (15/11) e 4 (16/11, até o meio-dia).
- **A causa ainda não foi confirmada.** O principal suspeito é o checkout: em 16/11, foram 171 cliques para comprar no Meta, mas só 16 carrinhos chegaram à Kiwify.
- **O teste de comprar pelo celular até gerar o Pix ficou pendente.** É a primeira coisa a fazer em qualquer diagnóstico de queda.
- O CTR estava em 11% a 13%, com clique a US$ 0,13. É alto demais. Suspeita: **Audience Network** ou clique de curiosidade. Confira em Detalhamento → Por entrega → Posicionamento.

### 5.2 Família (R$ 47 com VSL): o produto de ticket maior da vez
- Anúncio → `/familia`:
  - VSL de 5 min 32 s no topo, começando sem som e com legenda, com o botão "🔊 Toque para ouvir";
  - **quiz grátis** em que a pessoa digita os nomes e as datas da família e vê o santo de cada um;
  - livro por dentro, caixa do bônus, Natal, garantia, oferta de R$ 47.
- Checkout `GJSYLJP`, com o bump do Calendário.
- **Página de obrigado** = `/oferta-completa`: upsell **"Complete a Biblioteca"** por R$ 37 (Consagração + Rezo + Calendário; separados, custariam R$ 67,80), com 1 clique (ID `hyPTemQ`, que é uma oferta dentro do produto Biblioteca). Depois, a pessoa vai para `/dados-familia`.
- O servidor (v16) **dá o devocionário de bônus** a quem compra a Família. Se a pessoa já tiver o devocionário, não gera de novo.
- **Empate:** cada venda pode custar até uns **R$ 40** (o líquido de R$ 47 depois da taxa).
- **Lógica de escada:** a Família fica na frente, e a Biblioteca entra no upsell. Por isso a recomendação é **pausar o tráfego frio da Biblioteca**, para os dois não disputarem o mesmo público.

### 5.3 Biblioteca (R$ 97 com VSL)
- `/biblioteca`, com VSL de 5 min 49 s no topo.
- Testamos travar a página até o vídeo chegar na oferta: **os cliques para comprar caíram para 2,8%**, e desfizemos. Com a página aberta, **8,5%** clicaram em comprar no primeiro dia (82 visitas).
- **Empate:** uns **R$ 85** por venda.
- **Funil da VSL no primeiro dia** (amostra pequena):
  - 82 abriram a página;
  - 48% viram o vídeo rodar 10 s;
  - **27% ligaram o som**;
  - metade de quem ligou o som saiu antes de 25% (no bloco "tradição", que é lento);
  - quem passou da metade ficou até o fim.
  - Ideia para depois de umas 200 visitas: uma versão de ~4 min, cortando os blocos 02 e 04.

### 5.4 Pós-venda automático (servidor)
- **Lembretes para quem pagou e não preencheu os dados:** 20 min, ~20 h e ~68 h depois da compra. **Problema grave em aberto:** havia **187 compras paradas em `aguardando_dados`** contra 154 entregues. Daí vêm as reclamações de "foi golpe". Proposta já combinada, mas não feita:
  - reescrever o e-mail "Falta só um passo" para começar com "✅ Pagamento confirmado" e explicar que o devocionário é feito com o santo do dia do nascimento;
  - **entrega automática depois de 3 dias** com Nossa Senhora, mais um link para trocar pelo santo certo.
- **Recuperação de vendas** (tabela `recuperacao`): Pix gerado e não pago (60 min), cartão recusado (15 min), carrinho abandonado (90 min). Prioridade: biblioteca > santo > consagracao > livro_familia > enfermo.
  - Status `recuperado` = a pessoa pagou **depois** do e-mail;
  - status `pago` = pagou antes do e-mail sair.
  - O agente de recuperação da própria Kiwify também está ligado (aparece como `src=kiwify_sales_agent`).
- **Sequência da Biblioteca:** e-mails nos dias 1, 4 e 9 depois da primeira entrega, só nos primeiros 30 dias. Com **espera mínima de 2 dias entre ofertas** (correção da v14b, depois que um erro mandou o e-mail 1 e o 2 na mesma hora).
  - **Não manda** para quem pediu reembolso, para quem está em `dados/nao_enviar.txt` nem para quem já tem quase tudo.
  - O e-mail lista **só os livros que faltam**, com a soma real dos preços.
  - Descadastro em `/sair?t=…`.
- **Campanha para a lista de clientes:** `campanha_biblioteca.py` (`contar`, `teste EMAIL`, `enviar 1`). Só para quem comprou produto católico e recebeu. Mande aos poucos, com 300 a 500 no primeiro dia.

---

## 6. O servidor por dentro

**Fluxo:**
1. A Kiwify chama `/webhook/kiwify/<segredo>`.
2. O servidor identifica os SKUs pelo nome do produto.
3. A Biblioteca expande nos 5 SKUs, menos os que a pessoa já tem; a Família ganha o `santo` de bônus.
4. Cria as linhas em `compras` com status `aguardando_dados`.
5. Manda **um único e-mail** com um botão para cada página de dados.
6. A pessoa preenche em `/dados`, `/dados-familia`, `/dados-consagracao` ou `/dados-enfermo`. As páginas falam com `/api/cliente` e `/api/dados`.
7. A compra passa para `na_fila`. O trabalhador gera o texto com a IA (`interpretar.py`) e o PDF (`pdf.py`), e manda o e-mail com o link `/baixar/<token>`. Status final: `enviado`.

**Arquivos principais** (em `/opt/mapadaalma`):
- `servidor.py`: rotas, webhook, fila, e-mails, lembretes, recuperação, ofertas, eventos.
- `interpretar.py`: chamadas à IA e regras dos textos.
- `pdf.py`: layout dos PDFs.
- `santos.py` e `santos_dados.py`: a tabela dos 366 santos (199 do calendário litúrgico do Brasil, 167 do Martirológio Romano).
- `familia_extra.py`, `oracoes_familia.py`, `consagracao.py`, `enfermo.py`: conteúdo de cada produto.

**Versão atual: v16.** Histórico recente:
- **v14:** Biblioteca e sequência de e-mails.
- **v14b:** espera de 2 dias entre ofertas.
- **v14c:** recoloca na fila o que falhou e limita os alertas.
- **v15:** contador próprio de eventos (`/api/evento`) e `vsl_relatorio.py`.
- **v16:** bônus da Família e o nome novo do produto.

**Comandos úteis** (todos na **VPS**, `root@srv2014776`):
```
# saúde e status das compras
curl -s localhost:8010/health
cd /opt/mapadaalma && python3 -c "import sqlite3;c=sqlite3.connect('dados/mapa.db');print(dict(c.execute(\"SELECT status,COUNT(*) FROM compras GROUP BY status\").fetchall()))"

# entregas ao vivo (Ctrl+C para sair)
journalctl -u mapadaalma -f | grep --line-buffered "entregue"

# compras com erro e o motivo
cd /opt/mapadaalma && python3 -c "import sqlite3;c=sqlite3.connect('dados/mapa.db');[print(n,'x',e) for e,n in c.execute(\"SELECT substr(erro,1,160),COUNT(*) FROM compras WHERE status='erro' GROUP BY 1\")]"

# recolocar na fila tudo o que deu erro (ex.: depois de recarregar o crédito da Anthropic)
cd /opt/mapadaalma && python3 -c "import sqlite3;c=sqlite3.connect('dados/mapa.db');n=c.execute(\"UPDATE compras SET status='na_fila',tentativas=0 WHERE status='erro'\").rowcount;c.commit();print(n)"

# gerar o devocionário de uma cliente que mandou a data por e-mail (e-mail, dia, mês, nome)
bash /opt/mapadaalma/preencher_data.sh EMAIL 13 6 "Maria"

# reenviar uma compra que já foi entregue
cd /opt/mapadaalma && curl -s -X POST "http://localhost:8010/admin/reenviar?id=ID&chave=$(grep ^ADMIN_CHAVE= .env | cut -d= -f2)"

# funil das VSLs (contador próprio)
cd /opt/mapadaalma && ./venv/bin/python vsl_relatorio.py            # Biblioteca
cd /opt/mapadaalma && ./venv/bin/python vsl_relatorio.py familia    # Família

# e-mail de desculpas para quem teve a entrega atrasada (só uma vez por pessoa)
cd /opt/mapadaalma && ./venv/bin/python desculpas.py contar | teste EMAIL | enviar
```
Para consultar **uma** cliente, existe um script em Python que lê `clientes` e `compras` por e-mail e mostra o status e o link `/dados?t=<token>`. Rode na VPS e não guarde o resultado.

---

## 7. O site

- **Código-fonte:** os modelos ficam em `build/santo/*.tpl.html`, com um bloco `window.CFG = {...}` no topo que guarda o checkout, o preço, os IDs do upsell, a VSL e o nome da página.
- **Para publicar:**
  1. `python3 build/fazer_santo.py` monta tudo em `santo-site/`;
  2. faça o zip com `zip -qr site-meusantoprotetor.zip . -x '.env'`;
  3. no Cloudflare, abra o projeto e faça um **novo deploy com o zip inteiro**.
- **As páginas:**
  - `index` (quiz A), `b` (página B), `a24` (A a R$ 24,90), `qb` (quiz B);
  - `familia`, `biblioteca`, `consagracao`, `enfermo`;
  - os upsells: `oferta` (Consagração por R$ 27, antiga e fora de uso), `oferta-biblioteca` e `oferta-completa`;
  - as páginas de dados: `dados`, `dados-familia`, `dados-consagracao` e `dados-enfermo`.
- **VSL hospedada no próprio site:**
  - `vsl/biblioteca.mp4` e `vsl/familia.mp4`, em 720×900, com uns 18 MB cada;
  - **o limite do Cloudflare Pages é 25 MB por arquivo**;
  - no `familia.tpl.html`, a VSL é ligada pelo `CFG.VSL_SRC` (se ficar vazio, a página fica sem vídeo);
  - o vídeo não mostra a barra nem a duração, e um toque nele pausa.
- **Eventos:**
  - a função `track()` manda o evento para o pixel **e** para o contador próprio (`conta()` → `https://api.mapadaalma.online/api/evento`, sem dado pessoal);
  - eventos: `Entrou`, `Vsl10s`, `VslSom`, `Vsl25`, `Vsl50`, `Vsl75`, `Vsl95`, `VslOferta`, `Checkout`.

---

## 8. Meta Ads: o que já sabemos
- **Classificação "Religião" (detectada em 17/11):**
  - no Brasil, o pixel está em **configuração básica**: Compra e Finalização de compra **continuam chegando**, mas **eventos personalizados e parâmetros são descartados**. É por isso que existe o contador próprio no servidor;
  - na Europa, os dados são bloqueados.
  - **Não** tente contornar com domínio ou pixel novo.
  - A "lista de permissões" de domínios é opcional. Se for usar, coloque os dois domínios das marcas.
- **Pontos de empate por produto:** devocionário ~R$ 18 por compra, Família ~R$ 40, Biblioteca ~R$ 85. O ROAS que o Meta mostra é sobre o valor **bruto**: para empatar no líquido, ele precisa mostrar uns 1,15.
- **Estrutura que recomendamos:**
  - poucas campanhas e conjuntos com verba de verdade, em vez de várias campanhas pequenas;
  - criativos testados **dentro** do conjunto;
  - desligar o criativo que gastou uns US$ 10 a 15 sem compra;
  - comparar conjuntos pelo custo por compra depois de uns US$ 40;
  - formatos de tipos diferentes (apelativos de curiosidade × produto e preço) em **conjuntos separados**.
- **Criativos campeões do devocionário** (a pessoa participa e é visualmente simples):
  - "Qual destes é o seu santo protetor?" (A/B/C com 3 santinhos);
  - "Pergunte à sua mãe: qual é o santo do dia em que eu nasci? Ela provavelmente não sabe.";
  - os de **vela**: "Desde o dia em que você nasceu, um santo roga a Deus por você. Você sabe quem é ele?" e o vídeo "Acenda 6 velas…".
  - **Formatos novos feitos a partir deles:** raspadinha, enquete dos meses, conversa de chat com a mãe ou no grupo da família, lista escrita à mão da avó, barra de busca, velas acendendo com o nome de cada um.
- O Meta pediu confirmação de identidade por e-mail num dia em que o Outlook estava fora. Lição: na conta do Facebook, usar Gmail e verificação em duas etapas com app autenticador, e ter um segundo administrador real no Gerenciador de Negócios.

---

## 9. Criativos e VSL: como são feitos

**Motor (código em `/home/claude/criativos-santo` no ambiente de trabalho):**
- Cada cena é uma página HTML, fotografada pelo Playwright e montada em vídeo pelo ffmpeg.
- `build_p.py` traz o `el(html, entra, sai, efeito)`, o `cta()`, o `render_video()` e o tema claro. `build_f.py` traz o tema escuro (fundo azul-marinho com raios dourados).
- Fontes: Fraunces, Outfit, Cormorant Garamond e Cinzel. Paleta: azul `#17295A` / `#0B1636` e dourado `#E9CF93` / `#C9A052`.
- Formatos: estático **4:5 (1080×1350)**; vídeo **9:16 (1080×1920)**, de 10 a 15 s, sem áudio (a música vem da biblioteca do Meta) ou com a voz do Jorge e legenda.
- Imagens do produto: as páginas reais dos PDFs, em `santo-site/img/` e `img/prod/`. Os santinhos são os SVG por categoria.
- **Cuidado comum:** a função `el(html, a, b, efeito, classe, estilo)` tem `b` (a saída) como 3º argumento. Esquecer o `None` desloca tudo, e o elemento sai sem posição. Já aconteceu várias vezes.

**Pipeline da VSL (`/home/claude/vsl`):**
1. Roteiro em blocos curtos, cada um com uma função: gancho, tradição, dor e identificação, apresentação, quem somos (com a transparência de "não somos paróquia"), produto, bônus, legado, Natal, presente, preço, como recebe, garantia, chamada e fechamento ("Jesus, Maria e José, a nossa família vos pertence").
   - **Números por extenso** no texto narrado ("quarenta e sete reais"). Na legenda viram algarismos (R$ 47).
2. O Carlos gera **um bloco por vez** na ElevenLabs (voz Jorge, mesmas configurações) e manda os MP3. Antes, ele manda um bloco de teste para conferir o ritmo.
3. O `build_vsl.py` alinha as frases às pausas do áudio (`silencedetect` + programação dinâmica), faz uma cena por trecho com zoom lento, coloca legendas ASS (Fraunces SemiBold) e normaliza o volume.
   - A VSL completa sai em **4:5** para a página.
   - Os **cortes de anúncio** saem em **9:16**: trechos de blocos combinados, cada um com um gancho diferente, de 45 a 75 s, sempre fechando com o preço e a chamada.
4. **Áudios já gravados que podem ser reaproveitados:** blocos 01 a 10 (Biblioteca) e F1 a F7 (Família).
   - Uma VSL nova reaproveita a maior parte e grava só a oferta, o preço e a chamada. A da Família custou ~1.750 créditos.

---

## 10. A dinâmica de trabalho

### O "kit completo"
Sempre que o Carlos pede um **produto novo**, ele quer **tudo de uma vez, pronto para subir**, nesta lista:
1. **Nome** (com o nome exato para a Kiwify, compatível com o reconhecimento do servidor).
2. **Preço** (e as ofertas extras, se houver).
3. **Descrição** para a Kiwify.
4. **Order bumps** (nome, preço acima de R$ 10, título e descrição).
5. **Imagem do produto** (1000×1000) e **banners do checkout** (1200×400 para computador e 1080×540 para celular). Cores do checkout: `#F8F3EE` e `#17295A`.
6. **Páginas:** a de vendas (quiz ou VSL), a de obrigado/upsell e a de dados.
7. **Entrega no servidor:** SKU, reconhecimento do nome, geração, PDF, e-mails e testes. Entregue como **`atualizacao-servidor-N.zip`**, com o comando de instalação.
8. **E-mails** (dados, pronto, lembretes, recuperação).
9. **Criativos:** uns 5 a 10 estáticos e vídeos, apelativos dentro das regras.
10. **Legenda única** para os anúncios.
11. **Passo a passo de como subir** (`COMO-SUBIR.md`): Kiwify → servidor → site → anúncios → testes, **com o terminal indicado em cada comando**.

E entregar como **zips** (site inteiro, atualização do servidor e kit com imagens e guia). Conferir cada coisa antes de entregar: abrir as páginas no tamanho de celular, olhar os quadros dos vídeos e testar o webhook localmente com o `TestClient` do FastAPI.

### Como o Carlos quer ser atendido
- **Sempre apontar o que pode melhorar e discordar quando for o caso.** Não concordar só por concordar. Exemplos do que já foi feito: segurar a ideia de "muitas campanhas com pouca verba", travar a página da VSL com dados, segurar uma VSL para produto de R$ 19, recusar disparo por ferramentas de spam.
- Português informal, direto, com a ação primeiro. Comandos prontos para copiar, **dizendo em qual terminal rodar** (Mac ou VPS).
- **Assumir ROAS ≥ 1** e não pedir o gasto do anúncio.
- **Mudar uma coisa por vez** quando for testar (página **ou** preço **ou** criativo), para saber o que funcionou.
- **Antes de mexer em criativo por causa de queda de vendas, conferir o checkout e o rastreamento.**
- Quando errar, assumir o erro e corrigir na hora. Já aconteceu: o bug do e-mail 2 junto com o 1; o arquivo de lembrete; o produto proposto que já existia.

---

## 11. Pendências e próximos passos (em 18/11)
1. **Teste da compra pelo celular**, até gerar o Pix, nas páginas `/b` e `/familia`. É a principal suspeita da queda do devocionário.
2. **Checklist da Família:**
   - renomear "Livro de Orações da Família" na Kiwify;
   - colocar a página de obrigado `/oferta-completa`;
   - subir o servidor v16 e o site;
   - rodar os criativos (zip `criativos-familia-47`: 10 estáticos, 4 vídeos de formatos novos e 10 cortes da VSL), em 2 conjuntos de ~US$ 15 a 20 por dia, com link `/familia`.
3. **Pausar o tráfego frio da Biblioteca** (agora ela é upsell da Família).
4. **Os 187 compradores sem dados:** reescrever o e-mail e fazer a entrega automática em 3 dias.
5. **Teste do devocionário a R$ 24,90** na página B (uma "B24"), só depois que as vendas normalizarem.
6. **Até 16/12:** trocar os textos com o prazo do Natal. **Depois do Natal**, trocar o ângulo de presente.
7. **Próximo produto sugerido:** "Consagração a Nossa Senhora" com VSL. São 33 dias de preparação para uma festa de Nossa Senhora, com data real: começar em 29/11 para consagrar em 1º/1, ou começar em 31/12 para consagrar em 2/2. O produto já existe (R$ 37).
8. **Mais tarde:** assinatura mensal de oração do dia (receita todo mês).
9. **WhatsApp:** só pelo **Canal** (sem risco) ou com mensagens para clientes que deixaram o número, devagar. **Nada de lista fria nem de truques contra banimento.**
