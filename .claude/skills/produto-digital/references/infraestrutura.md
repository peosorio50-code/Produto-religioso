# Infraestrutura (a mesma para todas as marcas)

| Peça | Onde |
|---|---|
| **Servidor** | FastAPI + SQLite. Serviço `mapadaalma` (systemd), porta 8010, VPS `root@srv2014776` (2.25.252.204), pasta `/opt/mapadaalma`, banco `dados/mapa.db` |
| **API pública** | `https://api.mapadaalma.online` (Cloudflare Tunnel → localhost:8010) |
| **Sites** | Estáticos no Cloudflare Pages, **um projeto por produto** (o deploy substitui o projeto inteiro), num subdomínio ou domínio da marca |
| **Checkout** | Kiwify. Um webhook só para tudo (`/webhook/kiwify/<segredo>`). O servidor separa os produtos pelo trecho do nome (`PRODUTO_*` no CFG, ou `os.environ` no módulo novo). `KIWIFY_TOKEN` aceita vários tokens separados por vírgula |
| **E-mail** | Resend, com um remetente verificado por marca |
| **IA** | API da Anthropic, chave no `.env`. Cada módulo pode ter `<PRODUTO>_MODELO` e `<PRODUTO>_ANTHROPIC_API_KEY`. Deixe a recarga automática do crédito ligada (lição de 10 a 12/11) |

## Ganchos de um módulo novo no `servidor.py`
1. **CORS:** acrescentar o site novo na tupla `for _u in (...)`.
2. **Rotas:** `import produto as _produto` + `app.include_router(_produto.router)`, logo depois dos outros.
3. **Startup:** `_produto.iniciar()` dentro de `_iniciar()`, num `try/except` (cria as tabelas e liga o trabalhador).
4. **Webhook:** logo depois de `nomes_produtos = _produtos_no_payload(p)`, se `_produto.eh_produto(nomes)`, chama `evento_kiwify(...)`. Se der erro, `raise HTTPException(500)` para a Kiwify tentar de novo, então o evento precisa ser seguro contra repetição. Depois, tira os nomes do produto e segue o fluxo normal com o resto.

## Instalação padrão de uma atualização
**Mac:**
```
scp -o ServerAliveInterval=20 atualizacao-servidor-N.zip root@2.25.252.204:/root/
```
**VPS:**
```
cd /opt/mapadaalma && md5sum servidor.py && cp servidor.py /root/servidor-antes-N.py && unzip -o /root/atualizacao-servidor-N.zip -d /opt/mapadaalma && systemctl restart mapadaalma && sleep 4 && curl -s localhost:8010/health
```
- O `md5sum` precisa bater com o `servidor.py` em que o pacote foi montado. Se não bater, aplique só os ganchos.
- Rode `chown mapa:mapa` nos arquivos novos, se o serviço rodar como `mapa`.
- A VPS não tem `sqlite3`: use `python3`.

## Teste local antes de entregar
Monte uma cópia do servidor numa pasta temporária: o `servidor.py` real, os módulos que ele importa (`folego.py`, `clube.py`), um `santos.py` de mentira se precisar, `MOCK_IA=1` e sem `RESEND_API_KEY` (os e-mails vão para `dados/emails_teste`). Depois, simule a Kiwify com o `TestClient`. O modelo está em `templates/servidor/teste_casamento.py`.
