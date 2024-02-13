from tkinter import *
from tkinter import Entry, Frame, Tk, font
from tkinter import ttk
from pytube import YouTube
from tkinter import messagebox as MessageBox
import os
import threading


# Funciones del descargador
# Variable global para controlar la cancelación de la descarga
descarga_cancelada = True

# Funciones del descargador
def descargar_video(enlace):
    global descarga_cancelada
    try:
        video = YouTube(enlace)
        descarga = video.streams.get_highest_resolution()

        # Obtener el directorio de trabajo actual
        directorio_actual = os.getcwd()

        # Obtener el nombre del video
        nombre_video = video.title

        # Eliminar caracteres inválidos para el nombre del archivo
        nombre_video = "".join(x for x in nombre_video if x.isalnum() or x in [' ', '.', '_']).strip()

        # Construir la ruta completa para guardar el video
        ruta_video = os.path.join(directorio_actual, nombre_video + ".mp4")

        descarga.download(output_path=directorio_actual, filename=nombre_video + ".mp4")

        MessageBox.showinfo("Éxito", f"Descarga completada exitosamente. Video guardado en {ruta_video}")
    except Exception as e:
        if not descarga_cancelada:
            MessageBox.showerror("Error", f"Error al descargar el video:\n{str(e)}")
    finally:
        # Habilitar nuevamente el botón después de completar la descarga o cancelar
        boton.config(state=NORMAL)


def accion():
    global descarga_cancelada
    enlace = videos1.get()
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
    videos1.delete(0, END)







# Crear la ventana principal
root = Tk()
root.title("Descargador de Videos de YouTube")

# Configurar el tamaño de la ventana
ancho_ventana = 500
alto_ventana = 400

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
#frame_div_rojo = Frame(root, bg="#0C131F", width=500, height=500)
#frame_div_rojo.grid(row=0, column=0, padx=0, pady=0)

frame_div_verde = Frame(root, bg="#000000", width=500, height=500)
frame_div_verde.grid(row=0, column=1, padx=0, pady=0)

# Estructuras
menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Para más información", menu=helpmenu)
helpmenu.add_command(label="GitHub", command=lambda: MessageBox.showinfo("Usuario", "Soy Danny Crisostomo"))
helpmenu.add_command(label="Autor", command=lambda: MessageBox.showinfo("Autor", "@DannyVC\n"))
helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 1.0.0"))
menubar.add_command(label="Salir", command=root.destroy)


titulo = {
    "font": font.Font(family="Georgia", size=50, weight="bold"),
    "bg": "#000000",
    "fg": "#E91E63",
    "anchor": "center",
    "text": "DOWNLOAD",
}
titulo = Label(frame_div_verde, **titulo)
titulo.place(x=30, y=50)
# Estilo del titulo
estilo_titulo = {
    "font": font.Font(family="Georgia", size=13, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "anchor": "center",
    "text": "Ingrese link del vídeo de YouTube:",
}
titulo = Label(frame_div_verde, **estilo_titulo)
titulo.place(x=30, y=200)

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

videos1 = Entry(frame_div_verde, **estilo_entry)
videos1.place(x=30, y=240)

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
boton.place(x=30, y=320)

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
nuevo.place(x=185, y=320)
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
cancelar.place(x=340, y=320)


 


# Ejecutar el bucle principal de la aplicación
root.mainloop()
