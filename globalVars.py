import sys

import psycopg2
from PyQt5.QtWidgets import QApplication, QStackedWidget

from MainWIndow import MainWindow
from Screen2 import Screen2
from Screen3 import Screen3
from config import host, port, user, password, dbname

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
