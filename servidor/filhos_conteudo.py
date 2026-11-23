"""Novena pelos Filhos (Meu Santo Protetor): textos fixos, iguais para todos, preenchidos com os nomes.

Regras que valem para todo texto deste arquivo (as mesmas do Meu Santo Protetor):
- o santo não é adorado: intercede; quem concede é Deus;
- nada de promessa de resultado ("o seu filho vai voltar", "vai ser curado"), nada de superstição ou corrente;
- versículo só com a referência (a pessoa lê na Bíblia dela), sem citação literal;
- saúde: reza pela pessoa e lembra do cuidado médico; vício e crise emocional: lembra onde há ajuda gratuita;
- os 9 dias da novena são os mesmos dos 9 vídeos (roteiros em filhos/roteiros/): se mudar um, mude o outro.

Marcadores do grupo (filhos_pdf.contexto):
  {QUEM} primeiro nome de quem reza · {PAPEL} mãe/avó/pai/avô · {Q_o} "a"/"o" (cansada/cansado)
  {NOMES} "Pedro, Ana e Lucas" · {OS_FILHOS} "os meus filhos", "o meu neto"... (e {DOS_FILHOS} {PELOS_FILHOS} {AOS_FILHOS}) · {FILHOS} "filhos", "netos", "filhos e netos"
  {eles} {deles} {os} concordância do grupo (eles/elas/ele/ela; deles...; os/as/o/a)
  {INVOCACOES} "São José, rogai por Pedro. Santa Rita de Cássia, rogai por Ana."
  {FALECIDOS} frase sobre quem já partiu (vazia se ninguém)
Marcadores de uma pessoa (bênçãos, livro de cada filho, orações por situação):
  {N} nome (ou "(nome)" nas orações por situação quando há mais de um) · {o} o/a · {ele} {Ele} {dele}
  {filho} filho/filha/neto/neta · {SEU_PAPEL} "sua mãe", "sua avó", "seu pai", "seu avô" · {ASSIN} "mãe", "vó", "pai", "vô"
"""

# ------------------------------------------------------------------ orações de sempre
PAI_NOSSO = ("Pai nosso que estais nos céus, santificado seja o vosso nome; venha a nós o vosso Reino; seja feita a vossa vontade, assim na terra "
             "como no céu. O pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; "
             "e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém.")
AVE_MARIA = ("Ave, Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. "
             "Santa Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora da nossa morte. Amém.")
GLORIA = "Glória ao Pai, ao Filho e ao Espírito Santo. Como era no princípio, agora e sempre. Amém."
SANTO_ANJO = ("Santo Anjo do Senhor, meu zeloso guardador, se a ti me confiou a piedade divina, sempre me rege, me guarda, me governa e me ilumina. Amém.")
A_VOSSA_PROTECAO = ("À vossa proteção recorremos, Santa Mãe de Deus; não desprezeis as nossas súplicas em nossas necessidades, mas livrai-nos "
                    "sempre de todos os perigos, ó Virgem gloriosa e bendita. Amém.")
SALVE_RAINHA = ("Salve, Rainha, Mãe de misericórdia, vida, doçura e esperança nossa, salve! A vós bradamos, os degredados filhos de Eva; a vós "
                "suspiramos, gemendo e chorando neste vale de lágrimas. Eia, pois, advogada nossa, esses vossos olhos misericordiosos a nós volvei; "
                "e, depois deste desterro, mostrai-nos Jesus, bendito fruto do vosso ventre, ó clemente, ó piedosa, ó doce sempre Virgem Maria. "
                "Rogai por nós, santa Mãe de Deus, para que sejamos dignos das promessas de Cristo. Amém.")
CREIO = ("Creio em Deus Pai todo-poderoso, criador do céu e da terra; e em Jesus Cristo, seu único Filho, nosso Senhor, que foi concebido pelo "
         "poder do Espírito Santo; nasceu da Virgem Maria; padeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado; desceu à mansão dos "
         "mortos; ressuscitou ao terceiro dia; subiu aos céus; está sentado à direita de Deus Pai todo-poderoso, donde há de vir a julgar os vivos "
         "e os mortos. Creio no Espírito Santo, na santa Igreja Católica, na comunhão dos santos, na remissão dos pecados, na ressurreição da carne, "
         "na vida eterna. Amém.")
O_MEU_JESUS = ("Ó meu Jesus, perdoai-nos, livrai-nos do fogo do inferno, levai as almas todas para o Céu e socorrei principalmente as que mais "
               "precisarem.")

ORACOES_DE_SEMPRE = [
    ("Sinal da Cruz", "Em nome do Pai, do Filho e do Espírito Santo. Amém."),
    ("Pai-Nosso", PAI_NOSSO),
    ("Ave-Maria", AVE_MARIA),
    ("Glória ao Pai", GLORIA),
    ("Santo Anjo", SANTO_ANJO),
    ("À vossa proteção (a oração mais antiga a Nossa Senhora)", A_VOSSA_PROTECAO),
    ("Salve-Rainha", SALVE_RAINHA),
    ("Jaculatória da família", "Jesus, Maria e José, a nossa família vos pertence."),
]

FECHO_DIA = ("Reze um Pai-Nosso, uma Ave-Maria e um Glória. Santa Mônica, rogai por nós. Nossa Senhora, cobri-{os} com o vosso manto.")

# ------------------------------------------------------------------ como rezar (livro e área)
COMO_REZAR = ("Durante nove dias seguidos, reserve uns dez minutos para rezar {PELOS_FILHOS}. Cada dia tem um vídeo de poucos minutos: "
              "abra a página da sua novena, aperte o play e reze junto. Quando o narrador pedir, diga em voz alta o nome de cada um. "
              "Se preferir, ou se estiver sem internet, reze só com este livro: cada dia traz a leitura, a reflexão, a oração e um gesto simples.")
COMO_REZAR_DICAS = [
    "Escolha um horário e um cantinho: de manhã cedo, depois do almoço, antes de dormir. O que importa é a constância.",
    "Se quiser, acenda uma vela perto de uma imagem de Nossa Senhora ou de um crucifixo. Não é obrigatório: é só um sinal.",
    "Perdeu um dia? Não tem problema. Continue de onde parou. A novena não é uma regra: é uma companhia.",
    "Não precisa contar para {eles}. Rezar por alguém em silêncio é uma das formas mais bonitas de amar.",
    "Ao terminar o nono dia, você pode começar de novo quando quiser, por exemplo antes de um aniversário na família.",
]

# ------------------------------------------------------------------ a novena (os mesmos 9 dias dos vídeos)
NOVENA = [
    {"titulo": "Os filhos que Deus me confiou", "leitura": "1 Samuel 1,9-28",
     "reflexao": "A Bíblia conta a história de Ana, uma mulher que rezava tanto pelo filho que ainda não tinha que o sacerdote achou que ela estava "
                 "embriagada. Quando Samuel nasceu, ela voltou ao templo e disse que era por aquele menino que tinha rezado, e o entregou a Deus. "
                 "Toda novena pelos filhos começa assim: lembrando que eles são de Deus antes de serem nossos. Não é perder: é colocar em mãos "
                 "mais fortes do que as nossas.",
     "oracao": "Senhor Deus, Pai de todos nós, eu, {QUEM}, Vos agradeço pela vida {DOS_FILHOS}: {NOMES}. {Cada_um} é um presente que "
               "eu não mereci. Vós {os} conheceis desde sempre e {os} amais mais do que eu consigo amar. Hoje eu {os} entrego "
               "de novo nas Vossas mãos, como Ana entregou Samuel. Guardai-{os} pelo nome. {FALECIDOS}{INVOCACOES} Amém.",
     "gesto": "Escreva num papel o nome de cada um e guarde dentro da sua Bíblia ou junto de uma imagem de Nossa Senhora durante os nove dias."},
    {"titulo": "A oração que não desiste", "leitura": "Lucas 18,1-8",
     "reflexao": "Jesus contou a história de uma viúva que ia todos os dias pedir justiça a um juiz, até ser atendida, e disse que é preciso rezar "
                 "sempre, sem desanimar. Santa Mônica viveu isso: rezou durante anos pelo filho Agostinho, que tinha se afastado de Deus. "
                 "Às vezes a oração de uma mãe parece não dar em nada. Mas nenhuma oração feita com amor se perde diante de Deus. Ele escuta, "
                 "e responde do jeito e no tempo que só Ele conhece.",
     "oracao": "Senhor Jesus, Vós nos ensinastes a rezar sem desanimar. Às vezes eu me canso, me preocupo demais, acho que a minha oração não "
               "adianta. Dai-me a perseverança de Santa Mônica. Que eu nunca deixe de rezar por {NOMES}, nos dias bons e nos difíceis. "
               "Tirai de mim a ansiedade e deixai só a confiança. Eu não sei o que é melhor para {eles}; Vós sabeis. Santa Mônica, mãe que não "
               "desistiu, rezai comigo. Amém.",
     "gesto": "Escolha um horário fixo para os próximos dias da novena e coloque um lembrete no celular."},
    {"titulo": "A fé que passa de geração em geração", "leitura": "2 Timóteo 1,3-5",
     "reflexao": "São Paulo escreveu a Timóteo lembrando que a fé dele tinha começado na avó, Loide, e na mãe, Eunice. A fé quase sempre chega "
                 "assim: pelo colo, pela mesa, pelo exemplo de quem rezava em casa. Não depende de discurso nem de cobrança. Depende de testemunho, "
                 "de paciência e da graça de Deus, que trabalha em cada coração do jeito d'Ele.",
     "oracao": "Espírito Santo, que acendestes a fé no meu coração, acendei também no coração de {NOMES}. Que a fé {deles} seja viva, alegre e "
               "verdadeira, e não só um costume. Se {eles} {estiverem} perto de Vós, guardai essa amizade. Se {estiverem} longe, ide ao encontro "
               "{deles} pelos caminhos que só Vós conheceis. Que o meu exemplo fale mais do que as minhas palavras. Nossa Senhora, mãe da fé, "
               "rogai por nós. Amém.",
     "gesto": "Conte a {um_deles} uma lembrança de fé da sua família, ou mande uma mensagem curta dizendo que rezou hoje."},
    {"titulo": "Proteção: os anjos da guarda", "leitura": "Salmo 91 (90)",
     "reflexao": "O salmo fala de Deus como um abrigo e diz que Ele dá ordens aos seus anjos para nos guardar em todos os caminhos. A Igreja ensina "
                 "que cada pessoa tem um anjo da guarda que a acompanha desde o começo da vida (Catecismo, n. 336). Quando um filho sai de casa, "
                 "pega a estrada ou volta tarde, o coração aperta. Hoje, entregue {OS_FILHOS} aos cuidados de Deus e do anjo que acompanha cada um.",
     "oracao": "Senhor, sede o abrigo de {NOMES}. Guardai-{os} no trânsito, na rua, na escola, no trabalho e em todos os caminhos. Livrai-{os} da "
               "violência, das más companhias e de tudo o que possa fazer mal ao corpo e à alma. {Anjos} de {NOMES}, velai por "
               "{eles} de dia e de noite, e trazei-{os} sempre de volta para casa em paz. Amém.",
     "gesto": "Reze o Santo Anjo (está nas orações de sempre) uma vez por cada um, dizendo o nome."},
    {"titulo": "Saúde do corpo, da mente e do coração", "leitura": "Marcos 5,21-24.35-43",
     "reflexao": "Jairo era um pai desesperado: a filha estava muito doente e ele se jogou aos pés de Jesus pedindo por ela. Jesus foi com ele. "
                 "Hoje muitas dores dos filhos não aparecem por fora: ansiedade, tristeza, cansaço, solidão. Reze pela saúde inteira de cada um. "
                 "E lembre: rezar não substitui o médico, o psicólogo nem o tratamento. Deus também age pelas mãos de quem cuida.",
     "oracao": "Senhor Jesus, que fostes à casa de Jairo, vinde também até {NOMES}. Cuidai da saúde {deles}: do corpo, da mente e "
               "do coração. Onde houver doença, dai alívio e bons médicos. Onde houver tristeza ou ansiedade, dai paz e coragem para pedir ajuda. "
               "Onde houver cansaço, dai descanso. E a mim, dai sabedoria para perceber quando {eles} {precisam} de mim, e discrição para respeitar "
               "o tempo {deles}. Amém.",
     "gesto": "Mande uma mensagem ou ligue para {um_deles} só para perguntar: como você está de verdade?"},
    {"titulo": "O filho que está longe", "leitura": "Lucas 15,11-32",
     "reflexao": "Na parábola do filho pródigo, o pai não sai correndo atrás do filho para obrigá-lo a voltar. Ele espera, olha para a estrada todos "
                 "os dias e, quando o filho aparece ao longe, corre ao seu encontro e o abraça antes de ouvir qualquer explicação. Há filhos longe "
                 "de casa, longe da fé, longe da família por uma briga. O coração de Deus é o coração desse pai, e o nosso pode aprender com ele.",
     "oracao": "Pai de misericórdia, Vós conheceis as distâncias que às vezes existem entre mim e {OS_FILHOS}, e entre {eles} e Vós. Eu não "
               "quero cobrar nem forçar: quero rezar e deixar a porta aberta. Onde houver distância, guardai o caminho e preparai o "
               "reencontro do Vosso jeito. Curai as mágoas que eu causei e as que eu carrego. Dai-me um coração parecido com o Vosso, que espera "
               "sem desistir e abraça sem humilhar. Santa Mônica, rogai por {NOMES}. Amém.",
     "gesto": "Mande uma mensagem curta e sem cobrança para quem está longe: só para dizer que você se lembrou e rezou."},
    {"titulo": "Trabalho, estudos e o futuro", "leitura": "Jeremias 29,11-13 e Mateus 6,31-34",
     "reflexao": "Pelo profeta Jeremias, Deus diz que tem para o seu povo projetos de paz. E Jesus nos convida a não viver angustiados pelo amanhã, "
                 "buscando primeiro o Reino. Estudos, provas, emprego, contas, escolhas: o futuro dos filhos tira o sono de muita gente. Hoje, "
                 "entregue esse futuro a Deus, sem pedir que tudo saia do seu jeito, mas que nada falte a {eles} do que é essencial.",
     "oracao": "Senhor, eu Vos entrego o futuro de {NOMES}. Abençoai os estudos, o trabalho e as escolhas {deles}. Dai-{lhes} "
               "sabedoria para decidir, coragem para recomeçar e honestidade em tudo o que fizerem. Que nunca lhes falte o pão de cada dia nem "
               "a dignidade do trabalho. E livrai-me da ansiedade de querer controlar o caminho {deles}: que eu confie mais em Vós. São José, "
               "trabalhador de Nazaré, rogai por {eles}. Amém.",
     "gesto": "Faça o sinal da cruz sobre a mochila, o material de estudo ou a carteira de trabalho de {um_deles}, ou sobre uma foto."},
    {"titulo": "Paz em casa e união entre irmãos", "leitura": "Salmo 133 (132) e Gênesis 45,1-15",
     "reflexao": "O salmo diz como é bom e agradável os irmãos viverem unidos. Mas a Bíblia também conta a história de José do Egito, vendido "
                 "pelos próprios irmãos, que anos depois os perdoou e os abraçou chorando. Em toda família há ciúmes, palavras duras, distâncias. "
                 "A paz não nasce de ninguém ter razão: nasce de alguém dar o primeiro passo. Às vezes esse alguém somos nós.",
     "oracao": "Senhor, Príncipe da Paz, fazei da nossa família uma casa de paz. Uni a nossa família com laços de carinho e de respeito. Curai as "
               "feridas entre irmãos, entre pais e filhos, entre sogros, genros e noras. Tirai do meu coração o rancor e a vontade de ter "
               "sempre razão. Dai-me palavras que constroem e silêncio quando for melhor calar. Jesus, Maria e José, a nossa família vos pertence. Amém.",
     "gesto": "Dê hoje um passo de paz: um pedido de perdão, uma ligação, um convite para um café."},
    {"titulo": "Debaixo do manto de Maria", "leitura": "João 19,25-27",
     "reflexao": "Aos pés da cruz, Jesus entregou Maria ao discípulo amado e o discípulo a Maria. Desde então, a Igreja vê em Maria a mãe de todos "
                 "os que seguem o seu Filho. Uma das orações mais antigas a Nossa Senhora, a 'À vossa proteção', pede justamente isso: abrigo "
                 "debaixo do seu cuidado. Hoje, no último dia da novena, você vai entregar {OS_FILHOS} a Nossa Senhora com o Ato de Consagração, "
                 "que está na página seguinte, com o nome de cada um.",
     "oracao": "Maria, Mãe de Jesus e nossa Mãe, chegamos ao último dia desta novena. Eu Vos agradeço por estes nove dias e entrego nas vossas "
               "mãos {NOMES}. Cobri-{os} com o vosso manto. Onde eu não puder chegar, chegai vós; quando eu não souber o que dizer, falai vós ao "
               "vosso Filho por {eles}. Ensinai-{os} a dizer sim a Deus, como vós dissestes. {INVOCACOES} Nossa Senhora Aparecida, rogai por nós. Amém.",
     "gesto": "Reze o Ato de Consagração com calma e, se puder, acenda uma vela. Depois, guarde o papel com os nomes dentro da Bíblia."},
]

INTENCAO_PADRAO = "que Deus guarde {NOMES} com fé, saúde e paz"

# ------------------------------------------------------------------ Santa Mônica
MONICA_HISTORIA = [
    "Mônica nasceu por volta do ano 331, em Tagaste, no norte da África, onde hoje fica a Argélia. Casou-se com Patrício, um homem de "
    "temperamento difícil e que não tinha fé. Ela rezou por ele com paciência durante anos, e ele foi batizado pouco antes de morrer.",
    "O filho mais velho, Agostinho, era muito inteligente e se afastou da fé ainda jovem. Mônica rezou e chorou por ele durante muitos anos. "
    "Um bispo, vendo a aflição dela, disse-lhe uma frase que o próprio Agostinho guardou no livro das Confissões: \"Vai, e continua assim: não é "
    "possível que se perca o filho de tantas lágrimas\" (Confissões, livro III, capítulo 12).",
    "Quando Agostinho foi para a Itália, ela atravessou o mar e foi atrás dele, até Milão. Lá, ele ouviu as pregações de Santo Ambrósio, voltou "
    "para Deus e foi batizado na Páscoa do ano 387. Poucos meses depois, Mônica morreu em Óstia, perto de Roma. Aos filhos, pediu só uma coisa: "
    "que se lembrassem dela no altar do Senhor, onde quer que estivessem.",
    "Agostinho se tornou bispo, santo e um dos grandes Doutores da Igreja. A Igreja celebra Santa Mônica em 27 de agosto e Santo Agostinho no "
    "dia seguinte, 28 de agosto. Ela é lembrada como padroeira das mães e das esposas que rezam pela família.",
]
MONICA_LICOES = [
    ("Rezar sem desistir", "Mônica não rezou uma semana: rezou anos. A constância é a forma mais humilde de confiança."),
    ("Rezar sem desesperar", "Ela chorou, e não escondeu a dor. Mas entregou a dor a Deus, em vez de carregá-la sozinha."),
    ("Estar perto, sem sufocar", "Ela acompanhou o filho de perto, mas foi Deus quem tocou o coração dele, no tempo d'Ele e pelo caminho que Ele escolheu."),
    ("Cuidar da própria fé", "Mônica não esperou a conversão de ninguém para viver a fé: ia à igreja, ajudava os pobres, rezava todos os dias."),
]
MONICA_ORACAO = ("Santa Mônica, mãe paciente e perseverante, que rezastes tantos anos pelo vosso marido e pelo vosso filho, olhai para {OS_FILHOS}, "
                 "{NOMES}. Ensinai-me a rezar como vós rezastes: sem desistir, sem desesperar e confiando sempre em Deus. Apresentai ao Senhor as "
                 "minhas lágrimas e os meus pedidos. E pedi para mim a paz de quem sabe que {OS_FILHOS} {estao} nas mãos de Deus. Amém.")

# ------------------------------------------------------------------ consagração e bênção
CONSAGRACAO_INTRO = ("Consagrar os filhos a Nossa Senhora é um costume antigo das famílias católicas: é colocar cada um, pelo nome, debaixo do cuidado "
                     "da Mãe de Jesus. É uma entrega feita com o coração. Não substitui o Batismo nem nenhum sacramento, e não depende de "
                     "ninguém saber ou concordar: é a sua oração por {eles}. Reze no nono dia da novena e, se quiser, renove todo ano, por "
                     "exemplo no dia 12 de outubro (Nossa Senhora Aparecida) ou no dia 8 de dezembro (Imaculada Conceição).")
CONSAGRACAO_ATO = ("Ó Maria, Mãe de Jesus e nossa Mãe, que aos pés da cruz recebestes como filhos todos os discípulos do vosso Filho, eu, {QUEM}, "
                   "venho hoje entregar-vos {OS_FILHOS}: {NOMES}. {Eles_sao} de Deus antes de serem meus, e por isso {os} coloco nas vossas mãos. "
                   "Eu {os} consagro a vós: o corpo, a mente, o coração, a fé, o trabalho, os estudos, os amores e o futuro {deles}. Cobri-{os} "
                   "com o vosso manto. Guardai-{os} de todo mal. Onde eu não puder estar, estai vós; quando eu não souber o que fazer, intercedei "
                   "vós junto ao vosso Filho. Ensinai-{os} a dizer sim a Deus, como vós dissestes em Nazaré. E eu prometo continuar rezando por "
                   "{eles} todos os dias da minha vida. Nossa Senhora Aparecida, Mãe e Rainha, a vós {os} entrego. Amém.")
BENCAO_INTRO = ("No Brasil, muitos filhos ainda pedem: \"A bênção, mãe\", \"A bênção, vó\". É um costume bonito e cristão. O Catecismo da Igreja "
                "Católica lembra que todo batizado é chamado a ser uma bênção e a abençoar (n. 1669). A bênção dos pais e dos avós não substitui a "
                "bênção do padre: é a oração de quem ama, dita em voz alta sobre quem é amado.")
BENCAO_PASSOS = [
    "Coloque a mão sobre a cabeça ou o ombro de quem você vai abençoar, ou faça com o polegar uma pequena cruz na testa. Se a pessoa estiver longe, pode abençoar por "
    "telefone, por mensagem ou olhando uma foto.",
    "Diga o nome e as palavras abaixo, devagar.",
    "Termine com o sinal da cruz. Pode ser todos os dias: na saída para a escola ou o trabalho, na despedida de uma visita, antes de dormir.",
]
BENCAO = ("{N}, que Deus te abençoe e te guarde. Que Ele te mostre o seu rosto e tenha misericórdia de ti. Que Ele volte para ti o seu olhar e "
          "te dê a paz. Em nome do Pai, do Filho e do Espírito Santo. Amém.")
BENCAO_FONTE = "Inspirada na bênção de Números 6,24-26."

# ------------------------------------------------------------------ orações para cada situação ({N} = o nome, ou "(nome)" se houver mais de um)
SITUACOES = [
    ("Quando sai de casa", "Senhor, {N} está saindo agora. Ide junto. Guardai o caminho, o trânsito, as companhias e a volta. Santo Anjo da Guarda, "
                           "acompanhai cada passo. Que volte para casa em paz. Amém."),
    ("Antes de uma prova, uma entrevista ou um dia importante", "Espírito Santo, iluminai {N} neste dia. Dai-lhe calma, memória, clareza e "
                           "confiança. Que faça a sua parte com honestidade e entregue o resto a Vós. Seja qual for o resultado, que saiba que é "
                           "amado por Vós e por mim. Amém."),
    ("Quando está doente", "Senhor Jesus, que curastes tantos doentes, olhai para {N}. Dai-lhe alívio na dor, força no tratamento e confiança. "
                           "Abençoai os médicos, os enfermeiros e todos que cuidam. Que não falte o cuidado médico, e que não falte a fé. Amém."),
    ("Quando está triste ou ansioso", "Senhor, Vós conheceis a tristeza que pesa no coração de {N}, mesmo a que não consegue dizer. Ficai perto. "
                           "Dai-lhe descanso, esperança e pessoas boas por perto. Dai-me paciência para ouvir sem julgar, e coragem para ajudar a "
                           "procurar um profissional, se for preciso. Amém."),
    ("Quando se afastou da fé", "Senhor, eu Vos entrego o coração de {N}. Não quero cobrar nem discutir: quero rezar. Tocai esse coração do Vosso "
                           "jeito e no Vosso tempo. Que o meu exemplo fale mais do que as minhas palavras. Santa Mônica, que rezastes tantos anos "
                           "por Agostinho, rezai comigo. Amém."),
    ("Quando está preso a um vício", "Senhor, Vós vedes a luta de {N} contra o vício. Eu não consigo carregar isto sozinh{Q_o}. Dai-lhe a vontade de "
                           "pedir ajuda e pessoas certas no caminho. Dai-me firmeza com amor, para não alimentar o vício nem abandonar a pessoa. "
                           "Livrai a nossa família do desespero. Amém."),
    ("Quando está sem trabalho", "São José, que sustentastes a Sagrada Família com o trabalho das vossas mãos, olhai para {N}. Pedi a Deus "
                           "por um trabalho digno, coragem para procurar, humildade para aceitar recomeços e paz para atravessar este tempo. Amém."),
    ("Quando vai se casar ou formar a própria família", "Senhor, abençoai a família que {N} está formando. Dai-lhe um amor fiel, paciente e "
                           "generoso. E dai-me a sabedoria de apoiar sem me intrometer, de aconselhar sem decidir e de amar também quem chega à "
                           "nossa família. Jesus, Maria e José, rogai por {N}. Amém."),
    ("Quando está passando por uma separação", "Senhor, o coração de {N} está ferido. Ficai perto nesta dor. Dai-lhe paz para decidir, força para "
                           "recomeçar e proteção para as crianças, se houver. Livrai-me de julgar e de tomar partido com raiva: quero ser abrigo. Amém."),
    ("Pela gravidez na família", "Senhor da vida, abençoai a criança que está para nascer e a mãe que a espera. Guardai as duas vidas, dai saúde, "
                           "calma e um parto tranquilo. Sant'Ana, mãe de Nossa Senhora e avó de Jesus, rogai por esta família. Amém."),
    ("Quando mora longe", "Senhor, a distância não chega até Vós. Guardai {N} onde estiver: a casa, o trabalho, a saúde, as amizades. Que não lhe "
                           "falte nada do que é essencial, e que sinta, mesmo de longe, que é amado e lembrado. Amém."),
    ("Depois de uma briga", "Senhor, hoje {N} e eu nos machucamos. Acalmai o meu coração e tirai de mim a vontade de ganhar a discussão. Dai-nos "
                           "humildade para pedir perdão e generosidade para perdoar. Que a gente não termine longe um do outro. Amém."),
    ("Quando me sinto cansad{Q_o} ou culpad{Q_o}", "Senhor, às vezes eu acho que errei demais com {OS_FILHOS}. Vós conheceis as minhas falhas e "
                           "também o meu amor. Curai o que eu fiz de errado, completai o que eu não soube fazer e tirai de mim o peso da culpa. "
                           "Santa Mônica, ensinai-me a confiar. Amém."),
    ("Por um filho ou neto que já partiu", "Senhor, eu Vos entrego {N}, que já partiu desta vida. Dai-lhe o descanso eterno e a luz que não se apaga. "
                           "Consolai o meu coração e o de toda a família. Que um dia nos encontremos na Vossa casa. Nossa Senhora das Dores, "
                           "que conhecestes a dor de perder um filho, ficai comigo. Amém."),
    ("Antes de dormir", "Senhor, terminamos mais um dia. Guardai o sono {DOS_FILHOS}, onde quer que {eles} {estejam}. {Anjos}, velai "
                           "por {eles} esta noite. Em Vossas mãos, Senhor, entregamos a nossa vida. Amém."),
]
AJUDA = [
    ("Tristeza profunda ou pensamentos de morte", "CVV: ligue 188, de graça, 24 horas, ou acesse cvv.org.br. Em caso de risco, SAMU 192."),
    ("Álcool e drogas", "Os CAPS AD do SUS atendem de graça. Alcoólicos Anônimos e Narcóticos Anônimos têm grupos em todo o Brasil."),
    ("Para a família de quem tem um vício", "Al-Anon, Nar-Anon e Amor-Exigente são grupos gratuitos de apoio para pais, mães e parentes."),
    ("Violência contra criança ou adolescente", "Disque 100 (Direitos Humanos), de graça, 24 horas. Em perigo, 190."),
]
AJUDA_INTRO = "Rezar não substitui a ajuda de profissionais. Se alguém da sua família estiver passando por alguma destas situações, procure:"

PALAVRA_FINAL = ("Este livro é um material de oração pessoal, preparado pela equipe do Meu Santo Protetor. Não somos uma paróquia, e nada aqui "
                 "substitui a missa, os sacramentos, a confissão ou a orientação de um padre. Os santos não fazem milagres sozinhos: eles rezam "
                 "conosco e por nós, e quem concede as graças é Deus, que sabe o que é melhor para cada filho. Que esta novena seja o começo, ou a "
                 "continuação, de uma vida inteira rezando por quem você ama.")

# ------------------------------------------------------------------ order bump: 30 Bênçãos para Mandar aos Filhos
BENCAOS_INTRO = ("São 30 mensagens curtas para mandar {AOS_FILHOS} pelo WhatsApp, uma por dia, ou para ler em voz alta para quem ainda é pequeno. "
                 "Cada uma já vem com o nome. Na página da sua novena tem um botão para copiar cada mensagem e mandar direto. Não precisa mandar "
                 "todas: mande quando o coração pedir.")
BENCAOS = [
    "{N}, bom dia! Hoje cedo eu pedi a Deus por você. Que Ele abençoe o seu dia do começo ao fim.",
    "{N}, rezei por você hoje. Que Deus guarde os seus caminhos, na ida e na volta.",
    "Que Nossa Senhora cubra você com o manto dela hoje, {N}. Você nunca está sozinh{o}.",
    "{N}, Deus te conhece pelo nome e te ama do jeito que você é. Eu também.",
    "Que o seu anjo da guarda vá na sua frente hoje, {N}. Fica com Deus.",
    "{N}, que Deus te dê calma nas horas difíceis e alegria nas pequenas coisas. Pensei em você.",
    "Hoje eu agradeci a Deus pela sua vida, {N}. Você é um presente na minha.",
    "{N}, que o Espírito Santo te dê sabedoria em cada decisão de hoje.",
    "Que nada te falte hoje, {N}: nem o pão, nem a paz, nem a fé. Rezei por isso.",
    "{N}, se o dia estiver pesado, lembra: tem alguém rezando por você agora mesmo.",
    "Que Deus abençoe o seu trabalho e os seus estudos, {N}. Faça a sua parte e deixe o resto com Ele.",
    "{N}, que Jesus seja o seu descanso hoje. Não carregue tudo sozinh{o}.",
    "Hoje eu entreguei você nas mãos de Nossa Senhora, {N}. Pode ir tranquil{o}.",
    "{N}, que Deus cuide da sua saúde: do corpo, da cabeça e do coração.",
    "Que o seu dia seja cheio de gente boa, {N}. Deus te guarde.",
    "{N}, a bênção de Deus Pai, do Filho e do Espírito Santo esteja com você hoje e sempre.",
    "Rezei um terço por você hoje, {N}. Cada Ave-Maria levou o seu nome.",
    "{N}, Deus não desiste de ninguém, e eu também não desisto de rezar por você.",
    "Que a paz de Deus entre na sua casa hoje, {N}, e fique.",
    "{N}, que você tenha coragem para recomeçar quantas vezes for preciso. Deus está junto.",
    "Que São José abençoe o seu trabalho e a sua casa, {N}.",
    "{N}, que hoje você sinta, de algum jeito, o quanto é amad{o}. Por Deus e por mim.",
    "Pedi a Deus que te livre de todo perigo hoje, {N}. Vai com Ele.",
    "{N}, que a sua fé seja do tamanho que você precisa para hoje. Nem mais, nem menos.",
    "Que Deus te dê um sono tranquilo esta noite, {N}. Boa noite e fica com Deus.",
    "{N}, obrigad{Q_o} por existir. Rezei por você e por tudo o que você carrega.",
    "Que Santa Mônica, que rezou anos pelo filho, reze também por você hoje, {N}.",
    "{N}, que Deus abençoe as pessoas que você ama e os caminhos que você escolher.",
    "Hoje eu acendi uma vela e disse o seu nome, {N}. Que a luz de Deus brilhe na sua vida.",
    "{N}, Nossa Senhora Aparecida te abençoe e te guarde, hoje e sempre. Com todo o meu amor.",
]

# ------------------------------------------------------------------ order bump: Terço pelos Filhos (mistérios gozosos)
TERCO_INTRO = ("Os cinco mistérios gozosos contam a infância de Jesus: o anúncio, a espera, o nascimento, a apresentação no Templo e o menino "
               "perdido e encontrado. São os mistérios de uma mãe e de um pai cuidando de um filho. Por isso eles foram escolhidos para este terço: "
               "em cada mistério, você oferece {OS_FILHOS} a Deus pelas mãos de Maria. O vídeo reza junto com você; o roteiro completo está "
               "nas próximas páginas.")
TERCO_COMO = [
    "Faça o sinal da cruz e reze o Creio.",
    "Reze um Pai-Nosso, três Ave-Marias (pela fé, pela esperança e pela caridade) e um Glória.",
    "Em cada mistério: leia o título e a meditação, diga a oferta com os nomes, reze um Pai-Nosso, dez Ave-Marias, um Glória e o \"Ó meu Jesus\".",
    "No fim, reze a Salve-Rainha e a oração \"À vossa proteção\".",
]
TERCO = [
    ("1º mistério: a Anunciação do Anjo a Maria", "Lucas 1,26-38",
     "Um anjo anuncia a Maria que ela será a mãe do Filho de Deus, e ela responde: faça-se. Toda vida começa com um sim de Deus. Neste mistério, "
     "agradeça pelo dia em que soube que {cada_um} existia.",
     "Neste mistério, eu Vos agradeço, Senhor, pela vida de {NOMES}. Que {eles} {saibam} dizer sim a Vós, como Maria."),
    ("2º mistério: a Visitação de Maria a Isabel", "Lucas 1,39-56",
     "Grávida, Maria vai depressa ajudar a prima Isabel, que também esperava um filho. As duas se alegram juntas. Neste mistério, reze pela família "
     "que cerca {OS_FILHOS}: avós, tios, padrinhos, amigos, e pelas crianças que ainda vão chegar.",
     "Neste mistério, eu Vos ofereço {NOMES} e todas as pessoas que {os} amam. Que nunca lhes falte gente boa por perto."),
    ("3º mistério: o Nascimento de Jesus", "Lucas 2,1-20",
     "Jesus nasce pobre, numa manjedoura, cercado de cuidado. {Cada_um} também nasceu num dia que a Igreja dedica a um santo. Neste "
     "mistério, lembre o dia em que {cada_um} nasceu e peça a intercessão desse santo.",
     "Neste mistério, eu Vos ofereço o dia em que {cada_um} nasceu. {INVOCACOES}"),
    ("4º mistério: a Apresentação de Jesus no Templo", "Lucas 2,22-40",
     "Maria e José levam o menino ao Templo para apresentá-lo a Deus. O velho Simeão diz a Maria que uma espada traspassaria a sua alma. Toda mãe "
     "conhece essa espada: a dor de ver um filho sofrer. Neste mistério, consagre {OS_FILHOS} a Deus e entregue a Ele as suas dores.",
     "Neste mistério, eu apresento a Vós {NOMES}, como Maria e José apresentaram Jesus. Eu {os} entrego a Vós: guardai-{os}."),
    ("5º mistério: a Perda e o Encontro de Jesus no Templo", "Lucas 2,41-52",
     "Durante três dias, Maria e José procuraram o menino, aflitos, até encontrá-lo no Templo. Até a Sagrada Família passou pela angústia de um "
     "filho longe. Neste mistério, reze por quem está longe de casa, da família ou da fé.",
     "Neste mistério, eu Vos entrego quem está longe. Ide ao encontro de {NOMES} por onde {eles} {estiverem}, e trazei-{os} para perto de Vós."),
]
TERCO_FINAL = ("Terminado o terço, fique um minuto em silêncio. Você pode rezar este terço todos os dias, ou num dia fixo da semana: muitas "
               "famílias escolhem o sábado, dia dedicado a Nossa Senhora.")

# ------------------------------------------------------------------ upsell: Um Livro para Cada Filho
LIVRO_CARTA = {  # {N} nome, {QUEM} quem rezou, {SEU_PAPEL} "sua mãe"...
    "crianca": ("{N}, este livrinho é seu. Ele foi feito a pedido de {SEU_PAPEL}, {QUEM}, que reza por você todos os dias. Aqui você vai conhecer "
                "o santo do dia em que você nasceu, que é um amigo seu lá no Céu, e vai encontrar orações para rezar antes de dormir, quando estiver "
                "com medo e quando estiver feliz. Peça para alguém ler com você, se precisar. Deus te ama muito."),
    "jovem": ("{N}, este livro foi feito a pedido de {SEU_PAPEL}, {QUEM}, que reza por você todos os dias, mesmo quando você não sabe. Não é uma "
              "cobrança nem um sermão: é um presente. Aqui está o santo do dia em que você nasceu, a oração que {SEU_PAPEL} reza por você, uma "
              "bênção e uma oração curta para os dias em que você quiser conversar com Deus. Guarde no celular. Um dia ele pode fazer sentido."),
    "adulto": ("{N}, este livro foi preparado a pedido de {SEU_PAPEL}, {QUEM}, que reza por você todos os dias. Aqui está o santo que a Igreja "
               "recorda no dia em que você nasceu, a oração que {SEU_PAPEL} reza por você, pelo seu nome, e uma bênção para guardar. É um gesto "
               "simples de quem ama e confia você a Deus. Que ele chegue num bom momento."),
}
LIVRO_ORACAO = {
    "crianca": ("Papai do Céu, obrigado por mais um dia. Obrigado pela minha família, pela minha casa e pelos meus amigos. Cuida de mim quando eu "
                "estiver dormindo e quando eu estiver brincando. Meu anjo da guarda, fica do meu lado. Nossa Senhora, me dá a mão. Amém."),
    "jovem": ("Senhor, Tu me conheces melhor do que eu mesm{o}. Nos dias em que eu estiver perdid{o}, cansad{o} ou com medo, fica perto. Me ajuda a "
              "fazer boas escolhas, a ter amigos de verdade e a não desistir de mim. Obrigad{o} pela minha vida e por quem reza por mim. Amém."),
    "adulto": ("Senhor, eu Te entrego o meu dia, o meu trabalho, a minha casa e as pessoas que eu amo. Dá-me paz no que eu não posso mudar, coragem "
               "para mudar o que eu posso e sabedoria para perceber a diferença. Obrigad{o} pela minha vida e por quem reza por mim. Amém."),
}
LIVRO_SANTINHO = "Recorte, guarde na carteira, na capa do celular ou no espelho. É um lembrete de que alguém reza por você."
