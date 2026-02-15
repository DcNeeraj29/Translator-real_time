from gtts import gTTS
from playsound import playsound
import os 
import time
from datetime import datetime

def speak_text(text, lang="en"):
    try:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(BASE_DIR, "..", "..", "audio")
        os.makedirs(audio_dir, exist_ok=True)

        filename = f"tts_{datetime.now().strftime('%H%M%S%f')}.mp3"
        output_path = os.path.join(audio_dir, filename)

        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)

        playsound(output_path)

        time.sleep(0.5)
        os.remove(output_path)

    except Exception as e:
        print(f"TTS Error: {e}")
