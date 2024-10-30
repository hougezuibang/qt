from login_ui import Ui_login  # 替换为你的 UI 类名
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication   
import PyQt5.QtCore as QtCore
class Loginwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login()  # 使用正确的 UI 类

        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明背景
        # self.ui.pushButton_2.clicked.connect(self.close)  # 关闭窗口
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))      # 显示主窗口
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))      # 显示注册窗口

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Loginwindow()  # 实例化登录窗口
    sys.exit(app.exec_())