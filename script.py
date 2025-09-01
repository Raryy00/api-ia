import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (apenas para desenvolvimento local)
load_dotenv()

# Configuração da API (não levantar erro aqui)
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
except Exception as e:
    print(f"Aviso: Erro ao configurar a API no import: {e}")

model = None

def processar_texto(prompt: str) -> str:
    """
    Processa texto com IA baseado no prompt fornecido
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
        
        # Gera conteúdo com o prompt original
        response = model.generate_content(prompt)
        
        # Verifica se há texto na resposta
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "Nenhuma resposta válida retornada. Pode ter sido bloqueado por filtros de segurança."
            
    except Exception as e:
        return f"Erro ao processar texto: {str(e)}"