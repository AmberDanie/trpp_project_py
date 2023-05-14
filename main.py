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


def create_pie_chart(data: object, listBool) -> QWidget:
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
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.setAnimationEasingCurve(QEasingCurve.InCurve)
    for i in range(3):
        chart.legend().markers()[i].setFont(QFont("Times font", 15))

    chart.setBackgroundVisible(False)
    if listBool:
        chart.setTitle(f"Диаграмма оценки")
        chart.setAnimationDuration(2500)
    else:
        chart.legend().hide()
        chart.setAnimationDuration(0)

    # Создание виджета для отображения диаграммы
    chart_view = QChartView(chart)

    return chart_view


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
        screen2.init_ui(self.plainTextEdit.toPlainText())
        self.plainTextEdit.clear()
        self.resButton.setEnabled(True)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_screen3(self):
        screen3.get_last_res()
        self.plainTextEdit.clear()
        widget.setCurrentIndex(widget.currentIndex() + 2)


class Screen2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data")
        self.layout = QVBoxLayout()
        self.t_layout = QStackedLayout()

        self.pie_chart = QWidget()
        self.pie_button = QPushButton("Return")
        self.pie_button.clicked.connect(self.go_to_main_screen)

        self.layout.addLayout(self.t_layout)
        self.layout.addWidget(self.pie_button)

    def init_ui(self, text_to_analyze: str):
        self.pie_chart = QWidget()
        post_text = text_to_analyze.lower()
        sent_model = SentimentModel()
        predictions = sent_model.predict(post_text)
        results = [float('{:.3f}'.format(predictions[_type] * 100)) for
                   _type in ["POSITIVE", "NEUTRAL", "NEGATIVE"]]
        pred_str = f"POSITIVE: {results[0]}%\nNEUTRAL: {results[1]}%\nNEGATIVE: {results[2]}%"

        # формирование и выполнение запроса
        query = "INSERT INTO story (text, positive, neutral, negative)" \
                f" VALUES ('{text_to_analyze}', {results[0]}, {results[1]}, {results[2]})"
        curs.execute(query)
        # "подтверждение" запроса
        conn.commit()

        self.pie_chart = create_pie_chart({"POSITIVE": (results[0], QtGui.QColor("#32CD32")),
                                           "NEUTRAL": (results[1], QtGui.QColor("#F5D572")),
                                           "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))}, listBool=True)
        self.pie_chart.setFont(QFont("Times font", 20))

        self.pie_chart.setAlignment(Qt.AlignCenter)
        self.t_layout.addWidget(self.pie_chart)

        self.setLayout(self.layout)

    def go_to_main_screen(self):
        self.t_layout.removeWidget(self.pie_chart)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # вывод всех текстов за одну сессию (кроме последнего)
    def get_table(self):
        query = "SELECT ROW_NUMBER() over() as number,* FROM story ORDER BY number DESC"
        curs.execute(query)
        result_table = curs.fetchall()
        for row in result_table:
            print(row[1:])

    # очистка бд при удалении объекта
    def __del__(self):
        self.get_table()
        query = "DELETE FROM story *"
        curs.execute(query)
        conn.commit()


class Screen3(QWidget):
    def __init__(self):
        super().__init__()

        self.top_layout = QVBoxLayout(self)
        self.setLayout(self.top_layout)
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout()
        self.info_layout.addStretch()
        self.info_widget.setLayout(self.info_layout)

        self.scrollable_area = QScrollArea()
        self.scrollable_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollable_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollable_area.setWidgetResizable(True)
        self.scrollable_area.setWidget(self.info_widget)

        self.returnButton = QPushButton("Return")
        self.returnButton.clicked.connect(self.go_to_main_screen)
        self.top_layout.addWidget(self.scrollable_area)
        self.top_layout.addWidget(self.returnButton)

        percentage_text = QLabel("Percentage")
        percentage_text.setAlignment(Qt.AlignCenter)
        diagram_text = QLabel("Diagram")
        diagram_text.setAlignment(Qt.AlignCenter)
        inputed_text = QLabel("Inputed text")
        inputed_text.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(percentage_text)
        layout.addWidget(diagram_text)
        layout.addWidget(inputed_text)

        self.info_layout.addLayout(layout)

        layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.top_layout)


    def get_last_res(self):
        query = "SELECT ROW_NUMBER() over() as number,* FROM story ORDER BY number DESC"
        curs.execute(query)
        result_table = curs.fetchall()
        query = "DELETE FROM story *"
        curs.execute(query)
        conn.commit()
        for row in result_table:
            layout = QHBoxLayout()
            row_pie = create_pie_chart({"POSITIVE": (row[3], QtGui.QColor("#32CD32")),
                                        "NEUTRAL": (row[4], QtGui.QColor("#F5D572")),
                                        "NEGATIVE": (row[2], QtGui.QColor("#FF3E3E"))}, listBool=False)
            row_pie.setFixedSize(300, 300)
            img_url = 'angry.png'
            if max(row[2:5]) == row[3]:
                img_url = 'smile.png'
            elif max(row[2:5]) == row[4]:
                img_url = 'pokerface.png'
            row_pie.setStyleSheet(f"background-image: url({img_url});"
                                  "background-position: center;"
                                     "background-repeat: no-repeat; "
                                     "background-attachment: fixed; "
                                     "background-size: 100% 100%;")
            pred_str = f"POSITIVE: {row[3]}%\nNEUTRAL: {row[4]}%\nNEGATIVE: {row[2]}%"
            text_label = QLabel()
            text_label.setAlignment(Qt.AlignCenter)
            stat_label = QLabel(pred_str)
            stat_label.setAlignment(Qt.AlignCenter)
            stat_label.setStyleSheet('width: 33%; text-align="center"')
            text_label.setStyleSheet("width: 33%; text-align='center'")
            if row[1]:
                text_label.setText(row[1])
            else:
                text_label.setText("<<empty>>")

            layout.addWidget(stat_label)
            layout.addWidget(row_pie)
            layout.addWidget(text_label)

            self.info_layout.addLayout(layout)


    def go_to_main_screen(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)


# подключение к бд
conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    dbname=dbname,
)
curs = conn.cursor()

app = QApplication(sys.argv)
widget = QStackedWidget()
main_window = MainWindow()
screen2 = Screen2()
screen3 = Screen3()

widget.addWidget(main_window) # 0
widget.addWidget(screen2) # 1
widget.addWidget(screen3) # 2

widget.setWindowIcon(QIcon("minimalistic_icon.png"))
widget.setWindowTitle("QRage")
widget.show()
sys.exit(app.exec_())
