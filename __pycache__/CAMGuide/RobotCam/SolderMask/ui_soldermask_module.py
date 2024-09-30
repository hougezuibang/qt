from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import time

class processbar_UI(QDialog):
    def __init__(self,thread_class):
        super().__init__()
        self.dialog_init()
        self.sta(thread_class)
        #self.finish()
    def dialog_init(self):
        font=QFont()
        font.setFamily('宋体')
        font.setPointSize(20)
        self.setWindowTitle('Guide progressbar')
        self.setFont(font)
        self.setFixedHeight(50)
        self.setFixedWidth(400)
        vbox=QVBoxLayout()
        self.prgs = QProgressBar(self)
        self.prgs.setMinimum(0)
        self.prgs.setMaximum(0)
        self.prgs.setGeometry(300,400,200,250)
        deskrect = QApplication.desktop()
        self.move(deskrect.width() - self.width(), 0)
        self.prgs.setStyleSheet("QProgressBar{background-color:#E0E0E0;border:2px solid #5B677A;border-radius:5px;text-align:center}"
                "QProgressBar::chunk{background-color:#5B677A;width:10px;margin:0.5px;border-radius:5px;}")
        vbox.addWidget(self.prgs)
        self.setLayout(vbox)
    def finish(self):
        self.prgs.setMaximum(100)
        self.prgs.setValue(100)
        time.sleep(1)
        self.close()
    def sta(self,thread_class):
        self.cal = thread_class
        self.cal.finished.connect(self.finish)
        self.cal.start()

class soldermask_compensation_UI(QDialog):
    statue = True
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.connect_init()  
    def init_UI(self):    
        self.setObjectName("Form")
        self.resize(300, 150)
        #最小线宽
        self.width_ly = QtWidgets.QHBoxLayout()
        self.width_ly.setContentsMargins(0, 0, 0, 0)
        self.width_ly.setObjectName("width_ly")
        self.width_lbl = QtWidgets.QLabel()
        self.width_lbl.setObjectName("width_lbl")
        self.width_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.width_ly.addWidget(self.width_lbl)     
        self.width_dsb = QtWidgets.QDoubleSpinBox()
        self.width_dsb.setDecimals(3)
        self.width_dsb.setValue(8)
        self.width_ly.addWidget(self.width_dsb)       
        #功能按钮
        self.button_ly = QtWidgets.QHBoxLayout()
        self.button_ly.setContentsMargins(0, 0, 0, 0)
        self.button_ly.setObjectName("button_ly")
        self.continue_btn = QtWidgets.QPushButton()
        self.continue_btn.setObjectName("continue_btn")
        self.button_ly.addWidget(self.continue_btn)
        self.stop_btn = QtWidgets.QPushButton()
        self.stop_btn.setObjectName("stop_btn")
        self.button_ly.addWidget(self.stop_btn)
        self.main_ly = QtWidgets.QVBoxLayout()
        self.main_ly.setContentsMargins(0, 0, 0, 0)
        self.main_ly.setObjectName("main_ly")
        #添加主布局
        self.main_ly.addLayout(self.width_ly)
        self.main_ly.addLayout(self.button_ly)
        self.setLayout(self.main_ly)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.width_lbl.setText(_translate("Form", "防焊最小线宽"))
        self.continue_btn.setText(_translate("Form", "continue"))
        self.stop_btn.setText(_translate("Form", "stop"))


    def connect_init(self):
        self.continue_btn.clicked.connect(self.continue_clicked)
        self.stop_btn.clicked.connect(self.stop_clicked)

    def continue_clicked(self):
        self.statue = True
        self.close()

    def stop_clicked(self):
        self.statue = False
        self.close()

