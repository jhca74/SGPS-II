import os
import torch
import soundfile as sf
from flask import Flask, request, jsonify
from TTS.api import TTS

# Importações obrigatórias para deserialização do modelo
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Registo das classes permitidas no carregamento dos weights (PyTorch >=2.6)
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs,
])

# Nome do modelo XTTS
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

# Inicialização da TTS (sem GPU por compatibilidade)
tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)

# Inicializar API Flask
app = Flask(__name__)

@app.route("/", methods=["POST"])
def sintetizar():
    data = request.get_json()
    texto = data.get("texto", "")
    if not texto:
        return jsonify({"erro": "Texto não fornecido"}), 400

    try:
        wav = tts.tts(text=texto)
        caminho_saida = "saida.wav"
        sf.write(caminho_saida, wav, 22050)
        return jsonify({"mensagem": "Áudio sintetizado com sucesso.", "ficheiro": caminho_saida})
    except Exception as e:
        return jsonify({"erro": f"Erro ao sintetizar: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
