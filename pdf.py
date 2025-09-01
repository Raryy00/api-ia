import google.generativeai as genai
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

def processar_pdf(prompt: str, pdf_data: bytes) -> str:
    """
    Processa um PDF com IA baseado no prompt fornecido
    """
    try:
        # Verificar se a chave de API está configurada
        if not os.getenv('GEMINI_API_KEY'):
            return "Erro: Chave de API GEMINI_API_KEY não configurada"
        
        # Codificar PDF para base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        # Preparar conteúdo para a API
        contents = [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_base64
                        }
                    },
                    {
                        "text": prompt  # Removido "em português"
                    }
                ]
            }
        ]
        
        # Envia o PDF e o prompt para a API
        response = model.generate_content(contents)
        
        # Verifica se há texto na resposta
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "Nenhuma resposta válida retornada. Pode ter sido bloqueado por filtros de segurança."
            
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"