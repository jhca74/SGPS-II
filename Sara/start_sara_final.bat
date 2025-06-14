@echo off
cd /d C:\Users\anjos\Desktop\SGPS\Sara

echo [1/5] A iniciar containers Docker...
docker compose -f tts_openvoice\Docker-compose.yml up -d

timeout /t 5

echo [2/5] A iniciar servidor do Ollama...
start cmd /k "ollama serve"

timeout /t 3

echo [3/5] A carregar modelo DeepSeek R1 8B...
start cmd /k "ollama run deepseek-r1:8b"

timeout /t 3

echo [4/5] A iniciar backend FastAPI da Sara...
start cmd /k "uvicorn backend:app --port 8001 --reload"

timeout /t 2

echo [5/5] A iniciar painel visual da Sara...
start cmd /k "python frontend.py"

echo Tudo pronto. A Sara estara online em instantes.
