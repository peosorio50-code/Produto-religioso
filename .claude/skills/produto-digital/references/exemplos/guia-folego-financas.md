# Guia do Fôlego para o Claude (leia antes de mexer)

Você vai trabalhar no **Fôlego** (folegofinanceiro.shop): quiz sobre dívidas → resultado grátis → plano de quitação personalizado por R$ 29,90 (Kiwify), com texto escrito pelo Claude.

## 1. Arquitetura (mudou: não existe mais app Node na VPS nem túnel)

| Parte | Onde fica | O que faz |
|---|---|---|
| Site | Código Next.js (`folego-codigo-v2.zip`), exportado como **estático** (`output: "export"` → pasta `out/`) e publicado no **Cloudflare Pages**, projeto `folego`, domínio folegofinanceiro.shop | Quiz, resultado, checkout e o plano montado na tela. Todo o cálculo é feito no navegador. |
| Servidor | **`folego.py`** dentro do servidor Python (FastAPI) do Meu Santo Protetor: VPS, `/opt/mapadaalma`, serviço `mapadaalma`, porta 8010, público em `https://api.mapadaalma.online` (túnel que já existia) | Guarda pedidos/compras/leads (SQLite `dados/mapa.db`, tabelas `folego_*`), chama a IA, recebe a Kiwify e manda e-mail. |
| Kiwify | Mesmo webhook do Meu Santo: `https://api.mapadaalma.online/webhook/kiwify/<segredo>` | O `servidor.py` vê "folego" no nome do produto (`PRODUTO_FOLEGO`) e chama `folego.evento_kiwify()` **antes** de qualquer lógica do Meu Santo. |

Não é preciso servidor Node, Docker, porta nova nem túnel novo. Não crie isso de novo.

## 2. Fluxo

1. Quiz (`components/Quiz.tsx`). No início e no fim, `postar("/lead", {evento, contato, origem, resumo})` → tabela `folego_leads` + `folego_eventos`.
2. Resultado (`components/Resultado.tsx`): os números saem de `lib/diagnostico.ts`. Em "Liberar meu plano", o site chama `postar("/checkout", {respostas, contato, origem, resumo, dadosIA})`.
   - O servidor cria o `ref` (`fl-<12hex>-<16hex>`), guarda tudo e devolve `{ref, url}`.
   - `url` = `https://pay.kiwify.com.br/<FOLEGO_CHECKOUT>?sck=<ref>&name=&email=&utm_*`.
   - Se o e-mail já tem uma compra paga sem pedido (comprou antes de fazer o quiz), `url` já é o link do plano.
3. Kiwify → webhook → `evento_kiwify`. Liga a compra ao pedido nesta ordem:
   - pelo `TrackingParameters.sck`;
   - senão, pelo pedido mais recente do mesmo e-mail (7 dias) ainda não pago.

   Status e pesos: pendente/recusado 1, pago 2, reembolsado 3 (não regride). Na primeira aprovação, manda o e-mail com o link (só se `FOLEGO_REMETENTE` estiver no .env).
4. `/plano` (`components/TelaPlano.tsx`): `postar("/plano", {ref, regenerar})`:
   - 402 `{urlPagamento}` = ainda não pago;
   - 404 = pedido não existe;
   - 202 = a IA está escrevendo (a tela pergunta de novo a cada 5 s, até 60 vezes);
   - 200 `{respostas, ia, geradoEm, podeRegenerar}` = pronto. O navegador monta o plano: `diagnosticar` + `narrativaPadrao` + `conciliar(ia)`.
   - Se a IA falhar, `ia` vem `null` e sai a versão por regras. A pessoa pode pedir de novo (máx. 3 gerações no total).
5. `/reenviar {email}` (manda o link de novo; responde sempre igual para não revelar quem é cliente) e `/vincular {ref,email}` ("paguei com outro e-mail").

## 3. Onde mexer

| Quero mudar… | Arquivo |
|---|---|
| Perguntas do quiz | `lib/perguntas.ts`, `components/Quiz.tsx`, validação em `lib/validacao.ts` |
| Contas, juros, ordem da fila | `lib/diagnostico.ts` (tem teste: `npm test`) |
| Texto padrão do plano (sem IA) | `lib/narrativa-padrao.ts`, `lib/guia.ts` |
| O que vai para a IA / como o texto da IA entra no plano | `lib/ia-dados.ts` (`dadosParaIA`, `conciliar`, `normalizar`) |
| Prompt da IA e formato do JSON | `folego.py` no servidor: `SISTEMA` e `ESQUEMA` (devem bater com a interface `NarrativaIA` de `lib/ia-dados.ts`) |
| E-mail do plano | `folego.py`: `email_plano()` |
| Endereço da API | `lib/api.ts` (`NEXT_PUBLIC_API`, padrão `https://api.mapadaalma.online`) |
| Página de vendas / textos | `app/page.tsx`, `components/*` |

Se mudar o formato do JSON da IA, mude **os três juntos**: `ESQUEMA` em folego.py, `NarrativaIA` + `normalizar` em ia-dados.ts.

## 4. Build e deploy do site

```bash
npm ci
npm test                      # diagnostico.test.ts
npm run build                 # gera out/
cd out && zip -r ../site-folegofinanceiro.zip . && cd ..
```
Depois: Cloudflare → Workers e Pages → projeto `folego` → Criar implantação → upload do zip.

Variáveis de build (opcionais):
- `NEXT_PUBLIC_API`: endereço da API.
- `NEXT_PUBLIC_CONTATO_EMAIL`: e-mail de atendimento mostrado no site.
- `NEXT_PUBLIC_REENVIO=1`: liga o "receber o link por e-mail". Só ligue com o remetente configurado.
- `NEXT_PUBLIC_VENDA_ABERTA=0`: fecha a venda.

O site é estático: **não use** rotas `app/api`, `connection()`, `cookies()`, `headers()`, server actions nem nada que precise de servidor Node. O build falha ou o recurso some no Pages.

## 5. Deploy do servidor (folego.py / servidor.py)

- Gere um zip só com os arquivos alterados (nunca inclua `.env`: `zip -x '.env'`).
- Mac: `scp -o ServerAliveInterval=20 arquivo.zip root@2.25.252.204:/root/`
- VPS: `cd /opt/mapadaalma && cp folego.py /root/folego-antes.py && unzip -o /root/arquivo.zip -d /opt/mapadaalma && systemctl restart mapadaalma && sleep 3 && curl -s localhost:8010/health`
- Sempre diga em qual terminal cada comando roda: Mac `carlosaugusto@macbook` ou VPS `root@srv2014776`.
- Para testar localmente antes, rode com o `TestClient` do FastAPI ou com o uvicorn na porta de teste.

Configuração no `/opt/mapadaalma/.env`:

| Chave | Para quê |
|---|---|
| `FOLEGO_CHECKOUT` | Código do checkout Kiwify (obrigatória) |
| `KIWIFY_TOKEN` | Lista separada por vírgula; inclui o token do webhook do Fôlego |
| `FOLEGO_REMETENTE`, `FOLEGO_CONTATO` | E-mail (o domínio precisa estar verificado na Resend). O e-mail do Fôlego **nunca** usa o "responder para" do Meu Santo. |
| `FOLEGO_ANTHROPIC_API_KEY` | Opcional; vazio = usa a chave do Meu Santo |
| `FOLEGO_MODELO` | Opcional; padrão `claude-opus-5-5` |
| `FOLEGO_SITE` | Padrão `https://folegofinanceiro.shop`: usado no link do e-mail e no CORS |
| `PRODUTO_FOLEGO` | Trecho do nome do produto na Kiwify (padrão `folego`; aceita `a\|b`) |

## 6. Comandos úteis (VPS)

```
cd /opt/mapadaalma
./venv/bin/python folego.py status            # funil e vendas 24 h / 7 dias, planos com IA x versão padrão
./venv/bin/python folego.py buscar EMAIL      # pedidos e compras de uma pessoa + link do plano + erro da IA
./venv/bin/python folego.py leads 30 > /root/leads.csv   # dados pessoais: use e apague
journalctl -u mapadaalma -n 100 --no-pager | grep folego
```
Use python3, não o comando `sqlite3`.

## 7. Regras (não negociáveis)

- **Chaves e segredos nunca vão para o chat.** Anthropic, Kiwify, Resend e o segredo da URL do webhook são colados direto no `.env` da VPS.
- **A VPS é compartilhada**: nunca reinicie o Docker nem a máquina, nunca rode `do-release-upgrade`. Ignore "System restart required". Reinicie só `systemctl restart mapadaalma`.
- **Não quebre o Meu Santo Protetor**: o `servidor.py` é dele. Mudanças do Fôlego ficam em `folego.py`. No `servidor.py`, só o mínimo: CFG `FOLEGO_*`, CORS, `include_router` e o desvio no webhook.
- **LGPD**: nada de e-mail, CPF ou telefone de cliente em documentos, prints ou relatórios. Só números agregados.
- **Copy financeira honesta**: não prometa limpar o nome, quitar em X meses nem descontos garantidos. O plano já diz "estimativa". Nada de depoimento falso, escassez falsa nem copy de anúncio que aponte condição pessoal ("Você está endividado?"): a Meta reprova.
- O plano orienta. Não é consultoria financeira nem jurídica, e o texto deve continuar dizendo isso.
