import customtkinter
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate
from tkinter import PhotoImage
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System") # Modos: system (predeterminado), light, dark
customtkinter.set_default_color_theme("blue") # Temas: blue (predeterminado), dark-blue, green

def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")
    try:
        # Lexer
        tokens = lexer(input_expr)

        # Parser
        ast = parse_program(tokens)

        if ast:
            # Intérprete
            result = evaluate(ast)
            if result is not None:
                output_text.configure(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", f"Resultado: {result}\n")
                output_text.configure(state="disabled")
            else:
                output_text.configure(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", "Error al evaluar la expresión.\n")
                output_text.configure(state="disabled")
        else:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Error de sintaxis. Intente nuevamente.\n")
            output_text.configure(state="disabled")
    except Exception as e:
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Error: {e}\n")
        output_text.configure(state="disabled")

def clear_input():
    input_text.delete("1.0", "end")
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.configure(state="disabled")

# Configurar la ventana principal
app = customtkinter.CTk() # crear ventana CTk como se hace con la ventana Tk
app.title("MorChav IDE")

# Ajustar el tamaño de la ventana
app.geometry("1000x400")

# Crear un contenedor para los botones y centrarlos
button_container = customtkinter.CTkFrame(app)
button_container.pack()

# Cargar los iconos como imágenes
run_icon = Image.open("run.png")  # Reemplaza con la ubicación de tu icono "Ejecutar"
clear_icon = Image.open("clear.png")  # Reemplaza con la ubicación de tu icono "Limpiar"

# Convierte las imágenes a objetos PhotoImage
run_icon = ImageTk.PhotoImage(run_icon)
clear_icon = ImageTk.PhotoImage(clear_icon)

# Crear un campo de entrada de texto desplazable más grande
input_text = customtkinter.CTkTextbox(app, wrap=customtkinter.WORD, width=600, height=150)
input_text.pack(padx=10, pady=(10, 5), fill="both")  # Aumenta la altura y ajusta el relleno vertical

# Crea el botón para ejecutar la expresión con el icono
execute_button = customtkinter.CTkButton(button_container, text="Ejecutar", image=run_icon, compound="left", command=execute_expression)
execute_button.pack(side="left", padx=10)  # Alinea el botón "Ejecutar" a la izquierda

# Crea el botón para limpiar el campo de entrada y el campo de salida con el icono
clear_button = customtkinter.CTkButton(button_container, text="Limpiar", image=clear_icon, compound="left", command=clear_input)
clear_button.pack(side="left", padx=10)  # Alinea el botón "Limpiar" a la izquierda

# Crear un campo de salida de texto desplazable más grande
output_text = customtkinter.CTkTextbox(app, state="disabled", wrap=customtkinter.WORD, width=60, height=150)
output_text.pack(padx=10, pady=(5, 10), fill="both")  # Aumenta la altura y ajusta el relleno vertical

# Ejecutar la aplicación
app.mainloop()
