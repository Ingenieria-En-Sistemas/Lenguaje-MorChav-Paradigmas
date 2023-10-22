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

# Prueba del intérprete
input_expr = "3 + 5 * (2 - 1)"
tokens = lexer(input_expr)
ast = parse(tokens)
result = evaluate(ast)
print(f"Resultado: {result}")
