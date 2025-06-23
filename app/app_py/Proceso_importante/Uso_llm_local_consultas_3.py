import sys
import os
import pandas as pd
import json

# Agrega las rutas relativas a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LLM_Consulta.Consulta_Ollama import pull, generate

def generate_summary_and_topics_with_llm(dataframe, modelo="llama3.2", format=None):
    if format is None: #Formato por defecto si no se especifica
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
    dataframe_with_llm_responses = dataframe.copy()  # Hacer una copia del DataFrame original para evitar modificarlo directamente
    dataframe_with_llm_responses['Summary'] = None  # Crear una nueva columna 'Summary' para almacenar las respuestas del LLM
    dataframe_with_llm_responses['Topics'] = None  # Crear una nueva columna 'Topics' para almacenar las respuestas del LLM
    for i in range(len(dataframe_with_llm_responses)):
        title = dataframe_with_llm_responses.iloc[i]['Title']  # Obtener el título de la fila actual
        url = dataframe_with_llm_responses.iloc[i]['URL']  # Obtener la URL de la fila actual
        category = dataframe_with_llm_responses.iloc[i]['Category']
        full_article_text = dataframe_with_llm_responses.iloc[i]['FullArticleText']
        print(f"Article Number {i + 1} of {len(dataframe_with_llm_responses)}")
        
        # prompt para la primera solicitud. Un resumen del artículo
        prompt_first= f"""
    This is a article about the category {category} with the title '{title}'.
    Generate a concise, one-sentence summary of the article's main point.
    The article is as follows:
    {full_article_text} 
        """
        # prompt para la segunda solicitud. Identificar temas o palabras clave
        prompt_second = f"""
    This is a article about the category {category} with the title '{title}'.
    Identify and list 3-5 primary topics or keywords from the text.
    RESPOND USING A JSON FORMAT.
    The article is as follows:
    {full_article_text}
        """
        
        response_first, code = generate(modelo, prompt=prompt_first, format=None, keep_alive=False)
        if code == 200:
            dataframe_with_llm_responses.at[i, 'Summary'] = response_first  # Asignar None si hay error
        else:
            print("Error al generar la respuesta del LLM para la primera solicitud. URL:", url)
            dataframe_with_llm_responses.at[i, 'Summary'] = None  # Asignar la respuesta del LLM a la columna 'Summary'
        response_second, code = generate(modelo, prompt=prompt_second, format=format, keep_alive=False)
        if code == 200:
            response_second_in_json = json.loads(response_second)  # Convertir la respuesta a JSON
            response_second_just_response = response_second_in_json['response']  # Extraer el campo 'response' del JSON
            dataframe_with_llm_responses.at[i, 'Topics'] = response_second_just_response  # Asignar None si hay error
        else:
            print("Error al generar la respuesta del LLM para la segunda solicitud. URL: ",url)
            dataframe_with_llm_responses.at[i, 'Topics'] = None  # Asignar la respuesta del LLM a la columna 'Topics'
    return dataframe_with_llm_responses  # Devolver el DataFrame con las nuevas columnas 'Summary' y 'Topics'



def main(nombre_archivo= "scraped_data.csv",modelo_llm="llama3.2:3b", format = None):
    print("Iniciando el proceso de extracción de subdominios...")
    mensaje_final = ""
    try:
       df_scraped_data = pd.read_csv(nombre_archivo)  # Cargar el DataFrame desde el archivo CSV
       response, code = pull(modelo_llm)
       if code == 200:
              print(f"Modelo {modelo_llm} descargado correctamente.")
              
              if format is None:
                  #Formato por defecto para la consulta
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
              dataframe_with_llm_responses = generate_summary_and_topics_with_llm(df_scraped_data, modelo=modelo_llm, format=format)        
              dataframe_with_llm_responses.to_csv("analysis_summary.csv", index=False)  # Guardar el DataFrame en un archivo CSV
              return "Proceso de consultas a LLM terminado"
       else:
           mensaje_final = f"Error al descargar el modelo {modelo_llm}: {response.get('error', 'Error desconocido')}"
    except Exception as e:
        mensaje_final = f"Ocurrió un error durante la extracción: {e}"
    return mensaje_final

if __name__ == "__main__":
    resultado = main()
    print(resultado)