import os, sys, json
epcam_path = os.path.dirname(os.path.realpath(__file__)) + r'\epcam'
if epcam_path not in sys.path:
    sys.path.append(epcam_path)
import epcam
import epcam_api
import job_operation
import layer_info
from PyQt5.Qt import *

returndata = {'result':True,"status":"","request":""}

#判断step是否存在
def step_is_exist(job, step):
    steps = job_operation.get_all_steps(job)
    returndata['result'] = True
    returndata['status'] = ''
    if step not in steps:
        msg = 'job has no ' + step + ' step'
        returndata['result'] = False
        returndata['status'] = msg
        #QMessageBox.information(QWidget(), 'Information', msg, QMessageBox.Ok)
    return returndata

#不需要step存在时提示
def step_is_already_exist(job, step):
    steps = job_operation.get_all_steps(job)
    returndata['result'] = True
    returndata['status'] = ''
    if step in steps:
        msg = 'job already has ' + step + ' step'
        returndata['result'] = False
        returndata['status'] = msg
        #QMessageBox.information(QWidget(), 'Information', msg, QMessageBox.Ok)
    return returndata

#判断layer是否存在
def layer_is_exist(job, layer):
    layers = job_operation.get_all_layers(job)
    returndata['result'] = True
    returndata['status'] = ''
    if layer not in layers:
        msg = 'job has no ' + layer + ' layer'
        returndata['result'] = False
        returndata['status'] = msg
        #QMessageBox.information(QWidget(), 'Information', msg, QMessageBox.Ok)
    return returndata

#判断step是否有profile
def step_has_profile(job, step):
    setpoly = layer_info.get_profile(job, step)
    setpoly  = json.loads(setpoly)
    returndata['result'] = True
    returndata['status'] = ''
    if 'points' not in setpoly:
        msg = 'Step does not has profile, Please confirm'
        #QMessageBox.information(QWidget(), 'Information', msg, QMessageBox.Ok)
        returndata['result'] = False
        returndata['status'] = msg
    return returndata




if __name__ == "__main__":
    app = QApplication(sys.argv)
    epcam.init()
    epcam_api.open_job(r'C:\project\EPCAM\trunk\EPCAM\EP-CAM-Engineering\job', 'ep-10l-prepare_ep_10')
    flag = step_has_profile('ep-10l-prepare_ep_10', 'org')
    aaa = 0
    