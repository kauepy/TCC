from pyboard.parser.parser import (
    parsear_chamada,
    parsear_atribuicao,
    parsear_while,
)


def construir_ast(tokens):
    programa = []
    pos = 0

    while pos < len(tokens):
        token_atual = tokens[pos]

        if token_atual.tipo == "NEWLINE":
            pos += 1
            continue

        if token_atual.tipo == "PALAVRA_CHAVE" and token_atual.valor == "while":
            no, pos = parsear_while(tokens, pos)
            programa.append(no)

        elif token_atual.tipo == "IDENTIFICADOR":
            # decide entre atribuição (led = ...) e chamada solta (wait(...))
            proximo = tokens[pos + 1]
            if proximo.tipo == "IGUAL":
                no, pos = parsear_atribuicao(tokens, pos)
            else:
                no, pos = parsear_chamada(tokens, pos)
                pos += 1  # pula o NEWLINE que vem depois
            programa.append(no)

        else:
            pos += 1  # ignora por enquanto (ex: DEDENT sobrando no nível raiz)

    return programa

from pyboard.parser.lexer import tokenizar_arquivo

codigo = """led = Led(13)

while True:
    led.on()
    wait(1000)
    led.off()
    wait(1000)
"""

tokens = tokenizar_arquivo(codigo)
programa = construir_ast(tokens)

for comando in programa:
    print(comando)

