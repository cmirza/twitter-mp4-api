from flask import Flask, request, render_template
import subprocess
import json

app = Flask(__name__)

@app.route("/get-mp4", methods=["POST"])
def get_mp4():
    # Log raw incoming request
    print("HEADERS:", dict(request.headers))
    print("RAW BODY:", request.data)
    data = request.get_json(silent=True)
    print("JSON BODY:", data)

    tweet_url = data.get("url") if data else None

    if not tweet_url:
        return "Missing or invalid 'url'", 400

    try:
        result = subprocess.run(
            ["yt-dlp", "-j", tweet_url],
            capture_output=True,
            text=True,
            timeout=20
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # yt-dlp may output multiple JSON objects (one per line)
        video_data_list = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        video_data = video_data_list[0]  # pick the first video (or adjust as needed)

        http_formats = [f for f in video_data["formats"] if f["format_id"].startswith("http-")]
        if not http_formats:
            return "No MP4 formats found", 404

        best = sorted(http_formats, key=lambda f: f.get("height", 0), reverse=True)[0]
        return best["url"]
    except Exception as e:
        return f"yt-dlp error: {str(e)}", 500

@app.route("/")
def root():
    return "API is running"

@app.route("/app")
def serve_app():
    return render_template("app.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)