import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from SentimentModel import SentimentModel
from math import ceil


def create_pie_chart(data: object) -> QWidget:
    """

    :rtype: object
    """
    # Создание серии диаграммы
    series = QPieSeries()
    series.setHoleSize(0.5)

    # Добавление данных в серию
    for label, (value, color) in data.items():
        _slice = QPieSlice(label, value)
        _slice.setBrush(color)
        series.append(_slice)

    # Создание диаграммы
    chart = QChart()
    chart.addSeries(series)
    chart.setTitleFont(QFont("Times font", 20))
    chart.setTitle(f"Диаграмма оценки")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.setAnimationEasingCurve(QEasingCurve.InCurve)
    chart.setAnimationDuration(2500)
    for i in range(3):
        chart.legend().markers()[i].setFont(QFont("Times font", 15))

    # Создание виджета для отображения диаграммы
    chart_view = QChartView(chart)

    return chart_view


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("C:\\Users\\Setup\\Desktop\\trpp_project_py\\mainWindow.ui", self)
        self.pushButton.clicked.connect(self.go_to_screen2)

    def go_to_screen2(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        screen2.init_ui(self.plainTextEdit.toPlainText())


class Screen2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data")
        self.pie_chart = QWidget()

    def init_ui(self, text_to_analyze):
        post_text = text_to_analyze
        sent_model = SentimentModel()
        predictions = sent_model.predict(post_text)
        results = [float('{:.3f}'.format(predictions[_type] * 100)) for _type in ["POSITIVE", "NEUTRAL", "NEGATIVE"]]
        # pred_str = f"POSITIVE: {results[0]}%\n" \ # НА БУДУЩЕЕ
        #           f"NEUTRAL: {results[1]}%\n" \
        #           f"NEGATIVE: {results[2]}%"

        self.pie_chart = create_pie_chart({"POSITIVE": (results[0], QtGui.QColor("#32CD32")),
                                           "NEUTRAL": (results[1], QtGui.QColor("#F5D572")),
                                           "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))})
        self.pie_chart.setFont(QFont("Times font", 20))

        layout = QVBoxLayout()
        self.pie_chart.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pie_chart)

        self.setLayout(layout)

        self.show()


app = QApplication(sys.argv)
widget = QStackedWidget()
main_window = MainWindow()
screen2 = Screen2()
widget.addWidget(main_window)
widget.addWidget(screen2)
widget.setWindowIcon(QIcon("C:\\Users\\Setup\\Desktop\\trpp_project_py\\minimalistic_icon.png"))
widget.setWindowTitle("QRage")
widget.show()
sys.exit(app.exec_())
