# Guia do O Santo do Nosso Casamento para o Claude (leia antes de mexer)

Produto do **Meu Santo Protetor**: quiz com a data do casamento → o santo do dia, de graça → livro de orações do casal em PDF por R$ 37 (Kiwify), com 2 bumps e o upsell da Família. As regras do manual do Meu Santo valem aqui: doutrina, anúncios, segurança e LGPD.

## 1. Arquitetura

| Parte | Onde fica | O que faz |
|---|---|---|
| Site | `site/` (HTML estático) no **Cloudflare Pages**, projeto `santo-casamento`, domínio `casamento.meusantoprotetor.online` | Quiz, revelação grátis, oferta, obrigado (upsell e livro pronto), página de dados e privacidade. A configuração fica em **`site/config.js`**. |
| Servidor | **`casamento.py`** (+ `casamento_conteudo.py`, `casamento_pdf.py`, `casamento_fontes/`) dentro do servidor do Meu Santo: VPS, `/opt/mapadaalma`, serviço `mapadaalma`, porta 8010, `https://api.mapadaalma.online` | Guarda os quizzes e as compras (SQLite `dados/mapa.db`, tabelas `casamento_*`), gera o texto com a IA e o PDF, recebe a Kiwify, manda os e-mails, faz a recuperação de vendas e os lembretes. |
| Kiwify | O mesmo webhook do Meu Santo | O `servidor.py` vê "santo do nosso casamento" (ou o nome de um bump) e chama `casamento.evento_kiwify()` **antes** da lógica do Meu Santo. O que não é do casamento no mesmo pedido segue o fluxo normal. |

Não tem Node, Docker, porta nova nem túnel novo. Não crie isso.

## 2. Fluxo

1. **Quiz** (`site/index.html`).
   - Na revelação: `GET /api/casamento/santos?d=DDMM,DDMM,DDMM` (casamento, ela, ele). Usa o `santos.py` da VPS. Se o nome do dia não começa com São/Santo/Santa/Nossa Senhora..., é **festa** (`festa: true`) e a invocação passa a ser "Santa Maria, Mãe de Deus".
   - Ao comprar: `POST /api/casamento/pedido {pedido, origem}`. O servidor valida (`validar_pedido`), grava em `casamento_pedidos` com `ref = ca-<12hex>` e devolve o link da Kiwify com `?sck=<ref>&utm_*`. O site guarda o `ref` no `localStorage`.
   - Se o servidor não responder, o site manda direto para `CFG.CHECKOUT` (sem o `sck`). Nesse caso, depois da compra o e-mail pede os dados.
2. **Kiwify → webhook → `evento_kiwify`.**
   - A linha da compra (`casamento_compras`, uma por `order_id`) é ligada ao quiz pelo `TrackingParameters.sck`.
   - O bump que chega num aviso separado, sem `sck`, usa o quiz da compra mais recente do mesmo e-mail (2 dias). Cada linha gera só os PDFs dos `skus` dela.
   - **Status** (não regride): pendente/recusado 1, pago 2, reembolsado 3.
   - **Fase** (só para quem pagou): `na_fila` → `gerando` → `enviado`; `aguardando_dados` (sem quiz); `erro`; `cancelado` (reembolso antes de gerar).
   - Ao pagar, se a compradora informou o próprio aniversário (modo "nos"), a data vai para `clientes.dados.santo`, se ainda estiver vazia (`CASAMENTO_COMPARTILHAR_DATA=1`). Assim o devocionário de bônus do upsell da Família, ou um devocionário que ela já tinha pago, sai sem formulário.
3. **Trabalhador** (uma thread iniciada no startup):
   - `processar_um()` → `gerar()`, que faz a IA (`textos()`) e os PDFs (`casamento_pdf.gerar_pdf`), e manda `email_entrega()` com o livro anexo e um botão por PDF.
   - Uma falha tenta 3 vezes, volta para a fila a cada 30 min (até 9 tentativas) e só então alerta o admin.
   - A cada minuto também roda `lembretes()` (aguardando dados: ~20 h e ~68 h), `recuperar()` (Pix 60 min, cartão recusado 15 min, carrinho 90 min) e `_refila_erros()`.
   - A cada 6 h, `_limpar_quizzes()` apaga as respostas de quiz sem compra com mais de 60 dias, como promete a política de privacidade.
4. **IA (`textos()`).** Escreve só 6 campos: `carta`, `santo_historia`, `santo_casamento`, `oracao_casal`, `oracao_pessoal` e `intencao`.
   - Cada campo é conferido: tamanho, "Amém." no fim, os dois nomes na oração do casal e o filtro de promessa de resultado (`RE_PROMESSA`). O que vier ruim é trocado pelo `textos_padrao()`.
   - **Se a IA falhar, o livro sai com o texto padrão**, sem atrasar a entrega.
   - `RE_VIOLENCIA` e `RE_CRISE` olham o texto livre e ligam os avisos do 180 e do CVV no PDF.
5. **Obrigado** (`site/obrigado.html`). Mostra o upsell, se houver `UPSELL_ID`, e depois `GET /api/casamento/status?ref=` a cada 4 s até `pronto`, com os botões `GET /api/casamento/baixar/<token>/<n>`.
6. **Dados** (`site/dados.html?t=<token>`). Só para quem comprou sem quiz: `GET/POST /api/casamento/dados`.
7. **Reenviar.** `POST /api/casamento/reenviar {email}` responde sempre igual, para não revelar quem é cliente.

## 3. Onde mexer

| Quero mudar… | Arquivo |
|---|---|
| Perguntas do quiz, textos da página de vendas, FAQ | `site/index.html` (os pedidos do quiz têm que bater com `PEDIDOS` em `casamento.py`) |
| Preço mostrado, checkout de reserva, upsell, pixel, contato | `site/config.js` (o preço que vale é o da Kiwify: mantenha igual) |
| Visual do site | `site/estilo.css` |
| Novena, orações fixas, santos dos casais, 30 dias, Santa Rita | `servidor/casamento_conteudo.py` |
| Layout dos PDFs, capa, quadro, calendário | `servidor/casamento_pdf.py` (`CSS`, `html_livro`, `html_marido`, `html_rita`) |
| Prompt da IA e formato | `casamento.py`: `SISTEMA` e `ESQUEMA`. Se mudar um campo, mude também `textos_padrao()`, `textos()` e o `html_livro()` |
| E-mails | `casamento.py`: `email_entrega`, `email_pedir_dados`, `email_recuperacao` |
| Nomes dos produtos na Kiwify | `.env`: `CASAMENTO_PRODUTO`, `CASAMENTO_BUMP_MARIDO`, `CASAMENTO_BUMP_RITA` (alternativas com `\|`) |
| Criativos | `criativos/estaticos.html` e `criativos/videos.html`. Para gerar de novo: `node criativos/render_estaticos.js` e `node criativos/render_videos.js` |

Depois de mexer no servidor, rode o teste: `python testes/teste_casamento.py`. Ele precisa de `fastapi`, `httpx`, `anthropic` e um Chromium (variável `CASAMENTO_CHROME`); passe `V19_DIR` com a pasta que tem o `folego.py` e o `clube.py` reais. São 45 conferências, e todas têm que passar.

## 4. Configuração no `/opt/mapadaalma/.env`

| Chave | Para quê |
|---|---|
| `CASAMENTO_CHECKOUT` | Código (ou link) do checkout na Kiwify. **Obrigatória.** |
| `CASAMENTO_SITE` | Padrão `https://casamento.meusantoprotetor.online`. Vai no link do e-mail de dados e no CORS. |
| `CASAMENTO_PRODUTO`, `CASAMENTO_BUMP_MARIDO`, `CASAMENTO_BUMP_RITA` | Trechos do nome dos produtos (padrões: `santo do nosso casamento`, `rezando pelo meu marido\|rezando pela minha esposa`, `santa rita pelo casamento`) |
| `CASAMENTO_MODELO` | Padrão `claude-opus-5-5`. Para gastar menos: `claude-sonnet-5-5`. |
| `CASAMENTO_ANTHROPIC_API_KEY` | Opcional. Vazio = usa a `ANTHROPIC_API_KEY` do Meu Santo. |
| `CASAMENTO_PDF_MOTOR` | Opcional: `playwright`, `weasyprint` ou `chromium`. Vazio = tenta os três nessa ordem. `CASAMENTO_CHROME` = caminho do Chromium. |
| `CASAMENTO_RECUPERACAO` | `1` (padrão) = e-mails de Pix pendente, cartão recusado e carrinho abandonado. `0` desliga. |
| `CASAMENTO_COMPARTILHAR_DATA` | `1` (padrão) = guarda o aniversário de quem comprou no cadastro do Meu Santo. |
| `CASAMENTO_CONVITE_FAMILIA`, `CASAMENTO_LINK_FAMILIA` | Caixa "e o santo de cada pessoa da casa?" no e-mail de entrega (padrão: ligada, com o link `<site do Meu Santo>/familia`) |

O remetente dos e-mails é o do Meu Santo (`EMAIL_REMETENTE_SANTO`), que já está verificado na Resend.

## 5. Os 4 ganchos no `servidor.py` (se precisar aplicar num `servidor.py` diferente do v19)

1. **CORS:** acrescentar `os.environ.get("CASAMENTO_SITE", "https://casamento.meusantoprotetor.online")` na tupla `for _u in (CFG["SITE_URL_PROMESSA"], CFG["FOLEGO_SITE"], ...)`.
2. **Rotas:** logo depois de `app.include_router(_folego.router)`:
   ```python
   import casamento as _casamento  # noqa: E402
   app.include_router(_casamento.router)
   ```
3. **Startup:** dentro do `_iniciar()`, `try: _casamento.iniciar()` com `except Exception: log.exception(...)`.
4. **Webhook:** logo depois de `nomes_produtos = _produtos_no_payload(p)`:
   ```python
   if _casamento.eh_casamento(nomes_produtos):
       try:
           _casamento.evento_kiwify(p, status, email, nomes_produtos)
       except Exception:
           log.exception(...); alerta_admin(...); raise HTTPException(500)   # a Kiwify tenta de novo; não duplica
       nomes_produtos = [n for n in nomes_produtos if not _casamento.eh_casamento([n])]
       if not nomes_produtos:
           return {"ok": True}
   ```
   E, no `if status in ("paid", ...)` do Meu Santo, nada muda.

## 6. Comandos úteis (VPS)

```
cd /opt/mapadaalma
./venv/bin/python casamento.py diagnostico      # configuração, tabela de santos, IA e qual gerador de PDF funciona
./venv/bin/python casamento.py status           # vendas, bumps, entregas (IA x texto padrão) e recuperação, em 24 h e 7 dias
./venv/bin/python casamento.py funil 7          # funil da página (contador próprio)
./venv/bin/python casamento.py buscar EMAIL     # compras de uma pessoa, a fase, o erro e os links
./venv/bin/python casamento.py refazer PEDIDO   # gera e manda de novo (PEDIDO = order_id da Kiwify)
./venv/bin/python casamento.py teste EMAIL [ia] # livro de exemplo no seu e-mail
./venv/bin/python casamento.py santo 13 6       # o que a tabela de santos devolve para a data
journalctl -u mapadaalma -n 200 --no-pager | grep casamento
grep casamento dados/logs/servidor.log | tail -50
```
Use `python3`, não o comando `sqlite3`.

## 7. Regras (não negociáveis)

- **Chaves nunca no chat.** Elas ficam só no `.env` da VPS.
- **A VPS é compartilhada:** nunca reinicie o Docker nem a máquina. Reinicie só com `systemctl restart mapadaalma`.
- **Não quebre o Meu Santo:** o código do casamento fica nos arquivos `casamento*`. No `servidor.py`, só os 4 ganchos.
- **Doutrina.** O santo intercede e quem concede é Deus. Nada de promessa ("o casamento vai mudar"), de superstição ou de fato inventado sobre santo. Versículo só com a referência. Nunca dizer nem insinuar que é padre. "Não somos paróquia" fica no livro e no site.
- **Violência.** Rezar pelo casamento nunca significa aceitar violência. O aviso do 180 (e o Catecismo, n. 2383) não sai do livro, da novena de Santa Rita nem dos 30 dias.
- **Anúncios.** Sem atributo pessoal, sem escassez falsa, sem depoimento inventado, sem "de/por" falso. Prazo só se for verdadeiro.
- **LGPD.** Nada de e-mail, telefone ou nome de cliente em documento, print ou relatório. Só números agregados.
