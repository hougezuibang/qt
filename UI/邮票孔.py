# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from http.cookiejar import debug
from epkernel import BASE
from epkernel.Action import Information, Selection
from epkernel import Configuration, Input, GUI, Application, Guide
from epkernel.Edition import Matrix, Layers
import math
class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 504)
        JobName = '2s'
        step = ['set']
        # 设置自定义特征
        Information.get_origin_point(JobName, step[0])
        self.initData()
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
        self.pushButton_2.setText(_translate("Form", "移动"))
        self.pushButton.setText(_translate("Form", "打开"))
        self.label.setText(_translate("Form", "孔大小"))
        self.label_2.setText(_translate("Form", "间距"))
        self.radioButton_3.setText(_translate("Form", "外切"))
        self.label_3.setText(_translate("Form", "圆心位置"))
        self.radioButton.setText(_translate("Form", "内切"))
        self.radioButton_2.setText(_translate("Form", "正中"))
        self.pushButton_2.clicked.connect(self.move)
        self.pushButton.clicked.connect(self.open)

    def open(self):
        print("打开")
        
        # 设置符号范围过滤器并选择特征 
        # r400到r1200
        # Selection.set_symbol_range_filter([{'symbol_type':'r', 'min_value':400000, 'max_value':1200000, 'attr_name':'r'}])
        Application.set_featuretype_filter_jwApp(['arc'],['pos'])  # 设置特征类型过滤器，只选择类型为'arc'的特征，同时指定属性为'pos'
        Layers.outline2surface(JobName, step[0], ['drl'], True)  # 将指定层的轮廓转化为pad
        Selection.reset_select_filter()  # 重置选择过滤器，清除之前的选择条件
        Selection.set_symbol_range_filter([{'symbol_type':'r', 'min_value':400000, 'max_value':1200000, 'attr_name':'r'}])  # 设置符号范围过滤器，选择符号类型为'r'，并限制在400000到1200000之间
        Selection.select_features_by_filter(JobName, step[0], ['drl'])  # 根据之前设置的过滤器选择特征，找图层类型为'drl'
        GUI.show_layer(JobName, step[0], 'drl')
        print("打开jishu")
    def move(self):
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbo',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gto',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbl',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gtl',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gts',False, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbs',False, 0, 0, 0, 0, 0, 0, 0)
        # GUI.show_layer(JobName, step[0], 'gtl')
    def initData(self):
        JobName = '2s'
        Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
        # 打开指定的工作任务
        Input.open_job(JobName, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')

# 初始化配置，指定配置文件路径
JobName = '2s'
step = ['set']
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_Form()
    w.setupUi(w)  # 调用setupUi方法

    # 设置窗口为无边框
    w.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    w.show()  # 展示窗口
    app.exec()
