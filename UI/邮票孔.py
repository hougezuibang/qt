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
        Form.move(1200, 500)
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
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 340, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_2.setProperty("value", 1.0)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(270, 120, 70, 22))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 60, 72, 15))
        self.label.setObjectName("label")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox.setGeometry(QtCore.QRect(270, 60, 70, 22))
        self.doubleSpinBox.setMaximum(99990000.0)
        self.doubleSpinBox.setProperty("value", 650.0)
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
        self.pushButton_3.setText(_translate("Form", "提交"))
        self.pushButton_2.clicked.connect(self.move_copy)
        self.pushButton.clicked.connect(self.open)
        self.pushButton_3.clicked.connect(self.submit)

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
    def move_copy(self):
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbo',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gto',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbl',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gtl',True, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gts',False, 0, 0, 0, 0, 0, 0, 0)
        Layers.copy2other_layer(JobName,step[0], 'drl', 'gbs',False, 0, 0, 0, 0, 0, 0, 0)
        # GUI.show_layer(JobName, step[0], 'gtl')
    def submit(self):
        print("提交")
        # 读取输入参数
        Selection.reset_select_filter()  # 重置选择过滤器，清除之前的选择条件
        # Selection.set_exclude_attr_range_filter([{'attr_name':'tool','min_value':0,'max_value':80},
        #     {'attr_name':'.drill_flag','min_value':210,'max_value':99999}])
        Application.set_featuretype_filter_jwApp(['arc'],['pos'])  # 设置特征类型过滤器，只选择类型为'arc'的特征，同时指定属性为'pos'
        
        # Selection.set_symbol_range_filter([{'symbol_type':'r', 'min_value':400000, 'max_value':1200000, 'attr_name':'r'}])  # 设置符号范围过滤器，选择符号类型为'r'，并限制在400000到1200000之间
        Selection.select_features_by_filter(JobName, step[0], ['gko'])  # 根据之前设置的过滤器选择特征，找图层类型为'drl'
        # 从 Application 中获取选中的特征信息
        list1 = Application.get_selected_feature_infos_jwApp(JobName, step[0], 'gko')
        
        # 过滤出 D <= 0.08 的项
        # 假设 filtered_data 已经被定义并且满足之前的过滤条件
        filtered_data = [item for item in list1 if item["D"] < 0.07]
        # 存储 pad 的信息
        pads = []
        # 循环处理 filtered_data 中的每个项目
        for item in filtered_data:
            # 提取 D、XC 和 YC 值
            d_value = item["D"]
            xc = item["XC"] * 25400 * 1000  # 将 XC 转换成适当的单位
            yc = item["YC"] * 25400 * 1000  # 将 YC 转换成适当的单位
            
            # 生成 r_string
            r_string = "r" + str(int(d_value * 1000))  # 或者根据 d_value 的比例生成 r_string
            
            # 调用 add_pad 方法
            Layers.add_pad(JobName, step[0], ['gko'], r_string, xc, yc, True, 
                        8, [], 0) 
            # 将 pad 的信息加入列表
            pads.append((r_string, xc, yc))
            # 判断两两之间的最小距离并形成配对
        self.minimumdistance(pads)
        GUI.show_layer(JobName, step[0], 'gko')
    # def filter_d(list1):
    #     filtered_data = [item for item in list1 if item["D"] <= 0.08]
    #     return filtered_data      
    def initData(self):
        JobName = '2s'
        Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
        # 打开指定的工作任务
        Input.open_job(JobName, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')
    def minimumdistance(self,pads):
        # 判断两两之间的最小距离并形成配对
        pairs = []
        min_distance = 6000000  # 假设最小距离，需要根据实际情况设置

        for i in range(len(pads)):
            for j in range(i + 1, len(pads)):
                # 计算两个 pad 之间的距离
                r1, x1, y1 = pads[i]
                r2, x2, y2 = pads[j]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                # 如果距离小于 min_distance，则形成配对
                if distance < min_distance:
                    pairs.append((x1, y1,x2,y2))  # 存储配对信息
                    print(distance) 

        # 打印配对结果
        print("Pairs of pads within minimum distance:")
        print(len(pairs))
        print(pairs)

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




# Layers.fill_profile(job, step, layers, fill_type=0, step_repeat_nesting=True, nesting_child_steps=[], step_margin_x=0, step_margin_y=0, max_distance_x=0, max_distance_y=0, SR_step_margin_x=0, SR_step_margin_y=0, SR_max_distance_x=0, SR_max_distance_y=0, avoid_drill=0, avoid_rout=0, avoid_feature=0, polarity=True)
# 在指定层依外形轮廓(Profile)填充为实体，填充前需设置相关填充参数（set_fill_grid_param、set_fill_pattern_param、set_fill_solid_param相关参数），若不设置默认用实铜填充


# Layers.profile_to_outline(job, step, layers, linewidth)
# 指定料号根据profile线创建外框线


# Information.get_profile(job, step)
# 获取指定料号工作单元(step)中构成profile线上所有点的坐标