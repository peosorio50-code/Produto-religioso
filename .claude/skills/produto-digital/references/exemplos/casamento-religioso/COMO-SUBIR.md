# O Santo do Nosso Casamento: como subir

Funciona igual ao Fôlego: o site fica no Cloudflare Pages, e as rotas ficam no servidor do Meu Santo (`/opt/mapadaalma`). Não precisa de porta nova, túnel novo nem domínio novo: o site entra num subdomínio do Meu Santo, `casamento.meusantoprotetor.online`.

**Arquivos (pasta `entregas/`):**
- `atualizacao-servidor-20-casamento.zip`: o `servidor.py` (v19 com 4 ganchos do casamento), `casamento.py`, `casamento_conteudo.py`, `casamento_pdf.py` e `casamento_fontes/`.
- `site-santo-casamento.zip`: o site pronto para o Cloudflare Pages.
- `kit-casamento.zip`: imagens da Kiwify, criativos, PDFs de exemplo e estes documentos.

**Terminais:**
- **Mac** = o seu computador (de onde o zip sai).
- **VPS** = `root@srv2014776`.
- Use sempre `-o ServerAliveInterval=20` no `scp` e no `ssh`.

---

## Parte 1: Kiwify (faça primeiro, para ter o código do checkout)

Os textos para copiar estão em `TEXTOS-KIWIFY-E-ANUNCIOS.md`.

1. **Crie o produto `O Santo do Nosso Casamento`** (R$ 37, garantia de 7 dias):
   - cores do checkout `#F8F3EE` e `#17295A`, imagem e banners da pasta `kiwify/`;
   - pixel do Meta: o mesmo dos outros produtos.
2. **Crie os 2 bumps como produtos** e adicione os dois como order bump no checkout do principal:
   - `30 Dias Rezando pelo Meu Marido`: R$ 14,90;
   - `Novena de Santa Rita pelo Casamento`: R$ 12,90.
3. **Página de obrigado** do produto principal: `https://casamento.meusantoprotetor.online/obrigado.html`
4. **Webhook:** mesma URL do Meu Santo (`https://api.mapadaalma.online/webhook/kiwify/<segredo>`), com todos os eventos marcados. Duas opções:
   - **Mais simples:** edite o webhook que já existe e marque também os 3 produtos novos. O token continua o mesmo, e o `.env` não muda.
   - **Webhook novo:** só com os 3 produtos. Anote o token dele: ele vai no `KIWIFY_TOKEN` (passo 8).
5. **Anote o código do checkout:** é o trecho depois de `pay.kiwify.com.br/`.
6. *(Opcional, pode ser depois)* **Upsell:** no produto *Os Santos Protetores da Sua Família + Devocionário de Bônus*, crie uma oferta de R$ 27 e use o "Gerador de upsell". Anote:
   - o ID (o trecho depois de `kiwify-upsell-trigger-`);
   - o link do checkout dessa oferta.

## Parte 2: servidor (VPS)

7. **Mac**, na pasta onde está o zip:
   ```
   scp -o ServerAliveInterval=20 atualizacao-servidor-20-casamento.zip root@2.25.252.204:/root/
   ```

8. **VPS.** Primeiro confira se o `servidor.py` que está lá é o v19, o mesmo em que este pacote foi montado:
   ```
   cd /opt/mapadaalma && md5sum servidor.py
   ```
   - Tem que aparecer **`180e1cd74492a19cede3259abe56496f`**.
   - Se aparecer outro número, **pare aqui**: o `servidor.py` foi mudado depois do v19. Peça ao Claude para aplicar só os 4 ganchos do casamento (estão no `GUIA-CLAUDE-CASAMENTO.md`, seção 5) no arquivo que está na VPS, sem trocar o arquivo inteiro.

   Se o número bateu, faça o backup e descompacte:
   ```
   cd /opt/mapadaalma && cp servidor.py /root/servidor-antes-20.py && unzip -o /root/atualizacao-servidor-20-casamento.zip -d /opt/mapadaalma && (chown -R mapa:mapa servidor.py casamento.py casamento_conteudo.py casamento_pdf.py casamento_fontes 2>/dev/null; true)
   ```

9. **VPS:** abra o `.env`:
   ```
   nano /opt/mapadaalma/.env
   ```
   - Acrescente no fim (troque pelo código do passo 5):
     ```
     CASAMENTO_CHECKOUT=CODIGO_DO_CHECKOUT
     ```
   - Só se você criou um webhook novo no passo 4: na linha `KIWIFY_TOKEN=...`, acrescente no fim uma vírgula e o token novo, sem espaço.
   - Salve: Ctrl+O, Enter, Ctrl+X.

10. **VPS:** reinicie só o serviço do Meu Santo e confira:
    ```
    systemctl restart mapadaalma && sleep 4 && curl -s localhost:8010/health && cd /opt/mapadaalma && ./venv/bin/python casamento.py diagnostico
    ```
    Tem que aparecer `{"ok":true...}` e uma lista de `OK`. **Os três pontos que importam:**
    - `tabela de santos: 13/06 → ...`;
    - pelo menos um `OK gerador de PDF` (Playwright, WeasyPrint ou Chromium);
    - `CASAMENTO_CHECKOUT` preenchido.

    **Se nenhum gerador de PDF der OK** (improvável, porque o devocionário já gera PDF), instale o WeasyPrint. Na **VPS**:
    ```
    cd /opt/mapadaalma && ./venv/bin/pip install weasyprint && ./venv/bin/python casamento.py diagnostico
    ```
    Se ainda reclamar de "pango", rode na **VPS** e depois repita o diagnóstico:
    ```
    apt-get install -y libpango-1.0-0 libpangoft2-1.0-0
    ```
    Esse comando só instala as bibliotecas de texto: não reinicia nada e não mexe no Docker.

11. **VPS:** mande um livro de teste para você (texto padrão, sem IA, sem custo):
    ```
    cd /opt/mapadaalma && ./venv/bin/python casamento.py teste SEU_EMAIL
    ```
    Confira o e-mail e o PDF anexo. Os botões de baixar desse teste não funcionam; o anexo funciona. Para ver o texto escrito pela IA (custa ~US$ 0,05), troque o comando para:
    ```
    cd /opt/mapadaalma && ./venv/bin/python casamento.py teste SEU_EMAIL ia
    ```

**Para desfazer** (os arquivos do casamento ficam parados sem os ganchos). Na **VPS**:
```
cp /root/servidor-antes-20.py /opt/mapadaalma/servidor.py && systemctl restart mapadaalma
```

## Parte 3: site (Cloudflare Pages)

12. **Mac:** descompacte o `site-santo-casamento.zip` numa pasta e abra o `config.js` num editor de texto.
    - `CHECKOUT`: o link do checkout, `https://pay.kiwify.com.br/CODIGO`. É só a reserva para quando o servidor não responder.
    - Se já fez o upsell (passo 6): `UPSELL_ID` e `CHECKOUT_UPSELL`. Se não fez, deixe vazio e a página de obrigado mostra direto o livro.

    Depois gere o zip de novo. No **Mac**, dentro da pasta do site:
    ```
    zip -qr ../site-santo-casamento.zip . -x '.DS_Store'
    ```
13. **Cloudflare:**
    - Workers e Pages → Criar → aba Pages → "Fazer upload de ativos".
    - Nome do projeto: `santo-casamento` → Criar projeto → arraste o zip → Implantar.
14. **No projeto:** Domínios personalizados → Configurar domínio → `casamento.meusantoprotetor.online` → Ativar. O DNS já está no Cloudflare, então ele cria o registro sozinho.
15. Espere uns minutos e abra `https://casamento.meusantoprotetor.online`: tem que aparecer "Todo casamento acontece no dia de um santo".

> O deploy do Pages substitui o site inteiro daquele projeto. Como o casamento tem um projeto só dele, subir este zip **não mexe** no site do Meu Santo.

## Parte 4: teste de ponta a ponta (antes de ligar anúncio)

16. **No celular**, abra o site e faça o quiz até a revelação.
    - Confira se o santo bate com o calendário.
    - Toque em "Quero o livro": tem que abrir o checkout da Kiwify.
17. **Compre no Pix** (marque um bump para testar) e pague. A página de obrigado tem que mostrar "Estamos preparando o seu livro" e, em 1 a 3 minutos, os botões para baixar. O e-mail chega com o PDF anexo.
18. **VPS:** confira a compra:
    ```
    cd /opt/mapadaalma && ./venv/bin/python casamento.py buscar EMAIL_DA_COMPRA
    ```
    Tem que aparecer:
    - `fase=enviado`;
    - os `skus` com o bump que você marcou;
    - `IA` (se aparecer só o texto padrão, o motivo está no log, veja a seção 6 do `GUIA-CLAUDE-CASAMENTO.md`).
19. Peça o reembolso na Kiwify.
20. **Também teste pelo celular até gerar o Pix sem pagar.** É a suspeita principal da queda do devocionário no manual. Em 60 minutos tem que chegar o e-mail "O seu Pix ficou pendente".

## Parte 5: anúncios

Os criativos e a legenda estão em `TEXTOS-KIWIFY-E-ANUNCIOS.md`.

- **Campanha de vendas** com 2 conjuntos de US$ 15 a 20 por dia:
  - **A:** curiosidade e participação;
  - **B:** produto e presente.
- **Público:** o mesmo que já funciona nos produtos do Meu Santo. Na copy, nenhum atributo pessoal ("Você é católica?", "Você é casada?").
- **Link** com UTM (está no documento dos textos).
- Desligue o criativo que gastou US$ 10 a 15 sem compra. Compare os conjuntos depois de uns US$ 40.

## Parte 6: acompanhamento (VPS)

```
cd /opt/mapadaalma && ./venv/bin/python casamento.py status
```
Mostra quizzes, vendas, bumps, entregas com IA ou com texto padrão e recuperação, nas últimas 24 h e 7 dias.

```
cd /opt/mapadaalma && ./venv/bin/python casamento.py funil 7
```
Mostra o funil da página: entrou → começou o quiz → viu o santo → chegou à oferta → clicou em comprar → pagou.

**Onde olhar se as vendas não vierem:**
- **Muita gente para entre "viu o santo" e "clicou em comprar":** o problema é a oferta (preço, página).
- **Muitos cliques e poucas compras:** o problema é o checkout. Faça o teste no celular do passo 20.
