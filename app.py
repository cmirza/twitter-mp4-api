from flask import Flask, request, render_template, jsonify, abort
import subprocess
import json
import logging
import re

app = Flask(__name__)

# --- Rate limiting setup ---
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(get_remote_address, app=app, default_limits=["10/minute"])
    limiter_available = True
except ImportError:
    limiter_available = False

def is_valid_twitter_url(url):
    """Strict validation for X (formerly Twitter) status URLs."""
    pattern = r"^https?://(www\.)?x\.com/([A-Za-z0-9_]+)/status/(\d+)(\?.*)?$"
    match = re.match(pattern, url)
    return bool(match)


def fetch_mp4_url(tweet_url):
    """Run yt-dlp and extract the best available MP4 URL from a Twitter post."""
    try:
        result = subprocess.run(
            ["yt-dlp", "-j", tweet_url],
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )
        logging.debug(f"yt-dlp stdout: {result.stdout}")
        logging.debug(f"yt-dlp stderr: {result.stderr}")
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp failed: {result.stderr.strip()}")
        video_data_list = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        if not video_data_list:
            raise ValueError("No video data found.")
        video_data = video_data_list[0]
        http_formats = [f for f in video_data["formats"] if f["format_id"].startswith("http-")]
        if not http_formats:
            raise ValueError("No MP4 formats found.")
        best = sorted(http_formats, key=lambda f: f.get("height", 0), reverse=True)[0]
        return best["url"]
    except subprocess.TimeoutExpired:
        logging.warning("yt-dlp timed out")
        raise RuntimeError("yt-dlp timed out fetching video.")
    except Exception as e:
        logging.exception("Error fetching MP4 URL")
        raise

def get_mp4():
    """API endpoint to extract MP4 URL from a Twitter post."""
    if not request.is_json:
        return jsonify(error="Request must be JSON."), 400
    data = request.get_json(silent=True)
    tweet_url = data.get("url") if data else None
    if not tweet_url or not is_valid_twitter_url(tweet_url):
        return jsonify(error="Missing or invalid 'url'. Must be a Twitter status URL."), 400
    try:
        mp4_url = fetch_mp4_url(tweet_url)
        return mp4_url
    except ValueError as ve:
        return jsonify(error=str(ve)), 404
    except RuntimeError as re:
        return jsonify(error=str(re)), 504
    except Exception:
        logging.exception("Internal server error")
        return jsonify(error="Internal server error. Please try again later."), 500

app.add_url_rule("/get-mp4", view_func=get_mp4, methods=["POST"])
if limiter_available:
    get_mp4 = limiter.limit("10/minute")(get_mp4)

@app.route("/")
def root():
    return "API is running"

@app.route("/app")
def serve_app():
    return render_template("app.html")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=8080)