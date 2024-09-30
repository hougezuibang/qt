import os, sys
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_silkscreen_path = os.path.dirname(PyRecipe_base_path) + r'\module\silkscreen'
sys.path.append(PyRecipe_module_silkscreen_path)
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
import layer_info as layer_info
import job_operation
import analysis_dfm
import feature_resize
import json
import epcam
import epcam_api

class SolderMaskProcess():
    def __init__(self):
        pass
    def __del__(self):
        pass

    #防焊保证最小开窗
    def soldermask_line_resize(self, job, step, paras):
        min_width = paras['outter']['profile_line_width']
        if min_width == 0:
            return
        soldermask_list = layer_info.get_soldermask_list(job)
        min_name = 'r' + str(min_width)
        min_width = min_width * 25400
        if len(soldermask_list)==0:
            return 
        for _layer in soldermask_list:
            layer_info.reset_select_filter()
            layer_info.set_featuretype_filter(70)
            layer_info.select_features_by_filter(job, step, [_layer])
            info_list = layer_info.get_features_infos(job, step, _layer)    #获取所有line的信息
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, _layer)  #清除选中并对每一个line进行选中判断   
            if len(info_list):
                for _line_info in info_list:                       
                    epcam_api.select_feature_by_id(job, step, _layer, [_line_info[10]])
                    line_name = _line_info[2]        #线的symbolname
                    line_width = layer_info.get_drillsize_by_symbolname(line_name)   #通过symbolname获取线宽
                    if line_width < min_width:
                        layer_info.change_feature_symbols(job, step, [_layer], min_name)
                    layer_info.clear_select(job, step, _layer)
        layer_info.reset_select_filter()


    def soldermask_process_dfm(self, job, step, paras):
        include_outterlayer = []
        if 'include_outterlayer' in paras['outter']:
            include_outterlayer = paras['outter']['include_outterlayer']
        try:
            outter_list = []
            if (include_outterlayer):
                outter_list = include_outterlayer
            else:
                outter_list = layer_info.get_outter_list(job)
            outter = layer_info.get_outter_list(job)
            soldermask = []
            soldermask = layer_info.get_soldermask_list(job)
            soldermask_list = []
            for p in range(len(outter_list)):
                index = outter.index(outter_list[p])
                soldermask_list.append(soldermask[index])
        except Exception as e:
            print('Failed to get soldermask layer , Skip outter and soldermask operation !')
            return 0

        smdpad_ar_min = paras['outter']['smdpad_sm_min'] * 25400
        smdpad_ar_opt = paras['outter']['smdpad_sm_opt'] * 25400
        coverage_sm_min = paras['outter']['coverage_sm_min'] * 25400                                             
        coverage_sm_opt = paras['outter']['coverage_sm_opt'] * 25400
        bridge_size = paras['outter']['bridge_sm_min'] * 25400
        intersect_width = paras['outter']['intersect_width'] * 25400
        cut_surplus_width = paras['outter']['cut_surplus_width'] * 25400
        cut_surplus_height = paras['outter']['cut_surplus_height'] * 25400
        is_round = paras['outter']['is_round'] * 25400
        fan_shaved = paras['outter']['fan_shaped'] * 25400
        prevent_vertical_flow_add_sm = paras['outter']['soldermask_window'] * 25400
        prevent_vertical_flow_del_sm = paras['outter']['soldermask_dig'] * 25400
        drill_clearance_min = paras['outter']['pthpad_sm_min'] * 25400                                       
        drill_clearance_opt = paras['outter']['pthpad_sm_opt'] * 25400
        smd_clearance_min = paras['outter']['smdpad_sm_min'] * 25400
        smd_clearance_opt = paras['outter']['smdpad_sm_opt'] * 25400
        bga_clearance_min = paras['outter']['bgapad_sm_min'] * 25400
        bga_clearance_opt = paras['outter']['bgapad_sm_opt'] * 25400
        add_outline = paras['outter']['add_outline'] * 25400
        outline_width = paras['outter']['outline_width'] * 25400
        max_oversize_clearance = paras['outter']['max_oversize_clearance']
        if max_oversize_clearance == 0:
            max_oversize_clearance = 6
        max_oversize_clearance = max_oversize_clearance * 25400
        he_hong_resize_sm_in_surface = paras['outter']['copper_sufacepad'] * 25400
        gas_isdrill = paras['outter']['gas_isdrill'] * 25400
        gas_nodrill = paras['outter']['gas_nodrill'] * 25400
        v_cut_size = paras['outter']['v_cut'] * 25400
        sm_surface_size = 2 * 25400

        #删除防焊所有属性
        epcam_api.modify_attributes(job, step, soldermask_list, 1, [])
        analysis_dfm.solder_mask_DFM(job, step, soldermask_list, 'erf', smdpad_ar_min, smdpad_ar_opt, coverage_sm_min, coverage_sm_opt, 
                                    bridge_size, False, False, False, True, max_oversize_clearance, intersect_width, cut_surplus_width, cut_surplus_height, 
                                    is_round, fan_shaved, prevent_vertical_flow_add_sm, prevent_vertical_flow_del_sm,
                                    drill_clearance_min , drill_clearance_opt , smd_clearance_min,
                                    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, he_hong_resize_sm_in_surface, 
                                    gas_nodrill, gas_isdrill, v_cut_size, sm_surface_size)