import os, sys
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
import layer_info as layer_info
import feature_resize as feature_resize

#指定满足要求的孔和resize的大小
def resize_specify(job, step, layer, sel_type, size):
    layer_name = layer_info.get_drill_layer_name(job)
    layers = [layer]
    feature_resize.resize_global(job, step, layers, sel_type, size)


#指定满足要求的孔和resize的大小
def resize_base_symbol(job, step, sel_type, size):
    layer_name = layer_info.get_drill_layer_name(job)
    layers = []
    layers.append(layer_name)
    feature_resize.resize_global(job, step, layer, sel_type, size)

