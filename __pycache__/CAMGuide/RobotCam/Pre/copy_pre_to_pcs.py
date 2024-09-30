import import_path
import sys
import os
import json
import time
from PyQt5.Qt import *
import ui_module
import epcam_api as epcam_api
import epcam
import job_operation
import layer_info
import prepare_check



returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

class Mycal(QThread):
    finished = pyqtSignal()
    def _init_(self):
        super().__init__()
        self.name=''

    def run(self):
        # time.sleep(10)
        epcam.init()
        ret = job_operation.copy_step(self.name,"pre")
        #print(ret)
        job_operation.rename_step(self.name, ret, "pcs")

        self.finished.emit() 

def pre_check(jobname):
    epcam.init()
    job = jobname
    ret = prepare_check.step_is_exist(job, 'pre')
    if not ret['result']:
        return json.dumps(ret)
    ret = prepare_check.step_is_already_exist(job, 'pcs')
    if not ret['result']:
        return json.dumps(ret)
    return json.dumps(ret)

def main(jobname):
    try:
        #判断是否存在pre层, 不存在则提示且不执行
        pre_check(jobname)
        b = Mycal()
        b.name = jobname
        a = ui_module.processbar_UI(b)
        a.exec_() 

        showdialog_data['request_name']='Graphic'
        showdialog_data['step']='pcs'
        returndata['request']=showdialog_data
        return json.dumps(returndata)
    except Exception as e:
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    epcam.init()
    epcam_api.open_job(r'C:\project\EPCAM\trunk\EPCAM\EP-CAM-Engineering\job', 'ep-10l-prepare_ep_10')
    main('ep-10l-prepare_ep_10')
