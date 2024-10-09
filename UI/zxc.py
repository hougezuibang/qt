import random
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton
import sys


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("布局")  # 设置窗口名称
        self.resize(800, 800)       # 设置窗口大小

        # 创建一个中心小部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建一个垂直布局管理器
        layout = QVBoxLayout(self.central_widget)

        # 创建一个按钮并添加到布局中
        self.button = QPushButton('点击我', self.central_widget)
        self.button.setMinimumSize(50, 50)  # 设置最小尺寸
        self.button.setMaximumSize(50, 50)  # 设置最大尺寸
        layout.addWidget(self.button)       # 设置布局
        self.button.clicked.connect(self.on_button_clicked)  # 将按钮的clicked信号连接到槽函数

    def on_button_clicked(self):  # Button槽函数
        random1 = random.randint(0, 800)
        random2 = random.randint(0, 800)
        self.button.move(random1, random2)
        print("xxxxxx")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
