---
name: produto-religioso
description: Cria e mantém produtos digitais religiosos (católicos e evangélicos) do Meu Santo Protetor e marcas irmãs, vendidos com anúncios no Meta, checkout na Kiwify e entregues por PDF personalizado com IA a partir do servidor FastAPI da VPS (/opt/mapadaalma). Use sempre que o pedido for criar um produto novo de fé ("faz um produto", "kit completo", novena, devocionário, oração, santo, consagração, terço), mexer em funil, quiz, página de vendas, order bump, upsell, webhook da Kiwify, PDF, e-mails, criativos ou anúncios desses produtos, ou instalar uma atualização do servidor na VPS, mesmo que o pedido não cite o nome da marca.
---

# Produtos religiosos (Meu Santo Protetor)

Esta skill guarda o contexto do negócio e o jeito de trabalhar com o Carlos e o sócio. Antes de responder, leia o que o pedido exige:

| Situação | Leia |
|---|---|
| Qualquer trabalho nesses produtos | `references/manual-meu-santo-protetor.md` (seções 2 e 10 valem para todas as respostas) |
| Produto novo | `references/playbook-produto-novo.md` e o exemplo completo em `references/exemplo-casamento/` |
| Mexer no servidor (rotas, webhook, VPS) | `references/guia-folego.md` (o padrão de módulo separado) e `references/exemplo-casamento/GUIA-CLAUDE-CASAMENTO.md` |
| Instalar algo na VPS ou no Cloudflare | `references/folego-como-subir.md` e `references/exemplo-casamento/COMO-SUBIR.md` |

## Regras que não se negociam

**Doutrina e copy**
- O santo não é adorado: ele intercede. Quem concede as graças é Deus.
- Nunca prometer graça, cura, dinheiro, casamento ou mudança.
- Nunca usar superstição nem inventar fato, data ou fala de santo.
- Versículo: só a referência, ou o texto da Bíblia Livre com a fonte.
- A voz nunca diz nem insinua ser padre. "Não somos paróquia, nada substitui a missa e os sacramentos" fica no produto e no site.
- Nada de vocabulário evangélico nos produtos católicos, nem o contrário.
- Temas sensíveis levam aviso de ajuda:
  - doença: buscar também o cuidado médico;
  - violência no casamento: Ligue 180 e Catecismo, n. 2383;
  - crise emocional: CVV 188.

**Anúncios**
- Sem atributo pessoal ("Você é católica?").
- Sem depoimento inventado, escassez ou prazo falso, "de/por" falso, "digite amém", cloaker ou domínio/pixel novo para fugir da classificação "Religião".
- Prazo só se for verdadeiro, e com data para sair do ar.

**Operação**
- Chaves e tokens **nunca** no chat nem em arquivo. Eles ficam só no `/opt/mapadaalma/.env`.
- Zips sempre sem `.env` (`-x '.env'`).
- VPS compartilhada: nunca reiniciar o Docker ou a máquina, nem rodar `do-release-upgrade`. Reinicie só com `systemctl restart mapadaalma`.
- **Não quebrar o Meu Santo:** produto novo = módulo próprio (`produto.py` com tabelas `produto_*`). No `servidor.py`, só ganchos mínimos (CORS, `include_router`, startup, desvio no webhook).
- Se o `servidor.py` da VPS puder ser diferente do que você tem, mande conferir o `md5sum` antes de substituir.
- LGPD: nada de e-mail, CPF ou telefone de cliente em documento ou relatório.
- A VPS não tem `sqlite3`: use `python3`.

## Jeito de trabalhar

- Português informal e direto, com a ação primeiro.
- Comandos prontos para copiar, **dizendo em qual terminal rodar**:
  - **Mac** (de onde sai o `scp -o ServerAliveInterval=20 ... root@2.25.252.204:/root/`);
  - **VPS** `root@srv2014776`.
- Discorde quando for o caso e aponte o que pode melhorar. Assuma ROAS ≥ 1 e não peça o gasto do anúncio.
- Mude uma coisa por vez nos testes. Em queda de vendas, confira checkout e rastreamento antes de mexer em criativo.
- Errou? Assuma o erro e corrija na hora.
- Seja honesto sobre o que não testou: diga o que precisa ser conferido no primeiro uso real.

## Produto novo: o kit completo

Quando pedirem um produto, entregue **tudo de uma vez** (detalhes e checklist em `references/playbook-produto-novo.md`):

1. **Raciocínio:** por que este produto, as alternativas descartadas, preço e escada.
2. **Nome exato para a Kiwify,** compatível com o reconhecimento do servidor. Confira se não colide com os trechos `PRODUTO_*` já usados, inclusive `2027`, `ritual`, `livro de oracoes` e `devocionario`.
3. Preço, descrição, order bumps (acima de R$ 10) e upsell.
4. Imagem 1000×1000 e banners 1200×400 e 1080×540 (cores `#F8F3EE` e `#17295A`).
5. **Páginas:** vendas (quiz com revelação grátis), obrigado com upsell, dados (só de reserva), privacidade.
6. **Servidor:** módulo próprio com geração por IA com *fallback* de texto fixo (nunca deixe compra sem entrega), PDF, e-mails, recuperação, lembretes, CLI (`diagnostico`, `status`, `funil`, `buscar`, `refazer`, `teste`) e teste ponta a ponta com o `TestClient`.
7. E-mails de entrega, dados, lembretes e recuperação.
8. Criativos: 5 a 10 estáticos 4:5 e vídeos 9:16, e uma legenda única.
9. `COMO-SUBIR.md` (Kiwify → servidor → site → teste → anúncios) e um guia para o Claude.
10. Zips em `entregas/` e commit.
11. **Confira antes de entregar:**
    - páginas no tamanho de celular;
    - quadros dos vídeos;
    - páginas do PDF;
    - webhook simulado com o `TestClient`.

## Modelo pronto

`templates/` tem a implementação completa do *O Santo do Nosso Casamento*. Copie e adapte em vez de começar do zero:
- `templates/servidor/`: módulo, conteúdo, PDF e teste ponta a ponta;
- `templates/site/`: quiz, obrigado com upsell, dados e privacidade;
- `templates/*.js`: os renderizadores de criativos (Playwright + ffmpeg).

As fontes do PDF (Cormorant Garamond, Cinzel, Great Vibes e Outfit, licença OFL) baixam do Google Fonts.
