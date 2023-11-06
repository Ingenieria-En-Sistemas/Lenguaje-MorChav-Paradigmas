"""import tkinter as tk
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
root.geometry("800x400")

# Crear una etiqueta para la entrada
input_label = tk.Label(root, text="Ingrese una expresión:")
input_label.pack()

# Crear un campo de entrada para la expresión
input_entry = tk.Entry(root)
input_entry.pack(side="left", padx=10, pady=10, fill="both")

# Crear un botón para ejecutar la expresión
execute_button = tk.Button(root, text="Ejecutar", command=execute_expression)
execute_button.pack()

# Crear una etiqueta para mostrar el resultado
output_label = tk.Label(root, text="")
output_label.pack()

# Ejecutar la aplicación
root.mainloop()
"""
#OPCION 2
"""
import tkinter as tk
from tkinter import scrolledtext  # Importa scrolledtext para el campo de entrada de texto
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate

def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")  # Obtiene el texto desde la línea 1, caracter 0 hasta el final menos el último carácter
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
root.geometry("800x400")

# Crear una etiqueta para la entrada
input_label = tk.Label(root, text="Ingrese una expresión:")
input_label.pack()

# Crear un campo de entrada de texto desplazable
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
input_text.pack(padx=10, pady=10, fill="both")

# Crear un botón para ejecutar la expresión
execute_button = tk.Button(root, text="Ejecutar", command=execute_expression)
execute_button.pack()

# Crear una etiqueta para mostrar el resultado
output_label = tk.Label(root, text="")
output_label.pack()

# Ejecutar la aplicación
root.mainloop()
"""
#oPCION 3

import tkinter as tk
from tkinter import scrolledtext  # Importa scrolledtext para el campo de entrada de texto
from tkinter import Text  # Importa Text para el campo de salida
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate

def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")  # Obtiene el texto desde la línea 1, caracter 0 hasta el final menos el último carácter
    try:
        # Lexer
        tokens = lexer(input_expr)

        # Parser
        ast = parse_program(tokens)

        if ast:
            # Intérprete
            result = evaluate(ast)
            if result is not None:
                output_text.config(state="normal")  # Habilita la edición para escribir en el widget de salida
                output_text.delete("1.0", "end")  # Borra el texto existente
                output_text.insert("1.0", f"Resultado: {result[0]}\n")  # Inserta el nuevo resultado
                output_text.config(state="disabled")  # Deshabilita la edición nuevamente
            else:
                output_text.config(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", "Error al evaluar la expresión.\n")
                output_text.config(state="disabled")
        else:
            output_text.config(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Error de sintaxis. Intente nuevamente.\n")
            output_text.config(state="disabled")
    except Exception as e:
        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Error: {e}\n")
        output_text.config(state="disabled")

# Configurar la ventana principal
root = tk.Tk()
root.title("MorChav IDE")

# Ajustar el tamaño de la ventana
root.geometry("1000x500")

# Crear una etiqueta para la entrada
input_label = tk.Label(root, text="Ingrese una expresión:")
input_label.pack()

# Crear un campo de entrada de texto desplazable
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
input_text.pack(padx=10, pady=10, fill="both")

# Crear un botón para ejecutar la expresión
execute_button = tk.Button(root, text="Ejecutar", command=execute_expression)
execute_button.pack()

# Crear un campo de salida de texto desplazable
output_text = Text(root, state="disabled", wrap=tk.WORD, width=40, height=10)
output_text.pack(padx=10, pady=10, fill="both")

# Ejecutar la aplicación
root.mainloop()
