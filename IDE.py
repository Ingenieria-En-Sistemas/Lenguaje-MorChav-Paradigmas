import customtkinter, random
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkImage
from PIL import Image
from Lexer import lexer
from Parser import parse_program
from Interpreter import evaluate,evaluate_single

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


def execute_expression():
    input_expr = input_text.get("1.0", "end-1c")
    try:
        tokens = lexer(input_expr)
        ast = parse_program(tokens)

        if ast:
            # Intérprete
            for line_node in ast:
                line_result = evaluate_single(line_node)
                if line_result is not None:
                    output_text.configure(state="normal")
                    output_text.insert("end", str(line_result) + "\n")
                    output_text.configure(state="disabled")

        else:
            output_text.configure(state="normal")
            output_text.insert("end", "Error de sintaxis. Intente nuevamente.\n")
            output_text.configure(state="disabled")
    except Exception as e:
        output_text.configure(state="normal")
        output_text.insert("end", f"Error: {e}\n")
        output_text.configure(state="disabled")



def clear_input():
    input_text.delete("1.0", "end")
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.configure(state="disabled")


def add_selected_option_to_input_text():
    selected_option = combobox.get()
    if selected_option == "IF":
        input_text.insert(
            "end",
            """NORTE(2!=2){\n\tdracarys("Verdadero")\n}SUR{\n\tdracarys("Falso")\n}ENDNORTE""",
        )
    elif selected_option == "FOR":
        input_text.insert("end", f"VIAJE(espada i = 1 to 10 step 2) dracarys(i*2)")
    elif selected_option == "PRINT":
        input_text.insert("end", f"""dracarys("Hola mundo")""")
    elif selected_option == "WHILE":
        input_text.insert(
            "end",
            """\nespada i = 1 CAMINO(i<10){\n\tDRACARYS("Menor que 10")\n i=i+1\n}ENDCAMINO""",
        )


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
    # Use CTkMessagebox for the exit confirmation
    msg = CTkMessagebox(
        title="Salir",
        font=("Consolas", 17),
        message="¿Estás seguro de que quieres salir?",
        icon="question",
        option_1="Cancelar",
        option_2="Sí",
        justify="center",
    )
    response = msg.get()

    if response == "Sí":
        app.destroy()


# Configurar la ventana principal
app = customtkinter.CTk()
app.geometry("800x600")
app.iconbitmap("Icons/drake.ico")

# Crear un contenedor para los botones y centrarlos
button_container = customtkinter.CTkFrame(app)
button_container.pack()

option_container = customtkinter.CTkFrame(app)
option_container.pack(side="top", pady=10)


# Cargar las imágenes como CTkImage y ajustar el tamaño
run_image = Image.open("Icons/run.png")
run_icon = CTkImage(light_image=run_image, size=(35, 20))

exit_image = Image.open("Icons/exit.png")
exit_icon = CTkImage(light_image=exit_image, size=(35, 35))

new_image = Image.open("Icons/new.png")
new_icon = CTkImage(light_image=new_image, size=(35, 35))

clear_image = Image.open("Icons/clear.png")
clear_icon = CTkImage(light_image=clear_image, size=(45, 45))


# Crear un campo de entrada de texto desplazable más grande
input_text = customtkinter.CTkTextbox(app, wrap=customtkinter.WORD, height=250)
input_text.configure(font=("Consolas", 17), undo=True)
input_text.pack(padx=10, pady=(10, 5), fill="both")

options = ["IF", "FOR", "PRINT", "WHILE", "-"]
combobox = customtkinter.CTkComboBox(
    option_container, height=55, width=160, values=options
)
combobox.configure(font=("Consolas", 17))
combobox.pack(side="left", padx=20)
combobox.set("Opciones")


add_selected_option_button = customtkinter.CTkButton(
    option_container,
    height=55,
    width=160,
    image=run_icon,
    text="Agregar ",
    command=add_selected_option_to_input_text,
)
add_selected_option_button.configure(font=("Consolas", 17))
add_selected_option_button.pack(side="left", padx=20)

# Crear botones adicionales "Nuevo", "Opciones" y "Salir"
new_button = customtkinter.CTkButton(
    button_container,
    text="Nuevo",
    image=new_icon,
    compound="left",
    command=clear_input,
    fg_color="white",
    text_color="black",
)
new_button.configure(font=("Consolas", 17))
new_button.pack(side="left", padx=10)

# Crear el botón para ejecutar la expresión con el icono
execute_button = customtkinter.CTkButton(
    button_container,
    text="Ejecutar",
    image=clear_icon,
    compound="left",
    command=execute_expression,
    fg_color="green",
    text_color="black",
)
execute_button.configure(font=("Consolas", 17))
execute_button.pack(side="left", padx=10)


exit_button = customtkinter.CTkButton(
    button_container,
    text="Salir",
    image=exit_icon,
    compound="left",
    command=exit_action,
    fg_color="#ec5353",
    text_color="black",
)
exit_button.configure(font=("Consolas", 17))
exit_button.pack(side="left", padx=10)

# Crear un campo de salida de texto desplazable más grande
output_text = customtkinter.CTkTextbox(
    app, state="disabled", wrap=customtkinter.WORD, height=200
)
output_text.configure(font=("Consolas", 17))
output_text.pack(padx=10, pady=(5, 10), fill="both")

def compile_program():
    input_expr = input_text.get("1.0", "end-1c")
    try:
        tokens = lexer(input_expr)
        ast = parse_program(tokens)

        if ast:
            message = "Compilación correcta"
        else:
            message = "Error de sintaxis. Compilación fallida."

        # Muestra el mensaje en una ventana emergente
        msg_box = CTkMessagebox(
            title="Resultado de la Compilación",
            font=("Consolas", 17),
            message=message,
            icon="Icons/run.png" if ast else "",
            option_1="Aceptar",
            justify="center",
        )
        msg_box.get()

    except Exception as e:
        # Muestra un mensaje de error en una ventana emergente
        msg_box = CTkMessagebox(
            title="Error",
            font=("Consolas", 17),
            message=f"Error: {e}",
            icon="error",
            option_1="Aceptar",
            justify="center",
        )
        msg_box.get()
compile_button = customtkinter.CTkButton(
    button_container,
    text="Compilar",
    image=clear_icon,
    compound="left",
    command=compile_program,
    fg_color="orange",
    text_color="black",
)
compile_button.configure(font=("Consolas", 17))
compile_button.pack(side="left", padx=10)
# Carga y cambia el título de la ventana al iniciar
change_window_title()

# Ejecutar la aplicación
app.mainloop()
