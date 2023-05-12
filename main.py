import sys
import psycopg2
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from SentimentModel import SentimentModel
from math import ceil
from config import host, user, password, dbname, port


def create_pie_chart(data: object) -> QWidget:
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
        # loadUi("C:\\Users\\Setup\\Desktop\\trpp_project_py\\mainWindow.ui", self)
        loadUi("mainWindow.ui", self)
        self.pushButton.clicked.connect(self.go_to_screen2)

    def go_to_screen2(self):
        screen2.init_ui(self.plainTextEdit.toPlainText())
        self.plainTextEdit.clear()
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Screen2(QWidget):
    def __init__(self):
        super().__init__()
        # подключение к бд
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
        )
        # создание курсора - выполняет запросы к бд
        self.curs = self.conn.cursor()
        self.setWindowTitle("Data")
        self.layout = QVBoxLayout()

    def init_ui(self, text_to_analyze):
        self.pie_chart = QWidget()
        post_text = text_to_analyze
        sent_model = SentimentModel()
        predictions = sent_model.predict(post_text)
        results = [float('{:.3f}'.format(predictions[_type] * 100)) for _type in ["POSITIVE", "NEUTRAL", "NEGATIVE"]]
        pred_str = f"POSITIVE: {results[0]}%\nNEUTRAL: {results[1]}%\nNEGATIVE: {results[2]}%"

        # формирование и выполнение запроса
        query = "INSERT INTO story (text, negative, positive, neutral)" \
                f" VALUES ('{text_to_analyze}', {results[2]}, {results[0]}, {results[1]})"
        self.curs.execute(query)
        # "подтверждение" запроса
        self.conn.commit()

        self.pie_chart = create_pie_chart({"POSITIVE": (results[0], QtGui.QColor("#32CD32")),
                                           "NEUTRAL": (results[1], QtGui.QColor("#F5D572")),
                                           "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))})
        self.pie_chart.setFont(QFont("Times font", 20))
        self.pie_button = QPushButton("Return")
        self.pie_button.clicked.connect(self.go_to_main_screen)

        self.pie_chart.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.pie_chart)
        self.layout.addWidget(self.pie_button)

        self.setLayout(self.layout)

    def go_to_main_screen(self):
        self.layout.removeWidget(self.pie_chart)
        self.layout.removeWidget(self.pie_button)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # вывод всех текстов за одну сессию (кроме последнего)
    def get_table(self):
        query = "SELECT ROW_NUMBER() over() as number,* FROM story ORDER BY number DESC"
        self.curs.execute(query)
        result_table = self.curs.fetchall()
        result_table[1:] # потому что без послденей проверки текста
        for row in result_table[1:]:
             print(row[1:])

    # очистка бд при удалении объекта
    def __del__(self):
        self.get_table()
        query = "DELETE FROM story *"
        self.curs.execute(query)
        self.conn.commit()


app = QApplication(sys.argv)
widget = QStackedWidget()
main_window = MainWindow()
screen2 = Screen2()
widget.addWidget(main_window)
widget.addWidget(screen2)
# widget.setWindowIcon(QIcon("C:\\Users\\Setup\\Desktop\\trpp_project_py\\minimalistic_icon.png"))
widget.setWindowIcon(QIcon("minimalistic_icon.png"))
widget.setWindowTitle("QRage")
widget.show()
sys.exit(app.exec_())
