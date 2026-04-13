import os
from google import genai
from dotenv import load_dotenv

# Cargamos variables de entorno
load_dotenv()

# Configuración del cliente con la SDK moderna
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analizar_sintomas(sintomas: str) -> str:
    """
    Analiza los síntomas usando el modelo estable 'gemini-flash-latest' (Estándar 2026).
    """
    prompt = f"""
    Eres un asistente médico de triaje.
    El paciente describe los siguientes síntomas: "{sintomas}".
    Responde ÚNICAMENTE con el nombre de la especialidad médica más adecuada
    y una breve explicación de máximo 2 oraciones. No hagas diagnósticos.
    """
    try:
        # 'gemini-flash-latest' es la mejor opción para evitar 404 y 429
        respuesta = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return respuesta.text.strip()
    except Exception as e:
        error_msg = str(e)
        # Manejo amigable de límites de cuota (429)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "Sugerencia IA: Capacidad de la IA al límite temporalmente. Por favor, reintenta en un minuto."
        return f"Sugerencia IA: Error al analizar (Verifica tu conexión o API Key)."