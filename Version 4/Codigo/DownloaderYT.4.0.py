import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import *
from tkinter import Entry, Frame, Tk, font
from tkinter import ttk
from pytube import YouTube
from tkinter import messagebox as MessageBox
import os
import webbrowser
from pathlib import Path
import threading
import sys
from tkinter import font, messagebox, filedialog

os.system("cls")

#Ver contraseñas
def Mostrar_Contraseña_registrar():
    current_state = mostrar_contraseña_registrar.get()
    # Cambiar entre mostrar y ocultar el texto de la contraseña
    entry_nueva_contraseña.config(show="" if current_state else "*")
    entry_nueva_contraseña_confirmacion.config(show="" if current_state else "*")

def Mostrar_Contraseña_login():
    current_state = mostrar_contraseña_login.get()
    # Cambiar entre mostrar y ocultar el texto de la contraseña
    entry_contraseña.config(show="" if current_state else "*")

#Abrir Link
def abrir_github():
    webbrowser.open_new("https://github.com/DannyCrisostomo")
def abrir_linkedin():
    webbrowser.open_new("https://www.linkedin.com/in/danny-crisostomo/")

#Conexion login Usuario
def login():
    """
    Realiza la validación de usuario mediante la conexión a una base de datos MySQL.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para mostrar mensajes informativos y de error.

    Database Connection:
        - Se conecta a una base de datos MySQL local con credenciales predeterminadas.

    Parameters:
        None

    Returns:
        None
    """
    # Obtener el usuario y la contraseña desde la interfaz gráfica
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    try:
        # Verificar si se ingresaron credenciales
        if not usuario or not contraseña:
            messagebox.showinfo("Error!", "Ingrese sus credenciales.")
            return

        # Establecer la conexión a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="dowloaderyt.4.0"
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Consultar la base de datos para verificar las credenciales del usuario
        cursor.execute("SELECT * FROM login WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        resultado = cursor.fetchone()

        # Verificar el resultado de la consulta y mostrar mensajes correspondientes
        if resultado:
            abrir_segunda_ventana()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    except mysql.connector.Error as err:
        # Mostrar mensaje de error en caso de problemas de conexión a la base de datos
        messagebox.showerror("Error de conexión", f"Error: {err}")

    finally:
        # Cerrar cursor y conexión después de la ejecución
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

#Conexion Registrar Usuario
def registrar():
    """
    Registra un nuevo usuario en la base de datos MySQL después de validar la información proporcionada.

    Interfaz Gráfica:
        - Utiliza la biblioteca tkinter para mostrar mensajes informativos y de error.

    Database Connection:
        - Se conecta a una base de datos MySQL local con credenciales predeterminadas.

    Parameters:
        None

    Returns:
        None
    """
    # Obtener la información del nuevo usuario desde la interfaz gráfica
    nuevo_usuario = entry_nuevo_usuario.get()
    nueva_contraseña = entry_nueva_contraseña.get()
    confirmacion_contraseña = entry_nueva_contraseña_confirmacion.get()

    try:
        # Verificar si los campos obligatorios no están vacíos
        if not nuevo_usuario or not nueva_contraseña or not confirmacion_contraseña or nuevo_usuario == entry_nuevo_usuario.placeholder or nueva_contraseña == entry_nueva_contraseña.placeholder or confirmacion_contraseña == entry_nueva_contraseña_confirmacion.placeholder:
            messagebox.showinfo("Error!", "Todos los campos deben estar completos.")
            return

        # Verificar si el nuevo usuario tiene el dominio correcto
        dominios_obligatorios = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"]
        usuario_split = nuevo_usuario.split('@')
        if len(usuario_split) != 2 or usuario_split[1] not in dominios_obligatorios:
            messagebox.showinfo("Error!", f"El dominio del usuario debe ser uno de: {', '.join(dominios_obligatorios)}")
            return

        # Establecer la conexión a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="dowloaderyt.4.0"
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe en la base de datos
        if usuario_existente(nuevo_usuario):
            messagebox.showinfo("Error!", "El correo ya está vinculado. Elige otro correo para vincular.")
        elif nueva_contraseña != "":
            # Verificar si las contraseñas coinciden
            if nueva_contraseña == confirmacion_contraseña:
                # Insertar el nuevo usuario y contraseña en la base de datos
                cursor.execute("INSERT INTO login (usuario, contraseña) VALUES (%s, %s)", (nuevo_usuario, nueva_contraseña))
                conexion.commit()
                messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
                limpiar_entry()
            else:
                messagebox.showinfo("Error!", "Las contraseñas no coinciden")
        else:
            messagebox.showinfo("Error!", "La contraseña no puede estar vacía")

    except mysql.connector.Error as err:
        # Mostrar mensaje de error en caso de problemas de conexión a la base de datos
        messagebox.showerror("Error de conexión", f"Error: {err}")

    finally:
        # Cerrar cursor y conexión después de la ejecución
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

#Limpiar
def limpiar_entry():
    """
    Limpia el contenido de las entradas de usuario y contraseña en las ventanas de registro y login.

    Entradas:
        - Se asume que existen entradas llamadas `entry_usuario`, `entry_contraseña`, `entry_nueva_contraseña_confirmacion`,
          `entry_nueva_contraseña`, y `entry_nuevo_usuario` en las ventanas de registro y login.

    Funcionamiento:
        - Borra el contenido de las entradas de usuario y contraseña.

    Returns:
        None
    """
    entry_usuario.delete(0, tk.END)  # Borra el contenido de la entrada de usuario en la ventana de login
    entry_contraseña.delete(0, tk.END)  # Borra el contenido de la entrada de contraseña en la ventana de login
    entry_nueva_contraseña_confirmacion.delete(0, tk.END)  # Borra el contenido de la entrada de confirmación de contraseña en la ventana de registro
    entry_nueva_contraseña.delete(0, tk.END)  # Borra el contenido de la entrada de nueva contraseña en la ventana de registro
    entry_nuevo_usuario.delete(0, tk.END)  # Borra el contenido de la entrada de nuevo usuario en la ventana de registro

#Verifica si los usarios existen
def usuario_existente(usuario):
    """
    Verifica si un nombre de usuario ya existe en la base de datos MySQL.

    Database Connection:
        - Se conecta a una base de datos MySQL local con credenciales predeterminadas.

    Parameters:
        usuario (str): El nombre de usuario que se desea verificar en la base de datos.

    Returns:
        bool: True si el nombre de usuario ya existe, False si no existe o hay problemas de conexión.
    """
    try:
        # Establecer la conexión a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="dowloaderyt.4.0"
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Consultar la base de datos para verificar si el usuario existe
        cursor.execute("SELECT * FROM login WHERE usuario = %s", (usuario,))
        resultado = cursor.fetchone()

        # Devolver True si el usuario ya existe, False si no existe
        return resultado is not None

    except mysql.connector.Error as err:
        # Mostrar mensaje de error en caso de problemas de conexión a la base de datos
        messagebox.showerror("Error de conexión", f"Error: {err}")

    finally:
        # Cerrar cursor y conexión después de la ejecución
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

#Cambia las ventana
def cambiar_ventana():
    """
    Cambia entre las ventanas de registro y login.

    Ventanas:
        - Se asume que existen dos ventanas llamadas `ventana_login` y `ventana_registro`.

    Funcionamiento:
        - Si la ventana de login (`ventana_login`) está visible, la oculta y muestra la ventana de registro (`ventana_registro`).
        - Si la ventana de registro (`ventana_registro`) está visible, la oculta y muestra la ventana de login (`ventana_login`).

    Variables Globales:
        - Se asume que las variables globales `entry_nuevo_usuario`, `entry_nueva_contraseña`, y `entry_nueva_contraseña_confirmacion` están definidas.

    Returns:
        None
    """
    if ventana_login.state() == "normal":  # Si la ventana de login está visible
        ventana_login.withdraw()  # Oculta la ventana de login
        ventana_registro.deiconify()  # Muestra la ventana de registro
    else:
        ventana_registro.withdraw()  # Oculta la ventana de registro
        ventana_login.deiconify()  # Muestra la ventana de login

    # Variables globales relacionadas con las entradas de usuario y contraseña
    global entry_nuevo_usuario
    global entry_nueva_contraseña
    global entry_nueva_contraseña_confirmacion

#Agregar placeholder 
def agregar_placeholder(entry, placeholder_text):
    """
    Agrega un placeholder a un Entry en tkinter.

    Args:
        entry (tk.Entry): La entrada a la que se le agregará el placeholder.
        placeholder_text (str): El texto del placeholder.

    Returns:
        None
    """
    entry.insert(0, placeholder_text)
    entry.bind('<FocusIn>', lambda event: on_entry_click(entry, placeholder_text))
    entry.bind('<FocusOut>', lambda event: on_focus_out(entry, placeholder_text))
    entry.config(fg='#676767')  # Configura el color inicial del texto en gris
    entry.placeholder = placeholder_text  # Almacena el texto del Placeholder en una propiedad del Entry
def on_entry_click(entry, placeholder_text):
    """
    Función llamada cuando se hace clic en la entrada para manejar el evento FocusIn.

    Args:
        entry (tk.Entry): La entrada en la que se hizo clic.
        placeholder_text (str): El texto del placeholder.

    Returns:
        None
    """
    if entry.get() == entry.placeholder:
        entry.delete(0, "end")
        entry.config(fg='white')  # Cambia el color del texto a negro
def on_focus_out(entry, placeholder_text):
    """
    Función llamada cuando se pierde el foco de la entrada para manejar el evento FocusOut.

    Args:
        entry (tk.Entry): La entrada en la que se perdió el foco.
        placeholder_text (str): El texto del placeholder.

    Returns:
        None
    """
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg='#676767')  # Cambia el color del texto a gris

#Principal
ruta_ejecutable = getattr(sys, '_MEIPASS', Path(os.path.dirname(os.path.abspath(__file__))))
# Variable global para controlar la cancelación de la descarga
thread_descarga = None  # Hilo utilizado para la descarga
descarga_cancelada = False  # Variable booleana que indica si la descarga ha sido cancelada

def abrir_segunda_ventana():
    ventana_login.destroy()
    # Diseño del Software
    # Crear la ventana principal
    # Obtener la ruta del ejecutable o script
    #Abrir Link
# Función para mostrar información del usuario
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
    helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 4.0.0"))
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















# Crea la Ventana de Login
# Configuración de la ventana principal
ventana_login= tk.Tk()
# Configurar el tamaño de la ventana
ancho_ventana = 640
alto_ventana = 330
ventana_login.title("Ventana de Inicio")
# Configura el color de fondo 
ventana_login.configure(bg="#000000")
# Calcular las coordenadas x e y para centrar la ventana
x_pos = (ventana_login.winfo_screenwidth() - ancho_ventana) // 2
y_pos = (ventana_login.winfo_screenheight() - alto_ventana) // 2
# Establecer la geometría de la ventana para centrarla en la pantalla
ventana_login.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
# Bloquear el redimensionamiento de la ventana
ventana_login.resizable(False, False)
# Estructuras
menubar = Menu(ventana_login)
ventana_login.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Para más información", menu=helpmenu)
helpmenu.add_command(label="GitHub", command=abrir_github)
helpmenu.add_command(label="Linkedin", command=abrir_linkedin)
helpmenu.add_command(label="Autor", command=lambda: MessageBox.showinfo("Autor", "Danny Crisostomo Curi"))
helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 4.0.0"))
menubar.add_command(label="Limpiar", command=limpiar_entry)
menubar.add_command(label="Salir", command=ventana_login.destroy)

titulo = {
    "font": font.Font(family="Georgia", size=45, weight="bold"),
    "bg": "#000000",
    "fg": "#E91E63",
    "text": "Iniciar Sesión",
}
titulo = tk.Label(ventana_login, **titulo)
titulo.place(x=110, y=5)

etiqueta_usuario = {
    "font": font.Font(family="Georgia", size=15, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Correo:",
}
etiqueta_usuario = tk.Label(ventana_login, **etiqueta_usuario)
etiqueta_usuario.place(x=30, y=80)

entry_usuario = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3498db", 
    "fg": "white",  
    "bd": 2,  
    "relief": "flat", 
    "insertbackground": "#01579b",
}
entry_usuario = tk.Entry(ventana_login,**entry_usuario)
agregar_placeholder(entry_usuario , "admin@gmail.com")
entry_usuario.place(x=30, y=110)

etiqueta_contraseña = {
    "font": font.Font(family="Georgia", size=15, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Contraseña:",
}
etiqueta_contraseña = tk.Label(ventana_login, **etiqueta_contraseña)
etiqueta_contraseña.place(x=30, y=150)

entry_contraseña  = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3498db", 
    "fg": "white",  
    "bd": 2,  
    "relief": "flat", 
    "insertbackground": "#01579b",  
    "show":"*" # Muestra asteriscos en lugar de caracteres reales
}
entry_contraseña = tk.Entry(ventana_login, **entry_contraseña)  
agregar_placeholder(entry_contraseña, "***************************")
entry_contraseña.place(x=30, y=180)

checkbutton_mostrar_contraseña2  = {
    "bg": "#000000",
    "relief": "flat",
    "highlightthickness": 0,  
    "highlightcolor": "#000000"  
}
mostrar_contraseña_login = tk.BooleanVar()
checkbutton_mostrar_contraseña2 = tk.Checkbutton(ventana_login, **checkbutton_mostrar_contraseña2, variable=mostrar_contraseña_login, command=Mostrar_Contraseña_login)
checkbutton_mostrar_contraseña2.place(x=30, y=225)

etiqueta_checkbutton_mostrar_contraseña= {
    "font": font.Font(family="Georgia", size=12, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Mostrar Contraseña",
}
etiqueta_checkbutton_mostrar_contraseña = tk.Label(ventana_login, **etiqueta_checkbutton_mostrar_contraseña)
etiqueta_checkbutton_mostrar_contraseña.place(x=52, y=225)

boton_ingresar  = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Ingresar",
    "command": login,
    "width": 25,
    "height": 2,
    "bg": "#ff0050",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
boton_ingresar = tk.Button(ventana_login, **boton_ingresar)
boton_ingresar.place(x=50, y=267)

boton_registrar  = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Registrar",
    "command": cambiar_ventana,
    "width": 25,
    "height": 2,
    "bg": "#00c2ff",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
boton_registrar = tk.Button(ventana_login, **boton_registrar)
boton_registrar.place(x=330, y=267)




# Crea la Ventana de Registro
ventana_registro =tk.Toplevel(ventana_login)
ventana_registro.title("Ventana de Registro")
# Configura el color de fondo 
ventana_registro.configure(bg="#000000")
# Configurar el tamaño de la ventana
ancho_ventana = 640
alto_ventana = 400
# Calcular las coordenadas x e y para centrar la ventana
x_pos = (ventana_registro.winfo_screenwidth() - ancho_ventana) // 2
y_pos = (ventana_registro.winfo_screenheight() - alto_ventana) // 2
# Establecer la geometría de la ventana para centrarla en la pantalla
ventana_registro.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
# Bloquear el redimensionamiento de la ventana
ventana_registro.resizable(False, False)
# Oculta la ventana login
ventana_registro.withdraw() 
# Estructuras
menubar = Menu(ventana_registro)
ventana_registro.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Para más información", menu=helpmenu)
helpmenu.add_command(label="GitHub", command=abrir_github)
helpmenu.add_command(label="Linkedin", command=abrir_linkedin)
helpmenu.add_command(label="Autor", command=lambda: MessageBox.showinfo("Autor", "Danny Crisostomo Curi"))
helpmenu.add_command(label="Version", command=lambda: MessageBox.showinfo("Version", "Esta es la versión 4.0.0"))
menubar.add_command(label="Limpiar", command=limpiar_entry)
menubar.add_command(label="Salir", command=ventana_registro.destroy)

# Estilo del titulo
titulo = {
    "font": font.Font(family="Georgia", size=45, weight="bold"),
    "bg": "#000000",
    "fg": "#E91E63",
    "text": "Crear Cuenta",
}
titulo = tk.Label(ventana_registro, **titulo)
titulo.place(x=130, y=5)

etiqueta_nuevo_usuario = {
    "font": font.Font(family="Georgia", size=15, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Nuevo Correo:",
}
etiqueta_nuevo_usuario = tk.Label(ventana_registro, **etiqueta_nuevo_usuario)
etiqueta_nuevo_usuario.place(x=30, y=80)

entry_nuevo_usuario = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3fb0e3", 
    "fg": "white", 
    "bd": 2,  
    "relief": "flat", 
    "insertbackground": "#01579b"
}
entry_nuevo_usuario = tk.Entry(ventana_registro,**entry_nuevo_usuario)
agregar_placeholder(entry_nuevo_usuario, "admin@gmail.com")
entry_nuevo_usuario.place(x=30, y=110)

etiqueta_nueva_contraseña= {
    "font": font.Font(family="Georgia", size=15, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Nueva Contraseña:",
}
etiqueta_nueva_contraseña = tk.Label(ventana_registro,**etiqueta_nueva_contraseña)
etiqueta_nueva_contraseña.place(x=30, y=150)

entry_nueva_contraseña  = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3fb0e3", 
    "fg": "white",  
    "bd": 2,  
    "relief": "flat", 
    "insertbackground": "#01579b",  
    "show":"*"
}
entry_nueva_contraseña = tk.Entry(ventana_registro, **entry_nueva_contraseña)
agregar_placeholder(entry_nueva_contraseña, "***************************")
entry_nueva_contraseña.place(x=30, y=180)

etiqueta_confirmacion_contraseña= {
    "font": font.Font(family="Georgia", size=15, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Confirmar Contraseña:",
}
etiqueta_confirmacion_contraseña = tk.Label(ventana_registro, **etiqueta_confirmacion_contraseña)
etiqueta_confirmacion_contraseña.place(x=30, y=220)

entry_nueva_contraseña_confirmacion = {
    "font": font.Font(family="Arial", size=14, weight="bold"),
    "width": 52,
    "bg": "#3fb0e3", 
    "fg": "white",  
    "bd": 2,  
    "relief": "flat", 
    "insertbackground": "#01579b",  
    "show":"*"
}
entry_nueva_contraseña_confirmacion = tk.Entry(ventana_registro, **entry_nueva_contraseña_confirmacion)
agregar_placeholder(entry_nueva_contraseña_confirmacion, "***************************")
entry_nueva_contraseña_confirmacion.place(x=30, y=250)

checkbutton_mostrar_contraseña  = {
    "bg": "#000000",
    "relief": "flat",
    "highlightthickness": 0,  
    "highlightcolor": "#000000"  
}
mostrar_contraseña_registrar = tk.BooleanVar()
checkbutton_mostrar_contraseña = tk.Checkbutton(ventana_registro, **checkbutton_mostrar_contraseña, variable=mostrar_contraseña_registrar, command=Mostrar_Contraseña_registrar)
checkbutton_mostrar_contraseña.place(x=30, y=299)

etiqueta_checkbutton_mostrar_contraseña= {
    "font": font.Font(family="Georgia", size=12, weight="bold"),
    "bg": "#000000",
    "fg": "white",
    "text": "Mostrar Contraseña",
}
etiqueta_checkbutton_mostrar_contraseña = tk.Label(ventana_registro, **etiqueta_checkbutton_mostrar_contraseña)
etiqueta_checkbutton_mostrar_contraseña.place(x=52, y=299)




boton_registrar  = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Registrar",
    "command": registrar,
    "width": 25,
    "height": 2,
    "bg": "#ff0050",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
boton_registrar = tk.Button(ventana_registro, **boton_registrar)
boton_registrar.place(x=50, y=340)

cambiar_ventana1  = {
    "font": font.Font(family="Helvetica", size=12, weight="bold"),
    "text": "Iniciar Sesión",
    "command": cambiar_ventana,
    "width": 25,
    "height": 2,
    "bg": "#00c2ff",
    "fg": "#ffffff",
    "bd": 0,
    "relief": "solid",
}
cambiar_ventana1 = tk.Button(ventana_registro,**cambiar_ventana1)
cambiar_ventana1.place(x=330, y=340)
# Inicia el bucle principal de la ventana

ventana_login.mainloop()