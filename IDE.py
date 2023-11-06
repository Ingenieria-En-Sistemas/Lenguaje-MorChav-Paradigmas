import tkinter as tk
from tkinter import ttk
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate

def execute_expression():
    input_expr = input_entry.get()
    try:
        # Lexer
        tokens = lexer(input_expr)

        # Parser
        ast = parse_program(tokens)

        if ast:
            # Intérprete
            result = evaluate(ast)
            if result is not None:
                output_label.config(text=f"Resultado: {result[0]}")
            else:
                output_label.config(text="Error al evaluar la expresión.")
        else:
            output_label.config(text="Error de sintaxis. Intente nuevamente.")
    except Exception as e:
        output_label.config(text=f"Error: {e}")

# Configurar la ventana principal
root = tk.Tk()
root.title("IDE Simple")

# Ajustar el tamaño de la ventana
root.geometry("400x200")

# Crear una etiqueta para la entrada
input_label = tk.Label(root, text="Ingrese una expresión:")
input_label.pack()

# Crear un campo de entrada para la expresión
input_entry = tk.Entry(root)
input_entry.pack()

# Crear un botón para ejecutar la expresión
execute_button = tk.Button(root, text="Ejecutar", command=execute_expression)
execute_button.pack()

# Crear una etiqueta para mostrar el resultado
output_label = tk.Label(root, text="")
output_label.pack()

# Ejecutar la aplicación
root.mainloop()
