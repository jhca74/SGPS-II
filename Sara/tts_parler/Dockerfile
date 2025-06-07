FROM python:3.11-slim
WORKDIR /app
COPY parlertts_server.py .
RUN pip install flask numpy
CMD ["python", "parlertts_server.py"]
