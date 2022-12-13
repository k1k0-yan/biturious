import re
import os
import smtplib
import random
import uuid
import hashlib
import datetime

from forgotui import Ui_MainWindow as Ui_Forgot
from forgot2ui import Ui_MainWindow as Ui_Forgot2
from email.mime.text import MIMEText
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def check_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email)


def check_pass(test_str):
    allowed = set(string.digits + string.ascii_letters)
    return set(test_str) <= allowed


def check_acc(username, email):
    con = sqlite3.connect("auth.db")
    cur = con.cursor()
    true_email = cur.execute("""SELECT email FROM users 
                    WHERE login = ? """, (username, )).fetchall()
    return email == true_email[0][0]


def hash_password(password):
    salt = uuid.uuid4().hex
    os.environ['SALT'] = 'bK4-LbL-fT7-2WB'
    res = hashlib.sha512(os.getenv('SALT').encode() + salt.encode() + password.encode()).hexdigest() + ':' + salt
    os.environ.clear()
    return res


def send_code(email):
    code = random.randrange(100000, 999999)
    mail_user = 'bot@biturious.space'
    os.environ['MAIL_PASSWORD'] = 'XBG-dqP-3ES-Dbg'
    mail_pwd = os.getenv('MAIL_PASSWORD', '123456')
    content = """Пожалуйста, введите код в программу для завершения регистрации или восстановления пароля.
    Никому не сообщайте ваш код.
    Ваш код: """ + str(code)
    message = MIMEText(content, 'html')
    message['Subject'] = 'Личный код Biturious'
    message['From'] = mail_user
    message['To'] = email
    mail = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    mail.login(mail_user, mail_pwd)
    if not check_email(email):
        return False
    to = email
    mail.sendmail(mail_user, to, message.as_string())
    mail.quit()
    os.environ.clear()
    return code


class Forgot(QMainWindow, Ui_Forgot):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.main = args[0]
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit.setText(args[0].lineEdit.text())
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.restore)
        self.pushButton_5.clicked.connect(self.exit_app)

    def exit_app(self):
        self.close()
        self.main.show()

    def restore(self):
        self.label_2.setText('')
        self.label_6.setText('')
        self.label_7.setText('')

        login = self.lineEdit.text()
        email = self.lineEdit_2.text()

        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        logins = cur.execute("SELECT login FROM users").fetchall()
        emails = cur.execute("SELECT email FROM users").fetchall()

        res2 = []
        res = []

        for i in logins:
            for j in i:
                res.append(j)
        for i in emails:
            for j in i:
                res2.append(j)

        if not login:
            self.label_7.setText('Обязательно для заполнения')
            con.close()
            return 0
        elif login not in res:
            self.label_7.setText('Данного логина не существует')
            con.close()
            return 0
        elif not email:
            self.label_6.setText('Обязательно для заполнения')
            con.close()
            return 0
        elif email not in res2:
            self.label_6.setText('Данная почта не используется')
            con.close()
            return 0
        elif not check_acc(login, email):
            self.label_2.setText('Данная почта не соответсвует заданному логину')
            con.close()
            return 0

        con.commit()
        con.close()
        self.close()
        self.next = Forgot2(self, self.main)
        self.next.show()


class Forgot2(QMainWindow, Ui_Forgot2):
    def __init__(self, *args):
        super().__init__()
        self.main = args[1]
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_2.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_3.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.email = args[0].lineEdit_2.text()
        self.login = args[0].lineEdit.text()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.restore)
        self.true_code = send_code(self.email)
        self.pushButton_5.clicked.connect(self.exit_app)

    def exit_app(self):
        self.close()
        self.main.show()

    def restore(self):
        self.label_2.setText('')

        code = self.lineEdit.text()
        password1 = self.lineEdit_2.text()
        password2 = self.lineEdit_3.text()

        con = sqlite3.connect("auth.db")
        cur = con.cursor()

        if password1 != password2:
            self.label_2.setText('Введенные пароли отличаются')
            con.close()
            return 0
        elif not code:
            self.label_2.setText('Вы не ввели код')
            con.close()
            return 0
        elif int(self.true_code) != int(code):
            self.label_2.setText('Неверный код')
            con.close()
            return 0
        elif not password1 or not password2:
            self.label_2.setText('Вы не ввели пароль!')
            con.close()
            return 0
        elif not check_pass(password1):
            self.label_2.setText('Пароль содержит запрещенные символы')
            con.close()
            return 0

        true_password = cur.execute("""SELECT password FROM users 
                 WHERE login = ? """, (self.login,)).fetchall()

        cur.execute("INSERT INTO password_changes(user, time, old_password, new_password) VALUES(?, ?, ?, ?)",
                    (self.login, datetime.datetime.now(), true_password[0][0], hash_password(password1)))

        cur.execute("""UPDATE users 
                SET password = ? 
                WHERE login = ?""", (hash_password(password1), self.login))

        con.commit()
        con.close()
        self.exit_app()
