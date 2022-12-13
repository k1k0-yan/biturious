from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from help import Ui_MainWindow as Ui_Help


class Help(QMainWindow, Ui_Help):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.back_in_menu = args
        self.initUI()

    def initUI(self):
        self.move(500, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.exit)
        self.show()

    def exit(self):
        self.back_in_menu[0].show()
        self.close()