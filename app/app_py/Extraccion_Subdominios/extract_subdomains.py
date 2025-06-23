import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from webScrapping import webScrap


# Verifica si la página HTML indica que es la última página de resultados.
def bool_is_final_page(HTML, etiqueta='search-stats'):
    search_stats = HTML.find(class_=etiqueta)
    if search_stats:
        search_stats_arreglo = search_stats.text.split()
        indice_palabra_of = search_stats_arreglo.index("of")
        ultimo_elemento_de_pagina = int(search_stats_arreglo[indice_palabra_of - 1])
        total_elementos_de_pagina = int(search_stats_arreglo[indice_palabra_of + 1])
        return (ultimo_elemento_de_pagina >= total_elementos_de_pagina) #No debería haber más elementos en la página web, pero el método == puede fallar si hay un error en la web.
    return True # Si no se encuentra la clase, asumimos que es la última página para evitar errores en el bucle de paginación.

def obtener_subdominios(HTML, etiqueta_completa_todos_elementos = 'result-panel' ,etiqueta_elemento_individual='cta-area', dominio_principal="https://www.freshproduce.com"):
    result_panel_subdominio = HTML.find(class_=etiqueta_completa_todos_elementos) 
    if not result_panel_subdominio:
        print(f"No se encontró la clase '{etiqueta_completa_todos_elementos}' en el HTML.")
        return []
    subdominios = []
    encontrar_todos_los_hipervinculos = result_panel_subdominio.find_all('div', class_=etiqueta_elemento_individual)
    for enlace in encontrar_todos_los_hipervinculos:
        a_tag = enlace.find('a')
        if a_tag and 'href' in a_tag.attrs:
            subdominio_completo = f"{dominio_principal}{a_tag['href']}"
            subdominios.append(subdominio_completo)
    
    return subdominios

def extraccion_de_subdominios(url_a_extraer, numero_de_paginas_maximo_a_extraer=1, etiquetas_a_extraer_funcion=['search-stats', 'result-panel'], etiqueta_elemento_individual='cta-area', dominio_principal="https://www.freshproduce.com"):
    paginas_a_extraer = []  # Lista para almacenar las URLs de las páginas a extraer
    for (url, etiqueta) in url_a_extraer: #Separacion de URL y etiqueta para la extracción
        for i in range(0,numero_de_paginas_maximo_a_extraer):
            url_pagina = f"{url}?pageNumber={i}"
            print(f"URL de la página actual a extraer: {url_pagina}")
            Extraccion_HTML_dinamico = webScrap.scrape_website_with_dynamic_content(url_pagina, classes_to_wait=etiquetas_a_extraer_funcion, ID_OR_CLASS='CLASS')

            etiqueta_completa_todos_elementos = etiquetas_a_extraer_funcion[1]
            subdominios_en_pagina = obtener_subdominios(Extraccion_HTML_dinamico, etiqueta_completa_todos_elementos,etiqueta_elemento_individual, dominio_principal)
            for subdominio in subdominios_en_pagina:
                #print(subdominio)
                paginas_a_extraer.append([subdominio, etiqueta])  # Agregar la URL de la página a la lista y su etiqueta asociada
            etiqueta_busqueda_numeroElementos = etiquetas_a_extraer_funcion[0]
              
            # Verificar si se ha alcanzado la última página
            if bool_is_final_page(Extraccion_HTML_dinamico, etiqueta_busqueda_numeroElementos):
                print("Se ha alcanzado la última página. Terminando la extracción.")
                break
    print("Páginas extraidas:", len(paginas_a_extraer))
    return paginas_a_extraer
