# Descargador de YouTube 🎬

Este es un programa que permite a los usuarios registrados descargar videos de YouTube. La aplicación tiene una interfaz gráfica simple que permite a los usuarios registrarse e iniciar sesión.

## Características ✨

- **Inicio de sesión de usuario:** Los usuarios pueden iniciar sesión utilizando su nombre de usuario y contraseña registrados.
- **Registro de usuario:** Los nuevos usuarios pueden registrarse proporcionando un correo electrónico y una contraseña.
- **Descarga de videos de YouTube:** Una vez que los usuarios han iniciado sesión, pueden descargar videos de YouTube.

## Requisitos 📋

- Python 3.x
- Tkinter
- mysql-connector-python
- pytube

## Instalación 💻

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python 3.x instalado en tu sistema.
3. Instala las dependencias necesarias ejecutando `pip install -r requirements.txt`.
4. Configura la base de datos MySQL con las credenciales predeterminadas y el esquema `dowloaderyt.4.0` según se describe en el código.

## Uso 🚀

1. Ejecuta `python main.py` en tu terminal.
2. La aplicación se abrirá. Puedes iniciar sesión si ya tienes una cuenta o registrarte como nuevo usuario.
3. Una vez iniciada la sesión, podrás descargar videos de YouTube.

## Versiones 🔄

- **Versión 1:** Implementación inicial con funciones básicas, incluyendo un botón para descargar, un botón para limpiar la entrada, un botón para cancelar la descarga y un campo para la entrada de la URL.
  
![Descargador de YouTube](https://github.com/DannyCrisostomo/Descargador-de-YouTube/blob/26a3e4372d05ef7b310ed21f2cc9c463734d8e9b/Version%201/Imagen/DownloaderYT.1.0.png)

- **Versión 2:** Agregada la funcionalidad de descarga de videos y música de YouTube, manteniendo las funciones de la versión 1. Ahora los usuarios pueden descargar tanto videos como música desde YouTube.

- **Versión 3:** Se añadió un botón para seleccionar la carpeta de descarga y un campo de entrada para mostrar la ubicación de la carpeta seleccionada. Además, se mejoró la seguridad y se optimizó el rendimiento de la aplicación.

- **Versión 4:** Implementación de inicio de sesión y registro de usuarios, lo que permite a los usuarios guardar sus preferencias y acceder a la aplicación de manera personalizada. También se mantienen las mejoras de la versión 3 en seguridad y rendimiento.


## Autor 👨‍💻

Este proyecto fue creado por [Danny Crisostomo](https://github.com/DannyCrisostomo). Puedes encontrar más información sobre el autor en [LinkedIn](https://www.linkedin.com/in/danny-crisostomo/).

## Contribución 🤝

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia de mejora, por favor abre un nuevo issue o envía un pull request.

## Licencia 📄

Este proyecto está bajo la licencia [MIT](https://opensource.org/licenses/MIT).
