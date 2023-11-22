from Lexer import lexer
from Parser import parse_program

# Diccionario para rastrear las variables y sus valores
variables = {}


def evaluate(nodes):
    all_results = []  # Almacena todos los resultados de la ejecución
    for node in nodes:
        result = evaluate_single(node)
        if result is not None:
            all_results.append(result)  # Extiende la lista de resultados

    return all_results


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
    if node.type == "BOOLEAN":
        return node.value
    if node.type == "LIST":
        return node.value
    if node.type == "NOT":
        operand = evaluate_single(node.children[0])
        return not operand
    if node.type == "AND":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left and right
    if node.type == "OR":
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left or right
    if node.type == "CHAR":
        return node.value
    if node.type == "FLOAT":
        return node.value
    if node.type == "USERINPUT":
        user_input = input("RAVEN: ")
        return user_input
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
    if node.type == "WHILE":
        condition = node.children[0]
        body = node.children[1]

        results = []

        while evaluate_single(condition):
            result = evaluate_single(body)
            results.extend(result)

        return results

    if node.type == "VIAJE":
        variable_name = node.children[0].children[1].value
        initial_value = node.children[0].children[2].value
        final_value = node.children[1].value
        step = node.children[2].value
        body = node.children[3]

        results = []

        for i in range(initial_value, final_value + 1, step):
            variables[variable_name] = i
            result = evaluate_single(body)
            results.append(result)

        return results
    elif node.type == "DRACARYS":
        if node.children:
            dracarys_content = evaluate_single(node.children[0])
            # Check if the content is a list and there is an index
            if isinstance(dracarys_content, list) and len(node.children) > 1:
                index = evaluate_single(node.children[1])
                # Check if the index is valid
                if isinstance(index, int) and 0 <= index < len(dracarys_content):
                    return dracarys_content[index]
                else:
                    print(f"Error: Index {index} out of range.")
            else:
                return dracarys_content
        elif node.value:
            return evaluate_single(node.value)
    if node.type == "LOBOS":
        string_content = node.value
        if string_content and (
            string_content[0] == string_content[-1]
            and (string_content[0] == '"' or string_content[0] == "'")
        ):
            return [string_content[1:-1]]
        else:
            return [string_content]
    if node.type == "NORTE":
        condition = evaluate_single(node.children[0])
        if condition:
            return evaluate_single(node.children[1])
        elif len(node.children) == 3:
            return evaluate_single(node.children[2])
    if node.type == "VARIABLE_DECLARATION":
        if (
            len(node.children) == 4
            and node.children[0].type == "TYPE"
            and node.children[2].type == "ASSIGN"
        ):
            variable_name = node.children[1].value
            variable_value = evaluate_single(node.children[3])
            variables[variable_name] = variable_value
    if node.type == "VARIABLE":
        variable_name = node.value
        if variable_name in variables:
            return variables[variable_name]
    if node.type == "VARIABLE_ASSIGNMENT":
        variable_name = node.children[0].value
        variable_value = evaluate_single(node.children[2])
        variables[variable_name] = variable_value
    
    if node.type == "FUNC_DECLARATION":
        function_name = node.children[0].value
        function_params = [param.value for param in node.children[1:]]
        function_body = node.children[-1]

        # Crear una función lambda que representa la función declarada
        variables[function_name] = lambda *args: evaluate_single_function(function_body, function_params, args)
        return None
    if node.type == "FUNC_CALL":
        function_name = node.children[0].value
        args = [evaluate_single(arg) for arg in node.children[1:]]
        if function_name in variables and callable(variables[function_name]):
            return variables[function_name](*args)
    if node.type == "RAVEN":
        variable_name = node.children[1].value
        user_input = evaluate_single(node.children[3])
        variables[variable_name] = user_input
    if node.type == "VARIABLE_DECLARATION":
        if (
            len(node.children) == 4
            and node.children[0].type == "TYPE"
            and node.children[2].type == "ASSIGN"
        ):
            variable_name = node.children[1].value

            if node.children[0].value.endswith("[]"):
                array_values = [
                    evaluate_single(value) for value in node.children[3].children
                ]
                variables[variable_name] = array_values
            else:
                variable_value = evaluate_single(node.children[3])
                variables[variable_name] = variable_value
    return None

def evaluate_single_function(body, params, args):
    # Crear un diccionario para mapear parámetros con sus valores
    param_dict = {params[i]: args[i] for i in range(len(params))}

    # Asignar los valores de los parámetros en el contexto de la función
    for key, value in param_dict.items():
        variables[key] = value

    # Evaluar el cuerpo de la función
    result = None
    for statement in body:
        result = evaluate_single(statement)

    # Limpiar el contexto de los parámetros después de la llamada a la función
    for key in param_dict.keys():
        del variables[key]

    return result


program = """

void espada sumar(espada x, espada y) {
    dracarys(x + y)
}

espada a = 5
espada b = 10

sumar (a, b)

"""
tokens = lexer(program)
ast = parse_program(tokens)

# Ahora, ejecuta el intérprete línea por línea y muestra el resultado
for line_node in ast:
    line_result = evaluate_single(line_node)
    if line_result is not None:
        print(line_result)
