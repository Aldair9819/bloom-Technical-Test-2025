import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

URL_OLLAMA = os.getenv("URL_OLLAMA") #Cargamos un archivo .env con la URL de Ollama

def pull(model):
    #URL por defecto para descargas de modelos LLM
    url = f'{URL_OLLAMA}/api/pull'
    # Comprobar que los valores obligatorios están presentes
    response_data = {
        "model": model,
        "stream": False #Evita usar streaming. Que no mande la información en partes y la mande en su lugar todo en conjunto
    }
    try:
        #Usa POST para enviar los datos al servidor
        response = requests.post(url, json=response_data)
        if response.status_code == 200:
            return response.json(), 200
        else:
            print("Error:", response.status_code, response.text)
            return {"error": f"Error {response.status_code}: {response.text}"}, response.status_code
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return {"error": f"An error occurred: {e}"}, 500
    
def generate(model,prompt = None, format = None, keep_alive = None):
    url = f'{URL_OLLAMA}/api/generate'
    # Comprobar que los valores obligatorios están presentes
    response_data = {
        "model": model,
        "stream": False #Evita usar streaming. Que no mande la información en partes y la mande en su lugar todo en conjunto
    }
    #Corroborar los valores opcionales y los añade en dado caso de existir
    if prompt:
        response_data["prompt"] = prompt
    if format:
        response_data["format"] = format
    if keep_alive:
        response_data["keep_alive"] = keep_alive
    try:
        response = requests.post(url, json=response_data)
        if response.status_code == 200:
            return response.json()['response'], 200 #Devolver código HTTP junto a la respuesta del modelo
        else:
            print("Error:", response.status_code, response.text)
            return {"error": f"Error {response.status_code}: {response.text}"}, response.status_code # Devolver error si la solicitud no fue exitosa junto con el código HTTP correspondiente
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return {"error": f"An error occurred: {e}"}, 500 # Devolver error si ocurre un problema con la solicitud HTTP junto con el código HTTP 500

