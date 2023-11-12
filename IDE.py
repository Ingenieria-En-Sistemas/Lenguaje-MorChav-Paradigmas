import customtkinter
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate
from customtkinter import CTkImage  # Importar CTkImage desde customtkinter
from PIL import Image
import random

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

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
                output_text.insert("1.0", f"{result}\n")
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
def add_selected_option_to_input_text():
    selected_option = combobox.get()
    if selected_option=="IF":
        input_text.insert("end", f"\n")
    if selected_option=="FOR":
        input_text.insert("end", f"\n")
    if selected_option=="hola mundo":
        input_text.insert("end", f"dracarys('Hola mundo')")

# Lista de títulos aleatorios
random_titles = [
    "El odio es bueno si nos hace seguir adelante. (Sandor ‘El Perro’ Clegane)",
    "Cuando se juega al Juego de Tronos, solo se puede ganar o morir. (Cersei Lannister)",
    "Los dioses no tienen piedad, por eso son dioses. (Cersei Lannister)",
    "Las serpientes enfadadas atacan. Eso hace más fácil aplastar sus cabezas. (Daenerys Targaryen)",
    "Cualquier hombre que deba decir ‘soy el rey’, no es un verdadero rey. (Tywin Lannister)",
]

# Función para cambiar el título de la ventana
def change_window_title():
    new_title = random.choice(random_titles)
    app.title(new_title)

# Configurar la ventana principal
app = customtkinter.CTk()
app.geometry("1000x625")
app.iconbitmap("drake.ico")

# Crear un contenedor para los botones y centrarlos
button_container = customtkinter.CTkFrame(app)
button_container.pack()

options = ["Estructuras de datos","IF", "FOR", "hola mundo", "4", "5"]
combobox = customtkinter.CTkComboBox(button_container, values=options)
combobox.pack(side="left", padx=10)
add_selected_option_button = customtkinter.CTkButton(button_container, text="Agregar opción seleccionada", command=add_selected_option_to_input_text)
add_selected_option_button.pack(side="left", padx=10)
combobox.bind("<<ComboboxSelected>>", add_selected_option_to_input_text)

# Cargar las imágenes como CTkImage y ajustar el tamaño
run_image = Image.open("run.png")  # Reemplaza con la ubicación de tu icono "Ejecutar"
run_icon = CTkImage(light_image=run_image, size=(50, 50))  # Ajusta el tamaño a 32x32 píxeles

clear_image = Image.open("clear.png")  # Reemplaza con la ubicación de tu icono "Limpiar"
clear_icon = CTkImage(light_image=clear_image, size=(50, 50))  # Ajusta el tamaño a 32x32 píxeles

# Crear un campo de entrada de texto desplazable más grande
input_text = customtkinter.CTkTextbox(app, wrap=customtkinter.WORD, width=500, height=350)
input_text.configure(font=("Consolas", 17))
input_text.pack(padx=10, pady=(10, 5), fill="both")

# Crea el botón para ejecutar la expresión con el icono
execute_button = customtkinter.CTkButton(button_container, text="Run", image=run_icon, compound="left", command=execute_expression)
execute_button.configure(font=("Consolas", 17))
execute_button.pack(side="left", padx=10)

# Crea el botón para limpiar el campo de entrada y el campo de salida con el icono
clear_button = customtkinter.CTkButton(button_container, text="Clean", image=clear_icon, compound="left", command=clear_input)
clear_button.configure(font=("Consolas", 17))
clear_button.pack(side="left", padx=10)

# Crear un campo de salida de texto desplazable más grande
output_text = customtkinter.CTkTextbox(app, state="disabled", wrap=customtkinter.WORD, width=60, height=200)
output_text.configure(font=("Consolas", 17))
output_text.pack(padx=10, pady=(5, 10), fill="both")

# Carga y cambia el título de la ventana al iniciar
change_window_title()

# Ejecutar la aplicación
app.mainloop()

"""
norte(2==2){
	dracarys("hola")
}SUR{
	dracarys("falta")
}endnorte 
"""