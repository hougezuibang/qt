# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\demo\home.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_home(object):
    def setupUi(self, home):
        home.setObjectName("home")
        home.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(home)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(60, 20, 691, 431))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.login_btn = QtWidgets.QPushButton(self.frame)
        self.login_btn.setGeometry(QtCore.QRect(530, 0, 31, 28))
        self.login_btn.setObjectName("login_btn")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(582, 0, 31, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.exit = QtWidgets.QPushButton(self.frame)
        self.exit.setGeometry(QtCore.QRect(630, 0, 31, 28))
        self.exit.setObjectName("exit")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, -10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(85, 170, 255);")
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 40, 221, 391))
        self.frame_2.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(221, 244, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 141, 71))
        self.label_2.setStyleSheet("\n"
"color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 255), stop:0.339795 rgba(255, 0, 0, 255), stop:0.339799 rgba(255, 255, 255, 255), stop:0.662444 rgba(255, 255, 255, 255), stop:0.662469 rgba(0, 0, 255, 255), stop:1 rgba(0, 0, 255, 255));")
        self.label_2.setObjectName("label_2")
        self.bili_bun = QtWidgets.QPushButton(self.frame)
        self.bili_bun.setGeometry(QtCore.QRect(390, 120, 93, 28))
        self.bili_bun.setObjectName("bili_bun")
        self.baidu_btn = QtWidgets.QPushButton(self.frame)
        self.baidu_btn.setGeometry(QtCore.QRect(390, 170, 93, 28))
        self.baidu_btn.setObjectName("baidu_btn")
        self.douyin_btn = QtWidgets.QPushButton(self.frame)
        self.douyin_btn.setGeometry(QtCore.QRect(390, 220, 93, 28))
        self.douyin_btn.setObjectName("douyin_btn")
        self.tengxun_btn = QtWidgets.QPushButton(self.frame)
        self.tengxun_btn.setGeometry(QtCore.QRect(390, 270, 93, 28))
        self.tengxun_btn.setObjectName("tengxun_btn")
        self.mybtn = QtWidgets.QPushButton(self.frame)
        self.mybtn.setGeometry(QtCore.QRect(580, 40, 93, 28))
        self.mybtn.setObjectName("mybtn")
        home.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(home)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        home.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(home)
        self.statusbar.setObjectName("statusbar")
        home.setStatusBar(self.statusbar)

        self.retranslateUi(home)
        self.pushButton_2.clicked.connect(home.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(home)

    def retranslateUi(self, home):
        _translate = QtCore.QCoreApplication.translate
        home.setWindowTitle(_translate("home", "MainWindow"))
        self.login_btn.setText(_translate("home", "✈"))
        self.pushButton_2.setText(_translate("home", "-"))
        self.exit.setText(_translate("home", "X"))
        self.label.setText(_translate("home", "Logo"))
        self.label_2.setText(_translate("home", "欢迎来到我的主页"))
        self.bili_bun.setText(_translate("home", "哔哩哔哩"))
        self.baidu_btn.setText(_translate("home", "百度"))
        self.douyin_btn.setText(_translate("home", "抖音"))
        self.tengxun_btn.setText(_translate("home", "腾讯"))
        self.mybtn.setText(_translate("home", "my"))

