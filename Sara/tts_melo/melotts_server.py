from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def falar():
	data = request.json
	texto = data.get("texto", "")
	return jsonify({"mensagem": f"[MELO-TTS] Texto recebido: {texto}"})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)