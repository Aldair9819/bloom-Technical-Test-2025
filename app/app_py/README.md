# bloom-Technical-Test-2025
Examen técnico de Bloom. Web Scrapping y análisis de texto mediante LLM.
Script en python

## Dockerfile y docker-compose.yml

Contenedores para la facilidad de trabajo en entornos distintos de trabajo (Windows, Linux, MacOS) tipo X64

### Dockerfile
- Se toma una imagen que contiene python 3.10.18 slim
- Se usa usuarios Root (tema de permisos en Linux)
- Instalación de ping para revisión de contenedores en la misma red
- La carpeta por defecto en el contenedor es /app
- Copia el archivo requirements.txt a la carpeta por defecto
- Actualiza pip para encontrar librerías actualizadas
- Instala sin dejar residuos de caché todas las librerías de requirements.txt
- Comando que está por defecto: `python -u` 
- Comando opcional por defecto: `app.py` (Esto permite ejecutar un archivo diferente)

### docker-compose.yml
- Microservicio de un archivo de python
- Microservicio para el uso sencillo de LLMS de manera local.
**Nota:** Ninguno abre puertos. Se comunican mediante una red interna en docker

### docker-compose-cpu.yml
- Todo lo definido en docker-compose.yml, con la diferencia de solo usar CPU en lugar de GPU dedicada

### Comandos para el uso con Docker.
#### con GPU
`docker compose up --build`

#### sin GPU
`docker compose -f docker-compose-cpu.yml up --build`


### Problemas con usar docker porque no encuentra el archivo:
Para la utilización de docker es necesario abrir la terminal en la misma carpeta donde están los archivos de docker, sino los comandos no funcionarán.

**Nota:** el archivo `.envExample`  es un ejemplo para utilizarlo en el proyecto. Solo cambiar el nombre a `.env` y modificar los datos que se requieran.


## Correr los scripts .py local (No recomendado)
1. Tener instalado python 3.10
2. Tener instalado Ollama localmente. Por defecto Ollama utiliza el puerto 11434, por lo que dejar libre el puerto para ello. Y en el .env ponerlo como `URL_OLLAMA=http://localhost:11434`
3. Tener instalado navegador Google Chrome
4. Tener conda, anaconda, venv o forma de crear un ambiente para el programa
5. Con el ambiente creado, activar el ambiente para que las librerías a uardar se guarden en el ambiente y no en el ambiente global
6. En la terminal utilizar el comando `pip install -r requirements.txt`

**Nota:** El repositorio está hecho para correr con Docker. Se ha compilado en local y funciona, pero se recomienda correrlo en modo contenedor para evitar problemas de dependencias.

## Carpetas
Explicacion de lo que contiene cada carpeta
### Extraccion_Subdominios
Contiene programa para la extracción de los subdominios de una página web.
### LLM_Consulta
Contiene lo necesario para hacer peticiones API a Ollama y acceder a una LLM local

### ollama_data
El registro de los modelos LLM guardados localmente mediante Ollama

### Proceso_importante
Contiene los scripts de los tres pasos principales (El primer paso está divido en dos). A su vez cada uno se puede ejecutar individualmente por si se ocupa solo una parte del proceso

### webScrapping
Contiene las funciones para hacer webscrapping mediante Selenium o Beautiful soup

### APP_PY
Contiene los archivos Docker para configurar un entorno de trabajo. A su vez contiene el archivo app.py que ejecuta todo lo contenido en la carpeta **Proceso_importante**, y es donde se guardan los archivos .csv cuando se generan.