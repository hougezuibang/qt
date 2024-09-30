# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lianxi.ui'
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
        Form.resize(650, 400)
        Form.move(1200, 500)
        # 初始化配置，指定配置文件路径
        JobName = '6328037'
        step = ['orig']

        # 设置自定义特征
        Information.get_origin_point(JobName, step[0])
        self.initData()
        # 重命名图层函数调用
        rename_layers()
        # 移动图层函数调用
        sort()

        MergingHole()
        # 调用查找最小和最大孔大小的函数
        min_hole_size, max_hole_size = find_hole_sizes(JobName, step)
        print(f"最小孔大小: {min_hole_size} mm")
        print(f"最大孔大小: {max_hole_size} mm")
        self.pushButto = QtWidgets.QPushButton(Form)
        self.pushButto.setGeometry(QtCore.QRect(260, 190, 93, 28))
        self.pushButto.setObjectName("pushButto")
        self.pushButto_3= QtWidgets.QPushButton(Form)
        self.pushButto_3.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.pushButto_3.setObjectName("pushButto_3")
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setGeometry(QtCore.QRect(90, 40, 96, 22))
        self.spinBox.setMinimum(-2000000172)
        self.spinBox.setMaximum(2000000154)
        self.spinBox.setValue(6)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setGeometry(QtCore.QRect(90, 80, 96, 22))
        self.spinBox_2.setMinimum(-2000000172)
        self.spinBox_2.setMaximum(2000000000)
        self.spinBox_2.setValue(4)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(Form)
        self.spinBox_3.setGeometry(QtCore.QRect(390, 40, 96, 22))
        self.spinBox_3.setMinimum(-2000000172)
        self.spinBox_3.setMaximum(2000000000)
        self.spinBox_3.setValue(4)
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_4 = QtWidgets.QSpinBox(Form)
        self.spinBox_4.setGeometry(QtCore.QRect(520, 80, 96, 22))
        self.spinBox_4.setMinimum(-2000000172)
        self.spinBox_4.setMaximum(2000000000)
        self.spinBox_4.setValue(1)
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_5 = QtWidgets.QSpinBox(Form)
        self.spinBox_5.setGeometry(QtCore.QRect(290, 80, 96, 22))
        self.spinBox_5.setMinimum(-2000000172)
        self.spinBox_5.setMaximum(2000000000)
        self.spinBox_5.setValue(8)
        self.spinBox_5.setObjectName("spinBox_5")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 40, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 40, 141, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(190, 80, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(410, 80, 91, 16))
        self.label_5.setObjectName("label_5")
        self.pushButto_2 = QtWidgets.QPushButton(Form)
        self.pushButto_2.setGeometry(QtCore.QRect(460, 190, 93, 28))
        self.pushButto_2.setObjectName("pushButto_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButto.setText(_translate("Form", "引孔"))
        self.pushButto_3.setText(_translate("Form", "打开"))
        self.label.setText(_translate("Form", "引孔间距"))
        self.label_2.setText(_translate("Form", "小孔到大孔距离"))
        self.label_3.setText(_translate("Form", "小孔个数"))
        self.label_4.setText(_translate("Form", "小孔间间距"))
        self.label_5.setText(_translate("Form", "大孔小孔间距"))
        self.pushButto_2.setText(_translate("Form", "预钻孔"))
        self.pushButto.clicked.connect(self.yinkong)
        self.pushButto_2.clicked.connect(self.yuzuankong)
        self.pushButto_3.clicked.connect(self.dakai)
    def dakai(self):
        print("打开")
        try:
            spin_boxes = [self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4, self.spinBox_5]
            for i, spin_box in enumerate(spin_boxes, start=1):
                print(f"self.spinBox_{i}.value() = {spin_box.value()}")
        except Exception as e:
            print(f"发生错误: {e}")


        GUI.show_layer(JobName, 'orig', 'drill.out')

    def yinkong(self):
        print("yinkong")
        print(self.spinBox.value())

        caokong(JobName, step, self.spinBox.value(), self.spinBox_3.value())
        # GUI.show_layer(JobName, 'orig', 'drill.out')

    def yuzuankong(self):
        # print("yuzuankong")

        YuZuanKong(JobName, step, self.spinBox_2.value(), self.spinBox_4.value(), self.spinBox_5.value())

    def initData(self):
        JobName = '6328037'
        Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
        # 打开指定的工作任务
        Input.open_job(JobName, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')


# 初始化配置，指定配置文件路径
JobName = '6328037'
step = ['orig']




# 重命名以及设置属性
def rename_layers():
    changes = [
        ('etchlayer1top.gdo', 'board', 'signal', 'gtl'),
        ('etchlayer2.gdo', 'board', 'signal', 'l2'),
        ('etchlayer3.gdo', 'board', 'signal', 'l3'),
        ('etchlayer4.gdo', 'board', 'signal', 'l4'),
        ('etchlayer5.gdo', 'board', 'signal', 'l5'),
        ('etchlayer6bottom.gdo', 'board', 'signal', 'gbl'),
        ('generatedsilkscreenbottom.gdo', 'board', 'silk_screen', 'gbo'),
        ('generatedsilkscreentop.gdo', 'board', 'silk_screen', 'gto'),
        ('solderpastebottom.gdo', 'misc', 'signal', 'gbp'),
        ('solderpastetop.gdo', 'misc', 'signal', 'gtp'),
        ('soldermaskbottom.gdo', 'board', 'solder_mask', 'gbs'),
        ('soldermasktop.gdo', 'board', 'solder_mask', 'gts'),
        ('antisilk_top.gdo', 'misc', 'signal', 'antisilk_top.gdo'),
        ('thruholenonplated.ncd', 'board', 'drill', 'drill.out'),
        ('thruholeplated.ncd', 'board', 'drill', 'drill.pin'),
    ]

    for layer, type_, feature, new_value in changes:
        Matrix.change_matrix_row(JobName, layer, type_, feature, new_value, polarity=True)


# 设置排序
def sort():
    move_layers = [
        (9, 1),
        (13, 2),
        (3, 17),
        (12, 9),
        (14, 11),
        (15, 12)
    ]

    for src, dst in move_layers:
        Matrix.move_layer(JobName, src, dst)


def MergingHole():
    # 设置自定义特征
    Information.get_origin_point(JobName, step[0])
    # 复制图层到另一层
    Layers.copy2other_layer(JobName, step[0], 'drill.pin', 'drill.out', False, 0, 0, 0, 0, 0, 0, 0)
    # 删除原来多余图层
    Matrix.delete_layer(JobName, 'drill.pin')
    # 生成孔属性
    BASE.auto_classify_attribute(JobName, step[0], [['drill.out']])




def find_hole_sizes(JobName, step):
    try:
        Selection.reset_select_filter()
        Selection.set_featuretype_filter(True, True, True, True, True, True, True)

        # 选择特征
        Selection.select_features_by_filter(JobName, step[0], ['drill.out'])
        all_features = Information.get_selected_features_infos(JobName, step[0], 'drill.out')
        print(all_features)

        if not all_features:
            print("没有找到任何孔特征")
            return None, None

        # 初始化最小和最大孔大小
        min_hole_size = float('inf')
        max_hole_size = float('-inf')

        # 遍历所有特征以查找最小和最大孔大小
        for feature in all_features:
            hole_size_str = feature['symbolname']  # 假设 'symbolname' 表示孔的大小
            hole_size = float(hole_size_str[1:])  # 去掉 'r' 并转换为浮点数

            if hole_size < min_hole_size:
                min_hole_size = hole_size

            if hole_size > max_hole_size:
                max_hole_size = hole_size

        if min_hole_size == float('inf') or max_hole_size == float('-inf'):
            print("没有找到有效的孔特征")
            return None, None

        # 将孔大小转换为适当的单位并输出
        min_hole_size_mm = min_hole_size * 25.4  # 假设以微米为单位
        max_hole_size_mm = max_hole_size * 25.4  # 假设以微米为单位
        Selection.reset_select_filter()
        Selection.reverse_select(JobName, step[0], 'drill.out')
        return min_hole_size_mm, max_hole_size_mm

    except Exception as e:
        print(f"发生错误: {e}")



# liangkongjianju = 0.006
# liangbianjianju = 0.002  # 两面 两个边总距离


def caokong(jobname, step,kongjianju, bianjianju):
    try:
        # Selection.reset_select_filter()
        # Selection.reverse_select(jobname, step[0], 'drill.out')
        # GUI.show_layer(JobName, step[0], 'drill.out')
        # Selection.select_feature_by_id(jobname, step[0], 'drill.out', [3157])

        Information.get_selected_features_infos(jobname, step[0], 'drill.out')
        # GUI.show_layer(jobname, step[0], 'drill.out')
        selectFeatureInfo = Information.get_selected_features_infos(jobname, step[0], 'drill.out')
        liangkongjianju = kongjianju/1000
        liangbianjianju = bianjianju/1000
        if not selectFeatureInfo:
            print("没有找到选中的物件信息")
            return

        print("--------------------------获取选中物件信息----------")
        feature_info = selectFeatureInfo[0]  # 获取第一个（也是唯一的）字典

        # 从 feature_info 中提取必要参数并进行单位转换
        XS, XE = feature_info['XS'] * 25.4, feature_info['XE'] * 25.4
        YS, YE = feature_info['YS'] * 25.4, feature_info['YE'] * 25.4
        D = round(feature_info['linewidth'] / 1_000_000, 5)  # 假设线宽代表原来的圆柱直径
        angle = feature_info['angle']  # 角度

        print(XS, YS)
        print(XE, YE)
        print(D)

        # 计算槽孔长度
        delta_d = round(math.sqrt((XE - XS) ** 2 + (YE - YS) ** 2) + D, 5)
        # slot_length = round(delta_d + D, 5)
        print("槽孔长度:", delta_d)
        if delta_d > 0.008:
            guiding_hole_size = (delta_d - liangkongjianju - liangbianjianju) / 2
            # 计算导引孔大小
            # guiding_hole_size = (slot_length - 0.05) / 2
            print("槽孔长度:", delta_d)
            print("导引孔大小:", guiding_hole_size)

            # 将角度转换为弧度并计算导引孔位置
            angle_rad = math.radians(angle)
            if XE < XS :
                guiding_hole_position_start_x = XS + abs(
                    (guiding_hole_size - D + liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_start_y = YS + (guiding_hole_size - D + liangbianjianju) * math.sin(angle_rad) / 2
                guiding_hole_position_end_x = XE - abs(
                    (guiding_hole_size - D + liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_end_y = YE - (guiding_hole_size - D + liangbianjianju) * math.sin(angle_rad) / 2
            else:
                guiding_hole_position_start_x = XS - abs(
                    (guiding_hole_size - D + liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_start_y = YS - (guiding_hole_size - D + liangbianjianju) * math.sin(angle_rad) / 2
                guiding_hole_position_end_x = XE + abs(
                    (guiding_hole_size - D + liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_end_y = YE + (guiding_hole_size - D + liangbianjianju) * math.sin(angle_rad) / 2

            guiding_hole_size_str = f'r{str(guiding_hole_size * 1000 / 25.4)}'

            # 添加导引孔
            Layers.add_pad(jobname, step[0], ['drill.out'], guiding_hole_size_str,
                           int(guiding_hole_position_start_x * 1_000_000),
                           int(guiding_hole_position_start_y * 1_000_000), True, 0, [], 0)

            Layers.add_pad(jobname, step[0], ['drill.out'], guiding_hole_size_str,
                           int(guiding_hole_position_end_x * 1_000_000),
                           int(guiding_hole_position_end_y * 1_000_000), True, 0, [], 0)

        # GUI.show_layer(jobname, step[0], 'drill.out')
        Guide.refresh_joblist(JobName, step[0])
    except Exception as e:
        print(f"发生错误: {e}")


# caokong(JobName, step)
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def calculate_small_r(SmallToSmall, length_waibian):
    return (SmallToSmall * 2) / length_waibian


def YuZuanKong(jobname, step, count, small_to_large, small_to_small):
    try:
        # x_6 = 20000000  # 坐标
        # y_6 = 10000000  # 坐标
        # r_6 = 60000000  # 大小

        # count = 7  # 个数
        # SmallToLarge = 2000000  # 1为小到大距离
        # SmallToSmall = 10000000  # 2为小到小距离
        infos= Information.get_selected_features_infos(jobname, step[0], 'drill.out')
        print("infos--")
        print(infos[0])
        print(infos[0]['X'] * 25.4)
        print(infos[0]['Y'] * 25.4)
        print(float(infos[0]['symbolname'][1:]) * 25.4)

        x_6 = infos[0]['X'] * 25.4 * 1_000_000  # 坐标
        y_6 = infos[0]['Y'] * 25.4 * 1_000_000  # 坐标
        r_6 = float(infos[0]['symbolname'][1:]) * 25.4 *1000 # 大小

        SmallToLarge = small_to_large * 1_000_000  # 1为小到大距离
        SmallToSmall = small_to_small * 1_000_000  # 2为小到小距离
        # Selection.reset_select_filter()
        # Selection.reverse_select(jobname, step[0], 'drill.out')

        r_size = f"r{round(r_6 / 1000 / 25.4, 2)}"
        # 添加第一层 Pad
        # Layers.add_pad(jobname, step[0], ['drill.out'], r_size, x_6, y_6, True, 0, [], 0)
        jiaodu = 360 / count
        # 创建空列表来存储 x_i 和 y_i
        x_values = []
        y_values = []
        for i in range(1, count + 1):
            x_i = x_6 + r_6 / 2 * math.cos(math.radians(jiaodu * i)) - SmallToLarge * math.cos(math.radians(jiaodu * i))
            y_i = y_6 + r_6 / 2 * math.sin(math.radians(jiaodu * i)) - SmallToLarge * math.sin(math.radians(jiaodu * i))
            # 将计算得到的 x_i 和 y_i 存储到列表中
            x_values.append(x_i)
            y_values.append(y_i)
            print("x_i")
            print(jiaodu * i)
            print(x_i, y_i)

            # 输出存储的数组
        print("所有 x 值: ", x_values)
        print("所有 y 值: ", y_values)
        len_1 = calculate_distance(x_values[0], y_values[0], x_values[1], y_values[1])

        print("得到长度")
        print(len_1)

        xiaobanjing = (len_1 * r_6 / 2 - len_1 * SmallToLarge - (r_6 / 2 - SmallToLarge) * SmallToSmall) / (
                    r_6 - SmallToLarge * 2 + len_1)

        print("得到小半径")
        print(xiaobanjing)
        print("得到坐标")
        banjing = xiaobanjing / 1000 / 25.4

        print("得到半径")
        print(banjing)


        # 这里进行循环遍历 x_values 和 y_values，同时动态获取 i 的值
        for i, (x, y) in enumerate(zip(x_values, y_values), start=1):
            # 计算新的 x 和 y 值
            adjusted_x = x - xiaobanjing * math.cos(math.radians(jiaodu * i))
            adjusted_y = y - xiaobanjing * math.sin(math.radians(jiaodu * i))
            # 计算半径
            double_banjing = banjing * 2  # 计算两倍的 banjing

            # 将结果转换为字符串并拼接
            r_value = f"r{double_banjing}"  # 使用 f-string 进行字符串拼接
            # 调用 Layers.add_pad
            Layers.add_pad(jobname, step[0], ['drill.out'], r_value, adjusted_x, adjusted_y, True, 0, [], 0)
            # 打印输出以便调试
            print(f"第 {i} 个 pad 添加在位置: ({adjusted_x}, {adjusted_y})")
            Guide.refresh_joblist(JobName,step[0])

    except Exception as e:
        print(f"发生错误: {e}")


# yuzuankong(JobName, step)

# Layers.add_pad(jobname,step[0],['drill.out'],"r15",x_6+200000,y_6,True,0,[],0)
GUI.show_layer(JobName, step[0], 'drill.out')

Guide.get_affected_layers(JobName)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_Form()
    w.setupUi(w)  # 调用setupUi方法

    # 设置窗口为无边框
    w.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    w.show()  # 展示窗口
    app.exec()
