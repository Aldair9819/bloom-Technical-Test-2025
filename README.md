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
`docker compose -f docker-compose-cpu.yml up --build`


### Problemas con usar docker porque no encuentra el archivo:
Para la utilización de docker es necesario abrir la terminal en la misma carpeta donde están los archivos de docker, sino los comandos no funcionarán.
### Acceder al contenedor
http://localhost:8889/

http://127.0.0.1:8889/

La contraseña es la puesta en el .env definida como JUPYTER_TOKEN

**Nota:** el archivo `.envExample`  es un ejemplo para utilizarlo en el proyecto. Solo cambiar el nombre a `.env` y modificar los datos que se requieran. La contraseña por defecto sin modificar el .envExample es **contrasena_segura**

## Correr los scripts .ipynb local (No recomendado)
1. Tener instalado python 3.10
2. Tener instalado Ollama localmente. Por defecto Ollama utiliza el puerto 11434, por lo que dejar libre el puerto para ello. Y en el .env ponerlo como `URL_OLLAMA=http://localhost:11434`
3. Tener instalado navegador Google Chrome
4. Tener conda, anaconda, venv o forma de crear un ambiente para el programa
5. Con el ambiente creado, activar el ambiente para que las librerías a uardar se guarden en el ambiente y no en el ambiente global
6. En la terminal utilizar el comando `pip install -r requirements.txt`
7. En la terminal utilizar el comando `pip install notebook`. Esto porque el archivo **requirements.txt** no posee la librería por el Dockerfile que lo incluye por defecto.


**Nota:** El repositorio está hecho para correr con Docker. Se ha compilado en local y funciona, pero se recomienda correrlo en modo contenedor para evitar problemas de dependencias.

## Notebooks o programas en formato librera en python
### documentation
#### ollama_connection
Ollama es una herramienta de código abierto que permite ejecutar LLM localmente en la computadora.

En la notebook se muestran los comandos para descargar un modelo (pull), ver los modelos descargados (tags), generar texto mediante un prompt (generate) sea con rúbrica o no.

#### webScrapping

- Beautiful soup es una librería de python diseñada para analizar documentos HTML, con lo que se puede extraer información de páginas web de manera eficiente.
- Selenium son herramientas de código abierto diseñadas para automatizar navegadores web. Su función en el Web scrapping es para extraer el contenido HTML de una página web que posea contenido dinámico que no se puede extraer con una simple petición HTTPS

En la notebook se muestran comandos para encontrar etiquetas en particular con Beautiful Soup, y para el uso de Selenium y la espera de carga sobre un contenido dinámico.
### App
#### app
Mediante el conocimiento recopilado, se utilizan técnicas de extracción de contenido HTML de páginas web, obteniendo subdominios que en conjunto con el dominio principal forman enlaces directos a páginas web con contenido a extraer. Además viene el uso de una LLM local mediante Ollama.