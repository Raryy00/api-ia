import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def gerar_imagem(prompt: str) -> str:
    try:
        # Obter a chave da API do ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("Chave de API OPENAI_API_KEY não configurada.")
            return "Erro: Chave de API OPENAI_API_KEY não configurada."

        # Inicializar o cliente OpenAI explicitamente, sem argumentos adicionais
        logger.info("Inicializando cliente OpenAI...")
        client = OpenAI(api_key=api_key)

        # Gerar imagem
        logger.info(f"Gerando imagem com prompt: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        # Extrair dados da imagem em base64
        image_b64 = response.data[0].b64_json
        logger.info("Imagem gerada com sucesso.")
        return image_b64

    except Exception as e:
        logger.error(f"Erro detalhado ao gerar imagem: {str(e)}")
        return f"Erro ao gerar imagem: {str(e)}"