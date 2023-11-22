from Lexer import lexer
from Parser import parse_program


variables = {}



def evaluate(nodes):
    all_results = []
    for node in nodes:
        result = evaluate_single(node)
        if result is not None:
            all_results.append(result)

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
    if node.type == "CAMINO":
        condition = node.children[0]
        body = node.children[1]

        results = []

        while evaluate_single(condition):
            result = evaluate_single(body)
            results.extend(result)

        return results

    if node.type == "VIAJE":
        variable_name = node.children[0].children[1].value
        initial_value = (
            node.children[0].children[2].value
        )
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
    if node.type == "RAVEN":
        variable_name = node.children[1].value
        user_input = evaluate_single(node.children[3])
        variables[variable_name] = user_input
    return None


program = """
lealtad a = false

NORTE(2==2){
a = true
	dracarys(a)
}SUR{
	dracarys(a)
}ENDNORTE

"""
tokens = lexer(program)
ast = parse_program(tokens)

for line_node in ast:
    line_result = evaluate_single(line_node)
    if line_result is not None:
        print(line_result)