from PyQt6.QtWidgets import QApplication
from App import JanelaPrincipal
import sys

app = QApplication(sys.argv)
janela = JanelaPrincipal()
janela.show()
sys.exit(app.exec())
