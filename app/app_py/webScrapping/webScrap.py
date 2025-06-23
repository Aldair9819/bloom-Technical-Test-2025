import requests
from selenium import webdriver #Controlar google chrome para obtener HTML con contenido dinámico
from selenium.webdriver.chrome.options import Options #Controlar google chrome sin interfaz gráfica
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar elementos dinámicos
from selenium.webdriver.support import expected_conditions as EC  # Condiciones para la espera
from selenium.webdriver.common.by import By  # Para localizar elementos (por clase, ID, etc.)
from bs4 import BeautifulSoup # #Para parsear el HTML obtenido con selenium
import chromedriver_autoinstaller #Instalación automática del driver de Chrome


def scrape_website(url):
    # Realiza web scraping en la URL proporcionada. Extrae todo el HTML.

    try:
        print(f"Extrayendo HTML de: {url}")
        response = requests.get(url) # Realizar una solicitud HTTP GET a la URL
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP incorrectos (4xx o 5xx)

        # 2. Convierte el contenido obtenido a una estructura HTML con BeautifulSoup
        soup_html = BeautifulSoup(response.text, 'html.parser')
        print("Contenido HTML parseado exitosamente.")
        return soup_html

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la URL: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    return None  # Retorna None si ocurre un error


def scrape_website_with_dynamic_content(page, classes_to_wait = None, ID_OR_CLASS='CLASS'):
    # Instala automáticamente el chromedriver compatible con la versión de Chrome instalada
    print(f"Extrayendo HTML dinámico de: {page}")
    try:
        chromedriver_autoinstaller.install() 

        options = Options() # Configuraciones de opciones para el navegador
        options.add_argument("--headless") # Ejecuta chrome sin interfaz gráfica

        #Necesario por falta de permisos en el entorno aislado del contenedor
        options.add_argument("--no-sandbox") #Desactiva seguridad de Chrome por problemas de permisos en algunos sistemas
        
        options.add_argument("--disable-dev-shm-usage") #Prevenir fallos por falta de memoria (RAM) compartida en algunos sistemas. Usa memoria de disco duro.

        driver = webdriver.Chrome(options=options) # Inicia navegador chrome con las opciones configuradas

        driver.get(page) # Carga la página web en el navegador

        
        if classes_to_wait:
            tiempo_espera = 30 # Tiempo máximo de espera en segundos para que se cargue el contenido dinámico
            wait = WebDriverWait(driver, tiempo_espera)
            if ID_OR_CLASS.upper() == 'CLASS':
                for class_to_wait in classes_to_wait: #Recorre cada clase a esperar
                    wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, class_to_wait)) # Cambio a busqueda por clase
                    )# Espera cada una de las clases
            elif ID_OR_CLASS.upper() == 'ID':
                for id_to_wait in classes_to_wait: #Recorre cada ID a esperar
                    wait.until(
                        EC.presence_of_element_located((By.ID, id_to_wait)) #Cambio a busqueda por ID
                    )# Espera cada uno de los IDs
            else:
                raise ValueError("ID_OR_CLASS debe ser 'CLASS' o 'ID'.")  # Manejo de error si el parámetro no es válido
        html_completo = driver.page_source  # Obtención del HTML renderizado completo
        # Usar BeautifulSoup para parsear
        soup = BeautifulSoup(html_completo, "html.parser")
        driver.quit() #Cerrar navegador de Chrome
        print("Contenido HTML dinámico parseado exitosamente.")
        return soup

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la URL: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    return None  # Retorna None si ocurre un error