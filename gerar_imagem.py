# gerar_imagem.py
import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()

try:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        openai.api_key = api_key
except Exception as e:
    print(f"Aviso: Erro ao configurar a API no import: {e}")

def gerar_imagem(prompt: str) -> str:
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return "Erro: Chave de API OPENAI_API_KEY não configurada."
        
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="b64_json"
        )
        
        image_b64 = response['data'][0]['b64_json']
        return image_b64
    
    except Exception as e:
        return f"Erro ao gerar imagem: {str(e)}"