---
name: produto-digital
description: Cria e mantém produtos digitais de qualquer nicho (religioso, finanças, autoconhecimento, relacionamento, família, bem-estar e outros) vendidos com anúncios no Meta e checkout na Kiwify, e entregues pelo servidor FastAPI da VPS (/opt/mapadaalma) como PDF ou página personalizada com IA. Use sempre que o pedido for criar um produto novo ("faz um produto", "kit completo", "quero vender X"), mexer em quiz, página de vendas, order bump, upsell, webhook da Kiwify, geração por IA, PDF, e-mails, criativos ou anúncios, ou instalar uma atualização do servidor na VPS, mesmo que o pedido não cite marca nem nicho. Marcas conhecidas: Meu Santo Protetor (católico), Eu e a Minha Casa (evangélico), Fôlego (finanças), Mapa da Alma (autoconhecimento).
---

# Produtos digitais (Meta + Kiwify + servidor próprio)

O mesmo modelo serve para qualquer nicho:

> anúncio → quiz → resultado grátis na hora → oferta de um material personalizado → Kiwify → entrega automática em minutos

Esta skill guarda o modelo, as regras que valem para todos e as regras de cada nicho.

## O que ler antes de responder

| Situação | Leia |
|---|---|
| Qualquer trabalho | Este arquivo inteiro, mais o arquivo do nicho em `references/nichos/` |
| Produto novo | `references/playbook-produto-novo.md` e o exemplo mais parecido em `references/exemplos/` |
| Mexer no servidor ou instalar na VPS | `references/infraestrutura.md` |
| Contexto completo do negócio (história, números, o que já foi testado) | `references/nichos/manual-meu-santo-protetor.md`. Vale para todos os nichos, porque é o mesmo servidor e o mesmo jeito de trabalhar |

**Arquivos de cada nicho** (em `references/nichos/`):
- `religioso.md`: católico e evangélico;
- `financas.md`: dívidas, dinheiro, renda;
- `autoconhecimento.md`: astrologia, tarô, numerologia, perfil;
- `relacionamento-familia.md`;
- `saude-bem-estar.md`: o mais restrito no Meta.

**Se o nicho não estiver na lista:** use o mais parecido, siga as regras gerais e, no fim, proponha criar o arquivo do nicho novo (veja `references/nichos/COMO-CRIAR-NICHO.md`).

## Regras gerais (todos os nichos)

**Copy e anúncios (políticas do Meta e honestidade)**
- **Sem atributo pessoal na copy.** O texto fala do produto e da situação, nunca afirma algo sobre quem lê. Exemplos proibidos: "Você é católica?", "Você está endividado?", "Sofre de ansiedade?". Vale para religião, saúde, finanças, idade, orientação sexual e etnia.
- **Sem depoimento inventado, sem escassez ou contagem regressiva falsa, sem "de/por" falso, sem isca de engajamento.**
- Prazo só se for verdadeiro, sempre com a data em que ele sai do ar.
- **Nunca prometer resultado:** dinheiro, cura, emprego, casamento, nome limpo, "quitar em X meses". O produto orienta, acompanha ou inspira. Quando couber, escreva que é "estimativa" ou "material de apoio".
- **Sem cloaker, domínio ou pixel novo para fugir de classificação do Meta,** contas falsas, lista comprada ou raspada, ferramenta de spam.
- **Marcas separadas não se misturam.** O público católico nunca vê nada esotérico em domínio, e-mail ou página, e vice-versa. Cada marca tem domínio, remetente e tom próprios.
- Tema sensível leva aviso de ajuda gratuita, sem alarde:
  - crise emocional: CVV 188;
  - violência doméstica: Ligue 180;
  - saúde: procurar um profissional;
  - superendividamento: Procon e Defensoria.

**Operação**
- Chaves e tokens **nunca** no chat nem em arquivo. Eles ficam só no `/opt/mapadaalma/.env`.
- Zips sempre sem `.env`.
- **A VPS é compartilhada:** nunca reiniciar o Docker ou a máquina, nem rodar `do-release-upgrade`. Reinicie só com `systemctl restart mapadaalma`.
- **Produto novo = módulo próprio** (`produto.py`, tabelas `produto_*`). No `servidor.py`, só os ganchos mínimos. Não quebre os produtos que já vendem.
- Antes de substituir o `servidor.py`, mande conferir o `md5sum`.
- **LGPD:** nada de e-mail, CPF ou telefone de cliente em documento, print ou relatório. Só números agregados. Toda IA de terceiros usada na geração aparece na política de privacidade.
- Compra paga **nunca** fica sem entrega: a IA tem texto de reserva, e o que falhou volta sozinho para a fila.

## Jeito de trabalhar

- Português informal e direto, com a ação primeiro.
- Comandos prontos para copiar, **dizendo em qual terminal rodar**:
  - **Mac** (`scp -o ServerAliveInterval=20 ARQ root@2.25.252.204:/root/`);
  - **VPS** `root@srv2014776`.
- Aponte o que pode melhorar e **discorde quando for o caso**. Não concorde só por concordar.
- Assuma ROAS ≥ 1 e não peça o gasto do anúncio.
- Mude uma coisa por vez nos testes. Em queda de vendas, confira checkout e rastreamento antes de mexer em criativo.
- Errou? Assuma o erro e corrija na hora.
- Seja honesto sobre o que não testou e diga o que precisa ser conferido no primeiro uso real.

## Produto novo: o kit completo (entregue tudo de uma vez)

1. **Raciocínio** (`docs/ESTRATEGIA.md`):
   - por que este produto;
   - as alternativas descartadas;
   - preço e escada de ofertas;
   - o líquido por venda (taxa da Kiwify de ~8,99% + R$ 2,49) e o CPA de empate;
   - os riscos.
2. **Nome exato para a Kiwify.** O servidor reconhece o produto por um trecho do nome: confira se ele não colide com os trechos `PRODUTO_*` já usados (`2027`, `ritual`, `livro de oracoes`, `devocionario`, `folego`...).
3. Preço, descrição, order bumps (acima de R$ 10) e upsell na página de obrigado.
4. Imagem 1000×1000 e banners 1200×400 e 1080×540, nas cores da marca.
5. **Páginas:**
   - vendas, com quiz e resultado grátis;
   - obrigado, com upsell e entrega na própria página;
   - dados, só de reserva;
   - privacidade.
6. **Servidor:** módulo próprio com:
   - IA com texto de reserva;
   - entrega em PDF ou em página;
   - e-mails, recuperação de vendas e lembretes;
   - comandos de linha (`diagnostico`, `status`, `funil`, `buscar`, `refazer`, `teste`);
   - teste ponta a ponta com o `TestClient`.
7. E-mails de entrega, dados, lembretes e recuperação.
8. Criativos: 5 a 10 estáticos 4:5 e vídeos 9:16, e uma legenda única.
9. `COMO-SUBIR.md` (Kiwify → servidor → site → teste → anúncios) e um guia para o Claude.
10. Zips em `entregas/` e commit.
11. **Confira antes de entregar:**
    - páginas no tamanho de celular;
    - quadros dos vídeos;
    - páginas do PDF;
    - webhook simulado.

## Modelos prontos

- `templates/`: implementação completa de um produto **em PDF** (*O Santo do Nosso Casamento*):
  - `templates/servidor/`: módulo, conteúdo, PDF e teste;
  - `templates/site/`: quiz, obrigado com upsell, dados e privacidade;
  - renderizadores de criativos (Playwright + ffmpeg).

  Para outro nicho, troque `casamento_conteudo.py`, o prompt (`SISTEMA`), o quiz e as cores. O resto (webhook, fila, e-mails, recuperação, PDF, testes) serve como está.
- `references/exemplos/guia-folego-financas.md`: um produto **entregue como página** (Next.js estático), com o plano montado no navegador. Use esse formato quando o produto for interativo ou tiver muitas contas.
