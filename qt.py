import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, qDrawPlainRect

app = QApplication(sys.argv)            # Qt实例化一个app 必须有且只有一个 sys.argv一个列表是当前文件的名称元素
w = QWidget()							# 创建窗口
w.setWindowTitle("薪资统计")              # 设置窗口标题名称
w.resize(500, 400)                      # 设置窗口大小
# qDrawPlainRect(w)
w.show()                                # 展示窗口
app.exec()                              # 程序进入循环等待状态
