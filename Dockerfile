FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install yt-dlp Flask && \
    apt-get clean

COPY app.py /app.py

CMD ["python", "/app.py"]
