# Guia da Novena pelos Filhos para o Claude (leia antes de mexer)

Produto do **Meu Santo Protetor**: quiz com o nome e o aniversário de cada filho ou neto → o santo do dia de cada um, de graça → **novena em vídeo** (9 vídeos narrados) + livro em PDF por R$ 87 (Kiwify), com 2 bumps e o upsell "Um Livro para Cada Filho". As regras do manual do Meu Santo valem aqui: doutrina, anúncios, segurança e LGPD. A skill `produto-digital` tem o contexto completo.

## 1. Arquitetura

| Parte | Onde fica | O que faz |
|---|---|---|
| Site | `filhos/site/` (HTML estático) no **Cloudflare Pages**, projeto `santo-filhos`, domínio `filhos.meusantoprotetor.online` | Quiz, revelação grátis, oferta com VSL, obrigado (upsell e novena pronta), **página da novena** (`novena.html`), dados e privacidade. Configuração em **`filhos/site/config.js`**, inclusive os links dos vídeos. |
| Servidor | **`servidor/filhos.py`** (+ `filhos_conteudo.py`, `filhos_pdf.py`, `filhos_fontes/`) dentro do servidor do Meu Santo: VPS, `/opt/mapadaalma`, serviço `mapadaalma`, porta 8010, `https://api.mapadaalma.online` | Quizzes e compras (SQLite `dados/mapa.db`, tabelas `filhos_*`), IA com texto de reserva, 4 tipos de PDF, página da novena (API), e-mails (entrega, 8 lembretes diários, dados, recuperação). |
| Kiwify | O mesmo webhook do Meu Santo | O `servidor.py` vê "novena pelos filhos" (ou um bump, ou o upsell) e chama `filhos.evento_kiwify()` depois do gancho do casamento e **antes** da lógica do Meu Santo. O resto do pedido segue o fluxo normal. |
| Vídeos | Arquivos `videos/*.mp4` dentro do site (≤ 25 MB cada) ou YouTube não listado (`"youtube:ID"` no `config.js`) | Feitos pelo Carlos a partir de `filhos/roteiros/`. O servidor não conhece os vídeos: só o site. |

Não tem Node, Docker, porta nova nem túnel novo. Não crie isso.

## 2. Fluxo

1. **Quiz** (`site/index.html`).
   - Revelação: `GET /api/filhos/santos?d=DDMM,DDMM,...` (até 6). Usa o `santos.py` da VPS. Nome que não começa com São/Santo/Santa/Nossa Senhora... é **festa** (`festa: true`) e a invocação vira "Santa Maria, Mãe de Deus".
   - Compra: `POST /api/filhos/pedido {pedido, origem}`. `validar_pedido` exige o papel (`mae`, `avo_f`, `pai`, `avo_m`), o nome de quem reza e de 1 a 6 pessoas (`nome`, `rel` filho/filha/neto/neta, `dia`, `mes`, `ano` opcional, `partiu`). Grava em `filhos_pedidos` com `ref = fi-<12hex>` e devolve o link da Kiwify com `?sck=<ref>&utm_*`.
   - Se o servidor não responder, o site manda para `CFG.CHECKOUT` sem `sck`. Depois da compra, o e-mail pede os dados.
2. **Kiwify → webhook → `evento_kiwify`.** Uma linha em `filhos_compras` por `order_id`, ligada ao quiz pelo `sck`. Bump ou upsell que chega em aviso separado e sem `sck` usa o quiz da compra paga mais recente do mesmo e-mail (2 dias). Cada linha gera só os PDFs dos `skus` dela. Status não regride (pendente/recusado 1, pago 2, reembolsado 3). Se um bump entra numa linha já gerada (ou durante a geração), a linha volta para a fila e sai de novo com tudo.
3. **Trabalhador** (thread do startup): `processar_um()` → `gerar()` → `email_entrega()`. Falha tenta 3 vezes, volta para a fila a cada 30 min (até 9) e só então alerta o admin. A cada minuto: `lembretes()` (sem dados: ~20 h e ~68 h), `recuperar()` (Pix 60 min, cartão 15 min, carrinho 90 min), `_refila_erros()` e **`lembretes_novena()`** (um e-mail por dia, do 2º ao 9º, a partir de `FILHOS_HORA_DIA`, sem mandar os dias atrasados; para em reembolso ou no link `/api/filhos/sair`). A cada 6 h apaga quizzes sem compra com mais de 60 dias.
4. **IA (`textos()`).** Escreve só a `carta` (2 parágrafos), a lista `filhos` (`santo_texto` e `oracao` de cada pessoa, na mesma ordem) e a `intencao`. Cada campo é conferido (tamanho, "Amém.", o nome na oração, `RE_PROMESSA`); a ordem trocada é corrigida pelo nome; o que vier ruim vira o `textos_padrao()`. **Se a IA falhar, o livro sai igual.** `textos_do_ref()` guarda o resultado em `filhos_textos` e reaproveita na novena, nos bumps e no upsell. `RE_CRISE`, `RE_VIOLENCIA` e `RE_VICIO` ligam os avisos de ajuda.
5. **Obrigado** (`site/obrigado.html`): upsell (se houver `UPSELL_ID`; o botão do Pix leva `?sck=<ref>`), depois `GET /api/filhos/status?ref=` a cada 4 s até `pronto`, com o link da página da novena e os PDFs.
6. **Página da novena** (`site/novena.html?t=<token>`): `GET /api/filhos/area?t=` junta todas as linhas pagas do mesmo quiz e devolve os nomes, os santos, os 9 dias já preenchidos, a consagração, as bênçãos e o terço (se comprados) e os links. Os dias rezados ficam só no `localStorage` do aparelho.
7. **Dados** (`site/dados.html?t=<token>`): só para quem comprou sem quiz.

## 3. Onde mexer

| Quero mudar… | Arquivo |
|---|---|
| Perguntas do quiz, oferta, FAQ | `site/index.html` (os pedidos do quiz têm que bater com `PEDIDOS` em `filhos.py`; a lista também está no `dados.html`) |
| Editor de filhos e netos (quiz e dados) | `site/comum.js` (`FIL.Editor`) |
| Preço mostrado, checkout de reserva, VSL, vídeos, upsell, pixel | `site/config.js` (o preço que vale é o da Kiwify: mantenha igual) |
| Os 9 dias, Santa Mônica, consagração, bênção, situações, bênçãos, terço, livro de cada filho | `servidor/filhos_conteudo.py`. **Os 9 dias são os mesmos dos vídeos** (`filhos/roteiros/02-NOVENA-9-VIDEOS.md`): mudou um, mude o outro. Os títulos dos dias também estão no `index.html` e no `criativos/posters.html` |
| Layout dos PDFs | `servidor/filhos_pdf.py` (`CSS`, `html_novena`, `html_bencaos`, `html_terco`, `html_livro_filho`) |
| Concordância (filho/filha, singular/plural, "dos meus filhos") | `filhos_pdf.contexto()`: os marcadores estão descritos no topo de `filhos_conteudo.py` |
| Prompt da IA e formato | `filhos.py`: `SISTEMA` e `ESQUEMA`. Se mudar um campo, mude também `textos_padrao()`, `textos()` e os `html_*` |
| E-mails | `filhos.py`: `email_entrega`, `email_dia`, `email_pedir_dados`, `email_recuperacao` |
| Nomes dos produtos na Kiwify | `.env`: `FILHOS_PRODUTO`, `FILHOS_BUMP_TERCO`, `FILHOS_BUMP_BENCAOS`, `FILHOS_UPSELL` (alternativas com `\|`) |
| Criativos e capas dos vídeos | `filhos/criativos/`: `node filhos/criativos/render_estaticos.js posters.html` (capas em `site/img/`), `... estaticos.html` (kit) e `node filhos/criativos/render_videos.js` |

Depois de mexer no servidor, rode o teste: `python testes/teste_filhos.py` (60 conferências; precisa de `fastapi`, `httpx`, `anthropic` e um Chromium em `FILHOS_CHROME`, ou rode com `FILHOS_PDF_MOTOR=weasyprint`). Rode também o `testes/teste_casamento.py`, porque o `servidor.py` é o mesmo.

## 4. Configuração no `/opt/mapadaalma/.env`

| Chave | Para quê |
|---|---|
| `FILHOS_CHECKOUT` | Código (ou link) do checkout na Kiwify. **Obrigatória.** |
| `FILHOS_SITE` | Padrão `https://filhos.meusantoprotetor.online`. Vai nos links e no CORS. |
| `FILHOS_PRODUTO`, `FILHOS_BUMP_TERCO`, `FILHOS_BUMP_BENCAOS`, `FILHOS_UPSELL` | Trechos do nome (padrões: `novena pelos filhos`, `terco pelos filhos`, `bencaos para mandar`, `livro para cada filho`) |
| `FILHOS_MODELO` | Padrão `claude-opus-5-5`. Para gastar menos: `claude-sonnet-5-5`. |
| `FILHOS_ANTHROPIC_API_KEY` | Opcional. Vazio = usa a `ANTHROPIC_API_KEY` do Meu Santo. |
| `FILHOS_PDF_MOTOR`, `FILHOS_CHROME` | Opcional: `playwright`, `weasyprint` ou `chromium`, e o caminho do Chromium. |
| `FILHOS_EMAIL_DIAS` | `1` (padrão) = lembretes do 2º ao 9º dia. `0` desliga. |
| `FILHOS_HORA_DIA` | Hora a partir da qual sai o lembrete do dia (padrão `7`; nunca depois das 21 h). |
| `FILHOS_CONVITE_CONSAGRACAO`, `FILHOS_LINK_CONSAGRACAO` | Caixa da Consagração a Jesus por Maria no e-mail do 9º dia (padrão: ligada, `<site do Meu Santo>/consagracao`) |
| `FILHOS_RECUPERACAO` | `1` (padrão) = Pix pendente, cartão recusado e carrinho abandonado. |

O remetente é o do Meu Santo (`EMAIL_REMETENTE_SANTO`).

## 5. Os 4 ganchos no `servidor.py` (se precisar aplicar num `servidor.py` diferente)

1. **CORS:** acrescentar `os.environ.get("FILHOS_SITE", "https://filhos.meusantoprotetor.online")` na tupla `for _u in (...)`.
2. **Rotas:** logo depois de `app.include_router(_casamento.router)`:
   ```python
   try:
       import filhos as _filhos  # noqa: E402
       app.include_router(_filhos.router)
   except Exception:
       _filhos = None
       log.exception("filhos: módulo não carregou (as vendas da Novena pelos Filhos não serão entregues)")
   ```
3. **Startup:** dentro do `_iniciar()`, `if _filhos: _filhos.iniciar()` num `try/except`.
4. **Webhook:** logo depois do bloco do casamento:
   ```python
   if _filhos and _filhos.eh_filhos(nomes_produtos):
       try:
           _filhos.evento_kiwify(p, status, email, nomes_produtos)
       except Exception:
           log.exception(...); alerta_admin(...); raise HTTPException(500)   # a Kiwify tenta de novo; não duplica
       nomes_produtos = [n for n in nomes_produtos if not _filhos.eh_filhos([n])]
       if not nomes_produtos:
           return {"ok": True}
   ```

## 6. Comandos úteis (VPS)

```
cd /opt/mapadaalma
./venv/bin/python filhos.py diagnostico      # configuração, nomes que colidem, tabela de santos, IA e gerador de PDF
./venv/bin/python filhos.py status           # vendas, bumps, upsell, IA x texto padrão, lembretes e recuperação (24 h e 7 dias)
./venv/bin/python filhos.py funil 7          # funil da página, da VSL, do upsell e do uso da novena
./venv/bin/python filhos.py buscar EMAIL     # compras de uma pessoa, a fase, o erro e o link da página da novena
./venv/bin/python filhos.py refazer PEDIDO   # gera e manda de novo (PEDIDO = order_id da Kiwify)
./venv/bin/python filhos.py teste EMAIL [ia] # novena de exemplo (com bumps e upsell) no seu e-mail
./venv/bin/python filhos.py santo 13 6       # o que a tabela de santos devolve para a data
grep filhos dados/logs/servidor.log | tail -50
```
Use `python3`, não o comando `sqlite3`.

## 7. Regras (não negociáveis)

- **Chaves nunca no chat.** Elas ficam só no `.env` da VPS.
- **A VPS é compartilhada:** nunca reinicie o Docker nem a máquina. Reinicie só com `systemctl restart mapadaalma`.
- **Não quebre o Meu Santo nem o casamento:** o código da novena fica nos arquivos `filhos*`. No `servidor.py`, só os 4 ganchos.
- **Doutrina.** O santo intercede e quem concede é Deus. Nada de promessa ("o seu filho vai voltar", "vai largar o vício"), superstição ou fato inventado sobre santo. Versículo só com a referência. O narrador e o texto nunca dizem nem insinuam ser padre. "Não somos paróquia" fica no livro, no site e na VSL.
- **Temas sensíveis.** Vício, depressão e doença: rezar **e** procurar ajuda (CVV 188, CAPS, AA, NA, Al-Anon, Nar-Anon, Amor-Exigente, Disque 100). Filho que faleceu: oração de descanso eterno, nunca de proteção ou futuro.
- **Anúncios.** Sem atributo pessoal, sem escassez falsa, sem depoimento inventado, sem "de/por" falso. Prazo só se for verdadeiro (tabela no `ESTRATEGIA.md`).
- **LGPD.** Nada de e-mail, telefone ou nome de cliente em documento, print ou relatório. Só números agregados.
