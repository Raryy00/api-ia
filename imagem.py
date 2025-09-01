import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64

# Carregar variáveis de ambiente do arquivo .env (apenas para desenvolvimento local)
load_dotenv()

# Configuração da API (não levantar erro aqui; verificar no runtime)
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
    # Se não houver chave, não configure agora; verifique nas funções
except Exception as e:
    print(f"Aviso: Erro ao configurar a API no import: {e}")

# Inicializa o modelo (opcional; pode ser lazy loading nas funções)
model = None

def processar_imagem(prompt: str, image_data: bytes) -> str:
    """
    Processa uma imagem com IA baseado no prompt fornecido
    """
    global model
    try:
        # Verificar se a chave de API está configurada
        if not os.getenv('GEMINI_API_KEY'):
            return "Erro: Chave de API GEMINI_API_KEY não configurada. Configure no ambiente."
        
        # Configurar se ainda não foi
        if not model:
            api_key = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Converter bytes para imagem PIL
        image = Image.open(BytesIO(image_data))
        
        # Codificar imagem para base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Preparar conteúdo para a API
        contents = [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    },
                    {
                        "text": prompt  # Detecção automática de idioma
                    }
                ]
            }
        ]
        
        # Chamar a API
        response = model.generate_content(contents)
        
        return response.text if hasattr(response, 'text') else "Nenhuma resposta válida retornada."
        
    except Exception as e:
        return f"Erro ao processar imagem: {str(e)}"