from pyboard.parser.lexer import tokenizar, tokenizar_arquivo


class NoChamada:
    def __init__(self, nome, argumentos, objeto=None):
        self.nome = nome
        self.argumentos = argumentos
        self.objeto = objeto  # None = função solta (wait); senão, é o dono do método (led)

    def __repr__(self):
        if self.objeto:
            return f"Chamada({self.objeto}.{self.nome}, {self.argumentos})"
        return f"Chamada({self.nome}, {self.argumentos})"


def parsear_chamada(tokens, pos):
    objeto = None
    nome = tokens[pos].valor
    pos += 1

    if tokens[pos].tipo == "PONTO":
        pos += 1  # consome o PONTO
        objeto = nome
        nome = tokens[pos].valor
        pos += 1

    assert tokens[pos].tipo == "PAREN_ESQ"
    pos += 1

    argumentos = []
    while tokens[pos].tipo != "PAREN_DIR":
        argumentos.append(tokens[pos].valor)
        pos += 1

    pos += 1  # consome o PAREN_DIR

    return NoChamada(nome, argumentos, objeto), pos


class NoAtribuicao:
    def __init__(self, nome_variavel, valor):
        self.nome_variavel = nome_variavel
        self.valor = valor  # geralmente um NoChamada, ex: Led(13)

    def __repr__(self):
        return f"Atribuicao({self.nome_variavel}, {self.valor})"


def parsear_atribuicao(tokens, pos):
    nome_variavel = tokens[pos].valor
    pos += 1

    assert tokens[pos].tipo == "IGUAL"
    pos += 1

    valor, pos = parsear_chamada(tokens, pos)

    return NoAtribuicao(nome_variavel, valor), pos


class NoWhile:
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo  # lista de comandos dentro do while

    def __repr__(self):
        return f"While({self.condicao}, {self.corpo})"


def parsear_while(tokens, pos):
    assert tokens[pos].tipo == "PALAVRA_CHAVE" and tokens[pos].valor == "while"
    pos += 1

    condicao = tokens[pos].valor  # por enquanto só pega o valor bruto (ex: True)
    pos += 1

    assert tokens[pos].tipo == "DOIS_PONTOS"
    pos += 1

    assert tokens[pos].tipo == "NEWLINE"
    pos += 1

    assert tokens[pos].tipo == "INDENT"
    pos += 1

    corpo = []
    while tokens[pos].tipo != "DEDENT":
        if tokens[pos].tipo == "NEWLINE":
            pos += 1
            continue
        no, pos = parsear_chamada(tokens, pos)
        pos += 1  # pula o NEWLINE que vem depois da chamada
        corpo.append(no)

    pos += 1  # consome o DEDENT

    return NoWhile(condicao, corpo), pos


tokens = tokenizar("led = Led(13)")
no, pos = parsear_atribuicao(tokens, 0)
print(no)

tokens = tokenizar("led.on()")
no, pos = parsear_chamada(tokens, 0)
print(no)

codigo = """while True:
    wait(1000)
    wait(1000)
"""

tokens = tokenizar_arquivo(codigo)
no, pos = parsear_while(tokens, 0)
print(no)