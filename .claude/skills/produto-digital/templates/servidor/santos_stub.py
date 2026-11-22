"""Imitação mínima do santos.py da VPS, só para os testes locais (a tabela real tem os 366 dias)."""
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
TABELA = {(13, 6): ("Santo Antônio", "Presbítero franciscano e Doutor da Igreja", "franciscano"),
          (19, 3): ("São José", "Esposo da Virgem Maria", "esposo"),
          (26, 7): ("São Joaquim e Sant'Ana", "Pais da Virgem Maria", "familia"),
          (25, 12): ("Natal do Senhor", "Solenidade do Nascimento de Jesus", "senhor"),
          (5, 3): ("São João José da Cruz", "Religioso franciscano", "franciscano")}
INTENCOES = ("familia", "saude", "trabalho", "paz", "gratidao")
MOMENTOS = ("dificil", "tranquilo", "mudanca")


def santo_do_dia(dia, mes):
    nome, quem, cat = TABELA.get((int(dia), int(mes)), ("Santa Teresa de Ávila", "Virgem e Doutora da Igreja", "carmelita"))
    return {"nome": nome, "quem": quem, "data": f"{int(dia)} de {MESES[int(mes) - 1]}", "cat": cat}


def validar_data(dia, mes):
    import datetime as dt
    dt.date(2000, int(mes), int(dia))
    return int(dia), int(mes)
