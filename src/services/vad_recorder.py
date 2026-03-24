import collections
import sys
import wave
import webrtcvad
import pyaudio
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAME_DURATION = 30 
CHUNK_SIZE = int(RATE * FRAME_DURATION / 1000)

class VADRecorder:
    def __init__ (self, aggressiveness=2, silence_duration=1.0):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.silence_duration = silence_duration

    def record(self, output_file):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        
        print("Listening... Speak Now!")

        frames = []
        ring_buffer = collections.deque(maxlen=int(1000/FRAME_DURATION))
        triggered = False
        silence_counter = 0
        max_silence_frames = int(self.silence_duration * 1000/FRAME_DURATION)

        start_time = time.time()
        max_wait_time = 10.0
        try:
            while True:
                frame = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                is_speech = self.vad.is_speech(frame, RATE)

                if not triggered and (time.time() - start_time > max_wait_time):
                    print("No Voice detected, exiting... ")
                    break
                if not triggered:
                    ring_buffer.append((frame, is_speech))
                    num_voiced = len([f for f, speech in ring_buffer if speech])

                    if num_voiced > 0.8 * ring_buffer.maxlen:
                        triggered = True
                        print("voice detected, recording... ")
                        frames.extend([f for f, s in ring_buffer])
                        ring_buffer.clear()
                else:
                    frames.append(frame)

                    if not is_speech:
                        silence_counter += 1
                    else:
                        silence_counter = 0
                    
                    if silence_counter > max_silence_frames:
                        print("Silence detected, stopping recording. ")
                        break
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return output_file
