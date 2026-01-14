import whisper
import os

def transcribe_audio(audio_path, output_dir ="text"):
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print(f"Transcribing audio from {audio_path}...")
    result = model.transcribe(audio_path)
    
    os.makedirs(output_dir, exist_ok = True)
    output_path = os.path.join(output_dir, "transcription.txt")

    with open(output_path, "w", encoding = "utf-8")as f:
        f.write(result["text"])
    
    print(f"Transcription saved to: {output_path}")
    return result["text"]
