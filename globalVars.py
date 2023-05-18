import sys

import geocoder

import psycopg2
from PyQt5.QtWidgets import QApplication, QStackedWidget

from MainWIndow import MainWindow
from Screen2 import Screen2
from Screen3 import Screen3
from config import host, port, user, password, dbname, generate_key

conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    dbname=dbname,
)
user_id = ''.join(list(map(generate_key, geocoder.ip('me').ip.split('.'))))
curs = conn.cursor()
app = QApplication(sys.argv)
widget = QStackedWidget()
main_window = MainWindow()
screen2 = Screen2()
screen3 = Screen3()
