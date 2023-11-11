import re

# Lista de tokens
tokens = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('ENDIF', r'(?i)endif'),
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
    ('NORTE', r'norte'),
    ('NORTE', r'NORTE'),
    ('ELSE', r'else'),
    ('VIAJE', r'VIAJE'),
    ('VIAJE', r'viaje'),
    ('STEP', r'step'),
    ('STEP', r'STEP'),
    ('TO', r'to'),
    ('TYPE', r'espada|float|lobos|bool'),
    ('VARIABLE', r'[a-zA-Z_][a-zA-Z0-9_]*'),  
    ('EQUALS', r'=='),
    ('ASSIGN', r'='),
    ('WHITESPACE', r'\s+'),
    ('NOTEQUAL', r'!='),
    ('LESSTHAN', r'<'),
    ('GREATERTHAN', r'>'),
    ('LESSEQUAL', r'<='),
    ('GREATEQUAL', r'>=')
   
    
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
