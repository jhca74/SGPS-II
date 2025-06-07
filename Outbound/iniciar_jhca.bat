@echo off
echo Iniciando serviços da JHCA...

:: Caminho onde está o docker-compose.yml
cd /d "C:\Users\anjos\OneDrive\Desktop\JHCA SGPS\painel_geral"

:: Iniciar os containers em background
docker-compose up -d

:: Esperar um pouco para os serviços iniciarem
timeout /t 5

:: Mostrar status dos containers
echo Verificando estado dos containers:
docker ps

:: Mostrar logs dos serviços principais
echo Logs iniciais do EspoCRM:
docker logs --tail 10 espocrm

echo.
echo Sistema iniciado. Aceda ao CRM: http://localhost:8080
pause
