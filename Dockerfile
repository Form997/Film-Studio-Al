FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg fonts-noto-core && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY studio ./studio
COPY web ./web
ENV STUDIO_HOME=/app/data
EXPOSE 7860
CMD ["uvicorn","studio.api:app","--host","127.0.0.1","--port","7860"]
