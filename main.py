import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
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
    chart.setTitleFont(QFont("Times font", 20))
    chart.setTitle(f"Диаграмма оценки")

    # Создание виджета для отображения диаграммы
    chart_view = QChartView(chart)
    #chart_view.setRenderHint(QChartView.Antialiasing)

    return chart_view

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(650, 250, 570, 570)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RageAlert")
        self.setWindowIcon(QIcon("C:\\Users\\Setup\\Desktop\\trpp_project_py\\minimalistic_icon.png"))

        self.image_label = QLabel(self)
        pixmap = QPixmap('C:\\Users\\Setup\\Desktop\\trpp_project_py\\RAGE_ALERT.png')
        self.image_label.setPixmap(pixmap)
        self.image_label.setGeometry(10, 10, pixmap.width(), pixmap.height())
        self.image_label.setAlignment(Qt.AlignCenter)

        self.post_label = QLabel(self)
        self.post_label.setFont(QFont("Times font", 16))
        self.post_label.setText("Введите текст поста: ")
        self.post_label.move(130, 360)
        self.post_edit = QTextEdit(self)
        self.post_edit.setGeometry(130, 400, 320, 120)

        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.setGeometry(130, 530, 320, 30)
        self.analyze_button.clicked.connect(self.analyze_post)

        self.result_label = QLabel(self)
        self.result_label.setGeometry(20, 120, 360, 60)
        self.result_label.setAlignment(Qt.AlignCenter)

        #layout = QVBoxLayout()
        #layout.addWidget(self.pie_chart)

        #self.setLayout(layout)

        self.show()

    def analyze_post(self):
        post_text = self.post_edit.toPlainText()

        sent_model = SentimentModel()
        predictions = sent_model.predict(post_text)
        results = [float('{:.3f}'.format(predictions[_type]*100)) for _type in ["NEUTRAL", "POSITIVE", "NEGATIVE"]]
        pred_str = f"NEUTRAL: {results[0]}%\n" \
                   f"POSITIVE: {results[1]}%\n" \
                   f"NEGATIVE: {results[2]}%"

        self.pie_chart = create_pie_chart({"NEUTRAL": (results[0], QtGui.QColor("#F5D572")),
                                           "POSITIVE": (results[1], QtGui.QColor("#32CD32")),
                                           "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))})
        self.pie_chart.setFont(QFont("Times font", 20))

        layout = QVBoxLayout()
        layout.addWidget(self.pie_chart)

        self.image_label.hide()

        self.setLayout(layout)

        self.show()

        self.result_label.setText(pred_str)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


main()
