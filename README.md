# Sistema básico de gestión de ficheros con Flask y Jinja2

Esta aplicación permite subir, listar, eliminar y descargar ficheros a través de una interfaz basada en templates de Jinja2, se puede encontrar en localhost:8001.
Utiliza Flask-user y Flask-SQLAlchemy (sqlite) para la gestión de los usuarios y sus sesiones. Además de los usuarios, se pueden crear usuarios con permisos de administración que pueden operar sobre todos los ficheros que hay en el sistema.

Para instalar la aplicación se deben seguir estos pasos:
1. Descargar el código del repositorio.
2. Instalar las dependencias del proyecto, para ello:
  - Recomiendo utilizar un entorno virtual, yo uso pyenv. [Introducción a pyenv](https://realpython.com/intro-to-pyenv/)
  - Para generar el entorno virtual: pyenv virtualenv <versión_python> <nombre_entorno>. Para el desarrollo se ha usado python 3.9.0
  - Una vez generado el entorno, en la carpeta del proyecto, ejecutar: pip install -r requirements.txt
3. Modificar el fichero settings.ini, poniendo la flask-key **(Debe permanecer en secreto)**, y las rutas a la DB de sqlite(incluido el nombre de ésta) y a la carpeta dónde se alojarán los ficheros subidos por los usuarios.
4. El usuario administrador es opcional, si se desea crear hay que ejecutar el script create_admin.py (python create_admin.py).

Una vez instalado, se ejecuta el script app.py y listo.

Para ejecutarlo como un contenedor de docker hay que seguir los siguientes pasos:
1. Ir al directorio que contiene el fichero dockerfile.
2. Contruir la imagen: docker build <-t tag_para_la_imagen> . 
3. Lanzar el contenedor: docker run -dit -p 8001:8001 --name <nombre_contenedor> -v <Ruta_al_directorio_ficheros>:/sfms/files_storage/ -v <ruta_al_directorio_donde_almacenar_la_db>:/sfms/db  <tag_de_la_imagen>

Una vez en la interfaz tenemos un menú de navegación con las opciones Home, Files y Log out:
- Home nos llevará a la página de inicio.
- Files nos llevará a la página de gestión de ficheros que consta de dos elementos:
  1. A la izquierda el listado con la información de cada fichero: Título, fecha de creación, tamaño, y su hash. 
Debajo de cada fichero dos botones para descargar y eliminar, y al final del todo los botones next_page y prev_page, que nos permitirá navegar por todos los ficheros, mostrando 8 por página.
  2. A la derecha, el formulario para subir un nuevo fichero.
- Log out nos permite cerrar la sesión de usuario.

Errores conocidos: <br>
Durante las pruebas me he dado cuenta de que es posible que cuándo borramos un contenedor y ejecutamos la app desde otro, surja este error:         
*AttributeError: 'NoneType' object has no attribute 'password'*
Para resolverlo debemos acceder a las cookies de sesión y borrarlas:
- En Firefox: 
  - Abrir la consola con F12, ir a la pestaña de almacenamiento y en cookies, botón derecho -> eliminar todo.
- En Chrome:
  -  Abrir la consola con F12, ir a la pestaña de aplicación y pulsar en *limpiar los datos del sitio.*
 
# Simple File Management System with Flask and Jinja2

This app allows users to upload, list, download and delete files through an interface based on Jinja2 templates, which is located at localhost:8001.
The app use Flask-User and Flask-SQLAlchemy (sqlite) to manage users and their sessions. Also, there users with admin permissions so they can handle all files in the system.

To install the app, follow the next steps:
1. Download the code.
2. Install the dependencies:
  - I highly recommend to use a virtual environment, I usually use pyenv. [Pyenv introduction.](https://realpython.com/intro-to-pyenv/)
  - To generate the environment: pyenv virtualenv <versión_python> <nombre_entorno>. For this development, I've used python 3.9.0.
  - Once the environment has been generated, inside the project's folder, execute: pip install -r requirements.txt
3. Modify the settings.ini file, setting the flask key **(keep this key in secret!)**, the sqlite's DB path (including its name), and the path to the folder where files will be storage.
4. Admin user is optional, if you want to have one, execute the script named create_admin.py (python create_admin.py).

When the app is already installed, execute the app.py script and ready!

To execute the app inside a docker's container follow these steps:
1. Open a shell inside the project's directory.
2. Build the docker's image using: docker build <-t image_tag> .
3. Run the container: docker run -dit -p 8001:8001 --name <container_name> -v <path_to_files_storage_directoy_in_the_host>:/sfms/files_storage/ -v <path_to_db_directoy_in_the_host>:/sfms/db <image_tag>

Once, you connect to the interface using your browser, you'll see the next elements:
- Home will take to the main page.
- Files which will take you first to the log in or register views and then to the files management view which have two parts:
  - At the left side the user's file list with the detail of each file: Title, creation date, size and its hash. Below each one, you have two buttons, download and eliminate, and at the bottom two additional buttons, next_page and prev_page, which allows you to navigate between files, showing 8 per page.
  - At the right side, you've the file uploading form.
- Log out get your user's session off.

Known errors:
I realized that there's the possibility that if you delete the current docker container before log out, and then you execute the app from another container, then you'll get an error like this one: *AttributeError: 'NoneType' object has no attribute 'password*.
This solve this error you've to get rid off the session cookies.
- With Firefox:
  - Open the console with F12, go to storage section, and in cookies, press right mouse button and then select *remove all*.
- With Chrome:
  -   Open the console with F12, go to application section, and select *clear site data*

