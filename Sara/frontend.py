from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import Qt
import requests, sys

class SaraUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sara")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.label = QLabel("Escreve para a Sara:")
        self.chat = QTextEdit()
        self.chat.setPlaceholderText("Mensagem...")
        self.chat.installEventFilter(self)
        layout.addWidget(self.label)
        layout.addWidget(self.chat)
        self.setLayout(layout)

    def eventFilter(self, obj, event):
        if obj == self.chat and event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            texto = self.chat.toPlainText().strip()
            if texto:
                resposta = self.enviar_para_backend(texto)
                self.label.setText(f"Sara: {resposta}")
                self.chat.clear()
            return True
        return super().eventFilter(obj, event)

    def enviar_para_backend(self, texto):
        try:
            r = requests.post("http://localhost:8001/responder",
                              json={"mensagem": texto, "emissor": "utilizador"})
            return r.json().get("resposta", "[sem resposta]")
        except:
            return "[erro de conexão]"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = SaraUI()
    janela.show()
    sys.exit(app.exec_())