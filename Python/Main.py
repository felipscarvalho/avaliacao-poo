from PyQt6.QtWidgets import QApplication
from App import App
import sys

app = QApplication(sys.argv)
appExec = App()
appExec.show()
sys.exit(app.exec())
