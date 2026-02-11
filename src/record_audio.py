import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

audio_dir = project_root / "audio"
audio_file = audio_dir/"input.wav"

fs = 16000
seconds = 5
audio_dir.mkdir(parents=True, exist_ok=True)


# def record_audio(seconds):
#     print("Recording...")
#     audio = sd.rec(int(seconds * fs), samplerate = fs, channels = 1)
#     sd.wait()

#     write(audio_file,fs, audio)
#     print(f"Recording complete. Audio saved to \n{audio_file}")

def record_audio(output_path: str, duration: int =5, sample_rate: int = 16000, channels: int = 1):
    output_path = project_root/output_path
    print(f"Recording for {duration} seconds..")
    audio = sd.rec(int(duration * sample_rate), samplerate = sample_rate, channels=channels)
    sd.wait()
    write(output_path, sample_rate, audio)
    print(f"Recording complete. Audio saved to {output_path}")
