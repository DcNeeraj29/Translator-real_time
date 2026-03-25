from faster_whisper import WhisperModel
import os

print("Loading Whisper model...")
model = WhisperModel("base", compute_type="int8")

def transcribe_audio(audio_path, output_dir ="text"):

    print(f"Transcribing audio from {audio_path}...")
    segments, _ = model.transcribe(audio_path)

    text = ""
    for segment in segments:
        text += segment.text + " "
    text = text.strip()    
    os.makedirs(output_dir, exist_ok = True)
    output_path = os.path.join(output_dir, "transcription.txt")

    with open(output_path, "w", encoding = "utf-8")as f:
        f.write(text)
    
    print(f"Transcription saved to: {output_path}")
    return text