# script.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
except Exception as e:
    print(f"Aviso: Erro ao configurar a API no import: {e}")

model = None

def processar_texto(prompt: str) -> str:
    global model
    try:
        if not os.getenv('GEMINI_API_KEY'):
            return "Erro: Chave de API GEMINI_API_KEY não configurada."
        
        if not model:
            api_key = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        resultado = response.text if hasattr(response, 'text') else "Nenhuma resposta válida."
        
        return resultado
    
    except Exception as e:
        return f"Erro ao processar texto: {str(e)}"