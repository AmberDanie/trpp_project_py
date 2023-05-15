from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QHBoxLayout

from CreatePieChart import create_pie_chart
import globalVars


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
        inputted_text = QLabel("Inputted text")
        inputted_text.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(percentage_text)
        layout.addWidget(diagram_text)
        layout.addWidget(inputted_text)

        self.info_layout.addLayout(layout)

        layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.top_layout)

    def get_last_res(self):
        query = "SELECT ROW_NUMBER() over() as number,* FROM story ORDER BY number DESC"
        globalVars.curs.execute(query)
        result_table = globalVars.curs.fetchall()
        query = "DELETE FROM story *"
        globalVars.curs.execute(query)
        globalVars.conn.commit()
        for row in result_table:
            layout = QHBoxLayout()
            row_pie = create_pie_chart({"POSITIVE": (row[3], QtGui.QColor("#32CD32")),
                                        "NEUTRAL": (row[4], QtGui.QColor("#F5D572")),
                                        "NEGATIVE": (row[2], QtGui.QColor("#FF3E3E"))}, list_bool=False)
            row_pie.setFixedSize(300, 300)
            img_url = 'images/angry.png'
            if max(row[2:5]) == row[3]:
                img_url = 'images/smile.png'
            elif max(row[2:5]) == row[4]:
                img_url = 'images/pokerface.png'
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

    @staticmethod
    def go_to_main_screen():
        globalVars.widget.setCurrentIndex(globalVars.widget.currentIndex() - 2)
