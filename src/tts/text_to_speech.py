from gtts import gTTS
from playsound import playsound
import os 

def speak_text(text, lang="en"):
    try:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(BASE_DIR,"..","..","audio","output.mp3")

        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)

        playsound(output_path)


    except Exception as e:
        print(f"TTS Error: {e}")
