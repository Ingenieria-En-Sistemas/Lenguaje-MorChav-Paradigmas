# Definir los tipos de tokens y sus patrones
tokens = {
    "NUMBER": r"\d+", # Número entero
    "PLUS": r"\+", # Operador suma
    "MINUS": r"-", # Operador resta
    "LPAREN": r"\(", # Paréntesis izquierdo
    "RPAREN": r"\)", # Paréntesis derecho
}

# Definir una clase para representar los tokens
class Token:
    def __init__(self, type, value, pos):
        self.type = type # Nombre del tipo de token
        self.value = value # Valor del token
        self.pos = pos # Posición del token en la cadena de texto

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.pos})"

# Definir una función para obtener el primer token de una cadena de texto
def get_token(text, pos):
    # Recorrer los tipos de tokens y sus patrones
    for type, pattern in tokens.items():
        # Crear una expresión regular con el patrón
        regex = re.compile(pattern)
        # Buscar el patrón en la cadena de texto desde la posición actual
        match = regex.match(text, pos)
        # Si se encuentra una coincidencia, crear y devolver el token correspondiente
        if match:
            value = match.group()
            return Token(type, value, pos)
    # Si no se encuentra ninguna coincidencia, devolver None o lanzar una excepción
    return None

# Definir una función para obtener todos los tokens de una cadena de texto
def get_tokens(text):
    # Crear una lista vacía para almacenar los tokens
    tokens = []
    # Inicializar la posición actual en 0
    pos = 0
    # Mientras quede texto por analizar y no haya errores
    while pos < len(text):
        # Obtener el primer token desde la posición actual
        token = get_token(text, pos)
        # Si se obtiene un token válido, añadirlo a la lista y avanzar la posición
        if token:
            tokens.append(token)
            pos += len(token.value)
        # Si no se obtiene un token válido, lanzar una excepción o devolver la lista hasta el momento
        else:
            raise Exception(f"Invalid character at position {pos}")
            # return tokens
    # Devolver la lista completa de tokens
    return tokens

# Probar las funciones con un ejemplo
text = "(12+34)-56"
tokens = get_tokens(text)
print(tokens)
