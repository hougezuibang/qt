# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 504)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 340, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 340, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(270, 120, 70, 22))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 72, 15))
        self.label.setObjectName("label")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox.setGeometry(QtCore.QRect(270, 60, 70, 22))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 120, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 72, 15))
        self.label_2.setObjectName("label_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(580, 130, 115, 19))
        self.radioButton_3.setObjectName("radioButton_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(130, 60, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(470, 90, 72, 15))
        self.label_3.setObjectName("label_3")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(580, 40, 115, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(580, 80, 115, 19))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "添加"))
        self.pushButton.setText(_translate("Form", "打开"))
        self.label.setText(_translate("Form", "孔大小"))
        self.label_2.setText(_translate("Form", "间距"))
        self.radioButton_3.setText(_translate("Form", "外切"))
        self.label_3.setText(_translate("Form", "圆心位置"))
        self.radioButton.setText(_translate("Form", "内切"))
        self.radioButton_2.setText(_translate("Form", "正中"))

