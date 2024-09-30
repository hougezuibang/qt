import os, sys, json
import time

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}
func_data = {'func_name':"", "step":""}

def main(jobname):
    try:
        func_data['func_name'] = 'Inner_signal_layer_check'
        func_data['step'] = 'pcs'
        returndata['request'] = func_data
        return json.dumps(returndata)
    except Exception as e:
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)


if __name__ == "__main__":
    a = 0


