import os, sys
import import_camflow_path
import layer_info
import epcam_api

#指定满足要求的孔和resize的大小
def resize_specify(job, step, layer, sel_type, size):
    layer_name = layer_info.get_drill_layer_name(job)
    layers = [layer]
    epcam_api.resize_global(job, step, layers, sel_type, size)


#指定满足要求的孔和resize的大小
def resize_base_symbol(job, step, sel_type, size):
    layer_name = layer_info.get_drill_layer_name(job)
    layers = []
    layers.append(layer_name)
    epcam_api.resize_global(job, step, layer, sel_type, size)

