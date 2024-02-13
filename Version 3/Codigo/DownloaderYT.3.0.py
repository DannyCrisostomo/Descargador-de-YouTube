import sys
import os
import webbrowser
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import font, messagebox, filedialog
from tkinter import messagebox as MessageBox
from pytube import YouTube
import threading
import os
os.system("cls")

# Obtener la ruta del ejecutable o script
ruta_ejecutable = getattr(sys, '_MEIPASS', Path(os.path.dirname(os.path.abspath(__file__))))

# Variable global para controlar la cancelación de la descarga
thread_descarga = None  # Hilo utilizado para la descarga
descarga_cancelada = False  # Variable booleana que indica si la descarga ha sido cancelada

#Abrir Link
def abrir_github():
    webbrowser.open_new("https://github.com/DannyCrisostomo")
def abrir_linkedin():
    webbrowser.open_new("https://www.linkedin.com/in/danny-crisostomo/")

def descargar_video(enlace, carpeta_personalizada):
    """
    Descarga un video de YouTube y maneja la interfaz gráfica.

    Parameters:
        - enlace (str): El enlace del video de YouTube.
        - carpeta_personalizada (str): La carpeta de destino personalizada o None para usar la carpeta predeterminada.

    Global Variables:
        - descarga_cancelada (bool): Variable global que indica si la descarga ha sido cancelada.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para mostrar mensajes de éxito, error y cancelación.
        - Actualiza la interfaz gráfica según el estado de la descarga.

    Returns:
        None
    """
    global descarga_cancelada
    try:
        # Obtener información del video desde YouTube
        video = YouTube(enlace)

        # Obtener el directorio de trabajo actual
        directorio_actual = os.getcwd()

        # Inicializar las variables
        carpeta_destino = ""
        extension = ""

        # Determinar el tipo de descarga (video o audio)
        if seleccion.get() == 1:  # Descargar video
            carpeta_destino = carpeta_personalizada or os.path.join(directorio_actual, "Video")
            descarga = video.streams.get_highest_resolution()
            extension = "mp4"
        elif seleccion.get() == 2:  # Descargar audio
            carpeta_destino = carpeta_personalizada or os.path.join(directorio_actual, "Audio")
            os.makedirs(carpeta_destino, exist_ok=True)
            descarga = video.streams.filter(only_audio=True).first()
            extension = "mp3"
        else:
            # Manejar cualquier otro caso que pueda surgir
            messagebox.showerror("Error", "Selección no válida. Debe elegir entre Video o Música.")
            return

        # Obtener el título del video y limpiar caracteres no permitidos para nombres de archivos
        nombre_del_archivo = "".join(c for c in video.title if c.isalnum() or c.isspace())

        # Construir la ruta completa para guardar el archivo
        ruta_archivo = os.path.join(carpeta_destino, nombre_del_archivo + f".{extension}")

        # Descargar el archivo en la ruta especificada y con nombre aleatorio
        descarga.download(output_path=carpeta_destino, filename=nombre_del_archivo + f".{extension}")

        # Mostrar mensaje de descarga solo si no se ha cancelado
        if not descarga_cancelada:
            messagebox.showinfo("Éxito", f"Descarga completada exitosamente. Archivo guardado en {ruta_archivo}")
        else:
            # Acciones a realizar en caso de descarga cancelada
            video_temp_path = os.path.join(carpeta_destino, ruta_archivo)
            os.remove(video_temp_path)
            messagebox.showinfo("Cancelado", "Descarga cancelada. Acciones adicionales realizadas.")
            cancelar.config(state=NORMAL)

    except Exception as e:
        """  Maneja las excepciones que pueden ocurrir durante la descarga del video.
        Parameters:
            - e (Exception): La excepción capturada durante la descarga.
        Global Variables:
            - descarga_cancelada (bool): Variable global que indica si la descarga ha sido cancelada.
        Interfaz Gráfica:
            - Utiliza la biblioteca tkinter para mostrar un mensaje de error si la descarga falla.
        Returns:
            None  """
        if not descarga_cancelada:
            messagebox.showerror("Error", f"Error al descargar el video:\n{str(e)}")

    finally:
        """ Restaura el estado del botón después de la finalización de la descarga.
        Interfaz Gráfica:
            - Utiliza la biblioteca tkinter para habilitar nuevamente el botón.
        Returns:
            None """
        boton.config(state=NORMAL)


def accion():
    """
    Inicia el proceso de descarga del video de YouTube al hacer clic en el botón de descarga.

    Global Variables:
        - descarga_cancelada (bool): Variable global que indica si la descarga ha sido cancelada.
        - thread_descarga (Thread): Variable global que almacena la referencia al hilo de descarga.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para mostrar mensajes de advertencia, información y deshabilitar el botón durante la descarga.

    Returns:
        None
    """
    global descarga_cancelada, thread_descarga

    # Obtener el enlace del video y la carpeta personalizada
    enlace = URL_YT.get()
    carpeta_personalizada = ruta_carpeta.get()

    if enlace:
        # Verificar si no hay otro hilo de descarga en ejecución
        if not thread_descarga or not thread_descarga.is_alive():
            # Deshabilitar el botón mientras se realiza la descarga
            boton.config(state=DISABLED)

            # Reiniciar la variable de cancelación
            descarga_cancelada = False

            # Crear un hilo para la descarga y ejecutarlo
            thread_descarga = threading.Thread(target=descargar_video, args=(enlace, carpeta_personalizada))
            thread_descarga.start()
        else:
            # Acciones a realizar si hay otro hilo de descarga en curso
            boton.config(state=DISABLED)
            MessageBox.showinfo("Descarga", "Estás realizando una nueva descarga.")

    else:
        # Mostrar advertencia si no se ingresa un enlace antes de intentar descargar
        MessageBox.showwarning("Advertencia", "Por favor, ingresa un enlace antes de intentar descargar.")


def cancelar_descarga():
    """
    Cancela la descarga en curso y restaura el estado del botón después de la cancelación.

    Global Variables:
        - descarga_cancelada (bool): Variable global que indica si la descarga ha sido cancelada.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para deshabilitar el botón durante la cancelación y mostrar un mensaje informativo.

    Returns:
        None
    """
    global descarga_cancelada
    descarga_cancelada = True

    if descarga_cancelada:
        # Deshabilitar el botón durante la cancelación
        cancelar.config(state=DISABLED)

        # Mostrar mensaje informativo durante la cancelación
        messagebox.showinfo("Cancelado", "La descarga se está cancelando. Por favor, espere unos momentos.")

    # Habilitar nuevamente el botón después de cancelar
    boton.config(state=NORMAL)



def limpiar_entry():
    """
    Limpia el contenido del campo de entrada (Entry) en la interfaz gráfica.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para borrar el contenido del campo de entrada.

    Returns:
        None
    """
    URL_YT.delete(0, END)

def seleccionar_carpeta():
    """
    Abre un cuadro de diálogo para seleccionar una carpeta y actualiza el campo de entrada con la ruta seleccionada.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter y filedialog para abrir un cuadro de diálogo de selección de carpeta.
        - Actualiza el campo de entrada con la ruta de la carpeta seleccionada.

    Returns:
        None
    """
    carpeta_seleccionada = filedialog.askdirectory()

    # Borrar el contenido actual del campo de entrada
    ruta_carpeta.delete(0, tk.END)

    # Insertar la nueva ruta de la carpeta seleccionada en el campo de entrada
    ruta_carpeta.insert(0, carpeta_seleccionada)


# Diseño del Software

# Crear la ventana principal
root = Tk()
root.title("Descargador de Videos de YouTube")

# Configurar el tamaño de la ventana
ancho_ventana = 640
alto_ventana = 400

# Calcular las coordenadas x e y para centrar la ventana
x_pos = (root.winfo_screenwidth() - ancho_ventana) // 2
y_pos = (root.winfo_screenheight() - alto_ventana) // 2

# Establecer la geometría de la ventana para centrarla en la pantalla
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Bloquear el redimensionamiento de la ventana
root.resizable(False, False)

# Crear dos divisiones (Frames)
frame_div_verde = Frame(root, bg="#000000", width=640, height=500)
frame_div_verde.grid(row=0, column=1, padx=0, pady=0)

# Estructuras
menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Para más información", menu=helpmenu)
helpmenu.add_command(label="GitHub", command=abrir_github)
helpmenu.add_command(label="Linkedin", command=abrir_linkedin)
helpmenu.add_command(label="Autor", command=lambda: MessageBox.showinfo("Autor", "Danny Crisostomo Curi"))
helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 3.0.0"))
menubar.add_command(label="Salir", command=root.destroy)
# Opciones para descargar video o música
seleccion = tk.IntVar()
# Variable para la selección de contenido
seleccion_var = tk.IntVar()

# Estilo del titulo
estilo_titulo = {
    "font": font.Font(family="Georgia", size=45, weight="bold"),
    "bg": "#000000",
    "fg": "#E91E63",
    "anchor": "center",
    "text": "DOWNLOAD",
}
LOGO = tk.Label(frame_div_verde, **estilo_titulo)
LOGO.place(x=110, y=10)

#Ruta de direccion de carpeta label
texto1 = {
    "font": font.Font(family="Georgia", size=13, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "anchor": "center",
    "text": "Carpeta personalizada:",
}
texto1 = tk.Label(frame_div_verde, **texto1)
texto1.place(x=30, y=110)

#Ruta de direccion de carpeta
ruta_carpeta= {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3498db",  # Fondo oscuro con opacidad
    "fg": "white",  # Texto en color blanco
    "bd": 2,  # Ancho del borde
    "relief": "flat",  # Sin relieve en el borde
    "insertbackground": "#01579b",  # Color del cursor (azul oscuro)
}
ruta_carpeta = tk.Entry(frame_div_verde, **ruta_carpeta)
ruta_carpeta.place(x=30, y=140)

# Radiobuton de video
radio_video = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "width": 15,
    "height": 2,
    "bg": "#f54ba0",
    "fg": "black",
    "bd": 0,
    "relief": "solid",
}
radio_video = tk.Radiobutton(frame_div_verde, **radio_video, variable=seleccion, text="Video", value=1)
radio_video.place(x=30, y=190)

# Seleccionar Carpeta
boton_seleccionar_carpeta = {
    "font": font.Font(family="Helvetica",  size=12, weight="bold"),
    "width": 17,
    "height": 2,
    "bg": "#edbf7e",
    "fg": "white",
    "bd": 0,
    "relief": "solid",
}
boton_seleccionar_carpeta = tk.Button(frame_div_verde,**boton_seleccionar_carpeta, text="Seleccionar Carpeta", command=lambda: seleccionar_carpeta())
boton_seleccionar_carpeta.place(x=230, y=190)

# Radiobuton de musica
radio_audio = {
    "font": font.Font(family="Helvetica",  size=12, weight="bold"),
    "width": 15,
    "height": 2,
    "bg": "#be74e3",
    "fg": "black",
    "bd": 0,
    "relief": "solid",
}
radio_audio = tk.Radiobutton(frame_div_verde, **radio_audio,  variable=seleccion,  text="Música" , value=2)
radio_audio.place(x=430, y=190)

# Ingrese link de youtuve label
texto2 = {
    "font": font.Font(family="Georgia", size=13, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "anchor": "center",
    "text": "Ingrese link del vídeo de YouTube:",
}
texto2 = tk.Label(frame_div_verde, **texto2)
texto2.place(x=30, y=250)

# Estilo del Entry de link youtuve
estilo_entry = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3498db",  # Fondo oscuro con opacidad
    "fg": "white",  # Texto en color blanco
    "bd": 2,  # Ancho del borde
    "relief": "flat",  # Sin relieve en el borde
    "insertbackground": "#01579b",  # Color del cursor (azul oscuro)
}
URL_YT= tk.Entry(frame_div_verde, **estilo_entry)
URL_YT.place(x=30, y=280)

# Estilo del boton
estilo_boton = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Descargar",
    "command": accion,
    "width": 17,
    "height": 2,
    "bg": "#3498db",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
boton = Button(frame_div_verde, **estilo_boton)
boton.place(x=30, y=330)


# Estilo del boton nuevo
estilo_botonNuevo = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Nuevo",
    "command": limpiar_entry,
    "width": 17,
    "height": 2,
    "bg": "#8eeddd",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
nuevo = tk.Button(frame_div_verde, **estilo_botonNuevo)
nuevo.place(x=230, y=330)

# Estilo del boton cancelar
estilo_botonCancelar = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Cancelar",
    "command": cancelar_descarga,
    "width": 17,
    "height": 2,
    "bg": "#e74c3c",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
cancelar = tk.Button(frame_div_verde, **estilo_botonCancelar)
cancelar.place(x=430, y=330)

# Ejecutar el bucle principal de la aplicación
root.mainloop()