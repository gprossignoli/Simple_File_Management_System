# Sistema básico de gestión de ficheros con Flask y Jinja2

Esta aplicación permite subir, listar, eliminar y descargar ficheros a través de una interfaz basada en templates de Jinja2, se puede encontrar en localhost:8001.
Utiliza Flask-user y Flask-SQLAlchemy (sqlite) para la gestión de los usuarios y sus sesiones. Además de los usuarios, se pueden crear usuarios con permisos de administración que pueden operar sobre todos los ficheros que hay en el sistema.

Para instalar la aplicación se deben seguir estos pasos:
1. Descargar el código del repositorio.
2. Modificar el fichero settings.ini, poniendo la flask-key (Debe permanecer en secreto), y las rutas a la DB de sqlite(incluido el nombre de ésta) y la ruta a la carpeta dónde se alojarán los ficheros subidos por los usuarios.
3. El usuario administrador es opcional, si se desea crear hay que ejecutar el script create_admin.py (python create_admin.py).

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
Durante las pruebas me he dado cuenta de que es posible que cuándo borramos un contenedor y ejecutamos la app desde otro, de un problema con la password de usuario:         
*AttributeError: 'NoneType' object has no attribute 'password'*
Este problema se genera cuando eliminamos el contenedor sin haber cerrado sesión de usuario previamente. Para resolverlo debemos acceder a las cookies de sesión y borrarlas:
- En Firefox: 
  - Abrir la consola con F12, ir a la pestaña de almacenamiento y en cookies, botón derecho -> eliminar todo.
- En Chrome:
  -  Abrir la consola con F12, ir a la pestaña de aplicación y pulsar en *limpiar los datos del sitio.*


