"""Mapa da Alma - servidor de entrega.

Rotas:
  POST /webhook/kiwify/{SEGREDO}   venda/reembolso vindos da Kiwify
  GET  /api/cidades?q=rec          autocomplete de cidades
  GET  /api/cliente?t=TOKEN        dados para pré-preencher o formulário
  POST /api/dados                  formulário pós-compra (dados de nascimento)
  GET  /api/acompanhar?a=TOKEN     andamento dos PDFs depois do formulário (botão de baixar na página)
  GET  /baixar/{token}             download do PDF
  GET  /admin?chave=...            últimas compras (para você acompanhar)
  POST /admin/reenviar?chave=...&id=N   reprocessa uma entrega
  GET  /health
"""
import base64, datetime as dt, hashlib, hmac, json, logging, os, pathlib, re, secrets, sqlite3, threading, time, traceback

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

BASE = pathlib.Path(__file__).parent


# ------------------------------------------------------------------ config
def _carregar_env():
    f = BASE / ".env"
    if f.exists():
        for linha in f.read_text().splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_carregar_env()
CFG = {k: os.environ.get(k, d) for k, d in {
    "MARCA": "Mapa da Alma",
    "SITE_URL": "https://mapadaalma.online",          # onde fica a LP e a página /dados
    "API_URL": "https://api.mapadaalma.online",       # este servidor
    "WEBHOOK_SEGREDO": "",                            # trecho secreto da URL do webhook
    "KIWIFY_TOKEN": "",                               # token do webhook na Kiwify (confere a assinatura)
    "RESEND_API_KEY": "",
    "EMAIL_REMETENTE": "Mapa da Alma <contato@mapadaalma.online>",
    "EMAIL_RESPOSTA": "",                             # e-mail para respostas dos clientes (opcional)
    "ADMIN_EMAIL": "",                                # recebe alertas de erro
    "ADMIN_CHAVE": "",                                # senha da rota /admin
    "PRODUTO_NATAL": "mapa astral",                   # trecho do nome do produto na Kiwify
    "PRODUTO_ANO": "2027",
    "PRODUTO_CASAL": "compatibilidade",
    "PRODUTO_NUMERO": "numerologia",
    "PRODUTO_DEUSA": "deusas",
    "PRODUTO_RITUAL": "ritual",
    "PRODUTO_TARO": "taro da alma",
    "PRODUTO_TARO_AMOR": "taro do amor",
    "PRODUTO_TARO_ANO": "taro de 2027",
    # ---- marca "Meu Santo Protetor" (domínio próprio). Vazio = usa o do Mapa da Alma.
    "MARCA_SANTO": "Meu Santo Protetor",
    "SITE_URL_SANTO": "",                             # ex.: https://meusantoprotetor.com.br
    "API_URL_SANTO": "",                              # ex.: https://api.meusantoprotetor.com.br (links de download)
    "EMAIL_REMETENTE_SANTO": "",                      # ex.: Meu Santo Protetor <contato@meusantoprotetor.com.br>
    "PRODUTO_SANTO": "devocionario",
    "PRODUTO_SANTO_FAMILIA": "protetores da familia",
    "PRODUTO_SANTO_CAL": "calendario de fe",
    "PRODUTO_FOLEGO": "folego",                       # Fôlego (folegofinanceiro.shop): produto de outro nicho, com rotas próprias (folego.py)
    "FOLEGO_SITE": "https://folegofinanceiro.shop",
    "FOLEGO_CHECKOUT": "",                            # código do checkout do Fôlego (o trecho depois de pay.kiwify.com.br/)
    "FOLEGO_REMETENTE": "",                           # ex.: Fôlego <plano@folegofinanceiro.shop> (domínio verificado na Resend); vazio = sem e-mail
    "FOLEGO_CONTATO": "",                             # e-mail de atendimento do Fôlego (vai como "responder para")
    "FOLEGO_MODELO": "",                              # vazio = claude-opus-5-5
    "FOLEGO_ANTHROPIC_API_KEY": "",                   # chave só do Fôlego (vazio = usa a ANTHROPIC_API_KEY do Meu Santo)
    "PRODUTO_CLUBE": "terco diario",                 # assinatura: Clube Terço Diário
    "CLUBE_HORA": "6",                                # hora do envio diário do clube
    "CLUBE_PAGINA": "",                               # página de vendas do clube (vazio = <site>/clube)
    "CLUBE_CONVITE": "1",                             # 1 = convite do clube no e-mail de entrega do devocionário
    "VAPID_PRIVADA": "",                              # chaves da notificação do clube (crie com: python clube.py vapid)
    "VAPID_PUBLICA": "",
    "PRODUTO_SANTO_URGENTE": "causas urgentes",       # bump: Novena das Causas Urgentes (Santo Expedito e Santa Rita)
    "PRODUTO_SANTO_NOITE": "dormir em paz",           # bump: Orações para Dormir em Paz (30 noites)
    "PRODUTO_CONSAGRACAO": "consagracao",
    "PRODUTO_LIVRO_FAMILIA": "livro de oracoes|santos protetores da minha familia|santos protetores da sua familia|santo protetor de cada um",
    "FAMILIA_BONUS_SANTO": "1",                       # quem compra Os Santos Protetores da Família ganha o próprio devocionário de bônus
    "PRODUTO_CASA": "eu e a minha casa|proposito de 21 dias",  # Eu e a Minha Casa (evangélico, substitui o Meu Versículo no mesmo produto da Kiwify)
    "PRODUTO_PROMESSA": "meu versiculo|minha promessa",              # Meu Versículo para 2027 (evangélico); sem acento, o servidor ignora acentos
    "PRODUTO_PROMESSA_FILHOS": "orando pelos meus filhos",   # bump: 31 Dias Orando pelos Meus Filhos
    "PRODUTO_PROMESSA_JEJUM": "jejum de daniel",             # bump: Jejum de Daniel - 21 Dias
    "MARCA_PROMESSA": "Eu e a Minha Casa",
    "SITE_URL_PROMESSA": "https://meuversiculo.online",
    "EMAIL_REMETENTE_PROMESSA": "",                    # ex.: Meu Versículo <contato@meuversiculo.online> (domínio verificado na Resend)
    "CHECKOUT_PROMESSA": "https://pay.kiwify.com.br/lO8liOg",
    "PRODUTO_ENFERMO": "rezo por voce",                # Rezo por Você (orações por quem está doente)
    "PRODUTO_ENFERMO_SANTO": "santo protetor de quem", # bump: Santo Protetor de Quem Eu Amo
    "PRODUTO_ENFERMO_CARTOES": "cartoes de fe",        # bump: Cartões de Fé (30 imagens)
    "LEMBRETE_MINUTOS": "20",
    # ---- recuperação de vendas (Pix não pago, cartão recusado, carrinho abandonado): 1 e-mail, só para o Meu Santo Protetor
    "RECUPERACAO": "1",                               # 0 = desliga
    "RECUP_PIX_MIN": "60", "RECUP_RECUSADO_MIN": "15", "RECUP_CARRINHO_MIN": "90",
    "CHECKOUT_SANTO": "https://pay.kiwify.com.br/D68zu9g",
    "CHECKOUT_CONSAGRACAO": "https://pay.kiwify.com.br/ZdbeE6m",
    "CHECKOUT_LIVRO_FAMILIA": "https://pay.kiwify.com.br/GJSYLJP",
    "PRODUTO_BIBLIOTECA": "biblioteca",               # Biblioteca da Família Católica: libera os 5 produtos do Meu Santo Protetor
    "CHECKOUT_BIBLIOTECA": "",                        # oferta pública (R$ 97)
    "CHECKOUT_BIBLIOTECA_CLIENTE": "",                # oferta para quem já é cliente (R$ 77), usada nos e-mails automáticos
    "OFERTA_BIBLIOTECA": "1",                         # 1 = manda a sequência de e-mails da Biblioteca para quem comprou outro produto; 0 = desliga
    "PRECO_BIBLIOTECA_CLIENTE": "77",
    "CHECKOUT_ENFERMO": "https://pay.kiwify.com.br/fjiM4ZV",
    "SUPORTE_SEGREDO": "",                            # trecho secreto da URL /email/entrada/<segredo> (Email Worker do Cloudflare)
    "SUPORTE_IA": "1",                                # 1 = a IA responde os e-mails das clientes; 0 = só registra e avisa o admin
    "SUPORTE_MAX_DIA": "3",                           # no máximo N respostas automáticas por pessoa em 24h
    "SUPORTE_COPIA": "1",                             # 1 = o admin recebe cópia oculta de cada resposta da IA (bom nos primeiros dias)
    "QUIZ_AUTO": "1",                                 # 1 = usa a data do quiz (vem no checkout em s1) para entregar sem pedir os dados
    "MOCK_IA": "0",                                   # 1 = usa textos de exemplo (só para teste)
}.items()}

DADOS = BASE / "dados"; PDFS = DADOS / "pdfs"; LOGS = DADOS / "logs"; EMAILS = DADOS / "emails_teste"
for p in (DADOS, PDFS, LOGS, EMAILS):
    p.mkdir(exist_ok=True)
log = logging.getLogger("mapa")
log.setLevel(logging.INFO)
if not log.handlers:
    _h = logging.FileHandler(LOGS / "servidor.log", encoding="utf-8")
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(_h)
NOMES_PRODUTO = {"natal": "Mapa Astral Completo", "ano": "Seu 2027 nos Astros", "casal": "Compatibilidade Amorosa",
                 "numero": "Numerologia Completa", "deusa": "Mapa das 7 Deusas", "ritual": "Ritual de 21 Dias",
                 "taro": "Leitura de Tarô da Alma", "taro_amor": "Tarô do Amor", "taro_ano": "Tarô de 2027",
                 "santo": "Devocionário do Meu Santo Protetor", "santo_familia": "Santos Protetores da Família", "santo_cal": "Calendário de Fé 2027",
                 "santo_urgente": "Novena das Causas Urgentes", "santo_noite": "Orações para Dormir em Paz",
                 "consagracao": "Consagração a Jesus por Maria", "livro_familia": "Os Santos Protetores da Família",
                 "enfermo": "Rezo por Você", "enfermo_santo": "Santo Protetor de Quem Eu Amo", "enfermo_cartoes": "Cartões de Fé"}
SKUS_SANTO = {"biblioteca", "santo", "santo_familia", "santo_cal", "santo_urgente", "santo_noite", "consagracao", "livro_familia", "enfermo", "enfermo_santo", "enfermo_cartoes"}
SKUS_ENFERMO = {"enfermo", "enfermo_santo", "enfermo_cartoes"}
SKUS_PROMESSA = {"casa", "promessa", "promessa_filhos", "promessa_jejum"}  # marca evangélica separada
NOMES_PRODUTO.update({"biblioteca": "Biblioteca da Família Católica"})
NOMES_PRODUTO.update({"casa": "Eu e a Minha Casa", "promessa": "Meu Versículo para 2027", "promessa_filhos": "31 Dias Orando pelos Meus Filhos", "promessa_jejum": "Jejum de Daniel"})  # usam a página /dados-enfermo
SKUS_DEVOC = {"santo", "santo_familia", "santo_cal", "santo_urgente", "santo_noite"}
BIBLIOTECA = ("santo", "livro_familia", "consagracao", "enfermo", "santo_cal")   # o que a Biblioteca libera  # os que usam a página /dados (dia e mês de nascimento)


def _marca(sku=None):
    """Identidade (nome, site, links, remetente, cores) do produto: Mapa da Alma ou Meu Santo Protetor."""
    if sku in SKUS_PROMESSA:
        rem = CFG["EMAIL_REMETENTE_PROMESSA"] or f'{CFG["MARCA_PROMESSA"]} <{CFG["EMAIL_REMETENTE"].split("<")[-1].rstrip(">").strip()}>'
        return {"marca": CFG["MARCA_PROMESSA"], "site": CFG["SITE_URL_PROMESSA"].rstrip("/"), "api": (CFG["API_URL_SANTO"] or CFG["API_URL"]).rstrip("/"),
                "remetente": rem, "fundo": "#f6e6c8", "rodape": "Devocional cristão para a leitura e a oração pessoal. Dúvidas? É só responder este e-mail.", "simbolo": "✝"}
    if sku in SKUS_SANTO:
        rem = CFG["EMAIL_REMETENTE_SANTO"] or f'{CFG["MARCA_SANTO"]} <{CFG["EMAIL_REMETENTE"].split("<")[-1].rstrip(">").strip()}>'
        return {"marca": CFG["MARCA_SANTO"], "site": (CFG["SITE_URL_SANTO"] or CFG["SITE_URL"]).rstrip("/"),
                "api": (CFG["API_URL_SANTO"] or CFG["API_URL"]).rstrip("/"), "remetente": rem, "fundo": "#13224a",
                "rodape": "Material devocional católico para a oração pessoal. Dúvidas? É só responder este e-mail.", "simbolo": "✝"}
    return {"marca": CFG["MARCA"], "site": CFG["SITE_URL"].rstrip("/"), "api": CFG["API_URL"].rstrip("/"), "remetente": CFG["EMAIL_REMETENTE"],
            "fundo": "#0f0b26", "rodape": "Conteúdo de autoconhecimento e entretenimento. Dúvidas? É só responder este e-mail.", "simbolo": "✦"}


# ------------------------------------------------------------------ banco
_lock = threading.Lock()


def db():
    c = sqlite3.connect(DADOS / "mapa.db", check_same_thread=False, timeout=30)
    c.row_factory = sqlite3.Row
    return c


with db() as c:
    c.executescript("""
    CREATE TABLE IF NOT EXISTS clientes(email TEXT PRIMARY KEY, nome TEXT, token TEXT UNIQUE, dados TEXT, criado TEXT, atualizado TEXT);
    CREATE TABLE IF NOT EXISTS compras(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, sku TEXT, pedido TEXT, status TEXT,
        arquivo TEXT, baixar TEXT, tentativas INTEGER DEFAULT 0, erro TEXT, lembrado INTEGER DEFAULT 0, custo TEXT,
        criado TEXT, atualizado TEXT, UNIQUE(email, sku, pedido));
    CREATE TABLE IF NOT EXISTS acompanhamento(token TEXT PRIMARY KEY, email TEXT, desde TEXT);
    CREATE TABLE IF NOT EXISTS ofertas(email TEXT, campanha TEXT, vez INTEGER, enviado TEXT, PRIMARY KEY(email, campanha, vez));
    CREATE TABLE IF NOT EXISTS eventos(sessao TEXT, evento TEXT, pagina TEXT, src TEXT, quando TEXT, PRIMARY KEY(sessao, evento, pagina));
    CREATE TABLE IF NOT EXISTS quiz(id TEXT PRIMARY KEY, dados TEXT, criado TEXT);
    CREATE TABLE IF NOT EXISTS suporte(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, assunto TEXT, texto TEXT, categoria TEXT,
        acao TEXT, resposta TEXT, msgid TEXT, criado TEXT);
    CREATE TABLE IF NOT EXISTS recuperacao(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, nome TEXT, tipo TEXT, sku TEXT,
        pedido TEXT, link TEXT, status TEXT, criado TEXT, enviado TEXT);
    """)


agora = lambda: dt.datetime.now().isoformat(timespec="seconds")


def cliente(email, nome=None):
    email = email.strip().lower()
    with _lock, db() as c:
        r = c.execute("SELECT * FROM clientes WHERE email=?", (email,)).fetchone()
        if not r:
            c.execute("INSERT INTO clientes(email,nome,token,criado,atualizado) VALUES(?,?,?,?,?)",
                      (email, nome, secrets.token_urlsafe(16), agora(), agora()))
            r = c.execute("SELECT * FROM clientes WHERE email=?", (email,)).fetchone()
        elif nome and not r["nome"]:
            c.execute("UPDATE clientes SET nome=? WHERE email=?", (nome, email))
        return dict(r)


def compras_de(email):
    with db() as c:
        return [dict(r) for r in c.execute("SELECT * FROM compras WHERE email=? ORDER BY id", (email,))]


def dados_completos(dados, sku):
    if not dados:
        return False
    if sku == "casa":
        return bool((dados.get("promessa") or {}).get("pessoas"))
    if sku == "promessa":
        return bool((dados.get("promessa") or {}).get("dia"))
    if sku == "promessa_jejum":
        return bool((dados.get("promessa") or {}).get("nome"))
    if sku == "promessa_filhos":
        return bool((dados.get("promessa") or {}).get("filhos"))
    if sku == "numero":
        return bool(dados.get("num"))
    if sku in ("deusa", "ritual"):
        return bool(dados.get("deusas"))
    if sku in ("taro", "taro_amor", "taro_ano"):
        return bool(dados.get("taro"))
    if sku in ("santo", "santo_cal", "santo_urgente", "santo_noite"):
        return bool(dados.get("santo"))
    if sku == "santo_familia":
        return bool(dados.get("santo")) and bool((dados.get("santo_familia") or {}).get("pessoas"))
    if sku == "consagracao":  # no upsell, o nome e a intenção já vêm do devocionário
        return bool(dados.get("consagracao") or dados.get("santo"))
    if sku == "livro_familia":
        return bool((dados.get("livro_familia") or {}).get("pessoas"))
    if sku in ("enfermo", "enfermo_cartoes"):
        return bool(dados.get("enfermo"))
    if sku == "enfermo_santo":
        return bool((dados.get("enfermo") or {}).get("dia"))
    if not dados.get("p1"):
        return False
    return sku != "casal" or bool(dados.get("p2"))


def liberar_fila(email):
    """Coloca na fila as compras pagas que já têm os dados necessários."""
    cli = cliente(email)
    dados = json.loads(cli["dados"]) if cli["dados"] else None
    with _lock, db() as c:
        for r in c.execute("SELECT id, sku FROM compras WHERE email=? AND status='aguardando_dados'", (cli["email"],)).fetchall():
            if dados_completos(dados, r["sku"]):
                c.execute("UPDATE compras SET status='na_fila', atualizado=? WHERE id=?", (agora(), r["id"]))


# ------------------------------------------------------------------ e-mail
def enviar_email(para, assunto, html, anexo=None, remetente=None, headers=None, bcc=None, reply_to=None):
    if not CFG["RESEND_API_KEY"]:
        f = EMAILS / f'{int(time.time()*1000)}-{secrets.token_hex(2)}-{re.sub(r"[^a-z0-9]", "_", para.lower())}.html'
        f.write_text(f"<!-- de: {remetente or CFG['EMAIL_REMETENTE']} | para: {para} | assunto: {assunto} | anexo: {anexo} -->\n{html}")
        log.info("e-mail (modo teste) salvo em %s", f.name)
        return True
    corpo = {"from": remetente or CFG["EMAIL_REMETENTE"], "to": [para], "subject": assunto, "html": html}
    if reply_to:
        corpo["reply_to"] = reply_to
    elif CFG["EMAIL_RESPOSTA"] and "folego" not in (remetente or "").lower():  # o Fôlego nunca responde para o e-mail do Meu Santo
        corpo["reply_to"] = CFG["EMAIL_RESPOSTA"]
    if headers:
        corpo["headers"] = headers
    if bcc:
        corpo["bcc"] = [bcc]
    if anexo:
        p = pathlib.Path(anexo)
        corpo["attachments"] = [{"filename": p.name, "content": base64.b64encode(p.read_bytes()).decode()}]
    r = httpx.post("https://api.resend.com/emails", json=corpo, timeout=60,
                   headers={"Authorization": f'Bearer {CFG["RESEND_API_KEY"]}'})
    if r.status_code >= 300:
        raise RuntimeError(f"Resend {r.status_code}: {r.text[:300]}")
    return True


FEMININO = {"casal", "numero", "taro"}  # "a sua Compatibilidade", "a sua Numerologia", "a sua Leitura de Tarô"


def _seu(sku, maiuscula=False):
    """'o seu Mapa…', 'a sua Numerologia…'; o 'Seu 2027 nos Astros' já tem o 'seu' no nome."""
    prod = NOMES_PRODUTO[sku]
    if prod.lower().startswith("seu "):
        return prod if maiuscula else prod[0].lower() + prod[1:]
    t = ("a sua " if sku in FEMININO else "o seu ") + prod
    return t[0].upper() + t[1:] if maiuscula else t


def _pronto(sku):
    return "pronta" if sku in FEMININO else "pronto"


def _moldura(conteudo, fundo="#0f0b26", m=None):
    m = m or _marca()
    return f"""<div style="background:{fundo};padding:32px 16px;font-family:Arial,sans-serif">
<div style="max-width:520px;margin:0 auto;background:#fbf8f2;border-radius:16px;padding:32px 28px;color:#221a3d;line-height:1.6">
<div style="text-align:center;color:#b8924a;letter-spacing:3px;font-size:12px;font-weight:bold;margin-bottom:18px">{m["simbolo"]} {m["marca"].upper()} {m["simbolo"]}</div>
{conteudo}
<p style="color:#8a8199;font-size:12px;margin-top:28px;border-top:1px solid #e7dfcf;padding-top:14px">
{m["rodape"]}</p></div></div>"""


def _botao(url, txt):
    return (f'<p style="text-align:center;margin:26px 0"><a href="{url}" style="background:#d4ac62;color:#1d1406;'
            f'text-decoration:none;padding:15px 26px;border-radius:12px;font-weight:bold;display:inline-block">{txt}</a></p>')


def email_pedir_dados(cli, skus, vez=1):
    prom = [x for x in skus if x in SKUS_PROMESSA]
    if prom:
        _email_pedir_dados_promessa(cli, prom, vez); skus = [x for x in skus if x not in SKUS_PROMESSA]
        if not skus:
            return
    santo = [x for x in skus if x in SKUS_SANTO]
    if santo and len(santo) != len(skus):  # comprou das duas marcas: um e-mail para cada
        email_pedir_dados(cli, santo, vez); skus = [x for x in skus if x not in SKUS_SANTO]
    elif santo:
        return _email_pedir_dados_santo(cli, santo, vez)
    nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    precisa_p2 = "casal" in skus
    so_numero = set(skus) == {"numero"}
    so_deusa = bool(skus) and set(skus) <= {"deusa", "ritual"}
    so_taro = bool(skus) and set(skus) <= {"taro", "taro_amor", "taro_ano"}
    pagina = "dados-taro" if so_taro else "dados-deusas" if so_deusa else "dados-numerologia" if so_numero else "dados"
    url = f'{CFG["SITE_URL"]}/{pagina}?t={cli["token"]}'
    extra = "<p>Como você levou a <b>Compatibilidade Amorosa</b>, peça também a data, a hora e a cidade de nascimento da outra pessoa.</p>" if precisa_p2 else ""
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, falta só um passo ✨</h2>
<p>Seu pagamento foi confirmado. {"As suas cartas estão guardadas. Para a sua <b>leitura de tarô</b> ficar pronta, só falta confirmar o seu e-mail (leva menos de 1 minuto)." if so_taro else "Para montarmos o seu <b>Mapa das 7 Deusas</b>, confirme suas respostas do teste (leva menos de 1 minuto)." if so_deusa else "Para calcularmos os seus números, confirme seu <b>nome completo de registro e sua data de nascimento</b>." if so_numero else "Para calcularmos o seu céu com precisão, confirme sua <b>data, hora e cidade de nascimento</b>."}</p>{extra}
{_botao(url, "Revelar a minha leitura" if so_taro else "Enviar meus dados")}<p style="font-size:14px;color:#6b6385">{"Assim que você confirmar, a sua leitura fica pronta em poucos minutos e chega neste e-mail." if so_taro else "Assim que você enviar, seu mapa fica pronto em poucos minutos e chega neste e-mail."}</p>""", fundo="#1c0714" if so_taro else "#0f0b26")
    assunto = ("Falta só um passo para a sua leitura de tarô 🔮" if so_taro else "Falta só um passo para o seu Mapa das 7 Deusas" if so_deusa
               else "Falta só um passo para a sua Numerologia" if so_numero else "Falta só um passo para o seu Mapa da Alma")
    enviar_email(cli["email"], assunto, html)


def _email_pedir_dados_santo(cli, skus, vez=1):
    m = _marca("santo"); nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    if not CFG["SITE_URL_SANTO"]:
        alerta_admin("SITE_URL_SANTO vazio", "Venda do Meu Santo Protetor sem SITE_URL_SANTO no .env: o link do e-mail vai para o site errado.")
    devoc = [x for x in skus if x in SKUS_DEVOC]
    outros = [x for x in skus if x not in SKUS_DEVOC and not (x == "consagracao" and devoc)]
    if any(x in SKUS_ENFERMO for x in outros):  # os bumps do Rezo por Você usam a mesma página: um e-mail só
        outros = [x for x in outros if x not in SKUS_ENFERMO] + ["enfermo"]
    if outros:  # consagração (sem devocionário), livro da família e Rezo por Você têm páginas próprias
        tit = {"consagracao": ("a sua Consagração a Jesus por Maria", "dados-consagracao", "Confirmar e receber a minha consagração",
                               "o seu nome, a sua intenção e a data em que você quer se consagrar"),
               "livro_familia": ("Os Santos Protetores da sua Família", "dados-familia", "Montar o livro da minha família",
                                 "o nome e o dia de nascimento (dia e mês) de cada pessoa da família"),
               "enfermo": ("o seu livro de orações", "dados-enfermo", "Montar o livro de orações",
                           "o nome de quem está doente e o que essa pessoa está passando"
                           + (", e a data de nascimento dela (dia e mês), para o Santo Protetor" if "enfermo_santo" in skus else ""))}
        partes = ([("o seu Devocionário" + (" e a Consagração" if "consagracao" in skus else ""), "dados", "Preencher o meu devocionário", "o seu aniversário (dia e mês)")] if devoc else []) \
                 + [(tit[x][0][0].upper() + tit[x][0][1:], tit[x][1], tit[x][2], tit[x][3]) for x in outros]
        if len(partes) > 1:  # Biblioteca e combinações: um e-mail só, com um botão para cada parte
            site, tok = m["site"], cli["token"]
            bl = "".join(f'<div style="border:1px solid #e3d9c3;border-radius:12px;padding:14px 16px;margin:12px 0"><b>{i + 1}. {a}</b>'
                         f'<p style="margin:4px 0 10px;font-size:14px;color:#6b6385">Falta: {oque}.</p>{_botao(site + "/" + pg + "?t=" + tok, bt)}</div>'
                         for i, (a, pg, bt, oque) in enumerate(partes))
            html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, a sua compra tem {len(partes)} partes 🙏</h2>
<p><b>✅ Seu pagamento foi confirmado.</b> Os livros ainda não foram enviados porque cada um é preparado com os dados de quem vai recebê-lo, então são {len(partes)} formulários rápidos (1 a 2 minutos cada). Pode preencher um de cada vez, quando quiser: cada livro chega neste e-mail assim que você confirmar a parte dele.</p>{bl}""",
                            fundo=m["fundo"], m=m)
            enviar_email(cli["email"], (f"Falta só um passo para os seus {len(partes)} livros 🙏" if vez == 1 else f"Lembrete: ainda faltam dados para os seus livros"), html, remetente=m["remetente"])
            return
        for x in outros:
            a, pg, bt, oque = tit[x]
            html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, falta só um passo 🙏</h2>
<p><b>✅ Seu pagamento foi confirmado.</b> Ainda não enviamos {a} porque o material é feito com os seus dados: só falta confirmar {oque} (leva 2 minutos).</p>
{_botao(f'{m["site"]}/{pg}?t={cli["token"]}', bt)}<p style="font-size:14px;color:#6b6385">Assim que você confirmar, o PDF fica pronto em poucos minutos e chega neste e-mail.</p>""",
                            fundo=m["fundo"], m=m)
            enviar_email(cli["email"], (f"Falta só um passo para {a} 🙏" if vez == 1 else f"Lembrete: ainda falta um passo para {a}"), html, remetente=m["remetente"])
        if not devoc:
            return
        skus = devoc
    url = f'{m["site"]}/dados?t={cli["token"]}'
    fam = ("<p>Como você levou os <b>Santos Protetores da Família</b>, tenha em mãos o nome e a data de nascimento (dia e mês) "
           "de quem você quer incluir, até 4 pessoas.</p>") if "santo_familia" in skus else ""
    titulo, intro, assunto = {
        1: (f"✅ Pagamento confirmado, {nome}!",
            "O seu <b>devocionário</b> é feito com o santo do dia em que você nasceu, por isso <b>ele ainda não foi enviado</b>: "
            "só falta você informar o <b>dia e o mês do seu aniversário</b>. Leva menos de 1 minuto.",
            "✅ Pagamento confirmado: falta só a data do seu aniversário"),
        2: (f"{nome}, o seu devocionário ainda não foi preparado",
            "Você comprou o seu <b>devocionário</b>, mas ele ainda não foi gerado: falta só o dia e o mês do seu aniversário. "
            "É por essa data que descobrimos o seu santo. Toque no botão, confirme a data e ele chega aqui em poucos minutos.",
            "O seu Devocionário ainda está esperando por você 🙏"),
        3: (f"{nome}, posso preparar o seu devocionário por você?",
            "O seu <b>devocionário</b> ainda não foi gerado, porque falta o dia e o mês do seu aniversário. "
            "Se o formulário deu algum problema, <b>é só responder este e-mail com o dia e o mês em que você nasceu</b> (por exemplo: 13 de junho) "
            "que eu preparo e envio para você. Se preferir, o botão continua funcionando.",
            "Último lembrete: o seu Devocionário ainda não foi gerado"),
    }[min(vez, 3)]
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{titulo}</h2>
<p>{intro}</p>{fam}
{_botao(url, "Informar meu aniversário")}<p style="font-size:14px;color:#6b6385">Assim que você informar, o seu devocionário fica pronto em poucos minutos e chega neste e-mail, com o botão para baixar.
<b>Prefere não clicar?</b> É só responder este e-mail com o dia e o mês em que você nasceu (por exemplo: 13 de junho) que nós preparamos para você.</p>""",
                    fundo=m["fundo"], m=m)
    enviar_email(cli["email"], assunto, html, remetente=m["remetente"])


def _email_entrega_santo(cli, sku, arquivo, link):
    import santos
    m = _marca(sku); nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    try:
        sz = json.loads(cli["dados"])["santo"]; st = santos.santo_do_dia(sz["dia"], sz["mes"])["nome"]
    except Exception:
        st = "o seu santo protetor"
    try:
        ez = json.loads(cli["dados"])["enfermo"]; dn = ez["nome"].split()[0].capitalize()
        st_e = santos.santo_do_dia(ez["dia"], ez["mes"])["nome"] if ez.get("dia") else "o santo protetor"
    except Exception:
        dn, st_e = "quem você ama", "o santo protetor"
    titulo, assunto, corpo, botao = {
        "santo": ("o seu devocionário chegou", "O seu Devocionário está pronto 🙏",
                  f"Aqui está o devocionário de {st} feito para você: a história do seu santo, a sua oração pessoal, a novena de nove dias e o santinho para guardar.",
                  "Baixar meu devocionário"),
        "santo_familia": ("os santos da sua família chegaram", "Os Santos Protetores da sua Família estão prontos 🙏",
                          "O santo de cada pessoa da sua família, com uma oração para cada uma, a oração pela família e a consagração do lar.", "Baixar o PDF da família"),
        "santo_cal": ("o seu Calendário de Fé 2027 chegou", "O seu Calendário de Fé 2027 está pronto 🙏",
                      f"As festas de 2027 mês a mês, com o dia de {st} marcado, uma intenção e uma oração para cada mês.", "Baixar meu calendário"),
        "santo_urgente": ("a sua Novena das Causas Urgentes chegou", "A sua Novena das Causas Urgentes está pronta 🙏",
                          "Nove dias pedindo a intercessão de Santo Expedito e de Santa Rita, com a oração do seu pedido, a reflexão de cada dia e o santinho para guardar. "
                          "Comece hoje mesmo: é o jeito de Santo Expedito.", "Baixar a minha novena"),
        "santo_noite": ("as suas Orações para Dormir em Paz chegaram", "As suas Orações para Dormir em Paz estão prontas 🌙",
                        f"30 orações curtas para a noite, uma para cada dia, com {st} rezando com você. Deixe no celular, ao lado da cama: "
                        "são só 5 minutos antes de dormir.", "Baixar as orações da noite"),
        "consagracao": ("a sua Consagração chegou", "A sua Consagração a Jesus por Maria está pronta 🙏",
                        _corpo_consagracao(cli), "Baixar minha consagração"),
        "livro_familia": ("Os Santos Protetores da sua Família chegaram", "Os Santos Protetores da sua Família estão prontos 🙏",
                          "Uma página para cada pessoa da casa com o santo dela, a história e uma oração; os santinhos para recortar; a novena da família; o Natal em família; "
                          "a consagração do lar, o calendário de 2027 e as orações para cada momento.",
                          "Baixar o livro da família"),
        "enfermo": ("o seu livro de orações chegou", f"Rezo por Você: as orações por {dn} estão prontas 🙏",
                    f"Aqui está o livro de orações por {dn}: a sua oração pessoal, a novena de São Rafael, as orações para cada momento "
                    "(cirurgia, exame, noite no hospital, dor, melhora), a Unção dos Enfermos e o santinho de cabeceira.", "Baixar o livro de orações"),
        "enfermo_santo": (f"o santo protetor de {dn} chegou", f"O Santo Protetor de {dn} está pronto 🙏",
                          f"{dn} nasceu no dia de {st_e}. Aqui está o devocionário para entregar a {dn}: a história do santo, uma oração pessoal, a novena e o santinho.",
                          "Baixar o devocionário"),
        "enfermo_cartoes": ("os cartões de fé chegaram", f"Os 30 cartões de fé para {dn} estão prontos 🙏",
                            f"São 30 imagens com o nome de {dn}, uma para cada dia. Abra o arquivo no celular e mande uma por dia no WhatsApp, junto com uma mensagem sua.",
                            "Baixar os cartões"),
    }[sku]
    papel = _botao(link + "/papel-de-parede", "Baixar o papel de parede") if sku == "santo" and arquivo and _papel_de_parede(arquivo).exists() else ""
    try:
        sz0 = json.loads(cli["dados"])["santo"]
        if sku == "santo" and CFG["CLUBE_CONVITE"] == "1":
            papel += (f'<div style="border:1px solid #e2cf9f;background:#fffaf0;border-radius:14px;padding:14px 16px;margin:18px 0 0">'
                      f'<b>🙏 Quer rezar com o seu santo todos os dias?</b><br><span style="font-size:15px">No <b>Clube Terço Diário</b>, '
                      f'chega toda manhã uma oração com o seu nome, e todo mês o Caderno do Terço. '
                      f'<a href="{(CFG["CLUBE_PAGINA"] or m["site"] + "/clube")}?src=entrega" style="color:#a07b37">Conhecer o clube →</a></span></div>')
        if sku == "santo" and sz0.get("origem") == "quiz":
            papel += (f'<p style="font-size:14px;color:#6b6385">Usamos a data que você informou no teste: <b>{santos.santo_do_dia(sz0["dia"], sz0["mes"])["data"]}</b>. '
                      "Se não for essa a data do seu aniversário, é só responder este e-mail com a data certa que preparamos de novo.</p>")
    except Exception:
        pass
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, {titulo} 🙏</h2>
<p>{corpo} O PDF está em anexo e também pode ser baixado pelo botão abaixo.</p>
{_botao(link, botao)}{papel}
<p style="font-size:14px;color:#6b6385">{"Os cartões vêm num arquivo .zip: no celular, toque nele para abrir as imagens." if sku == "enfermo_cartoes" else "Dica: reze com calma, num momento só seu. Se quiser imprimir, as páginas foram feitas no tamanho A4."}</p>""",
                    fundo=m["fundo"], m=m)
    enviar_email(cli["email"], assunto, html, anexo=arquivo, remetente=m["remetente"])


def _corpo_consagracao(cli):
    import consagracao as cg
    try:
        d = json.loads(cli["dados"]); cz = d.get("consagracao") or {}
        f = cg.escolher(cz.get("festa"))
        return (f"Os 33 dias de preparação começam em <b>{cg.data_pt(f['inicio'], True)}</b>, e a sua consagração será em "
                f"<b>{cg.data_pt(f['data'], True)}</b>, festa de {f['festa']}. Dentro do PDF estão as meditações de cada dia, as orações, "
                "o Ato de Consagração com o seu nome e o certificado.")
    except Exception:
        return "As meditações de cada dia, as orações, o Ato de Consagração com o seu nome e o certificado."


def _email_pedir_dados_promessa(cli, skus, vez=1):
    m = _marca("promessa"); nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    url = f'{m["site"]}/dados?t={cli["token"]}'
    extra = []
    if "promessa_filhos" in skus: extra.append("o nome dos seus filhos")
    if "promessa_jejum" in skus: extra.append("os seus propósitos para o jejum (opcional)")
    base = "o nome de cada pessoa da sua casa" if "casa" in skus else "o dia e o mês do seu aniversário" if "promessa" in skus else "o seu nome"
    oque = base + ("".join(f", {x}" for x in extra[:-1]) + f" e {extra[-1]}" if extra else "")
    titulo, intro, assunto = {
        1: (f"{nome}, falta só um passo 🙏", f"Seu pagamento foi confirmado. Para prepararmos o seu material, só falta confirmar {oque} (leva 1 minuto).",
            "Falta só um passo para o seu propósito de oração 🙏" if "casa" in skus else "Falta só um passo para o seu Versículo para 2027 🙏"),
        2: (f"{nome}, o seu material ainda está esperando", f"Você comprou, mas ele ainda não foi preparado: falta {oque}. Toque no botão e ele chega aqui em poucos minutos.",
            "O seu propósito Eu e a Minha Casa ainda está esperando por você" if "casa" in skus else "O seu Versículo para 2027 ainda está esperando por você"),
        3: (f"{nome}, posso preparar para você?", f"O seu material ainda não foi preparado. Se o formulário deu algum problema, <b>é só responder este e-mail com {oque}</b> que nós preparamos e enviamos para você.",
            "Último lembrete: o seu material ainda não foi preparado"),
    }[min(vez, 3)]
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{titulo}</h2><p>{intro}</p>
{_botao(url, "Confirmar meus dados")}<p style="font-size:14px;color:#6b6385">Assim que você confirmar, o PDF fica pronto em poucos minutos e chega neste e-mail.</p>""", fundo=m["fundo"], m=m)
    enviar_email(cli["email"], assunto, html, remetente=m["remetente"])


def _email_entrega_promessa(cli, sku, arquivo, link):
    import promessa as P
    m = _marca(sku); nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    try:
        pz = json.loads(cli["dados"])["promessa"]; fil = pz.get("filhos") or []
        pr = P.promessa(pz["dia"], pz["mes"]) if pz.get("dia") else {"ref": "a sua promessa"}
    except Exception:
        pz, pr, fil = {}, {"ref": "a sua promessa"}, []
    ns = ", ".join(fil[:-1]) + " e " + fil[-1] if len(fil) > 1 else (fil[0] if fil else "os seus filhos")
    try:
        import casa as K; pess = K.lista([K.prim(x["nome"]) for x in (pz.get("pessoas") or []) if x.get("relacao") != "eu"]) or "a sua família"
    except Exception:
        pess = "a sua família"
    assunto, corpo, botao = {
        "casa": ("Eu e a Minha Casa: o seu propósito chegou 🙏", f"Aqui está o seu propósito de 21 dias de oração por {pess}, com o nome de cada um em cada oração, "
                 "a consagração do lar, o quadro “Eu e a minha casa serviremos ao Senhor” para imprimir e o caderno de respostas. Comece hoje, pelo Dia 1.", "Baixar o meu propósito"),
        "promessa": ("O seu Versículo para 2027 chegou 🙏", f"A promessa do dia do seu aniversário é <b>{pr['ref']}</b>. No PDF você encontra a explicação dela, a oração da sua promessa, "
                     "o devocional de 30 dias, uma promessa para cada mês de 2027 e o cartão para recortar.", "Baixar o meu devocional"),
        "promessa_filhos": ("31 Dias Orando pelos Meus Filhos 🙏", f"Aqui estão as 31 orações por {ns}, uma para cada dia, com um versículo e a bênção final.", "Baixar as orações"),
        "promessa_jejum": ("O seu Jejum de Daniel está pronto 🙏", "O plano de 21 dias com o que comer e o que evitar, os seus propósitos e uma leitura e uma oração para cada dia.", "Baixar o plano"),
    }[sku]
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, chegou 🙏</h2>
<p>{corpo} O PDF está em anexo e também pode ser baixado pelo botão abaixo.</p>{_botao(link, botao)}
<p style="font-size:14px;color:#6b6385">Dica: salve o PDF no celular para ler todos os dias. Se quiser imprimir, as páginas foram feitas no tamanho A4.</p>""", fundo=m["fundo"], m=m)
    enviar_email(cli["email"], assunto, html, anexo=arquivo, remetente=m["remetente"])


def email_entrega(cli, sku, arquivo, link):
    if sku in SKUS_PROMESSA:
        return _email_entrega_promessa(cli, sku, arquivo, link)
    if sku in SKUS_SANTO:
        return _email_entrega_santo(cli, sku, arquivo, link)
    nome = (cli["nome"] or "").split(" ")[0] or "Olá"
    prod = NOMES_PRODUTO[sku]
    taro = sku.startswith("taro")
    intro = {"taro": "As 7 cartas que você tirou foram reveladas e lidas uma a uma para a sua pergunta, incluindo a carta oculta, com uma página só para ela.",
             "taro_amor": "Três cartas novas, tiradas só para o seu coração: você, a outra pessoa e o que existe entre vocês.",
             "taro_ano": "Treze cartas tiradas para o seu ano: a carta regente de 2027 e uma carta para cada mês."}.get(sku)
    corpo = intro or f'Preparamos sua leitura a partir {"das suas respostas ao teste das 7 deusas" if sku in ("deusa", "ritual") else "do seu nome e da sua data de nascimento" if sku == "numero" else "do céu exato do seu nascimento"}.'
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, {_seu(sku)} chegou {"🔮" if taro else "✨"}</h2>
<p>{corpo} O PDF está em anexo e também pode ser baixado pelo botão abaixo.</p>
{_botao(link, "Baixar minha leitura" if taro else "Baixar meu PDF")}{_botao(link + "/papel-de-parede", "Baixar meu papel de parede") if sku == "deusa" and arquivo and _papel_de_parede(arquivo).exists() else ""}
<p style="font-size:14px;color:#6b6385">Dica: leia com calma, de preferência num momento só seu{", com a sua pergunta em mente" if taro else ""}. Se algo não fizer sentido, responda este e-mail.</p>""", fundo="#1c0714" if taro else "#0f0b26")
    enviar_email(cli["email"], f"{_seu(sku, True)} está {_pronto(sku)} {'🔮' if taro else '✨'}", html, anexo=arquivo)


_ultimo_alerta = {"t": 0.0, "n": 0}


def alerta_admin(assunto, texto):
    log.error("%s: %s", assunto, texto)
    # no máximo 1 alerta a cada 30 min: quando a IA cai, cada compra gerava um e-mail
    if time.time() - _ultimo_alerta["t"] < 1800:
        _ultimo_alerta["n"] += 1
        return
    if _ultimo_alerta["n"]:
        assunto = f"{assunto} (+{_ultimo_alerta['n']} outros alertas desde o último e-mail)"
    _ultimo_alerta.update(t=time.time(), n=0)
    if CFG["ADMIN_EMAIL"]:
        try:
            enviar_email(CFG["ADMIN_EMAIL"], f"[Mapa da Alma] {assunto}", f"<pre>{texto[:5000]}</pre>")
        except Exception:
            log.exception("falha ao alertar admin")


# ------------------------------------------------------------------ geração
def _pessoa(p):
    import calc
    d, m, y = map(int, p["data"].split("/"))
    h, mi = (None, None) if not p.get("hora") else map(int, p["hora"].split(":"))
    return calc.calcular(p["nome"], y, m, d, h, mi, p["cidade"])


def _texto_mock(sku):
    return json.loads((BASE / {"natal": "exemplo_ana.json", "ano": "exemplo_ana_2027.json", "casal": "exemplo_ana_rafael.json",
                               "numero": "exemplo_numero.json", "deusa": "exemplo_deusa.json", "ritual": "exemplo_ritual.json",
                               "taro": "exemplo_taro.json", "taro_amor": "exemplo_taro_amor.json", "taro_ano": "exemplo_taro_ano.json",
                               "santo": "exemplo_santo.json", "santo_familia": "exemplo_santo_familia.json", "santo_cal": "exemplo_santo_cal.json", "santo_urgente": "exemplo_santo_urgente.json", "santo_noite": "exemplo_santo_noite.json",
                               "consagracao": "exemplo_consagracao.json", "livro_familia": "exemplo_livro_familia.json",
                               "enfermo": "exemplo_enfermo.json", "enfermo_santo": "exemplo_santo.json", "promessa": "exemplo_promessa.json"}[sku]).read_text())


def _papel_de_parede(arq):
    p = pathlib.Path(arq)
    return p.with_name(p.stem + "-papel-de-parede.png")


def gerar(compra, dados):
    import calc, pdf, interpretar
    slug = lambda s: re.sub(r"[^a-z0-9]+", "-", _sem_acento(s)).strip("-")[:40]
    mock = CFG["MOCK_IA"] == "1"
    ctx = dados.get("contexto") or {}
    if compra["sku"] == "consagracao":
        import consagracao as cg, santos
        sz = dados.get("santo") or {}
        cz = dados.get("consagracao") or {"nome": sz.get("nome", ""), "intencao": sz.get("intencao", ""), "pedido": sz.get("pedido", "")}
        festa = cg.escolher(cz.get("festa"))
        st = santos.santo_do_dia(sz["dia"], sz["mes"])["nome"] if sz.get("dia") else None
        texto = _texto_mock("consagracao") if mock else interpretar.interpretar_consagracao(cz, festa, st)
        arq = PDFS / f'{compra["id"]}-consagracao-a-jesus-por-maria-{slug(cz["nome"].split()[0])}.pdf'
        pdf.gerar_pdf_consagracao(cz, texto, festa, arq, marca=CFG["MARCA_SANTO"])
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] in SKUS_PROMESSA:
        pz = dados["promessa"]; sku = compra["sku"]; prim = slug(pz["nome"].split()[0]); mc = CFG["MARCA_PROMESSA"]
        if sku == "casa":
            arq = PDFS / f'{compra["id"]}-eu-e-a-minha-casa-{prim}.pdf'; pdf.gerar_pdf_casa(pz, arq, marca=mc)
        elif sku == "promessa_filhos":
            arq = PDFS / f'{compra["id"]}-31-dias-orando-pelos-filhos-{prim}.pdf'; pdf.gerar_pdf_filhos(pz, pz["filhos"], arq, marca=mc)
        elif sku == "promessa_jejum":
            arq = PDFS / f'{compra["id"]}-jejum-de-daniel-{prim}.pdf'; pdf.gerar_pdf_jejum(pz, pz.get("propositos") or [], arq, marca=mc)
        else:
            texto = _texto_mock("promessa") if mock else interpretar.interpretar_promessa(pz)
            arq = PDFS / f'{compra["id"]}-meu-versiculo-2027-{prim}.pdf'; pdf.gerar_pdf_promessa(pz, texto, arq, marca=mc)
            arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] in SKUS_ENFERMO:
        import enfermo as ef, santos
        ez = dados["enfermo"]; sku = compra["sku"]; prim = slug(ez["nome"].split()[0]); mc = CFG["MARCA_SANTO"]
        if sku == "enfermo_cartoes":
            arq = PDFS / f'{compra["id"]}-cartoes-de-fe-{prim}.zip'
            pdf.gerar_cartoes_enfermo(ez, arq, marca=mc)
            return arq
        if sku == "enfermo_santo":  # o devocionário do santo do dia em que o doente nasceu, para entregar a ele
            _, gen = ef.RELACOES.get(ez.get("relacao"), ef.RELACOES["outro"])
            sz = {"nome": ez["nome"], "dia": ez["dia"], "mes": ez["mes"], "intencao": "", "momento": "",
                  "pedido": f"Estou passando por um momento de doença ({ef.situacao(ez.get('situacao'), gen)}) e quero rezar pela minha saúde, pela minha paz e pela minha família."}
            texto = _texto_mock("enfermo_santo") if mock else interpretar.interpretar_santo(sz)
            arq = PDFS / f'{compra["id"]}-santo-protetor-{slug(santos.santo_do_dia(ez["dia"], ez["mes"])["nome"])}-{prim}.pdf'
            pdf.gerar_pdf_santo(sz, texto, arq, marca=mc)
        else:
            texto = _texto_mock("enfermo") if mock else interpretar.interpretar_enfermo(ez)
            arq = PDFS / f'{compra["id"]}-rezo-por-{prim}.pdf'
            pdf.gerar_pdf_enfermo(ez, texto, arq, marca=mc)
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] == "livro_familia":
        lf = dados["livro_familia"]
        texto = _texto_mock("livro_familia") if mock else interpretar.interpretar_livro_familia(lf)
        if mock:  # o exemplo tem 4 pessoas; ajusta ao tamanho da família do teste
            texto["pessoas"] = (texto["pessoas"] * 3)[:len(lf["pessoas"])]
        arq = PDFS / f'{compra["id"]}-livro-de-oracoes-{slug(lf.get("sobrenome") or lf["pessoas"][0]["nome"].split()[0])}.pdf'
        pdf.gerar_pdf_livro_familia(lf, texto, arq, marca=CFG["MARCA_SANTO"])
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] in SKUS_SANTO:
        import santos
        sz = dados["santo"]; sku = compra["sku"]; prim = slug(sz["nome"].split()[0]); mc = CFG["MARCA_SANTO"]
        st = santos.santo_do_dia(sz["dia"], sz["mes"])
        pessoas = (dados.get("santo_familia") or {}).get("pessoas") or []
        if sku == "santo":
            texto = _texto_mock("santo") if mock else interpretar.interpretar_santo(sz)
            arq = PDFS / f'{compra["id"]}-devocionario-{slug(st["nome"])}-{prim}.pdf'
            try:  # o papel de parede é bônus: se falhar, o PDF sai mesmo assim
                pdf.gerar_papel_santo(sz, texto, _papel_de_parede(arq), marca=mc)
            except Exception:
                log.exception("papel de parede (santo) falhou")
            pdf.gerar_pdf_santo(sz, texto, arq, marca=mc)
        elif sku == "santo_urgente":
            texto = _texto_mock("santo_urgente") if mock else interpretar.interpretar_urgente(sz)
            arq = PDFS / f'{compra["id"]}-novena-das-causas-urgentes-{prim}.pdf'
            pdf.gerar_pdf_santo_urgente(sz, texto, arq, marca=mc)
        elif sku == "santo_noite":
            texto = _texto_mock("santo_noite") if mock else interpretar.interpretar_noite(sz)
            arq = PDFS / f'{compra["id"]}-oracoes-para-dormir-em-paz-{prim}.pdf'
            pdf.gerar_pdf_santo_noite(sz, texto, arq, marca=mc)
        elif sku == "santo_familia":
            texto = _texto_mock("santo_familia") if mock else interpretar.interpretar_santo_familia(sz, pessoas)
            arq = PDFS / f'{compra["id"]}-santos-da-familia-{prim}.pdf'
            pdf.gerar_pdf_santo_familia(sz, texto, pessoas, arq, marca=mc)
        else:
            meses = santos.calendario_2027(st, [dict(x, santo=santos.santo_do_dia(x["dia"], x["mes"])) for x in pessoas])
            texto = _texto_mock("santo_cal") if mock else interpretar.interpretar_santo_cal(sz, meses)
            arq = PDFS / f'{compra["id"]}-calendario-de-fe-2027-{prim}.pdf'
            pdf.gerar_pdf_santo_cal(sz, texto, meses, arq, marca=mc)
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"].startswith("taro"):
        import tarot
        tz = dados["taro"]; sku = compra["sku"]; prim = slug(tz["nome"].split()[0])
        if sku == "taro":
            texto = _texto_mock("taro") if mock else interpretar.interpretar_taro(tz)
            arq = PDFS / f'{compra["id"]}-leitura-de-taro-{prim}.pdf'
            pdf.gerar_pdf_taro(tz, texto, arq, marca=CFG["MARCA"])
        elif sku == "taro_amor":
            ids = tarot.tirar(f'{compra["pedido"]}-amor', 3, evitar=tz["cartas"])
            texto = _texto_mock("taro_amor") if mock else interpretar.interpretar_taro_amor(tz, ids)
            arq = PDFS / f'{compra["id"]}-taro-do-amor-{prim}.pdf'
            pdf.gerar_pdf_taro_amor(tz, texto, ids, arq, marca=CFG["MARCA"])
        else:
            ids = tarot.tirar(f'{compra["pedido"]}-2027', 13)
            texto = _texto_mock("taro_ano") if mock else interpretar.interpretar_taro_ano(tz, ids)
            arq = PDFS / f'{compra["id"]}-taro-de-2027-{prim}.pdf'
            pdf.gerar_pdf_taro_ano(tz, texto, ids, arq, marca=CFG["MARCA"])
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] in ("deusa", "ritual"):
        import deusas
        dz = deusas.calcular(dados["deusas"]["nome"], dados["deusas"]["respostas"])
        dctx = dados["deusas"].get("contexto") or {}
        if compra["sku"] == "deusa":
            texto = _texto_mock("deusa") if mock else interpretar.interpretar_deusa(dz, dctx)
            arq = PDFS / f'{compra["id"]}-mapa-das-7-deusas-{slug(dz["primeiro_nome"])}.pdf'
            papel = None
            try:  # o papel de parede é bônus: se falhar, o PDF sai mesmo assim
                papel = pdf.gerar_papel_de_parede(dz, texto, _papel_de_parede(arq), marca=CFG["MARCA"])
            except Exception:
                log.exception("papel de parede falhou")
            pdf.gerar_pdf_deusa(dz, texto, arq, marca=CFG["MARCA"], papel=papel)
        else:
            texto = _texto_mock("ritual") if mock else interpretar.interpretar_ritual(dz, dctx)
            arq = PDFS / f'{compra["id"]}-ritual-21-dias-{slug(dz["primeiro_nome"])}.pdf'
            pdf.gerar_pdf_ritual(dz, texto, arq, marca=CFG["MARCA"])
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    if compra["sku"] == "numero":
        import numerologia
        n = numerologia.calcular(dados["num"]["nome"], dados["num"]["data"])
        texto = _texto_mock("numero") if mock else interpretar.interpretar_numero(n, ctx)
        arq = PDFS / f'{compra["id"]}-numerologia-{slug(n["primeiro_nome"])}.pdf'
        pdf.gerar_pdf_numero(n, texto, arq, marca=CFG["MARCA"])
        arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
        arq.with_suffix(".html").unlink(missing_ok=True)
        return arq
    p1 = _pessoa(dados["p1"])
    nome_arq = {"natal": f"mapa-astral-{slug(p1['nome'])}", "ano": f"seu-2027-{slug(p1['nome'])}"}.get(compra["sku"])
    if compra["sku"] == "natal":
        texto = _texto_mock("natal") if mock else interpretar.interpretar(p1, ctx)
        arq = PDFS / f'{compra["id"]}-{nome_arq}.pdf'
        pdf.gerar_pdf(p1, texto, calc.desenhar_svg(p1), arq, marca=CFG["MARCA"])
    elif compra["sku"] == "ano":
        import ano
        a = ano.calcular_ano(p1)
        texto = _texto_mock("ano") if mock else interpretar.interpretar_ano(p1, a, ctx)
        arq = PDFS / f'{compra["id"]}-{nome_arq}.pdf'
        pdf.gerar_pdf_ano(p1, a, texto, arq, marca=CFG["MARCA"])
    else:
        import sinastria
        p2 = _pessoa(dados["p2"])
        s = sinastria.calcular_sinastria(p1, p2)
        texto = _texto_mock("casal") if mock else interpretar.interpretar_sinastria(s, ctx)
        arq = PDFS / f'{compra["id"]}-compatibilidade-{slug(p1["nome"].split()[0])}-{slug(p2["nome"].split()[0])}.pdf'
        pdf.gerar_pdf_sinastria(p1, p2, s, texto, sinastria.desenhar_svg_duplo(p1, p2), arq, marca=CFG["MARCA"])
    arq.with_suffix(".json").write_text(json.dumps(texto, ensure_ascii=False, indent=1))
    for extra in (arq.with_suffix(".html"),):
        extra.unlink(missing_ok=True)
    return arq


def processar_um():
    with _lock, db() as c:
        r = c.execute("SELECT * FROM compras WHERE status='na_fila' ORDER BY id LIMIT 1").fetchone()
        if not r:
            return False
        c.execute("UPDATE compras SET status='gerando', atualizado=? WHERE id=?", (agora(), r["id"]))
    compra = dict(r)
    cli = cliente(compra["email"])
    try:
        dados = json.loads(cli["dados"])
        t0 = time.time()
        arq = gerar(compra, dados)
        tok = secrets.token_urlsafe(20)
        link = f'{_marca(compra["sku"])["api"]}/baixar/{tok}'
        email_entrega(cli, compra["sku"], arq, link)
        with _lock, db() as c:
            c.execute("UPDATE compras SET status='enviado', arquivo=?, baixar=?, erro=NULL, atualizado=? WHERE id=?",
                      (str(arq), tok, agora(), compra["id"]))
        log.info("entregue compra %s (%s) para %s em %.0fs", compra["id"], compra["sku"], compra["email"], time.time() - t0)
    except Exception as e:
        tent = compra["tentativas"] + 1
        novo = "na_fila" if tent < 3 else "erro"
        with _lock, db() as c:
            c.execute("UPDATE compras SET status=?, tentativas=?, erro=?, atualizado=? WHERE id=?",
                      (novo, tent, f"{type(e).__name__}: {e}", agora(), compra["id"]))
        if novo == "erro" and tent >= 9:
            alerta_admin(f"Falha na compra {compra['id']} ({compra['email']})", traceback.format_exc())
        else:
            log.warning("tentativa %s falhou para compra %s: %s", tent, compra["id"], e)
            time.sleep(10)
    return True


def lembretes():
    """Quem pagou e não mandou os dados recebe até 3 lembretes: 20 min, ~1 dia e ~3 dias depois da compra."""
    agora_ = dt.datetime.now()
    etapas = ((0, agora_ - dt.timedelta(minutes=int(CFG["LEMBRETE_MINUTOS"]))), (1, agora_ - dt.timedelta(hours=20)), (2, agora_ - dt.timedelta(hours=68)))
    for nivel, quando in etapas:
        with db() as c:
            folga = (agora_ - dt.timedelta(hours=20)).isoformat(timespec="seconds") if nivel else "9999"  # 20h entre um lembrete e outro
            rows = c.execute("SELECT email, MIN(criado) AS c0 FROM compras WHERE status='aguardando_dados' AND lembrado=? "
                             "AND (atualizado IS NULL OR atualizado<=?) GROUP BY email HAVING c0<=?",
                             (nivel, folga, quando.isoformat(timespec="seconds"))).fetchall()
        for r in rows:
            try:
                skus = [x["sku"] for x in compras_de(r["email"]) if x["status"] == "aguardando_dados"]
                email_pedir_dados(cliente(r["email"]), skus, vez=nivel + 1)
                with _lock, db() as c:
                    c.execute("UPDATE compras SET lembrado=?, atualizado=? WHERE email=? AND status='aguardando_dados'", (nivel + 1, agora(), r["email"]))
            except Exception:
                log.exception("falha no lembrete para %s", r["email"])


# ------------------------------------------------------------------ recuperação de vendas
RECUP_DESC = {"biblioteca": "os 5 livros da Biblioteca da Família Católica: o seu devocionário, o santo de cada pessoa da sua casa, a consagração, as orações pelos doentes e o calendário de 2027",
              "santo": "o devocionário do seu santo protetor, com a sua oração pessoal e a novena",
              "consagracao": "os 33 dias de preparação, com a meditação de cada dia e o Ato de Consagração com o seu nome",
              "livro_familia": "o santo protetor de cada pessoa da sua casa, com a história, a oração, o santinho e a novena da família",
              "enfermo": "as orações por quem você ama, com a novena de São Rafael e uma oração para cada momento",
              "promessa": "a promessa da Bíblia para o dia do seu aniversário e o devocional de 30 dias com o seu nome",
              "casa": "o propósito de 21 dias de oração pela sua família, com o nome de cada um"}
RECUP_ORDEM = ("biblioteca", "santo", "consagracao", "livro_familia", "enfermo", "casa", "promessa")  # o produto principal do pedido (os bumps vêm junto)


def _recup_link(sku, link, tipo):
    base = link or CFG.get({"santo": "CHECKOUT_SANTO", "consagracao": "CHECKOUT_CONSAGRACAO", "livro_familia": "CHECKOUT_LIVRO_FAMILIA", "enfermo": "CHECKOUT_ENFERMO", "casa": "CHECKOUT_PROMESSA", "promessa": "CHECKOUT_PROMESSA", "biblioteca": "CHECKOUT_BIBLIOTECA"}[sku], "")
    if not base:
        return ""
    return base + ("&" if "?" in base else "?") + f"utm_source=email&utm_medium=recuperacao&utm_campaign=recuperacao_{tipo}&src=recuperacao"


def registrar_recuperacao(tipo, email, nome, skus, pedido, link):
    if CFG["RECUPERACAO"] != "1":
        return
    sku = next((x for x in RECUP_ORDEM if x in skus), None)
    if not sku:  # só o Meu Santo Protetor
        return
    with _lock, db() as c:
        if tipo == "carrinho" and c.execute("SELECT 1 FROM recuperacao WHERE email=? AND status='pendente' AND tipo!='carrinho'", (email,)).fetchone():
            return  # já gerou Pix ou tentou o cartão: vale o aviso mais específico
        if tipo != "carrinho":
            c.execute("UPDATE recuperacao SET status='substituido' WHERE email=? AND status='pendente'", (email,))
        c.execute("INSERT INTO recuperacao(email,nome,tipo,sku,pedido,link,status,criado) VALUES(?,?,?,?,?,?,?,?)",
                  (email, nome, tipo, sku, pedido, link, "pendente", agora()))


def email_recuperacao(r):
    m = _marca(r["sku"]); nome = (r["nome"] or "").split(" ")[0] or "Olá"
    prod = NOMES_PRODUTO[r["sku"]]; desc = RECUP_DESC[r["sku"]]; url = _recup_link(r["sku"], r["link"], r["tipo"])
    if not url:
        return False
    if r["tipo"] == "pix":
        assunto = f"O seu Pix ficou pendente: {prod}"
        corpo = (f"<p>Vimos que você gerou o Pix do <b>{prod}</b>, mas o pagamento ainda não chegou para nós.</p>"
                 f"<p>Às vezes o código expira ou o aplicativo do banco fecha no meio do caminho. Se você ainda quiser receber {desc}, "
                 "é só gerar um novo código pelo botão abaixo. Leva um minuto.</p>")
        botao = "Gerar um novo Pix"
    elif r["tipo"] == "recusado":
        assunto = f"O pagamento do {prod} não foi aprovado"
        corpo = (f"<p>O banco não aprovou o pagamento no cartão do <b>{prod}</b>. Isso acontece bastante em compras pela internet "
                 "(limite, segurança do banco) e não quer dizer nada de errado com você.</p>"
                 "<p>Se quiser, pode tentar de novo ou pagar no Pix, que é aprovado na hora.</p>")
        botao = "Tentar de novo"
    else:
        assunto = f"O seu pedido ficou pela metade: {prod}"
        corpo = (f"<p>Você começou o pedido do <b>{prod}</b> e não chegou a finalizar.</p>"
                 f"<p>Se ficou alguma dúvida sobre o material ({desc}), é só responder este e-mail que a gente te ajuda. "
                 "Se quiser concluir, o botão abaixo leva direto para o pagamento.</p>")
        botao = "Finalizar meu pedido"
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{nome}, tudo bem? 🙏</h2>
{corpo}{_botao(url, botao)}
<p style="font-size:14px;color:#6b6385">Se você já pagou ou mudou de ideia, pode ignorar este e-mail. Assim que o pagamento é confirmado, o PDF chega aqui no seu e-mail.</p>""",
                    fundo=m["fundo"], m=m)
    enviar_email(r["email"], assunto, html, remetente=m["remetente"])
    return True


def recuperar():
    if CFG["RECUPERACAO"] != "1":
        return
    espera = {"pix": int(CFG["RECUP_PIX_MIN"]), "recusado": int(CFG["RECUP_RECUSADO_MIN"]), "carrinho": int(CFG["RECUP_CARRINHO_MIN"])}
    with db() as c:
        rows = [dict(r) for r in c.execute("SELECT * FROM recuperacao WHERE status='pendente' ORDER BY id")]
    for r in rows:
        if r["criado"] > (dt.datetime.now() - dt.timedelta(minutes=espera.get(r["tipo"], 60))).isoformat(timespec="seconds"):
            continue
        desde = (dt.datetime.fromisoformat(r["criado"]) - dt.timedelta(hours=6)).isoformat(timespec="seconds")
        with db() as c:
            comprou = c.execute("SELECT 1 FROM compras WHERE email=? AND sku=? AND criado>=? AND status!='reembolsado'",
                                (r["email"], r["sku"], desde)).fetchone()
            recente = c.execute("SELECT 1 FROM recuperacao WHERE email=? AND status IN ('enviado','recuperado') AND enviado>=?",
                                (r["email"], (dt.datetime.now() - dt.timedelta(days=3)).isoformat(timespec="seconds"))).fetchone()
        novo = "pago" if comprou else "ignorado" if recente else None
        if not novo:
            try:
                novo = "enviado" if email_recuperacao(r) else "sem_link"
            except Exception:
                log.exception("falha na recuperação %s", r["id"]); novo = "erro"
        with _lock, db() as c:
            c.execute("UPDATE recuperacao SET status=?, enviado=? WHERE id=?", (novo, agora() if novo == "enviado" else None, r["id"]))
        if novo == "enviado":
            log.info("recuperação %s (%s) enviada para %s", r["id"], r["tipo"], r["email"])


# ------------------------------------------------------------------ Biblioteca: sequência automática para quem já é cliente
NAO_ENVIAR = DADOS / "nao_enviar.txt"
OFERTA_DIAS = (1, 4, 9)   # dias depois da entrega do primeiro livro


def _nao_enviar():
    return {l.strip().lower() for l in NAO_ENVIAR.read_text().splitlines()} if NAO_ENVIAR.exists() else set()


def email_oferta_biblioteca(cli, vez, campanha="biblioteca-auto"):
    """E-mail de oferta da Biblioteca (preço de cliente). vez 1, 2 ou 3. Devolve False se não houver link configurado."""
    import santos
    link = CFG["CHECKOUT_BIBLIOTECA_CLIENTE"] or CFG["CHECKOUT_BIBLIOTECA"]
    if not link:
        return False
    m = _marca("santo")
    try:
        sz = json.loads(cli.get("dados") or "{}").get("santo") or {}
        nome = (sz.get("nome") or cli.get("nome") or "").split()[0].capitalize()
        st = santos.santo_do_dia(sz["dia"], sz["mes"])["nome"] if sz.get("dia") else ""
    except Exception:
        nome, st = (cli.get("nome") or "").split(" ")[0].capitalize(), ""
    nome = nome or "Olá"; pr = CFG["PRECO_BIBLIOTECA_CLIENTE"]
    url = link + ("&" if "?" in link else "?") + f"utm_source=email&utm_medium=clientes&utm_campaign={campanha}-{vez}&src=email_biblioteca"
    sair = f'{m["api"]}/sair?t={cli["token"]}'
    BIB_ITENS = {"santo": ("Devocionário do Meu Santo Protetor", "o seu santo, a história dele, a oração com o seu nome e a novena", 19.0),
                 "livro_familia": ("Os Santos Protetores da sua Família", "o santo de cada pessoa da casa (até 8), com a história, a oração e o santinho", 47.0),
                 "consagracao": ("Consagração a Jesus por Maria", "os 33 dias de preparação e o Ato de Consagração com o seu nome", 37.0),
                 "enfermo": ("Rezo por Você", "orações por quem está doente, com a novena de São Rafael", 19.9),
                 "santo_cal": ("Calendário de Fé 2027", "as festas do ano mês a mês", 10.9)}
    tem = {x["sku"] for x in compras_de(cli["email"]) if x["status"] != "reembolsado"}
    falta = [k for k in BIBLIOTECA if k not in tem]; ja = [k for k in BIBLIOTECA if k in tem]
    soma = sum(BIB_ITENS[k][2] for k in falta)
    itens = ("<ul style='padding-left:18px;margin:10px 0'>" + "".join(f"<li><b>{BIB_ITENS[k][0]}</b>: {BIB_ITENS[k][1]}</li>" for k in falta) + "</ul>"
             + (f"<p style='margin:0'>Você já tem: {', '.join(BIB_ITENS[k][0] for k in ja)}. Por isso, para clientes, a Biblioteca sai mais barata.</p>" if ja else ""))
    preco_txt = (f"Separados, os {len(falta)} livros que faltam custam R$ {soma:.2f}".replace(".", ",") + f". Para quem já é cliente: <b style=\"color:#221a3d;font-size:20px\">R$ {pr}</b>")
    titulo, corpo, assunto = {
        1: (f"{nome}, e o santo de cada pessoa da sua casa?",
            (f"O seu santo protetor é <b>{st}</b>. " if st else "") + "Muita gente, depois de receber o devocionário, pergunta pelo santo do marido, dos filhos, da mãe. "
            "Por isso montamos a <b>Biblioteca da Família Católica</b>: os livros do Meu Santo Protetor juntos, para rezar em casa o ano inteiro." + itens,
            "O santo de cada pessoa da sua casa 🙏"),
        2: ((f"{nome}, um presente de Natal que fica",
             "O Natal está chegando. A Biblioteca traz a <b>novena da família</b> para rezarem juntos nos dias antes do Natal, a oração diante do presépio "
             "e a bênção da ceia, além do santo de cada um com o santinho para recortar. Dá para imprimir e encadernar numa papelaria." + itens,
             "Para rezar em família neste Natal 🎄") if dt.date.today() < dt.date(dt.date.today().year, 12, 24) and dt.date.today().month >= 10 else
            (f"{nome}, para rezar junto com a sua família",
             "A Biblioteca traz a <b>novena da família</b>, para rezarem juntos nove dias seguidos, o santo de cada pessoa da casa com o santinho para recortar "
             "e orações para cada momento da casa. Dá para imprimir e encadernar numa papelaria." + itens,
             "Para rezar em família 🙏")),
        3: (f"{nome}, este é o último e-mail sobre a Biblioteca",
            "Não queremos encher a sua caixa de entrada: este é o último e-mail que mandamos sobre a Biblioteca da Família Católica. "
            "Se fizer sentido para a sua casa, ela continua disponível pelo preço de cliente." + itens,
            "Último e-mail sobre a Biblioteca da Família Católica"),
    }[vez]
    html = _moldura(f"""<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:0 0 12px">{titulo}</h2><p>{corpo}</p>
<p style="text-align:center;margin:18px 0 0;font-size:15px;color:#6b6385">{preco_txt}</p>
{_botao(url, "Quero a Biblioteca da minha família")}
<p style="font-size:13px;color:#6b6385">Garantia de 7 dias. Pagamento único, no Pix ou no cartão.</p>
<p style="font-size:12px;color:#9a93ad;margin-top:20px">Não quer mais receber ofertas? <a href="{sair}" style="color:#9a93ad">Clique aqui</a> e não mandamos mais.</p>""", fundo=m["fundo"], m=m)
    enviar_email(cli["email"], assunto, html, remetente=m["remetente"])
    return True


def ofertas_biblioteca():
    if CFG["OFERTA_BIBLIOTECA"] != "1" or not (CFG["CHECKOUT_BIBLIOTECA_CLIENTE"] or CFG["CHECKOUT_BIBLIOTECA"]):
        return
    agora_ = dt.datetime.now(); nao = _nao_enviar()
    with db() as c:
        base = [dict(r) for r in c.execute(
            "SELECT email, MIN(atualizado) AS entregue FROM compras WHERE status='enviado' AND sku IN (%s) GROUP BY email" % ",".join("?" * len(SKUS_SANTO)),
            tuple(SKUS_SANTO))]
        reemb = {r[0] for r in c.execute("SELECT DISTINCT email FROM compras WHERE status='reembolsado'")}
        tem = {}
        for r in c.execute("SELECT email, sku FROM compras WHERE status!='reembolsado'"):
            tem.setdefault(r[0], set()).add(r[1])
        feitas = {(r[0], r[1]) for r in c.execute("SELECT email, vez FROM ofertas WHERE campanha='biblioteca-auto'")}
        ultimo = {r[0]: r[1] for r in c.execute("SELECT email, MAX(enviado) FROM ofertas GROUP BY email")}
    for b in base:
        e = b["email"]
        precos = {"santo": 19.0, "livro_familia": 47.0, "consagracao": 37.0, "enfermo": 19.9, "santo_cal": 10.9}
        falta = sum(v for k, v in precos.items() if k not in tem.get(e, set()))
        if e in nao or e in reemb or falta < float(CFG["PRECO_BIBLIOTECA_CLIENTE"]) * 1.2 or not b["entregue"]:
            continue  # se o que falta já custa perto do preço de cliente, a oferta não faz sentido
        idade = agora_ - dt.datetime.fromisoformat(b["entregue"])
        if idade > dt.timedelta(days=30):
            continue  # a sequência é para quem comprou agora; a lista antiga recebe pela campanha manual
        for vez, dias in enumerate(OFERTA_DIAS, 1):
            if (e, vez) in feitas or idade < dt.timedelta(days=dias):
                continue
            if vez > 1 and (e, vez - 1) not in feitas:
                break
            # nunca 2 ofertas em menos de 2 dias (quem comprou há 9 dias recebia o 1, o 2 e o 3 em sequência)
            if e in ultimo and agora_ - dt.datetime.fromisoformat(ultimo[e]) < dt.timedelta(days=2):
                break
            try:
                if email_oferta_biblioteca(cliente(e), vez):
                    with _lock, db() as c:
                        c.execute("INSERT OR IGNORE INTO ofertas(email,campanha,vez,enviado) VALUES(?,?,?,?)", (e, "biblioteca-auto", vez, agora()))
                    log.info("oferta biblioteca %s para %s", vez, e)
            except Exception:
                log.exception("falha na oferta da biblioteca para %s", e)
            break  # no máximo 1 e-mail por pessoa por rodada


def sair(t: str = ""):
    """Descadastro das ofertas (o e-mail continua recebendo só o que comprou)."""
    with db() as c:
        r = c.execute("SELECT email FROM clientes WHERE token=?", (t,)).fetchone()
    if r:
        if r["email"] not in _nao_enviar():
            with _lock:
                with NAO_ENVIAR.open("a") as f:
                    f.write(r["email"] + "\n")
        log.info("descadastro: %s", r["email"])
    return ("<html><body style='font-family:Arial;background:#13224a;color:#f5ecd9;text-align:center;padding:60px 20px'>"
            "<h2>Pronto 🙏</h2><p>Você não vai mais receber ofertas. Os e-mails dos livros que você comprou continuam chegando normalmente.</p></body></html>")


def _refila_erros():
    """Compra que falhou 3x volta para a fila depois de 30 min (até 9 tentativas no total).
    Se a IA ficou fora do ar ou sem crédito, a entrega sai sozinha quando ela voltar."""
    limite = (dt.datetime.now() - dt.timedelta(minutes=30)).isoformat(timespec="seconds")
    with _lock, db() as c:
        n = c.execute("UPDATE compras SET status='na_fila', atualizado=? WHERE status='erro' AND tentativas < 9 AND atualizado < ?",
                      (agora(), limite)).rowcount
    if n:
        log.info("recoloquei %s compras com erro na fila", n)


def _trabalhador():
    with _lock, db() as c:  # se o servidor caiu no meio de uma geração, recoloca na fila
        c.execute("UPDATE compras SET status='na_fila' WHERE status='gerando'")
    ultimo_lembrete = 0
    while True:
        try:
            if not processar_um():
                time.sleep(3)
            if time.time() - ultimo_lembrete > 60:
                lembretes(); recuperar(); ofertas_biblioteca(); _refila_erros(); ultimo_lembrete = time.time()
        except Exception:
            log.exception("erro no trabalhador"); time.sleep(5)


# ------------------------------------------------------------------ API
app = FastAPI(title="Mapa da Alma", docs_url=None, redoc_url=None)
origens = {CFG["SITE_URL"], CFG["SITE_URL"].replace("https://", "https://www.")}
if CFG["SITE_URL_SANTO"]:
    origens |= {CFG["SITE_URL_SANTO"].rstrip("/"), CFG["SITE_URL_SANTO"].rstrip("/").replace("https://", "https://www.")}
for _u in (CFG["SITE_URL_PROMESSA"], CFG["FOLEGO_SITE"], os.environ.get("CASAMENTO_SITE", "https://casamento.meusantoprotetor.online")):
    if _u:
        origens |= {_u.rstrip("/"), _u.rstrip("/").replace("https://", "https://www.")}
app.add_middleware(CORSMiddleware, allow_origins=list(origens) + ["null"], allow_origin_regex=r"https://.*\.pages\.dev",
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
import clube as _clube  # noqa: E402  (rotas do Clube Terço Diário)
app.include_router(_clube.router)
import folego as _folego  # noqa: E402  (rotas do Fôlego: folegofinanceiro.shop)
app.include_router(_folego.router)
import casamento as _casamento  # noqa: E402  (O Santo do Nosso Casamento: casamento.py, tabelas casamento_*)
app.include_router(_casamento.router)


@app.on_event("startup")
def _iniciar():
    def _aquecer():  # monta o calendário de 2027 uma vez, para a prévia do quiz responder rápido
        try:
            import ano; ano._efemerides()
        except Exception:
            log.exception("falha ao aquecer efemérides")
    threading.Thread(target=_aquecer, daemon=True).start()
    threading.Thread(target=_trabalhador, daemon=True).start()
    try:
        _folego.tabelas()
    except Exception:
        log.exception("folego: tabelas")
    try:
        _casamento.iniciar()
    except Exception:
        log.exception("casamento: não iniciou")
    try:
        import clube
        clube.iniciar()
    except Exception:
        log.exception("clube: não iniciou")
    log.info("servidor iniciado")


app.get("/sair", response_class=HTMLResponse)(sair)


_EV_OK = re.compile(r"^[A-Za-z0-9_]{1,32}$")


@app.post("/api/evento")
async def evento(req: Request):
    """Contador próprio de eventos das páginas (o Meta não recebe eventos personalizados de sites na categoria Religião).
    Cada sessão conta cada evento uma vez por página. Não guarda IP nem dado pessoal."""
    try:
        j = json.loads((await req.body())[:2000] or b"{}")
        s_, e_, p_ = str(j.get("s", ""))[:40], str(j.get("e", "")), str(j.get("p", ""))[:32]
        if not (_EV_OK.match(e_) and re.match(r"^[A-Za-z0-9_-]{8,40}$", s_) and re.match(r"^[A-Za-z0-9_-]{0,32}$", p_)):
            return {"ok": False}
        with db() as c:
            c.execute("INSERT OR IGNORE INTO eventos VALUES(?,?,?,?,?)", (s_, e_, p_, str(j.get("src", ""))[:40], agora()))
    except Exception:
        return {"ok": False}
    return {"ok": True}


@app.get("/health")
def health():
    with db() as c:
        fila = c.execute("SELECT COUNT(*) FROM compras WHERE status IN ('na_fila','gerando')").fetchone()[0]
    return {"ok": True, "fila": fila}


def _produtos_no_payload(p):
    """Junta todos os nomes de produto do webhook (produto principal e order bumps, se vierem juntos)."""
    nomes = []
    def andar(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(v, str) and (k == "product_name" or (k == "name" and "product_id" in x)):
                    nomes.append(v)
                andar(v)
        elif isinstance(x, list):
            for v in x:
                andar(v)
    andar(p)
    return list(dict.fromkeys(nomes))


def _sem_acento(t):
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(ch) != "Mn")


def _sku(nome):
    n = _sem_acento(nome)
    for sku, chave in (("biblioteca", "PRODUTO_BIBLIOTECA"), ("promessa_filhos", "PRODUTO_PROMESSA_FILHOS"), ("promessa_jejum", "PRODUTO_PROMESSA_JEJUM"), ("casa", "PRODUTO_CASA"), ("promessa", "PRODUTO_PROMESSA"), ("enfermo_santo", "PRODUTO_ENFERMO_SANTO"), ("enfermo_cartoes", "PRODUTO_ENFERMO_CARTOES"), ("enfermo", "PRODUTO_ENFERMO"), ("consagracao", "PRODUTO_CONSAGRACAO"), ("livro_familia", "PRODUTO_LIVRO_FAMILIA"), ("clube", "PRODUTO_CLUBE"), ("santo_urgente", "PRODUTO_SANTO_URGENTE"), ("santo_noite", "PRODUTO_SANTO_NOITE"), ("santo_cal", "PRODUTO_SANTO_CAL"), ("santo_familia", "PRODUTO_SANTO_FAMILIA"), ("santo", "PRODUTO_SANTO"), ("taro_amor", "PRODUTO_TARO_AMOR"), ("taro_ano", "PRODUTO_TARO_ANO"), ("taro", "PRODUTO_TARO"), ("ritual", "PRODUTO_RITUAL"), ("deusa", "PRODUTO_DEUSA"), ("numero", "PRODUTO_NUMERO"), ("casal", "PRODUTO_CASAL"), ("ano", "PRODUTO_ANO"), ("natal", "PRODUTO_NATAL")):
        if any(alt.strip() and _sem_acento(alt.strip()) in n for alt in CFG[chave].split("|")):  # aceita nomes alternativos: "a|b"
            return sku
    return None


@app.post("/webhook/kiwify/{segredo}")
async def webhook(segredo: str, request: Request):
    if not CFG["WEBHOOK_SEGREDO"] or not hmac.compare_digest(segredo, CFG["WEBHOOK_SEGREDO"]):
        raise HTTPException(404)
    bruto = await request.body()
    (LOGS / f"webhook-{int(time.time()*1000)}.json").write_bytes(bruto)  # guarda o original para conferência
    assinatura = request.query_params.get("signature")
    if CFG["KIWIFY_TOKEN"] and assinatura:
        tokens = [t.strip() for t in CFG["KIWIFY_TOKEN"].split(",") if t.strip()]
        if not any(hmac.compare_digest(hmac.new(t.encode(), bruto, hashlib.sha1).hexdigest(), assinatura) for t in tokens):
            log.warning("assinatura inválida no webhook"); raise HTTPException(401)
    p = json.loads(bruto or b"{}")
    status = (p.get("order_status") or p.get("webhook_event_type") or p.get("status") or "").lower()
    cust = p.get("Customer") or p.get("customer") or {}
    email = (cust.get("email") or p.get("email") or "").strip().lower()  # carrinho abandonado vem com o e-mail solto
    pedido = str(p.get("order_id") or p.get("order_ref") or "")
    if not email:
        log.warning("webhook sem e-mail: %s", bruto[:300]); return {"ok": True, "ignorado": "sem email"}
    nomes_produtos = _produtos_no_payload(p)
    if _casamento.eh_casamento(nomes_produtos):  # O Santo do Nosso Casamento (e os bumps dele): tabelas e e-mails próprios (casamento.py)
        try:
            _casamento.evento_kiwify(p, status, email, nomes_produtos)
        except Exception:
            log.exception("casamento: webhook falhou para %s", email); alerta_admin("Casamento: webhook falhou", traceback.format_exc())
            raise HTTPException(500)  # a Kiwify manda de novo; o evento_kiwify pode rodar duas vezes sem duplicar
        nomes_produtos = [n for n in nomes_produtos if not _casamento.eh_casamento([n])]
        if not nomes_produtos:
            return {"ok": True}
    if _folego.eh_folego(nomes_produtos):  # Fôlego: outro nicho, outro banco, outros e-mails (folego.py)
        _folego.tabelas()
        return _folego.evento_kiwify(p, status, email)
    skus = [s for s in map(_sku, nomes_produtos) if s]
    log.info("webhook %s %s pedido=%s produtos=%s", status, email, pedido, skus)
    if "clube" in skus:  # assinatura: tem eventos próprios (renovada, atrasada, cancelada)
        try:
            import clube
            clube.evento(p.get("webhook_event_type") or status, email, cust.get("first_name") or cust.get("full_name") or cust.get("name"), p)
        except Exception:
            log.exception("clube: evento falhou para %s", email)
        skus = [x for x in skus if x != "clube"]
        if not skus:
            return {"ok": True}
    if status in ("paid", "approved", "order_approved", "compra_aprovada"):
        cli = cliente(email, cust.get("full_name") or cust.get("name"))
        if "biblioteca" in skus:  # libera os 5 produtos; o que a pessoa já tem (comprado antes, não reembolsado) não é gerado de novo
            ja = {x["sku"] for x in compras_de(email) if x["status"] != "reembolsado"}
            skus = list(dict.fromkeys([x for x in skus if x != "biblioteca"] + [x for x in BIBLIOTECA if x not in ja]))
            log.info("biblioteca %s: libera %s (já tinha %s)", email, skus, sorted(ja & set(BIBLIOTECA)))
        if "livro_familia" in skus and "santo" not in skus and CFG["FAMILIA_BONUS_SANTO"] == "1":  # bônus: o devocionário de quem comprou
            if "santo" not in {x["sku"] for x in compras_de(email) if x["status"] != "reembolsado"}:
                skus.append("santo"); log.info("familia %s: + devocionário de bônus", email)
        with _lock, db() as c:
            for s in skus:
                c.execute("INSERT OR IGNORE INTO compras(email,sku,pedido,status,criado,atualizado) VALUES(?,?,?,?,?,?)",
                          (email, s, pedido, "aguardando_dados", agora(), agora()))
        if "santo" in skus:
            try:
                _dados_do_quiz(email, p, cust)
            except Exception:
                log.exception("quiz automático falhou para %s", email)
        liberar_fila(email)
        with _lock, db() as c:  # comprou: cancela os avisos pendentes e marca como recuperado quem voltou pelo e-mail
            c.execute("UPDATE recuperacao SET status='pago' WHERE email=? AND status='pendente'", (email,))
            c.execute("UPDATE recuperacao SET status='recuperado' WHERE email=? AND status='enviado' AND enviado>=?",
                      (email, (dt.datetime.now() - dt.timedelta(days=3)).isoformat(timespec="seconds")))
    elif status in ("waiting_payment", "pix_created", "pix_gerado", "billet_created", "boleto_gerado") and \
            (str(p.get("payment_method") or "pix").lower() == "pix" or "pix" in status):
        registrar_recuperacao("pix", email, cust.get("full_name") or cust.get("name"), skus, pedido, p.get("checkout_link"))
    elif status in ("refused", "order_rejected", "compra_recusada"):
        registrar_recuperacao("recusado", email, cust.get("full_name") or cust.get("name"), skus, pedido, p.get("checkout_link"))
    elif status in ("abandoned", "abandoned_cart", "carrinho_abandonado"):
        registrar_recuperacao("carrinho", email, p.get("name") or cust.get("name"), skus, pedido, p.get("checkout_link"))
    elif status in ("refunded", "chargedback", "chargeback", "order_refunded", "compra_reembolsada"):
        with _lock, db() as c:
            c.execute("UPDATE compras SET status='reembolsado', atualizado=? WHERE email=? AND pedido=? AND status!='enviado'",
                      (agora(), email, pedido))
    return {"ok": True}


def _dados_do_quiz(email, p, cust):
    """A página do quiz manda o aniversário no link do checkout (s1=dDDMM) e um id do quiz (s2).
    Se veio, o devocionário sai sozinho, sem a cliente precisar preencher a página /dados."""
    if CFG["QUIZ_AUTO"] != "1":
        return
    tp = p.get("TrackingParameters") or p.get("tracking_parameters") or {}
    m = re.fullmatch(r"d(\d{2})(\d{2})", str(tp.get("s1") or "").strip())
    qid = str(tp.get("s2") or "")
    if not m:  # a Kiwify sempre repassa o sck: lá vai "q<id>d<DDMM>"
        k = re.fullmatch(r"q([a-z0-9]{6,40})d(\d{2})(\d{2})", str(tp.get("sck") or p.get("sck") or "").strip())
        if not k:
            return
        qid, m = k.group(1), re.fullmatch(r"d(\d{2})(\d{2})", f"d{k.group(2)}{k.group(3)}")
    cli = cliente(email)
    dados = json.loads(cli["dados"]) if cli["dados"] else {}
    if dados.get("santo"):
        return
    qz = {}
    if qid:
        with db() as c:
            r = c.execute("SELECT dados FROM quiz WHERE id=?", (qid[:40],)).fetchone()
        qz = json.loads(r["dados"]) if r else {}
    nome = qz.get("nome") or (cust.get("first_name") or (cust.get("full_name") or cust.get("name") or cli["nome"] or "").split(" ")[0])
    sz = _validar_santo({"nome": (nome or "Amigo").strip().title(), "dia": int(m.group(1)), "mes": int(m.group(2)),
                         "intencao": qz.get("intencao"), "momento": qz.get("momento"), "pedido": qz.get("pedido")})
    sz["origem"] = "quiz"
    dados["santo"] = sz
    with _lock, db() as c:
        c.execute("UPDATE clientes SET dados=?, atualizado=? WHERE email=?", (json.dumps(dados, ensure_ascii=False), agora(), email))
    log.info("quiz %s: devocionário com a data do quiz (%s/%s)", email, sz["dia"], sz["mes"])


@app.post("/api/quiz")
async def api_quiz(req: Request):
    """Guarda as respostas do quiz (primeiro nome, aniversário, intenção, pedido) pelo id que vai no checkout (s2)."""
    try:
        j = json.loads((await req.body())[:3000] or b"{}")
        qid = str(j.get("id") or "")
        if not re.fullmatch(r"[A-Za-z0-9]{6,40}", qid):
            return {"ok": False}
        d = {k: str(j.get(k) or "")[:300] for k in ("nome", "intencao", "momento", "pedido")}
        d["nome"] = d["nome"][:40]
        with _lock, db() as c:
            c.execute("INSERT OR REPLACE INTO quiz VALUES(?,?,?)", (qid, json.dumps(d, ensure_ascii=False), agora()))
            c.execute("DELETE FROM quiz WHERE criado < ?", ((dt.datetime.now() - dt.timedelta(days=30)).isoformat(timespec="seconds"),))
    except Exception:
        return {"ok": False}
    return {"ok": True}


@app.post("/email/entrada/{segredo}")
async def email_entrada(segredo: str, request: Request):
    """Recebe o e-mail cru que o Email Worker do Cloudflare repassa (contato@meusantoprotetor.online) e responde com a IA em segundo plano."""
    if not CFG["SUPORTE_SEGREDO"] or not hmac.compare_digest(segredo, CFG["SUPORTE_SEGREDO"]):
        raise HTTPException(404)
    bruto = await request.body()
    import suporte_ia
    threading.Thread(target=suporte_ia.processar, args=(bruto,), daemon=True).start()
    return {"ok": True}


@app.get("/api/cidades")
def cidades(q: str = ""):
    import calc
    return calc.sugerir_cidades(q[:60])


@app.get("/api/cliente")
def api_cliente(t: str):
    with db() as c:
        r = c.execute("SELECT * FROM clientes WHERE token=?", (t,)).fetchone()
    if not r:
        raise HTTPException(404, "Link inválido")
    return {"email": r["email"], "nome": r["nome"], "dados": json.loads(r["dados"]) if r["dados"] else None,
            "produtos": [x["sku"] for x in compras_de(r["email"]) if x["status"] != "reembolsado"]}


def _validar_pessoa(p, quem):
    rot = {"p1": ("seu nome", "sua data de nascimento", "sua hora de nascimento", "sua cidade de nascimento"),
           "p2": ("o nome da outra pessoa", "a data de nascimento da outra pessoa", "a hora de nascimento da outra pessoa",
                  "a cidade de nascimento da outra pessoa")}[quem]
    import calc
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = (p.get("nome") or "").strip()[:60]
    if len(nome) < 2:
        raise HTTPException(400, f"Informe {rot[0]}")
    try:
        d, m, y = map(int, (p.get("data") or "").split("/")); dt.date(y, m, d)
        assert 1900 < y <= dt.date.today().year
    except Exception:
        raise HTTPException(400, f"Confira {rot[1]} (use dd/mm/aaaa)")
    hora = (p.get("hora") or "").strip()
    if hora and not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", hora):
        raise HTTPException(400, f"Confira {rot[2]} (use hh:mm)")
    c = calc.buscar_cidade(p.get("cidade") or "")
    if not c:
        raise HTTPException(400, f"Não encontramos {rot[3]}. Escolha uma das sugestões da lista.")
    return {"nome": nome, "data": f"{d:02d}/{m:02d}/{y}", "hora": hora or None, "cidade": f'{c["name"]} - {c["uf"]}'}


def _validar_num(p):
    """Numerologia: nome completo de registro + data. Não precisa de hora nem cidade."""
    import numerologia
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join((p.get("nome") or "").split())[:100]
    if len(nome.split()) < 2:
        raise HTTPException(400, "Informe seu nome completo (como está na certidão de nascimento)")
    try:
        d, m, y = map(int, (p.get("data") or "").split("/")); dt.date(y, m, d)
        assert 1900 < y <= dt.date.today().year
        numerologia.calcular(nome, f"{d:02d}/{m:02d}/{y}")
    except Exception:
        raise HTTPException(400, "Confira sua data de nascimento (use dd/mm/aaaa)")
    return {"nome": nome, "data": f"{d:02d}/{m:02d}/{y}"}


def _validar_taro(p):
    """Tarô: primeiro nome + as 7 cartas que a pessoa tirou + tema, pergunta e momento (opcionais)."""
    import tarot
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(nome) < 2:
        raise HTTPException(400, "Informe o seu nome")
    try:
        cartas = tarot.validar_tiragem(p.get("cartas") or [])
    except Exception:
        raise HTTPException(400, "Tire as suas 7 cartas")
    return {"nome": nome, "cartas": cartas,
            "area": p.get("area") if p.get("area") in tarot.AREAS else "",
            "momento": p.get("momento") if p.get("momento") in tarot.MOMENTOS else "",
            "pergunta": " ".join(str(p.get("pergunta") or "").split())[:400]}


def _validar_santo(p):
    """Meu Santo Protetor: primeiro nome + dia e mês de nascimento + intenção, momento e pedido (opcionais)."""
    import santos
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(nome) < 2:
        raise HTTPException(400, "Informe o seu nome")
    try:
        dia, mes = santos.validar_data(p.get("dia"), p.get("mes"))
    except Exception:
        raise HTTPException(400, "Informe o dia e o mês do seu nascimento")
    return {"nome": nome, "dia": dia, "mes": mes,
            "intencao": p.get("intencao") if p.get("intencao") in santos.INTENCOES else "",
            "momento": p.get("momento") if p.get("momento") in santos.MOMENTOS else "",
            "pedido": " ".join(str(p.get("pedido") or "").split())[:300]}


def _validar_santo_familia(lista):
    import santos
    if not isinstance(lista, list):
        raise HTTPException(400, "Dados da família incompletos")
    out = []
    for i, x in enumerate(lista[:4]):
        if not isinstance(x, dict) or not str(x.get("nome") or "").strip():
            continue
        nome = " ".join(str(x["nome"]).split())[:40]
        try:
            dia, mes = santos.validar_data(x.get("dia"), x.get("mes"))
        except Exception:
            raise HTTPException(400, f"Confira o dia e o mês de nascimento de {nome}")
        out.append({"nome": nome, "dia": dia, "mes": mes, "relacao": x.get("relacao") if x.get("relacao") in santos.RELACOES else "outro"})
    return out


def _validar_promessa(p):
    """Meu Versículo: primeiro nome + dia e mês do aniversário + pedido (opcional) + filhos (bump) + propósitos do jejum (bump)."""
    import santos
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(nome) < 2:
        raise HTTPException(400, "Informe o seu nome")
    import casa as K
    pessoas = []
    for x in (p.get("pessoas") or [])[:8]:
        if isinstance(x, dict) and str(x.get("nome") or "").strip():
            pessoas.append({"nome": " ".join(str(x["nome"]).split())[:40], "relacao": x.get("relacao") if x.get("relacao") in K.RELACOES and x.get("relacao") != "eu" else "outro"})
    dia = mes = None
    if p.get("dia") or p.get("mes") or not pessoas and p.get("exige_data"):
        try:
            dia, mes = santos.validar_data(p.get("dia"), p.get("mes"))
        except Exception:
            raise HTTPException(400, "Informe o dia e o mês do seu aniversário")
    if p.get("exige_pessoas") and not pessoas:
        raise HTTPException(400, "Coloque pelo menos uma pessoa da sua casa")
    filhos = [" ".join(str(x).split())[:40] for x in (p.get("filhos") or []) if str(x).strip()][:8]
    props = [" ".join(str(x).split())[:120] for x in (p.get("propositos") or []) if str(x).strip()][:3]
    if not filhos:  # bump dos filhos: aproveita os filhos/netos que a pessoa já colocou na casa
        filhos = [x["nome"] for x in pessoas if x["relacao"] in ("filho", "filha", "neto", "neta")]
    out = {"nome": nome, "pedido": " ".join(str(p.get("pedido") or "").split())[:300], "filhos": filhos, "propositos": props, "pessoas": pessoas}
    if dia:
        out.update(dia=dia, mes=mes)
    return out


def _validar_enfermo(p):
    """Rezo por Você: quem reza + nome do doente + relação + situação + pedido (opcional) + nascimento do doente (só para o bump do santo)."""
    import enfermo as ef, santos
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    quem = " ".join(str(p.get("quem") or "").split())[:60]
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(quem) < 2:
        raise HTTPException(400, "Informe o seu nome")
    if len(nome) < 2:
        raise HTTPException(400, "Informe o nome de quem está doente")
    out = {"quem": quem, "nome": nome, "relacao": p.get("relacao") if p.get("relacao") in ef.RELACOES else "outro",
           "situacao": p.get("situacao") if p.get("situacao") in ef.SITUACOES else "outro",
           "pedido": " ".join(str(p.get("pedido") or "").split())[:300]}
    if p.get("dia") or p.get("mes"):
        try:
            out["dia"], out["mes"] = santos.validar_data(p.get("dia"), p.get("mes"))
        except Exception:
            raise HTTPException(400, f"Confira o dia e o mês de nascimento de {nome.split()[0]}")
    return out


def _validar_consagracao(p):
    """Consagração: primeiro nome + intenção + pedido (opcionais) + festa escolhida (opcional; vazio = a próxima)."""
    import consagracao as cg
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(nome) < 2:
        raise HTTPException(400, "Informe o seu nome")
    f = str(p.get("festa") or "")
    f = f if cg.por_id(f) and cg.escolher(f)["id"] == f else ""
    return {"nome": nome, "intencao": p.get("intencao") if p.get("intencao") in cg.INTENCOES else "",
            "pedido": " ".join(str(p.get("pedido") or "").split())[:300], "festa": f}


def _validar_livro_familia(p):
    """Livro da família: sobrenome (opcional) + de 1 a 8 pessoas (nome, relação, dia e mês) + intenções e pedido."""
    import santos, oracoes_familia as of
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    pessoas = []
    for x in (p.get("pessoas") or [])[:8]:
        if not isinstance(x, dict) or not str(x.get("nome") or "").strip():
            continue
        nome = " ".join(str(x["nome"]).split())[:40]
        try:
            dia, mes = santos.validar_data(x.get("dia"), x.get("mes"))
        except Exception:
            raise HTTPException(400, f"Confira o dia e o mês de nascimento de {nome}")
        pessoas.append({"nome": nome, "dia": dia, "mes": mes, "relacao": x.get("relacao") if x.get("relacao") in of.RELACOES else "outro"})
    if not pessoas:
        raise HTTPException(400, "Coloque pelo menos uma pessoa da família")
    sob = " ".join(re.sub(r"[^\w\s'-]", "", str(p.get("sobrenome") or "")).split())[:30]
    return {"sobrenome": sob, "pessoas": pessoas, "intencoes": [i for i in (p.get("intencoes") or []) if i in of.INTENCOES][:5],
            "pedido": " ".join(str(p.get("pedido") or "").split())[:300]}


def _validar_deusas(p):
    """Mapa das 7 Deusas: primeiro nome + as 12 respostas do teste (0 a 3) + foco/momento opcionais."""
    import deusas
    if not isinstance(p, dict):
        raise HTTPException(400, "Dados incompletos")
    nome = " ".join(str(p.get("nome") or "").split())[:60]
    if len(nome) < 2:
        raise HTTPException(400, "Informe o seu nome")
    try:
        resp = [int(x) for x in p.get("respostas") or []]
        deusas.calcular(nome, resp)
    except Exception:
        raise HTTPException(400, "Responda todas as perguntas do teste")
    c = p.get("contexto") if isinstance(p.get("contexto"), dict) else {}
    ctx = {k: c[k] for k, ok in (("foco", deusas.FOCOS), ("momento", deusas.MOMENTOS)) if c.get(k) in ok}
    return {"nome": nome, "respostas": resp, "contexto": ctx}


CONTEXTO_VALORES = {"foco": {"amor", "carreira", "emocoes", "eu"},
                    "momento": {"intenso", "travado", "tranquilo", "dificil"},
                    "amor": {"solteiro", "relacionamento", "complicado", "reservado"},
                    "perfil": {"sente", "pensa", "cuida", "cobra"}}


def _validar_contexto(x):
    """Respostas pessoais do quiz. Só aceita os valores conhecidos; o resto é descartado."""
    if not isinstance(x, dict):
        return {}
    return {k: x[k] for k, ok in CONTEXTO_VALORES.items() if isinstance(x.get(k), str) and x[k] in ok}


@app.post("/api/dados")
async def api_dados(request: Request):
    b = await request.json()
    email = None
    if b.get("t"):
        with db() as c:
            r = c.execute("SELECT email FROM clientes WHERE token=?", (b["t"],)).fetchone()
        email = r["email"] if r else None
    email = email or (b.get("email") or "").strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""):
        raise HTTPException(400, "Informe o mesmo e-mail usado na compra")
    novos = {}
    if b.get("num"):
        novos["num"] = _validar_num(b["num"])
    if b.get("deusas"):
        novos["deusas"] = _validar_deusas(b["deusas"])
    if b.get("taro"):
        novos["taro"] = _validar_taro(b["taro"])
    if b.get("consagracao"):
        novos["consagracao"] = _validar_consagracao(b["consagracao"])
    if b.get("livro_familia"):
        novos["livro_familia"] = _validar_livro_familia(b["livro_familia"])
    if b.get("enfermo"):
        novos["enfermo"] = _validar_enfermo(b["enfermo"])
    if b.get("promessa"):
        novos["promessa"] = _validar_promessa(b["promessa"])
    if b.get("santo"):
        novos["santo"] = _validar_santo(b["santo"])
        fam = _validar_santo_familia(b.get("santo_familia") or [])
        if fam:
            novos["santo_familia"] = {"pessoas": fam}
    if b.get("p1") or not novos:
        novos["p1"] = _validar_pessoa(b.get("p1"), "p1")
        if b.get("p2") and (b["p2"].get("nome") or b["p2"].get("data")):
            novos["p2"] = _validar_pessoa(b["p2"], "p2")
    nome_cli = (({"nome": novos["enfermo"]["quem"]} if novos.get("enfermo") else None) or novos.get("promessa") or novos.get("p1") or novos.get("num") or novos.get("deusas") or novos.get("taro") or novos.get("santo") or novos.get("consagracao")
                or {"nome": (novos.get("livro_familia") or {"pessoas": [{"nome": ""}]})["pessoas"][0]["nome"]})["nome"]
    cli = cliente(email, nome_cli)
    anterior = json.loads(cli["dados"]) if cli["dados"] else {}
    dados = {**anterior, **novos}  # quem comprou numerologia e mapa não perde um ao enviar o outro
    ctx = _validar_contexto(b.get("contexto")) or anterior.get("contexto") or {}
    if ctx:
        dados["contexto"] = ctx
    acomp = secrets.token_urlsafe(18)
    with _lock, db() as c:
        c.execute("UPDATE clientes SET dados=?, nome=COALESCE(nome, ?), atualizado=? WHERE email=?",
                  (json.dumps(dados, ensure_ascii=False), nome_cli, agora(), email))
        c.execute("INSERT INTO acompanhamento(token,email,desde) VALUES(?,?,?)", (acomp, email, agora()))
    liberar_fila(email)
    compras = compras_de(email)
    falta_p2 = any(x["sku"] == "casal" and x["status"] == "aguardando_dados" for x in compras) and "p2" not in dados
    return {"ok": True, "pagamento_confirmado": bool(compras), "falta_p2": falta_p2, "acompanhar": acomp,
            "produtos": [{"sku": x["sku"], "status": x["status"]} for x in compras]}


@app.get("/api/acompanhar")
def acompanhar(a: str):
    """Andamento dos PDFs para a página /dados mostrar o botão de baixar.
    Só mostra PDFs gerados DEPOIS do envio que criou este token (quem preencheu os dados vê o que foi gerado com eles)."""
    with db() as c:
        r = c.execute("SELECT * FROM acompanhamento WHERE token=?", (a,)).fetchone()
    if not r or r["desde"] < (dt.datetime.now() - dt.timedelta(days=2)).isoformat(timespec="seconds"):
        raise HTTPException(404, "Link expirado")
    cli = cliente(r["email"])
    dados = json.loads(cli["dados"]) if cli["dados"] else {}
    itens = []
    for x in compras_de(r["email"]):
        st = x["status"]
        if st == "reembolsado" or (st == "enviado" and (x["atualizado"] or "") < r["desde"]):
            continue
        item = {"sku": x["sku"], "nome": NOMES_PRODUTO[x["sku"]]}
        if st == "enviado":
            api = _marca(x["sku"])["api"]
            item.update(status="pronto", baixar=f'{api}/baixar/{x["baixar"]}')
            if x["sku"] in ("deusa", "santo") and x["arquivo"] and _papel_de_parede(x["arquivo"]).exists():
                item["papel"] = f'{api}/baixar/{x["baixar"]}/papel-de-parede'
        elif st == "erro":
            item["status"] = "erro"
        elif st == "aguardando_dados" and not dados_completos(dados, x["sku"]):
            item["status"] = "falta_p2" if x["sku"] == "casal" else "falta_dados"
        else:
            item["status"] = "preparando"
        itens.append(item)
    out = {"pagamento_confirmado": bool(compras_de(r["email"])), "itens": itens}
    sz = dados.get("santo") or {}
    if sz.get("dia") and any(i["sku"] == "livro_familia" and i["status"] == "falta_dados" for i in itens):
        # comprou o livro junto com o devocionário: a página /dados-familia já abre com a pessoa e a família que ela informou
        fam = (dados.get("santo_familia") or {}).get("pessoas") or []
        out["previa_familia"] = {"pessoas": ([{"nome": sz["nome"].split()[0], "dia": sz["dia"], "mes": sz["mes"], "relacao": "eu"}] +
                                             [{"nome": x["nome"].split()[0], "dia": x["dia"], "mes": x["mes"], "relacao": x.get("relacao")} for x in fam])[:8]}
    return out


@app.get("/baixar/{tok}/papel-de-parede")
def baixar_papel(tok: str):
    with db() as c:
        r = c.execute("SELECT arquivo FROM compras WHERE baixar=?", (tok,)).fetchone()
    png = _papel_de_parede(r["arquivo"]) if r and r["arquivo"] else None
    if not png or not png.exists():
        raise HTTPException(404, "Arquivo não encontrado")
    return FileResponse(png, media_type="image/png", filename=png.name.split("-", 1)[1])


@app.get("/baixar/{tok}")
def baixar(tok: str):
    with db() as c:
        r = c.execute("SELECT arquivo FROM compras WHERE baixar=?", (tok,)).fetchone()
    if not r or not r["arquivo"] or not pathlib.Path(r["arquivo"]).exists():
        raise HTTPException(404, "Arquivo não encontrado")
    arq = pathlib.Path(r["arquivo"])
    return FileResponse(arq, media_type="application/zip" if arq.suffix == ".zip" else "application/pdf", filename=arq.name.split("-", 1)[1])


def _admin(chave):
    if not CFG["ADMIN_CHAVE"] or not hmac.compare_digest(chave or "", CFG["ADMIN_CHAVE"]):
        raise HTTPException(404)


@app.get("/admin")
def admin(chave: str = ""):
    _admin(chave)
    with db() as c:
        rows = [dict(r) for r in c.execute("SELECT id,email,sku,pedido,status,tentativas,erro,criado,atualizado FROM compras ORDER BY id DESC LIMIT 100")]
        resumo = {r[0]: r[1] for r in c.execute("SELECT status, COUNT(*) FROM compras GROUP BY status")}
    return JSONResponse({"resumo": resumo, "compras": rows})


@app.post("/admin/reenviar")
def reenviar(chave: str = "", id: int = 0):
    _admin(chave)
    with _lock, db() as c:
        c.execute("UPDATE compras SET status='na_fila', tentativas=0, erro=NULL, atualizado=? WHERE id=?", (agora(), id))
    return {"ok": True}


# ------------------------------------------------------------------ prévia grátis do quiz
@app.get("/api/previa")
def previa(data: str, cidade: str, hora: str = ""):
    """Sol, Lua e Ascendente reais para o resultado do quiz (sem IA, só cálculo)."""
    import calc
    try:
        d, m, y = map(int, data.split("/")); dt.date(y, m, d)
        h, mi = (None, None)
        if hora:
            h, mi = map(int, hora.split(":"))
        mp = calc.calcular("Prévia", y, m, d, h, mi, cidade[:60])
    except Exception:
        raise HTTPException(400, "Dados inválidos")
    pl = {p["planeta"]: p for p in mp["planetas"]}
    return {"sol": pl["Sol"]["signo"], "lua": pl["Lua"]["signo"], "lua_alternativa": mp["lua_alternativa"],
            "asc": mp["ascendente"]["signo"] if mp["ascendente"] else None,
            "elemento_dominante": mp["elemento_dominante"], "cidade": mp["cidade"].split(" (")[0]}



@app.get("/api/previa_ano")
def previa_ano(data: str, cidade: str, hora: str = ""):
    """Prévia grátis do 'Seu 2027': trânsito mais forte, Júpiter, eclipse que toca o mapa e mês mais ativo."""
    import calc, ano
    try:
        d, m, y = map(int, data.split("/")); dt.date(y, m, d)
        h, mi = (None, None)
        if hora:
            h, mi = map(int, hora.split(":"))
        mp = calc.calcular("Prévia", y, m, d, h, mi, cidade[:60])
        a = ano.calcular_ano(mp)
    except Exception:
        raise HTTPException(400, "Dados inválidos")
    pl = {p["planeta"]: p for p in mp["planetas"]}
    top = [{"transito": t["transito"], "periodos": t["periodos"]} for t in a["principais"][:3]]
    ecl = next((e for e in a["eclipses"] if e["toca"]), None) or next((e for e in a["eclipses"] if "total" in e["tipo"]), a["eclipses"][0] if a["eclipses"] else None)
    meses = sorted(a["por_mes"].items(), key=lambda kv: -len(kv[1]))
    jup = a["jupiter_saturno"]["Júpiter"]
    return {"sol": pl["Sol"]["signo"], "asc": mp["ascendente"]["signo"] if mp["ascendente"] else None,
            "transitos": top, "total_transitos": len(a["principais"]) + len(a["outros"]),
            "eclipse": ({"data": ecl["data"], "tipo": ecl["tipo"], "signo": ecl["signo"], "casa": ecl["casa"],
                         "toca": ecl["toca"][:2]} if ecl else None),
            "mes_mais_ativo": meses[0][0] if meses and meses[0][1] else None,
            "jupiter": [{"signo": j["signo"], "casa": j["casa"], "de": j["de"], "ate": j["ate"]} for j in jup],
            "eclipses_total": len(a["eclipses"])}
