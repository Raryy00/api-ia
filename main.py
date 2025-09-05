from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import base64
from dotenv import load_dotenv

load_dotenv()

try:
    from imagem import processar_imagem
    from pdf import processar_pdf
    from script import processar_texto
    from gerar_imagem import gerar_imagem
except ImportError as e:
    raise ImportError(f"Erro ao importar módulos: {str(e)}")

class ProcessarTextoRequest(BaseModel):
    prompt: str

class ProcessarArquivoRequest(BaseModel):
    prompt: str
    arquivo_base64: str

app = FastAPI(
    title="API de Serviços de IA",
    description="API para processamento de imagens, PDFs e textos usando IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API de Serviços de IA - Use /docs para ver a documentação"}

@app.post("/processar/imagem")
async def processar_imagem_route(request: ProcessarArquivoRequest = Body(...)):
    try:
        image_data = base64.b64decode(request.arquivo_base64)
        resultado = processar_imagem(request.prompt, image_data)
        return JSONResponse({"status": "sucesso", "prompt": request.prompt, "resultado": resultado})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

@app.post("/processar/pdf")
async def processar_pdf_route(request: ProcessarArquivoRequest = Body(...)):
    try:
        pdf_data = base64.b64decode(request.arquivo_base64)
        resultado = processar_pdf(request.prompt, pdf_data)
        return JSONResponse({"status": "sucesso", "prompt": request.prompt, "resultado": resultado})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

@app.post("/processar/texto")
async def processar_texto_route(request: ProcessarTextoRequest = Body(...)):
    try:
        resultado = processar_texto(request.prompt)
        return JSONResponse({"status": "sucesso", "prompt": request.prompt, "resultado": resultado})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar texto: {str(e)}")

@app.post("/gerar/imagem")
async def gerar_imagem_route(request: ProcessarTextoRequest = Body(...)):
    try:
        resultado = gerar_imagem(request.prompt)
        return JSONResponse({"status": "sucesso", "prompt": request.prompt, "resultado": resultado})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar imagem: {str(e)}")

@app.get("/saude")
async def health_check():
    return {"status": "online", "servico": "API de IA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))