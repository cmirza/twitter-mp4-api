FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install yt-dlp Flask && \
    apt-get clean

WORKDIR /app
COPY . /app

# Optional but explicit:
COPY templates/ templates/

CMD ["python", "app.py"]
