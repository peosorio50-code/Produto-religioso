# VSL da Novena pelos Filhos (página de vendas)

**Onde aparece:** logo depois da revelação grátis (a pessoa acabou de ver o santo de cada filho), antes do preço. Configurado em `site/config.js` → `VSL_SRC`. Começa sem som, com legenda, e o botão "🔊 Toque para ouvir".

**Duração alvo:** uns 4 minutos (~570 palavras). A da Biblioteca tinha 5 min 49 s e metade de quem ligou o som saiu no bloco lento da "tradição". Aqui não tem bloco de tradição: a história de Santa Mônica faz esse papel, e é uma história de verdade.

**Voz:** Jorge – Calm & Warm, as mesmas configurações de sempre. Grave **um bloco por vez** e mande antes o bloco V01 de teste para conferir o ritmo. Números estão por extenso; na legenda, eles viram algarismos (R$ 87).

**Formato:** 4:5, 720×900, até 22 MB (o limite do Cloudflare Pages é 25 MB por arquivo). Legenda queimada desde o primeiro segundo, porque o vídeo começa mudo.

**Regras que valem para a VSL inteira:**
- O narrador é "da equipe do Meu Santo Protetor". Nunca diz nem insinua ser padre.
- Nada de promessa: não dizer que o filho "vai voltar", "vai ser curado", "vai largar o vício".
- Nada de "Você é mãe?", "Você é católica?". O texto fala do produto e da situação.
- Sem escassez falsa, sem "de/por", sem depoimento.

---

### V01 · Gancho (0:00 a 0:20)
> Se você chegou até aqui, já sabe: todo filho nasce no dia de um santo. E agora você conhece o santo de cada um. Mas eu quero te contar a história de uma mãe que descobriu uma coisa ainda mais importante: o que fazer, todos os dias, por um filho que ela não conseguia mais alcançar.

*Imagem:* uma vela acesa e, ao lado, três santinhos sobre uma mesa de madeira. Legenda em destaque: **"Todo filho nasce no dia de um santo."**

### V02 · Santa Mônica (0:20 a 1:25)
> O nome dela era Mônica. Ela viveu no norte da África, há mais de mil e seiscentos anos. O filho mais velho, Agostinho, era muito inteligente, e se afastou de Deus ainda jovem. Foi embora de casa, viveu do jeito dele e não queria ouvir falar de fé.
>
> Mônica fez a única coisa que estava ao alcance dela: rezou. Rezou durante anos. Rezou chorando.
>
> Um dia, um bispo, vendo a aflição daquela mãe, disse a ela uma frase que o próprio Agostinho guardou para sempre num livro: não é possível que se perca o filho de tantas lágrimas.
>
> E quando Agostinho atravessou o mar e foi para a Itália, ela foi atrás. Lá, anos depois, ele voltou para Deus. Foi batizado, virou bispo e hoje é Santo Agostinho, um dos maiores santos da Igreja. E a mãe dele é Santa Mônica, lembrada até hoje por quem reza pelos filhos.

*Imagens:* "Santo Agostinho e Santa Mônica" (Ary Scheffer, 1846), com zoom lento nos rostos; mar ao entardecer; estrada antiga de pedra. Legenda da frase do bispo em destaque, com a fonte pequena embaixo: *Santo Agostinho, Confissões, III, 12*.

### V03 · Quem reza pelos filhos (1:25 a 2:00)
> Quem reza pelos filhos e pelos netos conhece esse aperto. O filho que pega a estrada à noite. A filha que anda triste e não conta por quê. O neto que está crescendo longe. Aquele que se afastou da fé, ou da família, por causa de uma briga. A gente não consegue estar junto em todos os caminhos. Mas pode fazer o que Mônica fez: entregar cada um a Deus, pelo nome, todos os dias.

*Imagens (sem rostos nítidos):* faróis de carro numa estrada à noite; menina de costas olhando pela janela; criança correndo num quintal; celular com uma mensagem não respondida; mãos de uma senhora segurando um terço.

### V04 · A novena (2:00 a 2:35)
> Foi pensando nisso que a equipe do Meu Santo Protetor preparou a Novena pelos Filhos. São nove dias. Em cada dia, um vídeo curto como este, de poucos minutos. Você aperta o play, reza junto, e na hora certa diz o nome de cada filho e de cada neto. No primeiro dia, você entrega cada um a Deus. Depois vem a oração que não desiste, a fé, a proteção dos anjos da guarda, a saúde, o filho que está longe, o trabalho e o futuro, a paz em casa. E no nono dia, você consagra cada um a Nossa Senhora.

*Imagens:* as capas dos 9 dias (`site/img/dia1.jpg` … `dia9.jpg`) passando uma a uma; um celular apoiado numa mesa, com o vídeo do primeiro dia tocando.

### V05 · O livro (2:35 a 3:10)
> Junto com os vídeos, você recebe o livro da novena em PDF, feito com o nome de quem você escreveu. O santo do dia em que cada um nasceu. Uma oração para cada um, pelo nome. A história de Santa Mônica. Os nove dias para ler, se preferir rezar sem o vídeo. O ato de consagração a Nossa Senhora, com um certificado para imprimir. Como dar a bênção. Orações para cada situação: quando sai de casa, numa prova, na doença, na tristeza, no vício, longe da fé. E um quadro com o nome de todos, para emoldurar.

*Imagens:* as páginas do livro de exemplo (`site/img/amostra-*.jpg`), deslizando, com a etiqueta pequena "livro de exemplo".

### V06 · Quem somos (3:10 a 3:30)
> Uma palavra de honestidade. Nós não somos uma paróquia, e eu não sou padre: sou da equipe do Meu Santo Protetor. Nada substitui a missa, os sacramentos e o padre da sua comunidade. E nós não prometemos milagre. Quem concede as graças é Deus. O que a novena oferece é companhia, para você rezar com constância, como Santa Mônica rezou.

*Imagem:* igreja vazia com luz entrando pelos vitrais. Legenda: **"Não somos paróquia. Não prometemos milagres."**

### V07 · Preço e como recebe (3:30 a 3:55)
> A Novena pelos Filhos custa oitenta e sete reais, num pagamento só, no Pix ou no cartão. Logo depois do pagamento, a página da sua novena abre na hora, com os nove vídeos e o livro para baixar. Tudo chega também no seu e-mail. E, durante os nove dias, você recebe de manhã um lembrete curto com o vídeo do dia.

*Imagem:* o celular com a página da novena (pode ser um print da página `novena.html` de teste). Legenda: **R$ 87 · pagamento único**.

### V08 · Garantia (3:55 a 4:05)
> E se não for o que você esperava, você tem sete dias para pedir o seu dinheiro de volta, sem precisar explicar nada.

*Imagem:* selo simples "7 dias de garantia" sobre o fundo azul.

### V09 · Chamada e fechamento (4:05 a 4:25)
> Toque no botão logo abaixo deste vídeo e comece hoje o primeiro dia. Cada filho, cada neto, entregue a Deus pelo nome. Santa Mônica, rogai por nós. Nossa Senhora, cobri os nossos filhos com o vosso manto.

*Imagem:* "Madonna della Misericordia" (Piero della Francesca) abrindo devagar; seta para baixo. Legenda: **Toque no botão abaixo 👇**.

---

## Cortes de anúncio a partir da VSL (9:16)

Depois da VSL pronta, dá para montar 3 cortes de 45 a 70 s em 9:16, como nos outros produtos, sempre fechando com o preço e a chamada (V07 + V09):
1. **Santa Mônica:** V02 → V04 (só o começo) → V07 → V09.
2. **O aperto:** V03 → V04 → V07 → V09.
3. **Por dentro:** V04 → V05 → V07 → V09.

No anúncio, a chamada muda: em vez de "toque no botão abaixo deste vídeo", use o bloco **A-CTA** do arquivo `04-ANUNCIOS-NARRADOS.md` ("Toque em Saiba mais e descubra, de graça, o santo de cada um").
