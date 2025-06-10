import sys
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import pygame

# Caminho onde o áudio é gerado (ajusta se for diferente)
CAMINHO_AUDIO = "voz_sara/output.wav"
BACKEND_URL = "http://localhost:8001/falar"  # Ou outro endpoint como /ia

class SaraUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sara")
        self.setGeometry(100, 100, 500, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        self.image_label = QLabel()
        pixmap = QPixmap("logo_jhca_optimized.png")  # Ou imagem da Sara
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.enviar_mensagem)
        layout.addWidget(self.input_field)

        self.setLayout(layout)

        pygame.mixer.init()

    def enviar_mensagem(self):
        texto = self.input_field.text().strip()
        if not texto:
            return

        self.chat_display.append(f"<b>Tu:</b> {texto}")
        self.input_field.clear()

        try:
            resposta = requests.post(BACKEND_URL, json={"texto": texto})
            resposta_json = resposta.json()
            mensagem = resposta_json.get("resposta", "[Sem resposta]")

            self.chat_display.append(f"<b>Sara:</b> {mensagem}")

            if os.path.exists(CAMINHO_AUDIO):
                pygame.mixer.music.load(CAMINHO_AUDIO)
                pygame.mixer.music.play()
        except Exception as e:
            self.chat_display.append(f"<b>Erro:</b> {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = SaraUI()
    janela.show()
    sys.exit(app.exec_())

