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


class ForNode:
    def __init__(self, variable, initial_value, final_value, step, body):
        self.type = "FOR"
        self.variable = variable
        self.initial_value = initial_value
        self.final_value = final_value
        self.step = step
        self.body = body


# Diccionario para rastrear las variables y sus valores
variables = {}


# Función para el símbolo no terminal "programa"
# Función para el símbolo no terminal "programa"
def parse_program(tokens):
    statements = []
    while tokens:
        if tokens[0].type == "TYPE":
            # Si el token actual es una declaración de variable, procesarla como tal
            variable_declaration = parse_variable_declaration(tokens)
            statements.append(variable_declaration)
        elif tokens[0].type == "FOR":
            # Si el token actual es un bucle FOR, procesarlo como tal
            for_statement = parse_for_statement(tokens)
            statements.append(for_statement)
        elif tokens[0].type == "IF":
            # Si el token actual es una expresión condicional (if), procesarlo como tal
            if_statement = parse_if_statement(tokens)
            statements.append(if_statement)
        else:
            # De lo contrario, procesar la sentencia como una expresión
            statement = parse_single_statement(tokens)
            statements.append(statement)
    return statements


# Función para el símbolo no terminal "sentencia"
def parse_single_statement(tokens):
    if tokens[0].type == "IF":
        return parse_if_statement(tokens)
    elif tokens[0].type == "ELSE":
        return parse_else_statement(tokens)
    elif tokens[0].type == "DRACARYS":
        return parse_dracarys(tokens)
    elif tokens[0].type == "LBRACE":
        return parse_block(tokens)
    elif tokens[0].type == "FOR":
        return parse_for_statement(tokens)
    elif tokens[0].type == "TYPE":  # Identifica las declaraciones de variables
        return parse_variable_declaration(tokens)
    return expression(tokens)


# Función para analizar la declaración de una variable
def parse_variable_declaration(tokens):
    var_type = tokens.pop(0).value  # Tipo de variable (int, string, etc.)
    variable_name = tokens.pop(0).value  # Nombre de la variable
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)  # Consume '='
        value = expression(tokens)
        variables[variable_name] = value
        return Node(
            "VARIABLE_DECLARATION",
            children=[
                Node("TYPE", value=var_type),
                Node("VARIABLE", value=variable_name),
                Node("ASSIGN"),
                value,
            ],
        )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '=' después del nombre de la variable."
        )


# Función para analizar una referencia a una variable
def parse_variable_reference(tokens):
    variable_name = tokens.pop(0).value
    if variable_name in variables:
        return variables[variable_name]
    else:
        raise NameError(f"La variable '{variable_name}' no está definida.")


# Función para analizar un bucle FOR
def parse_for_statement(tokens):
    tokens.pop(0)  # Consume 'FOR'
    if tokens[0].type == "LPAREN":  # Corrige el token esperado
        tokens.pop(0)  # Consume '('
        variable = tokens.pop(0)
        if variable.type == "VARIABLE":
            if tokens[0].type == "ASSIGN":
                tokens.pop(0)  # Consume '='
                initial_value = expression(tokens)
                if tokens[0].type == "TO":
                    tokens.pop(0)  # Consume 'TO'
                    final_value = expression(tokens)
                    step = 1  # Valor por defecto para el paso
                    if tokens and tokens[0].type == "STEP":
                        tokens.pop(0)  # Consume 'STEP'
                        step = int(
                            tokens.pop(0).value
                        )  # Convierte el valor del token en un número entero
                    if tokens[0].type == "RPAREN":
                        tokens.pop(0)  # Consume ')'  # Corrige el token esperado
                        body = parse_single_statement(tokens)
                        return ForNode(
                            variable.value, initial_value, final_value, step, body
                        )
                    else:
                        raise SyntaxError(
                            "Error de sintaxis: Se esperaba ')' al final del bucle FOR."
                        )
                else:
                    raise SyntaxError(
                        "Error de sintaxis: Se esperaba 'TO' en la definición del bucle FOR."
                    )
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba '=' en la definición del bucle FOR."
                )
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba un nombre de variable en la definición del bucle FOR."
            )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '(' en la definición del bucle FOR."
        )


def parse_if_statement(tokens):
    tokens.pop(0)  # Consume 'IF'
    condition = expression(tokens)
    if_statement = parse_single_statement(tokens)
    else_statement = None  # Inicialmente, no hay un 'ELSE' statement

    # Comprueba si hay 'ELSE'
    if tokens and tokens[0].type == "ELSE":
        tokens.pop(0)  # Consume 'ELSE'
        else_statement = parse_single_statement(tokens)

    # Busca 'ENDIF' sin importar los espacios en blanco
    if tokens and tokens[0].type == "ENDIF":
        tokens.pop(0)  # Consume 'ENDIF'
        return Node("IF", [condition, if_statement, else_statement])

    raise SyntaxError(
        "Error de sintaxis: Se esperaba 'ENDIF' al final de la declaración condicional."
    )


def parse_else_statement(tokens):
    tokens.pop(0)  # Consume 'ELSE'
    else_statement = parse_single_statement(tokens)
    return Node("ELSE", [else_statement])


# Función para el símbolo no terminal "expresión"
def expression(tokens):
    left = equality(tokens)
    return left


# Función para el símbolo no terminal "igualdad"
def equality(tokens):
    left = comparison(tokens)
    while tokens and tokens[0].type in ("EQUALS", "NOTEQUAL"):
        op = tokens.pop(0)
        right = comparison(tokens)
        left = Node(op.type, [left, right])
    return left


# Función para el símbolo no terminal "comparación"
def comparison(tokens):
    left = addition(tokens)
    while tokens and tokens[0].type in (
        "LESSTHAN",
        "GREATERTHAN",
        "LESSEQUAL",
        "GREATEQUAL",
    ):
        op = tokens.pop(0)
        right = addition(tokens)
        left = Node(op.type, [left, right])
    return left


# Función para el símbolo no terminal "suma"
def addition(tokens):
    left = multiplication(tokens)
    while tokens and tokens[0].type in ("PLUS", "MINUS"):
        op = tokens.pop(0)
        right = multiplication(tokens)
        if op.type == "PLUS":
            left = Node("PLUS", [left, right])
        else:
            left = Node("MINUS", [left, right])
    return left


# Función para el símbolo no terminal "término"
def multiplication(tokens):
    left = factor(tokens)
    while tokens and tokens[0].type in ("TIMES", "DIVIDE"):
        op = tokens.pop(0)
        right = factor(tokens)
        left = Node(op.type, [left, right])
    return left


def factor(tokens):
    if tokens[0].type == "NUMBER":
        return Node("NUMBER", value=int(tokens.pop(0).value))
    elif tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume el paréntesis izquierdo
        if tokens[0].type == "IF":
            # Manejar una expresión condicional (if)
            condition = expression(tokens)
            if tokens[0].type == "RPAREN":
                tokens.pop(0)  # Consume el paréntesis derecho
                # Manejar las ramas "THEN" y "ELSE" si fuera necesario
                then_expression = factor(tokens)
                if tokens[0].type == "ELSE":
                    tokens.pop(0)  # Consume 'ELSE'
                    else_expression = factor(tokens)
                    return Node(
                        "IF", children=[condition, then_expression, else_expression]
                    )
                return Node("IF", children=[condition, then_expression])
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba ')' después de la condición en la expresión condicional."
                )
        else:
            expr = expression(tokens)
            if tokens[0].type == "RPAREN":
                tokens.pop(0)  # Consume el paréntesis derecho
            return expr
    elif tokens[0].type == "DRACARYS":
        return parse_dracarys(tokens)
    elif tokens[0].type == "STRING":
        return Node("STRING", value=tokens.pop(0).value)
    elif tokens[0].type == "VARIABLE":
        return Node("VARIABLE", value=tokens.pop(0).value)
    raise SyntaxError(
        f"Error de sintaxis: Token inesperado '{tokens[0].type}' en factor."
    )


def parse_dracarys(tokens):
    tokens.pop(0)  # Consume 'DRACARYS'
    if tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume '('
        expression_node = expression(tokens)
        if tokens[0].type == "RPAREN":
            tokens.pop(0)  # Consume ')'
            result_node = Node("DRACARYS", children=[expression_node])
            return result_node
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba ')' después de la expresión."
            )
    elif tokens[0].type == "STRING":
        string_node = tokens.pop(0).value
        return Node("DRACARYS", value=string_node)
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '(' o una cadena después de 'DRACARYS'."
        )


# Función para el símbolo no terminal "bloque"
def parse_block(tokens):
    tokens.pop(0)  # Consume '{'
    statements = []

    while tokens and tokens[0].type != "RBRACE":
        statement = parse_single_statement(tokens)
        statements.append(statement)

    if tokens and tokens[0].type == "RBRACE":
        tokens.pop(0)  # Consume '}'
    else:
        raise SyntaxError("Error de sintaxis: Falta '}' al final del bloque.")

    return statements


def print_ast(node, level=0):
    if isinstance(node, list):
        for item in node:
            print_ast(item, level)
    else:
        if node is None:
            return
        if isinstance(node, ForNode):
            print("  " * level + node.type)
            print("  " * (level + 1) + f"Variable: {node.variable}")
            print("  " * (level + 1) + f"Initial Value: {node.initial_value.value}")
            print("  " * (level + 1) + f"Final Value: {node.final_value.value}")
            print("  " * (level + 1) + f"Step: {node.step}")
            print("  " * (level + 1) + "Body:")
            if isinstance(node.body, list):
                for child in node.body:
                    print_ast(
                        child, level + 2
                    )  # Imprime los elementos del cuerpo del bucle FOR
            else:
                print_ast(node.body, level + 2)  # Imprime el cuerpo del bucle FOR
        else:
            print("  " * level + node.type + (f" ({node.value})" if node.value else ""))
        if hasattr(node, "children"):
            for child in node.children:
                print_ast(child, level + 1)


# Ejemplo de entrada con un bucle FOR
entrada_ejemplo = """int a = 2
int b = 3
dracarys(a + b)"""

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
