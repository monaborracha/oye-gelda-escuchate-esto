import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import time
import pygame  # Importar pygame para modificar el audio
import sys  # Importar sys para salir del programa

# Inicializar pygame para la música
pygame.mixer.init()

# Crear la ventana principal
root = tk.Tk()
root.withdraw()  # Ocultar ventana principal temporalmente

# Inicializar variable global para el tamaño del logo
logo_size = None

# Función principal que pide el peso
def pedir_peso():
    global logo_size  # Hacer que logo_size sea global
    while True:  # Bucle para seguir pidiendo el peso
        # Preguntar al usuario por su peso
        peso_input = simpledialog.askstring("Peso", "Ingrese su peso en kg:", parent=root)
        
        # Verificar si el usuario presionó "Cancelar" o cerró el diálogo
        if peso_input is None:
            root.quit()  # Salir de la aplicación
            sys.exit()   # Terminar el programa

        try:
            peso = float(peso_input)  # Intentar convertir la entrada a float
            if peso >= 100:
                mostrar_animacion()
            elif peso < 100:
                messagebox.showinfo("Resultado", "god")  # Mostrar "god"
            else:
                print("No se ingresó un peso válido.")
        except ValueError:
            messagebox.showwarning("Error", "Por favor, ingrese un número válido.")  # Mensaje de error

# Función para mostrar la animación
def mostrar_animacion():
    global root, logo_size  # Hacer que root y logo_size sean globales
    logo_size = int(min(root.winfo_screenwidth(), root.winfo_screenheight()) * 0.2)  # Inicializar tamaño del logo

    # Reproducir la música en bucle
    pygame.mixer.music.load("D:/zzz/oyegelda/musica.mp3")  # Reemplaza con la ruta completa de tu archivo de música
    pygame.mixer.music.play(-1)  # -1 hace que la música se reproduzca en bucle

    # Crear nueva ventana para mostrar la animación
    ventana = tk.Toplevel(root)
    ventana.title("GORDA")

    # Obtener tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Configurar la ventana para ocupar casi toda la pantalla
    ventana.geometry(f"{screen_width}x{screen_height}")
    ventana.resizable(False, False)  # Evitar que el usuario redimensione la ventana

    # Cargar imagen de fondo (usa la ruta completa)
    fondo = Image.open("D:/zzz/oyegelda/fondo.jpg")  # Reemplaza con la ruta completa de fondo.jpg
    fondo = fondo.resize((screen_width, screen_height))
    fondo = ImageTk.PhotoImage(fondo)

    # Crear canvas para fondo y logo
    canvas = tk.Canvas(ventana, width=screen_width, height=screen_height)
    canvas.pack()

    # Mostrar imagen de fondo
    canvas.create_image(0, 0, anchor=tk.NW, image=fondo)

    # Cargar logo inicial (usa la ruta completa)
    logo_img_original = Image.open("D:/zzz/oyegelda/logo.png").convert("RGBA")

    # Variable para guardar la imagen rotada
    logo_tk_rotado = None

    # Función para rotar y agrandar el logo
    def rotar_y_agrandar_logo(angulo=0):
        global logo_size, logo_tk_rotado

        # Aumenta el tamaño del logo poco a poco
        logo_size += 5  # Ajusta el valor para cambiar la velocidad de crecimiento
        logo_img = logo_img_original.resize((logo_size, logo_size))

        # Rota el logo
        logo_rotado = logo_img.rotate(angulo, expand=True)  # expand=True para evitar recortes
        logo_rotado = logo_rotado.convert("RGBA")  # Asegurarse de que sea RGBA

        # Crear un fondo transparente para la imagen rotada
        fondo_transparente = Image.new("RGBA", logo_rotado.size, (255, 255, 255, 0))  # Fondo transparente
        fondo_transparente.paste(logo_rotado, (0, 0), logo_rotado)  # Pegar la imagen rotada en el fondo

        logo_tk_rotado = ImageTk.PhotoImage(fondo_transparente)

        # Limpiar el canvas antes de dibujar el nuevo logo
        canvas.delete("logo")  # Elimina cualquier logo anterior
        canvas.create_image(screen_width // 2, screen_height // 2, image=logo_tk_rotado, tags="logo")  # Añade nuevo logo

        # Esperar antes de la próxima rotación
        ventana.update()
        time.sleep(0.05)

        # Incrementa el ángulo para la siguiente rotación
        ventana.after(50, rotar_y_agrandar_logo, angulo + 10)

    # Función para manejar el cierre de la ventana
    def on_closing():
        pygame.mixer.music.stop()  # Detener la música
        ventana.destroy()  # Cerrar la ventana
        pedir_peso()  # Volver a preguntar el peso

    # Asignar la función on_closing al evento de cierre de la ventana
    ventana.protocol("WM_DELETE_WINDOW", on_closing)

    # Iniciar la rotación y el agrandamiento del logo
    rotar_y_agrandar_logo()

    # Mostrar ventana y empezar bucle de Tkinter
    ventana.mainloop()

# Iniciar el proceso pidiendo el peso
pedir_peso()