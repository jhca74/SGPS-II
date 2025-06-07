FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests
CMD ["uvicorn", "modules.outbound_main:app", "--host", "0.0.0.0", "--port", "8081"]
