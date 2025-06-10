from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['POST'])
def falar():
	data = request.json
	texto = data.get("texto", "")
	energia = np.random.rand()
	return jsonify({"mensagem": f"[PARLER-TTS] Texto recebido: {texto}", "intensidade": energia})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)