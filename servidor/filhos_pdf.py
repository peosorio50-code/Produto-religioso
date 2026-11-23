"""Novena pelos Filhos: monta o HTML dos PDFs e converte em PDF.

PDFs:
  novena   Novena pelos Filhos (produto principal): o livro que acompanha os 9 vídeos
  bencaos  30 Bênçãos para Mandar aos Filhos (order bump)
  terco    Terço pelos Filhos (order bump): o roteiro que acompanha o vídeo do terço
  livros   Um Livro para Cada Filho (upsell): um PDF para cada filho ou neto vivo

Conversão HTML → PDF: tenta, nesta ordem, Playwright (Python), WeasyPrint e o Chromium pela linha de comando.
Para saber qual funciona na VPS: ./venv/bin/python filhos.py diagnostico
"""
import base64, datetime as dt, glob, html as H, math, os, pathlib, re, shutil, subprocess, tempfile

import filhos_conteudo as C

BASE = pathlib.Path(__file__).parent
FONTES = BASE / "filhos_fontes" if (BASE / "filhos_fontes").exists() else BASE / "casamento_fontes"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
E = H.escape
MAX_FILHOS = 6

PREFIXOS_SANTO = ("são ", "santo ", "santa ", "santos ", "santas ", "beato", "beata", "bem-aventurad", "nossa senhora", "virgem",
                  "imaculad", "todos os santos", "os santos", "anjo", "arcanjo", "sagrado coração de maria", "maria, mãe")
PAPEIS = {  # papel → (como se chama, terminação, "sua mãe", assinatura)
    "mae": ("mãe", "a", "sua mãe", "mãe"), "avo_f": ("avó", "a", "sua avó", "vó"),
    "pai": ("pai", "o", "seu pai", "pai"), "avo_m": ("avô", "o", "seu avô", "vô"),
}
RELS = ("filho", "filha", "neto", "neta")


# ------------------------------------------------------------------ dados → marcadores
def data_pt(d, m, a=None):
    return f"{d} de {MESES[m - 1]}" + (f" de {a}" if a else "")


def eh_festa(nome):
    """True quando o dia é uma festa do Senhor (Natal, Batismo do Senhor, Santa Cruz...), e não um santo que intercede."""
    return not (nome or "").strip().lower().startswith(PREFIXOS_SANTO)


def primeiro(nome):
    p = (nome or "").strip().split()
    return p[0].capitalize() if p else ""


def lista(nomes):
    nomes = [n for n in nomes if n]
    return nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1] if nomes else ""


def fase(ano, hoje=None):
    if not ano:
        return ""
    idade = (hoje or dt.date.today()).year - int(ano)
    return "crianca" if idade < 13 else "jovem" if idade < 30 else "adulto"


def genero_pessoa(nome, rel):
    """Marcadores de uma pessoa: {N} {o} {ele} {Ele} {dele} {filho}."""
    f = rel in ("filha", "neta")
    return {"N": nome, "o": "a" if f else "o", "ele": "ela" if f else "ele", "Ele": "Ela" if f else "Ele", "dele": "dela" if f else "dele",
            "filho": rel}


def _concordancia(fem, plural):
    if plural:
        e = "elas" if fem else "eles"
        return {"eles": e, "Eles": e.capitalize(), "deles": "d" + e, "os": "as" if fem else "os", "lhes": "lhes",
                "cada_um": "cada uma delas" if fem else "cada um deles", "Cada_um": "Cada uma delas" if fem else "Cada um deles",
                "estao": "estão", "Eles_sao": e.capitalize() + " são", "saibam": "saibam", "estiverem": "estiverem", "precisam": "precisam",
                "estejam": "estejam", "Anjos": "Santos Anjos da Guarda"}
    e = "ela" if fem else "ele"
    return {"eles": e, "Eles": e.capitalize(), "deles": "d" + e, "os": "a" if fem else "o", "lhes": "lhe", "cada_um": e, "Cada_um": e.capitalize(),
            "estao": "está", "Eles_sao": e.capitalize() + " é", "saibam": "saiba", "estiverem": "estiver", "precisam": "precisa",
            "estejam": "esteja", "Anjos": "Santo Anjo da Guarda"}


def _palavra_grupo(pessoas):
    """'filhos', 'netas', 'filhos e netos'... e o artigo: ('os meus filhos', 'filhos', título)."""
    filhos = [p for p in pessoas if p["rel"] in ("filho", "filha")]
    netos = [p for p in pessoas if p["rel"] in ("neto", "neta")]
    partes = []
    for grupo, m, f in ((filhos, "filho", "filha"), (netos, "neto", "neta")):
        if grupo:
            fem = all(p["rel"] == f for p in grupo)
            partes.append(((f if fem else m) + ("s" if len(grupo) > 1 else ""), fem, len(grupo)))
    palavra = " e ".join(x[0] for x in partes)
    fem = all(x[1] for x in partes); n = sum(x[2] for x in partes)
    art = ("as minhas " if fem else "os meus ") if n > 1 else ("a minha " if fem else "o meu ")
    if len(partes) == 2 and n > 1:  # "os meus filhos e netos"
        art = "as minhas " if fem else "os meus "
    titulo = "Novena pelos Filhos e Netos" if len(partes) == 2 else "Novena pelos Netos" if netos else "Novena pelos Filhos"
    return art + palavra, palavra, titulo


CONTRACOES = {"os meus ": ("dos meus ", "pelos meus ", "aos meus "), "as minhas ": ("das minhas ", "pelas minhas ", "às minhas "),
              "o meu ": ("do meu ", "pelo meu ", "ao meu "), "a minha ": ("da minha ", "pela minha ", "à minha ")}


def _contrai(os_filhos):
    """'os meus filhos' → ('dos meus filhos', 'pelos meus filhos', 'aos meus filhos')."""
    for art, (de, por, a) in CONTRACOES.items():
        if os_filhos.startswith(art):
            resto = os_filhos[len(art):]
            return de + resto, por + resto, a + resto
    return "de " + os_filhos, "por " + os_filhos, "a " + os_filhos


def contexto(pedido, santos, hoje=None):
    """Tudo o que os modelos de página precisam, já em texto. santos = lista na mesma ordem de pedido['filhos']."""
    hoje = hoje or dt.date.today()
    papel = pedido.get("papel") if pedido.get("papel") in PAPEIS else "mae"
    p_nome, q_o, seu_papel, assin = PAPEIS[papel]
    pessoas = []
    for f, st in zip(pedido["filhos"], santos):
        nome = primeiro(f["nome"]); festa = eh_festa(st["nome"])
        pessoas.append({"nome": nome, "rel": f.get("rel") if f.get("rel") in RELS else "filho", "dia": f["dia"], "mes": f["mes"],
                        "ano": f.get("ano"), "partiu": bool(f.get("partiu")), "fase": fase(f.get("ano"), hoje), "santo": st, "festa": festa,
                        "invocacao": "Santa Maria, Mãe de Deus" if festa else st["nome"],
                        "data": data_pt(f["dia"], f["mes"])})
    vivos_reais = [p for p in pessoas if not p["partiu"]]
    vivos = vivos_reais or pessoas  # se todos já partiram, a novena reza por todos pelo nome, sem a frase à parte
    partiram = [p for p in pessoas if p["partiu"]] if vivos_reais else []
    os_filhos, filhos, titulo = _palavra_grupo(vivos)
    fem = all(p["rel"] in ("filha", "neta") for p in vivos)
    ctx = {"QUEM": primeiro(pedido.get("quem", {}).get("nome") or "") or p_nome.capitalize(), "PAPEL": p_nome, "Q_o": q_o,
           "SEU_PAPEL": seu_papel, "ASSIN": assin, "PAPEL_KEY": papel,
           "NOMES": lista([p["nome"] for p in vivos]), "TODOS": lista([p["nome"] for p in pessoas]),
           "OS_FILHOS": os_filhos, "FILHOS": filhos, "TITULO": titulo,
           "DOS_FILHOS": _contrai(os_filhos)[0], "PELOS_FILHOS": _contrai(os_filhos)[1], "AOS_FILHOS": _contrai(os_filhos)[2],
           "um_deles": (("uma delas" if fem else "um deles") if len(vivos) > 1 else vivos[0]["nome"]),
           "INVOCACOES": " ".join(f"{p['invocacao']}, rogai por {p['nome']}." for p in pessoas),
           "FALECIDOS": (f"Lembrai-Vos também de {lista([p['nome'] for p in partiram])}, que já {'partiram' if len(partiram) > 1 else 'partiu'} "
                         f"para junto de Vós: dai-{'lhes' if len(partiram) > 1 else 'lhe'} o descanso eterno. ") if partiram else "",
           "pessoas": pessoas, "vivos": vivos, "vivos_reais": vivos_reais, "partiram": partiram, "pedido": pedido, "AREA": "", "hoje": hoje}
    ctx.update(_concordancia(fem, len(vivos) > 1))
    return ctx


def preencher(txt, ctx, extra=None):
    trocas = {k: str(v) for k, v in ctx.items() if isinstance(v, (str, int)) and not isinstance(v, bool)}
    trocas.update(extra or {})
    return re.sub(r"\{([A-Za-z_]+)\}", lambda m: trocas.get(m.group(1), m.group(0)), txt)


def situacao_nome(ctx):
    vivos = ctx["vivos"]
    return vivos[0]["nome"] if len(vivos) == 1 else "(nome)"


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


def svg_manto(tam=150, cor="#C9A052", raios=True):
    """Coroa de doze estrelas sobre um manto aberto (Nossa Senhora), com raios atrás."""
    r = ""
    if raios:
        for i in range(36):
            a = math.radians(i * 10); c1, c2 = 50, 74 if i % 2 else 66
            r += (f'<line x1="{75 + c1 * math.cos(a):.1f}" y1="{80 + c1 * math.sin(a):.1f}" x2="{75 + c2 * math.cos(a):.1f}" '
                  f'y2="{80 + c2 * math.sin(a):.1f}" stroke="{cor}" stroke-width="{1.2 if i % 2 else 0.7}" opacity=".5"/>')
    est = ""
    for i in range(12):
        a = math.radians(200 + i * (140 / 11)); x, y = 75 + 40 * math.cos(a), 62 + 40 * math.sin(a)
        est += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{cor}"/>'
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">{r}{est}'
            f'<path d="M75 44 C60 58 52 86 44 120 Q75 128 106 120 C98 86 90 58 75 44 Z" fill="none" stroke="{cor}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="75" cy="58" r="8" fill="none" stroke="{cor}" stroke-width="3.5"/>'
            f'<path d="M75 76 v30 M65 86 h20" stroke="{cor}" stroke-width="3.5" stroke-linecap="round"/></svg>')


def svg_vela(tam=110, cor="#C9A052"):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{cor}" stroke-width="3" stroke-linecap="round">'
            '<path d="M55 14c6 9 9 15 9 20a9 9 0 0 1-18 0c0-5 3-11 9-20z"/><path d="M42 50h26v46H42z"/><path d="M55 44v6"/><path d="M34 96h42"/></svg>')


def svg_rosario(tam=110, cor="#C9A052"):
    contas = "".join(f'<circle cx="{55 + 34 * math.cos(math.radians(a)):.1f}" cy="{44 + 30 * math.sin(math.radians(a)):.1f}" r="3.2" fill="{cor}"/>'
                     for a in range(0, 360, 18) if not 75 < a < 105)
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">{contas}'
            f'<path d="M55 74 v10 M55 88 v16 M48 94 h14" stroke="{cor}" stroke-width="3" stroke-linecap="round" fill="none"/></svg>')


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
.capa .marca { font-family: Cinzel, serif; letter-spacing: .32em; font-size: 9.5pt; color: #E9CF93; margin-bottom: 12mm; }
.capa h1 { font-family: Cinzel, serif; font-weight: 500; font-size: 25pt; letter-spacing: .08em; line-height: 1.25; margin: 6mm 0 2mm; color: #F5ECD9; }
.capa .nomes { font-family: 'Great Vibes', cursive; font-size: 48pt; color: #E9CF93; line-height: 1.12; margin: 8mm 0 4mm; }
.capa .nomes.muitos { font-size: 36pt; } .capa .nomes.muitissimos { font-size: 29pt; }
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
.diapag { break-before: page; }
.num { font-family: Cinzel, serif; color: #A57F35; font-size: 10pt; letter-spacing: .2em; text-align: center; }
.gesto { font-family: Outfit, sans-serif; font-size: 10pt; color: #4b4560; background: #f1e8d8; border-radius: 6px; padding: 2.5mm 3.5mm; margin: 2mm 0 3mm; break-inside: avoid; }
.gesto b { color: #17295A; }
.santinho { text-align: center; margin: 0 0 2mm; }
.cada { break-inside: avoid; }
.santo-nome { font-family: Cinzel, serif; font-size: 18pt; color: #17295A; text-align: center; margin: 1mm 0; letter-spacing: .03em; line-height: 1.25; }
.santo-quem { text-align: center; font-style: italic; color: #6b6385; margin: 0 0 3mm; }
.cartao { border: 1px solid #e2cf9f; background: #fffaf0; border-radius: 12px; padding: 5mm 6mm 3mm; margin: 0 0 6mm; break-inside: avoid; }
.cartao .quem { font-family: Cinzel, serif; font-size: 9pt; letter-spacing: .22em; color: #A57F35; text-align: center; }
.cartao .nome { font-family: 'Great Vibes', cursive; font-size: 30pt; color: #17295A; text-align: center; line-height: 1.1; margin: 1mm 0 0; }
.aviso { font-family: Outfit, sans-serif; font-size: 10.2pt; line-height: 1.5; border: 1px solid #d9b8a0; background: #fff3ea; border-radius: 8px; padding: 3.5mm 4.5mm; margin: 4mm 0; break-inside: avoid; }
.aviso b { color: #7a3414; }
.caixa { border: 1px solid #e2cf9f; background: #fffaf0; border-radius: 10px; padding: 4mm 5mm; margin: 4mm 0; break-inside: avoid; }
.link { font-family: Outfit, sans-serif; font-size: 10pt; word-break: break-all; color: #17295A; }
ul.dicas { padding-left: 5mm; margin: 0 0 4mm; } ul.dicas li { margin-bottom: 2mm; }
ol.passos { padding-left: 6mm; margin: 0 0 4mm; } ol.passos li { margin-bottom: 2mm; }
.licoes { margin: 2mm 0 4mm; } .licoes > div { border: 1px solid #eadfca; border-radius: 8px; padding: 2.5mm 4mm; margin: 0 0 2.5mm; break-inside: avoid; }
.licoes b { font-family: Cinzel, serif; font-size: 10pt; color: #17295A; letter-spacing: .05em; display: block; margin-bottom: 1mm; }
.licoes span { font-size: 12.5pt; }
.citacao { text-align: center; font-style: italic; font-size: 17pt; color: #17295A; margin: 5mm 8mm; line-height: 1.35; }
.citacao small { display: block; font-family: Outfit, sans-serif; font-style: normal; font-size: 9pt; color: #6b6385; margin-top: 2mm; }
.sempre h3 { margin-top: 4mm; }
.msgs { counter-reset: m; padding: 0; margin: 0; list-style: none; }
.msgs li { counter-increment: m; position: relative; padding: 1.6mm 0 1.6mm 10mm; border-bottom: 1px solid #f0e6d3; font-size: 13pt; line-height: 1.4; break-inside: avoid; }
.msgs li::before { content: counter(m); position: absolute; left: 0; top: 1.8mm; font-family: Cinzel, serif; font-size: 9.5pt; color: #A57F35; }
.ajuda { font-family: Outfit, sans-serif; font-size: 9.8pt; line-height: 1.45; border: 1px solid #e2cf9f; border-radius: 8px; padding: 3mm 4.5mm; margin: 4mm 0; break-inside: avoid; }
.ajuda b { color: #17295A; } .ajuda div { margin: 1.2mm 0; }
.quadro { page: capa; width: 210mm; height: 297mm; box-sizing: border-box; background: #F8F3EE; position: relative; display: flex; flex-direction: column;
          align-items: center; justify-content: center; text-align: center; padding: 30mm 28mm; break-before: page; }
.quadro::before { content: ""; position: absolute; top: 14mm; right: 14mm; bottom: 14mm; left: 14mm; border: 2px solid #C9A052; border-radius: 6px; }
.quadro::after { content: ""; position: absolute; top: 18mm; right: 18mm; bottom: 18mm; left: 18mm; border: .8px solid #C9A052; border-radius: 4px; }
.quadro .l1 { font-family: Cinzel, serif; letter-spacing: .22em; font-size: 11pt; color: #A57F35; }
.quadro .t { font-family: Cinzel, serif; font-size: 20pt; color: #17295A; margin: 4mm 0 6mm; letter-spacing: .05em; line-height: 1.3; }
.quadro .fil { margin: 1.6mm 0; } .quadro .fil b { font-family: 'Great Vibes', cursive; font-weight: normal; font-size: 30pt; color: #17295A; display: block; line-height: 1.05; }
.quadro .fil span { font-style: italic; font-size: 12.5pt; color: #6b6385; }
.quadro .jac { font-family: Cinzel, serif; font-size: 12pt; color: #17295A; letter-spacing: .06em; margin-top: 9mm; line-height: 1.6; }
.quadro .data { font-size: 13pt; color: #4b4560; margin-top: 8mm; }
.quadro .dica { position: absolute; bottom: 7mm; left: 0; right: 0; font-family: Outfit, sans-serif; font-size: 8pt; color: #9a93ad; }
.recorte { border: 1.5px dashed #C9A052; border-radius: 10px; width: 70mm; margin: 6mm auto; padding: 6mm 5mm; text-align: center; background: #fffaf0; break-inside: avoid; }
.recorte .st { font-family: Cinzel, serif; font-size: 13pt; color: #17295A; margin: 2mm 0; }
.recorte .r { font-style: italic; font-size: 12pt; }
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


def _secao(kicker, titulo, corpo, nova=True, classe=""):
    return (f'<section class="{"secao" if nova else ""} {classe}"><div class="kicker">{E(kicker)}</div><h2>{E(titulo)}</h2>{DIV}{corpo}</section>')


def _classe_nomes(txt):
    return "muitissimos" if len(txt) > 34 else "muitos" if len(txt) > 20 else ""


def _ajuda(ctx):
    return (f'<div class="ajuda"><div>{E(preencher(C.AJUDA_INTRO, ctx))}</div>'
            + "".join(f"<div><b>{E(t)}:</b> {E(x)}</div>" for t, x in C.AJUDA) + "</div>")


def _alertas(ia, ctx):
    a = ""
    if ia.get("_alerta_crise"):
        a += ('<div class="aviso"><b>Se a dor estiver pesada demais,</b> ninguém precisa carregar isso sozinho. O CVV atende de graça, a qualquer hora, '
              'pelo telefone 188 ou pelo site cvv.org.br. Em caso de risco, ligue 192 (SAMU). Procure também um padre ou alguém de confiança.</div>')
    if ia.get("_alerta_violencia"):
        a += ('<div class="aviso"><b>Antes de tudo:</b> rezar nunca significa aceitar violência. Se alguém da casa está em perigo, procure ajuda: '
              '190 (Polícia), 180 (Central de Atendimento à Mulher) ou Disque 100 (crianças e adolescentes), todos gratuitos.</div>')
    if ia.get("_alerta_vicio"):
        a += (f'<div class="aviso"><b>Você não está sozinh{ctx["Q_o"]}.</b> Os CAPS AD do SUS atendem de graça quem luta contra o álcool e as drogas, '
              'e grupos como Al-Anon, Nar-Anon e Amor-Exigente apoiam as famílias. Rezar e buscar ajuda andam juntos.</div>')
    return a


# ------------------------------------------------------------------ livro principal
def html_novena(ctx, ia):
    f = lambda t: preencher(t, ctx)
    nomes_capa = " · ".join(p["nome"] for p in ctx["pessoas"])
    capa = (f'<div class="capa"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_manto(150)}'
            f'<h1>{E(ctx["TITULO"]).replace(" pelos ", "<br>pelos ")}</h1>'
            f'<div class="nomes {_classe_nomes(nomes_capa)}">{E(nomes_capa)}</div>'
            f'<div class="linha">com a oração de {E(ctx["QUEM"])}</div>'
            f'<div class="rodape">9 DIAS COM SANTA MÔNICA E NOSSA SENHORA</div></div>')
    carta = _secao("Para começar", ctx["QUEM"], "".join(f"<p>{E(x)}</p>" for x in ia["carta"]) + _alertas(ia, ctx)
                   + '<p style="text-align:right;font-style:italic;margin-top:6mm">Com carinho,<br>equipe do Meu Santo Protetor</p>')
    como = _p(f(C.COMO_REZAR))
    if ctx.get("AREA"):
        como += (f'<div class="caixa"><b>Os vídeos da sua novena estão aqui:</b><br><span class="link">{E(ctx["AREA"])}</span><br>'
                 '<span class="pequeno">Guarde este link. Ele também está no e-mail da compra.</span></div>')
    como += "<ul class='dicas'>" + "".join(f"<li>{E(f(x))}</li>" for x in C.COMO_REZAR_DICAS) + "</ul>"
    como += f'<div class="caixa"><b>A intenção desta novena:</b> {E(ia["intencao"])}.</div>'
    pag_como = _secao("Antes do primeiro dia", "Como rezar esta novena", como)
    # os santos de cada um
    st_html = _p(f"Todo dia do ano a Igreja recorda um santo ou celebra uma festa. Estes são os santos dos dias em que {ctx['TODOS']} "
                 f"{'nasceram' if len(ctx['pessoas']) > 1 else 'nasceu'}. Eles não ocupam o lugar de Deus: são amigos no Céu que rezam conosco.")
    for i, p in enumerate(ctx["pessoas"]):
        st = p["santo"]; txt = ia["filhos"][i]["santo_texto"]
        quem = f'{p["rel"].upper()} · NASCEU EM {p["data"].upper()}' + (" · JÁ ESTÁ COM DEUS" if p["partiu"] else "")
        invoc = (f"Santa Maria, Mãe de Deus, rogai por {p['nome']}." if p["festa"] else f"{st['nome']}, rogai por {p['nome']}.")
        st_html += (f'<div class="cartao"><div class="quem">{E(quem)}</div><div class="nome">{E(p["nome"])}</div>'
                    f'<div class="santo-nome">{E(("Festa: " if p["festa"] else "") + st["nome"])}</div>'
                    + (f'<div class="santo-quem">{E(st.get("quem") or "")}</div>' if st.get("quem") else "")
                    + _p(txt) + f'<p style="text-align:center;font-family:Cinzel,serif;color:#A57F35;font-size:11pt">{E(invoc)}</p></div>')
    pag_santos = _secao("O dia em que cada um nasceu", "Os santos de cada um", st_html)
    # a oração de cada um
    or_html = _p(f"Uma oração para cada um, pelo nome. Reze a de cada um no dia que quiser, ou todas juntas, no fim de cada dia da novena.")
    for i, p in enumerate(ctx["pessoas"]):
        or_html += f'<div class="cada"><h3>Por {E(p["nome"])}</h3>{_oracao(ia["filhos"][i]["oracao"])}</div>'
    pag_oracoes = _secao("Pelo nome", "A oração de cada um", or_html)
    # Santa Mônica
    mon = "".join(_p(x) for x in C.MONICA_HISTORIA[:1]) + "".join(_p(x) for x in C.MONICA_HISTORIA[1:2])
    mon += ('<div class="citacao">"Não é possível que se perca o filho de tantas lágrimas."<small>dito a Santa Mônica · Santo Agostinho, Confissões, III, 12</small></div>')
    mon += "".join(_p(x) for x in C.MONICA_HISTORIA[2:])
    mon += "<div class='cada'><h3>O que Santa Mônica ensina a quem reza pelos filhos</h3><div class='licoes'>" + "".join(
        f"<div><b>{E(t)}</b><span>{E(x)}</span></div>" for t, x in C.MONICA_LICOES) + "</div></div>"
    mon += "<h3>Oração a Santa Mônica</h3>" + _oracao(f(C.MONICA_ORACAO))
    pag_monica = _secao("A mãe que não desistiu", "Santa Mônica", mon)
    # novena
    dias = ""
    for i, d in enumerate(C.NOVENA, 1):
        dias += (f'<section class="diapag"><div class="num">{i}º DIA DA NOVENA</div><h2>{E(d["titulo"])}</h2>{DIV}'
                 f'<div class="leitura" style="text-align:center">Leia na sua Bíblia: <b>{E(d["leitura"])}</b> · vídeo do {i}º dia</div>'
                 f'{_p(f(d["reflexao"]))}<h3>Oração do dia</h3>{_oracao(f(d["oracao"]))}'
                 f'<div class="gesto"><b>Gesto do dia:</b> {E(f(d["gesto"]))}</div>'
                 f'<p class="pequeno" style="text-align:center">{E(f(C.FECHO_DIA))}</p></section>')
    abre_nov = _secao("Nove dias", ctx["TITULO"], _p(f"Os nove dias abaixo são os mesmos dos nove vídeos. Em cada um: leia a passagem na sua Bíblia, "
                                                     f"a reflexão e a oração, faça o gesto do dia e termine com um Pai-Nosso, uma Ave-Maria e um Glória.")
                       + f'<div class="caixa"><b>Por quem você reza:</b> {E(ctx["TODOS"])}.<br><b>A intenção:</b> {E(ia["intencao"])}.</div>'
                       + "<h3>Os nove dias</h3><ol class='passos'>" + "".join(f"<li>{E(d['titulo'])}</li>" for d in C.NOVENA) + "</ol>")
    # consagração
    cons = _p(f(C.CONSAGRACAO_INTRO)) + "<h3>Ato de consagração</h3>" + _oracao(f(C.CONSAGRACAO_ATO))
    pag_cons = _secao("No nono dia", "Consagração a Nossa Senhora", cons)
    cert = (f'<div class="quadro"><div style="margin-bottom:4mm">{svg_manto(90, raios=False)}</div><div class="l1">CONSAGRADOS A NOSSA SENHORA</div>'
            f'<div class="t">Debaixo do vosso manto</div>'
            + "".join(f'<div class="fil"><b>{E(p["nome"])}</b></div>' for p in ctx["vivos"])
            + f'<div class="data">por {E(ctx["QUEM"])}, em ____ de ______________ de ________</div>'
            f'<div class="jac">Nossa Senhora,<br>cobri-{E(ctx["os"])} com o vosso manto.</div>'
            f'<div class="dica">Para imprimir, assinar no dia da consagração e guardar · tamanho A4</div></div>')
    # bênção
    ben = _p(C.BENCAO_INTRO) + "<ol class='passos'>" + "".join(f"<li>{E(f(x))}</li>" for x in C.BENCAO_PASSOS) + "</ol>"
    for p in ctx["vivos"]:
        ben += f'<div class="cada"><h3>Para {E(p["nome"])}</h3>{_oracao(preencher(C.BENCAO, ctx, {"N": p["nome"]}))}</div>'
    ben += f'<p class="pequeno">{E(C.BENCAO_FONTE)}</p>'
    pag_ben = _secao(f"A bênção da {ctx['PAPEL']}" if ctx["Q_o"] == "a" else f"A bênção do {ctx['PAPEL']}", "Como abençoar", ben)
    # situações
    sn = situacao_nome(ctx)
    sit = _p("Orações curtas para guardar no celular e rezar quando a vida pedir." + (" Onde aparece (nome), diga o nome de quem precisa." if sn == "(nome)" else ""))
    for t, x in C.SITUACOES:
        if t.startswith("Por um filho ou neto que já partiu") and not ctx["partiram"]:
            continue
        nome_sit = ctx["partiram"][0]["nome"] if t.startswith("Por um filho ou neto que já partiu") and len(ctx["partiram"]) == 1 else sn
        sit += f'<div class="dia"><h3 style="margin-top:0">{E(f(t))}</h3>{_oracao(preencher(x, ctx, {"N": nome_sit}))}</div>'
    sit += _ajuda(ctx)
    pag_sit = _secao("Para cada momento", "Orações para cada situação", sit)
    sempre = "".join(f"<h3>{E(t)}</h3>{_p(x)}" for t, x in C.ORACOES_DE_SEMPRE)
    pag_sempre = _secao("Para não esquecer", "As orações de sempre", f'<div class="sempre">{sempre}</div>')
    quadro = (f'<div class="quadro"><div class="l1">{"OS FILHOS QUE DEUS ME CONFIOU" if "neto" not in ctx["FILHOS"] else "OS QUE DEUS ME CONFIOU"}</div>'
              f'<div class="t">{E(ctx["TITULO"])}</div>'
              + "".join(f'<div class="fil"><b>{E(p["nome"])}</b><span>{E(p["data"])} · '
                        f'{E(p["santo"]["nome"] if not p["festa"] else "festa: " + p["santo"]["nome"])}</span></div>' for p in ctx["pessoas"])
              + '<div class="jac">Jesus, Maria e José,<br>a nossa família vos pertence.</div>'
              '<div class="dica">Para imprimir e emoldurar · tamanho A4</div></div>')
    final = _secao("Antes de terminar", "Uma palavra final", f'<div class="final">{_p(C.PALAVRA_FINAL)}{_ajuda(ctx)}<div style="margin-top:6mm">{svg_vela(80)}</div>'
                   f'<p style="font-family:Cinzel,serif;color:#17295A;margin-top:5mm">Santa Mônica, rogai por nós.<br>Nossa Senhora, cobri-{E(ctx["os"])} com o vosso manto.</p></div>')
    return _doc(f"{ctx['TITULO']} - {ctx['TODOS']}",
                capa + carta + pag_como + pag_santos + pag_oracoes + pag_monica + abre_nov + dias + pag_cons + cert + pag_ben
                + pag_sit + pag_sempre + quadro + final)


# ------------------------------------------------------------------ 30 bênçãos
def bencaos_de(ctx, p):
    g = genero_pessoa(p["nome"], p["rel"])
    return [preencher(x, ctx, g) for x in C.BENCAOS]


def html_bencaos(ctx):
    f = lambda t: preencher(t, ctx)
    nomes = " · ".join(p["nome"] for p in ctx["vivos"])
    capa = (f'<div class="capa clara"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_vela(120)}'
            f'<h1>30 Bênçãos para<br>Mandar aos {"Netos" if ctx["FILHOS"].startswith("net") else "Filhos"}</h1>'
            f'<div class="nomes {_classe_nomes(nomes)}" style="color:#A57F35">{E(nomes)}</div>'
            f'<div class="linha">uma mensagem por dia, já com o nome</div>'
            f'<div class="rodape" style="color:#A57F35">PREPARADO PARA {E(ctx["QUEM"].upper())}</div></div>')
    intro = _secao("Como usar", "Uma bênção por dia", _p(f(C.BENCAOS_INTRO)) + '<div class="caixa">Dica: mande de manhã cedo, antes de o dia '
                   'começar. Uma frase curta, sem cobrança, costuma ser recebida com mais carinho do que um sermão.</div>')
    corpo = ""
    for p in ctx["vivos"]:
        corpo += _secao("30 dias", f"Para {p['nome']}", "<ol class='msgs'>" + "".join(f"<li>{E(x)}</li>" for x in bencaos_de(ctx, p)) + "</ol>")
    fim = _secao("Antes de terminar", "Uma palavra final", f'<div class="final">{_p(C.PALAVRA_FINAL)}</div>')
    return _doc("30 Bênçãos para Mandar aos Filhos", capa + intro + corpo + fim)


# ------------------------------------------------------------------ terço
def html_terco(ctx):
    f = lambda t: preencher(t, ctx)
    capa = (f'<div class="capa"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_rosario(130, "#E9CF93")}'
            f'<h1>Terço pelos<br>{"Netos" if ctx["FILHOS"].startswith("net") else "Filhos"}</h1>'
            f'<div class="nomes {_classe_nomes(ctx["NOMES"])}">{E(" · ".join(p["nome"] for p in ctx["vivos"]))}</div>'
            f'<div class="linha">os mistérios gozosos, oferecidos pelo nome de cada um</div><div class="rodape">ROTEIRO DO VÍDEO DO TERÇO</div></div>')
    intro = _p(f(C.TERCO_INTRO)) + "<h3>Como rezar</h3><ol class='passos'>" + "".join(f"<li>{E(x)}</li>" for x in C.TERCO_COMO) + "</ol>"
    base = "".join(f"<h3>{E(t)}</h3>{_p(x)}" for t, x in (("Creio", C.CREIO), ("Pai-Nosso", C.PAI_NOSSO), ("Ave-Maria", C.AVE_MARIA),
                                                       ("Glória", C.GLORIA), ("Ó meu Jesus", C.O_MEU_JESUS)))
    mist = ""
    for tit, ref, med, ofe in C.TERCO:
        mist += (f'<div class="dia"><h3 style="margin-top:0">{E(tit)}</h3><div class="leitura">Para ler: <b>{E(ref)}</b></div>{_p(f(med))}'
                 f'{_oracao(f(ofe))}<div class="pequeno">Um Pai-Nosso, dez Ave-Marias, um Glória e o Ó meu Jesus.</div></div>')
    fim = ("<h3>Salve-Rainha</h3>" + _p(C.SALVE_RAINHA) + "<h3>À vossa proteção</h3>" + _p(C.A_VOSSA_PROTECAO) + _p(C.TERCO_FINAL))
    return _doc("Terço pelos Filhos", capa + _secao("Antes de começar", "O terço de quem reza pelos filhos", intro)
                + _secao("As orações", "As orações do terço", f'<div class="sempre">{base}</div>')
                + _secao("Os cinco mistérios", "Mistérios gozosos", mist) + _secao("Para terminar", "Salve-Rainha", fim)
                + _secao("Antes de terminar", "Uma palavra final", f'<div class="final">{_p(C.PALAVRA_FINAL)}</div>'))


# ------------------------------------------------------------------ livro de cada filho (upsell)
def html_livro_filho(ctx, ia_filho, p):
    g = genero_pessoa(p["nome"], p["rel"])
    ex = dict(g, N=p["nome"])
    fase_ = p["fase"] or "adulto"
    st = p["santo"]
    capa = (f'<div class="capa"><div class="marca">✝ MEU SANTO PROTETOR ✝</div>{svg_manto(130)}'
            f'<div class="linha" style="font-family:Cinzel,serif;font-style:normal;letter-spacing:.25em;font-size:11pt;color:#E9CF93">UM LIVRO PARA</div>'
            f'<div class="nomes">{E(p["nome"])}</div>'
            f'<div class="linha">nasceu em {E(p["data"])}, {"num dia de festa da Igreja" if p["festa"] else "no dia de " + E(st["nome"])}</div>'
            f'<div class="rodape">COM O AMOR DE {E(ctx["QUEM"].upper())}, {E(ctx["SEU_PAPEL"].upper())}</div></div>')
    carta = _secao("Para você", p["nome"], _p(preencher(C.LIVRO_CARTA[fase_], ctx, ex)))
    invoc = f"Santa Maria, Mãe de Deus, rogai por {p['nome']}." if p["festa"] else f"{st['nome']}, rogai por {p['nome']}."
    santo = (f'<div class="santinho">{svg_manto(84, raios=True)}</div><div class="santo-nome">{E(st["nome"])}</div>'
             + (f'<div class="santo-quem">{E(st.get("quem") or "")}</div>' if st.get("quem") else "")
             + _p(f"Você nasceu em {p['data']}. " + ("Nesse dia, a Igreja celebra uma festa: " + st["nome"] + "." if p["festa"]
                                                       else "Nesse dia, a Igreja recorda " + st["nome"] + "."))
             + _p(ia_filho["santo_texto"]) + f'<p style="text-align:center;font-family:Cinzel,serif;color:#A57F35">{E(invoc)}</p>')
    pag_santo = _secao("O dia em que você nasceu", "O seu santo", santo)
    pag_or = _secao("Pelo seu nome", f"A oração que {ctx['SEU_PAPEL']} reza por você", _oracao(ia_filho["oracao"])
                    + _p(f"{ctx['QUEM']} reza esta oração por você. Você não precisa fazer nada: só saber que alguém entrega o seu nome a Deus todos os dias."))
    pag_sua = _secao("Quando quiser conversar com Deus", "Uma oração para você", _oracao(preencher(C.LIVRO_ORACAO[fase_], ctx, ex))
                     + "<h3>Santo Anjo</h3>" + _p(C.SANTO_ANJO) + "<h3>Ave-Maria</h3>" + _p(C.AVE_MARIA))
    recorte = (f'<div class="recorte">{svg_manto(60, raios=False)}<div class="st">{E(st["nome"])}</div>'
               f'<div class="r">{E(invoc)}</div><div class="pequeno" style="margin-top:2mm">{E(p["nome"])} · {E(p["data"])}</div></div>')
    pag_ben = _secao("Para guardar", "Uma bênção para você", _oracao(preencher(C.BENCAO, ctx, {"N": p["nome"]})) + _p(C.LIVRO_SANTINHO) + recorte
                     + f'<div class="final" style="margin-top:8mm"><p class="pequeno">Material devocional católico do Meu Santo Protetor (meusantoprotetor.online). '
                       'Não somos uma paróquia: nada substitui a missa, os sacramentos e a orientação de um padre.</p></div>')
    return _doc(f"Um livro para {p['nome']}", capa + carta + pag_santo + pag_or + pag_sua + pag_ben)


# ------------------------------------------------------------------ HTML → PDF
def _chrome_bin():
    cands = [os.environ.get("FILHOS_CHROME", ""), os.environ.get("CASAMENTO_CHROME", "")]
    cands += [shutil.which(x) or "" for x in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")]
    for pat in ("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome", "/root/.cache/ms-playwright/chromium-*/chrome-linux*/chrome",
                "/home/*/.cache/ms-playwright/chromium-*/chrome-linux*/chrome", "/opt/pw-browsers/chromium-*/chrome-linux*/chrome"):
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
    preferido = motor or os.environ.get("FILHOS_PDF_MOTOR", "")
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
