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
        elif tokens[0].type == "NORTE":
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
    if tokens[0].type == "NORTE":
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


def parse_variable_declaration(tokens):
    var_type = tokens.pop(0).value  # Tipo de variable (espada, string, etc.)
    variable_name = tokens.pop(0).value  # Nombre de la variable
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)  # Consume '='
        if var_type == 'espada':
            if tokens[0].type == "NUMBER":
                value = expression(tokens)
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un número entero como valor para 'espada'.")
        elif var_type == 'string':
            if tokens[0].type == "STRING":
                value = expression(tokens)
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba una cadena entre comillas como valor para 'string'.")
        elif var_type == 'bool':
            # Agrega la lógica para bool aquí si es necesario
            pass
        else:
            # Agrega la lógica para otros tipos aquí si es necesario
            pass

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


# ...

def parse_for_statement(tokens):
    tokens.pop(0)  # Consume 'FOR'
    if tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume '('
        if tokens[0].type == "TYPE":
            var_type = tokens.pop(0).value  # Tipo de variable (int, string, etc.)
            variable = tokens.pop(0).value  # Nombre de la variable
            initial_value = None  # Inicialmente, no hay valor asignado

            if tokens[0].type == "ASSIGN":
                tokens.pop(0)  # Consume '='
                if tokens[0].type == "NUMBER":
                    initial_value = expression(tokens)  
                else:
                    raise SyntaxError("Error de sintaxis: Se esperaba un número como valor inicial en la definición del bucle FOR.")

                if tokens[0].type == "TO":
                    tokens.pop(0)  # Consume 'TO'
                    final_value = expression(tokens)
                    step = None
                    if tokens[0].type == "STEP":
                        tokens.pop(0)  # Consume 'STEP'
                        step = expression(tokens)
                    if tokens[0].type == "RPAREN":
                        tokens.pop(0)  # Consume ')'
                        body = parse_single_statement(tokens)

                        # Asignar el valor inicial solo si se proporcionó
                        if initial_value:
                            variables[variable] = initial_value.value  # Almacenar el valor numérico

                        # Crear un nodo 'FOR' utilizando la clase 'Node'
                        return Node(
                            "FOR",
                            children=[
                                Node("VARIABLE_DECLARATION", children=[
                                    Node("TYPE", value=var_type),
                                    Node("VARIABLE", value=variable),
                                    initial_value,  # Agregar el valor inicial directamente
                                ]),
                                Node("FINAL_VALUE", value=final_value.value),
                                Node("STEP", value=step.value if step else None),
                                body
                            ]
                        )
                    else:
                        raise SyntaxError("Error de sintaxis: Se esperaba ')' al final del bucle FOR.")
                else:
                    raise SyntaxError("Error de sintaxis: Se esperaba 'TO' en la definición del bucle FOR.")
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '=' en la definición del bucle FOR.")
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba el tipo de variable en la definición del bucle FOR.")
    else:
        raise SyntaxError("Error de sintaxis: Se esperaba '(' en la definición del bucle FOR.")





def parse_if_statement(tokens):
    tokens.pop(0)  # Consume 'NORTE'
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
        return Node("NORTE", [condition, if_statement, else_statement])

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
        if tokens[0].type == "NORTE":
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
                        "NORTE", children=[condition, then_expression, else_expression]
                    )
                return Node("NORTE", children=[condition, then_expression])
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
    if isinstance(node, Node):
        print("  " * level + node.type + (f" ({node.value})" if node.value else ""))
        if hasattr(node, "children"):
            for child in node.children:
                print_ast(child, level + 1)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, level)
    else:
        print("  " * level + str(node))



# Ejemplo de entrada con un bucle FOR
entrada_ejemplo = """for (espada i = 1 to 10 step 3) dracarys(2 + i)
"""

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
