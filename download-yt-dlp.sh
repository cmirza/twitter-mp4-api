#!/bin/bash

# Download latest yt-dlp binary to project root
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o yt-dlp

# Make it executable
chmod +x yt-dlp

echo "yt-dlp downloaded and made executable"
