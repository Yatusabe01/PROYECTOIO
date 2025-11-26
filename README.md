# FLUJO-MAXIMO
Proyecto de IO

# ORGANIZACION DE CARPETAS
.web:
Contiene las dependencias y archivos generados por Reflex para construir el frontend. No se debe borrar ni modificar manualmente.

app:
Aqui se encuentra el archivo principal de la aplicacion (app.py) y los componentes relacionados con la interfaz y las paginas.

assets:
Carpeta destinada a guardar archivos estaticos como imagenes o recursos adicionales.

matriz:
Logica que estamos implementando. En el futuro esta carpeta sera eliminada.

services:
Servicios auxiliares como validaciones y funciones de apoyo.

# RECOMENDACIONES PARA EL TRABAJO DEL PROYECTO
Para trabajar el proyecto sin afectar el sistema y sin subir librerias al repositorio, se recomienda usar un entorno virtual.


# RECONSTRUIR EL ENTORNO EN OTRO EQUIPO
1. Clonar el proyecto
2. Crear y activar un entorno virtual(Las instrucciones para hacerlo estan abajo)
3. Instalar dependencias:
    pip install -r requirements.txt

# CREAR UN ENTORNO VIRTUAL
Pasos para crearlo en Windows:
1. Abrir CMD o PowerShell en la carpeta del proyecto.
2. Crear el entorno virtual:
    python -m venv venv
3. Activarlo:
    venv\Scripts\activate
4. Verificar que aparece (venv) al inicio de la linea de comandos.

# COMO ACTUALIZAR EL requirements.txt
1. Instalar una libreria:
    pip install nombre_libreria
2. Actualizar el archivo:
    pip freeze > requirements.txt

# EJECUTAR EL PROYECTO
reflex run

