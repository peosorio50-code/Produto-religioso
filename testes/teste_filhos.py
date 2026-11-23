"""Teste ponta a ponta da Novena pelos Filhos com o servidor.py de verdade (v19 + ganchos do casamento + ganchos da novena).

Uso (fora da VPS, numa pasta qualquer):
  pip install fastapi httpx anthropic
  python testes/teste_filhos.py
Monta uma cópia do servidor numa pasta temporária, com um santos.py de mentira, MOCK_IA=1 e sem Resend
(os e-mails vão para dados/emails_teste). Precisa de um Chromium para o PDF (FILHOS_CHROME ou Playwright).
"""
import datetime as dt, json, os, pathlib, re, shutil, sys, tempfile, time

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="filhos-teste-"))
for f in (RAIZ / "servidor").glob("*.py"):
    shutil.copy(f, TMP / f.name)
for d in ("casamento_fontes", "filhos_fontes"):
    shutil.copytree(RAIZ / "servidor" / d, TMP / d)
shutil.copy(RAIZ / "testes" / "santos_stub.py", TMP / "santos.py")
V19 = pathlib.Path(os.environ.get("V19_DIR", "/nao-existe"))  # pasta com o folego.py e o clube.py da VPS (opcional)
for nome in ("folego.py", "clube.py"):
    if (V19 / nome).exists():
        shutil.copy(V19 / nome, TMP / nome)
    elif not (TMP / nome).exists():
        (TMP / nome).write_text("from fastapi import APIRouter\nrouter = APIRouter()\n"
                                "def tabelas(): pass\ndef iniciar(): pass\ndef eh_folego(n): return False\n")
os.environ.update({"WEBHOOK_SEGREDO": "segredo", "FILHOS_CHECKOUT": "FiLh0s1", "CASAMENTO_CHECKOUT": "AbCdEf1", "MOCK_IA": "1", "RESEND_API_KEY": "",
                   "SITE_URL_SANTO": "https://meusantoprotetor.online", "QUIZ_AUTO": "1", "FILHOS_HORA_DIA": "0"})
os.environ.setdefault("FILHOS_PDF_MOTOR", "chromium")
sys.path.insert(0, str(TMP)); os.chdir(TMP)

from fastapi.testclient import TestClient  # noqa: E402
import servidor  # noqa: E402
import filhos  # noqa: E402

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
         "Commissions": {"charge_amount": 8700}, "TrackingParameters": {"sck": sck} if sck else {}}
    if len(produtos) > 1:
        p["order_bumps"] = [{"product_id": f"b{i}", "name": n} for i, n in enumerate(produtos[1:])]
    r = cli.post("/webhook/kiwify/segredo", json=p)
    confere(r.status_code == 200, f"webhook {evento} {produtos[0][:32]} → {r.status_code}")
    return r


def espera_fase(order, fase, seg=120):
    t0 = time.time()
    while time.time() - t0 < seg:
        with servidor.db() as c:
            r = c.execute("SELECT fase, erro FROM filhos_compras WHERE order_id=?", (order,)).fetchone()
        if r and r["fase"] == fase:
            return True
        if r and r["fase"] == "erro":
            print("erro:", r["erro"]); return False
        time.sleep(1)
    return False


def emails(trecho):
    return sorted((TMP / "dados" / "emails_teste").glob(f"*{trecho}*"))


PEDIDO = {"papel": "mae", "quem": {"nome": "maria"},
          "filhos": [{"nome": "pedro HENRIQUE", "rel": "filho", "dia": 13, "mes": 6, "ano": 1996},
                     {"nome": "Ana", "rel": "filha", "dia": 25, "mes": 12, "ano": 2016},
                     {"nome": "João", "rel": "filho", "dia": 19, "mes": 3, "partiu": True}],
          "pedidos": ["fe", "protecao", "vicios", "xx"], "pedido": "Que o Pedro volte a rezar e saia da bebida."}

with TestClient(servidor.app) as cli:
    # 1. revelação grátis
    r = cli.get("/api/filhos/santos?d=1306,2512,1903")
    s = r.json()["santos"]
    confere(r.status_code == 200 and s[0]["nome"] == "Santo Antônio" and s[1]["festa"] is True and len(s) == 3, "santos do dia de cada filho (e Natal = festa)")
    confere(cli.get("/api/filhos/santos?d=3102").status_code == 400, "data impossível recusada")
    # 2. pedido do quiz
    confere(cli.post("/api/filhos/pedido", json={"pedido": {**PEDIDO, "filhos": []}}).status_code == 400, "pedido sem filhos recusado")
    confere(cli.post("/api/filhos/pedido", json={"pedido": {**PEDIDO, "filhos": PEDIDO["filhos"] * 3}}).status_code == 400, "mais de 6 recusado")
    confere(cli.post("/api/filhos/pedido", json={"pedido": {**PEDIDO, "quem": {"nome": ""}}}).status_code == 400, "sem o nome de quem reza recusado")
    fut = [{"nome": "Bia", "dia": 1, "mes": 1, "ano": dt.date.today().year + 1}]
    confere(cli.post("/api/filhos/pedido", json={"pedido": {**PEDIDO, "filhos": fut}}).status_code == 400, "nascimento no futuro recusado")
    r = cli.post("/api/filhos/pedido", json={"pedido": PEDIDO, "origem": {"utm_source": "fb", "utm_campaign": "c1", "lixo": "x"}})
    ref, url = r.json()["ref"], r.json()["url"]
    confere(r.status_code == 200 and url.startswith("https://pay.kiwify.com.br/FiLh0s1?sck=" + ref) and "utm_source=fb" in url and "lixo" not in url,
            f"checkout com sck e utm ({url})")
    ped = filhos._pedido(ref)
    confere(ped["quem"]["nome"] == "Maria" and ped["filhos"][0]["nome"] == "Pedro Henrique" and ped["filhos"][2]["partiu"] is True
            and ped["filhos"][1]["partiu"] is False and ped["pedidos"] == ["fe", "protecao", "vicios"], "nomes, partiu e pedidos normalizados")
    confere(cli.get(f"/api/filhos/status?ref={ref}").json() == {"pago": False}, "status antes de pagar")
    # 3. Pix gerado e depois pago, com os 2 bumps no mesmo aviso
    kiwify(cli, "pix_created", "F1", "maria@teste.com", ["Novena pelos Filhos (em vídeo)"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM filhos_recup WHERE email='maria@teste.com'").fetchone()["status"] == "pendente", "Pix pendente vira recuperação pendente")
    kiwify(cli, "order_approved", "F1", "maria@teste.com",
           ["Novena pelos Filhos (em vídeo)", "Terço pelos Filhos (em vídeo)", "30 Bênçãos para Mandar aos Filhos"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT status FROM filhos_recup WHERE email='maria@teste.com'").fetchone()["status"] == "pago", "recuperação cancelada ao pagar")
        confere(c.execute("SELECT COUNT(*) FROM compras").fetchone()[0] == 0 and c.execute("SELECT COUNT(*) FROM casamento_compras").fetchone()[0] == 0,
                "nada entrou nas compras do Meu Santo nem do casamento")
    confere(espera_fase("F1", "enviado"), "novena + 2 bumps gerados e enviados")
    st = cli.get(f"/api/filhos/status?ref={ref}").json()
    confere(st["pronto"] and [a["sku"] for a in st["arquivos"]] == ["novena", "bencaos", "terco"] and "/novena.html?t=" in st["area"],
            "status pronto com a página da novena e 3 arquivos")
    tok = st["area"].split("t=")[1]
    for i in range(3):
        b = cli.get(f"/api/filhos/baixar/{tok}/{i}")
        confere(b.status_code == 200 and b.content[:4] == b"%PDF", f"download do PDF {i} ({len(b.content) // 1024} KB)")
    confere(cli.get(f"/api/filhos/baixar/{tok}/7").status_code == 404, "índice inexistente → 404")
    ar = cli.get(f"/api/filhos/area?t={tok}").json()
    confere(ar["ok"] and ar["quem"] == "Maria" and [p["nome"] for p in ar["pessoas"]] == ["Pedro", "Ana", "João"] and ar["nomes"] == "Pedro e Ana",
            "área: nomes (quem partiu fica fora da lista de vivos)")
    confere(len(ar["dias"]) == 9 and "Pedro e Ana" in ar["dias"][0]["oracao"] and "João" in ar["dias"][0]["oracao"] and not re.search(r"\{[A-Za-z_]+\}", json.dumps(ar, ensure_ascii=False)),
            "área: 9 dias com os nomes, sem marcador sobrando")
    confere(ar["pessoas"][1]["festa"] and len(ar["bencaos"]) == 2 and len(ar["bencaos"][0]["msgs"]) == 30 and "Pedro" in ar["bencaos"][0]["msgs"][0],
            "área: 30 bênçãos para cada filho vivo")
    confere(len(ar["terco"]) == 5 and "Pedro e Ana" in ar["terco"][0]["oferta"] and ar["pessoas"][0]["oracao"].endswith("Amém."), "área: terço e oração de cada um")
    confere(any("Pedro e Ana" in e.read_text() and "anexo:" in e.read_text() and "novena.html?t=" in e.read_text() for e in emails("maria_teste_com")),
            "e-mail de entrega com anexo e o link da novena")
    # 4. aviso repetido não duplica
    kiwify(cli, "order_approved", "F1", "maria@teste.com", ["Novena pelos Filhos (em vídeo)"], sck=ref)
    with servidor.db() as c:
        confere(c.execute("SELECT COUNT(*) FROM filhos_compras").fetchone()[0] == 1, "aviso repetido não cria outra compra")
    # 5. upsell de 1 clique (outro pedido, sem sck) usa o quiz da compra principal
    kiwify(cli, "order_approved", "F2", "maria@teste.com", ["Um Livro para Cada Filho"], metodo="credit_card")
    confere(espera_fase("F2", "enviado"), "upsell entregue sozinho")
    with servidor.db() as c:
        r2 = c.execute("SELECT * FROM filhos_compras WHERE order_id='F2'").fetchone()
    arqs = json.loads(r2["arquivos"])
    confere(json.loads(r2["skus"]) == ["livros"] and [a["titulo"] for a in arqs] == ["Um Livro para Pedro", "Um Livro para Ana"],
            "upsell: um livro para cada filho vivo, sem duplicar a novena")
    ar = cli.get(f"/api/filhos/area?t={tok}").json()
    confere(set(ar["skus"]) == {"novena", "bencaos", "terco", "livros"} and len(ar["arquivos"]) == 5, "área junta a novena, os bumps e o upsell")
    with servidor.db() as c:
        confere(c.execute("SELECT COUNT(*) FROM filhos_textos").fetchone()[0] == 1, "textos escritos uma vez só para o quiz")
    # 6. compra sem quiz (link direto): pede os dados e entrega depois
    kiwify(cli, "order_approved", "F3", "joao@teste.com", ["Novena pelos Filhos (em vídeo)"])
    with servidor.db() as c:
        r3 = c.execute("SELECT * FROM filhos_compras WHERE order_id='F3'").fetchone()
    confere(r3["fase"] == "aguardando_dados", "sem sck → aguardando dados")
    time.sleep(1.5)
    confere(any("Pagamento confirmado" in e.read_text() for e in emails("joao_teste_com")), "e-mail pedindo os nomes e as datas")
    g = cli.get(f"/api/filhos/dados?t={r3['token']}").json()
    confere(g["precisa"] and g["nome"] == "Maria", "página de dados reconhece o link")
    confere(cli.get(f"/api/filhos/area?t={r3['token']}").json().get("precisa_dados"), "área sem dados manda para a página de dados")
    avo = {"papel": "avo_f", "quem": {"nome": "Teresa"}, "filhos": [{"nome": "Bia", "rel": "neta", "dia": 22, "mes": 5, "ano": 2019}], "pedidos": ["saude"],
           "pedido": ""}
    confere(cli.post("/api/filhos/dados", json={"t": r3["token"], "pedido": avo}).json()["ok"], "dados enviados")
    confere(espera_fase("F3", "enviado"), "novena da avó pela neta (uma pessoa só) entregue")
    pdf = filhos.P.html_novena(filhos.P.contexto(avo, [filhos.santo_info(22, 5)]),
                               filhos.textos_padrao(filhos.P.contexto(avo, [filhos.santo_info(22, 5)]), avo))
    confere("Novena pelos Netos" in pdf and "a minha neta" in pdf and "cada um deles" not in pdf and not re.search(r"\{[A-Za-z_]+\}", pdf.split("<body>")[1]) and "por a minha" not in pdf,
            "texto no singular e no feminino (neta), sem marcador sobrando")
    # 7. venda do Meu Santo e do casamento continuam no fluxo de sempre; pedido misto separa
    kiwify(cli, "order_approved", "M1", "outra@teste.com", ["Devocionário do Meu Santo Protetor"])
    kiwify(cli, "order_approved", "M2", "mista@teste.com", ["Novena pelos Filhos (em vídeo)", "Calendário de Fé 2027"])
    kiwify(cli, "order_approved", "C1", "casal@teste.com", ["O Santo do Nosso Casamento"])
    with servidor.db() as c:
        meu = {(r["email"], r["sku"]) for r in c.execute("SELECT email, sku FROM compras")}
        fil = {r["email"] for r in c.execute("SELECT email FROM filhos_compras")}
        cas = {r["email"] for r in c.execute("SELECT email FROM casamento_compras")}
    confere(("outra@teste.com", "santo") in meu and "outra@teste.com" not in fil, "devocionário segue no Meu Santo")
    confere(("mista@teste.com", "santo_cal") in meu and "mista@teste.com" in fil, "pedido misto: cada parte no seu lugar")
    confere("casal@teste.com" in cas and "casal@teste.com" not in fil, "casamento segue no módulo dele")
    # 8. reembolso
    kiwify(cli, "order_refunded", "F3", "joao@teste.com", ["Novena pelos Filhos (em vídeo)"])
    kiwify(cli, "order_approved", "F3", "joao@teste.com", ["Novena pelos Filhos (em vídeo)"])
    with servidor.db() as c:
        r3 = c.execute("SELECT status, sem_email FROM filhos_compras WHERE order_id='F3'").fetchone()
    confere(r3["status"] == "reembolsado" and r3["sem_email"] == 1, "reembolso registrado, não volta para pago e para os lembretes")
    # 9. lembretes diários da novena (dia 2 e depois o dia 9, sem repetir)
    with servidor._lock, servidor.db() as c:
        c.execute("UPDATE filhos_compras SET enviado=? WHERE order_id='F1'", ((dt.datetime.now() - dt.timedelta(days=1)).isoformat(timespec="seconds"),))
    filhos.lembretes_novena(); filhos.lembretes_novena()
    confere(len([e for e in emails("maria_teste_com") if "2º dia da novena" in e.read_text()]) == 1, "lembrete do 2º dia, uma vez só")
    with servidor._lock, servidor.db() as c:
        c.execute("UPDATE filhos_compras SET enviado=? WHERE order_id='F1'", ((dt.datetime.now() - dt.timedelta(days=10)).isoformat(timespec="seconds"),))
    filhos.lembretes_novena()
    e9 = [e for e in emails("maria_teste_com") if "9º dia da novena" in e.read_text()]
    confere(len(e9) == 1 and "Consagração a Jesus por Maria" in e9[0].read_text() and "/api/filhos/sair?t=" in e9[0].read_text(),
            "pula para o 9º dia (sem mandar os atrasados), com o convite e o link para parar")
    with servidor.db() as c:
        confere(c.execute("SELECT dia_email FROM filhos_compras WHERE order_id='F1'").fetchone()[0] == 9, "lembretes terminam no 9º dia")
    confere("não vai mais receber" in cli.get(f"/api/filhos/sair?t={tok}").text, "link para parar os lembretes")
    # 10. carrinho abandonado → e-mail de recuperação depois da espera
    cli.post("/webhook/kiwify/segredo", json={"status": "abandoned", "email": "fulana@teste.com", "name": "Fulana",
                                              "product_name": "Novena pelos Filhos (em vídeo)", "product_id": "p1", "checkout_link": "https://pay.kiwify.com.br/FiLh0s1"})
    with servidor._lock, servidor.db() as c:
        c.execute("UPDATE filhos_recup SET criado='2020-01-01T00:00:00' WHERE email='fulana@teste.com'")
    filhos.recuperar()
    confere(any("ficou pela metade" in e.read_text() for e in emails("fulana_teste_com")), "e-mail de carrinho abandonado")
    # 11. reenviar sempre responde igual
    confere(cli.post("/api/filhos/reenviar", json={"email": "ninguem@teste.com"}).json() == {"ok": True}, "reenviar não revela quem é cliente")
    # 12. conferência dos textos da IA (sem chamar a API)
    santos = [filhos.santo_info(f["dia"], f["mes"]) for f in ped["filhos"]]
    ctx = filhos.P.contexto(ped, santos)
    servidor.CFG["MOCK_IA"] = "0"
    filhos._chamar_ia = lambda e: {"carta": ["Maria, " + "palavra " * 30, "Segundo " + "texto " * 30],
                                   "filhos": [{"nome": "Ana", "santo_texto": "Natal " * 40, "oracao": "Senhor, eu Vos entrego a minha filha Ana " + "rezo " * 50},
                                              {"nome": "Pedro", "santo_texto": "curto", "oracao": "Senhor, Pedro vai voltar com certeza " + "a " * 80},
                                              {"nome": "João", "santo_texto": "João " * 40, "oracao": "Senhor, dai a João o descanso eterno " + "paz " * 50 + "Amém."}],
                                   "intencao": "Que Pedro e Ana vivam perto de Deus."}
    tx, usou = filhos.textos(ctx, ped)
    pad = filhos.textos_padrao(ctx, ped)
    confere(usou and tx["intencao"] == "que Pedro e Ana vivam perto de Deus" and tx["filhos"][1]["oracao"].startswith("Senhor, eu Vos entrego a minha filha Ana")
            and tx["filhos"][1]["oracao"].endswith("Amém."), "IA aproveitada, na ordem certa mesmo trocada, e ajustada")
    confere(tx["filhos"][0] == pad["filhos"][0], "campo curto ou com promessa volta para o padrão")
    confere("descanso eterno" in pad["filhos"][2]["oracao"] and "Guardai" not in pad["filhos"][2]["oracao"], "oração padrão de quem partiu")
    confere(tx["_alerta_vicio"], "aviso de ajuda para vício ligado")
    filhos._chamar_ia = lambda e: (_ for _ in ()).throw(RuntimeError("sem crédito"))
    tx, usou = filhos.textos(ctx, {**ped, "pedido": "meu filho falou que quer se matar"})
    confere(not usou and tx["_alerta_crise"] and tx["filhos"] == pad["filhos"], "IA fora do ar → texto padrão; aviso do CVV ligado")

print(f"\n{sum(OK)} conferências OK. Pasta do teste: {TMP}")
