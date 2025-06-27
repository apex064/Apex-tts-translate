from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
from uuid import uuid4

app = Flask(__name__)

AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Supported language codes
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh-CN": "Chinese (Simplified)",
    "hi": "Hindi",
    "yo": "Yoruba",
    "ar": "Arabic",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "tr": "Turkish",
    "id": "Indonesian"
}

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = None
    audio_file = None
    original_text = ""
    source_lang = "auto"
    target_lang = "en"
    speed = "normal"

    if request.method == "POST":
        original_text = request.form.get("text", "")
        source_lang = request.form.get("source_lang", "auto")
        target_lang = request.form.get("target_lang", "en")
        speed = request.form.get("speed", "normal")
        slow = True if speed == "slow" else False

        try:
            # Translate text
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(original_text)

            # Generate audio
            filename = f"{uuid4().hex}.mp3"
            filepath = os.path.join(AUDIO_DIR, filename)
            tts = gTTS(text=translated_text, lang=target_lang, slow=slow)
            tts.save(filepath)
            audio_file = filepath

        except Exception as e:
            translated_text = f"⚠️ Error: {str(e)}"

    # List audio history
    audio_files = sorted(os.listdir(AUDIO_DIR), reverse=True)

    return render_template(
        "index.html",
        languages=LANGUAGES,
        translated_text=translated_text,
        audio_file=audio_file,
        audio_files=audio_files,
        original_text=original_text,
        source_lang=source_lang,
        target_lang=target_lang,
        speed=speed
    )

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(AUDIO_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
