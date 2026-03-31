import sys
import os

# Disable CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Preloading Whisper...")
from asr.speech_to_text import transcribe_audio

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QComboBox, QTextEdit, QVBoxLayout, QCheckBox
)
from PyQt6.QtCore import QThread, pyqtSignal

# ---------------------------
# Paths
# ---------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "..", "..", "audio", "input.wav")

# ---------------------------
# Supported Languages
# ---------------------------

SUPPORTED_LANG = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Russian": "ru"
}



# ---------------------------
# Worker Thread
# ---------------------------

class TranslatorWorker(QThread):
    result_signal = pyqtSignal(str, str)
    status_signal = pyqtSignal(str)

    def __init__(self, src, tgt, auto_detect, translator_cache, continuous):
        super().__init__()
        self.src = src
        self.tgt = tgt
        self.auto_detect = auto_detect
        self.translator_cache = translator_cache
        self.continuous = continuous
        self.running = True

    def run(self):
        try:
            from translator.translate_text import TextTranslator
            from Utils.lang_detect import detect_language
            from services.mic_services import record_audio_vad
            from tts.text_to_speech import speak_text

            while self.running:

                self.status_signal.emit("🎙 Recording... Speak now.")
                audio_path  = record_audio_vad()

                if not audio_path:
                    self.status_signal.emit("No speech detected.")
                    if not self.continuous:
                        break
                    continue
                self.status_signal.emit("🧠 Transcribing...")
                asr_text = transcribe_audio(audio_path)
                
                if not asr_text.strip():
                    if not self.continuous:
                        break
                    continue

                current_src = self.src

                if self.auto_detect:
                    detected = detect_language(asr_text)
                    if detected in SUPPORTED_LANG.values():
                        current_src = detected

                if (current_src, self.tgt) not in self.translator_cache:
                    self.status_signal.emit("⏳ Loading translation model...")
                    self.translator_cache[(current_src, self.tgt)] = TextTranslator(current_src, self.tgt)

                translator = self.translator_cache[(current_src, self.tgt)]
                translated = translator.translate(asr_text)

                self.status_signal.emit("🔊 Speaking translated text...")
                speak_text(translated, self.tgt)

                self.result_signal.emit(asr_text, translated)
                if not self.continuous:
                    self.running = False
                    break

        except Exception as e:
            print("Worker Error:", e)

    def stop(self):
        self.running = False


# ---------------------------
# Main GUI Window
# ---------------------------

class TranslatorGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Svarnuvad Translator")
        self.setGeometry(200, 200, 600, 500)

        self.translator_cache = {}
        self.worker = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.src_combo = QComboBox()
        self.src_combo.addItems(SUPPORTED_LANG.keys())

        self.tgt_combo = QComboBox()
        self.tgt_combo.addItems(SUPPORTED_LANG.keys())

        self.auto_checkbox = QCheckBox("Auto Detect Source Language")
        self.continuous_checkbox = QCheckBox("Continuous Mode")

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        self.start_button = QPushButton("Start Translation")
        self.start_button.clicked.connect(self.start_translation)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_translation)
        self.stop_button.setEnabled(False)

        layout.addWidget(QLabel("Source Language"))
        layout.addWidget(self.src_combo)

        layout.addWidget(QLabel("Target Language"))
        layout.addWidget(self.tgt_combo)

        layout.addWidget(self.auto_checkbox)
        layout.addWidget(self.continuous_checkbox)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def start_translation(self):
        self.output_box.clear()
        self.output_box.append("Initializing...")

        src_name = self.src_combo.currentText()
        tgt_name = self.tgt_combo.currentText()

        src = SUPPORTED_LANG[src_name]
        tgt = SUPPORTED_LANG[tgt_name]

        auto_detect = self.auto_checkbox.isChecked()
        continuous = self.continuous_checkbox.isChecked()

        self.worker = TranslatorWorker(
            src, tgt, auto_detect,
            self.translator_cache,
            continuous
        )

        self.worker.result_signal.connect(self.display_result)
        self.worker.status_signal.connect(self.update_status)

        self.worker.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_translation(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_status(self, message):
        self.output_box.append(message)

    def display_result(self, asr, translated):
        self.output_box.clear()
        self.output_box.append("🗣 You said:")
        self.output_box.append(asr)
        self.output_box.append("")
        self.output_box.append("🌍 Translation:")
        self.output_box.append(translated)
        self.output_box.append("\n-----------------------------\n")
        self.output_box.append("Click Start to translate again.")


# ---------------------------
# Run Application
# ---------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorGUI()
    window.show()
    sys.exit(app.exec())
