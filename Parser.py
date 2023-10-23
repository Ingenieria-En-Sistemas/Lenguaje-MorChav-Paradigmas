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
    if tokens[0].type == 'TRUE':
        tokens.pop(0)  # Consume 'TRUE'
        return True
    elif tokens[0].type == 'FALSE':
        tokens.pop(0)  # Consume 'FALSE'
        return False
    elif tokens[0].type == 'NUMBER':
        return int(tokens.pop(0).value)
    elif tokens[0].type == 'LPAREN':
        tokens.pop(0)  # Consume el paréntesis izquierdo
        expr = condition(tokens)
        if tokens[0].type == 'RPAREN':
            tokens.pop(0)  # Consume el paréntesis derecho
        return expr

# Función para el símbolo no terminal "igualdad"
def equality(tokens):
    left = comparison(tokens)

    while tokens and tokens[0].type in ('EQUALS', 'NOTEQUAL'):
        op = tokens.pop(0)
        right = comparison(tokens)
        left = Node(op.type, [left, right])

    return left

# Función para el símbolo no terminal "comparación"
def comparison(tokens):
    left = addition(tokens)

    while tokens and tokens[0].type in ('LESSTHAN', 'GREATERTHAN', 'LESSEQUAL', 'GREATEQUAL'):
        op = tokens.pop(0)
        right = addition(tokens)
        left = Node(op.type, [left, right])

    return left

# Función para el símbolo no terminal "suma"
def addition(tokens):
    left = multiplication(tokens)

    while tokens and tokens[0].type in ('PLUS', 'MINUS'):
        op = tokens.pop(0)
        right = multiplication(tokens)
        left = Node(op.type, [left, right])

    return left

# Función para el símbolo no terminal "término"
def multiplication(tokens):
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
    elif tokens[0].type == 'DRACARYS':
        return parse_dracarys(tokens)

    raise SyntaxError(f"Error de sintaxis: Token inesperado '{tokens[0].type}' en factor.")

# Función para el símbolo no terminal "DRACARYS"
def parse_dracarys(tokens):
    tokens.pop(0)  # Consume 'DRACARYS'
    if tokens[0].type == 'LPAREN':
        tokens.pop(0)  # Consume '('
        if tokens[0].type == 'STRING':
            value = tokens.pop(0).value[1:-1]  # Elimina comillas del valor de cadena
            if tokens[0].type == 'RPAREN':
                tokens.pop(0)  # Consume ')'
                return Node('DRACARYS', value=value)
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba ')' después del valor de cadena.")
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba un valor de cadena después de '('.")
    else:
        raise SyntaxError("Error de sintaxis: Se esperaba '(' después de 'DRACARYS'.")

# Función para el símbolo no terminal "bloque"
def parse_block(tokens):
    tokens.pop(0)  # Consume '{'
    statements = []

    while tokens and tokens[0].type != 'RBRACE':
        statement = parse_single_statement(tokens)
        statements.append(statement)

    if tokens and tokens[0].type == 'RBRACE':
        tokens.pop(0)  # Consume '}'
    else:
        raise SyntaxError("Error de sintaxis: Falta '}' al final del bloque.")

    return statements

# Función para el símbolo no terminal "programa"
def parse_program(tokens):
    statements = []

    while tokens:
        statement = parse_single_statement(tokens)
        statements.append(statement)

    return statements

# Función para el símbolo no terminal "condición"
# Función para el símbolo no terminal "condición"
def condition(tokens):
    left = expression(tokens)

    if tokens and tokens[0].type in ('EQUALS', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUAL', 'GREATEQUAL'):
        op = tokens.pop(0)
        right = expression(tokens)

        if op.type == 'EQUALS':
            return left == right
        elif op.type == 'NOTEQUAL':
            return left != right
        elif op.type == 'LESSTHAN':
            return left < right
        elif op.type == 'GREATERTHAN':
            return left > right
        elif op.type == 'LESSEQUAL':
            return left <= right
        elif op.type == 'GREATEQUAL':
            return left >= right

    return left


# Función para el símbolo no terminal "expresión"


# Función para el símbolo no terminal "sentencia"
def parse_single_statement(tokens):
    if tokens[0].type == 'IF':
        return parse_if_statement(tokens)
    elif tokens[0].type == 'ELSE':
        return parse_else_statement(tokens)
    elif tokens[0].type == 'DRACARYS':
        return parse_dracarys(tokens)
    elif tokens[0].type == 'LBRACE':
        return parse_block(tokens)
    return expression(tokens)


def parse_if_statement(tokens):
    tokens.pop(0)  # Consume 'IF'
    condition_value = condition(tokens)
    true_branch = parse_single_statement(tokens)
    false_branch = None

    # Comprueba si hay 'ELSE'
    if tokens and tokens[0].type == 'ELSE':
        tokens.pop(0)  # Consume 'ELSE'
        false_branch = parse_single_statement(tokens)

    # Busca 'ENDIF' sin importar los espacios en blanco
    if tokens and tokens[0].type == 'ENDIF':
        tokens.pop(0)  # Consume 'ENDIF'
        if condition_value:
            return true_branch
        else:
            if false_branch:
                return false_branch

    raise SyntaxError("Error de sintaxis: Se esperaba 'ENDIF' al final de la declaración condicional.")


def parse_else_statement(tokens):
    tokens.pop(0)  # Consume 'ELSE'
    else_statement = parse_single_statement(tokens)
    return Node('ELSE', [else_statement])

# Función para imprimir el árbol de forma recursiva
def print_ast(node, level=0):
    if isinstance(node, list):
        for item in node:
            print_ast(item, level)
    else:
        if node is None:
            return
        print("  " * level + node.type + (f" ({node.value})" if node.value else ""))
        for child in node.children:
            print_ast(child, level + 1)


# Ejemplo de entrada
entrada_ejemplo = "if (3==3) {dracarys('Verdad')} else {dracarys('Falso')} endif"

# Llama al lexer con el ejemplo de entrada
tokens_ejemplo = lexer(entrada_ejemplo)

# Verifica si el lexer generó tokens correctamente
if tokens_ejemplo:
    print("Tokens generados correctamente:")
    for token in tokens_ejemplo:
        print(f"Tipo: {token.type}, Valor: {token.value}")
else:
    print("Error de sintaxis en la entrada de ejemplo.")

# Llama al parser con los tokens generados
ast = parse_program(tokens_ejemplo)

# Verifica si el parser generó el AST correctamente
if ast:
    print("\nÁrbol de sintaxis abstracta (AST):")
    for node in ast:
        print_ast(node)
