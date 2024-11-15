# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\PythonProject\UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from epkernel import BASE, Configuration, Input, GUI, Application
from epkernel.Action import Information, Selection
from epkernel.Edition import Layers
import math
from epkernel.Edition import  Matrix
class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 504)
        Form.move(1200, 500)
        
        self.initialize_job()
        self.initUI(Form)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def initialize_job(self):
        self.JobName = '2s'
        self.step = ['set']
        Information.get_origin_point(self.JobName, self.step[0])
        self.initData()

    def initUI(self, Form):
        self.pushButton_2 = QtWidgets.QPushButton("移动", Form)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 340, 93, 28))
        self.pushButton_2.clicked.connect(self.move_copy)
        
        self.pushButton = QtWidgets.QPushButton("打开", Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 340, 93, 28))
        self.pushButton.clicked.connect(self.open)
        
        self.pushButton_3 = QtWidgets.QPushButton("提交", Form)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 340, 93, 28))
        self.pushButton_3.clicked.connect(self.submit)

        # 新增的“获取孔”按钮
        self.pushButton_get_hole = QtWidgets.QPushButton("获取孔", Form)
        self.pushButton_get_hole.setGeometry(QtCore.QRect(350, 340, 93, 28))
        self.pushButton_get_hole.clicked.connect(self.get_holes)  # 连接到获取孔的函数

        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_2.setProperty("value", 1.0)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(270, 120, 70, 22))
        
        self.label = QtWidgets.QLabel("孔大小", Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 72, 15))
        
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox.setGeometry(QtCore.QRect(270, 60, 70, 22))
        self.doubleSpinBox.setMaximum(99990000.0)
        self.doubleSpinBox.setProperty("value", 650.0)

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 120, 113, 21))
        
        self.label_2 = QtWidgets.QLabel("间距", Form)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 72, 15))
        
        self.radioButton_3 = QtWidgets.QRadioButton("外切", Form)
        self.radioButton_3.setGeometry(QtCore.QRect(580, 130, 115, 19))
        
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(130, 60, 113, 21))
        
        self.label_3 = QtWidgets.QLabel("圆心位置", Form)
        self.label_3.setGeometry(QtCore.QRect(470, 90, 72, 15))
        
        self.radioButton = QtWidgets.QRadioButton("内切", Form)
        self.radioButton.setGeometry(QtCore.QRect(580, 40, 115, 19))
        
        self.radioButton_2 = QtWidgets.QRadioButton("正中", Form)
        self.radioButton_2.setGeometry(QtCore.QRect(580, 80, 115, 19))

    def get_holesbeifen(self):
        print("获取孔的逻辑可以放在这里")
        # 在这里实现获取孔的具体逻辑
        Matrix.create_layer(self.JobName, 'asd111',-1)
        Layers.flatten_step(self.JobName, self.step[0], ['gko'], 'asd111')
        Layers.profile_to_outline(self.JobName, self.step[0], ['asd111'], 30*1000)
        # 指定料号根据profile线创建外框线
        Selection.reset_select_filter() 
        Application.set_featuretype_filter_jwApp(['line'],['pos'])
        
        selected_features = Application.get_selected_feature_infos_jwApp(self.JobName, self.step[0], 'asd111')
        print(selected_features)
        
        filtered_data = [item for item in selected_features if item["linewidth"] < 150000]
        print("filtered_data")
        print(filtered_data)
        GUI.show_layer(self.JobName, self.step[0], 'asd111')
    def get_holes(self):
        fixed_value = 210000000000

        # 指定料号根据profile线创建外框线
        Selection.reset_select_filter()
        Application.set_featuretype_filter_jwApp(['line'], ['pos'])

        selected_features = Application.get_selected_feature_infos_jwApp(self.JobName, self.step[0], 'gko')
        print("selected_features")
        print(len(selected_features))
        filtered_data = []

        for item in selected_features:
            # 获取起点和终点的坐标，假设它们是item字典中的键
            start_x = item.get("start_x", 0)
            start_y = item.get("start_y", 0)
            end_x = item.get("end_x", 0)
            end_y = item.get("end_y", 0)

            # 计算横向和纵向的长度
            length = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5

            # 检查长度是否小于固定值
            if length < fixed_value:
                filtered_data.append(item)

        print("filtered_data")
        print(filtered_data)
        print(len(filtered_data))
        GUI.show_layer(self.JobName, self.step[0], 'gko')


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def open(self):
        print("打开")
        self.setup_symbol_filter()
        Layers.outline2surface(self.JobName, self.step[0], ['drl'], True)  # 转化为pad
        self.select_features('drl')
        GUI.show_layer(self.JobName, self.step[0], 'drl')

    def setup_symbol_filter(self):
        Application.set_featuretype_filter_jwApp(['arc'], ['pos'])
        Selection.reset_select_filter() 
        Selection.set_symbol_range_filter([{'symbol_type': 'r', 'min_value': 400000, 'max_value': 1200000}])
    def select_features(self, layer_type):
        Selection.select_features_by_filter(self.JobName, self.step[0], [layer_type])  

    def move_copy(self):
        layers_to_copy = ['gbo', 'gto', 'gbl', 'gtl']
        for layer in layers_to_copy:
            Layers.copy2other_layer(self.JobName, self.step[0], 'drl', layer, True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(self.JobName, self.step[0], 'drl', 'gts', False, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(self.JobName, self.step[0], 'drl', 'gbs', False, 0, 0, 0, 0, 0, 0, 0)

    def submit(self):
        print("提交")
        Selection.reset_select_filter()
        Application.set_featuretype_filter_jwApp(['arc'], ['pos'])
        self.select_features('gko')
        
        selected_features = Application.get_selected_feature_infos_jwApp(self.JobName, self.step[0], 'gko')
        filtered_data = [item for item in selected_features if item["D"] < 0.07]

        pads = self.process_filtered_data(filtered_data)
        self.minimumdistance(pads)
        GUI.show_layer(self.JobName, self.step[0], 'gko')

    def process_filtered_data(self, filtered_data):
        pads = []
        for item in filtered_data:
            d_value = item["D"]
            xc = item["XC"] * 25400 * 1000  
            yc = item["YC"] * 25400 * 1000  
            r_string = f"r{int(d_value * 1000)}"
            
            Layers.add_pad(self.JobName, self.step[0], ['gko'], r_string, xc, yc, True, 8, [], 0) 
            pads.append((r_string, xc, yc))
        return pads

    def initData(self):
        Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
        Input.open_job(self.JobName, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')

    def minimumdistance(self, pads):
        pairs = []
        min_distance = 6000000  

        for i in range(len(pads)):
            for j in range(i + 1, len(pads)):
                x1, y1 = pads[i][1:3]
                x2, y2 = pads[j][1:3]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < min_distance:
                    pairs.append((x1, y1, x2, y2))  
                    print(distance)

        print("Pairs of pads within minimum distance:")
        print(len(pairs), pairs)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_Form()
    w.setupUi(w)
    w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    w.show()
    app.exec()


# Layers.fill_profile(job, step, layers, fill_type=0, step_repeat_nesting=True, nesting_child_steps=[], step_margin_x=0, step_margin_y=0, max_distance_x=0, max_distance_y=0, SR_step_margin_x=0, SR_step_margin_y=0, SR_max_distance_x=0, SR_max_distance_y=0, avoid_drill=0, avoid_rout=0, avoid_feature=0, polarity=True)
# 在指定层依外形轮廓(Profile)填充为实体，填充前需设置相关填充参数（set_fill_grid_param、set_fill_pattern_param、set_fill_solid_param相关参数），若不设置默认用实铜填充


# Layers.profile_to_outline(job, step, layers, linewidth)
# 指定料号根据profile线创建外框线


# Information.get_profile(job, step)
# 获取指定料号工作单元(step)中构成profile线上所有点的坐标
