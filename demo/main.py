from login_ui import Ui_login  # 导入登录界面相关的 UI 类
from home_ui import Ui_home  # 导入主窗口界面相关的 UI 类
from my_ui import Ui_my  # 导入设置界面相关的 UI 类

import pymysql
import sys
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QApplication   
import PyQt5.QtCore as QtCore

class Database:
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='ceshi_login',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def fetch_all_users(self):
        self.cur.execute("SELECT * FROM user")
        return self.cur.fetchall()

    def insert_user(self, username, password):
        try:
            self.cur.execute("INSERT INTO user(name, password) VALUES(%s, %s)", (username, password))
            self.conn.commit()
            print('注册成功')
        except pymysql.Error as e:
            print(f'注册过程中发生错误: {e}')

    def close(self):
        self.cur.close()
        self.conn.close()

class Loginwindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_login()  # 使用正确的 UI 类
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明背景

        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))  # 显示主窗口
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  # 显示注册窗口
        self.ui.pushButton.clicked.connect(self.logintohome)  # 登录到主页
        self.ui.pushButton_2.clicked.connect(self.zhuce)  # 注册

        self.user_data = self.db.fetch_all_users()  # 缓存用户数据
        self.show()

    def zhuce(self):
        username = self.ui.lineEdit_4.text()
        password = self.ui.lineEdit_9.text()
        password1 = self.ui.lineEdit_3.text()

        if username and password and password == password1:
            self.db.insert_user(username, password)
            
        else:
            print('用户名和密码不能为空，或密码不一致')

    def logintohome(self):
        self.user_data = self.db.fetch_all_users()  # 缓存用户数据
        lineEdit = self.ui.lineEdit.text()
        lineEdit_2 = self.ui.lineEdit_2.text()
# TOOD  待维护
# TOOD (待维护)
        user_found = next((i for i in self.user_data if lineEdit == i[0] and lineEdit_2 == i[1]), None)
        if user_found:
            print('登录成功')
            self.succeed_login()
        else:
            print('用户名或密码错误')

    def succeed_login(self):
        self.hide()
        self.home_window = homewindow(self.db)
        self.home_window.show()
        # user=self.ui.lineEdit.text()
        # password=self.ui.lineEdit_2.text()
        self.close()

class homewindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_home()  # 使用正确的 UI 类
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明背景

        self.ui.bili_bun.clicked.connect(lambda: webbrowser.open('https://www.bilibili.com'))
        self.ui.baidu_btn.clicked.connect(lambda: webbrowser.open('https://www.baidu.com'))
        self.ui.douyin_btn.clicked.connect(lambda: webbrowser.open('https://www.douyin.com'))
        self.ui.tengxun_btn.clicked.connect(lambda: webbrowser.open('https://www.qq.com'))
        self.ui.login_btn.clicked.connect(self.tologin)
        self.ui.mybtn.clicked.connect(self.tomy)
        self.ui.exit.clicked.connect(self.close)
        self.show()
    def tomy(self):
        self.hide()  # 隐藏当前窗口
        try:
            self.my_window = MyWindows(self.db)  # 实例化 MyWindows
            self.my_window.show()  # 显示 MyWindows
        except Exception as e:
            print(f"打开 MyWindows 时发生错误: {e}")  # 打印错误信息
    def close(self):
        self.hide()
        # self.login_window = Loginwindow(self.db)
        # self.login_window.show()
        exit()
    def tologin(self):
        self.hide()
        self.login_window = Loginwindow(self.db)
        self.login_window.show()
class MyWindows(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_my()  # 使用正确的 UI 类
        self.ui.setupUi(self)  # 设置UI
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.show()  # 显示窗口
        # self.ui.lineEdit.text().values()=self.db.fetch_all_users()
        value = self.db.fetch_all_users()
        # self.ui.lineEdit.setText(value)  # 使用 setText() 方法设置文本
        print("self.db.fetch_all_users()")
        print(value)
        self.ui.lineEdit_2.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database()
    win = Loginwindow(db)  # 实例化登录窗口
    sys.exit(app.exec_())
    db.close()

