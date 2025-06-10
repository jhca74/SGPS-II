@echo off
cd /d %~dp0

echo 🔁 A encerrar containers antigos...
docker compose down

echo 🛠️ A construir a imagem limpa...
docker compose build --no-cache

echo 🚀 A iniciar backend da Sara...
docker compose up

echo 🛑 Backend terminou. Verifica mensagens acima.
pause
