from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QPushButton

from CreatePieChart import create_pie_chart
from SentimentModel import SentimentModel
import globalVars


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
        # pred_str = f"POSITIVE: {results[0]}%\nNEUTRAL: {results[1]}%\nNEGATIVE: {results[2]}%"

        # формирование и выполнение запроса
        query = "INSERT INTO story (user_id, text, positive, neutral, negative)" \
                f" VALUES ('{globalVars.user_id}', '{text_to_analyze}', {results[0]}, {results[1]}, {results[2]})"
        globalVars.curs.execute(query)
        # "подтверждение" запроса
        globalVars.conn.commit()

        self.pie_chart = create_pie_chart({"POSITIVE": (results[0], QtGui.QColor("#32CD32")),
                                           "NEUTRAL": (results[1], QtGui.QColor("#F5D572")),
                                           "NEGATIVE": (results[2], QtGui.QColor("#FF3E3E"))}, list_bool=True)
        self.pie_chart.setFont(QFont("Times font", 20))

        self.pie_chart.setAlignment(Qt.AlignCenter)
        self.t_layout.addWidget(self.pie_chart)

        self.setLayout(self.layout)

    def go_to_main_screen(self):
        self.t_layout.removeWidget(self.pie_chart)
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() - 1)
