from PyQt5.QtChart import QPieSeries, QPieSlice, QChart, QChartView
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget


def create_pie_chart(data: object, list_bool) -> QWidget:
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
    if list_bool:
        chart.setTitle(f"Диаграмма оценки")
        chart.setAnimationDuration(2500)
    else:
        chart.legend().hide()
        chart.setAnimationDuration(0)

    # Создание виджета для отображения диаграммы
    chart_view = QChartView(chart)

    return chart_view
