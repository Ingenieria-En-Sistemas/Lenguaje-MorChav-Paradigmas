# Importa el lexer y el parser (deben estar definidos previamente)
from Lexer import lexer
from Parser import parse_program

# Función para evaluar el AST
def evaluate(nodes):
    results = []

    for node in nodes:
        result = evaluate_single(node)
        results.append(result)

    return results

def evaluate_single(node):
    if isinstance(node, list):
        results = []
        for child in node:
            result = evaluate_single(child)
            if result is not None:
                results.append(result)
        return results

    if node.type == 'NUMBER':
        return node.value
    if node.type == 'PLUS':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left + right
    if node.type == 'MINUS':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left - right
    if node.type == 'TIMES':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left * right
    if node.type == 'DIVIDE':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left / right
    if node.type == 'DRACARYS':
        return node.value
    if node.type == 'IF':
        condition = evaluate_single(node.children[0])
        if condition:
            return evaluate_single(node.children[1])
        elif len(node.children) == 3:
            return evaluate_single(node.children[2])
    return None


# Prueba del intérprete
while True:
    input_expr = input("Ingrese una expresión condicional (o 'exit' para salir): ")
    if input_expr == 'exit':
        break
    input_expr = input_expr.strip()  # Elimina espacios en blanco al inicio y al final
    tokens = lexer(input_expr)
    ast = parse_program(tokens)
    if ast:
        result = evaluate(ast)
        if result is not None:
            # El resultado puede ser una lista de resultados, imprime cada uno
            for res in result:
                print(f"Resultado: {res}")
    else:
        print("Error de sintaxis. Intente nuevamente.")
