import sys

from PyQt5.QtWidgets import QApplication
from Frames.Ui_main_window import Ui_MainWindow


# Запуск основного окна приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
    