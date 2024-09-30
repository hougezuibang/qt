from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

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
        #time.sleep(1)
        self.close()
    def sta(self,thread_class):
        self.cal = thread_class
        self.cal.finished.connect(self.finish)
        self.cal.start()
