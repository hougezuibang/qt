from login_ui import Ui_login  # 替换为你的 UI 类名
from  home_ui import Ui_home # 替换为你的主窗口类名
import pymysql
import sys
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QApplication   
import PyQt5.QtCore as QtCore
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='ceshi_login',
    charset='utf8'
)
cur = conn.cursor()
cur.execute("select * from user")
result = cur.fetchall()
print(result)

class Loginwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login()  # 使用正确的 UI 类
        # self.ui = Ui_home()  # 使用正确的 UI 类

        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明背景
        # self.ui.pushButton_2.clicked.connect(self.close)  # 关闭窗口
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))      # 显示主窗口
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))      # 显示注册窗口
        self.ui.pushButton.clicked.connect(self.logintohome)  # 登录到主页
        self.ui.pushButton_2.clicked.connect(self.zhuce)  # 登录到主页
        self.show()
    def zhuce(self):
                username = self.ui.lineEdit_4.text()
                password = self.ui.lineEdit_9.text()
                password1 = self.ui.lineEdit_3.text()
                # 直接获取输入框内容，避免多次调用方法
                if username and password==password1:
                    try:
                        # 使用参数化查询插入用户
                        cur.execute("INSERT INTO user(user, password) VALUES(%s, %s)", (username, password))
                        conn.commit()  # 提交事务
                        print('注册成功')
                    except pymysql.Error as e:
                        print(f'注册过程中发生错误: {e}')
                else:
                    print('用户名和密码不能为空')
    def logintohome(self):
        lineEdit = self.ui.lineEdit.text()
        lineEdit_2 = self.ui.lineEdit_2.text()

        try:
            # 直接判断结果集是否含有对应的用户名和密码
            user_found = next((i for i in result if lineEdit == i[0] and lineEdit_2 == i[1]), None)

            if user_found:
                print('登录成功')
                self.ui = homewindow()
                self.close()
            else:
                print('用户名或密码错误')
        except Exception as e:
            print(f'登录过程中发生错误: {e}')
            

        
        
        # self.ui.stackedWidget.setCurrentIndex(0)
        
class homewindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =  Ui_home()  # 使用正确的 UI 类
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明背景
        # self.ui.pushButton.clicked.connect(self.logintohome)  # 关闭窗口
        # self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))      # 显示主窗口
        # self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))      # 显示注册窗口
        self.ui.bili_bun.clicked.connect(lambda: webbrowser.open('https://www.bilibili.com'))
        self.ui.baidu_btn.clicked.connect(lambda: webbrowser.open('https://www.baidu.com'))
        self.ui.douyin_btn.clicked.connect(lambda: webbrowser.open('https://www.douyin.com'))
        self.ui.tengxun_btn.clicked.connect(lambda: webbrowser.open('https://www.qq.com'))
        self.ui.login_btn.clicked.connect(self.tologin) 
        self.ui.exit.clicked.connect(self.close)
        self.show()
    def close(self):
        # self.ui = Loginwindow()
        self.close()
        exit()

    def tologin(self):
        self.ui = Loginwindow()
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Loginwindow()  # 实例化登录窗口
    sys.exit(app.exec_())
    for i in range(10):
        print('test')
