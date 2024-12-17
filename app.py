from flask import Flask, request, render_template, send_from_directory
import os
import yt_dlp

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to download YouTube videos
def download_yt_videos(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)  # Get the downloaded file path
            return os.path.basename(filename)  # Return only the file name
    except Exception as e:
        print(f"Error: {e}")
        return None

# Route for downloading videos
@app.route("/", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            file_name = download_yt_videos(video_url)
            if file_name:
                return render_template("index.html", video_path=file_name)
        return render_template("index.html", error="Failed to download video.")
    return render_template("index.html", video_path=None)

# Route to serve downloaded videos
@app.route('/downloads/<path:filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__== "__main__":
    app.run(debug=True)