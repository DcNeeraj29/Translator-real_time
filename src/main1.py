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

mode = input("Mode: 1 for Manual | 2 for Auto Detect: ")

SUPPORTED_LANG = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Russian": "ru"
}

SUPPORTED_PAIRS = {
    ("en", "hi"),
    ("hi", "en"),
    ("en", "fr"),
    ("fr", "en"),
    ("en", "de"),
    ("de", "en"),
    ("en", "es"),
    ("es", "en"),
    ("en", "ru"),
    ("ru", "en")
}


print("Program Started...")

print("Available Languages:")
for name in SUPPORTED_LANG:
    print("-", name)

src_choice = input("Enter the SRC Language: ").strip().title()
trg_choice = input("Enter the Target Language: ").strip().title()

src = SUPPORTED_LANG.get(src_choice)
tgt = SUPPORTED_LANG.get(trg_choice)


if not src or not tgt:
    print("Invalid Language Choice...")
    exit()

translator_cache = {}

running = True

while running:
    try:
        print("Recording...")
        record_audio(output_path=AUDIO_PATH, duration=5)

        print("Transcribing...")
        asr_text = transcribe_audio(AUDIO_PATH)

        if not asr_text or asr_text.strip() == "":
            print("No Speech detected. Speak again.")
            continue

        print(f"[ASR] {asr_text}")

        # AUTO DETECT MODE
        current_src = src
        if mode == "2":
            detected_lang = detect_language(asr_text)
            if detected_lang in SUPPORTED_LANG.values():
                current_src = detected_lang
                print(f"[DETECTED LANGUAGE] {current_src}")
            else:
                print("Detected language not supported. Using selected sources.")

        if (current_src, tgt) not in SUPPORTED_PAIRS:
            print("This language pair is not supported in demo version.")
            continue

        # MODEL CACHING
        if (current_src, tgt) not in translator_cache:
            translator_cache[(current_src, tgt)] = TextTranslator(current_src, tgt)

        translator = translator_cache[(current_src, tgt)]
        translated_text = translator.translate(asr_text)

        print(f"[TRANSLATED] {translated_text}")

        print("Speaking...")
        speak_text(translated_text, tgt)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{current_src}_to_{tgt}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"ASR ({current_src}): {asr_text}\n")
            f.write(f"Translated ({tgt}): {translated_text}")

        print(f"[SAVED] {filepath}\n")
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("Translator Stopped")
        running = False

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
