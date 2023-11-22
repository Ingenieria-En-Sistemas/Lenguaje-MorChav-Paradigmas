from Lexer import lexer

class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.value = value

variables = {}

def parse_program(tokens):
    statements = []
    while tokens:
        if tokens[0].type == "TYPE":
            variable_declaration = parse_variable_declaration(tokens)
            statements.append(variable_declaration)
        elif tokens[0].type == "VIAJE":
            for_statement = parse_for_statement(tokens)
            statements.append(for_statement)
        elif tokens[0].type == "CAMINO":
            if len(tokens) == 2 and tokens[1].type == "ENDCAMINO":
                return parse_while_statement(tokens)
            else:
                while_statement = parse_while_statement(tokens)
                statements.append(while_statement)
        elif tokens[0].type == "NORTE":
            if_statement = parse_if_statement(tokens)
            statements.append(if_statement)
        else:
            statement = parse_single_statement(tokens)
            statements.append(statement)
    return statements

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
    if tokens[0].type == "CAMINO":
        return parse_while_statement(tokens)
    elif tokens[0].type == "TYPE":
        return parse_variable_declaration(tokens)
    elif tokens[0].type == "RAVEN":
        return input_statement(tokens)
    return expression(tokens)

def parse_while_statement(tokens):
    tokens.pop(0)
    condition = expression(tokens)

    if tokens[0].type == "LBRACE":
        tokens.pop(0)

        body = parse_while_block(tokens)

        if tokens[0].type == "ENDCAMINO":
            tokens.pop(0)
            return Node("CAMINO", [condition, body])
        else:
            raise SyntaxError(
                "Error de sintaxis: Se esperaba '}' después del cuerpo del bucle CAMINO."
            )
    else:
        raise SyntaxError(
            "Error de sintaxis: Se esperaba '{' al comienzo del cuerpo del bucle CAMINO."
        )


def parse_boolean(tokens):
    if tokens[0].type == "TRUE" or tokens[0].type == "FALSE":
        return Node("BOOLEAN", value=(tokens.pop(0).type == "TRUE"))
    raise SyntaxError(
        f"Error de sintaxis: Token inesperado '{tokens[0].type}' en parse_boolean."
    )


def parse_variable_declaration(tokens):
    var_type = tokens.pop(0).value
    variable_name = tokens.pop(0).value
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)

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
        elif var_type == "lealtad":
            if tokens[0].type == "TRUE" or tokens[0].type == "FALSE":
                value = parse_boolean(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba 'TRUE' o 'FALSE' como valor para 'lealtad'."
                )
        elif var_type == "float":
            if tokens[0].type == "NUMBER" or tokens[0].type == "FLOAT":
                value = expression(tokens)
            else:
                raise SyntaxError(
                    "Error de sintaxis: Se esperaba un número o decimal como valor para 'float'."
                )
        elif var_type == "char":
            if (
                tokens[0].type == "STRING"
                and len(tokens[0].value) == 1
            ):
                value = expression(tokens)
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un carácter entre comillas como valor para 'char'.")
        else:
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
        raise SyntaxError("Error de sintaxis: Se esperaba '=' después del nombre de la variable.")



def parse_variable_assignment(tokens):
    variable_name = tokens.pop(0).value
    if tokens[0].type == "ASSIGN":
        tokens.pop(0)
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
        raise SyntaxError("Error de sintaxis: Se esperaba '=' después del nombre de la variable.")


def parse_variable_reference(tokens):
    variable_name = tokens.pop(0).value
    if variable_name in variables:
        return variables[variable_name]
    else:
        raise NameError(f"La variable '{variable_name}' no está definida.")


def parse_for_statement(tokens):
    tokens.pop(0)
    if tokens[0].type == "LPAREN":
        tokens.pop(0)

        if tokens[0].type == "TYPE":
            var_type = tokens.pop(0).value
            variable = tokens.pop(0).value
            initial_value = None

            if tokens[0].type == "ASSIGN":
                tokens.pop(0)
                initial_value = expression(tokens)
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '=' en la definición del bucle VIAJE.")

            if tokens[0].type == "TO":
                tokens.pop(0)
                final_value = expression(tokens)
                step = None
                if tokens[0].type == "KILL":
                    tokens.pop(0)
                    step = expression(tokens)

                if tokens[0].type == "RPAREN":
                    tokens.pop(0)
                    body = parse_single_statement(tokens)
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
                            Node("KILL", value=step.value if step else None),
                            body,
                        ],
                    )
                else:
                    raise SyntaxError("Error de sintaxis: Se esperaba ')' al final del bucle VIAJE.")
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba 'TO' en la definición del bucle VIAJE.")
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba el tipo de variable en la definición del bucle VIAJE.")
    else:
        raise SyntaxError("Error de sintaxis: Se esperaba '(' en la definición del bucle VIAJE.")


def parse_if_statement(tokens):
    tokens.pop(0)
    condition = expression(tokens)
    if_statement = parse_single_statement(tokens)
    else_statement = None

    if tokens and tokens[0].type == "SUR":
        tokens.pop(0)
        else_statement = parse_single_statement(tokens)

    if tokens and tokens[0].type == "ENDNORTE":
        tokens.pop(0)
        return Node("NORTE", [condition, if_statement, else_statement])

    raise SyntaxError("Error de sintaxis: Se esperaba 'ENDNORTE' al final de la declaración condicional.")


def input_statement(tokens):
    tokens.pop(0)
    if tokens[0].type == "LPAREN":
        tokens.pop(0)
        if tokens[0].type == "VARIABLE":
            variable_name = tokens.pop(0).value
            if variable_name not in variables:
                raise NameError(f"Error: La variable '{variable_name}' no está declarada.")
            if tokens[0].type == "RPAREN":
                tokens.pop(0)
                input_node = Node("RAVEN")
                variable_assignment_node = Node("VARIABLE_ASSIGNMENT")
                variable_node = Node("VARIABLE", value=variable_name)
                assign_node = Node("ASSIGN")
                user_input_node = Node("USERINPUT")

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
    if variable_name in variables:
        variable_type = variables[variable_name].type

        if (
            (variable_type == "LOBOS" and not user_input.isdigit())
            or (variable_type == "NUMBER" and user_input.isdigit())
            or (variable_type == "lealtad" and user_input.lower() in ("true", "false"))
        ):
            return True

    raise TypeError(
        f"Error: El tipo de '{user_input}' no es compatible con la variable '{variable_name}'."
    )





def parse_else_statement(tokens):
    tokens.pop(0)
    else_statement = parse_single_statement(tokens)
    return Node("SUR", [else_statement])


def expression(tokens):
    left = equality(tokens)
    return left


def equality(tokens):
    left = comparison(tokens)
    while tokens and tokens[0].type in ("EQUALS", "NOTEQUAL"):
        op = tokens.pop(0)
        right = comparison(tokens)
        left = Node(op.type, [left, right])
    return left


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
        tokens.pop(0)
        if tokens[0].type == "NORTE":
            condition = expression(tokens)
            if tokens[0].type == "RPAREN":
                tokens.pop(0)
                then_expression = factor(tokens)
                if tokens[0].type == "SUR":
                    tokens.pop(0)
                    else_expression = factor(tokens)
                    return Node("NORTE", children=[condition, then_expression, else_expression])
                return Node("NORTE", children=[condition, then_expression])
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba ')' después de la condición en la expresión condicional.")
        else:
            expr = expression(tokens)
            if tokens[0].type == "RPAREN":
                tokens.pop(0)
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
    raise SyntaxError(f"Error de sintaxis: Token inesperado '{tokens[0].type}' en factor.")

def parse_dracarys(tokens):
    tokens.pop(0)
    if tokens[0].type == "LPAREN":
        tokens.pop(0)
        expression_node = expression(tokens)
        if tokens[0].type == "RPAREN":
            tokens.pop(0)
            result_node = Node("DRACARYS", children=[expression_node])
            if result_node.children[0].value in variables:
                return result_node
            else:
                return result_node
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba ')' después de la expresión.")
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
        raise SyntaxError("Error de sintaxis: Se esperaba '(' o una cadena después de 'DRACARYS'.")

def parse_block(tokens):
    tokens.pop(0)
    statements = []

    while tokens and tokens[0].type != "RBRACE":
        statement = parse_single_statement(tokens)
        statements.append(statement)

    if tokens and tokens[0].type == "RBRACE":
        tokens.pop(0)
    else:
        raise SyntaxError("Error de sintaxis: Falta '}' al final del bloque.")
    return statements

def parse_while_block(tokens):
    statements = []

    while tokens and tokens[0].type != "RBRACE":
        statement = parse_single_statement(tokens)
        statements.append(statement)

    if tokens and tokens[0].type == "RBRACE":
        tokens.pop(0)
    else:
        raise SyntaxError("Error de sintaxis: Falta '}' al final del bloque CAMINO.")

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

entrada_ejemplo = """ 
lealtad a = true
NORTE(a){
	dracarys("Verdadero")
}SUR{
	dracarys("Falso")
}ENDNORTE
"""
tokens_ejemplo = lexer(entrada_ejemplo)
if tokens_ejemplo:
    print("Tokens generados correctamente:")
    for token in tokens_ejemplo:
        print(f"Tipo: {token.type}, Valor: {token.value}")
else:
    print("Error de sintaxis en la entrada de ejemplo.")
ast = parse_program(tokens_ejemplo)
if ast:
    print("\nÁrbol de sintaxis abstracta (AST):")
    for node in ast:
        print_ast(node)