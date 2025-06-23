import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Extraccion_Subdominios import extract_subdomains
from webScrapping import webScrap

def clean_text(text):
    # Elimina espacios en blanco al principio y al final, y elimina líneas vacías
    text_without_empty_lines_start_end = text.strip()  # Eliminar espacios en blanco al principio y al final del texto 
    cleaned_text = ""
    for line in text_without_empty_lines_start_end.split('\n'):  # Hace un arreglo de saltos de línea
        line = line.strip()  # Eliminar espacios en blanco al principio y al final de cada línea
        if line:  # Verificar si la línea no está vacía
            cleaned_text += line + "\n"  # Concatenar la línea al texto final, agregando un salto de línea al final
    return cleaned_text.strip()  # Devolver el texto final después de eliminar espacios en blanco al principio y al final

def copy_df_and_add_title_and_text_from_URL(dataframe):
    # Extrae el texto de la columna 'URL' del DataFrame y lo coloca en una nueva columna 'Text'
    dataframe_result = dataframe.copy()  # Hacer una copia del DataFrame original para evitar modificarlo directamente
    dataframe_result['Title'] = None  # Crear una nueva columna 'Title' con valores nulos
    dataframe_result['FullArticleText'] = None  # Crear una nueva columna 'Topics' con valores nulos
    
    for i in range(len(dataframe_result)):
        URL, Category = dataframe_result.iloc[i][['URL', 'Category']]  # Acceder a cada fila por índice
        print(f"Extrayendo texto de la URL: {URL}, Categoría: {Category}")
        id_a_extraer = 'pageContent'  # ID del elemento HTML que contiene el texto
        Extraccion_HTML_dinamico_todo_el_contenido = webScrap.scrape_website_with_dynamic_content(URL, classes_to_wait=[id_a_extraer], ID_OR_CLASS='ID')
        title_page = Extraccion_HTML_dinamico_todo_el_contenido.find('h1')  # Buscar el título de la página
        if title_page:
            dataframe_result.at[i, 'Title'] = title_page.text.strip()  # Asignar el título a una nueva columna 'Title'
        else:
            print(f"No se encontró el título en la URL: {URL}")
            dataframe_result.at[i, 'Title'] = None
        all_content_page = Extraccion_HTML_dinamico_todo_el_contenido.find(id=id_a_extraer)  # Buscar el contenido principal de la página
        if all_content_page:
            cleaned_text = clean_text(all_content_page.text)
            dataframe_result.at[i, 'FullArticleText'] = cleaned_text  # Asignar el texto limpio a la nueva columna
        else:
            print(f"No se encontró el contenido principal en la URL: {URL}")
            dataframe_result.at[i, 'FullArticleText'] = None
    dataframe_result = dataframe_result[['Title', 'URL', 'Category', 'FullArticleText']]  # Reordenar las columnas del DataFrame
    return dataframe_result  # Devolver el DataFrame con la nueva columna 'Text' que contiene el texto extraído de las URLs

def main(nombre_archivo= "extracted_subdomains.csv" ):
    mensaje_final = ""
    try: 
        df_subdominios = pd.read_csv(nombre_archivo)  # Cargar el DataFrame desde el archivo CSV
        df_extracted_info_from_pages = copy_df_and_add_title_and_text_from_URL(df_subdominios)
        df_extracted_info_from_pages.to_csv("scraped_data.csv", index=False)  # Guardar el DataFrame en un archivo CSV
        mensaje_final = f"Extracción completada. Se han guardado los datos en 'scraped_data.csv'."
    except FileNotFoundError:
        mensaje_final = f"El archivo '{nombre_archivo}' no se encontró. Asegúrate de haber ejecutado el script de extracción primero."
    except Exception as e:
        mensaje_final = f"Ocurrió un error inesperado: {e}"
    return mensaje_final

if __name__ == "__main__":
    resultado = main()  # Llamar a la función principal
    print(resultado)
