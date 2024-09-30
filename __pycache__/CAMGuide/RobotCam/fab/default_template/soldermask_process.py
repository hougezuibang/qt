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

def soldermask_line_resize(job, step, min_width):
    #try:
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


def soldermask_process_dfm(job, step, include_outterlayer, smdpad_ar_min, smdpad_ar_opt, coverage_sm_min, coverage_sm_opt, bridge_size, intersect_width, 
                    cut_surplus_width, cut_surplus_height, is_round, fan_shaved, prevent_vertical_flow_add_sm, 
                    prevent_vertical_flow_del_sm, drill_clearance_min , drill_clearance_opt , smd_clearance_min,
				    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, pth_fan_shave, pad_covered_clearance,
                    max_oversize_clearance, he_hong_resize_sm_in_surface = 0,
                    gas_isdrill = 0, gas_nodrill = 0, v_cut_size = 0, sm_surface_size = 0):
    try:
        if (include_outterlayer):
            outter_list = include_outterlayer
        else:
            outter_list = layer_info.get_outter_list(job)
        outter = layer_info.get_outter_list(job)
        soldermask = layer_info.get_soldermask_list(job)
        soldermask_list = []
        for p in range(len(outter_list)):
            index = outter.index(outter_list[p])
            soldermask_list.append(soldermask[index])
    except Exception as e:
        print('Failed to get soldermask layer , Skip outter and soldermask operation !')
        return 0
    #防焊优化
    smdpad_ar_min = smdpad_ar_min * 25400
    smdpad_ar_opt = smdpad_ar_opt *25400
    coverage_sm_min = coverage_sm_min * 25400
    coverage_sm_opt = coverage_sm_opt * 25400
    bridge_size = bridge_size * 25400
    intersect_width = intersect_width * 25400
    cut_surplus_width = cut_surplus_width * 25400
    cut_surplus_height = cut_surplus_height * 25400
    prevent_vertical_flow_add_sm = prevent_vertical_flow_add_sm * 25400
    prevent_vertical_flow_del_sm = prevent_vertical_flow_del_sm * 25400
    drill_clearance_min = drill_clearance_min * 25400
    drill_clearance_opt = drill_clearance_opt * 25400
    smd_clearance_min = smd_clearance_min * 25400
    smd_clearance_opt = smd_clearance_opt * 25400
    bga_clearance_min = bga_clearance_min * 25400
    bga_clearance_opt = bga_clearance_opt * 25400
    outline_width = outline_width * 25400
    he_hong_resize_sm_in_surface = he_hong_resize_sm_in_surface * 25400
    gas_isdrill = gas_isdrill * 25400
    gas_nodrill = gas_nodrill * 25400
    v_cut_size = v_cut_size * 25400
    sm_surface_size = sm_surface_size * 25400
    if max_oversize_clearance == 0:
        max_oversize_clearance = 6
    max_oversize_clearance = max_oversize_clearance * 25400
    pad_covered_clearance = pad_covered_clearance * 25400
    #删除防焊所有属性
    epcam_api.modify_attributes(job, step, soldermask_list, 1, [])
    analysis_dfm.solder_mask_DFM(job, step, soldermask_list, 'erf', smdpad_ar_min, smdpad_ar_opt, coverage_sm_min, coverage_sm_opt, 
                                bridge_size, False, False, False, True, max_oversize_clearance, intersect_width, cut_surplus_width, cut_surplus_height, 
                                is_round, fan_shaved, prevent_vertical_flow_add_sm, prevent_vertical_flow_del_sm,
                                drill_clearance_min , drill_clearance_opt , smd_clearance_min,
                                smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, pth_fan_shave, pad_covered_clearance,
                                he_hong_resize_sm_in_surface, 
                                gas_nodrill, gas_isdrill, v_cut_size, sm_surface_size)
    #     #输出参数
    #     f.write("solder_mask_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"soldermask_list:"+str(soldermask_list)+"\n"+ 
    #         "erf:"+'erf'+"\n"+"smdpad_sm_min:"+str(smdpad_ar_min)+"\n"+ "smdpad_sm_opt:"+str(smdpad_ar_opt)+"\n"+"coverage_sm_min:"+str(coverage_sm_min)+"\n"+ 
    #         "coverage_sm_opt:"+str(coverage_sm_opt)+"\n"+ "bridge_sm_min:"+str(bridge_size)+"\n"+"apply_to:"+str(False)+"\n"+"use_existing_mask:"+str(False) +"\n"+ 
    #         "use_shaves:"+str(False)+"\n"+"do_resize:"+str(True)+"\n"+"max_oversized_clearance:"+str(152400)+"\n"+ 
    #         "intersect_width:"+str(intersect_width)+"\n"+"cut_surplus_width:"+str(cut_surplus_width)+"\n"+ 
    #         "cut_surplus_height:"+str(cut_surplus_height)+"\n"+"is_round:"+str(is_round)+"\n"+"fan_shaved:"+str(fan_shaved)+"\n"+
    #         "fan_shaved:"+str(fan_shaved)+"\n"+"prevent_vertical_flow_add_sm:"+str(prevent_vertical_flow_add_sm)+"\n"+
    #         "prevent_vertical_flow_del_sm:"+str(prevent_vertical_flow_del_sm)+"\n"+ 
    #         "drill_clearance_min:"+str(drill_clearance_min)+"\n"+
    #         "drill_clearance_opt:"+str(drill_clearance_opt)+"\n"+
    #         "smd_clearance_min:"+str(smd_clearance_min)+"\n"+
    #         "smd_clearance_opt:"+str(smd_clearance_opt)+"\n"+
    #         "bga_clearance_min:"+str(bga_clearance_min)+"\n"+
    #         "bga_clearance_opt:"+str(bga_clearance_opt)+"\n"+
    #         "add_outline:"+str(add_outline)+"\n"+
    #         "outline_width:"+str(outline_width)+"\n"+
    #         "he_hong_resize_sm_in_surface:"+str(he_hong_resize_sm_in_surface)+"\n")
    # f.write("**************************\n")
    # f.close()