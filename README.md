# Twitter to MP4 API

A simple Flask-based API to extract direct MP4 video links from Twitter posts using `yt-dlp`. Includes a minimal web UI for fetching and previewing videos.

Twitter doesn't give video previews in apps like Messages, which makes it difficult to share memes with non Twitter users. Extracting video URLs works around that.

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

## Changelog

### 2025-08-04
- Project created: initial version with Flask API and minimal web UI.
- Added `/get-mp4` endpoint to extract MP4 links from Twitter using yt-dlp.
- Basic HTML UI for fetching and previewing videos.
- Dockerfile and requirements for deployment.

### 2025-08-05
- Refactored `app.py` for better code structure and maintainability.
- Added strict Twitter URL validation and improved input sanitization.
- Improved error handling and user-friendly error messages (JSON responses, status codes).
- Switched from print statements to Python logging for all diagnostics.
- Added subprocess timeout and graceful handling of yt-dlp errors.
- Added optional API rate limiting using Flask-Limiter (if installed).
- Internal errors are now hidden from users in production responses.
- Updated security and robustness of the API endpoint.