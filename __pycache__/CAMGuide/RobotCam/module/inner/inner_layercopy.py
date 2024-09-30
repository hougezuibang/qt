import os, sys, json
PyRecipe_module_inner_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_path + r'\epcam')
import job_operation as job_operation
import layer_info as layer_info 
import epcam


#将内层copy备份
def inner_copy_layer(job):
    inner_list = layer_info.get_inner_layer_list(job)
    for i in range(0, len(inner_list)):
        new_layer = job_operation.copy_layer(job, inner_list[i])
        #修改新复制出的内层的context为misc
        layer_info.change_layer_context(job, new_layer, 'misc')
        #修改newlayer名
        rename = inner_list[i] + '-min'
        job_operation.rename_layer(job, new_layer, rename)
