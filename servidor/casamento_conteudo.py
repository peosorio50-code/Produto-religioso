"""O Santo do Nosso Casamento: textos fixos (iguais para todos, com os nomes do casal).

Regras que valem para todo texto deste arquivo (as mesmas do Meu Santo Protetor):
- o santo não é adorado: intercede; quem concede é Deus;
- nada de promessa de resultado ("o seu casamento vai mudar"), nada de superstição;
- versículo só com a referência (a pessoa lê na Bíblia dela), sem citação literal;
- rezar pelo casamento NUNCA significa aceitar violência: o aviso do 180 aparece onde o tema pede.

Marcadores (trocados por casamento_pdf.preencher):
  {ELA} {ELE}         primeiros nomes da esposa e do marido
  {DATA}              "12 de junho de 1993"
  {INVOCACAO}         "Santo Antônio, rogai por nós." (ou "Santa Maria, Mãe de Deus, rogai por nós." se o dia for festa do Senhor)
  {INTERCESSAO}       "pela intercessão de Santo Antônio"
  {QUEM} {CONJ}       quem reza e o cônjuge por quem reza (orações individuais)
Nos 30 dias (gênero de quem recebe a oração): {N} {ele} {Ele} {dele} {nele} {o} {x} {pai} {marido}
"""

# ------------------------------------------------------------------ orações de sempre
ORACOES_DE_SEMPRE = [
    ("Sinal da Cruz", "Em nome do Pai, do Filho e do Espírito Santo. Amém."),
    ("Pai-Nosso", "Pai nosso que estais nos céus, santificado seja o vosso nome; venha a nós o vosso Reino; seja feita a vossa vontade, "
                  "assim na terra como no céu. O pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos "
                  "a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém."),
    ("Ave-Maria", "Ave, Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. "
                  "Santa Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora da nossa morte. Amém."),
    ("Glória ao Pai", "Glória ao Pai, ao Filho e ao Espírito Santo. Como era no princípio, agora e sempre. Amém."),
    ("Jaculatória da família", "Jesus, Maria e José, a nossa família vos pertence."),
]

# ------------------------------------------------------------------ novena do casal (livro principal)
NOVENA_INTRO = ("Durante nove dias seguidos, rezem juntos, de preferência no mesmo horário: depois do jantar, antes de dormir, quando der. "
                "Cada dia leva uns dez minutos. Leiam a passagem na Bíblia de vocês, a reflexão e a oração do dia, e terminem com um Pai-Nosso, "
                "uma Ave-Maria e um Glória. Se um dos dois não puder ou não quiser rezar, quem reza pode rezar pelos dois: "
                "a oração de um já é um presente para o outro.")

NOVENA = [
    {"titulo": "O dia do nosso sim", "leitura": "Gênesis 2,18-24",
     "reflexao": "Tudo começou com um sim. No dia {DATA}, vocês disseram sim um ao outro. Desde então, muita coisa aconteceu: alegrias, lutas, "
                 "mudanças. Mas aquele sim continua de pé, e hoje vocês o entregam de novo nas mãos de Deus. Antes de rezar, lembrem juntos "
                 "de um momento bonito daquele dia.",
     "oracao": "Senhor Deus, que criastes o homem e a mulher e os chamastes a ser uma só carne, nós, {ELA} e {ELE}, Vos agradecemos pelo dia "
               "em que dissemos sim um ao outro. Nós Vos agradecemos por tudo o que vivemos desde então: as alegrias, as lutas e o que aprendemos juntos. "
               "Renovai em nós a graça daquele dia, e que o nosso sim seja, a cada manhã, um pouco mais verdadeiro. {INVOCACAO} Amém."},
    {"titulo": "O amor é paciente", "leitura": "1 Coríntios 13,4-7",
     "reflexao": "São Paulo escreveu que o amor é paciente, não guarda rancor, tudo desculpa e tudo espera. Não é uma lista para cobrar do outro: "
                 "é um espelho para cada um olhar para si. Hoje, cada um pense em silêncio: em que ponto eu preciso ter mais paciência?",
     "oracao": "Senhor Jesus, Vós sois paciente conosco todos os dias. Ensinai-nos a ter paciência um com o outro. Quando a palavra dura estiver "
               "na ponta da língua, dai-nos um segundo de silêncio. Quando o cansaço falar mais alto, lembrai-nos do quanto nos amamos. "
               "Livrai a nossa casa do rancor e enchei-a de pequenos gestos de carinho. Nós Vos pedimos {INTERCESSAO}. Amém."},
    {"titulo": "Saber ouvir", "leitura": "Tiago 1,19-20",
     "reflexao": "São Tiago aconselha a ser rápido para ouvir e lento para falar. No casamento, muita briga nasce de duas pessoas falando e "
                 "ninguém ouvindo. Hoje, experimentem: cada um fala por alguns minutos sobre como está se sentindo, e o outro só escuta, "
                 "sem responder e sem corrigir.",
     "oracao": "Espírito Santo, abri os nossos ouvidos e o nosso coração. Que {ELA} se sinta ouvida e que {ELE} se sinta ouvido. "
               "Tirai de nós a pressa de responder e a vontade de ter sempre razão. Dai-nos palavras que constroem e a coragem de dizer, com calma, "
               "o que dói. Que a nossa casa seja um lugar onde cada um pode falar e ser acolhido. {INVOCACAO} Amém."},
    {"titulo": "O perdão", "leitura": "Colossenses 3,12-15",
     "reflexao": "Não existe casamento sem perdão. Perdoar não é fingir que nada aconteceu nem aceitar o que machuca: é decidir não carregar mais "
                 "o peso do rancor e entregá-lo a Deus. Às vezes o perdão leva tempo. Hoje, peçam a graça de dar o primeiro passo e, se for o caso, "
                 "peçam perdão com palavras simples.",
     "oracao": "Pai de misericórdia, Vós nos perdoais sempre que voltamos para Vós. Ensinai-nos a perdoar como somos perdoados. Curai as feridas "
               "que fizemos um no outro, as que lembramos e as que esquecemos. Tirai de nós o orgulho que impede de pedir perdão e a dureza que "
               "impede de perdoar. Que nenhum dia termine com mágoa entre nós. Nós Vos pedimos {INTERCESSAO}. Amém."},
    {"titulo": "A casa sobre a rocha", "leitura": "Mateus 7,24-27",
     "reflexao": "Jesus fala de uma casa construída sobre a rocha: vieram a chuva, os rios e os ventos, e ela não caiu. A rocha da casa de vocês é Deus. "
                 "Não é preciso fazer coisas difíceis: uma oração curta juntos, a missa de domingo, um agradecimento antes de comer. São essas pedras "
                 "que seguram a casa nas tempestades.",
     "oracao": "Senhor, sede Vós a rocha da nossa casa. Quando vierem as chuvas e os ventos, as dificuldades de dinheiro, de saúde ou de família, "
               "que a nossa casa não caia, porque está firmada em Vós. Ajudai-nos a dar a Vós o primeiro lugar, na oração de cada dia e no domingo. "
               "Abençoai cada cômodo desta casa e todos os que entram nela. {INVOCACAO} Amém."},
    {"titulo": "A família que formamos", "leitura": "Salmo 128 (127)",
     "reflexao": "O salmo fala da mesa da família como uma bênção de Deus. Cada família tem a sua forma: com muitos filhos, com poucos, sem filhos, "
                 "com netos, com afilhados, com os pais que moram junto. Hoje, rezem pelo nome de cada pessoa que faz parte da família de vocês, "
                 "uma por uma.",
     "oracao": "Senhor, nós Vos entregamos a nossa família, cada pessoa pelo nome (digam aqui o nome de cada um). Protegei os que moram conosco "
               "e os que estão longe. Dai-nos sabedoria para orientar, paciência para conviver e humildade para pedir ajuda. Que a nossa mesa "
               "nunca fique sem pão nem sem alegria. Jesus, Maria e José, a nossa família vos pertence. Amém."},
    {"titulo": "O pão de cada dia", "leitura": "Mateus 6,25-34",
     "reflexao": "Contas, trabalho, desemprego, dívidas: o dinheiro é uma das maiores fontes de briga num casamento. Jesus não diz que essas coisas "
                 "não importam: diz que o Pai sabe do que precisamos e nos convida a buscar primeiro o Reino. Hoje, entreguem juntos a Deus as "
                 "preocupações com o trabalho e com as contas, e conversem com calma sobre um passo prático.",
     "oracao": "Pai, Vós conheceis as nossas necessidades antes mesmo de pedirmos. Abençoai o trabalho das nossas mãos. Dai-nos o pão de cada dia "
               "e a sabedoria para cuidar bem do que temos. Livrai-nos da ansiedade que rouba a paz e das brigas por causa de dinheiro. "
               "Que nunca falte o necessário na nossa casa, e que sempre sobre um pouco para partilhar com quem tem menos. "
               "São José, trabalhador de Nazaré, rogai por nós. Amém."},
    {"titulo": "Um ajudando o outro", "leitura": "Eclesiastes 4,9-12",
     "reflexao": "O Eclesiastes diz que dois valem mais do que um: se um cair, o outro o levanta. E fala de um cordão de três fios, que não se "
                 "rompe facilmente. Muitos casais veem nesses três fios o marido, a esposa e Deus. Hoje, rezem pela saúde de vocês dois e pelos "
                 "momentos em que um precisa carregar o outro.",
     "oracao": "Senhor, Vós nos unistes para caminharmos juntos, na saúde e na doença, na alegria e na tristeza. Quando um de nós cair, que o outro "
               "esteja perto para levantar. Cuidai da saúde de {ELA} e de {ELE}: do corpo, da mente e do coração. Nos dias de cansaço e de dor, "
               "sede Vós o terceiro fio que não deixa o cordão se romper. {INVOCACAO} Amém."},
    {"titulo": "Fazei tudo o que Ele vos disser", "leitura": "João 2,1-11",
     "reflexao": "Nas bodas de Caná, o vinho acabou no meio da festa. Foi Maria quem percebeu e levou o problema a Jesus, e disse aos que serviam "
                 "que fizessem tudo o que Ele mandasse. E o melhor vinho ficou para o fim. Em todo casamento, às vezes o vinho acaba. Hoje, "
                 "entreguem nas mãos de Maria o que está faltando na casa de vocês.",
     "oracao": "Maria, Mãe de Jesus e nossa Mãe, vós que estivestes nas bodas de Caná, olhai para o nosso casamento. Vós sabeis o que está faltando "
               "na nossa casa, mesmo o que não conseguimos dizer. Levai o nosso pedido ao vosso Filho, e nós queremos fazer o que Ele nos disser. "
               "Senhor Jesus, que os anos que vêm sejam de mais amor, mais paz e mais fé. {INVOCACAO} Jesus, Maria e José, a nossa família vos pertence. Amém."},
]

# ------------------------------------------------------------------ santos dos casais
SANTOS_CASAIS = [
    ("A Sagrada Família de Nazaré", "domingo depois do Natal",
     "Jesus, Maria e José: a família em que o Filho de Deus quis crescer. Uma casa simples, de trabalho e de oração, que passou por muitas "
     "dificuldades: a viagem a Belém, a fuga para o Egito, a vida escondida em Nazaré. A Igreja celebra a Sagrada Família no domingo depois do Natal."),
    ("São José", "19 de março",
     "O esposo de Maria. A Bíblia não guarda nenhuma palavra dele, só gestos: acolheu, protegeu, trabalhou e confiou. É o padroeiro da Igreja, "
     "dos trabalhadores e das famílias, e o modelo dos esposos e dos pais."),
    ("São Joaquim e Sant'Ana", "26 de julho",
     "Segundo uma tradição antiga da Igreja, são os pais de Nossa Senhora e os avós de Jesus. Por isso, no Brasil, 26 de julho é também o Dia dos Avós. "
     "São lembrados como o casal que esperou com fé e criou Maria no amor a Deus."),
    ("São Luís Martin e Santa Zélia Guérin", "12 de julho",
     "Ele era relojoeiro; ela fazia rendas, em Alençon, na França, no século XIX. Casaram-se em 1858 e tiveram nove filhos, quatro dos quais "
     "morreram pequenos. A caçula é Santa Teresinha do Menino Jesus. Em 2015, o Papa Francisco os canonizou juntos: foi a primeira vez que um "
     "casal foi declarado santo na mesma cerimônia."),
    ("Santa Mônica", "27 de agosto",
     "Viveu no norte da África, no século IV. Casada com Patrício, um homem de temperamento difícil e que não tinha fé, rezou por ele a vida inteira; "
     "ele foi batizado pouco antes de morrer. Depois, rezou durante muitos anos pela conversão do filho, que se tornou Santo Agostinho. "
     "É lembrada como padroeira das mães e das esposas que rezam pela família."),
    ("Santa Rita de Cássia", "22 de maio",
     "Viveu na Itália, entre os séculos XIV e XV. A tradição conta que se casou muito jovem, com um homem de temperamento violento, e que rezou "
     "por ele até ele mudar de vida. Viúva, e depois de perder os dois filhos, entrou no mosteiro das agostinianas de Cássia. É chamada a santa "
     "das causas impossíveis e é muito procurada nos momentos difíceis do casamento."),
    ("Santo Antônio", "13 de junho",
     "Frade franciscano nascido em Lisboa, morreu em Pádua, em 1231. Grande pregador e Doutor da Igreja. O povo brasileiro o chama de santo "
     "casamenteiro, e a véspera da festa dele, 12 de junho, virou o Dia dos Namorados."),
]

# ------------------------------------------------------------------ sacramento (varia: casados na Igreja ou não)
SACRAMENTO_IGREJA = ("Quando dois batizados se casam na Igreja, o próprio casamento é um sacramento: um sinal do amor de Cristo, que permanece com "
                     "o casal todos os dias, e não só no dia da cerimônia. A graça do sacramento não ficou na igreja, naquele dia: ela mora na casa "
                     "de vocês e pode ser pedida em cada oração deste livro.")
SACRAMENTO_CIVIL = ("Este livro é para vocês do mesmo jeito: Deus ouve a oração de todo casal que procura por Ele. Se um dia desejarem receber o "
                    "sacramento do Matrimônio, procurem a paróquia e conversem com o padre, sem medo. Cada situação é diferente, e ele saberá orientar. "
                    "Muitas paróquias fazem casamentos comunitários e ajudam os casais a se preparar.")

# ------------------------------------------------------------------ renovação das promessas em casa
RENOVACAO_INTRO = ("Um gesto simples para o aniversário de casamento ou para qualquer dia especial. Não substitui nenhum rito da Igreja: "
                   "é uma oração do casal, em casa.")
RENOVACAO_PASSOS = [
    "Acendam uma vela e coloquem perto dela uma imagem de Jesus ou de Nossa Senhora e, se tiverem, uma foto do casamento.",
    "Façam o sinal da cruz e leiam juntos o Evangelho das bodas de Caná (João 2,1-11).",
    "De mãos dadas, cada um diz ao outro, olhando nos olhos, as palavras abaixo.",
    "Terminem com a oração do casal e um Pai-Nosso, rezado juntos.",
]
RENOVACAO_FALA = ("Eu, {A}, agradeço a Deus por você, {B}. Hoje eu renovo o sim que disse a você no dia {DATA}. Quero continuar ao seu lado "
                  "nos dias bons e nos difíceis, na saúde e na doença, todos os dias da minha vida. Peço perdão pelo que errei e perdoo o que me "
                  "feriu. Com a ajuda de Deus, quero amar você um pouco melhor a cada dia.")
RENOVACAO_FINAL = ("Senhor, que nos unistes no dia {DATA}, renovai em nós o amor daquele dia. Guardai o nosso casamento, {INTERCESSAO}. "
                   "Jesus, Maria e José, a nossa família vos pertence. Amém.")
RENOVACAO_DICA = ("Muitas paróquias abençoam os casais no aniversário de casamento ou num domingo especial. Conversem com o padre da sua "
                  "paróquia: a bênção da Igreja é um presente que nenhum livro substitui.")

# ------------------------------------------------------------------ orações para cada momento
MOMENTOS = [
    ("Ao acordar", "Senhor, nós Vos agradecemos por mais um dia juntos. Abençoai o nosso trabalho, os nossos caminhos e as pessoas que vamos encontrar. "
                   "Que hoje sejamos gentis um com o outro, e que à noite possamos Vos agradecer por um dia bem vivido. Amém."),
    ("Bênção da mesa", "Abençoai, Senhor, esta mesa, as mãos que prepararam este alimento e a nossa família aqui reunida. "
                       "Dai pão a quem tem fome e fome de Vós a quem tem pão. Amém."),
    ("Depois de uma briga", "Senhor, hoje nós nos machucamos. Acalmai o nosso coração e tirai de nós a vontade de ganhar a discussão. "
                            "Dai-nos humildade para pedir perdão e generosidade para perdoar. Que este dia não termine com a gente longe um do outro. Amém."),
    ("Quando falta dinheiro", "São José, que sustentastes a Sagrada Família com o trabalho das vossas mãos, olhai para a nossa casa. Vós conheceis "
                              "as nossas contas e as nossas preocupações. Pedi a Deus por nós: trabalho digno, sabedoria para gastar, coragem para mudar "
                              "o que for preciso e união para atravessar este tempo sem brigas. Amém."),
    ("Quando um de nós está doente", "Senhor Jesus, que curastes tantos doentes, olhai para quem está doente na nossa casa. Dai-lhe força, alívio na dor "
                                     "e confiança. Abençoai os médicos, os enfermeiros e todos que cuidam dessa pessoa. Dai a quem cuida paciência e descanso. "
                                     "Que não falte o cuidado médico, e que não falte a fé. Amém."),
    ("Pela fé de {CONJ}", "Senhor, Vós conheceis o coração de {CONJ}. Não quero cobrar nem obrigar: quero rezar. Tocai esse coração do Vosso jeito e no "
                          "Vosso tempo. Que o meu exemplo fale mais do que as minhas palavras. Santa Mônica, que rezastes tantos anos pelo vosso marido "
                          "e pelo vosso filho, rezai comigo. Amém."),
    ("No aniversário de casamento", "Senhor, hoje completamos mais um ano de casamento. Nós Vos agradecemos por cada um destes anos: pelos dias de festa "
                                    "e pelos dias de luta, pelo que construímos e pelo que aprendemos. Perdoai o que fizemos de errado e abençoai o "
                                    "caminho que ainda temos pela frente. {INVOCACAO} Amém."),
    ("Antes de dormir", "Senhor, terminamos mais um dia. Nós Vos agradecemos pelo que foi bom e pedimos perdão pelo que não foi. Guardai o nosso sono, a nossa casa e as "
                        "pessoas que amamos. Santo Anjo da Guarda de cada um de nós, velai por nós esta noite. Em vossas mãos, Senhor, entregamos o "
                        "nosso espírito. Amém."),
    ("Nos dias difíceis", "Senhor, estamos passando por um tempo difícil no nosso casamento. Vós sabeis tudo o que aconteceu, até o que não conseguimos "
                          "dizer. Não pedimos que tudo se resolva de uma vez, mas que não nos falte a Vossa presença. Dai-nos humildade para buscar ajuda: "
                          "uma conversa com o padre, um casal amigo, um profissional. Santa Rita de Cássia, rogai por nós. Amém."),
]

AVISO_VIOLENCIA = ("Rezar pelo casamento nunca significa aceitar violência. Se existe agressão, ameaça ou humilhação, a sua segurança vem primeiro: "
                   "procure ajuda. Ligue 180 (Central de Atendimento à Mulher, gratuita, 24 horas) ou 190 em caso de perigo. A Igreja ensina que, "
                   "em alguns casos, a separação do casal pode ser necessária (Catecismo da Igreja Católica, n. 2383).")

PALAVRA_FINAL = ("Este livro é um material de oração pessoal, preparado pela equipe do Meu Santo Protetor. Não somos uma paróquia, e nada aqui "
                 "substitui a missa, os sacramentos, a confissão ou a orientação de um padre. Os santos não fazem milagres sozinhos: eles rezam "
                 "conosco e por nós, e quem concede as graças é Deus, que sabe o que é melhor para cada casal. Que este livro ajude vocês a rezar "
                 "juntos, um pouco a cada dia.")

# ------------------------------------------------------------------ datas fixas para o calendário do casal
FESTAS_2027 = [  # (mês, dia, nome, observação)
    (3, 19, "São José", "padroeiro das famílias"),
    (5, 22, "Santa Rita de Cássia", "os casamentos em momentos difíceis"),
    (6, 13, "Santo Antônio", "o santo casamenteiro"),
    (7, 12, "São Luís e Santa Zélia Martin", "o casal santo"),
    (7, 26, "São Joaquim e Sant'Ana", "os avós de Jesus"),
    (8, 27, "Santa Mônica", "as esposas que rezam pela família"),
    (10, 12, "Nossa Senhora Aparecida", "a padroeira do Brasil"),
    (12, 26, "Sagrada Família de Nazaré", "o domingo depois do Natal"),
]

BODAS = {1: "Bodas de Papel", 5: "Bodas de Madeira", 10: "Bodas de Estanho", 15: "Bodas de Cristal", 20: "Bodas de Porcelana",
         25: "Bodas de Prata", 30: "Bodas de Pérola", 50: "Bodas de Ouro", 60: "Bodas de Diamante"}

# ------------------------------------------------------------------ order bump: 30 Dias Rezando pelo Meu Marido (ou pela minha esposa)
GENERO = {
    "m": {"ele": "ele", "Ele": "Ele", "dele": "dele", "nele": "nele", "o": "o", "x": "o", "pai": "pai", "marido": "meu marido"},
    "f": {"ele": "ela", "Ele": "Ela", "dele": "dela", "nele": "nela", "o": "a", "x": "a", "pai": "mãe", "marido": "minha esposa"},
}

TRINTA_INTRO = ("Durante 30 dias, reze um pouco por {N}. Leva cinco minutos: leia o tema do dia, reze a oração e, se quiser, faça o gesto proposto. "
                "Não é preciso contar para {ele}: rezar por alguém, em silêncio, é uma das formas mais bonitas de amar. Se perder um dia, não tem "
                "problema. Continue de onde parou.")

TRINTA = [
    ("A fé", "Efésios 3,14-19",
     "Senhor, eu Vos entrego {N}. Aumentai a fé {dele}. Que {ele} descubra, do jeito {dele} e no Vosso tempo, o quanto é amad{x} por Vós. "
     "Não quero cobrar nem pressionar: quero apenas rezar e deixar que Vós trabalheis. Amém.",
     "Agradeça a Deus, em silêncio, por três qualidades de {N}."),
    ("O coração", "Ezequiel 36,26",
     "Senhor, tocai o coração de {N}. Onde houver dureza, colocai ternura; onde houver mágoa, colocai paz; onde houver cansaço, colocai alegria. "
     "Guardai o coração {dele} de tudo o que afasta de Vós e da nossa família. Amém.",
     "Pergunte, sem pressa: como você está de verdade?"),
    ("Os pensamentos", "Filipenses 4,6-8",
     "Senhor, guardai os pensamentos de {N}. Livrai-{o} da ansiedade, do desânimo e das preocupações que tiram o sono. Que {ele} pense no que é "
     "verdadeiro, justo e bom. Dai-lhe uma mente serena e confiante. Amém.",
     "Deixe um bilhete com uma frase de incentivo."),
    ("O trabalho", "Salmo 90 (89),17",
     "Senhor, abençoai o trabalho de {N}. Dai-lhe força, competência e honestidade. Que {ele} seja respeitad{x} e trate bem quem trabalha ao lado {dele}. "
     "Se estiver sem trabalho ou insatisfeit{x}, abri caminhos. São José, trabalhador, rogai por {ele}. Amém.",
     "Pergunte como foi o dia {dele} e escute até o fim."),
    ("A saúde", "3 João 1,2",
     "Senhor, cuidai da saúde de {N}: do corpo, da mente e do coração. Dai-lhe disposição para cada dia e prudência para se cuidar. "
     "Se houver alguma doença, dai-lhe alívio, bons médicos e coragem. Amém.",
     "Incentive um cuidado: um exame atrasado, uma caminhada juntos."),
    ("O descanso", "Mateus 11,28-30",
     "Senhor Jesus, Vós chamastes para perto de Vós os cansados e sobrecarregados. Dai descanso a {N}. Aliviai o peso que {ele} carrega em silêncio. "
     "Que {ele} encontre em casa um lugar de paz, e não mais uma cobrança. Amém.",
     "Poupe {N} de uma tarefa hoje e deixe {ele} descansar."),
    ("As palavras", "Efésios 4,29",
     "Senhor, abençoai as palavras de {N}. Que da boca {dele} saiam palavras que constroem. E abençoai as minhas palavras também: que eu não fale "
     "com dureza nem com desprezo. Que a nossa casa seja um lugar de palavras boas. Amém.",
     "Elogie {N} hoje, de verdade, de preferência na frente de alguém."),
    ("A paciência", "Gálatas 5,22-23",
     "Senhor, dai a {N} o fruto da paciência, e dai a mim também. Quando o dia for pesado, que {ele} não descarregue em quem ama, e que eu saiba "
     "acolher sem revidar. Ensinai-nos a esperar um pelo outro. Amém.",
     "Respire fundo antes de responder a qualquer coisa que irrite."),
    ("As amizades", "Provérbios 27,17",
     "Senhor, abençoai as amizades de {N}. Dai-lhe amigos verdadeiros, que façam bem a {ele}, e afastai as companhias que levam para longe de Vós "
     "e de casa. Amém.",
     "Convide um casal amigo para um café."),
    ("As tentações", "1 Coríntios 10,13",
     "Senhor, protegei {N} das tentações: do vício, da mentira e de tudo o que destrói por dentro. Dai-lhe força nos momentos de fraqueza e humildade "
     "para pedir ajuda. Livrai a nossa casa de todo mal. Amém.",
     "Reze um Pai-Nosso por {N}, devagar, pensando no “livrai-nos do mal”."),
    ("Na família", "Colossenses 3,12-14",
     "Senhor, abençoai {N} em cada papel que {ele} tem na família: como {pai}, se Vós nos destes filhos, como filh{x}, como amig{x}. "
     "Que quem convive com {ele} encontre {nele} apoio e carinho. Amém.",
     "Conte para {N} uma coisa que você admira no jeito {dele} de cuidar das pessoas."),
    ("O perdão entre nós", "Mateus 18,21-22",
     "Senhor, curai o que ficou ferido entre mim e {N}. Perdoai as vezes em que eu {o} magoei e dai-me a graça de perdoar o que me magoou. "
     "Não deixeis o rancor morar na nossa casa. Amém.",
     "Se houver algo pendente, peça perdão com uma frase simples."),
    ("A alegria", "Neemias 8,10",
     "Senhor, devolvei a alegria a {N}. Que {ele} volte a rir das coisas simples, a curtir a família e a sentir gosto pela vida. "
     "Dai-nos momentos de leveza juntos. Amém.",
     "Planeje um momento divertido a dois, mesmo que simples."),
    ("A coragem", "Josué 1,9",
     "Senhor, dai coragem a {N} diante dos desafios. Que {ele} não se deixe vencer pelo medo, pelo fracasso nem pela opinião dos outros. "
     "Sede Vós a força {dele}. Amém.",
     "Diga hoje: eu acredito em você."),
    ("As contas da casa", "Mateus 6,31-34",
     "Senhor, abençoai a vida financeira da nossa casa. Dai a {N} e a mim sabedoria para ganhar, gastar e guardar. Livrai-nos das dívidas que "
     "sufocam e das brigas por dinheiro. Que confiemos em Vós sem deixar de fazer a nossa parte. Amém.",
     "Conversem dez minutos, com calma, sobre as contas do mês."),
    ("A humildade", "Filipenses 2,3-5",
     "Senhor, dai a {N} um coração humilde, e a mim também. Que saibamos reconhecer os nossos erros, pedir ajuda e ouvir conselhos. "
     "Tirai de nós o orgulho que separa. Amém.",
     "Reconheça hoje um erro seu, sem esperar que {ele} reconheça os {dele}."),
    ("A família {dele}", "Êxodo 20,12",
     "Senhor, abençoai a família de {N}: os pais, os irmãos, os parentes, os que estão vivos e os que já partiram. Curai as feridas antigas e "
     "ajudai-nos a conviver com amor e respeito. Amém.",
     "Mande uma mensagem carinhosa para alguém da família {dele}."),
    ("A fidelidade", "Cântico dos Cânticos 8,6-7",
     "Senhor, guardai a fidelidade entre mim e {N}. Protegei o nosso casamento de tudo o que pode dividir: das tentações, das distâncias e da rotina "
     "que esfria. Que o nosso amor seja forte, como o amor de que fala o Cântico. Amém.",
     "Relembrem juntos como se conheceram."),
    ("As decisões", "Tiago 1,5",
     "Senhor, iluminai as decisões de {N}. Que {ele} não decida com raiva nem com pressa. Dai-lhe o dom do conselho e a humildade para decidir "
     "junto comigo o que é da nossa casa. Amém.",
     "Peça a opinião {dele} sobre algo que você precisa decidir."),
    ("As feridas do passado", "Salmo 147 (146),3",
     "Senhor, Vós conheceis a história de {N}, as alegrias e as dores que {ele} traz desde criança. Curai as feridas que ainda doem. "
     "Que o passado não roube o presente {dele}. Amém.",
     "Tenha paciência com uma reação {dele} que vem de uma dor antiga."),
    ("A proteção", "Salmo 91 (90),11",
     "Senhor, protegei {N} nos caminhos: no trânsito, nas viagens, no trabalho, em todo lugar. Que o anjo da guarda {dele} {o} acompanhe. "
     "Livrai-{o} de todo perigo e trazei-{o} sempre de volta para casa. Amém.",
     "Peça que {ele} avise quando chegar."),
    ("A gratidão", "1 Tessalonicenses 5,18",
     "Senhor, eu Vos agradeço por {N}: pelo que {ele} é, pelo que já fez pela nossa família e pelo que vivemos juntos. Às vezes eu esqueço de "
     "agradecer; hoje eu quero lembrar. Amém.",
     "Escreva num papel três motivos de gratidão por {N}."),
    ("Os medos", "Isaías 41,10",
     "Senhor, Vós conheceis os medos de {N}, até os que {ele} não conta para ninguém. Acalmai o coração {dele}. Que {ele} sinta que não está "
     "sozinh{x}. Amém.",
     "Pergunte: o que está te preocupando?"),
    ("A vida de oração", "Lucas 11,1-4",
     "Senhor, ensinai {N} a rezar, como ensinastes os discípulos. Despertai {nele} a vontade de estar convosco, de ir à missa e de se confessar. "
     "E ajudai-me a rezar mais com {ele}, sem cobrar. Amém.",
     "Convide {N} para rezar com você, nem que seja um Pai-Nosso antes de dormir."),
    ("O nosso amor", "1 João 4,7-12",
     "Senhor, renovai o amor entre mim e {N}. Que a rotina não apague o carinho e que o tempo não esfrie a ternura. Ensinai-nos a amar com gestos, "
     "e não só com palavras. Amém.",
     "Faça um carinho inesperado."),
    ("Os sonhos", "Salmo 37 (36),4-5",
     "Senhor, abençoai os sonhos de {N}. Os que estão de acordo com a Vossa vontade, ajudai-{o} a realizar; os que não estão, dai-lhe paz para deixar ir. "
     "E que sonhemos também juntos. Amém.",
     "Pergunte qual é um sonho que {ele} ainda tem."),
    ("A mansidão", "Provérbios 15,1",
     "Senhor, dai a {N} um coração manso. Que a raiva não fale mais alto nas palavras e nos gestos {dele}. E dai-me sabedoria para não alimentar "
     "a briga. Amém.",
     "Quando sentir a briga começar, proponha uma pausa: vamos conversar daqui a pouco."),
    ("Envelhecer juntos", "Isaías 46,4",
     "Senhor, que eu e {N} possamos envelhecer juntos, cuidando um do outro. Dai-nos saúde, paciência com as limitações e um amor que amadurece "
     "com os anos. Amém.",
     "Olhem juntos uma foto antiga de vocês dois."),
    ("Servir", "Marcos 10,43-45",
     "Senhor, fazei de {N} uma pessoa que serve: em casa, no trabalho, na comunidade. Que {ele} encontre alegria em fazer o bem, e que eu {o} ajude "
     "nisso. Amém.",
     "Façam juntos um gesto de caridade nesta semana."),
    ("Nas mãos de Maria", "João 19,25-27",
     "Maria, Mãe de Jesus e nossa Mãe, eu vos entrego {N}. Cuidai {dele} como cuidastes de Jesus. Levai a Deus tudo o que rezei nestes 30 dias. "
     "Eu confio que Deus sabe o que é melhor para {ele} e para nós. Amém.",
     "Reze uma dezena do terço por {N}."),
]
TRINTA_FINAL = ("Os 30 dias terminaram, mas a oração continua. Você pode recomeçar do Dia 1 quantas vezes quiser, ou escolher o tema que mais "
                "fala ao seu coração em cada semana. Deus ouve cada oração que você fez por {N}, e responde do jeito e no tempo Dele.")

# ------------------------------------------------------------------ order bump: Novena de Santa Rita pelo Casamento
RITA_QUEM = ("Rita nasceu por volta de 1381, em Roccaporena, perto de Cássia, na Itália. Casou-se muito jovem e, segundo a tradição, viveu anos "
             "difíceis ao lado de um marido de temperamento violento, por quem nunca deixou de rezar. Ele mudou de vida, mas foi assassinado numa "
             "briga entre famílias. Pouco depois, Rita perdeu também os dois filhos. Viúva, entrou no mosteiro das agostinianas de Cássia, "
             "onde viveu na oração até morrer, em 22 de maio de 1457. Foi canonizada em 1900. É chamada a santa das causas impossíveis.")
RITA_INTRO = ("Nesta novena, você entrega a Santa Rita o seu casamento e o seu pedido. Reze nove dias seguidos: leia a história do dia, "
              "a oração, e termine com um Pai-Nosso, uma Ave-Maria e um Glória. Santa Rita não faz milagres sozinha: ela leva o seu pedido a Deus, "
              "que sabe o que é melhor para você e para a sua família.")
RITA = [
    ("A menina que rezava",
     "A tradição conta que os pais de Rita, já de idade, a criaram na fé, e que desde pequena ela gostava de rezar. Toda caminhada com Deus começa "
     "assim: com um coração que conversa com Ele. Hoje, comece a novena com calma, sem pressa.",
     "Santa Rita, que desde menina conversáveis com Deus, ensinai-me a rezar com confiança. Coloco nas vossas mãos o meu casamento com {CONJ} "
     "e tudo o que levo no coração. Ajudai-me a começar esta novena com fé. Amém."),
    ("O casamento difícil",
     "Ainda muito jovem, Rita se casou. A tradição conta que o marido tinha um temperamento violento, e que ela não deixou de rezar por ele um só dia. "
     "A paciência de Santa Rita não é um convite para aceitar violência: é o exemplo de quem não deixou a fé morrer no meio da dificuldade.",
     "Santa Rita, vós sabeis o que é um casamento difícil. Olhai para o meu casamento com {CONJ}, com tudo o que ele tem de bonito e de difícil. "
     "Pedi a Deus por nós: que onde houver dureza venha a ternura, e onde houver distância venha a aproximação. Amém."),
    ("A mansidão",
     "Rita aprendeu que gritar não resolve. A mansidão não é fraqueza: é a força de quem não deixa a raiva mandar. Hoje, peça a graça de uma "
     "palavra calma no momento em que a vontade for de responder com raiva.",
     "Santa Rita, mulher mansa e forte, ensinai-me a responder com calma. Que eu não alimente a briga e não guarde rancor. Pedi a Deus que a paz "
     "volte a morar na minha casa e no coração de {CONJ}. Amém."),
    ("O perdão",
     "A tradição conta que, depois que o marido foi assassinado, Rita perdoou os assassinos e rezou para que os filhos não buscassem vingança. "
     "Perdoar é uma das coisas mais difíceis que existem, e uma das mais libertadoras.",
     "Santa Rita, que perdoastes o que parecia imperdoável, ajudai-me a perdoar o que me feriu no meu casamento, e a pedir perdão pelo que eu errei. "
     "Pedi a Deus que cure as feridas entre mim e {CONJ}. Amém."),
    ("A mãe que confia",
     "Rita teve dois filhos e temia que eles se perdessem no ódio depois da morte do pai. Os dois morreram ainda jovens, de doença. Ela entregou a Deus "
     "o que não podia controlar. Hoje, entregue a Deus as pessoas da sua família que mais preocupam você.",
     "Santa Rita, mãe que confiou em Deus na dor, eu vos entrego a minha família, cada pessoa pelo nome. Pedi a Deus que nos proteja e nos mantenha "
     "unidos. Amém."),
    ("Recomeçar",
     "Viúva e sozinha, Rita pediu para entrar no mosteiro das agostinianas de Cássia. A tradição conta que foi recusada mais de uma vez, até ser aceita. "
     "Ela não desistiu. Há fases do casamento que pedem um recomeço.",
     "Santa Rita, que não desististes diante das portas fechadas, pedi a Deus por mim e por {CONJ} a graça de recomeçar: um novo jeito de conversar, "
     "de cuidar e de rezar juntos. Amém."),
    ("O espinho",
     "Já religiosa, Rita pedia para participar das dores de Jesus. A tradição conta que recebeu na testa a ferida de um espinho, que carregou por "
     "muitos anos. Unir as nossas dores às de Jesus dá sentido até ao sofrimento que não conseguimos evitar.",
     "Santa Rita, que unistes as vossas dores às de Jesus, ajudai-me a entregar a Ele o que hoje me faz sofrer no meu casamento. Que nenhuma dor "
     "me afaste de Deus. Amém."),
    ("A rosa no inverno",
     "Perto de morrer, Rita pediu a uma parente uma rosa do jardim da casa onde nasceu. Era inverno, e a tradição conta que a parente encontrou uma "
     "rosa aberta. Por isso Santa Rita é lembrada com rosas: sinal de que Deus pode fazer florescer o que parecia morto.",
     "Santa Rita, das rosas, pedi a Deus que faça florescer de novo o amor, a paciência e a alegria no meu casamento com {CONJ}, do jeito e no "
     "tempo Dele. Amém."),
    ("A santa das causas impossíveis",
     "Rita morreu em 22 de maio de 1457 e foi canonizada em 1900. Até hoje, muita gente pede a sua intercessão nas causas que parecem não ter saída. "
     "Hoje, entregue o seu pedido por inteiro, com confiança.",
     "Santa Rita de Cássia, santa das causas impossíveis, apresentai a Deus o meu pedido: {PEDIDO}. Eu confio que Ele me ouve e sabe o que é melhor "
     "para mim, para {CONJ} e para a nossa família. Amém."),
]
