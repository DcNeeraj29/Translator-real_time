import pyttsx3

def speak_text(text, lang=None):
    try:
        engine = pyttsx3.init()   # ✅ NEW instance every time

        engine.say(text)
        engine.runAndWait()

        engine.stop()  # ✅ important cleanup

    except Exception as e:
        print("TTS Error:", e)
        