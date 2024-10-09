import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, qDrawPlainRect, QPlainTextEdit
num = 0
def onclick():
  print("统计按钮被点击")
  global num
  textEdit.appendPlainText("num---"+str(num))  # 在文本编辑器末尾添加文字
  num += 1  # num+=1
# qDrawPlainRect = drawRect  # 重写qDrawPlainRect函数
app = QApplication(sys.argv)  # Qt实例化一个app 必须有且只有一个 sys.argv一个列表是当前文件的名称元素
w = QWidget()  # 创建窗口
w.setWindowTitle("薪资统计")  # 设置窗口标题名称
w.resize(1000, 800)  # 设置窗口大小

textEdit = QPlainTextEdit(w)  # 创建一个文本编辑器
textEdit.setPlaceholderText("欢迎使用薪资统计软件！")  # 设置文本编辑器初始内容
textEdit.move(10, 10)  # 设置文本编辑器位置
textEdit.resize(480, 380)  # 设置文本编辑器大小
button = QPushButton(w)  # 创建一个按钮
button.setText("统计")  # 设置按钮文字
button.move(500, 200)  # 设置按钮位置
button.clicked.connect(onclick)  # 按钮点击事件绑定onclick函数
w.show()  # 展示窗口
app.exec()  # 程序进入循环等待状态
