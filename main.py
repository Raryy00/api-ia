from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import base64
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Importe suas funções (ajuste os caminhos se necessário)
try:
    from imagem import processar_imagem
    from pdf import processar_pdf
    from script import processar_texto
except ImportError as e:
    raise ImportError(f"Erro ao importar módulos: {str(e)}")

# Modelos Pydantic para requisições JSON
class ProcessarTextoRequest(BaseModel):
    prompt: str

class ProcessarArquivoRequest(BaseModel):
    prompt: str
    arquivo_base64: str  # Base64 do arquivo (imagem ou PDF)

app = FastAPI(
    title="API de Serviços de IA",
    description="API para processamento de imagens, PDFs e textos usando IA",
    version="1.0.0"
)

# Adicionar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API de Serviços de IA - Use /docs para ver a documentação"}

@app.post("/processar/imagem")
async def processar_imagem_route(request: ProcessarArquivoRequest = Body(...)):
    """
    Processa uma imagem (base64) com IA baseado no prompt fornecido
    """
    try:
        # Decodifica base64 para bytes
        try:
            image_data = base64.b64decode(request.arquivo_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Formato base64 inválido para a imagem")
        
        # Processa a imagem
        resultado = processar_imagem(request.prompt, image_data)
        
        return JSONResponse(
            content={
                "status": "sucesso",
                "prompt": request.prompt,
                "resultado": resultado
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

@app.post("/processar/pdf")
async def processar_pdf_route(request: ProcessarArquivoRequest = Body(...)):
    """
    Processa um PDF (base64) com IA baseado no prompt fornecido
    """
    try:
        # Decodifica base64 para bytes
        try:
            pdf_data = base64.b64decode(request.arquivo_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Formato base64 inválido para o PDF")
        
        # Processa o PDF
        resultado = processar_pdf(request.prompt, pdf_data)
        
        return JSONResponse(
            content={
                "status": "sucesso",
                "prompt": request.prompt,
                "resultado": resultado
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

@app.post("/processar/texto")
async def processar_texto_route(request: ProcessarTextoRequest = Body(...)):
    """
    Processa texto com IA baseado no prompt fornecido
    """
    try:
        # Processa o texto
        resultado = processar_texto(request.prompt)
        
        return JSONResponse(
            content={
                "status": "sucesso",
                "prompt": request.prompt,
                "resultado": resultado
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar texto: {str(e)}")

@app.get("/saude")
async def health_check():
    """
    Endpoint para verificar se a API está funcionando
    """
    return {"status": "online", "servico": "API de IA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)