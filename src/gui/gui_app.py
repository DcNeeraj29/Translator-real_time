import sys
import os
import pyttsx3
# Disable CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Preloading Whisper...")
from asr.speech_to_text import transcribe_audio

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox,
    QTextEdit, QVBoxLayout, QHBoxLayout,
    QCheckBox, QGroupBox
)

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont

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
        self.setGeometry(200, 200, 800, 600)

        self.translator_cache = {}
        self.worker = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # =========================
        # GLOBAL FONT
        # =========================
        self.setFont(QFont("Segoe UI", 10))

        # =========================
        # LANGUAGE SECTION
        # =========================
        lang_layout = QHBoxLayout()

        source_label = QLabel("Source")
        source_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        target_label = QLabel("Target")
        target_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        arrow_label = QLabel("→")
        arrow_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        arrow_label.setStyleSheet("color: #38BDF8;")

        self.src_combo = QComboBox()
        self.src_combo.addItems(SUPPORTED_LANG.keys())

        self.tgt_combo = QComboBox()
        self.tgt_combo.addItems(SUPPORTED_LANG.keys())

        lang_layout.addWidget(source_label)
        lang_layout.addWidget(self.src_combo)
        lang_layout.addSpacing(10)
        lang_layout.addWidget(arrow_label)
        lang_layout.addSpacing(10)
        lang_layout.addWidget(target_label)
        lang_layout.addWidget(self.tgt_combo)

        # =========================
        # OPTIONS SECTION
        # =========================
        options_layout = QHBoxLayout()

        self.continuous_checkbox = QCheckBox("Continuous Mode")
        self.auto_checkbox = QCheckBox("Auto Detect")

        options_layout.addSpacing(10)
        options_layout.addWidget(self.continuous_checkbox)
        options_layout.addSpacing(15)
        options_layout.addWidget(self.auto_checkbox)
        options_layout.addStretch()

        # =========================
        # TRANSLATION WINDOW
        # =========================
        translation_group = QGroupBox("Translation Window")
        translation_layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("You said...")
        self.input_text.setReadOnly(True)
        self.input_text.setMinimumHeight(120)

        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Translated text...")
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(120)

        translation_layout.addWidget(self.input_text)
        translation_layout.addWidget(self.output_text)

        translation_group.setLayout(translation_layout)

        # =========================
        # BUTTONS
        # =========================
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        button_layout.addWidget(self.stop_button)

        # =========================
        # ADD EVERYTHING
        # =========================
        main_layout.addLayout(lang_layout)
        main_layout.addLayout(options_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(translation_group)
        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # =========================
        # STYLING
        # =========================
        self.setStyleSheet("""
        QWidget {
            background-color: #0F172A;
            color: #F1F5F9;
            font-size: 13px;
        }

        QComboBox {
            background-color: #1E293B;
            border-radius: 6px;
            padding: 6px;
        }

        QGroupBox {
            border: 1px solid #334155;
            border-radius: 12px;
            margin-top: 10px;
            padding: 12px;
            font-weight: bold;
            color: #38BDF8;
        }

        QTextEdit {
            background-color: #1E293B;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #334155;
        }

        QPushButton {
            background-color: #38BDF8;
            color: #0F172A;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            min-width: 100px;
        }

        QPushButton:hover {
            background-color: #0EA5E9;
        }
        """)

        # Make STOP button secondary
        self.stop_button.setStyleSheet("""
        background-color: #334155;
        color: #F1F5F9;
        padding: 10px;
        border-radius: 8px;
        min-width: 100px;
        """)

        # =========================
        # CONNECT
        # =========================
        self.start_button.clicked.connect(self.start_translation)
        self.stop_button.clicked.connect(self.stop_translation)

    def start_translation(self):
        self.input_text.clear()
        self.output_text.clear()
        self.input_text.append("Initializing...")

        src = SUPPORTED_LANG[self.src_combo.currentText()]
        tgt = SUPPORTED_LANG[self.tgt_combo.currentText()]

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
        self.input_text.append(message)

    def display_result(self, asr, translated):
        self.input_text.setText(asr)
        self.output_text.setText(translated)

# ---------------------------
# Run Application
# ---------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorGUI()
    window.show()
    sys.exit(app.exec())
