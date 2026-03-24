from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class HomeWin(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Svarnuvad")
        self.setGeometry(300, 200, 400, 400)

        layout = QVBoxLayout()

        title = QLabel("Svarnuvad")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.ocr_btn = QPushButton("Smart OCR")
        self.mic_btn = QPushButton("Translate using Microphone")
        self.system_audio_btn = QPushButton("Translate System Audio")
        self.exit_btn = QPushButton("Exit")

        layout.addWidget(self.ocr_btn)
        layout.addWidget(self.mic_btn)
        layout.addWidget(self.system_audio_btn)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)
