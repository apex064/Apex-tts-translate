from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import os
from uuid import uuid4

app = Flask(__name__)

AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh-CN": "Chinese",
    "hi": "Hindi",
    "yo": "Yoruba"
}

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form["text"]
        lang = request.form.get("lang", "en")
        slow = True if request.form.get("speed") == "slow" else False

        filename = f"{uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(filepath)
        audio_file = filepath

    # List of audio files for history (latest first)
    audio_files = sorted(os.listdir(AUDIO_DIR), reverse=True)

    return render_template("index.html", audio_file=audio_file, audio_files=audio_files, languages=LANGUAGES)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(AUDIO_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
