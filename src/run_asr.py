from asr.speech_to_text import transcribe_audio

AUDIO_FILE = "audio/input.wav"

if __name__ == "__main__":
    transcribe_audio(AUDIO_FILE)
