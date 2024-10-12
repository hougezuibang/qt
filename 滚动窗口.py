from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout


class Ui_MainWindow(QtWidgets.QWidget):
    mas_list = pyqtSignal(str)
    i = int(0)
    def setupUi(self):
        self.resize(400, 400)       # 设置窗口大小
        qvbl = QHBoxLayout(self)
        qvbl_con = QVBoxLayout(self)
        qhbl = QHBoxLayout(self)
    
        btn_tijiao = QtWidgets.QPushButton(self)
        self.text_con = QtWidgets.QTextEdit(self)
        # qvbl_con.resize(600, 400)
        qvbl_con.addWidget(self.text_con)
        self.text_con.setStyleSheet("background-color:#666;")
        self.text_con.setFixedSize(300, 200)
        btn_tijiao.setText("提交")
        btn_tijiao.clicked.connect(self.tijiao)
        qvbl_con.addWidget(btn_tijiao)
        qhbl.addLayout(qvbl_con)        
        qvbl.addLayout(qhbl)
        self.setLayout(qvbl)
        self.mas_list.connect(self.set_mas)
    def tijiao(self):
        # print("提交成功")
        self.i += 1
        self.mas_list.emit(str(self.i))
        self.text_con.textCursor().insertText("收到信号"+str(self.i)+"\n")
        # print(mas)
    def set_mas(self,mas):
        print("输出数值"+mas)

        print(mas)
if __name__ == '__main__':
    app =QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.setupUi()
    mainWindow.show()
    sys.exit(app.exec_())
