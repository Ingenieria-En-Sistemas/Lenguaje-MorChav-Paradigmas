import re

tokens = [
    ("NUMBER", r"\d+"),
    ("PLUS", r"\+"),
    ("ENDNORTE", r"(?i)endnorte"),
    ("MINUS", r"-"),
    ("RAVEN", r"(?i)RAVEN"),
    ("TIMES", r"\*"),
    ("NOT", r"(?i)not"),
    ("AND", r"(?i)and"),
    ("OR", r"(?i)or"),
    ("DIVIDE", r"/"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("DRACARYS", r"(?i)dracarys"),
    ("STRING", r'"[^"]*"'),
    ("NORTE", r"(?i)norte"),
    ("CAMINO", r"(?i)camino"),
    ("TRUE", r"true"),
    ("FALSE", r"false"),
    ("ENDCAMINO", "(?i)endcamino"),
    ("SUR", r"(?i)sur"),
    ("VIAJE", r"(?i)viaje"),
    ("KILL", r"(?i)kill"),
    ("TO", r"(?i)to"),
    ("TYPE", r"espada|float|lobos|lealtad|ejercito"),
    ("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("EQUALS", r"=="),
    ("ASSIGN", r"="),
    ('COMMA', r','),
    ("WHITESPACE", r"\s+"),
    ("NOTEQUAL", r"!="),
    ("LESSTHAN", r"<"),
    ("GREATERTHAN", r">"),
    ("LESSEQUAL", r"<="),
    ("GREATEQUAL", r">="),
]

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

def lexer(input_string):
    token_list = []
    input_string = input_string.replace("\n", "")
    pos = 0

    while pos < len(input_string):
        match = None
        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(input_string, pos)
            if match:
                value = match.group(0)
                if token_type != "WHITESPACE":
                    token_list.append(Token(token_type, value))
                pos = match.end()
                break

        if not match:
            print(f"Token no reconocido: {input_string[pos]}")
            return None

    return token_list
