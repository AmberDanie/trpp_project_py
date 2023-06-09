import sys

from PyQt5.QtGui import QIcon

import globalVars


class CreateApp:
    def __init__(self):
        globalVars.widget.addWidget(globalVars.main_window)  # 0
        globalVars.widget.addWidget(globalVars.screen2)  # 1
        globalVars.widget.addWidget(globalVars.screen3)  # 2

        globalVars.widget.setFixedSize(1200, 780)
        globalVars.widget.setWindowIcon(QIcon("images/pie-chart-icon.png"))
        globalVars.widget.setWindowTitle("QRage")
        globalVars.widget.show()
        sys.exit(globalVars.app.exec_())

    def __del__(self):
        query = f"DELETE FROM story * WHERE user_id = '{globalVars.user_id}'"
        globalVars.curs.execute(query)
        globalVars.conn.commit()
