import os, sys
PyRecipe_module_outter_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_path + r'\epcam')
import layer_info
import feature_resize
import job_operation
import epcam_api as api
import json
import epcam
import analysis_dfm

#根据npth孔，在soldermask层对应位置添加开窗
def soldermask_add_npth_window(job, step, pthpad_sm):
    try:
        drill_layers = layer_info.get_drill_layer_name(job)
        soldermask_layers = layer_info.get_soldermask_list(job)
        if drill_layers == []:
            print('no drill_layer found !')
            return 0
        for i in range(len(drill_layers)):
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, drill_layers[i])
            layer_info.select_features_by_attributes(job, step, [drill_layers[i]], 1, [{".drill": "non_plated"}])
            pad_list = layer_info.get_selected_pad_point(job, step, drill_layers[i])
            if pad_list == []:
                continue
            new_drill_layer = drill_layers[i] + '-copy'
            job_operation.create_layer(job, new_drill_layer)
            layer_info.sel_copy_other(job, step, [drill_layers[i]], [new_drill_layer], False, 0, 0, 0, 0, 0, 0, 0)
            feature_resize.resize_global(job, step, [new_drill_layer], 1, pthpad_sm * 25400)
            layer_info.sel_copy_other(job, step, [new_drill_layer], soldermask_layers, False, 0, 0, 0, 0, 0, 0, 0)
            job_operation.delete_layer(job, new_drill_layer)
    except:
        print('soldermask_add_npth_window skip')



