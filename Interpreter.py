from Lexer import lexer
from Parser import parse_program

# Diccionario para rastrear las variables y sus valores
variables = {}


def evaluate(nodes):
    last_result = None  # Variable para almacenar el valor del último nodo visitado

    for node in nodes:
        result = evaluate_single(node)
        if result is not None:
            last_result = result

    return last_result


def evaluate_single(node):
    if isinstance(node, list):
        results = []
        for child in node:
            result = evaluate_single(child)
            if result is not None:
                results.append(result)
        return results

    if node.type == "NUMBER":
        return node.value
    if node.type == "PLUS":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left + right
    if node.type == "MINUS":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left - right
    if node.type == "TIMES":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left * right
    if node.type == "DIVIDE":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left / right
    if node.type == "NOTEQUAL":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left != right
    if node.type == "LESSTHAN":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left < right
    if node.type == "GREATERTHAN":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left > right
    if node.type == "EQUALS":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left == right
    if node.type == "VIAJE":
        variable_name = node.children[0].children[1].value
        initial_value = node.children[0].children[2].value  # El valor inicial es un nodo
        final_value = node.children[1].value
        step = node.children[2].value
        body = node.children[3]  # El cuerpo del bucle

        # Lista para almacenar los resultados de las iteraciones
        results = []

        for i in range(initial_value, final_value + 1, step):
            # Agregar la variable de control al diccionario de variables
            variables[variable_name] = i
            result = evaluate_single(body)
            results.append(result)

        return results  # Devolver la lista de resultados de las iteraciones

    elif node.type == "DRACARYS":
        if node.children:
            dracarys_content = evaluate_single(node.children[0])
            return dracarys_content
        elif node.value:  # Manejar el caso donde DRACARYS es una variable
            return evaluate_single(node.value)
    if node.type == "LOBOS":
        string_content = node.value
        if string_content and (
            string_content[0] == string_content[-1]
            and (string_content[0] == '"' or string_content[0] == "'")
        ):
            return string_content[1:-1]
        else:
            return string_content
    if node.type == "NORTE":
        condition = evaluate_single(node.children[0])
        if condition:
            return evaluate_single(node.children[1])
        elif len(node.children) == 3:
            return evaluate_single(node.children[2])
    if node.type == "VARIABLE_DECLARATION":
        # Si es una declaración de variable, almacena el valor en el diccionario
        if (
            len(node.children) == 4
            and node.children[0].type == "TYPE"
            and node.children[2].type == "ASSIGN"
        ):
            variable_name = node.children[1].value
            variable_value = evaluate_single(node.children[3])
            variables[variable_name] = variable_value
            return f"{variable_name} = {variable_value}"
    if node.type == "VARIABLE":
        variable_name = node.value
        if variable_name in variables:
            return variables[variable_name]
    return None


# Código de prueba
program = """
lobos a ='hola'

"""
tokens = lexer(program)
ast = parse_program(tokens)
results = evaluate(ast)  # Ahora devuelve una lista de resultados
for result in results:
    print(result)
