import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No se encontró GEMINI_API_KEY en el .env")
    exit()

try:
    client = genai.Client(api_key=api_key)
    print("--- Listado de Modelos Disponibles ---")
    
    # Listamos todos los modelos disponibles para tu clave de forma simple
    for m in client.models.list():
        print(f"Modelo: {m.name}")
            
except Exception as e:
    print(f"Error al conectar con la API: {str(e)}")
