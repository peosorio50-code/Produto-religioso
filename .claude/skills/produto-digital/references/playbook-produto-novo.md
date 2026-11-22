# Playbook: produto novo (qualquer nicho)

As regras do nicho ficam em `nichos/<nicho>.md`. O exemplo completo em PDF é `exemplos/casamento-religioso/`; o exemplo de produto entregue como página é `exemplos/guia-folego-financas.md`.

O que aprendemos montando o *O Santo do Nosso Casamento* (veja `exemplos/casamento-religioso/`), para repetir em qualquer produto.

## 1. Escolher o produto

**Comece pelo que já foi validado.** O mecanismo dado → resultado grátis → material personalizado vale para qualquer nicho: no religioso, a data dá o santo; no financeiro, o quiz das dívidas dá o diagnóstico; no autoconhecimento, a data de nascimento dá o mapa. O gancho do Meu Santo é "Todo mundo nasce no dia de um santo. Descubra o seu." O mecanismo vencedor é:
1. a pessoa digita uma data;
2. vê de graça o santo (ou a promessa, ou a oração) daquela data;
3. recebe a oferta de um material feito com o nome dela.

**Datas que podem virar produto novo com o mesmo gancho:** casamento (feito), batizado, o dia em que um ente querido partiu ("dies natalis": candidato a próximo, pede cuidado redobrado com o luto), ordenação, primeira comunhão.

**Critérios para dar nota a cada ideia:**
- o público é um que já compra das nossas marcas (ou está claramente definido);
- a emoção é positiva;
- serve de presente;
- tem preço de R$ 37 a R$ 97;
- tem uma escada para os produtos que já existem na marca;
- o risco é baixo (regras do nicho, Meta, atendimento).

**Produto sazonal só com prazo verdadeiro.** Avise quantas semanas de venda restam.

**Escreva o raciocínio no `docs/ESTRATEGIA.md`:**
- a ideia e por que ela;
- as alternativas descartadas;
- o conteúdo;
- o funil;
- o líquido por venda (taxa da Kiwify de ~8,99% + R$ 2,49);
- o CPA de empate;
- o que conferir no primeiro teste.

## 2. Funil que evita os problemas do manual

```
Anúncio → quiz (dados ANTES da compra) → revelação grátis → oferta (capa com o nome, itens, páginas de exemplo, preço, garantia, FAQ)
 → Kiwify com ?sck=<ref do quiz>&utm_* → bumps → obrigado.html (upsell de 1 clique → livro pronto para baixar na página + e-mail)
```

- **Dados antes da compra.** Sem formulário depois do pagamento: é isso que gerou as 187 compras paradas em `aguardando_dados`. A página de dados existe só como reserva, para quem compra pelo link direto, com lembretes de ~20 h e ~68 h.
- **Se o servidor cair no clique de comprar,** mande direto para o checkout de reserva (`CFG.CHECKOUT`): não perca a venda.
- **Página de obrigado:** primeiro o upsell (com o `UPSELL_ID`, e o `CHECKOUT_UPSELL` de reserva para quem pagou no Pix), depois o andamento do livro (pergunta a cada 4 s) com os botões de baixar.
- **Contador próprio de eventos** via `/api/evento` (p = nome do produto), porque o Meta descarta eventos personalizados na categoria Religião. No pixel, só eventos padrão: PageView, ViewContent e InitiateCheckout.

## 3. Servidor (padrão de módulo separado)

- Arquivos `produto.py`, `produto_conteudo.py` (textos fixos) e `produto_pdf.py` (HTML → PDF), mais as fontes.
- O módulo importa `servidor as S` depois de criar o `router`, e reaproveita:
  - `S.db`, `S._lock`;
  - `S.enviar_email`, `S._moldura`, `S._botao`;
  - `S._marca("santo")` (remetente e cores);
  - `S.alerta_admin`, `S.PDFS`, `S._sem_acento`;
  - `S.cliente`, `S.liberar_fila`.
- As configurações vêm do `os.environ` (o `servidor.py` carrega o `.env`), então não é preciso mexer no `CFG`.
- **4 ganchos no `servidor.py`:**
  1. CORS do site novo;
  2. `include_router`;
  3. `iniciar()` no startup;
  4. desvio no webhook logo depois de `_produtos_no_payload`. Ele processa só os nomes do produto novo e devolve o resto para o fluxo normal. Em caso de erro, `raise HTTPException(500)` para a Kiwify tentar de novo, e o processamento precisa ser seguro contra repetição (upsert por `order_id`).
- **Bumps:** trate os dois casos, no mesmo aviso ou em avisos separados. Use uma linha por `order_id`, gere só os `skus` daquela linha, e ligue o bump sem `sck` ao quiz da compra recente do mesmo e-mail.
- **IA:**
  - a IA escreve poucos campos curtos, com saída em `json_schema`;
  - cada campo é conferido (tamanho, nomes, "Amém.", filtro de promessa de resultado);
  - *fallback* de texto fixo campo a campo: **se a IA falhar, o produto sai mesmo assim**;
  - modelo configurável por `.env` (padrão `claude-opus-5-5`, com fallback de recusa do lado da API).
- **PDF:** tenta o Playwright, depois o WeasyPrint, depois o Chromium pela linha de comando.
  - Embuta as fontes em base64.
  - Use `@page`, páginas nomeadas para a capa de página inteira, e `top/right/bottom/left` em vez de `inset` (por causa do WeasyPrint).
  - Fundo branco no miolo, porque imprime melhor.
- **CLI:** `diagnostico`, `status`, `funil`, `buscar`, `refazer`, `teste EMAIL [ia]`, `santo DIA MES`.
- **Recuperação própria:** Pix pendente em 60 min, cartão recusado em 15 min, carrinho abandonado em 90 min. Limpeza dos quizzes sem compra depois de 60 dias (está prometida na política de privacidade).
- **Teste ponta a ponta** com o `servidor.py` real e um `santos.py` de mentira: pedido, Pix, pago com bumps, aviso repetido, sem quiz, bump separado, venda do Meu Santo intacta, pedido misto, reembolso, carrinho abandonado, conferência dos textos da IA. Rode com os dois motores de PDF.

## 4. Conteúdo

- **Texto fixo** escrito por você e revisado contra a seção 2 do manual. Versículo só com a referência.
- **Fatos sobre santos: só o que é certo.** Se houver dúvida, fale da virtude, não da biografia.
- **Dias que são festa do Senhor** (Natal, Batismo...) e não um santo: troque a invocação por "Santa Maria, Mãe de Deus, rogai por nós" e o texto por "dia de festa da Igreja: ...".
- **Página final:** "Não somos paróquia…", e os avisos de ajuda quando o tema pedir.

## 5. Criativos

- Desenhe em HTML com as fontes da marca e fotografe com o Playwright. Vídeo: um quadro por vez, a 24 fps, montado com o ffmpeg, sem áudio.
- **Formatos campeões que dá para adaptar:**
  - "Qual destes é o seu…" (A/B/C);
  - "Pergunte à sua mãe / em casa";
  - lista de datas com o santo de cada uma;
  - vela;
  - conversa de chat (como cena, nunca como depoimento);
  - produto e preço;
  - presente;
  - páginas por dentro.
- **Dois conjuntos:** curiosidade × produto. Mostre "exemplo" e "imagem ilustrativa" quando couber.

## 6. Checklist de entrega

- [ ] `docs/`: ESTRATEGIA, COMO-SUBIR (com o terminal de cada comando e o `md5sum` antes de substituir o `servidor.py`), TEXTOS-KIWIFY-E-ANUNCIOS e GUIA-CLAUDE
- [ ] `entregas/`: `atualizacao-servidor-N-produto.zip` (sem `.env`), `site-produto.zip` (projeto Pages próprio, num subdomínio do domínio da marca) e `kit-produto.zip`
- [ ] Teste do servidor passando, site conferido no celular, PDF e vídeos conferidos quadro a quadro
- [ ] Lista honesta do que só dá para confirmar em produção (formato dos bumps na Kiwify, script do upsell, tabela real de santos, motor de PDF da VPS, `suporte_ia`)
- [ ] Commit e push no branch combinado; mande os arquivos para o usuário agrupados e com legenda
