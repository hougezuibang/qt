# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\UI\计算器.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import sys
import math  # 确保引入math模块
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 80, 391, 87))
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(140, 180, 395, 205))
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_23 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_23, 0, 0, 1, 1)
        self.pushButton_22 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_22, 0, 1, 1, 1)
        self.pushButton_24 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_24, 0, 2, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_15, 0, 3, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_20, 1, 0, 1, 1)
        self.pushButton_21 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_21, 1, 1, 1, 1)
        self.pushButton_19 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_19, 1, 2, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_13, 1, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_16, 2, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_5, 3, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_6, 3, 2, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_17, 3, 3, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_7, 4, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_8, 4, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_9, 4, 2, 1, 1)
        self.pushButton_18 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_18, 4, 3, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_12, 5, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_11, 5, 1, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_10, 5, 2, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.widget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 5, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "计算器"))
        self.pushButton_23.setText(_translate("MainWindow", "%"))
        self.pushButton_22.setText(_translate("MainWindow", "CE"))
        self.pushButton_24.setText(_translate("MainWindow", "C"))
        self.pushButton_15.setText(_translate("MainWindow", "删除"))
        self.pushButton_20.setText(_translate("MainWindow", "1/x"))
        self.pushButton_21.setText(_translate("MainWindow", "平方"))
        self.pushButton_19.setText(_translate("MainWindow", "根号"))
        self.pushButton_13.setText(_translate("MainWindow", "/"))
        self.pushButton.setText(_translate("MainWindow", "1"))
        self.pushButton_2.setText(_translate("MainWindow", "2"))
        self.pushButton_3.setText(_translate("MainWindow", "3"))
        self.pushButton_16.setText(_translate("MainWindow", "*"))
        self.pushButton_4.setText(_translate("MainWindow", "4"))
        self.pushButton_5.setText(_translate("MainWindow", "5"))
        self.pushButton_6.setText(_translate("MainWindow", "6"))
        self.pushButton_17.setText(_translate("MainWindow", "-"))
        self.pushButton_7.setText(_translate("MainWindow", "7"))
        self.pushButton_8.setText(_translate("MainWindow", "8"))
        self.pushButton_9.setText(_translate("MainWindow", "9"))
        self.pushButton_18.setText(_translate("MainWindow", "+"))
        self.pushButton_12.setText(_translate("MainWindow", "+/-"))
        self.pushButton_11.setText(_translate("MainWindow", "0"))
        self.pushButton_10.setText(_translate("MainWindow", "."))
        self.pushButton_14.setText(_translate("MainWindow", "="))
        self.pushButton_14.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.pushButton.clicked.connect(lambda: self.textEdit.insertPlainText("1"))
        self.pushButton_2.clicked.connect(lambda: self.textEdit.insertPlainText("2"))
        self.pushButton_3.clicked.connect(lambda: self.textEdit.insertPlainText("3"))
        self.pushButton_4.clicked.connect(lambda: self.textEdit.insertPlainText("4"))
        self.pushButton_5.clicked.connect(lambda: self.textEdit.insertPlainText("5"))
        self.pushButton_6.clicked.connect(lambda: self.textEdit.insertPlainText("6"))
        self.pushButton_7.clicked.connect(lambda: self.textEdit.insertPlainText("7"))
        self.pushButton_8.clicked.connect(lambda: self.textEdit.insertPlainText("8"))
        self.pushButton_9.clicked.connect(lambda: self.textEdit.insertPlainText("9"))
        self.pushButton_10.clicked.connect(lambda: self.textEdit.insertPlainText("."))
        self.pushButton_11.clicked.connect(lambda: self.textEdit.insertPlainText("0"))
        
        self.pushButton_12.clicked.connect(self.positiveandnegative)# 正负号按钮
        self.pushButton_14.clicked.connect(self.content) # 计算按钮
        self.pushButton_15.clicked.connect(self.backspace)# 删除按钮
        
        self.pushButton_13.clicked.connect(lambda: self.textEdit.insertPlainText("/"))
        self.pushButton_16.clicked.connect(lambda: self.textEdit.insertPlainText("*"))
        self.pushButton_17.clicked.connect(lambda: self.textEdit.insertPlainText("-"))
        self.pushButton_18.clicked.connect(lambda: self.textEdit.insertPlainText("+"))
        self.pushButton_19.clicked.connect(self.sqrt_text) # 开方按钮
        self.pushButton_20.clicked.connect(self.onePart) # 分之一按钮
        self.pushButton_21.clicked.connect(self.square) # 平方按钮
        self.pushButton_22.clicked.connect(lambda: self.textEdit.clear())
        self.pushButton_23.clicked.connect(self.percent) # 百分比按钮
        self.pushButton_24.clicked.connect(lambda: self.textEdit.clear())
    def content(self):
        try:
            result = eval(self.textEdit.toPlainText())
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
            # self.textEdit.insertPlainText("错误")
    def backspace(self):
        new_s = self.textEdit.toPlainText()[:-1]
        # if self.textEdit.position() > 0:
        print(new_s)
        self.textEdit.clear()
        self.textEdit.insertPlainText(new_s)
    def sqrt_text(self):
        try:
            result = eval("math.sqrt(" + self.textEdit.toPlainText() + ")")
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
    def square(self):
        try:
            result = eval(self.textEdit.toPlainText() + "**2")
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
    def onePart(self):
        try:
            result = eval("1/"+self.textEdit.toPlainText())
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
    def percent(self):
        try:
            result = eval(self.textEdit.toPlainText() + "/100")
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
    def positiveandnegative(self):
        try:
            result = eval(self.textEdit.toPlainText() + "*(-1)")
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(result))
        except:
            self.textEdit.clear()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow实例
    
    ui = Ui_MainWindow()  # 创建Ui_MainWindow实例
    ui.setupUi(MainWindow)  # 设置UI
    MainWindow.show()  # 展示窗口
    
    app.exec()
