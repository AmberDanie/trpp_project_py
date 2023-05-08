import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import *
from SentimentModel import SentimentModel
from math import ceil


def create_pie_chart(data):
    # Создание серии диаграммы
    series = QPieSeries()

    # Добавление данных в серию
    for label, (value, color) in data.items():
        _slice = QPieSlice(label, value)
        _slice.setBrush(color)
        series.append(_slice)

    # Создание диаграммы
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Кольцевая диаграмма")

    # Создание виджета для отображения диаграммы
    chart_view = QChartView(chart)
    #chart_view.setRenderHint(QChartView.Antialiasing)

    return chart_view

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Данные для кольцевой диаграммы
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RageAlert")
        self.setWindowIcon(QIcon("C:\\Users\\Setup\\Desktop\\trpp_project_py\\minimalistic_icon.png"))
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
        self.result_label.setGeometry(20, 120, 360, 60)
        self.result_label.setAlignment(Qt.AlignCenter)

        #layout = QVBoxLayout()
        #layout.addWidget(self.pie_chart)

        #self.setLayout(layout)

        self.show()

    def analyze_post(self):
        post_text = self.post_edit.text()

        sent_model = SentimentModel()
        predictions = sent_model.predict(post_text)
        results = [float('{:.3f}'.format(predictions[_type]*100)) for _type in ["NEUTRAL", "POSITIVE", "NEGATIVE"]]
        pred_str = f"NEUTRAL: {results[0]}%\n" \
                   f"POSITIVE: {results[1]}%\n" \
                   f"NEGATIVE: {results[2]}%"

        #self.pie_chart = create_pie_chart({"NEUTRAL": (results[0], QtGui.QColor("#F5D572")),
        #                                   "POSITIVE": (results[1], QtGui.QColor("#32CD32")),
        #                                   "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))})

        #layout = QVBoxLayout()
        #layout.addWidget(self.pie_chart)

        #self.setLayout(layout)

        #self.show()

        self.result_label.setText(pred_str)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


main()
