from Proceso_importante import Navegar_Extraer_Subdominios_1, Extraer_Informacion_Subdominios_2, Uso_llm_local_consultas_3

def main(url_a_extraer_arr, num_paginas_extraer, etiquetas_a_extraer_funcion_arr, etiqueta_elemento_individual, dominio_principal,
         nombre_archivo_con_subdominios, nombre_archivo_scrap_todas_las_paginas, modelo_llm, format):
    print("Iniciando el proceso de extracción de subdominios...")
    resultado_navegacion = Navegar_Extraer_Subdominios_1.main(url_a_extraer_arr,
                                                               num_paginas_extraer,
                                                               etiquetas_a_extraer_funcion_arr,
                                                               etiqueta_elemento_individual,
                                                               dominio_principal)
    print(resultado_navegacion)
    print("Iniciando el proceso de extracción de información de subdominios...")
    resultado_extraccion = Extraer_Informacion_Subdominios_2.main(nombre_archivo_con_subdominios)
    print(resultado_extraccion)
    print("Iniciando el proceso de consultas a LLM...")
    resultado_consultas = Uso_llm_local_consultas_3.main(nombre_archivo_scrap_todas_las_paginas,
                                                           modelo_llm=modelo_llm, format=format)
    print(resultado_consultas)

if __name__ == "__main__":
    #Paso 1 parametros
    url_a_extraer = [
                                    ["https://www.freshproduce.com/resources/global-trade/","Global Trade"],
                                    ["https://www.freshproduce.com/resources/technology/","Technology"],
                                    ["https://www.freshproduce.com/resources/food-safety/","Food Safety"]
                                    ] # Ya viene con su respectivo etiquetado para identificar el subdominio
        
    num_paginas_extraer = 1 # Solo se ocupa extraer una página, la primera página.
    etiquetas_a_extraer_funcion=['search-stats', 'result-panel']
    etiqueta_elemento_individual='cta-area'
    dominio_principal="https://www.freshproduce.com"

    #Paso 2 parametros
    nombre_archivo_con_subdominios = "extracted_subdomains.csv"  # Nombre del archivo CSV donde se guardarán los subdominios extraídos

    #Paso 3 parametros
    nombre_archivo_scrap_todas_las_paginas = "scraped_data.csv"
    modelo_llm="llama3.2:3b"
    format = {
                        "type": "object",
                        "properties": {
                        "response": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": {
                            "type": "string"
                            }
                        }
                        },
                        "required": [
                        "response"
                        ]
                    }

    main(url_a_extraer,
         num_paginas_extraer,
         etiquetas_a_extraer_funcion,
         etiqueta_elemento_individual,
         dominio_principal,
         nombre_archivo_con_subdominios,
         nombre_archivo_scrap_todas_las_paginas,
         modelo_llm,
         format)