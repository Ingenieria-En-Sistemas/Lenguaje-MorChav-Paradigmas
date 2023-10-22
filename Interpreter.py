# Importa el lexer y el parser (deben estar definidos previamente)
from Lexer import lexer
from Parser import parse

# Función para evaluar el AST
def evaluate(node):
    if node.type == 'NUMBER':
        return node.value
    if node.type == 'PLUS':
        return evaluate(node.children[0]) + evaluate(node.children[1])
    if node.type == 'MINUS':
        return evaluate(node.children[0]) - evaluate(node.children[1])
    if node.type == 'TIMES':
        return evaluate(node.children[0]) * evaluate(node.children[1])
    if node.type == 'DIVIDE':
        return evaluate(node.children[0]) / evaluate(node.children[1])
    if node.type == 'VALAR':
        print(node.value)  # Imprimir el valor de cadena
    return None

# Prueba del intérprete
while True:
    input_expr = input("Ingrese una expresión aritmética (o 'exit' para salir): ")
    if input_expr == 'exit':
        break
    tokens = lexer(input_expr)
    ast = parse(tokens)
    if ast:
        result = evaluate(ast)
        print(f"Resultado: {result}")
    else:
        print("Error de sintaxis. Intente nuevamente.")