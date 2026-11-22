"""Teste ponta a ponta do O Santo do Nosso Casamento com o servidor.py de verdade (v19 + ganchos).

Uso (fora da VPS, numa pasta qualquer):
  pip install fastapi httpx anthropic
  python testes/teste_casamento.py
Monta uma cópia do servidor numa pasta temporária, com um santos.py de mentira, MOCK_IA=1 e sem Resend
(os e-mails vão para dados/emails_teste). Precisa de um Chromium para o PDF (CASAMENTO_CHROME ou Playwright).
"""
import json, os, pathlib, shutil, sqlite3, sys, tempfile, time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="casamento-teste-"))
for f in (RAIZ / "servidor").glob("*.py"):
    shutil.copy(f, TMP / f.name)
shutil.copytree(RAIZ / "servidor" / "casamento_fontes", TMP / "casamento_fontes")
shutil.copy(RAIZ / "testes" / "santos_stub.py", TMP / "santos.py")
V19 = pathlib.Path(os.environ.get("V19_DIR", "/nao-existe"))  # pasta com o folego.py e o clube.py da VPS (opcional)
for nome in ("folego.py", "clube.py"):  # módulos do v19 que o servidor importa; sem a pasta, entra uma versão vazia
    if (V19 / nome).exists():
        shutil.copy(V19 / nome, TMP / nome)
    elif not (TMP / nome).exists():
        (TMP / nome).write_text("from fastapi import APIRouter\nrouter = APIRouter()\n"
                                "def tabelas(): pass\ndef iniciar(): pass\ndef eh_folego(n): return False\n")
os.environ.update({"WEBHOOK_SEGREDO": "segredo", "CASAMENTO_CHECKOUT": "AbCdEf1", "MOCK_IA": "1", "RESEND_API_KEY": "",
                   "SITE_URL_SANTO": "https://meusantoprotetor.online", "QUIZ_AUTO": "1"})
os.environ.setdefault("CASAMENTO_PDF_MOTOR", "chromium")
sys.path.insert(0, str(TMP)); os.chdir(TMP)

from fastapi.testclient import TestClient  # noqa: E402
import servidor  # noqa: E402
import casamento  # noqa: E402

OK = []


def confere(cond, msg):
    print(("✔ " if cond else "✘ ") + msg)
    OK.append(cond)
    if not cond:
        raise SystemExit(f"FALHOU: {msg}")


def kiwify(cli, evento, order, email, produtos, sck=None, status=None, metodo="pix"):
    p = {"order_id": order, "order_status": status or {"order_approved": "paid", "pix_created": "waiting_payment", "order_refunded": "refunded",
                                                       "order_rejected": "refused"}.get(evento, evento),
         "webhook_event_type": evento, "payment_method": metodo,
         "Product": {"product_id": "p1", "product_name": produtos[0]},
         "Customer": {"full_name": "Maria Teste", "first_name": "Maria", "email": email},
         "Commissions": {"charge_amount": 3790}, "TrackingParameters": {"sck": sck} if sck else {}}
    if len(produtos) > 1:
        p["order_bumps"] = [{"product_id": f"b{i}", "name": n} for i, n in enumerate(produtos[1:])]
    r = cli.post("/webhook/kiwify/segredo", json=p)
    confere(r.status_code == 200, f"webhook {evento} {produtos[0][:30]} → {r.status_code}")
    return r


def espera_fase(order, fase, seg=90):
    t0 = time.time()
    while time.time() - t0 < seg:
        with servidor.db() as c:
            r = c.execute("SELECT fase, erro FROM casamento_compras WHERE order_id=?", (order,)).fetchone()
        if r and r["fase"] == fase:
            return True
        if r and r["fase"] == "erro":
            print("erro:", r["erro"]); return False
        time.sleep(1)
    return False


PEDIDO = {"modo": "nos", "quem": "ela", "ela": {"nome": "ana maria", "dia": 5, "mes": 3}, "ele": {"nome": "JOSÉ", "dia": 19, "mes": 3},
          "casamento": {"dia": 13, "mes": 6, "ano": 1998}, "igreja": "sim", "pedidos": ["paciencia", "fe", "xx"], "pedido": "Que o José volte a rezar comigo."}

with TestClient(servidor.app) as cli:
    # 1. revelação grátis
    r = cli.get("/api/casamento/santos?d=1306,0503,2512")
    s = r.json()["santos"]
    confere(r.status_code == 200 and s[0]["nome"] == "Santo Antônio" and s[2]["festa"] is True and s[0]["festa"] is False, "santos do dia (e Natal = festa)")
    confere(cli.get("/api/casamento/santos?d=3102").status_code == 400, "data impossível recusada")
    # 2. pedido do quiz
    confere(cli.post("/api/casamento/pedido", json={"pedido": {**PEDIDO, "ela": {"nome": ""}}}).status_code == 400, "pedido sem nome recusado")
    confere(cli.post("/api/casamento/pedido", json={"pedido": {**PEDIDO, "casamento": {"dia": 1, "mes": 1, "ano": 2999}}}).status_code == 400, "casamento no futuro recusado")
    r = cli.post("/api/casamento/pedido", json={"pedido": PEDIDO, "origem": {"utm_source": "fb", "utm_campaign": "c1", "lixo": "x"}})
    ref, url = r.json()["ref"], r.json()["url"]
    confere(r.status_code == 200 and url.startswith("https://pay.kiwify.com.br/AbCdEf1?sck=" + ref) and "utm_source=fb" in url and "lixo" not in url,
            f"checkout com sck e utm ({url})")
    ped = casamento._pedido(ref)
    confere(ped["ela"]["nome"] == "Ana Maria" and ped["ele"]["nome"] == "José" and ped["pedidos"] == ["paciencia", "fe"], "nomes e pedidos normalizados")
    confere(cli.get(f"/api/casamento/status?ref={ref}").json() == {"pago": False}, "status antes de pagar")
    # 3. Pix gerado e depois pago, com os 2 bumps no mesmo aviso
    kiwify(cli, "pix_created", "K1", "maria@teste.com", ["O Santo do Nosso Casamento"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM casamento_recup WHERE email='maria@teste.com'").fetchone()["status"] == "pendente", "Pix pendente vira recuperação pendente")
    kiwify(cli, "order_approved", "K1", "maria@teste.com",
           ["O Santo do Nosso Casamento", "30 Dias Rezando pelo Meu Marido", "Novena de Santa Rita pelo Casamento"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM casamento_recup WHERE email='maria@teste.com'").fetchone()["status"] == "pago", "recuperação cancelada ao pagar")
        confere(c.execute("SELECT COUNT(*) FROM compras").fetchone()[0] == 0, "nada entrou nas compras do Meu Santo")
    confere(espera_fase("K1", "enviado"), "livro + 2 bumps gerados e enviados")
    st = cli.get(f"/api/casamento/status?ref={ref}").json()
    confere(st["pronto"] and [a["sku"] for a in st["arquivos"]] == ["casamento", "marido", "rita"], "status pronto com 3 arquivos")
    tok = st["arquivos"][0]["url"].split("/baixar/")[1]
    for i in range(3):
        b = cli.get("/api/casamento/baixar/" + tok.rsplit("/", 1)[0] + f"/{i}")
        confere(b.status_code == 200 and b.content[:4] == b"%PDF", f"download do PDF {i} ({len(b.content) // 1024} KB)")
    confere(cli.get("/api/casamento/baixar/" + tok.rsplit("/", 1)[0] + "/7").status_code == 404, "índice inexistente → 404")
    emails = sorted((TMP / "dados" / "emails_teste").glob("*maria_teste_com*"))
    confere(any("Ana e José" in e.read_text() and "anexo:" in e.read_text() for e in emails), "e-mail de entrega com anexo")
    with servidor.db() as c:
        dados = json.loads(c.execute("SELECT dados FROM clientes WHERE email='maria@teste.com'").fetchone()["dados"])
    confere(dados["santo"]["dia"] == 5 and dados["santo"]["mes"] == 3 and dados["santo"]["origem"] == "casamento", "aniversário guardado no cadastro do Meu Santo")
    # 4. aviso repetido não duplica
    kiwify(cli, "order_approved", "K1", "maria@teste.com", ["O Santo do Nosso Casamento"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT COUNT(*) FROM casamento_compras").fetchone()[0] == 1, "aviso repetido não cria outra compra")
    # 5. compra sem quiz (link direto): pede os dados e entrega depois
    kiwify(cli, "order_approved", "K2", "joao@teste.com", ["O Santo do Nosso Casamento"])
    with servidor.db() as c:
        r2 = c.execute("SELECT * FROM casamento_compras WHERE order_id='K2'").fetchone()
    confere(r2["fase"] == "aguardando_dados", "sem sck → aguardando dados")
    time.sleep(1.5)
    confere(any("Pagamento confirmado" in e.read_text() for e in (TMP / "dados" / "emails_teste").glob("*joao_teste_com*")), "e-mail pedindo a data do casamento")
    g = cli.get(f"/api/casamento/dados?t={r2['token']}").json()
    confere(g["precisa"] and g["nome"] == "Maria", "página de dados reconhece o link")
    pres = {**PEDIDO, "modo": "presente", "presenteador": "Clara", "dedicatoria": "Para os meus pais, com amor.", "casamento": {"dia": 25, "mes": 12, "ano": 1976},
            "pedido": "Que eles tenham saúde", "igreja": "civil"}
    confere(cli.post("/api/casamento/dados", json={"t": r2["token"], "pedido": pres}).json()["ok"], "dados enviados")
    confere(espera_fase("K2", "enviado"), "livro de presente (casados no Natal, só no civil) entregue")
    # 6. bump que chega num aviso separado, sem sck
    kiwify(cli, "order_approved", "K3", "joao@teste.com", ["Novena de Santa Rita pelo Casamento"])
    confere(espera_fase("K3", "enviado"), "bump separado usa o quiz da compra principal e sai sozinho")
    with servidor.db() as c:
        confere(json.loads(c.execute("SELECT skus FROM casamento_compras WHERE order_id='K3'").fetchone()["skus"]) == ["rita"], "bump separado não duplica o livro")
    # 7. venda do Meu Santo continua no fluxo de sempre; pedido misto separa os dois
    kiwify(cli, "order_approved", "M1", "outra@teste.com", ["Devocionário do Meu Santo Protetor"])
    kiwify(cli, "order_approved", "M2", "mista@teste.com", ["O Santo do Nosso Casamento", "Calendário de Fé 2027"], sck=None)
    with servidor.db() as c:
        meu = {(r["email"], r["sku"]) for r in c.execute("SELECT email, sku FROM compras")}
        cas = {r["email"] for r in c.execute("SELECT email FROM casamento_compras")}
    confere(("outra@teste.com", "santo") in meu and "outra@teste.com" not in cas, "devocionário segue no Meu Santo")
    confere(("mista@teste.com", "santo_cal") in meu and "mista@teste.com" in cas, "pedido misto: cada parte no seu lugar")
    # 8. reembolso e recusa
    kiwify(cli, "order_refunded", "K2", "joao@teste.com", ["O Santo do Nosso Casamento"])
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM casamento_compras WHERE order_id='K2'").fetchone()["status"] == "reembolsado", "reembolso registrado")
    kiwify(cli, "order_approved", "K2", "joao@teste.com", ["O Santo do Nosso Casamento"])
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM casamento_compras WHERE order_id='K2'").fetchone()["status"] == "reembolsado", "reembolso não volta para pago")
    # 9. carrinho abandonado → e-mail de recuperação depois da espera
    cli.post("/webhook/kiwify/segredo", json={"status": "abandoned", "email": "fulana@teste.com", "name": "Fulana",
                                              "product_name": "O Santo do Nosso Casamento", "product_id": "p1", "checkout_link": "https://pay.kiwify.com.br/AbCdEf1"})
    with servidor._lock, servidor.db() as c:
        c.execute("UPDATE casamento_recup SET criado='2020-01-01T00:00:00' WHERE email='fulana@teste.com'")
    casamento.recuperar()
    confere(any("ficou pela metade" in e.read_text() for e in (TMP / "dados" / "emails_teste").glob("*fulana_teste_com*")), "e-mail de carrinho abandonado")
    # 10. reenviar sempre responde igual
    confere(cli.post("/api/casamento/reenviar", json={"email": "ninguem@teste.com"}).json() == {"ok": True}, "reenviar não revela quem é cliente")
    # 11. conferência dos textos da IA (sem chamar a API)
    ctx = casamento.P.contexto(ped, casamento.santo_info(13, 6))
    servidor.CFG["MOCK_IA"] = "0"
    casamento._chamar_ia = lambda e: {"carta": ["Ana e José, " + "palavra " * 30, "Segundo " + "texto " * 30], "santo_historia": "x",
                                      "santo_casamento": "Isto vai mudar com certeza o casamento de vocês " + "a " * 60,
                                      "oracao_casal": "Senhor, nós, Ana e José, " + "rezamos " * 60, "oracao_pessoal": "Senhor, " + "peço " * 50 + "Amém.",
                                      "intencao": "Mais paciência entre nós."}
    tx, usou = casamento.textos(ctx, ped)
    confere(usou and tx["oracao_casal"].endswith("Amém.") and tx["intencao"] == "mais paciência entre nós", "IA aproveitada e ajustada")
    confere(tx["santo_historia"] == casamento.textos_padrao(ctx, ped)["santo_historia"], "campo curto demais volta para o padrão")
    confere("vai mudar" not in tx["santo_casamento"], "promessa de resultado é barrada")
    casamento._chamar_ia = lambda e: (_ for _ in ()).throw(RuntimeError("sem crédito"))
    tx, usou = casamento.textos(ctx, {**ped, "pedido": "ele me bate quando bebe"})
    confere(not usou and tx["_alerta_violencia"], "IA fora do ar → texto padrão; aviso de violência ligado")

print(f"\n{sum(OK)} conferências OK. Pasta do teste: {TMP}")
