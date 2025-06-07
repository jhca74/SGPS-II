
# Base Linux image
FROM ubuntu:22.04

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualização e instalação de dependências
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-pyqt5 xvfb \
    adb usbutils libimobiledevice-utils ideviceinstaller ifuse \
    libqt5gui5 libqt5widgets5 libqt5core5a libglib2.0-bin \
    && apt-get clean

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . /app

# Instalar dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt || true

# Executar interface via X virtual framebuffer se for app gráfico
CMD ["xvfb-run", "python3", "main/main_ia.py"]
