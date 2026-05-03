import pyttsx3

# Initialize once
engine = pyttsx3.init()

# Optimal: adjust voice setting
engine.setProperty('rate',170) # speed
engine.setProperty('volume',1.0) # volume(0-1)

# Select voice 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak_text(text, lang='en'):
    try:
        if not text.strip():
            return
        
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Remove after test
for v in voices:
    print(v.id)

