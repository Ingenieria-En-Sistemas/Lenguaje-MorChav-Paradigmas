# Importa el lexer y el parser (deben estar definidos previamente)
from Lexer import lexer
from Parser import parse

# Función para evaluar el AST
def evaluate(nodes):
    results = []

    for node in nodes:
        result = evaluate_single(node)
        results.append(result)

    return results

def evaluate_single(node):
    if node.type == 'NUMBER':
        return node.value
    if node.type == 'PLUS':
        return evaluate_single(node.children[0]) + evaluate_single(node.children[1])
    if node.type == 'MINUS':
        return evaluate_single(node.children[0]) - evaluate_single(node.children[1])
    if node.type == 'TIMES':
        return evaluate_single(node.children[0]) * evaluate_single(node.children[1])
    if node.type == 'DIVIDE':
        return evaluate_single(node.children[0]) / evaluate_single(node.children[1])
    if node.type == 'VALAR':
        print(node.value)  # Imprimir el valor de cadena
    return None

# Prueba del intérprete
while True:
    input_expr = input("Ingrese una expresión aritmética (o 'exit' para salir): ")
    if input_expr == 'exit':
        break
    input_expr = input_expr.strip()  # Elimina espacios en blanco al inicio y al final
    if not input_expr.endswith(";"):
        print("Error de sintaxis: Se esperaba un punto y coma al final de la instrucción.")
        continue
    tokens = lexer(input_expr)
    ast = parse(tokens)
    if ast:
        result = evaluate(ast)
        print(f"Resultado: {result[0]}")
    else:
        print("Error de sintaxis. Intente nuevamente.")