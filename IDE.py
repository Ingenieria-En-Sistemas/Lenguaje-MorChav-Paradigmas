import customtkinter
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate
from customtkinter import CTkImage
from PIL import Image
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")
    try:
        tokens = lexer(input_expr)
        ast = parse_program(tokens)

        if ast:
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

def exit_action():
    if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
        app.destroy()

def options_action():
    def save_options():
        selected_option = v.get()
        print(f"Opción seleccionada: {selected_option}")
        options_window.destroy()

    options_window = tk.Toplevel(app)
    options_window.title("Opciones")

    v = tk.StringVar(options_window)
    v.set("Opción 1")

    options_menu = ttk.Combobox(options_window, textvariable=v)
    options_menu['values'] = ("Opción 1", "Opción 2", "Opción 3")
    options_menu.pack(padx=10, pady=10)

    save_button = tk.Button(options_window, text="Guardar", command=save_options)
    save_button.pack(padx=10, pady=10)

# Configurar la ventana principal
app = customtkinter.CTk()
app.geometry("1000x625")
app.iconbitmap("drake.ico")

# Crear un contenedor para los botones y centrarlos
button_container = customtkinter.CTkFrame(app)
button_container.pack()

# Cargar las imágenes como CTkImage y ajustar el tamaño
run_image = Image.open("run.png")
run_icon = CTkImage(light_image=run_image, size=(45, 45))

exit_image = Image.open("exit.png")
exit_icon = CTkImage(light_image=exit_image, size=(45, 45))

new_image = Image.open("new.png")
new_icon = CTkImage(light_image=new_image, size=(45, 45))

clear_image = Image.open("clear.png")
clear_icon = CTkImage(light_image=clear_image, size=(45, 45))


# Crear un campo de entrada de texto desplazable más grande
input_text = customtkinter.CTkTextbox(app, wrap=customtkinter.WORD, width=500, height=350)
input_text.configure(font=("Consolas", 17))
input_text.pack(padx=10, pady=(10, 5), fill="both")

optionmenu_1 = customtkinter.CTkOptionMenu(button_container, height=55,width=160, values=["Estructuras de Lenguaje", "Palabras Reservadas", "Sintaxis", "Semántica", "Tipos de Datos"])
optionmenu_1.configure(font=("Consolas", 17))
optionmenu_1.pack(side="left", padx=10)
optionmenu_1.set("Opciones")

# Crear botones adicionales "Nuevo", "Opciones" y "Salir"
new_button = customtkinter.CTkButton(button_container, text="Nuevo", image=new_icon, compound="left", command=clear_input, fg_color="white",text_color="black")
new_button.configure(font=("Consolas", 17))
new_button.pack(side="left", padx=10)

# Crear el botón para ejecutar la expresión con el icono
execute_button = customtkinter.CTkButton(button_container, text="Ejecutar", image=run_icon, compound="left", command=execute_expression, fg_color="green",text_color="black")
execute_button.configure(font=("Consolas", 17))
execute_button.pack(side="left", padx=10)



exit_button = customtkinter.CTkButton(button_container, text="Salir",image=exit_icon, compound="left", command=exit_action, fg_color="#ec5353", text_color="black")
exit_button.configure(font=("Consolas", 17))
exit_button.pack(side="left", padx=10)

# Crear un campo de salida de texto desplazable más grande
output_text = customtkinter.CTkTextbox(app, state="disabled", wrap=customtkinter.WORD, width=60, height=200)
output_text.configure(font=("Consolas", 17))
output_text.pack(padx=10, pady=(5, 10), fill="both")

# Carga y cambia el título de la ventana al iniciar
change_window_title()

# Ejecutar la aplicación
app.mainloop()
