import re

# Lista de tokens
tokens = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('DRACARYS', r'dracarys'),
    ('DRACARYS', r'DRACARYS'),
    ('STRING', r'\'[^\']*\'|"[^"]*"'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('WHITESPACE', r'\s+'),
    ('EQUALS', r'=='),
    ('NOTEQUAL', r'!='),
    ('LESSTHAN', r'<'),
    ('GREATERTHAN', r'>'),
    ('LESSEQUAL', r'<='),
    ('GREATEQUAL', r'>='),
    ('ASSIGN', r'='),
    ('ENDIF', r'(?i)endif'),
    ('TRUE', r'True'),
    ('FALSE', r'False'),
]

# Clase Token para almacenar información sobre cada token
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

# Función lexer que divide la entrada en tokens
def lexer(input_string):
    token_list = []
    input_string = input_string.replace('\n', '')  # Elimina saltos de línea
    pos = 0

    while pos < len(input_string):
        match = None
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(input_string, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':  # Ignorar espacios en blanco
                    token_list.append(Token(token_type, value))
                pos = match.end()
                break

        if not match:
            print(f"Token no reconocido: {input_string[pos]}")
            return None

    return token_list
