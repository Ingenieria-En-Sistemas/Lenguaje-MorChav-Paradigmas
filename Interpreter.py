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
        # Consulta el primer hijo del nodo 'DRACARYS'
        if node.children and len(node.children) > 0:
            dracarys_content = evaluate_single(node.children[0])
            return dracarys_content
        else:
            return None  # Maneja el caso en el que no hay hijos
    if node.type == 'STRING':
        # Procesa el contenido del nodo 'STRING'
        string_content = node.value
        if string_content and (string_content[0] == string_content[-1] and (string_content[0] == '"' or string_content[0] == "'")):
            return string_content[1:-1]  # Quita las comillas iniciales y finales
        else:
            return string_content  # Devuelve el contenido sin comillas si no están presentes
    if node.type == 'IF':
        condition = evaluate_single(node.children[0])
        if condition:
            return evaluate_single(node.children[1])
        elif len(node.children) == 3:
            return evaluate_single(node.children[2])
    return None


