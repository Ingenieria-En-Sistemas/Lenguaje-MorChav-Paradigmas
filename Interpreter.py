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

import ast

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
    if node.type == 'NOTEQUAL':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left != right
    if node.type == 'LESSTHAN':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left < right
    if node.type == 'GREATERTHAN':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left > right
    if node.type == 'EQUALS':
        left = evaluate_single(node.children[0])
        right = evaluate_single(node.children[1])
        return left == right
    if node.type == 'DRACARYS':
        dracarys_content = node.value
        try:
            # Use ast.literal_eval to evaluate the content of DRACARYS
            result = ast.literal_eval(dracarys_content)
            return result
        except (ValueError, SyntaxError) as e:
            return f"Error: {str(e)}"
    if node.type == 'IF':
        condition = evaluate_single(node.children[0])
        if condition:
            return evaluate_single(node.children[1])
        elif len(node.children) == 3:
            return evaluate_single(node.children[2])
    return None
