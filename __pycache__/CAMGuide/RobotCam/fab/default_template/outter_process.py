import os, sys, json
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(__file__)) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_outter_path = os.path.dirname(os.path.dirname(__file__)) + r'\module\outter'
sys.path.append(PyRecipe_module_outter_path)
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
sys.path.append(PyRecipe_epcam_path)
import layer_info as layer_info
import analysis_dfm
import epcam
import epcam_api
import job_operation
import job_input

#print("*"*100)
#print(os.path.dirname(__file__))
module_outter_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+r"\module\outter"
#print(module_outter_path)
sys.path.append(module_outter_path)
#print("*"*100)
module_soldermask_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+r"\module\soldermask"
sys.path.append(module_soldermask_path)
import outter_resize
import outter_copy as outter_copy
import soldermask_resize
import soldermask_copy
import job_input_XY


#外层涨至最小值，以及防焊开窗的处理
def outter_process_resize(job, step, line_resize, surface_resize, smd_resize, bga_resize, mark_resize, pthpad_dl_min, smdpad_ar_min, bgapad_ar_min, 
                            pthpad_sm_min, drillpad_opt_size, smdpad_ar_opt, bgapad_ar_opt, coverage_sm_min, coverage_sm_opt,
                            bridge_size, pth_dl_opt, via_dl_min, via_dl_opt, pth_sm_opt, include_outterlayer, 
                            arc_angle, bga_pads, intersect_width, cut_surplus_width, is_round, coverage_min,  
                            mending_copper_wire, add_tear, line2surface, min_add_tear, 
                            avoid_NPTH, sm_NPTH_size, teardrop_line_width_radio, fill_seam,
                            cut_surplus_height, 
                            fan_shaved, prevent_vertical_flow_add_sm, prevent_vertical_flow_del_sm, pthsize, viasize, manual_sliver_check,
                            drill_clearance_min , drill_clearance_opt , smd_clearance_min, smd_clearance_opt , bga_clearance_min, bga_clearance_opt,
                            avoid_profile_size, signal_layer_DFM_show, avoid_features_DFM_op_show, New_signal_layer_DFM_show,
                            sliver_DFM_op_show, teardrop_create_DFM_show, line2laser, surface2laser, pth2laser, via2laser, smd2laser, bga2laser,
                            laser2laser, line_to_laser_artio, surface_to_laser_artio, pth_to_laser_artio, via_to_laser_artio, smd_to_laser_artio, bga_to_laser_artio,
                            blind_min, blind_opt, add_outline, outline_width, he_hong_resize_sm_in_surface, rules, smdbga_less, smdbga_compensate, soldermaskflag,
                            sm_PTH_size, gas_isdrill, gas_nodrill, v_cut_size, sm_surface_size, avoid_v_cut, tdsize): 
     #新建参数txt
    param_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + r'\parameter'
    if not os.path.exists(param_path):
        os.makedirs(param_path)
    f = open(param_path + '\\' + job + ".txt", "a")
    f.write("***********\n")
    f.write("   outter   \n")
    f.write("***********\n")
    # #设置梯形图relationship
    # line_to_surface_artio = line_to_surface_artio * 0.01
    # line_to_smd_artio = line_to_smd_artio * 0.01
    # line_to_bga_artio = line_to_bga_artio * 0.01
    # line_to_pth_artio = line_to_pth_artio * 0.01
    # line_to_via_artio = line_to_via_artio * 0.01
    # surface_to_smd_artio = surface_to_smd_artio * 0.01
    # surface_to_bga_artio = surface_to_bga_artio * 0.01
    # surface_to_pth_artio = surface_to_pth_artio * 0.01
    # surface_to_via_artio = surface_to_via_artio * 0.01
    # smd_to_bga_artio = smd_to_bga_artio * 0.01
    # smd_to_pth_artio = smd_to_pth_artio * 0.01
    # smd_to_via_artio = smd_to_via_artio * 0.01
    # bga_to_pth_artio = bga_to_pth_artio * 0.01
    # bga_to_via_artio = bga_to_via_artio * 0.01
    # pth_to_via_artio = pth_to_via_artio * 0.01
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.fiducial_name=trace', line2line, 0.5)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.pattern_fill', line2surface, line_to_surface_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.smd', line2smd, line_to_smd_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.bga', line2bga, line_to_bga_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.pth_pad', line2pth, line_to_pth_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.via_pad', line2via, line_to_via_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.laser_via_pad', line2laser, line_to_laser_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.pattern_fill', surface2surface, 0.5)
    # analysis_dfm.setRelationship('.pattern_fill', '.smd', surface2smd, surface_to_smd_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.bga', surface2bga, surface_to_bga_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.pth_pad', surface2pth, surface_to_pth_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.via_pad', surface2via, surface_to_via_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.laser_via_pad', surface2laser, surface_to_laser_artio)
    # analysis_dfm.setRelationship('.smd', '.smd', smd2smd, 0.5)
    # analysis_dfm.setRelationship('.smd', '.bga', smd2bga, smd_to_bga_artio)
    # analysis_dfm.setRelationship('.smd', '.pth_pad', smd2pth, smd_to_pth_artio)
    # analysis_dfm.setRelationship('.smd', '.via_pad', smd2via, smd_to_via_artio)
    # analysis_dfm.setRelationship('.smd', '.laser_via_pad', smd2laser, smd_to_laser_artio)
    # analysis_dfm.setRelationship('.bga', '.bga', bga2bga, 0.5)
    # analysis_dfm.setRelationship('.bga', '.pth_pad', bga2pth, bga_to_pth_artio)
    # analysis_dfm.setRelationship('.bga', '.via_pad', bga2via, bga_to_via_artio)
    # analysis_dfm.setRelationship('.bga', '.laser_via_pad', bga2laser, bga_to_laser_artio)
    # analysis_dfm.setRelationship('.pth_pad', '.pth_pad', pth2pth, 0.5)
    # analysis_dfm.setRelationship('.pth_pad', '.via_pad', pth2via, pth_to_via_artio)
    # analysis_dfm.setRelationship('.pth_pad', '.laser_via_pad', pth2laser, pth_to_laser_artio)
    # analysis_dfm.setRelationship('.via_pad', '.via_pad', via2via, 0.5)
    # analysis_dfm.setRelationship('.via_pad', '.laser_via_pad', via2laser, via_to_laser_artio)
    # analysis_dfm.setRelationship('.laser_via_pad', '.laser_via_pad', laser2laser, 0.5)

    # #设置梯形图Introduction
    # analysis_dfm.setIntroduction('.fiducial_name=trace', line_resize, 0, line_resize, 0, False)
    # analysis_dfm.setIntroduction('.pattern_fill', surface_resize, 0, 0, 0, False)
    # analysis_dfm.setIntroduction('.smd', smd_resize, 0, smd_resize, 0, True)
    # analysis_dfm.setIntroduction('.bga', bga_resize, 0, bga_resize, 0, True)
    # analysis_dfm.setIntroduction('.pth_pad', 0, pthpad_dl_min, 0, pth_dl_opt, True)
    # analysis_dfm.setIntroduction('.via_pad', 0, via_dl_min, 0, via_dl_opt, True)
    # analysis_dfm.setIntroduction('.laser_via_pad', 0, blind_min, 0, blind_opt, True)

    # #输出梯形图参数
    # f.write("Relationship:\n线到线:" + str(line2line) + "\n" + "线到铜:" + str(line2surface) + "\n" + "线到SMDPad:" + str(line2smd) + "\n" 
    #     + "线到BGAPad:" + str(line2bga) + "\n" + "线到PTHPad:" + str(line2pth) + "\n" + "线到VIAPad:" + str(line2via) + "\n" 
    #     + "铜到铜:" + str(surface2surface) + "\n" + "铜到SMDPad:" + str(surface2smd) + "\n" + "铜到BGAPad:" + str(surface2bga) + "\n" 
    #     + "铜到PTH孔:" + str(surface2pth) + "\n" + "铜到VIA孔:" + str(surface2via) + "\n" 
    #     + "SMDPad到SMDPad:" + str(smd2smd) + "\n" + "SMDPad到BGAPad:" + str(smd2bga) + "\n" 
    #     + "SMDPad到PTHPad:" + str(smd2pth) + "\n" + "SMDPad到VIAPad:" + str(smd2via) + "\n"
    #     + "BGAad到BGAPad:" + str(bga2bga) + "\n" + "BGAPad到PTHPad:" + str(bga2pth) + "\n" 
    #     + "BGAPad到VIAPad:" + str(bga2via) + "\n" + "PTHPad到PTHPad:" + str(pth2pth) + "\n" 
    #     + "PTHPad到VIAPad:" + str(pth2via) + "\n" + "VIAPad到VIAPad:" + str(via2via) + "\n" 
    #     + "Introduction:\n线:" + "(" + str(line_resize) + " " + str(0) + " " + str(line_resize) + " " 
    #     + str(0) + " " +  str(False) + " " + str(100) + ")" + "\n" 
    #     + "铜:" + "(" + str(surface_resize) + " " + str(0) + " " + str(0) + " " + str(0) + " " +  str(False) + " " + str(100) + ")" + "\n" 
    #     + "SMDPad:" + "(" + str(smd_resize) + " " + str(0) + " " + str(smd_resize) + " " + str(0) + " " +  str(True) + " " + str(95) + ")" + "\n" 
    #     + "BGAPad:" + "(" + str(bga_resize) + " " + str(0) + " " + str(bga_resize) + " " + str(0) + " " +  str(True) + " " + str(98) + ")" + "\n" 
    #     + "PTHPad:" + "(" + str(0) + " " + str(pthpad_dl_min) + " " + str(0) + " " + str(pth_dl_opt) + " " +  str(True) + " " + str(90) + ")" + "\n" 
    #     + "VIAPad:" + "(" + str(0) + " " + str(via_dl_min) + " " + str(0) + " " + str(via_dl_opt) + " " +  str(True) + " " + str(80) + ")" + "\n") 
    # f.write("**************************\n")

    #参数转为纳米单位
    pth_dl_opt = pth_dl_opt * 25400
    via_dl_min = via_dl_min * 25400
    via_dl_opt = via_dl_opt * 25400
    line2surface = line2surface * 25400
    smdpad_ar_opt = smdpad_ar_opt * 25400
    bgapad_ar_opt = bgapad_ar_opt * 25400
    coverage_sm_min = coverage_sm_min * 25400
    coverage_sm_opt = coverage_sm_opt * 25400
    bridge_size = bridge_size * 25400
    pth_sm_opt = pth_sm_opt * 25400
    intersect_width = intersect_width * 25400
    cut_surplus_width = cut_surplus_width * 25400
    cut_surplus_height = cut_surplus_height * 25400

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


    #备份原layer
    # for v in range(len(outter_list)):
    #     prepare_layer = job_operation.copy_layer(job, outter_list[v])
    #     pcs_layer = outter_list[v] + '-pre'
    #     job_operation.rename_layer(job, prepare_layer, pcs_layer, 'misc')

    # for t in range(len(soldermask_list)):
    #     prepare_smlayer = job_operation.copy_layer(job, soldermask_list[t])
    #     sm_layer = soldermask_list[t] + '-pre'
    #     job_operation.rename_layer(job, prepare_smlayer, sm_layer, 'misc')  

    #清空筛选
    layer_info.reset_select_filter()

    #外层蚀刻补偿（resize_global）
    smdbga_less = smdbga_less * 25400
    smdbga_compensate = smdbga_compensate * 25400
    job_input.outterlayer_resize(job, step, smdbga_less, smdbga_compensate, line_resize, surface_resize, smd_resize, bga_resize, mark_resize, pthsize, viasize, tdsize)
    #job_input_XY.outterlayer_resize(job, step, smdbga_less, smdbga_compensate, line_resize, surface_resize, smd_resize, bga_resize, mark_resize, pthsize, viasize, tdsize,
    #                            line_resize_list, smd_resize_list, bga_resize_list)

    #复制处理后的外层
    #outter_copy.outter_copy_layer(job, outter_list)

    #复制处理后的防焊层
    #soldermask_copy.soldermask_copy_layer(job, soldermask_list)

    #涨PTH_Pad和VIA_Pad（调用优化signal_layer_DFM）
    pthpad_dl_min = pthpad_dl_min * 25400  
    spacingmin = 0.5 * 25400  
    laser_dl_min = blind_min * 25400
    laser_dl_opt = blind_opt * 25400
    analysis_dfm.signal_layer_DFM(job, step, outter_list, 'erf', pthpad_dl_min, pth_dl_opt, via_dl_min, via_dl_opt, 
                                0, 0, spacingmin, spacingmin, spacingmin, spacingmin, 25400, 254000, 10, 127000, 203200, 
                                True, True, True, True, True, False, False, False, False, False, False, False, laser_dl_min, laser_dl_opt, 0, 0)
    #输出参数
    f.write("signal_layer_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
           "erf:"+'erf'+"\n"+"pthpad_dl_min:"+str(pthpad_dl_min)+"\n"+ "pthpad_dl_opt:"+str(pth_dl_opt)+"\n"+"viapad_dl_min:"+str(via_dl_min)+"\n"+ 
           "viapad_dl_opt:"+str(via_dl_opt)+"\n"+ "mvia_ar_min:"+str(0)+"\n"+"mvia_ar_opt:"+str(0)+"\n"+"spacing_min:"+str(spacingmin) +"\n"+ 
           "spacing_opt:"+str(spacingmin)+"\n"+"pad_to_pad_spacing_min:"+str(spacingmin)+"\n"+"pad_to_pad_spacing_opt:"+str(spacingmin)+"\n"+"lre_range_fr:"+str(25400)+"\n"+ 
           "lre_range_to:"+str(254000)+"\n"+"reduction:"+str(10)+"\n"+"abs_min:"+str(127000)+"\n"+"drill_to_cu:"+str(203200)+"\n"+ 
           "apply_to:"+str(True)+"\n"+"pads:"+str(True)+"\n"+"smds:"+str(True)+"\n"+"drills:"+str(True)+"\n"+"padup:"+str(True)+"\n"+ 
           "shave:"+str(False)+"\n"+"paddn:"+str(False)+"\n"+"rerout:"+str(False)+"\n"+"linedn:"+str(False)+"\n"+"reshape:"+str(False)+"\n"+
           "padup_can_touch_pad:"+str(False)+"\n"+"cut_pad_touch_pad:"+str(False)+"\n" + "laser_ar_min:"+str(laser_dl_min)+"\n"+"laser_ar_opt:"+str(laser_dl_opt)+"\n")
    f.write("**************************\n") 
    if signal_layer_DFM_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": outter_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js) 

    #处理SMD_Pad,保证开窗与对应pad的最佳公差(仅针对cle属性操作)
    #outter_resize.smd_pad_resize_opt(job, step, smdpad_ar_opt, outter_list, smd_resize)

    #处理BGA_Pad,保证开窗与对应pad的最佳公差(仅针对cle属性操作)
    #outter_resize.bga_pad_resize_opt(job, step, bgapad_ar_opt, outter_list, bga_resize)

    #处理PTH_Pad开窗至最佳公差
    #outter_resize.clearance_resize_opt(job, step, outter_list, soldermask_list, {".pth_pad":""}, pth_sm_opt)

    #处理VIA_Pad开窗至最佳公差
    #outter_resize.clearance_resize_opt(job, step, outter_list, soldermask_list, {".via_pad":""}, pth_sm_opt)
    
    #避铜(调用优化avoid_conductor_DFM_op)
    coverage_min = coverage_min * 25400 #补
    #coverage_opt = coverage_opt * 25400 #削
    coverage_opt = 0
    use_global = True
    analysis_dfm.avoid_conductor_DFM_op(job, step, outter_list, 'erf', coverage_min, coverage_opt, 0, mending_copper_wire, manual_sliver_check, use_global, 0, 0) 
    #输出参数
    f.write("avoid_conductor_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"coverage_min:"+str(coverage_min)+"\n"+ 
           "coverage_opt:"+str(coverage_opt)+"\n"+"radius_opt:"+str(0)+"\n"+ "mending_copper_wire:"+str(mending_copper_wire)+"\n" 
           + "fast_avoid_copper:"+str(manual_sliver_check)+"\n"+ "use_global:"+str(use_global)+"\n" + "viadrill2Cu:"+str(0)+"\n"
           + "pthdrill2Cu:"+str(0)+"\n")
    f.write("**************************\n")
    #人工检查补细丝
    if manual_sliver_check:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":outter_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js)


    #避NPTH孔和profile线（调用优化avoid_features_DFM_op）（外层做NPTH开窗）（外层无VIA独立孔）
    avoid_NPTH = avoid_NPTH * 25400 
    sm_NPTH_size1 = sm_NPTH_size * 25400
    avoid_profile_size = avoid_profile_size * 25400
    avoid_v_cut = avoid_v_cut * 25400
    analysis_dfm.avoid_features_DFM_op(job, step, outter_list, 'erf', True, avoid_profile_size, True, avoid_NPTH, False, 0, True, sm_NPTH_size1, avoid_v_cut)
    #输出参数
    f.write("avoid_features_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"avoid_profile:"+str(True)+"\n"+ "avoid_profile_size:"+str(avoid_profile_size)+"\n"+ 
            "avoid_npth:"+str(True)+"\n"+ "avoid_npth_size:"+str(avoid_NPTH)+"\n"+ "avoid_alone_drill:"+str(False)+"\n"+
            "avoid_alone_drill_size:"+str(0)+"\n"+"npth_add_solder_mask:"+str(True)+"\n"+"npth_add_solder_mask_size:"+str(sm_NPTH_size1)+"\n"
            +"avoid_v_cut:"+str(avoid_v_cut)+"\n") 
    f.write("**************************\n") 
    if avoid_features_DFM_op_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": outter_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js) 

    #削PAD(旧版)
    # analysis_dfm.signal_layer_DFM(job, step, outter_list, 'erf', pthpad_dl_min, pth_dl_opt, via_dl_min, via_dl_opt, 
    #                             0, 0, spacing_min, spacing_min, spacing_min, spacing_min, 25400, 
    #                             254000, 10, 127000, 203200, True, True, True, True, False, True, False, False, False, False, False, False)

    #削PAD(调用优化New_signal_layer_DFM)
    analysis_dfm.New_signal_layer_DFM(job, step, outter_list, 'erf', False, 0)
    #输出参数
    f.write("New_signal_layer_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"cut_pad_touch_pad:"+str(False)+"\n") 
    f.write("**************************\n") 
    if New_signal_layer_DFM_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": outter_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js) 

    #补细丝（调用优化sliver_DFM_op）
    if fill_seam != 0:
        fill_seam = fill_seam * 25400
        analysis_dfm.sliver_DFM_op(job, step, outter_list, 'erf', fill_seam, fill_seam)    #2.5
        #输出参数
        f.write("sliver_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"max_width:"+str(fill_seam)+"\n"+ "max_height:"+str(fill_seam)+"\n")
        if sliver_DFM_op_show == True:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": outter_list[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js) 

    #加泪滴（调用优化teardrop_create_DFM）（BGA可选是否添加泪滴）
    min_add_tear = min_add_tear * 25400
    use_arc_tear = False
    if arc_angle > 0:
        use_arc_tear = True
    #teardrop_line_width_radio(0 ~ 1)
    if add_tear:
        analysis_dfm.teardrop_create_DFM(job, step, outter_list, 'erf', 0, True, True, min_add_tear, 0, 2032000, 
                                line2surface, 279400, 0, False, True, use_arc_tear, arc_angle, bga_pads, teardrop_line_width_radio)
        #输出参数
        f.write("teardrop_create_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"outter_list:"+str(outter_list)+"\n"+ 
           "erf:"+'erf'+"\n"+"sel_type:"+str(0)+"\n"+ "drilled_pads:"+str(True)+"\n"+"undrilled_pads:"+str(True)+"\n"+ 
           "ann_ring_min:"+str(min_add_tear)+"\n"+ "drill_size_min:"+str(0)+"\n"+"drill_size_max:"+str(2032000)+"\n"+ 
           "spacing_min:"+str(line2surface)+"\n"+ "drill_spacing:"+str(279400)+"\n"+"delete_old_teardrops:"+str(0)+"\n"+ 
           "apply_to:"+str(False)+"\n"+"work_mode:"+str(True)+"\n"+ "use_arc_tear:"+str(use_arc_tear)+"\n"+"arc_angle:"+str(arc_angle)+"\n"+ 
           "bga_pads:"+str(bga_pads)+"\n" + "tear_line_width_ratio:"+str(teardrop_line_width_radio)+"\n") 
        f.write("**************************\n")
        if teardrop_create_DFM_show == True:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": outter_list[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js) 

    #动态补偿（待集成）

    # # 防焊优化前保存料号
    # job_operation.save_job(job)
    # # 压缩tgz
    # file_name = os.path.basename(out_path)
    # file_path = os.path.dirname(out_path)
    # outter_file = file_name.split('.')[0] + '_outter'
    # outter_file = outter_file + '.tgz'
    # job_operation.maketgz(in_path, file_path, outter_file)

    #pth npth开窗
    sm_clearance = sm_PTH_size * 25400 * 0.5
    sm_np_clearance = sm_NPTH_size * 25400 * 0.5
    add_sm_pads = True
    add_signal_pads = False
    analysis_dfm.npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads)
    #输出参数
    f.write("npth_and_pth_prepare_op:\njob:"+job+"\n"+"step:"+step+"\n"+"sm_clearance:"+str(sm_clearance)+"\n"+ 
        "sm_np_clearance:"+str(sm_np_clearance)+"\n"+"add_sm_pads:"+str(add_sm_pads)+"\n"+ "add_signal_pads:"+str(add_signal_pads)+"\n") 
    f.write("**************************\n")
    f.close()

    # f.write("***********\n")
    # f.write(" soldermask \n")
    # f.write("***********\n")
    # #防焊优化
    # smdpad_ar_min = smdpad_ar_min * 25400
    # prevent_vertical_flow_add_sm = prevent_vertical_flow_add_sm * 25400
    # prevent_vertical_flow_del_sm = prevent_vertical_flow_del_sm * 25400
    # drill_clearance_min = drill_clearance_min * 25400
    # drill_clearance_opt = drill_clearance_opt * 25400
    # smd_clearance_min = smd_clearance_min * 25400
    # smd_clearance_opt = smd_clearance_opt * 25400
    # bga_clearance_min = bga_clearance_min * 25400
    # bga_clearance_opt = bga_clearance_opt * 25400
    # outline_width = outline_width * 25400
    # he_hong_resize_sm_in_surface = he_hong_resize_sm_in_surface * 25400
    # gas_isdrill = gas_isdrill * 25400
    # gas_nodrill = gas_nodrill * 25400
    # v_cut_size = v_cut_size * 25400
    # sm_surface_size = sm_surface_size * 25400
    # if soldermaskflag:           #是否执行防焊
    #     analysis_dfm.solder_mask_DFM(job, step, soldermask_list, 'erf', smdpad_ar_min, smdpad_ar_opt, coverage_sm_min, coverage_sm_opt, 
    #                                 bridge_size, False, False, False, True, 127000, intersect_width, cut_surplus_width, cut_surplus_height, 
    #                                 is_round, fan_shaved, prevent_vertical_flow_add_sm, prevent_vertical_flow_del_sm,
    #                                 drill_clearance_min , drill_clearance_opt , smd_clearance_min,
    #                                 smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, he_hong_resize_sm_in_surface, 
    #                                 gas_nodrill, gas_isdrill, v_cut_size, sm_surface_size)
    #     #输出参数
    #     f.write("solder_mask_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"soldermask_list:"+str(soldermask_list)+"\n"+ 
    #         "erf:"+'erf'+"\n"+"smdpad_sm_min:"+str(smdpad_ar_min)+"\n"+ "smdpad_sm_opt:"+str(smdpad_ar_opt)+"\n"+"coverage_sm_min:"+str(coverage_sm_min)+"\n"+ 
    #         "coverage_sm_opt:"+str(coverage_sm_opt)+"\n"+ "bridge_sm_min:"+str(bridge_size)+"\n"+"apply_to:"+str(False)+"\n"+"use_existing_mask:"+str(False) +"\n"+ 
    #         "use_shaves:"+str(False)+"\n"+"do_resize:"+str(True)+"\n"+"max_oversized_clearance:"+str(127000)+"\n"+ 
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
    # #删除防焊所有属性
    # epcam_api.modify_attributes(job, step, soldermask_list, 1, [])

