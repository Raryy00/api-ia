import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def gerar_imagem(prompt: str) -> str:
    try:
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Erro: Chave de API OPENAI_API_KEY não configurada."

        # Initialize OpenAI client explicitly
        client = OpenAI(api_key=api_key)

        # Generate image
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        # Extract base64 image data
        image_b64 = response.data[0].b64_json
        return image_b64

    except Exception as e:
         print(f"Erro detalhado: {str(e)}")  # Add this line
    return f"Erro ao gerar imagem: {str(e)}"  
    