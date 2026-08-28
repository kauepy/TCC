PALAVRAS_CHAVE = {"while", "if", "else", "for", "True", "False"}


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r})"


def tokenizar(codigo):
    tokens = []
    i = 0

    while i < len(codigo):
        char = codigo[i]

        if char == "(":
            tokens.append(Token("PAREN_ESQ", "("))
            i += 1

        elif char == ")":
            tokens.append(Token("PAREN_DIR", ")"))
            i += 1

        elif char == ".":
            tokens.append(Token("PONTO", "."))
            i += 1
        elif char == "=":
            tokens.append(Token("IGUAL", "="))
            i += 1
        elif char == ":":
            tokens.append(Token("DOIS_PONTOS", ":"))
            i += 1
        elif char in (" ", "\t", "\n"):
            i += 1
        
        elif char.isdigit():
            numero = ""
            while i < len(codigo) and codigo[i].isdigit():
                numero += codigo[i]
                i += 1
            tokens.append(Token("NUMERO", int(numero)))

        elif char.isalpha() or char == "_":
            palavra = ""
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == "_"):
                palavra += codigo[i]
                i += 1

            if palavra in PALAVRAS_CHAVE:
                tokens.append(Token("PALAVRA_CHAVE", palavra))
            else:
                tokens.append(Token("IDENTIFICADOR", palavra))
        else:
            i += 1  # por enquanto, ignora qualquer outro caractere

    return tokens

def medir_indentacao(linha):
    coluna = 0
    for char in linha:
        if char == " ":
            coluna += 1
        elif char == "\t":
            coluna += 8 - (coluna % 8)  # avança até a próxima coluna múltipla de 8
        else:
            break
    return coluna


def tokenizar_arquivo(codigo):
    tokens = []
    pilha_indentacao = [0]  # nível 0 = sem indentação nenhuma

    for numero_linha, linha in enumerate(codigo.split("\n"), start=1):
        conteudo = linha.strip()

        if conteudo == "":
            continue  # ignora linhas em branco

        nivel = medir_indentacao(linha)

        if nivel > pilha_indentacao[-1]:
            pilha_indentacao.append(nivel)
            tokens.append(Token("INDENT", nivel))
        elif nivel < pilha_indentacao[-1]:
            while pilha_indentacao and nivel < pilha_indentacao[-1]:
                pilha_indentacao.pop()
                tokens.append(Token("DEDENT", nivel))
            if nivel != pilha_indentacao[-1]:
                raise SyntaxError(f"Indentação inconsistente na linha {numero_linha}")

        tokens.extend(tokenizar(conteudo))
        tokens.append(Token("NEWLINE", None))

    return tokens

def tokenizar_arquivo(codigo):
    tokens = []
    pilha_indentacao = [0]

    for numero_linha, linha in enumerate(codigo.split("\n"), start=1):
        conteudo = linha.strip()

        if conteudo == "":
            continue

        nivel = medir_indentacao(linha)

        if nivel > pilha_indentacao[-1]:
            pilha_indentacao.append(nivel)
            tokens.append(Token("INDENT", nivel))
        elif nivel < pilha_indentacao[-1]:
            while pilha_indentacao and nivel < pilha_indentacao[-1]:
                pilha_indentacao.pop()
                tokens.append(Token("DEDENT", nivel))
            if nivel != pilha_indentacao[-1]:
                raise SyntaxError(f"Indentação inconsistente na linha {numero_linha}")

        tokens.extend(tokenizar(conteudo))
        tokens.append(Token("NEWLINE", None))

    while len(pilha_indentacao) > 1:
        pilha_indentacao.pop()
        tokens.append(Token("DEDENT", pilha_indentacao[-1]))

    return tokens

codigo = """led = Led(13)

while True:
    led.on()
    wait(1000)
    led.off()
    wait(1000)
"""

for token in tokenizar_arquivo(codigo):
    print(token)

class NoWhile:
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo  # lista de comandos dentro do while

    def __repr__(self):
        return f"While({self.condicao}, {self.corpo})"

