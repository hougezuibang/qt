import random
from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from PyQt5.QtWidgets import QGroupBox,QVBoxLayout,QHBoxLayout


class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self):
        self.resize(800, 800)       # 设置窗口大小
        cout = QVBoxLayout(self)
        
        
        
        groupBox = QGroupBox("GroupBox")
        cout_1 = QVBoxLayout()
    
        groupBox2 = QGroupBox("GroupBox2")
        cout_2 = QHBoxLayout() 

        # cout_2.addWidget(cout_1)
        # cout.setLayout(cout_1)
        
        # cout.addWidget(cout_2)
        
        print("qqqqqqqqqqqqqq") 
        radioButton = QtWidgets.QRadioButton("RadioButton1")
        radioButton2= QtWidgets.QRadioButton("RadioButton2")
        radioButton3= QtWidgets.QRadioButton("RadioButton3")
        radioButton4= QtWidgets.QRadioButton("RadioButton4")
        radioButton5= QtWidgets.QRadioButton("RadioButton5")
        radioButton6 = QtWidgets.QRadioButton("RadioButton6")
        radioButton7 = QtWidgets.QRadioButton("RadioButton7")
        radioButton8 = QtWidgets.QRadioButton("RadioButton8")
        radioButton9 = QtWidgets.QRadioButton("RadioButton9")
        radioButton2.setChecked(True)
        cout_1.addWidget(radioButton)
        cout_1.addWidget(radioButton2)
        cout_1.addWidget(radioButton3)

        cout_2.addWidget(radioButton4)
        cout_2.addWidget(radioButton5)

        cout_1.addWidget(radioButton6)
        cout_2.addWidget(radioButton7)
        # cout.addStretch()
        cout_1.addWidget(radioButton8)
        cout_2.addWidget(radioButton9)
        groupBox.setLayout(cout_1)
        groupBox2.setLayout(cout_2)
        cout.addWidget(groupBox)
        cout.addWidget(groupBox2)
        self.setLayout(cout)
if __name__ == '__main__':
    app =QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.setupUi()
    mainWindow.show()
    sys.exit(app.exec_())
