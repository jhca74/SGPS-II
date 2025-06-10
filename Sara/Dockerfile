FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    ffmpeg \
    espeak \
    git \
    curl \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "backend.py"]









