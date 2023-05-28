from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

import globalVars


class MainWindow(QMainWindow):
    """
    Realise switching between windows of application
    """

    def __init__(self):
        """
        Show main window
        Contains text panel for entering analyzed text,
        buttons for analyzing text and showing previous results
        """
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)
        self.pushButton.clicked.connect(self.go_to_screen2)
        self.resButton.setEnabled(False)
        self.resButton.clicked.connect(self.go_to_screen3)

    def go_to_screen2(self):
        """
        Shows second window
        Contains analyzed text diagram with sentimental marks: positive, neutral, negative
        """
        globalVars.screen2.init_ui(self.plainTextEdit.toPlainText())
        self.plainTextEdit.clear()
        self.resButton.setEnabled(True)
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() + 1)

    def go_to_screen3(self):
        """
        Shows third window
        Contains window with all diagrams of analyzed text from previous tries
        """
        globalVars.screen3.get_last_res()
        self.plainTextEdit.clear()
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() + 2)
