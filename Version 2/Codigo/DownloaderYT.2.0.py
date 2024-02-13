import sys
import tkinter as tk
from pathlib import Path
import os
from tkinter import *
from tkinter import Entry, Frame, Tk, font
from tkinter import ttk
from pytube import YouTube
from tkinter import messagebox as MessageBox
import threading

# Obtener la ruta del ejecutable o script
ruta_ejecutable = getattr(sys, '_MEIPASS', Path(os.path.dirname(os.path.abspath(__file__))))

# Funciones del descargador
# Variable global para controlar la cancelación de la descarga
descarga_cancelada = False

# Funciones del descargador
def descargar_video(enlace):
    global descarga_cancelada
    try:
        video = YouTube(enlace)
        
        if seleccion.get() == 1:  # Descargar video
            descarga = video.streams.get_highest_resolution()
        elif seleccion.get() == 2:  # Descargar audio
            descarga = video.streams.filter(only_audio=True).first()

        # Obtener el nombre del video
        nombre_video = video.title

        # Eliminar caracteres inválidos para el nombre del archivo
        nombre_video = "".join(x for x in nombre_video if x.isalnum() or x in [' ', '.', '_']).strip()

        # Obtener el directorio de trabajo actual
        directorio_actual = os.getcwd()

        # Descargar el video o audio con el nombre del video
        descarga.download(output_path=directorio_actual, filename=nombre_video + ".mp4" if seleccion.get() == 1 else nombre_video + ".mp3")

        # Construir la ruta completa del archivo descargado
        ruta_archivo = os.path.join(directorio_actual, nombre_video + (".mp4" if seleccion.get() == 1 else ".mp3"))

        # Mensaje de descarga
        MessageBox.showinfo("Éxito", f"Descarga completada exitosamente. Video guardado en {ruta_archivo}")
    except Exception as e:
        if not descarga_cancelada:
            MessageBox.showerror("Error", f"Error al descargar el video:\n{str(e)}")
    finally:
        # Habilitar nuevamente el botón después de completar la descarga o cancelar
        boton.config(state=NORMAL)

def accion():
    global descarga_cancelada
    enlace = videos.get()
    if enlace:
        # Deshabilitar el botón mientras se realiza la descarga
        boton.config(state=DISABLED)

        # Reiniciar la variable de cancelación
        descarga_cancelada = False

        # Crear un hilo para la descarga y ejecutarlo
        thread_descarga = threading.Thread(target=descargar_video, args=(enlace,))
        thread_descarga.start()
    else:
        MessageBox.showwarning("Advertencia", "Por favor, ingresa un enlace antes de intentar descargar.")

def cancelar_descarga():
    global descarga_cancelada
    descarga_cancelada = True
    MessageBox.showinfo("Cancelado", "Descarga cancelada.")
    # Habilitar nuevamente el botón después de cancelar
    boton.config(state=NORMAL)

def limpiar_entry():
    videos.delete(0, END)

# Crear la ventana principal
root = Tk()
root.title("Descargador de Videos de YouTube")


# Configurar el tamaño de la ventana
ancho_ventana = 500
alto_ventana = 340

# Calcular las coordenadas x e y para centrar la ventana
x_pos = (root.winfo_screenwidth() - ancho_ventana) // 2
y_pos = (root.winfo_screenheight() - alto_ventana) // 2

# Establecer la geometría de la ventana para centrarla en la pantalla
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Bloquear el redimensionamiento de la ventana
root.resizable(False, False)

# Configurar el tema de Tkinter
style = ttk.Style(root)
style.theme_use('clam')  # Puedes probar con otros temas como 'default' o 'alt'

# Cambiar el color de fondo de la barra superior a verde
style.configure('TFrame', background='green')  # Cambia el color a tu preferencia

# Crear dos divisiones (Frames)
frame_div_verde = Frame(root, bg="#000000", width=500, height=500)
frame_div_verde.grid(row=0, column=1, padx=0, pady=0)

# Estructuras
menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Para más información", menu=helpmenu)
helpmenu.add_command(label="GitHub", command=lambda: MessageBox.showinfo("Usuario", "Soy Danny Crisostomo"))
helpmenu.add_command(label="Autor", command=lambda: MessageBox.showinfo("Autor", "@DannyVC\n"))
helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 2.0.0"))
menubar.add_command(label="Salir", command=root.destroy)


# Estilo del titulo
estilo_titulo = {
    "font": font.Font(family="Georgia", size=45, weight="bold"),
    "bg": "#000000",
    "fg": "#E91E63",
    "anchor": "center",
    "text": "DOWNLOAD",
}
LOGO = Label(frame_div_verde, **estilo_titulo)
LOGO.place(x=50, y=10)

estilo_titulo1 = {
    "font": font.Font(family="Georgia", size=0, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "anchor": "center",
    "text": "________________________________________",
}
LOGO1 = Label(frame_div_verde, **estilo_titulo1)
LOGO1.place(x=30, y=80)


# Infrese link texto
estilo_titulo = {
    "font": font.Font(family="Georgia", size=13, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "anchor": "center",
    "text": "Ingrese link del vídeo de YouTube:",
}
titulo = Label(frame_div_verde, **estilo_titulo)
titulo.place(x=30, y=180)

# Estilo del Entry
estilo_entry = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 40,
    "bg": "#3498db",  # Fondo oscuro con opacidad
    "fg": "white",  # Texto en color blanco
    "bd": 2,  # Ancho del borde
    "relief": "flat",  # Sin relieve en el borde
    "insertbackground": "#01579b",  # Color del cursor (azul oscuro)
}

videos = Entry(frame_div_verde, **estilo_entry)
videos.place(x=30, y=220)

# Estilo del boton
estilo_boton = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Descargar",
    "command": accion,
    "width": 13,
    "height": 2,
    "bg": "#3498db",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
boton = Button(frame_div_verde, **estilo_boton)
boton.place(x=30, y=270)

# Estilo del boton nuevo
estilo_botonNuevo = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Nuevo",
    "command": limpiar_entry,
    "width": 13,
    "height": 2,
    "bg": "#8eeddd",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
nuevo = Button(frame_div_verde, **estilo_botonNuevo)
nuevo.place(x=185, y=270)

# Estilo del boton cancelar
estilo_botonCancelar = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Cancelar",
    "command": cancelar_descarga,
    "width": 13,
    "height": 2,
    "bg": "#e74c3c",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
cancelar = Button(frame_div_verde, **estilo_botonCancelar)
cancelar.place(x=340, y=270)


# Opciones para descargar video o música
seleccion = tk.IntVar()

radio_video = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "width": 18,
    "height": 2,
    "bg": "#f54ba0",
    "fg": "black",
    "bd": 0,
    "relief": "solid",
}
radio_video = tk.Radiobutton(frame_div_verde, **radio_video, variable=seleccion, text="Video", value=1)
radio_video.place(x=30, y=120)

radio_audio = {
    "font": font.Font(family="Helvetica",  size=12, weight="bold"),
    "width": 18,
    "height": 2,
    "bg": "#be74e3",
    "fg": "black",
    "bd": 0,
    "relief": "solid",
}
radio_audio = tk.Radiobutton(frame_div_verde, **radio_audio,  variable=seleccion,  text="Música" , value=2)
radio_audio.place(x=270, y=120)




# Ejecutar el bucle principal de la aplicación
root.mainloop()
