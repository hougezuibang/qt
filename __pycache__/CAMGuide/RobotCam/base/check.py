import os,sys,time,shutil,re
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api
import json
import job_operation
import epcam_api
import epcam as epcam
import layer_info
import feature_resize
import math

def ok_step_check(job, step1, step2, layers):
    result = {'job': job, 'layer':{}}
    dst_layers = []
    for _layer in layers:
        point_list = epcam_api.layer_compare_point(job, step1, _layer, job, step2, _layer)
        point_list=json.loads(point_list)
        result['layer'][_layer] = point_list
        dst_layer = _layer + '-ok'
        job_operation.create_layer(job, dst_layer)
        dst_layers.append(dst_layer)
    
    result=json.dumps(result)
    epcam_api.ok_step_check(result)
    epcam_api.copy_layer_features(job, step2, layers, job, step1, dst_layers, True, False)

