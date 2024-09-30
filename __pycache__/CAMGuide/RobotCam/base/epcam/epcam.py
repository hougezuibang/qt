from ctypes import *
import ctypes
import sys
import os
import threading
#import win32api
#from libc.stdlib cimport malloc, free
#%env DYLD_LIBRARY_PATH ./bin
#%env LD_LIBRARY_PATH ./bin

sys.path.append(os.path.dirname(__file__))
#bin_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\bin'
#base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
base_dir = os.path.basename(base_path)
if base_dir == "EP-CAM-Engineering":
    trunk_path = os.path.dirname(os.path.dirname(base_path))
    bin_path = os.path.join(trunk_path,'bin/x64/Release')
else:
    bin_path = base_path
sys.path.append(bin_path)
#print(os.environ('path'))
#epbin_path = os.getcwd() + r"\bin"
#os.environ['path'] += (r";" + epbin_path)

ld_path = os.getenv('LD_LIBRARY_PATH')

#print(epbin_path +  r"\EPCAM_CTYPE.dll")
#dll = ctypes.cdll.LoadLibrary(pp)

#epbin_path = os.getcwd() + r'py\bin"
os.environ['path'] += (r";" + bin_path)

dll = ctypes.CDLL(bin_path + r"\EPCAM_CTYPE.dll")
dmsdll = ctypes.CDLL(bin_path + r"\DMS_CTYPE.dll")
vdll = ctypes.CDLL(bin_path + r"\Form_View.dll")


dll.process.restype =  ctypes.c_char_p
dll.init_func_map.restype =  ctypes.c_char_p
dll.init_orig_func_map.restype =  ctypes.c_char_p
dll.process.argtypes = [ctypes.c_char_p]
vdll.init.argtypes = [ctypes.c_char_p]
vdll.view_cmd.argtypes = [ctypes.c_char_p]
dmsdll.init.restype = ctypes.c_char_p
dmsdll.uploadmongo.restype = ctypes.c_char_p
dmsdll.getParam.restype = ctypes.c_char_p
dmsdll.downloadjob.restype = ctypes.c_char_p

dmsdll.downloadorigin.restype = ctypes.c_char_p
dmsdll.downloadpre.restype = ctypes.c_char_p
#cdef extern from"stdio.h":
#    extern int printf(const char* format, ...)
dmsdll.upload_robot2mongo.restype = ctypes.c_char_p

dmsdll.getOrderInfoByJobName.restype = ctypes.c_char_p
dmsdll.set_robot_status.restype = ctypes.c_int
dmsdll.epdms_order_status_update.restype = ctypes.c_char_p
dmsdll.epdms_flow_status_update.restype = ctypes.c_char_p
dmsdll.get_mongo_fsname.restype = ctypes.c_char_p

global threadshow

def dms_init():
    dmsdll.init()

def uploadmongo(djson):
    string_djson = bytes(djson, encoding='utf-8')
    ret = dmsdll.uploadmongo(string_djson)
    return ret.decode('utf-8')

def upload_robot2mongo(djson):
    string_djson = bytes(djson, encoding='utf-8')
    ret = dmsdll.upload_robot2mongo(string_djson)
    return ret.decode('utf-8')

def getParam(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.getParam(string_dmsjson)
    return ret.decode('utf-8')
    
def downloadjob(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.downloadjob(string_dmsjson)
    return ret.decode('utf-8')


def downloadorigin(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.downloadorigin(string_dmsjson)
    return ret.decode('utf-8')

def downloadpre(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.downloadpre(string_dmsjson)
    return ret.decode('utf-8')

def get_mongo_fsname(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.get_mongo_fsname(string_dmsjson)
    return ret.decode('utf-8')

def init_robot_status(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    dmsdll.init_robot_status(string_dmsjson)

def getOrderInfoByJobName(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.getOrderInfoByJobName(string_dmsjson)
    return ret.decode('utf-8')
    
def set_robot_status(dmsjson, status):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.set_robot_status(string_dmsjson, status)
    return ret
    
def epdms_order_status_update(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.epdms_order_status_update(string_dmsjson)
    return ret.decode('utf-8')

def epdms_flow_status_update(dmsjson):
    string_dmsjson = bytes(dmsjson, encoding='utf-8')
    ret = dmsdll.epdms_flow_status_update(string_dmsjson)
    return ret.decode('utf-8')

def SayHello():
    print("hello, world!\n")

def init():
    ret = dll.init_func_map()
    ret = dll.init_orig_func_map()
    vstring_path = bytes(bin_path, encoding='utf-8')
    vdll.init(vstring_path)
    return ret.decode('utf-8')

def set_use_times(times):
    times.encode('utf-8')
    #print(type(json))
    times_str = bytes(times, encoding='utf-8')
    dll.setUseTimes(times_str)

def process(json):
    json.encode('utf-8')
    #print(type(json))
    string_buff = bytes(json, encoding='utf-8')
    #print(type(string_buff), string_buff)
    ret = dll.process(string_buff)
    #print(ret)
    return ret.decode('utf-8')


def view_cmd(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    # string_job = bytes(job, encoding='utf-8')
    # string_step = bytes(step, encoding='utf-8')
    # string_layer = bytes(layer, encoding='utf-8')
    vdll.view_cmd(string_vjson)
    # global threadshow
    # threadshow = threading.Thread(target=vdll.show, args=(string_path, string_job, string_step, string_layer))
    # threadshow.start()

# def alertStep(step,layer):
#     string_step = bytes(step, encoding='utf-8')
#     string_layer = bytes(layer, encoding='utf-8')
#     vdll.alertStep(string_step, string_layer)
#
# def threadjoin():
#     global threadshow
#     threadshow.join()
#
# def refresh(clayer):
#     string_clayer = bytes(clayer, encoding='utf-8')
#     print(string_clayer)
#     vdll.refresh(string_clayer)

