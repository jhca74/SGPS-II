FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main_backend:app", "--host", "0.0.0.0", "--port", "8001"]







