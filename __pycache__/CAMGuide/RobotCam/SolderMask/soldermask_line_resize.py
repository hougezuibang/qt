import import_path
import os, sys, json
import ui_soldermask_module
import time
from PyQt5.Qt import *
from soldermask_process import SolderMaskProcess
import epcam
import epcam_api
import layer_info
import job_operation
import epcam_log
import prepare_check

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

class Mycal(QThread):
    finished = pyqtSignal()
    def _init_(self):
        super().__init__()
        self.jobname = ''   
        self.stepname = ''
        self.width = 0
    def run(self):
        '''
        执行内层补偿功能
        '''
        data = {}
        data['min_width'] = self.width
        SolderMaskProcess().soldermask_line_resize(self.jobname, self.stepname, data)
        time.sleep(1)
        self.finished.emit() 

def pre_check(jobname):
    job = jobname
    step = 'pcs'
    epcam.init()
    ret = prepare_check.step_is_exist(job, step)
    if not ret['result']:
        return json.dumps(ret)
    return json.dumps(ret)
    
def main(jobname):
    try:
        job = jobname
        step = 'pcs'
        ui = ui_soldermask_module.soldermask_compensation_UI()
        ui.show()
        ui.exec()
        if ui.statue == True:
            epcam.init()
            b = Mycal()
            b.jobname = job
            b.stepname = step
            b.width = ui.width_dsb.value()
            a = ui_soldermask_module.processbar_UI(b)
            a.exec_()
        showdialog_data['request_name'] = 'Update_job'
        showdialog_data['step'] = 'pcs'
        returndata['request'] = showdialog_data
        return json.dumps(returndata)
    except Exception as e:
        epcam_log.logger.exception(sys.exc_info())
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    job = '760tbv_pre1'
    step = 'pre'
    ui = ui_soldermask_module.soldermask_compensation_UI()
    ui.show()
    ui.exec()
    if ui.statue ==True:
        epcam.init()
        epcam_api.open_job(r'C:\project\EPCAM\trunk\EPCAM\EP-CAM-Engineering\job', '760tbv_pre1')
        b=Mycal()
        b.jobname = job
        b.stepname = step
        b.width = ui.width_dsb.value()
        a = ui_soldermask_module.processbar_UI(b)
        a.exec_()
    showdialog_data['request_name'] = 'Update_job'
    showdialog_data['step'] = 'pcs'
    returndata['request'] = showdialog_data

   

   

   
