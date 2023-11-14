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

textIf="NORTE(2!=2){\n\tdracarys('Verdadero')\n}SUR{\n\tdracarys('Falso')\n}ENDNORTE"
textFor="VIAJE(espada i = 1 to 10 step 2)\n\tdracarys(i*2)"
def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")
    try:
        tokens = lexer(input_expr)
        ast = parse_program(tokens)

        if ast:
            # Intérprete
            results = evaluate(ast)
            if results:
                output_text.configure(state="normal")
                output_text.delete("1.0", "end")

                # Modificar la forma en que se manejan los resultados
                for result in results:
                    if isinstance(result, list):
                        # Si es una lista, concaténala en una línea sin comas ni espacios
                        result_line = "".join(map(str, result))
                        output_text.insert("end", result_line + "\n")
                    else:
                        # Si no es una lista, imprímelo en una nueva línea
                        output_text.insert("end", str(result) + "\n")

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
    if selected_option == "IF":
        input_text.insert("end", "\nNORTE(2==2){\n\tDRACARYS('VERDAD')\n}SUR{\n\tDRACARYS('FALSO')\n}ENDNORTE")
    elif selected_option == "FOR":
        input_text.insert("end", f"VIAJE(espada i = 1 to 10 step 2) dracarys(i*2)")
    elif selected_option == "PRINT":
        input_text.insert("end", f"dracarys('Hola mundo')")
    elif selected_option == "WHILE":
        input_text.insert("end", "\nMIENTRAS(2==2){\n\tDRACARYS('Bucle infinito')\n}ENDMIENTRAS")

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
def add_selected_option_to_input_text():
    selected_option = combobox.get()
    clear_input()
    if selected_option=="IF":
        input_text.insert("end", textIf)
    if selected_option=="FOR":
        input_text.insert("end", textFor)
    if selected_option=="hola mundo":
        input_text.insert("end", f"dracarys('Hola mundo')")
    if selected_option=="op 4":
        input_text.insert("end", f"text")
    if selected_option=="5":
        input_text.insert("end", f"text")


# Configurar la ventana principal
app = customtkinter.CTk()
app.geometry("1000x625")
app.iconbitmap("drake.ico")

# Crear un contenedor para los botones y centrarlos
button_container = customtkinter.CTkFrame(app)
button_container.pack()

options = ["Estructuras de datos", "IF", "FOR", "WHILE", "PRINT", "-", "-"]
combobox = customtkinter.CTkComboBox(button_container, values=options)
combobox.pack(side="left", padx=10)
add_selected_option_button = customtkinter.CTkButton(button_container, text="Agregar", command=add_selected_option_to_input_text)
add_selected_option_button.configure(font=("Consolas", 17))
add_selected_option_button.pack(side="left", padx=10)
combobox.bind("<<ComboboxSelected>>", add_selected_option_to_input_text)

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

options = ["IF", "FOR", "hola mundo", "op 4", "5"]
combobox = customtkinter.CTkComboBox(button_container,height=55,width=160, values=options)
combobox.pack(side="left", padx=10)
combobox.set("Opciones")


add_selected_option_button = customtkinter.CTkButton(button_container,height=55,width=160, text="Agregar opción seleccionada", command=add_selected_option_to_input_text)
add_selected_option_button.pack(side="left", padx=10)

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
