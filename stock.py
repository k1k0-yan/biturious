import sys

from PyQt5.QtWidgets import QMainWindow
from parse import parse
from PyQt5.QtCore import Qt
from binance_api import client
from stockui import Ui_MainWindow as Ui_Stock


class Stock(QMainWindow, Ui_Stock):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.back_in_menu = args
        self.label.setText(parse())
        self.initUI()

    def initUI(self):
        self.move(500, 150)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.pushButton_3.clicked.connect(self.buttons)
        try:
            coins = (client.get_account()['balances'])
            rubles, btc = 0, 0
            for coin in coins:
                if coin['asset'] == 'RUB':
                    rubles = coin['free']
                elif coin['asset'] == 'BTC':
                    btc = coin['free']
            self.green.setText(f'Баланс: {round(float(rubles), 2)}₽')
            self.red.setText(f'Доступно: {round(float(btc), 2)} BTC')
        except:
            self.plainTextEdit.setPlainText('ERROR\n\nПрочитайте "Помощь в покупке и продаже Bitcoin"')
        self.pushButton.clicked.connect(self.buttons)
        self.pushButton_2.clicked.connect(self.buttons)
        self.pushButton_4.clicked.connect(self.exit)

    def buttons(self):
        self.button = self.sender().text()
        if self.button == 'Обновить':
            self.label.setText(parse())
        elif self.button == 'Купить' or self.button == 'Продать':
            self.deal()

    def deal(self):
        quantity = self.lineEdit.text()
        if ',' in quantity:
            quantity = quantity.replace(',', '.')
        try:
            if self.button == 'Купить':
                order = client.order_market_buy(
                    symbol='BTCRUB',
                    quantity=float(quantity))
            elif self.button == 'Продать':
                order = client.order_market_sell(
                    symbol='BTCRUB',
                    quantity=float(quantity))
            self.plainTextEdit.setPlainText(' ')
        except:
            self.plainTextEdit.setPlainText('ERROR\n\nПрочитайте "Помощь в покупке и продаже Bitcoin"')

    def exit(self):
        self.back_in_menu[0].show()
        self.close()
