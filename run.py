import sys

from PyQt5.QtWidgets import QApplication
from Frames.Ui_main_window import Ui_MainWindow

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = Ui_MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)