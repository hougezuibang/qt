import os, sys, json
PyRecipe_module_outter_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
import job_operation as job_operation
import layer_info as layer_info 

#将防焊层copy备份
def soldermask_copy_layer(job, soldermask_layers):
    try:
        for i in range(0, len(soldermask_layers)):
            new_layer = job_operation.copy_layer(job, soldermask_layers[i])
            #修改新复制出的内层的context为misc
            layer_info.change_layer_context(job, new_layer, 'misc')
            #修改newlayer名
            rename = soldermask_layers[i] + '-min'
            job_operation.rename_layer(job, new_layer, rename)
    except:
        print('soldermask_copy_layer skip')