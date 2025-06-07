@echo off
cd /d "%~dp0"

IF NOT EXIST "docker-compose.yml" (
    echo ERRO: Ficheiro docker-compose.yml NAO ENCONTRADO!
    pause
    exit /b
)

echo === [1/7] A PARAR CONTAINERS E REMOVER ORFAOS ===
docker compose down --volumes --remove-orphans

echo === [2/7] A ELIMINAR TODOS OS CONTAINERS EXISTENTES ===
FOR /F %%i IN ('docker ps -aq') DO docker rm -f %%i

echo === [3/7] A ELIMINAR TODAS AS IMAGENS ===
FOR /F %%i IN ('docker images -q') DO docker rmi -f %%i

echo === [4/7] A LIMPAR BUILDER CACHE ===
docker builder prune -a -f

echo === [5/7] A LIMPAR VOLUMES E SISTEMA INTEIRO ===
docker volume prune -f
docker system prune -a --volumes -f

echo === [6/7] A FAZER BUILD LIMPO DA SARA ===
docker compose build --no-cache

echo === [7/7] A INICIAR CONTAINERS ===
docker compose up -d

echo.
echo === [VERIFICAR SARA COM CURL] ===
curl http://localhost:8001/
echo.
echo === FIM DO PROCESSO ===
pause