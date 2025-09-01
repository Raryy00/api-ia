import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Chave de API não encontrada. Defina a variável de ambiente GEMINI_API_KEY.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Erro ao configurar a API: {e}")
    raise

# Inicializa o modelo
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Erro ao inicializar o modelo: {e}")
    raise

def processar_imagem(prompt: str, image_data: bytes) -> str:
    """
    Processa uma imagem com IA baseado no prompt fornecido
    """
    try:
        # Verificar se a chave de API está configurada
        if not os.getenv('GEMINI_API_KEY'):
            return "Erro: Chave de API GEMINI_API_KEY não configurada"
        
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
                        "text": prompt  # Removido "em português"
                    }
                ]
            }
        ]
        
        # Chamar a API
        response = model.generate_content(contents)
        
        return response.text if hasattr(response, 'text') else "Nenhuma resposta válida retornada."
        
    except Exception as e:
        return f"Erro ao processar imagem: {str(e)}"