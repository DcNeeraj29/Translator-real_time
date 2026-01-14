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



print("Recording...")
audio = sd.rec(int(seconds * fs), samplerate = fs, channels = 1)
sd.wait()

write(audio_file,fs, audio)
print(f"Recording complete. Audio saved to \n{audio_file}")
