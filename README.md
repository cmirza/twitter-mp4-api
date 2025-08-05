# Twitter to MP4 API

A simple Flask-based API to extract direct MP4 video links from Twitter posts using `yt-dlp`. Includes a minimal web UI for fetching and previewing videos.

## Features

- **API Endpoint**:  
  - `POST /get-mp4` — Accepts a JSON body with a Twitter URL (`{"url": "<tweet_url>"}`) and returns the best available MP4 link.
- **Web UI**:  
  - `/app?url=<tweet_url>` — Fetches and previews the video, and copies the MP4 link to your clipboard.
- **Health Check**:  
  - `/` — Returns a simple status message.

## Requirements

- Python 3.11+
- Flask
- yt-dlp
- ffmpeg (for yt-dlp)

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the server:
   ```
   python app.py
   ```
3. Deploy with Docker or Fly.io as needed.

## Files

- `app.py` — Main Flask app and API logic
- `templates/app.html` — Minimal web UI
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container setup
- `fly.toml` — Fly.io deployment config