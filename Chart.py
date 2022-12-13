from PyQt5.QtWidgets import QMainWindow, QLabel
from PriceBit import price
from matplotlib import pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from random import choice
import os
from graph import Ui_MainWindow as Ui_Graph


class Graph(QMainWindow, Ui_Graph):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.back_in_menu = args
        self.initUI()

    def initUI(self):
        self.move(500, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.label_graph = QLabel(self)
        self.label_graph.move(65, 196)
        self.label_graph.setStyleSheet('background-color: rgb(46, 52, 54)')
        self.pushButton.clicked.connect(self.graph)
        self.pushButton_2.clicked.connect(self.graph)
        self.pushButton_3.clicked.connect(self.graph)
        self.pushButton_4.clicked.connect(self.graph)
        self.pushButton_5.clicked.connect(self.exit)
        self.show()

    def graph(self):
        text_button = self.sender().text()
        prices = price(text_button)
        all_price = list(map(lambda x: float(x[4]), prices))
        plt.figure(figsize=(6.7, 3))
        if len(all_price) in (7, 24, 28, 29, 30, 31):
            x = [day_hour for day_hour in range(1, len(all_price) + 1)]
        else:
            x = [minute for minute in range(1, 5)]
        plt.plot(x, all_price, 'o-k')
        plt.grid(True)

        alp = list(map(chr, range(ord('a'), ord('z')+1)))
        file_name = ''
        for i in range(7):
            file_name += choice(alp)
        plt.savefig(file_name)

        pixmap = QPixmap(file_name)
        self.label_graph.setPixmap(pixmap)
        self.label_graph.adjustSize()
        os.remove(file_name + '.png')

    def exit(self):
        self.back_in_menu[0].show()
        self.close()
