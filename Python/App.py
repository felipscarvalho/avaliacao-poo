import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análise do SISU-UFS")
        self.setGeometry(700, 300, 800, 600)
        # self.setWindowIcon(QIcon("profile"))

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        headerWidget = QWidget()
        headerWidget.setFixedHeight(80)
        headerWidget.setStyleSheet(
            """background-color: white; border-bottom: 0px solid #d0d0d0;"""
        )

        headerLayout = QHBoxLayout(headerWidget)
        titleLabel = QLabel("Análise de Dados - SISU | UFS")
        titleLabel.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        headerLayout.addWidget(titleLabel)

        headerLayout.addStretch()

        self.graphArea = QWidget()
        self.graphArea.setStyleSheet("background-color: rgb(200, 200, 200);")

        mainLayout.addWidget(headerWidget)
        mainLayout.addWidget(self.graphArea)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
