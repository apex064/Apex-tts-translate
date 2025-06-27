from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
from googletrans import Translator
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
    "yo": "Yoruba",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese"
}

translator = Translator()

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    translated_text = ""
    detected_lang = None

    if request.method == "POST":
        text = request.form["text"]
        from_lang = request.form.get("from_lang")
        to_lang = request.form.get("to_lang")
        slow = request.form.get("speed") == "slow"

        # Detect or use source language
        if from_lang == "auto":
            detection = translator.detect(text)
            from_lang = detection.lang
            detected_lang = LANGUAGES.get(from_lang, from_lang)

        # Translate
        translation = translator.translate(text, src=from_lang, dest=to_lang)
        translated_text = translation.text

        # Text to Speech
        filename = f"{uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text=translated_text, lang=to_lang, slow=slow)
        tts.save(filepath)
        audio_file = filepath

    audio_files = sorted(os.listdir(AUDIO_DIR), reverse=True)

    return render_template(
        "index.html",
        audio_file=audio_file,
        audio_files=audio_files,
        languages={"auto": "Auto Detect", **LANGUAGES},
        translated_text=translated_text,
        detected_lang=detected_lang
    )

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(AUDIO_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
