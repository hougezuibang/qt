import sys
import os
import json

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

def main(jobname):
    try:
        showdialog_data['request_name'] = 'Advanced_etching_compensation'
        showdialog_data['step'] = 'pcs'
        returndata['request'] = showdialog_data
        return json.dumps(returndata)
    except Exception as e:
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)