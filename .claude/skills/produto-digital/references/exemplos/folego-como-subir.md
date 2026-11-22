# Fôlego: como subir (sem túnel, sem cartão)

Funciona igual aos outros produtos: site no Cloudflare Pages + rotas no servidor do Meu Santo (`/opt/mapadaalma`).
NÃO instale o `folego-vps.zip` antigo (aquele com Next na porta 8020 e túnel): ele foi substituído por este kit.

Arquivos do kit:
- `atualizacao-servidor-19-folego.zip`: servidor.py + folego.py (+ clube.py e vsl_relatorio.py, iguais aos que já estão lá)
- `site-folegofinanceiro.zip`: o site pronto para o Cloudflare Pages
- `folego-codigo-v2.zip`: o código-fonte novo do site (para o sócio editar)
- `GUIA-CLAUDE-FOLEGO.md`: o guia para o Claude do sócio

## Parte 1: servidor (VPS)

1) No Mac (`carlosaugusto@macbook`), na pasta onde baixou o kit:
```
scp -o ServerAliveInterval=20 atualizacao-servidor-19-folego.zip root@2.25.252.204:/root/
```

2) Na VPS (`root@srv2014776`), faça o backup e descompacte:
```
cd /opt/mapadaalma && cp servidor.py /root/servidor-antes-19.py && unzip -o /root/atualizacao-servidor-19-folego.zip -d /opt/mapadaalma
```

3) Ainda na VPS, abra o .env:
```
nano /opt/mapadaalma/.env
```
- Na linha `KIWIFY_TOKEN=...`, acrescente no fim uma vírgula e o token do webhook do Fôlego, sem espaço. Fica assim: `KIWIFY_TOKEN=tokenquejaestava,outrotoken,<TOKEN_DO_WEBHOOK>`
- Acrescente no fim do arquivo:
```
FOLEGO_CHECKOUT=CODIGO_DO_CHECKOUT
```
(troque CODIGO_DO_CHECKOUT pelo código do checkout do Fôlego na Kiwify: o pedaço depois de `pay.kiwify.com.br/`)
- Salve: Ctrl+O, Enter, Ctrl+X.

4) Reinicie só o serviço do Meu Santo e confira:
```
systemctl restart mapadaalma && sleep 3 && curl -s localhost:8010/health && cd /opt/mapadaalma && ./venv/bin/python folego.py status
```
Tem que aparecer `{"ok":true...}` e duas linhas "últimas 24 h / 7 dias" (com zeros, por enquanto).

## Parte 2: site (Cloudflare Pages, igual ao Meu Santo)

5) Cloudflare → Workers e Pages → Criar → aba Pages → "Fazer upload de ativos" (Upload assets).
6) Nome do projeto: `folego` → Criar projeto → arraste o `site-folegofinanceiro.zip` → Implantar.
7) No projeto: Domínios personalizados → Configurar domínio → `folegofinanceiro.shop` → Ativar. Repita para `www.folegofinanceiro.shop`.
8) Espere uns minutos e abra https://folegofinanceiro.shop: o quiz tem que aparecer.

## Parte 3: Kiwify

9) O nome do produto precisa ter a palavra **Fôlego** (é por ela que o servidor separa as vendas do Fôlego das do Meu Santo).
10) Página de obrigado / redirecionamento depois da compra: `https://folegofinanceiro.shop/plano`
11) Webhook: pode deixar o que o sócio já criou (mesma URL do Meu Santo, token <TOKEN_DO_WEBHOOK>). Confira só: produto = só o Fôlego, todos os eventos marcados.

## Parte 4: teste

12) Faça o quiz em https://folegofinanceiro.shop até o resultado e clique em "Liberar meu plano": tem que abrir o checkout da Kiwify com nome e e-mail preenchidos.
13) Compre (ou peça para alguém comprar) e volte para a página do plano. A tela mostra "escrevendo seu plano" por 1 a 3 minutos e depois o plano completo.
14) Na VPS, confira:
```
cd /opt/mapadaalma && ./venv/bin/python folego.py status
```
Deve mostrar compras {'pago': 1} e "planos com IA 1". Se aparecer "versão padrão (IA falhou)", rode `./venv/bin/python folego.py buscar EMAIL_DA_COMPRA`: a linha do pedido mostra o erro da IA.

## Opcional
- **E-mail com o link do plano**: só funciona quando o domínio folegofinanceiro.shop estiver verificado na Resend. Depois disso, coloque no .env `FOLEGO_REMETENTE=Fôlego <plano@folegofinanceiro.shop>` e `FOLEGO_CONTATO=` (o e-mail de atendimento do Fôlego) e reinicie como no passo 4. Sem isso, o comprador só vê o plano pela página de obrigado (que já funciona).
- **Chave da Anthropic separada** (para o custo do Fôlego não se misturar com o do Meu Santo): crie uma chave no console da Anthropic, cole no .env como `FOLEGO_ANTHROPIC_API_KEY=` e reinicie. Sem ela, o Fôlego usa a mesma chave do Meu Santo. **Ela vence em 25/11**: a nova chave precisa ser "Never" (sem validade), senão os dois produtos param de gerar texto.
- **Modelo**: o padrão é `claude-opus-5-5` (o mesmo nível de qualidade que o sócio usava). Para gastar menos: `FOLEGO_MODELO=claude-sonnet-5-5`.
