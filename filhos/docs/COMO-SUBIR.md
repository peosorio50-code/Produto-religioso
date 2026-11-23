# Novena pelos Filhos: como subir

Funciona igual ao casamento: o site fica no Cloudflare Pages e as rotas ficam no servidor do Meu Santo (`/opt/mapadaalma`). Não precisa de porta nova, túnel novo nem domínio novo: o site entra num subdomínio do Meu Santo, `filhos.meusantoprotetor.online`.

**Tudo vem num zip só: `novena-pelos-filhos.zip`.** No **Mac**, dê dois cliques nele para abrir a pasta `novena-pelos-filhos`, com:
- `servidor/`: o que vai para `/opt/mapadaalma`: o `servidor.py` (v21 = v19 + ganchos do casamento + ganchos da novena), `filhos.py`, `filhos_conteudo.py`, `filhos_pdf.py`, `filhos_fontes/` e, de novo, os arquivos do casamento (para funcionar mesmo que o casamento ainda não tenha sido instalado);
- `site/`: o site para o Cloudflare Pages (falta só pôr os vídeos e preencher o `config.js`);
- `roteiros/`: os roteiros dos vídeos e as capas prontas;
- `kiwify/`, `criativos/` e `exemplos/`: imagens da Kiwify, criativos dos anúncios e PDFs de exemplo;
- `docs/`: este passo a passo, a estratégia, os textos da Kiwify e dos anúncios e o guia técnico.

**Terminais:**
- **Mac** = o seu computador (de onde o zip sai).
- **VPS** = `root@srv2014776`.
- Use sempre `-o ServerAliveInterval=20` no `scp` e no `ssh`.

**Ordem recomendada:** grave os 9 vídeos (roteiros na pasta `roteiros/`) enquanto faz as partes 1 a 3. Só ligue os anúncios (parte 5) depois do teste de ponta a ponta (parte 4) com os vídeos no ar.

---

## Parte 1: Kiwify (faça primeiro, para ter o código do checkout)

Os textos para copiar estão em `docs/TEXTOS-KIWIFY-E-ANUNCIOS.md`.

1. **Crie o produto `Novena pelos Filhos (em vídeo)`** (R$ 87, garantia de 7 dias):
   - cores do checkout `#F8F3EE` e `#17295A`, imagem e banners da pasta `kiwify/`;
   - pixel do Meta: o mesmo dos outros produtos.
2. **Crie os 2 bumps como produtos** e adicione como order bump no checkout do principal:
   - `30 Bênçãos para Mandar aos Filhos`: R$ 14,90;
   - `Terço pelos Filhos (em vídeo)`: R$ 19,90. **Crie, mas só ligue como bump quando o vídeo do terço estiver no ar.**
3. **Crie o produto do upsell `Um Livro para Cada Filho`** (R$ 37) e use o "Gerador de upsell" dele. Anote:
   - o ID (o trecho depois de `kiwify-upsell-trigger-`);
   - o link do checkout desse produto.
4. **Página de obrigado** do produto principal: `https://filhos.meusantoprotetor.online/obrigado.html`
5. **Webhook:** mesma URL do Meu Santo (`https://api.mapadaalma.online/webhook/kiwify/<segredo>`), com todos os eventos marcados. Duas opções:
   - **Mais simples:** edite o webhook que já existe e marque também os 4 produtos novos. O token continua o mesmo, e o `.env` não muda.
   - **Webhook novo:** só com os 4 produtos. Anote o token: ele vai no `KIWIFY_TOKEN` (passo 8).
6. **Anote o código do checkout** do produto principal: é o trecho depois de `pay.kiwify.com.br/`.

## Parte 2: servidor (VPS)

7. **Mac**: abra o Terminal **dentro da pasta `novena-pelos-filhos`** (no Finder, clique com o botão direito na pasta → Serviços → Novo Terminal na Pasta) e mande a pasta do servidor:
   ```
   scp -o ServerAliveInterval=20 -r servidor root@2.25.252.204:/root/novena-servidor-21
   ```
   Se precisar mandar de novo, apague antes a cópia antiga na **VPS** (senão o `scp` cria uma pasta dentro da outra):
   ```
   rm -rf /root/novena-servidor-21
   ```

8. **VPS.** Primeiro confira qual `servidor.py` está lá:
   ```
   cd /opt/mapadaalma && md5sum servidor.py
   ```
   Tem que aparecer **um destes dois**:
   - **`0cfbd62f7cc1b87e308623185cba50d8`**: o v20, com o casamento já instalado;
   - **`180e1cd74492a19cede3259abe56496f`**: o v19, sem o casamento (o pacote instala o casamento junto, parado até você pôr o `CASAMENTO_CHECKOUT`).

   Se aparecer **outro número, pare aqui**: o `servidor.py` foi mudado depois. Peça ao Claude para aplicar só os 4 ganchos da novena (estão no `docs/GUIA-CLAUDE-FILHOS.md`, seção 5) no arquivo que está na VPS, sem trocar o arquivo inteiro.

   Se o número bateu, faça o backup e descompacte:
   ```
   cd /opt/mapadaalma && cp servidor.py /root/servidor-antes-21.py && cp -r /root/novena-servidor-21/. /opt/mapadaalma/ && (chown -R mapa:mapa servidor.py filhos.py filhos_conteudo.py filhos_pdf.py filhos_fontes casamento.py casamento_conteudo.py casamento_pdf.py casamento_fontes 2>/dev/null; true)
   ```

9. **VPS:** abra o `.env`:
   ```
   nano /opt/mapadaalma/.env
   ```
   - Acrescente no fim (troque pelo código do passo 6):
     ```
     FILHOS_CHECKOUT=CODIGO_DO_CHECKOUT
     ```
   - Só se você criou um webhook novo no passo 5: na linha `KIWIFY_TOKEN=...`, acrescente no fim uma vírgula e o token novo, sem espaço.
   - Salve: Ctrl+O, Enter, Ctrl+X.

10. **VPS:** reinicie só o serviço do Meu Santo e confira:
    ```
    systemctl restart mapadaalma && sleep 4 && curl -s localhost:8010/health && cd /opt/mapadaalma && ./venv/bin/python filhos.py diagnostico
    ```
    Tem que aparecer `{"ok":true...}` e uma lista de `OK`. **Os pontos que importam:**
    - `tabela de santos: 13/06 → ...`;
    - pelo menos um `OK gerador de PDF` (Playwright, WeasyPrint ou Chromium);
    - `FILHOS_CHECKOUT` preenchido;
    - as 4 linhas `FILHOS_PRODUTO`, `FILHOS_BUMP_BENCAOS`, `FILHOS_BUMP_TERCO` e `FILHOS_UPSELL` com `OK` (se alguma disser `CHOCA`, o nome colide com outro produto: me avise antes de vender).

    Se o `diagnostico` disser que o módulo não existe, veja o log na **VPS**:
    ```
    grep "filhos" /opt/mapadaalma/dados/logs/servidor.log | tail -20
    ```
    O servidor sobe mesmo se o módulo da novena falhar (os outros produtos continuam vendendo), mas aí a novena não é entregue.

11. **VPS:** mande uma novena de teste para você (texto padrão, sem IA, sem custo; gera a novena, o terço, as bênçãos e o livro de cada filho de um exemplo com 3 filhos):
    ```
    cd /opt/mapadaalma && ./venv/bin/python filhos.py teste SEU_EMAIL
    ```
    Confira o e-mail e o PDF anexo. Os botões e o link da novena desse teste não funcionam; o anexo funciona. Para ver o texto escrito pela IA (custa ~US$ 0,10), troque o comando para:
    ```
    cd /opt/mapadaalma && ./venv/bin/python filhos.py teste SEU_EMAIL ia
    ```

**Para desfazer** (os arquivos novos ficam parados sem os ganchos). Na **VPS**:
```
cp /root/servidor-antes-21.py /opt/mapadaalma/servidor.py && systemctl restart mapadaalma
```

## Parte 3: site (Cloudflare Pages)

12. **Mac:** abra a pasta `site/` (dentro de `novena-pelos-filhos`).
    - Ponha os vídeos que você montou na pasta `videos/` (`dia1.mp4` … `dia9.mp4` e `vsl.mp4`). Cada arquivo precisa ter **menos de 25 MB**.
    - Abra o `config.js` num editor de texto e preencha:
      - `CHECKOUT`: `https://pay.kiwify.com.br/CODIGO` (é só a reserva para quando o servidor não responder);
      - `VSL_SRC`: `"videos/vsl.mp4"`;
      - `VIDEOS`: `dia1: "videos/dia1.mp4"` … `dia9: "videos/dia9.mp4"`, e `terco: "youtube:ID"` quando o terço estiver no YouTube;
      - `UPSELL_ID` e `CHECKOUT_UPSELL` (passo 3). Se deixar vazio, a página de obrigado pula a oferta e mostra a novena.

    Depois gere o zip do site. No **Mac**, num Terminal aberto dentro da pasta `site/`:
    ```
    zip -qr ../site-santo-filhos.zip . -x '.DS_Store'
    ```
    O arquivo `site-santo-filhos.zip` aparece ao lado da pasta `site/`, dentro de `novena-pelos-filhos`.
13. **Cloudflare:**
    - Workers e Pages → Criar → aba Pages → "Fazer upload de ativos".
    - Nome do projeto: `santo-filhos` → Criar projeto → arraste o zip → Implantar.
14. **No projeto:** Domínios personalizados → Configurar domínio → `filhos.meusantoprotetor.online` → Ativar. O DNS já está no Cloudflare, então ele cria o registro sozinho.
15. Espere uns minutos e abra `https://filhos.meusantoprotetor.online`: tem que aparecer "Todo filho nasce no dia de um santo".

> O deploy do Pages substitui o site inteiro daquele projeto. Como a novena tem um projeto só dela, subir este zip **não mexe** no site do Meu Santo nem no do casamento. Para trocar um vídeo depois, gere o zip de novo com tudo e faça um novo deploy no mesmo projeto.

## Parte 4: teste de ponta a ponta (antes de ligar anúncio)

16. **No celular**, abra o site e faça o quiz com 2 ou 3 nomes até a revelação.
    - Confira se os santos batem com o calendário.
    - A VSL começa muda, com legenda; o botão "Toque para ouvir" liga o som do começo.
    - Toque em "Quero rezar a novena": tem que abrir o checkout da Kiwify.
17. **Compre no Pix** (marque o bump das bênçãos) e pague. A página de obrigado tem que mostrar o upsell; toque em "Não, obrigado". Em 1 a 3 minutos aparece "A sua novena está pronta". Toque em "Abrir a minha novena":
    - o vídeo do 1º dia toca;
    - a oração do dia aparece embaixo, já com os nomes;
    - a seção das bênçãos tem os botões de copiar e de WhatsApp;
    - o e-mail chega com o PDF anexo e o botão da novena.
18. **VPS:** confira a compra:
    ```
    cd /opt/mapadaalma && ./venv/bin/python filhos.py buscar EMAIL_DA_COMPRA
    ```
    Tem que aparecer `fase=enviado`, os `skus` com o bump que você marcou e o link da página da novena.
19. **Teste o upsell** uma vez (com cartão, para testar o 1 clique) e confira que chega "Um Livro para Cada Filho" com um PDF para cada nome. Depois peça o reembolso de tudo na Kiwify.
20. **Também teste pelo celular até gerar o Pix sem pagar.** Em 60 minutos tem que chegar o e-mail "O seu Pix ficou pendente".
21. **No dia seguinte de manhã**, confira se chegou o e-mail "2º dia da novena".

## Parte 5: anúncios

Os criativos (pasta `criativos/`) e a legenda estão em `docs/TEXTOS-KIWIFY-E-ANUNCIOS.md`.

- **Campanha de vendas própria** (não misture com a Família), com 2 conjuntos de US$ 15 a 20 por dia:
  - **A:** curiosidade e participação;
  - **B:** produto e preço.
- **Público:** o mesmo que já funciona nos produtos do Meu Santo. Na copy, nenhum atributo pessoal ("Você é mãe?", "Seu filho está longe de Deus?").
- **Link** com UTM (está no documento dos textos).
- Desligue o criativo que gastou US$ 10 a 15 sem compra. Compare os conjuntos depois de uns US$ 40.

## Parte 6: acompanhamento (VPS)

```
cd /opt/mapadaalma && ./venv/bin/python filhos.py status
```
Mostra quizzes, vendas, bumps, upsell, textos com IA ou padrão, lembretes diários e recuperação, nas últimas 24 h e 7 dias.

```
cd /opt/mapadaalma && ./venv/bin/python filhos.py funil 7
```
Mostra o funil da página: entrou → começou o quiz → viu os santos → VSL (10 s, som, metade, fim) → chegou ao preço → clicou em comprar → upsell → abriu a novena → rezou o 1º e o 9º dia.

**Onde olhar se as vendas não vierem:**
- **Muita gente para entre "viu os santos" e "clicou em comprar":** o problema é a oferta (preço, VSL, página).
- **Muitos cliques e poucas compras:** o problema é o checkout. Faça o teste no celular do passo 20.
- **Pouca gente marca o 1º dia rezado:** confira se os vídeos estão tocando no celular. Quem não usa o produto pede reembolso.
