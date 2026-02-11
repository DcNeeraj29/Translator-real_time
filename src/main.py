from translator.translate_text import TextTranslator
from asr.speech_to_text import transcribe_audio
from record_audio import record_audio
from Utils.lang_detect import detect_language
import os
import time
from datetime import datetime


# PATH = 
audio_path = "./audio/input.wav"
os.makedirs("text", exist_ok=True)

record_audio(output_path="audio/input.wav",duration = 5)

translator = TextTranslator("en","hi")

print("Continuous Translator started...")
print("Press CTRL+C to stop. ")
print("Main file started...")

try:
    while True:
        record_audio(output_path=audio_path, duration=5)
        asr_text = transcribe_audio(audio_path)

        if not asr_text.strip():
            print("No speech detected. Try again ")
            continue

        translated_text = translator.translate(asr_text)

        print(f"ASR Output: {asr_text}")
        print(f"Translated Output: {translated_text}")

        with open("text/translated_output.txt", "w", encoding="utf-8") as f:
            f.write(asr_text + "\n")
            f.write(translated_text + "\n\n")
except KeyboardInterrupt:
    print("\n Translator stopped by user.")
