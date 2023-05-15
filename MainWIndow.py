from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import globalVars


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)
        self.pushButton.clicked.connect(self.go_to_screen2)
        self.pushButton.setStyleSheet("background-color : lightgrey")
        self.resButton.setEnabled(False)
        self.resButton.clicked.connect(self.go_to_screen3)
        self.resButton.setStyleSheet("background-color : lightgrey")

    def go_to_screen2(self):
        globalVars.screen2.init_ui(self.plainTextEdit.toPlainText())
        self.plainTextEdit.clear()
        self.resButton.setEnabled(True)
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() + 1)

    def go_to_screen3(self):
        globalVars.screen3.get_last_res()
        self.plainTextEdit.clear()
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() + 2)
