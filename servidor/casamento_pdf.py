"""O Santo do Nosso Casamento: monta o HTML dos PDFs e converte em PDF.

Três PDFs:
  livro   O Santo do Nosso Casamento (produto principal)
  marido  30 Dias Rezando pelo Meu Marido / pela Minha Esposa (order bump)
  rita    Novena de Santa Rita pelo Casamento (order bump)

Conversão HTML → PDF: tenta, nesta ordem, Playwright (Python), WeasyPrint e o Chromium pela linha de comando.
Para saber qual funciona na VPS: ./venv/bin/python casamento.py diagnostico
"""
import base64, datetime as dt, html as H, os, pathlib, re, shutil, subprocess, tempfile

import casamento_conteudo as C

BASE = pathlib.Path(__file__).parent
FONTES = BASE / "casamento_fontes"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
ANO_CAL = 2027
E = H.escape

PREFIXOS_SANTO = ("são ", "santo ", "santa ", "santos ", "santas ", "beato", "beata", "bem-aventurad", "nossa senhora", "virgem",
                  "imaculad", "todos os santos", "os santos", "anjo", "arcanjo", "sagrado coração de maria", "maria, mãe")


# ------------------------------------------------------------------ dados → marcadores
def data_pt(d, m, a=None):
    return f"{d} de {MESES[m - 1]}" + (f" de {a}" if a else "")


def eh_festa(nome):
    """True quando o dia é uma festa do Senhor (Natal, Batismo do Senhor, Santa Cruz...), e não um santo que intercede."""
    return not (nome or "").strip().lower().startswith(PREFIXOS_SANTO)


def primeiro(nome):
    p = (nome or "").strip().split()
    return p[0].capitalize() if p else ""


def contexto(pedido, santo, santo_ela=None, santo_ele=None, hoje=None):
    """Tudo o que os modelos de página precisam, já em texto."""
    hoje = hoje or dt.date.today()
    cz = pedido["casamento"]; ela, ele = primeiro(pedido["ela"]["nome"]), primeiro(pedido["ele"]["nome"])
    festa = eh_festa(santo["nome"])
    if festa:
        invoc, interc = "Santa Maria, Mãe de Deus, rogai por nós.", "pela intercessão de Nossa Senhora"
    else:
        invoc, interc = f"{santo['nome']}, rogai por nós.", f"pela intercessão de {santo['nome']}"
    anos_hoje = hoje.year - cz["ano"] - ((hoje.month, hoje.day) < (cz["mes"], cz["dia"]))
    anos_cal = ANO_CAL - cz["ano"]
    quem = pedido.get("quem") or "ela"
    if pedido.get("modo") == "presente":
        quem = "ela"
    quem_nome, conj_nome = (ela, ele) if quem == "ela" else (ele, ela)
    return {
        "ELA": ela, "ELE": ele, "CASAL": f"{ela} e {ele}", "DATA": data_pt(cz["dia"], cz["mes"], cz["ano"]),
        "DATA_CURTA": data_pt(cz["dia"], cz["mes"]), "SANTO": santo["nome"], "SANTO_QUEM": santo.get("quem") or "",
        "FESTA": festa, "INVOCACAO": invoc, "INTERCESSAO": interc, "ANOS": max(anos_hoje, 0), "ANOS_CAL": anos_cal,
        "QUEM": quem_nome, "CONJ": conj_nome, "GEN_CONJ": "m" if quem == "ela" else "f",
        "IGREJA": pedido.get("igreja") != "civil", "MODO": pedido.get("modo") or "nos",
        "PRESENTEADOR": primeiro(pedido.get("presenteador") or ""), "DEDICATORIA": (pedido.get("dedicatoria") or "").strip(),
        "SANTO_ELA": santo_ela, "SANTO_ELE": santo_ele, "pedido": pedido, "santo": santo,
    }


def preencher(txt, ctx, extra=None):
    trocas = {k: str(v) for k, v in ctx.items() if isinstance(v, (str, int)) and k.isupper()}
    trocas.update(extra or {})
    return re.sub(r"\{([A-Za-z_]+)\}", lambda m: trocas.get(m.group(1), m.group(0)), txt)


def ctx_genero(nome, gen):
    g = dict(C.GENERO[gen]); g["N"] = nome
    return g


# ------------------------------------------------------------------ peças visuais
def _fontes_css():
    faces = [("Cormorant Garamond", "CormorantGaramond-400.ttf", 400, "normal"), ("Cormorant Garamond", "CormorantGaramond-400i.ttf", 400, "italic"),
             ("Cormorant Garamond", "CormorantGaramond-600.ttf", 600, "normal"), ("Cormorant Garamond", "CormorantGaramond-600i.ttf", 600, "italic"),
             ("Cinzel", "Cinzel-500.ttf", 500, "normal"), ("Cinzel", "Cinzel-700.ttf", 700, "normal"),
             ("Great Vibes", "GreatVibes-400.ttf", 400, "normal"), ("Outfit", "Outfit-400.ttf", 400, "normal"), ("Outfit", "Outfit-600.ttf", 600, "normal")]
    out = []
    for fam, arq, w, st in faces:
        f = FONTES / arq
        if f.exists():
            b = base64.b64encode(f.read_bytes()).decode()
            out.append(f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{b}) format('truetype');font-weight:{w};font-style:{st}}}")
    return "\n".join(out)


def svg_aliancas(tam=150, cor="#C9A052", raios=True):
    """Duas alianças entrelaçadas com uma cruz em cima e raios atrás."""
    r = ""
    if raios:
        import math
        for i in range(36):
            a = math.radians(i * 10); c1, c2 = 44, 72 if i % 2 else 64
            r += (f'<line x1="{75 + c1 * math.cos(a):.1f}" y1="{82 + c1 * math.sin(a):.1f}" x2="{75 + c2 * math.cos(a):.1f}" '
                  f'y2="{82 + c2 * math.sin(a):.1f}" stroke="{cor}" stroke-width="{1.2 if i % 2 else 0.7}" opacity=".55"/>')
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">{r}'
            f'<circle cx="62" cy="90" r="22" fill="none" stroke="{cor}" stroke-width="5"/>'
            f'<circle cx="88" cy="90" r="22" fill="none" stroke="{cor}" stroke-width="5"/>'
            f'<path d="M75 30 v32 M64 41 h22" stroke="{cor}" stroke-width="4.5" stroke-linecap="round"/></svg>')


def svg_rosa(tam=120, cor="#C9A052"):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{cor}" stroke-width="3" stroke-linecap="round">'
            '<path d="M60 26c-14 0-24 10-24 22 0 13 11 22 24 22s24-9 24-22c0-12-10-22-24-22z"/>'
            '<path d="M60 36c-7 0-12 5-12 11 0 7 6 11 12 11s12-4 12-11"/><path d="M60 44c-3 0-5 2-5 4"/>'
            '<path d="M60 70v34"/><path d="M60 86c-9-2-16-8-18-16 8 0 16 5 18 16z"/><path d="M60 80c8-2 14-8 16-15-8 0-14 5-16 15z"/></svg>')


def svg_vela(tam=110, cor="#C9A052"):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{cor}" stroke-width="3" stroke-linecap="round">'
            '<path d="M55 14c6 9 9 15 9 20a9 9 0 0 1-18 0c0-5 3-11 9-20z"/><path d="M42 50h26v46H42z"/><path d="M55 44v6"/><path d="M34 96h42"/></svg>')


DIV = '<div class="div"><span></span><i>✦</i><span></span></div>'

CSS = """
@page { size: A4; margin: 18mm 19mm 18mm 19mm; }
@page capa { margin: 0; }
html, body { background: #ffffff; }
body { margin: 0; font-family: 'Cormorant Garamond', Georgia, 'DejaVu Serif', serif; color: #2a2338; font-size: 14.2pt; line-height: 1.5; }
.capa { page: capa; width: 210mm; height: 297mm; box-sizing: border-box; background: #0B1636; color: #F5ECD9; position: relative;
        display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 26mm 22mm; break-after: page; }
.capa::before { content: ""; position: absolute; top: 11mm; right: 11mm; bottom: 11mm; left: 11mm; border: 1.2px solid #C9A052; border-radius: 4px; }
.capa::after { content: ""; position: absolute; top: 14mm; right: 14mm; bottom: 14mm; left: 14mm; border: .6px solid rgba(201,160,82,.55); border-radius: 3px; }
.capa .marca { font-family: Cinzel, serif; letter-spacing: .32em; font-size: 9.5pt; color: #E9CF93; margin-bottom: 14mm; }
.capa h1 { font-family: Cinzel, serif; font-weight: 500; font-size: 25pt; letter-spacing: .08em; line-height: 1.25; margin: 6mm 0 2mm; color: #F5ECD9; }
.capa .nomes { font-family: 'Great Vibes', cursive; font-size: 54pt; color: #E9CF93; line-height: 1.1; margin: 8mm 0 4mm; }
.capa .linha { font-size: 15pt; font-style: italic; color: #E6DCC6; margin: 1mm 0; }
.capa .rodape { position: absolute; bottom: 24mm; left: 0; right: 0; font-family: Cinzel, serif; font-size: 9pt; letter-spacing: .25em; color: #C9A052; }
.capa.clara { background: #F8F3EE; color: #17295A; }
.capa.clara h1 { color: #17295A; } .capa.clara .nomes { color: #A57F35; } .capa.clara .linha { color: #4b4560; } .capa.clara .marca { color: #A57F35; }
.secao { break-before: page; }
.kicker { font-family: Cinzel, serif; font-size: 9pt; letter-spacing: .28em; color: #A57F35; text-transform: uppercase; text-align: center; margin: 0 0 2mm; }
h2 { font-family: Cinzel, serif; font-weight: 500; color: #17295A; font-size: 19pt; text-align: center; margin: 0 0 3mm; letter-spacing: .04em; line-height: 1.25; }
h3 { font-family: Cinzel, serif; font-weight: 700; color: #17295A; font-size: 11.5pt; letter-spacing: .08em; margin: 6mm 0 1.5mm; text-transform: uppercase; }
p { margin: 0 0 3.2mm; text-align: justify; hyphens: auto; }
.div { display: flex; align-items: center; justify-content: center; gap: 4mm; margin: 2mm 0 6mm; color: #C9A052; }
.div span { display: block; width: 26mm; height: 1px; background: #C9A052; opacity: .7; } .div i { font-style: normal; font-size: 10pt; }
.oracao { border-left: 2.5px solid #C9A052; background: #fffaf1; padding: 4mm 5mm; margin: 3mm 0 5mm; font-style: italic; border-radius: 0 6px 6px 0; break-inside: avoid; }
.oracao p { margin: 0; }
.leitura { font-family: Outfit, sans-serif; font-size: 9.5pt; color: #6b6385; letter-spacing: .02em; margin: -1mm 0 3mm; }
.leitura b { color: #17295A; }
.dia { break-inside: avoid; margin: 0 0 6mm; padding-bottom: 2mm; border-bottom: 1px dashed rgba(201,160,82,.45); }
.dia:last-child { border-bottom: 0; }
.num { font-family: Cinzel, serif; color: #A57F35; font-size: 10pt; letter-spacing: .2em; }
.gesto { font-family: Outfit, sans-serif; font-size: 10pt; color: #4b4560; background: #f1e8d8; border-radius: 6px; padding: 2mm 3.5mm; display: inline-block; }
.santinho { text-align: center; margin: 0 0 2mm; }
.cada { break-inside: avoid; }
.santo-nome { font-family: Cinzel, serif; font-size: 21pt; color: #17295A; text-align: center; margin: 1mm 0; letter-spacing: .03em; }
.santo-quem { text-align: center; font-style: italic; color: #6b6385; margin: 0 0 4mm; }
.aviso { font-family: Outfit, sans-serif; font-size: 10.2pt; line-height: 1.5; border: 1px solid #d9b8a0; background: #fff3ea; border-radius: 8px; padding: 3.5mm 4.5mm; margin: 4mm 0; break-inside: avoid; }
.aviso b { color: #7a3414; }
.caixa { border: 1px solid #e2cf9f; background: #fffaf0; border-radius: 10px; padding: 4mm 5mm; margin: 4mm 0; break-inside: avoid; }
.dois { display: flex; gap: 6mm; break-inside: avoid; } .dois > div { flex: 1; }
.mini { text-align: center; border: 1px solid #e2cf9f; border-radius: 10px; padding: 3mm; background: #fffaf0; }
.mini .quem { font-family: Cinzel, serif; font-size: 9pt; letter-spacing: .2em; color: #A57F35; }
.mini .st { font-family: Cinzel, serif; font-size: 13pt; color: #17295A; margin: 1.5mm 0; }
.mini .dt { font-style: italic; color: #6b6385; font-size: 12pt; }
table.cal { width: 100%; border-collapse: collapse; font-size: 12.5pt; }
table.cal td { padding: 2.2mm 2mm; border-bottom: 1px solid #eadfca; vertical-align: top; }
table.cal td.d { font-family: Cinzel, serif; color: #17295A; white-space: nowrap; width: 34mm; font-size: 11pt; }
table.cal tr.nosso td { background: #fff3d9; } table.cal tr.nosso td.d { color: #8a6420; }
.sempre h3 { margin-top: 4mm; }
ol.passos { padding-left: 6mm; margin: 0 0 4mm; } ol.passos li { margin-bottom: 2mm; }
.fala { font-style: italic; margin: 2mm 0 4mm; } .fala b { font-style: normal; font-family: Cinzel, serif; font-size: 10pt; color: #A57F35; letter-spacing: .12em; }
.quadro { page: capa; width: 210mm; height: 297mm; box-sizing: border-box; background: #F8F3EE; position: relative; display: flex; flex-direction: column;
          align-items: center; justify-content: center; text-align: center; padding: 30mm; break-before: page; }
.quadro::before { content: ""; position: absolute; top: 14mm; right: 14mm; bottom: 14mm; left: 14mm; border: 2px solid #C9A052; border-radius: 6px; }
.quadro::after { content: ""; position: absolute; top: 18mm; right: 18mm; bottom: 18mm; left: 18mm; border: .8px solid #C9A052; border-radius: 4px; }
.quadro .nomes { font-family: 'Great Vibes', cursive; font-size: 66pt; color: #17295A; line-height: 1.05; margin: 8mm 0 6mm; }
.quadro .l1 { font-family: Cinzel, serif; letter-spacing: .22em; font-size: 11pt; color: #A57F35; }
.quadro .l2 { font-size: 17pt; font-style: italic; color: #2a2338; margin: 2mm 0; }
.quadro .jac { font-family: Cinzel, serif; font-size: 12.5pt; color: #17295A; letter-spacing: .06em; margin-top: 12mm; line-height: 1.6; }
.quadro .dica { position: absolute; bottom: 7mm; left: 0; right: 0; font-family: Outfit, sans-serif; font-size: 8pt; color: #9a93ad; }
.final { text-align: center; } .final p { text-align: center; }
.pequeno { font-family: Outfit, sans-serif; font-size: 9.5pt; color: #6b6385; }
"""


def _doc(titulo, corpo):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(titulo)}</title>'
            f'<style>{_fontes_css()}\n{CSS}</style></head><body>{corpo}</body></html>')


def _p(txt):
    return "".join(f"<p>{E(x.strip())}</p>" for x in re.split(r"\n\s*\n", txt.strip()) if x.strip())


def _oracao(txt):
    return f'<div class="oracao"><p>{E(txt)}</p></div>'


def _secao(kicker, titulo, corpo, nova=True):
    return (f'<section class="{"secao" if nova else ""}"><div class="kicker">{E(kicker)}</div><h2>{E(titulo)}</h2>{DIV}{corpo}</section>')


# ------------------------------------------------------------------ livro principal
def _calendario(ctx):
    pz = ctx["pedido"]; cz = pz["casamento"]; linhas = []
    d_cas = (cz["mes"], cz["dia"] if (cz["mes"], cz["dia"]) != (2, 29) else 28)
    anos = ctx["ANOS_CAL"]; bodas = C.BODAS.get(anos)
    oque = f"Aniversário de casamento: {anos} {'ano' if anos == 1 else 'anos'} juntos{' (' + bodas + ')' if bodas else ''}"
    oque += " e dia de " + ctx["SANTO"] if not ctx["FESTA"] else " e festa: " + ctx["SANTO"]
    linhas.append((d_cas, oque, True))
    for chave, nome in (("SANTO_ELA", ctx["ELA"]), ("SANTO_ELE", ctx["ELE"])):
        st = ctx.get(chave)
        if st:
            linhas.append(((st["mes"], st["dia"] if (st["mes"], st["dia"]) != (2, 29) else 28), f"Aniversário de {nome} e dia de {st['nome']}", True))
    ja = {x[0] for x in linhas}
    for m, d, nome, obs in C.FESTAS_2027:
        if (m, d) not in ja:  # o dia já aparece como aniversário de alguém (ex.: casou ou nasceu no dia de Santo Antônio)
            linhas.append(((m, d), f"{nome}: {obs}", False))
    linhas.sort(key=lambda x: x[0])
    tr = "".join(f'<tr class="{"nosso" if nosso else ""}"><td class="d">{d:02d}/{m:02d} · {SEMANA[dt.date(ANO_CAL, m, d).weekday()].split("-")[0]}</td>'
                 f'<td>{E(o)}</td></tr>' for (m, d), o, nosso in linhas)
    return (_p(f"As datas de vocês em {ANO_CAL} (em destaque) e as festas dos santos que acompanham os casais. Marquem na agenda: no dia do "
               "aniversário de casamento, rezem juntos a renovação das promessas desta página em diante.") + f'<table class="cal">{tr}</table>')


def html_livro(ctx, ia):
    f = lambda t: preencher(t, ctx)
    capa = (f'<div class="capa"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_aliancas(150)}'
            f'<h1>O Santo do<br>Nosso Casamento</h1><div class="nomes">{E(ctx["ELA"])} &amp; {E(ctx["ELE"])}</div>'
            f'<div class="linha">casados em {E(ctx["DATA"])}</div>'
            f'<div class="linha">{"no dia de " + E(ctx["SANTO"]) if not ctx["FESTA"] else "num dia de festa da Igreja: " + E(ctx["SANTO"])}</div>'
            f'<div class="rodape">LIVRO DE ORAÇÕES DO CASAL</div></div>')
    # carta
    ded = ""
    if ctx["MODO"] == "presente" and ctx["PRESENTEADOR"]:
        ded = (f'<div class="caixa"><div class="kicker" style="text-align:left">Um presente de {E(ctx["PRESENTEADOR"])}</div>'
               + (f'<p style="font-style:italic;margin:0">{E(ctx["DEDICATORIA"])}</p>' if ctx["DEDICATORIA"] else "") + "</div>")
    alertas = ""
    if ia.get("_alerta_violencia"):
        alertas += f'<div class="aviso"><b>Antes de tudo:</b> {E(C.AVISO_VIOLENCIA)}</div>'
    if ia.get("_alerta_crise"):
        alertas += ('<div class="aviso"><b>Se a dor estiver pesada demais,</b> você não precisa carregar sozinha ou sozinho. O CVV atende de graça, '
                    'a qualquer hora, pelo telefone 188 ou pelo site cvv.org.br. Procure também um padre ou alguém de confiança.</div>')
    carta = _secao("Para começar", f"{ctx['ELA']} e {ctx['ELE']}", ded + "".join(f"<p>{E(x)}</p>" for x in ia["carta"]) + alertas
                   + f'<p style="text-align:right;font-style:italic;margin-top:6mm">Com carinho,<br>equipe do Meu Santo Protetor</p>')
    # o santo do casamento
    if ctx["FESTA"]:
        abre = f"Vocês se casaram no dia {ctx['DATA_CURTA']}, um dia de festa da Igreja: {ctx['SANTO']}."
    else:
        abre = f"Vocês se casaram no dia {ctx['DATA_CURTA']}. Nesse dia, a Igreja recorda {ctx['SANTO']}."
    santo = (f'<div class="santinho">{svg_aliancas(92, raios=True)}</div><div class="santo-nome">{E(ctx["SANTO"])}</div>'
             + (f'<div class="santo-quem">{E(ctx["SANTO_QUEM"])}</div>' if ctx["SANTO_QUEM"] else '<div class="santo-quem"></div>')
             + _p(abre) + "".join(_p(x) for x in (ia["santo_historia"],)) + "<h3>O que este dia diz ao casamento de vocês</h3>" + _p(ia["santo_casamento"])
             + _oracao(f"{ctx['INVOCACAO']} Rogai a Deus por {ctx['ELA']} e por {ctx['ELE']}, e pelo casamento que começou no vosso dia. Amém."
                       if not ctx["FESTA"] else f"Santa Maria, Mãe de Deus, que celebrais conosco esta festa, rogai a Deus por {ctx['ELA']} e por {ctx['ELE']}. Amém."))
    if ctx.get("SANTO_ELA") or ctx.get("SANTO_ELE"):
        minis = ""
        for nome, st in ((ctx["ELA"], ctx.get("SANTO_ELA")), (ctx["ELE"], ctx.get("SANTO_ELE"))):
            if st:
                minis += (f'<div class="mini"><div class="quem">{E(nome.upper())}</div><div class="st">{E(st["nome"])}</div>'
                          f'<div class="dt">nasceu em {E(data_pt(st["dia"], st["mes"]))}</div></div>')
        santo += ('<div class="cada"><h3>Os santos de cada um</h3>' + _p("Cada um de vocês também nasceu no dia de um santo, que acompanha o casal "
                  "junto com o santo do dia do casamento.") + f'<div class="dois">{minis}</div></div>')
    pagina_santo = _secao("O dia do nosso sim", "O santo do nosso casamento", santo)
    # orações do casal
    oracoes = (_p("Esta é a oração do casamento de vocês, escrita com o nome dos dois e com o que vocês contaram. Rezem juntos, de mãos dadas, "
                  "sempre que quiserem: no aniversário de casamento, num dia difícil, antes de dormir.")
               + _oracao(ia["oracao_casal"]))
    if ctx["MODO"] == "presente":
        oracoes += f"<h3>Para rezar por {E(ctx['ELA'])} e {E(ctx['ELE'])}</h3>" + _oracao(ia["oracao_pessoal"])
    else:
        oracoes += f"<h3>Oração de {E(ctx['QUEM'])} por {E(ctx['CONJ'])}</h3>" + _oracao(ia["oracao_pessoal"])
    oracoes += "<h3>" + ("O sacramento do Matrimônio" if ctx["IGREJA"] else "E o sacramento?") + "</h3>" + _p(C.SACRAMENTO_IGREJA if ctx["IGREJA"] else C.SACRAMENTO_CIVIL)
    pagina_oracoes = _secao("Feita para vocês dois", "A oração do nosso casamento", oracoes)
    # novena
    nov = _p(C.NOVENA_INTRO) + (f'<div class="caixa"><b>A intenção de vocês nesta novena:</b> {E(ia["intencao"])}</div>')
    for i, d in enumerate(C.NOVENA, 1):
        nov += (f'<div class="dia"><div class="num">{i}º DIA</div><h3 style="margin-top:1mm">{E(d["titulo"])}</h3>'
                f'<div class="leitura">Leiam na Bíblia: <b>{E(d["leitura"])}</b></div>{_p(f(d["reflexao"]))}{_oracao(f(d["oracao"]))}'
                f'<div class="pequeno">Lembrem a intenção da novena e rezem um Pai-Nosso, uma Ave-Maria e um Glória.</div></div>')
    pagina_novena = _secao("Nove dias juntos", "Novena do casal", nov)
    # santos dos casais
    sc = _p("Além do santo do dia do casamento, a Igreja tem santos que viveram o casamento e a família de perto. Peçam que eles rezem por vocês.")
    for nome, data, txt in C.SANTOS_CASAIS:
        sc += f'<div class="dia"><h3 style="margin-top:0">{E(nome)}</h3><div class="leitura">Festa: <b>{E(data)}</b></div>{_p(txt)}</div>'
    pagina_santos = _secao("Amigos do Céu", "Os santos dos casais", sc)
    # renovação
    rn = _p(f(C.RENOVACAO_INTRO)) + "<ol class='passos'>" + "".join(f"<li>{E(x)}</li>" for x in C.RENOVACAO_PASSOS) + "</ol>"
    for a, b in ((ctx["ELA"], ctx["ELE"]), (ctx["ELE"], ctx["ELA"])):
        rn += f'<div class="fala"><b>{E(a.upper())}</b><br>{E(preencher(C.RENOVACAO_FALA, ctx, {"A": a, "B": b}))}</div>'
    rn += "<h3>Juntos</h3>" + _oracao(f(C.RENOVACAO_FINAL)) + f'<div class="caixa">{E(C.RENOVACAO_DICA)}</div>'
    pagina_renov = _secao("No aniversário de casamento", "Renovação das promessas em casa", rn)
    # momentos
    mo = _p("Orações curtas para guardar no celular e rezar quando a vida pedir.")
    for tit, txt in C.MOMENTOS:
        mo += f'<div class="dia"><h3 style="margin-top:0">{E(f(tit))}</h3>{_oracao(f(txt))}'
        if tit == "Nos dias difíceis":
            mo += f'<div class="aviso"><b>Importante:</b> {E(C.AVISO_VIOLENCIA)}</div>'
        mo += "</div>"
    pagina_momentos = _secao("Para cada momento", "Orações do dia a dia do casal", mo)
    sempre = "".join(f"<h3>{E(t)}</h3>{_p(x)}" for t, x in C.ORACOES_DE_SEMPRE)
    pagina_sempre = _secao("Para não esquecer", "As orações de sempre", f'<div class="sempre">{sempre}</div>')
    pagina_cal = _secao(f"O ano de {ANO_CAL}", "O calendário do casal", _calendario(ctx))
    quadro = (f'<div class="quadro"><div class="l1">UNIDOS POR DEUS</div><div class="nomes">{E(ctx["ELA"])} &amp; {E(ctx["ELE"])}</div>'
              f'<div class="l2">{E(ctx["DATA"])}</div>'
              f'<div class="l2">{"no dia de " + E(ctx["SANTO"]) if not ctx["FESTA"] else E(ctx["SANTO"])}</div>'
              f'<div style="margin-top:10mm">{svg_aliancas(90, raios=False)}</div>'
              f'<div class="jac">Jesus, Maria e José,<br>a nossa família vos pertence.</div>'
              f'<div class="dica">Para imprimir e emoldurar · tamanho A4</div></div>')
    final = _secao("Antes de terminar", "Uma palavra final", f'<div class="final">{_p(C.PALAVRA_FINAL)}<div style="margin-top:8mm">{svg_vela(90)}</div>'
                   f'<p style="font-family:Cinzel,serif;color:#17295A;margin-top:6mm">{E(ctx["INVOCACAO"])}</p></div>')
    return _doc(f"O Santo do Nosso Casamento - {ctx['ELA']} e {ctx['ELE']}",
                capa + carta + pagina_santo + pagina_oracoes + pagina_novena + pagina_santos + pagina_renov + pagina_momentos
                + pagina_sempre + pagina_cal + quadro + final)


# ------------------------------------------------------------------ 30 dias
def html_marido(ctx):
    nome, gen = ctx["CONJ"], ctx["GEN_CONJ"]
    g = ctx_genero(nome, gen)
    f = lambda t: preencher(t, ctx, g)
    titulo = f"30 Dias Rezando {'pelo' if gen == 'm' else 'pela'} {nome}"
    capa = (f'<div class="capa clara"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_vela(120)}'
            f'<h1>30 Dias Rezando<br>{"pelo Meu Marido" if gen == "m" else "pela Minha Esposa"}</h1>'
            f'<div class="nomes">{E(nome)}</div><div class="linha">um tema, uma oração e um gesto para cada dia</div>'
            f'<div class="rodape" style="color:#A57F35">PREPARADO PARA {E(ctx["QUEM"].upper())}</div></div>')
    intro = _p(f(C.TRINTA_INTRO))
    if gen == "m":
        intro += f'<div class="aviso"><b>Importante:</b> {E(C.AVISO_VIOLENCIA)}</div>'
    corpo = ""
    for i, (tema, ref, ora, gesto) in enumerate(C.TRINTA, 1):
        corpo += (f'<div class="dia"><div class="num">DIA {i}</div><h3 style="margin-top:1mm">{E(f(tema))}</h3>'
                  f'<div class="leitura">Para ler: <b>{E(ref)}</b></div>{_oracao(f(ora))}<span class="gesto">Gesto de hoje: {E(f(gesto))}</span></div>')
    fim = _secao("E agora?", "A oração continua", f'<div class="final">{_p(f(C.TRINTA_FINAL))}{_p(C.PALAVRA_FINAL)}</div>')
    return _doc(titulo, capa + _secao("Como rezar", titulo, intro, nova=True) + _secao("Os 30 dias", f"Por {nome}", corpo) + fim)


# ------------------------------------------------------------------ Santa Rita
def html_rita(ctx, pedido_txt):
    conj = ctx["CONJ"]
    f = lambda t: preencher(t, ctx, {"PEDIDO": pedido_txt})
    capa = (f'<div class="capa"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_rosa(130, "#E9CF93")}'
            f'<h1>Novena de Santa Rita<br>pelo Casamento</h1><div class="nomes">{E(ctx["ELA"])} &amp; {E(ctx["ELE"])}</div>'
            f'<div class="linha">nove dias com a santa das causas impossíveis</div><div class="rodape">22 DE MAIO · FESTA DE SANTA RITA</div></div>')
    quem = _p(C.RITA_QUEM) + _p(C.RITA_INTRO) + f'<div class="caixa"><b>O seu pedido nesta novena:</b> {E(pedido_txt)}</div>' \
        + f'<div class="aviso"><b>Importante:</b> {E(C.AVISO_VIOLENCIA)}</div>'
    dias = ""
    for i, (tit, hist, ora) in enumerate(C.RITA, 1):
        dias += (f'<div class="dia"><div class="num">{i}º DIA</div><h3 style="margin-top:1mm">{E(tit)}</h3>{_p(f(hist))}{_oracao(f(ora))}'
                 f'<div class="pequeno">Reze um Pai-Nosso, uma Ave-Maria e um Glória. Santa Rita de Cássia, rogai por nós.</div></div>')
    fim = _secao("Antes de terminar", "Uma palavra final", f'<div class="final">{_p(C.PALAVRA_FINAL)}<div>{svg_rosa(80)}</div></div>')
    return _doc("Novena de Santa Rita pelo Casamento", capa + _secao("Quem foi", "Santa Rita de Cássia", quem) + _secao("Os nove dias", "A novena", dias) + fim)


# ------------------------------------------------------------------ HTML → PDF
def _chrome_bin():
    cands = [os.environ.get("CASAMENTO_CHROME", "")] + [shutil.which(x) or "" for x in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")]
    for pat in ("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome", "/root/.cache/ms-playwright/chromium-*/chrome-linux*/chrome",
                "/home/*/.cache/ms-playwright/chromium-*/chrome-linux*/chrome", "/opt/pw-browsers/chromium-*/chrome-linux*/chrome"):
        import glob
        cands += sorted(glob.glob(os.path.expanduser(pat)), reverse=True)
    return next((c for c in cands if c and os.path.exists(c)), None)


def _motor_playwright(html, arq):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        try:
            pg = b.new_page()
            pg.set_content(html, wait_until="load")
            pg.pdf(path=str(arq), print_background=True, prefer_css_page_size=True)
        finally:
            b.close()


def _motor_weasyprint(html, arq):
    from weasyprint import HTML
    HTML(string=html, base_url=str(BASE)).write_pdf(str(arq))


def _motor_chromium(html, arq):
    exe = _chrome_bin()
    if not exe:
        raise RuntimeError("Chromium não encontrado")
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "doc.html"; src.write_text(html, encoding="utf-8")
        r = subprocess.run([exe, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                            f"--user-data-dir={tmp}/perfil", f"--print-to-pdf={arq}", src.as_uri()], capture_output=True, timeout=180)
        if not pathlib.Path(arq).exists() or pathlib.Path(arq).stat().st_size < 1000:
            raise RuntimeError(f"chromium falhou: {r.stderr.decode(errors='ignore')[-300:]}")


MOTORES = (("playwright", _motor_playwright), ("weasyprint", _motor_weasyprint), ("chromium", _motor_chromium))


def gerar_pdf(html, arq, motor=None):
    """Grava o PDF e devolve o nome do motor que funcionou."""
    arq = pathlib.Path(arq); erros = []
    preferido = motor or os.environ.get("CASAMENTO_PDF_MOTOR", "")
    ordem = sorted(MOTORES, key=lambda m: m[0] != preferido)
    for nome, fn in ordem:
        try:
            arq.unlink(missing_ok=True)
            fn(html, arq)
            if arq.exists() and arq.stat().st_size > 1000:
                return nome
        except Exception as e:
            erros.append(f"{nome}: {type(e).__name__}: {str(e)[:160]}")
    raise RuntimeError("Nenhum gerador de PDF funcionou → " + " | ".join(erros))
