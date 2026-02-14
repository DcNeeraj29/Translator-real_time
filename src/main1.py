import os
import time
from datetime import datetime
from asr.speech_to_text import transcribe_audio
from translator.translate_text import TextTranslator
from Utils.lang_detect import detect_language
from record_audio import record_audio
from tts.text_to_speech import speak_text


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "..", "audio", "input.wav")
# Here ".." this is folder "audio" is subfolder, "input.wav" is file
OUTPUT_DIR = os.path.join(BASE_DIR, "..","text")
# Set output directory to ".." IN FOLDER, "Text" in text folder

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Program Started...")

while True:
    try:

        print("Recording...")
        record_audio(output_path=AUDIO_PATH, duration=5)

        print("Transcribing...")
        asr_text = transcribe_audio(AUDIO_PATH)

        if not asr_text or asr_text.strip() == "":
            print(f"No Speech is detected. speek again")
            continue

        print(f"[ASR] {asr_text}")
        detected_lang = detect_language(asr_text)

        if detected_lang not in ["en","hi"]:
            print("Unsupported Languge")
            continue

        if detected_lang == "en":
            src, tgt = "en" , "hi"
        else:
            src, tgt = "hi","en"

        translator = TextTranslator(src, tgt)
        translated_text = translator.translate(asr_text)

        print(f"[TRANSLATED] {translated_text}")
        print("Speaking...")
        speak_text(translated_text, tgt)


        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{src}_to_{tgt}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding = "utf-8") as f:
            f.write(f"ASR ({src}):{asr_text}\n")
            f.write(f"Translated ({tgt}): {translated_text}")
        
        print(f"[SAVED] {filepath}\n")
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("Translator Stopped")
        break

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
