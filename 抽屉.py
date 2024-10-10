from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QStackedLayout


class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self):
        self.resize(800, 800)       # 设置窗口大小
        cout1 = QVBoxLayout(self)
        self.cout = QStackedLayout()

        cout1.addLayout(self.cout)

        self.window_1 = win1()
        self.window_2 = win2()
        self.but_1 = QtWidgets.QPushButton("抽屉1")
        self.but_2 = QtWidgets.QPushButton("抽屉2")
        self.but_1.clicked.connect(self.win1show)
        self.but_2.clicked.connect(self.win2show)
        self.cout.addWidget(self.window_1)
        self.cout.addWidget(self.window_2)
        self.cout.addWidget(self.but_1)
        self.cout.addWidget(self.but_2)
        cout1.addLayout(self.cout)
    def win1show(self):
        self.cout.setCurrentIndex(0)
    def win2show(self):
        self.cout.setCurrentIndex(1)
class win1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽屉1")
        label = QtWidgets.QLabel("这是抽屉1", self)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)
class win2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽屉2")
        label = QtWidgets.QLabel("这是抽屉2", self)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == '__main__':
    app =QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.setupUi()
    mainWindow.show()
    sys.exit(app.exec_())
