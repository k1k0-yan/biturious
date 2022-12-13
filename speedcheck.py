import speedtest
import time

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from speedtestui import Ui_MainWindow as Ui_Speedtest

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        for i in range(101):
            time.sleep(0.21)
            self.countChanged.emit(i)


class External2(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        for i in range(3):
            st = speedtest.Speedtest()
            if i == 0:
                try:
                    self.countChanged.emit(int(st.download()))
                except speedtest.ConfigRetrievalError:
                    print('[ERROR] Timed out.')
            elif i == 1:
                try:
                    self.countChanged.emit(int(st.upload()))
                except speedtest.ConfigRetrievalError:
                    print('[ERROR] Timed out.')
            else:
                self.countChanged.emit(st.results.ping)


class Speedtest(QMainWindow, Ui_Speedtest):
    def __init__(self, *args):
        super().__init__()
        self.ex = args[0]
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.exit_app)
        self.thread = External()
        self.thread.countChanged.connect(self.progressbar_update)
        self.thread.start()
        self.thread2 = External2()
        self.thread2.countChanged.connect(self.labels_change)
        self.thread2.start()
        self.counter = 0

    def exit_app(self):
        self.close()
        self.ex.show()

    def labels_change(self, value):
        if self.counter == 0:
            value /= 8
            if value > 1024:
                value /= 1024
                if value > 1024:
                    value /= 1024
                    self.label_3.setText('Скорость загрузки: ' + str(round(value, 2)) + ' Мб/с')
                else:
                    self.label_3.setText('Скорость загрузки: ' + str(round(value, 2)) + ' Кб/с')
            else:
                self.label_3.setText('Скорость загрузки: ' + str(round(value, 2)) + ' Б/с')
        elif self.counter == 1:
            value /= 8
            if value > 1024:
                value /= 1024
                if value > 1024:
                    value /= 1024
                    self.label_4.setText('Скорость отдачи: ' + str(round(value, 2)) + ' Мб/с')
                else:
                    self.label_4.setText('Скорость отдачи: ' + str(round(value, 2)) + ' Кб/с')
            else:
                self.label_4.setText('Скорость отдачи: ' + str(round(value, 2)) + ' Б/с')
        else:
            self.label_5.setText('Пинг: ' + str(value))
            self.thread.terminate()
            self.progressBar.setValue(100)
        self.counter += 1

    def progressbar_update(self, value):
        self.progressBar.setValue(value)
