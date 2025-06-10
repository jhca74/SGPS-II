from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import logging

# --- Carregar variáveis de ambiente ---
load_dotenv()
SARA_TTS_URL = os.getenv("SARA_TTS_URL", "http://localhost:5010/falar")
SARA_MODE = os.getenv("SARA_MODE", "normal")

# --- Inicializar logs ---
logging.basicConfig(level=logging.INFO)

# --- FastAPI App ---
app = FastAPI(
    title="Sara Backend",
    description="API principal da IA Sara",
    version="1.0.0"
)

# --- CORS (libertar chamadas locais/web) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelo para entrada de texto ---
class Mensagem(BaseModel):
    texto: str

# --- Endpoint de saúde ---
@app.get("/status")
def status():
    return {"status": "online", "modo": SARA_MODE}

# --- Endpoint principal da Sara (fala) ---
@app.post("/falar")
def falar(mensagem: Mensagem):
    texto = mensagem.texto
    logging.info(f"[SARA] Recebido: {texto}")

    try:
        # Envia para o TTS
        resposta = requests.post(SARA_TTS_URL, json={"texto": texto})
        if resposta.status_code == 200:
            return {"voz": "gerada", "mensagem": texto}
        else:
            logging.error("Erro TTS")
            return {"erro": "TTS não respondeu"}

    except Exception as e:
        logging.error(f"Erro na fala: {e}")
        return {"erro": str(e)}

# --- Fallback simples ---
@app.post("/responder")
def responder(mensagem: Mensagem):
    texto = mensagem.texto.lower()

    if "sara" in texto and "normal" in texto:
        global SARA_MODE
        SARA_MODE = "humano_total"
        return {"resposta": "Modo humano_total ativado"}

    return {"resposta": f"Sara respondeu: {texto}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8001, reload=True)
# --- Iniciar o servidor com Uvicorn ---
# Para iniciar o servidor, execute:
# uvicorn backend:app --host