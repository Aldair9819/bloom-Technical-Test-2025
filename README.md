# bloom-Technical-Test-2025
Examen técnico de Bloom. Web Scrapping y análisis de texto mediante LLM

## Dockerfile y docker-compose.yml

Contenedores para la facilidad de trabajo en entornos distintos de trabajo (Windows, Linux, MacOS) tipo X64

### Dockerfile
- Se toma una imagen que contiene python 3.10 con lo esencial para trabajos en jupyter.
- Se usa usuarios Root (tema de permisos en Linux)
- Instalación de ping para revisión de contenedores en la misma red, y git para la utilización de github dentro del contenedor.
- La carpeta por defecto en el contenedor es /app
- Copia el archivo requirements.txt a la carpeta por defecto
- Actualiza pip para encontrar librerías actualizadas
- Instala sin dejar residuos de caché todas las librerías de requirements.txt
- Expone el puerto 8889 dentro de la red. Por si el mapeo de puertos no funciona correctamente.
- Comando inicial del contenedor como si fuera colocado en CMD: `jupyter notebook --ip=0.0.0.0 --port=8889 --allow-root --no-browser`

### docker-compose.yml
- Microservicio de un jupyter notebook que depende de ollama, utiliza nvidia y utiliza una red interna para conectarse.
- Microservicio para el uso sencillo de LLMS de manera local.

### docker-compose-cpu.yml
- Todo lo definido en docker-compose.yml, con la diferencia de solo usar CPU en lugar de GPU dedicada

### Comandos para el uso con Docker.
#### con GPU
`docker compose up --build`

#### sin GPU
`docker compose -f docker-compose-cpu.yml up`

### Problemas con usar docker porque no encuentra el archivo:
Para la utilización de docker es necesario abrir la terminal en la misma carpeta donde están los archivos de docker, sino los comandos no funcionarán.
### Acceder al contenedor
http://localhost:8889/

http://127.0.0.1:8889/

La contraseña es la puesta en el .env definida como JUPYTER_TOKEN

**Nota:** el archivo `.envExample`  es un ejemplo para utilizarlo en el proyecto. Solo cambiar el nombre a `.env` y modificar los datos que se requieran. La contraseña por defecto sin modificar el .envExample es **contrasena_segura**

## Correr los scripts .ipynb local
1. Tener instalado python 3.10
2. Tener conda, anaconda, venv o forma de crear un ambiente para el programa
3. Con el ambiente creado, activar el ambiente para que las librerías a guardar se guarden en el ambiente y no en el ambiente global
4. En la terminal utilizar el comando `pip install -r requirements.txt`
5. En la terminal utilizar el comando `pip install notebook`. Esto porque el archivo **requirements.txt** no posee la librería por el Dockerfile que lo incluye por defecto.

## Notebooks o programas en formato librera en python
### ollama_connection
Ollama es una herramienta de código abierto que permite ejecutar LLM localmente en la computadora.

En la notebook se muestran los comandos para descargar un modelo (pull), ver los modelos descargados (tags), generar texto mediante un prompt (generate) sea con rúbrica o no.

