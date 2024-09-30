from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QPushButton
import sys


class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)

        # 创建文本编辑框
        self.edit_text = QtWidgets.QPlainTextEdit(Form)
        self.edit_text.setGeometry(QtCore.QRect(100, 20, 181, 161))
        self.edit_text.setPlainText("")
        self.edit_text.setPlaceholderText("请输入信息")
        self.edit_text.setObjectName("edit_text")

        # 创建按钮
        self.pushbutton = QtWidgets.QPushButton(Form)
        self.pushbutton.setGeometry(QtCore.QRect(150, 200, 93, 28))
        self.pushbutton.setObjectName("pushbutton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "测试"))
        self.pushbutton.setText(_translate("Form", "提交"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_Form()
    w.setupUi(w)  # 调用setupUi方法

    # 设置窗口为无边框
    w.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    w.show()  # 展示窗口
    app.exec()
