from services.vad_recorder import VADRecorder

def record_audio_vad():
    recorder = VADRecorder()
    return recorder.record("audio/input.wav")