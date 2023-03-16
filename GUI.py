import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Анализатор агрессии в постах")
        self.setGeometry(100, 100, 400, 200)

        self.post_label = QLabel(self)
        self.post_label.setText("Введите текст поста: ")
        self.post_label.move(20, 20)
        self.post_edit = QLineEdit(self)
        self.post_edit.setGeometry()