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

class inner_compensation_UI(QDialog):
    statue = True
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.connect_init()  
    def init_UI(self):      
        self.setObjectName("Form")
        self.resize(853, 257)
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setGeometry(QRect(50, 50, 762, 163))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inner_lbl = QLabel(self.groupBox_2)
        self.inner_lbl.setObjectName("inner_lbl")
        self.verticalLayout.addWidget(self.inner_lbl)
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.trace_lbl = QLabel(self.groupBox_3)
        self.trace_lbl.setObjectName("trace_lbl")
        self.horizontalLayout_2.addWidget(self.trace_lbl)
        self.trace_dsb = QDoubleSpinBox(self.groupBox_3)
        self.trace_dsb.setObjectName("trace_dsb")
        self.horizontalLayout_2.addWidget(self.trace_dsb)
        self.surface_lbl = QLabel(self.groupBox_3)
        self.surface_lbl.setObjectName("surface_lbl")
        self.horizontalLayout_2.addWidget(self.surface_lbl)
        self.surface_dsb =QDoubleSpinBox(self.groupBox_3)
        self.surface_dsb.setObjectName("surface_dsb")
        self.horizontalLayout_2.addWidget(self.surface_dsb)
        self.tear_lbl = QLabel(self.groupBox_3)
        self.tear_lbl.setObjectName("tear_lbl")
        self.horizontalLayout_2.addWidget(self.tear_lbl)
        self.tear_dsb = QDoubleSpinBox(self.groupBox_3)
        self.tear_dsb.setObjectName("tear_dsb")
        self.horizontalLayout_2.addWidget(self.tear_dsb)
        self.via_lbl = QLabel(self.groupBox_3)
        self.via_lbl.setObjectName("via_lbl")
        self.horizontalLayout_2.addWidget(self.via_lbl)
        self.via_dsb = QDoubleSpinBox(self.groupBox_3)
        self.via_dsb.setObjectName("via_dsb")
        self.horizontalLayout_2.addWidget(self.via_dsb)
        self.pth_lbl = QLabel(self.groupBox_3)
        self.pth_lbl.setObjectName("pth_lbl")
        self.horizontalLayout_2.addWidget(self.pth_lbl)
        self.pth_dsb = QDoubleSpinBox(self.groupBox_3)
        self.pth_dsb.setObjectName("pth_dsb")
        self.horizontalLayout_2.addWidget(self.pth_dsb)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.continue_btn = QPushButton(self.groupBox)
        self.continue_btn.setObjectName("continue_btn")
        self.horizontalLayout.addWidget(self.continue_btn)
        self.stop_btn = QPushButton(self.groupBox)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))
        self.inner_lbl.setText(_translate("Form", "内层补偿（整体）"))
        self.groupBox_3.setTitle(_translate("Form", "GroupBox"))
        self.trace_lbl.setText(_translate("Form", "线(Trace)："))
        self.surface_lbl.setText(_translate("Form", "大铜面(Surface):"))
        self.tear_lbl.setText(_translate("Form", "泪滴属性(Tear_Drop):"))
        self.via_lbl.setText(_translate("Form", "VIA Pad:"))
        self.pth_lbl.setText(_translate("Form", "PTH Pad:"))
        self.groupBox.setTitle(_translate("Form", "GroupBox"))
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

