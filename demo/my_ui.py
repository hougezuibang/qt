# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\demo\my.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_my(object):
    def setupUi(self, my):
        my.setObjectName("my")
        my.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(my)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 100, 131, 101))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 180, 72, 15))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 270, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 140, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 180, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        my.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(my)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        my.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(my)
        self.statusbar.setObjectName("statusbar")
        my.setStatusBar(self.statusbar)

        self.retranslateUi(my)
        QtCore.QMetaObject.connectSlotsByName(my)

    def retranslateUi(self, my):
        _translate = QtCore.QCoreApplication.translate
        my.setWindowTitle(_translate("my", "MainWindow"))
        self.label.setText(_translate("my", "账号"))
        self.label_2.setText(_translate("my", "密码"))
        self.pushButton.setText(_translate("my", "修改信息"))

