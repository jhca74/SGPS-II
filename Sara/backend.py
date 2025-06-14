from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests, os

load_dotenv()

app = FastAPI()

class Mensagem(BaseModel):
    mensagem: str
    emissor: str

estado_sara = {"modo": "normal"}

def consultar_ollama(mensagem):
    try:
        resposta = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:8b",
            "prompt": mensagem,
            "stream": False
        }, timeout=30)

        dados = resposta.json()
        print("🧠 DEBUG (resposta do Ollama):", dados)

        if "response" in dados:
            return dados["response"]
        elif "text" in dados:
            return dados["text"]
        else:
            return f"[IA local: formato inesperado] → {dados}"

    except Exception as e:
        print("❌ ERRO no consultar_ollama:", str(e))
        return "[Erro IA local]"

def consultar_gpt(mensagem):
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        chat = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4", temperature=0)
        resposta = chat([HumanMessage(content=mensagem)])
        return resposta.content
    except:
        return "[Erro GPT]"

def consultar_claude(mensagem):
    import anthropic
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        resposta = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.5,
            messages=[{"role": "user", "content": mensagem}]
        )
        return resposta.content[0].text if resposta.content else "[Erro Claude]"
    except:
        return "[Erro Claude]"

def consultar_gemini(mensagem):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-pro")
        resposta = model.generate_content(mensagem)
        return resposta.text if hasattr(resposta, 'text') else "[Erro Gemini]"
    except:
        return "[Erro Gemini]"

@app.post("/responder")
def responder(dados: Mensagem):
    pergunta = dados.mensagem.lower()

    if "sara se natural" in pergunta:
        estado_sara["modo"] = "humano_total"
        return {"resposta": "Modo humano_total ativado."}
    elif "sara se profissional" in pergunta:
        estado_sara["modo"] = "normal"
        return {"resposta": "Modo normal ativado."}

    resposta = ""
    if estado_sara["modo"] == "humano_total":
        resposta = consultar_claude(dados.mensagem)
    else:
        resposta = consultar_ollama(dados.mensagem)
        if not resposta or resposta.strip() == "":
            resposta = consultar_gpt(dados.mensagem)
        if not resposta or resposta.strip() == "":
            resposta = consultar_claude(dados.mensagem)
        if not resposta or resposta.strip() == "":
            resposta = consultar_gemini(dados.mensagem)

    os.makedirs("compendio", exist_ok=True)
    with open("compendio/historico_conversas.txt", "a", encoding="utf-8") as f:
        f.write(f"Pergunta: {dados.mensagem}\n")
        f.write(f"Resposta: {resposta}\n\n")

    return {"resposta": resposta}

@app.get("/status")
def status():
    return {"estado": "Sara operacional", "modo": estado_sara["modo"]}

@app.post("/falar")
def falar(dados: Mensagem):
    with open("voz_sara/output.txt", "w", encoding="utf-8") as f:
        f.write(dados.mensagem)
    return {"mensagem": "Texto recebido para falar."}
