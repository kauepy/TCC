from pyboard.parser.parser import NoAtribuicao, NoChamada, NoWhile


def gerar_comando(no):
    if isinstance(no, NoAtribuicao):
        if isinstance(no.valor, NoChamada) and no.valor.nome == "Led":
            pino = no.valor.argumentos[0]
            return f"pinMode({pino}, OUTPUT);"
        return f"// TODO: atribuicao nao suportada ainda: {no}"

    return f"// TODO: comando nao suportado ainda: {no}"

def gerar_programa(programa):
    linhas = []
    pinos = {}  # nome da variável -> número do pino

    for no in programa:
        linhas.extend(gerar_comando(no, pinos))

    return linhas


def gerar_comando(no, pinos):
    if isinstance(no, NoAtribuicao):
        if isinstance(no.valor, NoChamada) and no.valor.nome == "Led":
            pino = no.valor.argumentos[0]
            pinos[no.nome_variavel] = pino
            return [f"pinMode({pino}, OUTPUT);"]
        return [f"// TODO: atribuicao nao suportada ainda: {no}"]

    if isinstance(no, NoChamada):
        if no.objeto and no.nome in ("on", "off"):
            pino = pinos[no.objeto]
            estado = "HIGH" if no.nome == "on" else "LOW"
            return [f"digitalWrite({pino}, {estado});"]
        if no.nome == "wait":
            tempo = no.argumentos[0]
            return [f"delay({tempo});"]
        return [f"// TODO: chamada nao suportada ainda: {no}"]

    if isinstance(no, NoWhile):
        linhas = ["while (true) {"]
        for comando in no.corpo:
            for linha in gerar_comando(comando, pinos):
                linhas.append("    " + linha)
        linhas.append("}")
        return linhas

    return [f"// TODO: comando nao suportado ainda: {no}"]

def gerar_ino(programa):
    pinos = {}
    linhas_setup = []
    linhas_loop = []

    for no in programa:
        if isinstance(no, NoAtribuicao):
            linhas_setup.extend(gerar_comando(no, pinos))
        elif isinstance(no, NoWhile):
            for comando in no.corpo:
                linhas_loop.extend(gerar_comando(comando, pinos))
        else:
            linhas_loop.extend(gerar_comando(no, pinos))

    ino = ["void setup() {"]
    for linha in linhas_setup:
        ino.append("    " + linha)
    ino.append("}")
    ino.append("")
    ino.append("void loop() {")
    for linha in linhas_loop:
        ino.append("    " + linha)
    ino.append("}")

    return "\n".join(ino)

from pyboard.parser.lexer import tokenizar_arquivo
from pyboard.parser.ast_builder import construir_ast

codigo = """led = Led(13)

while True:
    led.on()
    wait(1000)
    led.off()
    wait(1000)
"""

tokens = tokenizar_arquivo(codigo)
programa = construir_ast(tokens)

print(gerar_ino(programa))