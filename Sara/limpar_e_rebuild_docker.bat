@echo off
echo === A PARAR CONTAINERS EM EXECUÇÃO ===
FOR /F %%i IN ('docker ps -q') DO docker stop %%i

echo === A REMOVER CONTAINERS PARADOS ===
FOR /F %%i IN ('docker ps -aq') DO docker rm %%i

echo === A REMOVER IMAGENS ===
FOR /F %%i IN ('docker images -q') DO docker rmi -f %%i

echo === A LIMPAR CACHE, VOLUMES E REDES ORFÃS ===
docker system prune -a --volumes --force

echo === A CONSTRUIR TUDO DE NOVO (BUILD COMPLETO) ===
docker compose build --no-cache

echo === LIMPEZA E REBUILD CONCLUÍDOS ===
pause
