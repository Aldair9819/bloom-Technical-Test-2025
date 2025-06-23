import sys
import os
import pandas as pd

# Agrega las rutas relativas a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Extraccion_Subdominios import extract_subdomains


def main(url_a_extraer=None, num_paginas_extraer=1):
    print("Iniciando el proceso de extracción de subdominios...")
    mensaje_final = ""
    try:
        if url_a_extraer is None:
            url_a_extraer = [
                                    ["https://www.freshproduce.com/resources/global-trade/","Global Trade"],
                                    ["https://www.freshproduce.com/resources/technology/","Technology"],
                                    ["https://www.freshproduce.com/resources/food-safety/","Food Safety"]
                                    ] # Ya viene con su respectivo etiquetado para identificar el subdominio
        
        num_paginas_extraer = 1 # Solo se ocupa extraer una página, la primera página.
        paginas_extraidas = extract_subdomains.extraccion_de_subdominios(url_a_extraer, num_paginas_extraer)
        print(f"Total de subdominios extraídos: {len(paginas_extraidas)}")
        columnas = ['URL','Category']
        df_dominios = pd.DataFrame(paginas_extraidas, columns=columnas)
        df_dominios.to_csv(f"extracted_subdomains.csv", index=False)  # Guardar el DataFrame en un archivo CSV
        mensaje_final = f"Extracción completada. Se han guardado {len(paginas_extraidas)} subdominios en 'extracted_subdomains.csv'."
    except Exception as e:
        mensaje_final = f"Ocurrió un error durante la extracción: {e}"
    return mensaje_final

if __name__ == "__main__":
    resultado = main()
    print(resultado)