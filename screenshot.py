import subprocess
import sys
import base64
import re
from io import BytesIO

def get_stream_url(youtube_url):
    """Fetch the direct stream URL of a YouTube livestream."""
    command = ["yt-dlp", "-g", "-f", "best", youtube_url]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching stream URL:", result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def capture_frame(stream_url, time_position="00:00:01"):
    """Capture a single frame from the livestream and return it as a base64-encoded image data URL."""
    if not isinstance(stream_url, str) or not re.match(r'^https?://\S+$', stream_url):
        print("Invalid stream URL")
        sys.exit(1)
    
    command = [
        "ffmpeg", "-y", "-i", stream_url, "-vf", "select=eq(n\,1)",
        "-vsync", "vfr", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "pipe:1"
    ]
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        print("Error capturing frame:", result.stderr)
        sys.exit(1)
    
    base64_encoded = base64.b64encode(result.stdout).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_encoded}"

def get_screenshot(youtube_url):
    stream_url = get_stream_url(youtube_url)
    base64_image = capture_frame(stream_url)
    return base64_image
