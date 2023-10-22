# Importa el lexer (debe estar definido previamente)
from Lexer import lexer

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
        raise SyntaxError("Error de sintaxis: Se esperaba un punto y coma al final de la instrucción.")

# Función para el símbolo no terminal "sentencia"
def parse(tokens):
    statements = []

    while tokens:
        statement = parse_single_statement(tokens)
        statements.append(statement)

        if tokens:
            if tokens[0].type == 'SEMICOLON':
                tokens.pop(0)  # Consume el punto y coma
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un punto y coma al final de la instrucción.")

    return statements

def parse_single_statement(tokens):
    if tokens[0].type == 'VALAR':
        tokens.pop(0)  # Consume 'VALAR'
        if tokens[0].type == 'LPAREN':
            tokens.pop(0)  # Consume '('
            if tokens[0].type == 'STRING':
                value = tokens.pop(0).value[1:-1]  # Elimina comillas dobles del valor de cadena
                if tokens[0].type == 'RPAREN':
                    tokens.pop(0)  # Consume ')'
                    return Node('VALAR', value=value)
                else:
                    raise SyntaxError("Error de sintaxis: Se esperaba ')' después del valor de cadena.")
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un valor de cadena después de '('.")
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba '(' después de 'VALAR'.")

    # Si no es una sentencia 'valar', se asume que es una expresión
    return expression(tokens)

def p_statement_valar(p):
    'statement : VALAR LPAREN STRING RPAREN'
    print(p[3][1:-1])
