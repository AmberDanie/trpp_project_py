import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


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
        self.post_edit.setGeometry(20, 40, 360, 30)

        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.setGeometry(20, 80, 360, 30)
        self.analyze_button.clicked.connect(self.analyze_post)

        self.result_label = QLabel(self)
        self.result_label.setGeometry(20, 120, 360, 30)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.show()

    def analyze_post(self):
        post_text = self.post_edit.text()

        ## Тут будет код для анализа поста

        self.result_label.setText("Уровень агрессии: 50%")  # Потом изменю


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


main()
