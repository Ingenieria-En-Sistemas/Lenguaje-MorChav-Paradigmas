# Importa el lexer (debe estar definido previamente)
from Lexer import lexer


# Nodos para operadores lógicos



# Clase Node para construir el árbol de sintaxis abstracta (AST)
class Node:
    LOGICAL_OPERATORS = {"AND", "OR", "NOT"}
    def __init__(self, type, children=None, value=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.value = value


# Diccionario para rastrear las variables y sus valores
variables = {}


def parse_program(tokens):
    statements = []
    while tokens:
        if tokens[0].type == "TYPE":
            # Si el token actual es una declaración de variable, procesarla como tal
            variable_declaration = parse_variable_declaration(tokens)
            statements.append(variable_declaration)
        elif tokens[0].type == "VIAJE":
            # Si el token actual es un bucle VIAJE, procesarlo como tal
            for_statement = parse_for_statement(tokens)
            statements.append(for_statement)
        elif tokens[0].type == "WHILE":
            # Verifica si solo quedan 2 tokens y el siguiente token es "ENDWHILE"
            if len(tokens) == 2 and tokens[1].type == "ENDWHILE":
                return parse_while_statement(tokens)
            else:
                # Si no es el caso, procesa el bucle WHILE normalmente
                while_statement = parse_while_statement(tokens)
                statements.append(while_statement)
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
    elif tokens[0].type == "SUR":
        return parse_else_statement(tokens)
    elif tokens[0].type == "DRACARYS":
        return parse_dracarys(tokens)
    elif tokens[0].type == "LBRACE":
        return parse_block(tokens)
    elif tokens[0].type == "RBRACE":
        return parse_while_block(tokens)
    elif tokens[0].type == "VIAJE":
        return parse_for_statement(tokens)
    if tokens[0].type == "WHILE":
        return parse_while_statement(tokens)
    elif tokens[0].type == "TYPE":  # Identifica las declaraciones de variables
        return parse_variable_declaration(tokens)
    elif tokens[0].type == "RAVEN":
        return input_statement(tokens)
    return expression(tokens)


# Función para el símbolo no terminal "sentencia_while"
def parse_while_statement(tokens):
    tokens.pop(0)  # Consume 'WHILE'
    condition = expression(tokens)

    # Verifica si hay una apertura de llave '{'
    if tokens[0].type == "LBRACE":
        tokens.pop(0)  # Consume '{'

        # Obtiene el cuerpo del bucle usando la nueva función parse_while_block
        body = parse_while_block(tokens)

        # Verifica si hay un cierre de llave '}'
        if tokens[0].type == "ENDWHILE":
            tokens.pop(0)  # Consume 'endwhile'
            return Node("WHILE", [condition, body])
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba '}' después del cuerpo del bucle WHILE."
            )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '{' al comienzo del cuerpo del bucle WHILE."
        )


def parse_boolean(tokens):
    if tokens[0].type == "TRUE" or tokens[0].type == "FALSE":
        return Node("BOOLEAN", value=(tokens.pop(0).type == "TRUE"))
    raise SyntaxError(
        f"Error de sintaxis: Token inesperado '{tokens[0].type}' en parse_boolean."
    )


def parse_variable_declaration(tokens):
    var_type = tokens.pop(
        0
    ).value  # Tipo de variable (espada, string, bool, float, char, etc.)
    variable_name = tokens.pop(0).value  # Nombre de la variable
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)  # Consume '='

        if var_type == "espada":
            if tokens[0].type == "NUMBER":
                value = expression(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba un número entero como valor para 'espada'."
                )
        elif var_type == "lobos":
            if tokens[0].type == "STRING":
                value = expression(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba una cadena entre comillas como valor para 'LOBOS'."
                )
        elif var_type == "bool":
            if tokens[0].type == "TRUE" or tokens[0].type == "FALSE":
                value = parse_boolean(tokens)
            else:
                raise SyntaxError(
                    f"Error de sintaxis: Se esperaba 'TRUE' o 'FALSE' como valor para 'bool '{variable_name}'."
                )
        elif var_type == "float":
            if (
                tokens[0].type == "NUMBER" or tokens[0].type == "FLOAT"
            ):  # Permitir números y decimales
                value = expression(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba un número o decimal como valor para 'float'."
                )
        elif var_type == "char":
            if tokens[0].type == "STRING" and len(tokens[0].value) == 1:
                value = expression(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba un carácter entre comillas como valor para 'char'."
                )
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


"""
def parse_variable_declaration(tokens):
    var_type = tokens.pop(0).value  # Tipo de variable (espada, string, etc.)
    variable_name = tokens.pop(0).value  # Nombre de la variable

    if tokens[0].type == "ASSIGN":
        tokens.pop(0)  # Consume '='

        # Verifica si la inicialización es una lista
        if tokens[0].type == "LBRACE":
            tokens.pop(0)  # Consume '{'

            # Parsea la lista de enteros
            list_values = []
            while tokens[0].type != "RBRACE":
                if tokens[0].type == "NUMBER":
                    list_values.append(int(tokens.pop(0).value))
                elif tokens[0].type == "COMMA":
                    tokens.pop(0)  # Consume ','
                else:
                    raise SyntaxError("Error de sintaxis: Lista mal formada.")

            # Consume '}'
            tokens.pop(0)

            # Asigna la lista a la variable
            variables[variable_name] = Node("LIST", value=list_values)

            return Node(
                "VARIABLE_DECLARATION",
                children=[
                    Node("TYPE", value=var_type),
                    Node("VARIABLE", value=variable_name),
                    Node("ASSIGN"),
                    Node("LIST", value=list_values),
                ],
            )
        else:
            # Si no es una lista, parsea la expresión normalmente
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
"""


def parse_variable_assignment(tokens):
    variable_name = tokens.pop(0).value
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)  # Consume '='
        value = expression(tokens)
        variables[variable_name] = value
        return Node(
            "VARIABLE_ASSIGNMENT",
            children=[
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


def parse_for_statement(tokens):
    tokens.pop(0)  # Consume 'VIAJE'
    if tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume '('

        # Parsea la declaración de la variable y la inicialización
        if tokens[0].type == "TYPE":
            var_type = tokens.pop(0).value  # Tipo de variable (int, string, etc.)
            variable = tokens.pop(0).value  # Nombre de la variable
            initial_value = None  # Inicialmente, no hay valor asignado

            if tokens[0].type == "ASSIGN":
                tokens.pop(0)  # Consume '='
                initial_value = expression(tokens)  # Parsea la expresión inicial
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba '=' en la definición del bucle VIAJE."
                )

            # Verifica la palabra clave 'TO'
            if tokens[0].type == "TO":
                tokens.pop(0)  # Consume 'TO'

                # Parsea la expresión final y el paso si está presente
                final_value = expression(tokens)
                step = None
                if tokens[0].type == "STEP":
                    tokens.pop(0)  # Consume 'STEP'
                    step = expression(tokens)

                # Verifica la existencia de un paréntesis derecho ')'
                if tokens[0].type == "RPAREN":
                    tokens.pop(0)  # Consume ')'

                    # Parsea el cuerpo del bucle
                    body = parse_single_statement(tokens)

                    # Crea el nodo 'VIAJE' utilizando la clase 'Node'
                    return Node(
                        "VIAJE",
                        children=[
                            Node(
                                "VARIABLE_DECLARATION",
                                children=[
                                    Node("TYPE", value=var_type),
                                    Node("VARIABLE", value=variable),
                                    initial_value,
                                ],
                            ),
                            Node("FINAL_VALUE", value=final_value.value),
                            Node("STEP", value=step.value if step else None),
                            body,
                        ],
                    )
                else:
                    raise SyntaxError(
                        "Error de sintaxis: Se esperaba ')' al final del bucle VIAJE."
                    )
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba 'TO' en la definición del bucle VIAJE."
                )
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba el tipo de variable en la definición del bucle VIAJE."
            )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '(' en la definición del bucle VIAJE."
        )


def parse_if_statement(tokens):
    tokens.pop(0)  # Consume 'NORTE'
    condition = expression(tokens)
    if_statement = parse_single_statement(tokens)
    else_statement = None  # Inicialmente, no hay un 'ELSE' statement

    # Comprueba si hay 'ELSE'
    if tokens and tokens[0].type == "SUR":
        tokens.pop(0)  # Consume 'ELSE'
        else_statement = parse_single_statement(tokens)

    # Busca 'ENDIF' sin importar los espacios en blanco
    if tokens and tokens[0].type == "ENDNORTE":
        tokens.pop(0)  # Consume 'ENDIF'
        return Node("NORTE", [condition, if_statement, else_statement])

    raise SyntaxError(
        "Error de sintaxis: Se esperaba 'ENDNORTE' al final de la declaración condicional."
    )


def input_statement(tokens):
    tokens.pop(0)  # Consume 'RAVEN'

    # Asegúrate de que haya un paréntesis izquierdo después de 'RAVEN'
    if tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume '('

        # Busca el nombre de la variable después del paréntesis izquierdo
        if tokens[0].type == "VARIABLE":
            variable_name = tokens.pop(0).value  # Obtiene el nombre de la variable

            # Verifica si la variable ya ha sido declarada
            if variable_name not in variables:
                raise NameError(
                    f"Error: La variable '{variable_name}' no está declarada."
                )

            # Asegúrate de que haya un paréntesis derecho después del nombre de la variable
            if tokens[0].type == "RPAREN":
                tokens.pop(0)  # Consume ')'

                # Crea nodos para representar la estructura deseada
                input_node = Node("RAVEN")
                variable_assignment_node = Node("VARIABLE_ASSIGNMENT")
                variable_node = Node("VARIABLE", value=variable_name)
                assign_node = Node("ASSIGN")
                user_input_node = Node("USERINPUT")

                # Construye la estructura del árbol
                input_node.children = [
                    variable_assignment_node,
                    variable_node,
                    assign_node,
                    user_input_node,
                ]

                return input_node
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba ')' después del nombre de la variable en la declaración RAVEN."
                )
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba el nombre de la variable después del paréntesis izquierdo en la declaración RAVEN."
            )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '(' después de la declaración RAVEN."
        )


def check_variable_type(variable_name, user_input):
    # Verifica si la variable ya ha sido declarada
    if variable_name in variables:
        # Obtiene el tipo de la variable
        variable_type = variables[variable_name].type

        # Verifica si el tipo del valor ingresado es compatible con la variable
        if (
            (variable_type == "LOBOS" and not user_input.isdigit())
            or (variable_type == "NUMBER" and user_input.isdigit())
            or (variable_type == "bool" and user_input.lower() in ("true", "false"))
        ):
            # Si llegamos aquí, el tipo es correcto
            return True

    # Si no es compatible, genera un error
    raise TypeError(
        f"Error: El tipo de '{user_input}' no es compatible con la variable '{variable_name}'."
    )


def parse_else_statement(tokens):
    tokens.pop(0)  # Consume 'ELSE'
    else_statement = parse_single_statement(tokens)
    return Node("SUR", [else_statement])


# Actualiza la función expression para incluir operadores lógicos
def expression(tokens):
    left = logical_or(tokens)
    return left

def logical_or(tokens):
    left = logical_and(tokens)
    while tokens and tokens[0].type == "OR":
        op = tokens.pop(0)
        right = logical_and(tokens)
        left = Node(op.type, [left, right])
    return left

def logical_and(tokens):
    left = equality(tokens)
    while tokens and tokens[0].type == "AND":
        op = tokens.pop(0)
        right = equality(tokens)
        left = Node(op.type, [left, right])
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
    elif tokens[0].type == "TRUE" or tokens[0].type == "FALSE":
        return parse_boolean(tokens)
    elif tokens[0].type == "LPAREN":
        tokens.pop(0)  # Consume el paréntesis izquierdo
        if tokens[0].type == "NORTE":
            # Manejar una expresión condicional (if)
            condition = expression(tokens)
            if tokens[0].type == "RPAREN":
                tokens.pop(0)  # Consume el paréntesis derecho
                # Manejar las ramas "THEN" y "SUR" si fuera necesario
                then_expression = factor(tokens)
                if tokens[0].type == "SUR":
                    tokens.pop(0)  # Consume 'SUR'
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
        return Node("LOBOS", value=tokens.pop(0).value)
    elif tokens[0].type == "VARIABLE":
        if tokens[1].type == "ASSIGN":
            return parse_variable_assignment(tokens)
        else:
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
            if result_node.children[0].value in variables:
                return result_node
            else:
                return result_node
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba ')' después de la expresión."
            )
    elif tokens[0].type == "STRING":
        string_node = tokens.pop(0).value
        return Node("DRACARYS", value=string_node)
    elif tokens[0].type == "VARIABLE":
        variable_node = tokens.pop(0).value
        return Node("DRACARYS", value=variable_node)
    elif tokens[0].type == "NUMBER":
        number_node = tokens.pop(0).value
        return Node("DRACARYS", value=number_node)
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


def parse_while_block(tokens):
    statements = []

    while tokens and tokens[0].type != "RBRACE":
        statement = parse_single_statement(tokens)
        statements.append(statement)

    if tokens and tokens[0].type == "RBRACE":
        tokens.pop(0)  # Consume '}'
    else:
        raise SyntaxError("Error de sintaxis: Falta '}' al final del bloque WHILE.")

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
entrada_ejemplo = """ 

bool a = false

NORTE(2==2 and 3==3){
a = true
	dracarys(a)
}SUR{
	dracarys(a)
}ENDNORTE


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
