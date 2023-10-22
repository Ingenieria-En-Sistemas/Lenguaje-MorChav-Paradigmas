# Importa el lexer (debe estar definido previamente)
from lexer import lexer

# Lista de tokens generados por el lexer
tokens = lexer("3+4*10-20")

# Clase Node para construir el árbol de sintaxis abstracta (AST)
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.value = value

# Función para el símbolo no terminal "expresión"
def expression(tokens):
    # Inicialmente, asumimos que la expresión es un término
    left = term(tokens)

    while tokens and tokens[0].type in ('PLUS', 'MINUS'):
        op = tokens.pop(0)
        right = term(tokens)
        left = Node(op.type, [left, right])

    return left

# Función para el símbolo no terminal "término"
def term(tokens):
    left = factor(tokens)

    while tokens and tokens[0].type in ('TIMES', 'DIVIDE'):
        op = tokens.pop(0)
        right = factor(tokens)
        left = Node(op.type, [left, right])

    return left

# Función para el símbolo no terminal "factor"
def factor(tokens):
    if tokens[0].type == 'NUMBER':
        return Node('NUMBER', value=int(tokens.pop(0).value))
    elif tokens[0].type == 'LPAREN':
        tokens.pop(0)  # Consume el paréntesis izquierdo
        expr = expression(tokens)
        if tokens[0].type == 'RPAREN':
            tokens.pop(0)  # Consume el paréntesis derecho
        return expr
    else:
        raise SyntaxError("Error de sintaxis")

# Función principal para el parser
def parse(tokens):
    ast = expression(tokens)
    if tokens:
        raise SyntaxError("Error de sintaxis")
    return ast

# Prueba del parser
ast = parse(tokens)
print(ast)
