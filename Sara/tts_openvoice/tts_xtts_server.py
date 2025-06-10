from fastapi import FastAPI, Request
from TTS.api import TTS
import os

app = FastAPI()

# Caminho para o modelo XTTS
XTTS_PATH = os.getenv("XTTS_MODEL_PATH", "modelo_xtts")
VOICE_SAMPLE = os.getenv("XTTS_VOICE_SAMPLE", "voz_base_sara.wav")
tts = TTS(XTTS_PATH, gpu=False)

@app.get("/")
def ping():
	return {"status": "xtts online"}

@app.post("/falar")
async def falar(req: Request):
	data = await req.json()
	texto = data.get("texto", "")
	idioma = data.get("idioma", "pt")
	ficheiro_saida = data.get("ficheiro_saida", "output_xtts.wav")
	tts.tts_to_file(
		text=texto,
		speaker_wav=VOICE_SAMPLE,
		language=idioma,
		file_path=ficheiro_saida
	)
	return {"ficheiro": ficheiro_saida}