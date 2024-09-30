import os, sys, json
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(__file__)) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_inner_path = os.path.dirname(os.path.dirname(__file__)) + r'\module\inner'
sys.path.append(PyRecipe_module_inner_path)
import layer_info as layer_info
import job_operation
import analysis_dfm

#print("*"*100)
#print(os.path.dirname(__file__))
module_inner_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+r"\module\inner"
#print(module_inner_path)
sys.path.append(module_inner_path)
#print("*"*100)
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
sys.path.append(PyRecipe_epcam_path)

import inner_resize as inner_resize
import inner_layercopy as inner_layercopy
from threading import Thread
from time import sleep
import queue
import epcam
import job_input
import configparser
import job_input_XY

#内层涨至最小值处理
def inner_process_resize(job, step, line_resize, surface_resize, drillpad_min_size, pthpad_dl_opt,via_dl_min, via_dl_opt, 
                         include_innerlayer, arc_angle, coverage_min, mending_copper_wire, isolated, add_tear, 
                         line2surface, min_add_tear, avoid_NPTH, avoid_VIA, teardrop_line_width_radio,
                         fill_seam, pthsize, viasize, ismergenegafteravoid, manual_sliver_check, avoid_profile_size, isolated_show,
                         signal_layer_DFM_show, avoid_features_DFM_op_show, New_signal_layer_DFM_show, sliver_DFM_op_show, teardrop_create_DFM_show,
                         avoid_PTH_size, line2laser, surface2laser, pth2laser, via2laser, laser2laser, line_to_laser_artio, 
                         surface_to_laser_artio, pth_to_laser_artio, via_to_laser_artio, blind_min, blind_opt, rules, avoid_v_cut, tdsize, 
                         buried_min, buried_opt):
    #新建参数txt
    param_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + r'\parameter'
    if not os.path.exists(param_path):
        os.makedirs(param_path)
    f = open(param_path + '\\' + job + ".txt", "w+")
    f.write("***********\n")
    f.write("   inner   \n")
    f.write("***********\n")

    # #读取配置参数
    # cf = configparser.ConfigParser()
    # config_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + r'\config.ini'
    # cf.read(config_path)
    # NFP_removal_DFM_drill_over = cf.getboolean('inner', 'NFP_removal_DFM_drill_over') #删除独立PAD
    # NFP_removal_DFM_duplicate = cf.getboolean('inner', 'NFP_removal_DFM_duplicate')
    # NFP_removal_DFM_covered = cf.getboolean('inner', 'NFP_removal_DFM_covered')
    # NFP_removal_DFM_work_on = cf.getboolean('inner', 'NFP_removal_DFM_work_on')
    # NFP_removal_DFM_pth = cf.getboolean('inner', 'NFP_removal_DFM_pth')
    # NFP_removal_DFM_pth_pressfit = cf.getboolean('inner', 'NFP_removal_DFM_pth_pressfit')
    # NFP_removal_DFM_npth = cf.getboolean('inner', 'NFP_removal_DFM_npth')
    # NFP_removal_DFM_via_laser = cf.getboolean('inner', 'NFP_removal_DFM_via_laser')
    # NFP_removal_DFM_via = cf.getboolean('inner', 'NFP_removal_DFM_via')
    # NFP_removal_DFM_via_photo = cf.getboolean('inner', 'NFP_removal_DFM_via_photo')
    # NFP_removal_DFM_remove_undrilled_pads = cf.getboolean('inner', 'NFP_removal_DFM_remove_undrilled_pads')
    # NFP_removal_DFM_apply_to = cf.getboolean('inner', 'NFP_removal_DFM_apply_to')
    # NFP_removal_DFM_remove_mark_NFP = cf.getboolean('inner', 'NFP_removal_DFM_remove_mark_NFP')

    # #设置梯形图relationship
    # line_to_surface_artio = line_to_surface_artio * 0.01
    # line_to_pth_artio = line_to_pth_artio * 0.01
    # line_to_via_artio = line_to_via_artio * 0.01
    # surface_to_pth_artio = surface_to_pth_artio * 0.01
    # surface_to_via_artio = surface_to_via_artio * 0.01
    # pth_to_via_artio = pth_to_via_artio * 0.01
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.fiducial_name=trace', line2line, 0.5)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.pattern_fill', line2surface, line_to_surface_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.pth_pad', line2pth, line_to_pth_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.via_pad', line2via, line_to_via_artio)
    # analysis_dfm.setRelationship('.fiducial_name=trace', '.laser_via_pad', laser2laser, line_to_laser_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.pattern_fill', surface2surface, 0.5)
    # analysis_dfm.setRelationship('.pattern_fill', '.pth_pad', surface2pth, surface_to_pth_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.via_pad', surface2via, surface_to_via_artio)
    # analysis_dfm.setRelationship('.pattern_fill', '.laser_via_pad', surface2laser, surface_to_laser_artio)
    # analysis_dfm.setRelationship('.pth_pad', '.pth_pad', pth2pth, 0.5)
    # analysis_dfm.setRelationship('.pth_pad', '.via_pad', pth2via, pth_to_via_artio)
    # analysis_dfm.setRelationship('.pth_pad', '.laser_via_pad', pth2laser, pth_to_laser_artio)
    # analysis_dfm.setRelationship('.via_pad', '.via_pad', via2via, 0.5)
    # analysis_dfm.setRelationship('.via_pad', '.laser_via_pad', via2via, via_to_laser_artio)
    # analysis_dfm.setRelationship('.laser_via_pad', '.laser_via_pad', laser2laser, 0.5)
    # #设置梯形图Introduction
    # analysis_dfm.setIntroduction('.fiducial_name=trace', line_resize, 0, line_resize, 0, False)
    # analysis_dfm.setIntroduction('.pattern_fill', surface_resize, 0, 0, 0, True)
    # analysis_dfm.setIntroduction('.pth_pad', 0, drillpad_min_size, 0, pthpad_dl_opt, True)
    # analysis_dfm.setIntroduction('.via_pad', 0, via_dl_min, 0, via_dl_opt, True)
    # analysis_dfm.setIntroduction('.via_pad', 0, via_dl_min, 0, via_dl_opt, True)
    # analysis_dfm.setIntroduction('.laser_via_pad', 0, blind_min, 0, blind_opt, True)


    # xxx = analysis_dfm.getRelationship()
    # #输出梯形图参数
    # f.write("Relationship:\n线到线:" + str(line2line) + "\n" + "线到铜:" + str(line2surface) + "\n" + "线到PTHPad:" + str(line2pth) + "\n" + 
    #     "线到VIAPad:" + str(line2via) + "\n" + "铜到铜:" + str(surface2surface) + "\n" + "铜到PTHPad:" + str(surface2pth) + "\n" + 
    #     "铜到VIAPad:" + str(surface2via) + "\n" + "PTHPad到PTHPad:" + str(pth2pth) + "\n" + "PTHPad到VIAPad:" + str(pth2via) + "\n" +
    #     "VIAPad到VIAPad:" + str(via2via) + "\n" + "Introduction:\n线:" + "(" + str(line_resize) + " " + str(0) + " " + str(line_resize) + " " 
    #     + str(0) + " " +  str(False) + " " + str(100) + ")" + "\n" + "铜:" + "(" + str(surface_resize) + " " + str(0) + " " + str(0)
    #     + " " + str(0) + " " +  str(True) + " " + str(0) + ")" + "\n" + "PTHPad:" + "(" + str(0) + " " + str(drillpad_min_size) 
    #     + " " + str(0) + " " + str(pthpad_dl_opt) + " " +  str(True) + " " + str(90) + ")" + "\n" + "VIAPad:" + "(" + str(0) 
    #     + " " + str(via_dl_min) + " " + str(0) + " " + str(via_dl_opt) + " " +  str(True) + " " + str(80) + ")" + "\n") 
    # f.write("**************************\n")
       
    #清空筛选
    layer_info.reset_select_filter()

    #获取内层表
    if (include_innerlayer):
        inner_list = include_innerlayer
    else:
        inner_list = layer_info.get_inner_layer_list(job) 

    if inner_list == []:
        return 0
    #备份原layer
    # for v in range(len(inner_list)):
    #     prepare_layer = job_operation.copy_layer(job, inner_list[v])
    #     pcs_layer = inner_list[v] + '-pre'
    #     job_operation.rename_layer(job, prepare_layer, pcs_layer, 'misc')

    #删除独立pad(调用优化NFP_removal_DFM)
    if isolated:
        analysis_dfm.NFP_removal_DFM(job, step, inner_list, 'erf', isolated, False, False, False, True, True, False, True, 
                    False, True, False, False, True, True)
        #输出参数
        f.write("NFP_removal_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
           "erf:"+'erf'+"\n"+"remove_island_pad:"+str(isolated)+"\n"+ "drill_over:"+str(False)+"\n"+"duplicate:"+str(False)+"\n"+ 
           "covered:"+str(False)+"\n"+ "work_on:"+str(True)+"\n"+"pth:"+str(True)+"\n"+"pth_pressfit:"+str(False)+"\n"+ 
           "npth:"+str(True)+"\n"+"via_laser:"+str(False)+"\n"+"via:"+str(True)+"\n"+"via_photo:"+str(False)+"\n"+ 
           "remove_undrilled_pads:"+str(True)+"\n"+"apply_to:"+str(True)+"\n"+"remove_mark_NFP:"+str(True)+"\n") 
        f.write("**************************\n")
        if isolated_show == True:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js)


    #内层蚀刻补偿（resize global）
    job_input.innerlayer_resize(job, step, line_resize, surface_resize, pthsize, viasize, tdsize, inner_list)
    #job_input_XY.innerlayer_resize(job, step, line_resize, surface_resize, pthsize, viasize, tdsize, inner_list, line_resize_list)

    # data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
    # js = json.dumps(data2)
    # epcam.view_cmd(js)

    #在resize之前，复制内层到新层，方便后续比对
    #inner_layercopy.inner_copy_layer(job)       

    #涨pth_pad和via_pad (调用优化signal_layer_DFM) 
    drillpad_min_size = drillpad_min_size * 25400
    pthpad_dl_opt = pthpad_dl_opt * 25400
    via_dl_min = via_dl_min * 25400
    via_dl_opt = via_dl_opt * 25400
    spacingmin = 0.5 * 25400
    laser_dl_min = blind_min * 25400
    laser_dl_opt = blind_opt * 25400
    buried_min = buried_min * 25400
    buried_opt = buried_opt * 25400
    analysis_dfm.signal_layer_DFM(job, step, inner_list, 'erf', drillpad_min_size, pthpad_dl_opt, via_dl_min, 
                                    via_dl_opt, 0, 0, spacingmin, 
                                    spacingmin, spacingmin, spacingmin, 25400, 254000, 10, 127000, 203200, 
                                    True, True, True, True, True, 
                                    False, False, False, False, False, False, False, laser_dl_min, laser_dl_opt,
                                    buried_min, buried_opt)
    #输出参数
    f.write("signal_layer_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
           "erf:"+'erf'+"\n"+"pthpad_dl_min:"+str(drillpad_min_size)+"\n"+ "pthpad_dl_opt:"+str(pthpad_dl_opt)+"\n"+"viapad_dl_min:"+str(via_dl_min)+"\n"+ 
           "viapad_dl_opt:"+str(via_dl_opt)+"\n"+ "mvia_ar_min:"+str(0)+"\n"+"mvia_ar_opt:"+str(0)+"\n"+"spacing_min:"+str(spacingmin) +"\n"+ 
           "spacing_opt:"+str(spacingmin)+"\n"+"pad_to_pad_spacing_min:"+str(spacingmin)+"\n"+"pad_to_pad_spacing_opt:"+str(spacingmin)+"\n"+"lre_range_fr:"+str(25400)+"\n"+ 
           "lre_range_to:"+str(254000)+"\n"+"reduction:"+str(10)+"\n"+"abs_min:"+str(127000)+"\n"+"drill_to_cu:"+str(203200)+"\n"+ 
           "apply_to:"+str(True)+"\n"+"pads:"+str(True)+"\n"+"smds:"+str(True)+"\n"+"drills:"+str(True)+"\n"+"padup:"+str(True)+"\n"+ 
           "shave:"+str(False)+"\n"+"paddn:"+str(False)+"\n"+"rerout:"+str(False)+"\n"+"linedn:"+str(False)+"\n"+"reshape:"+str(False)+"\n"+
           "padup_can_touch_pad"+str(False)+"\n"+"cut_pad_touch_pad:"+str(False)+"\n"+"laser_ar_min:"+str(laser_dl_min)+"\n"+"laser_ar_opt:"+str(laser_dl_opt)+"\n"
           +"buried_min:"+str(buried_min)+"\n"+"buried_opt:"+str(buried_opt)+"\n") 
    f.write("**************************\n")
    if signal_layer_DFM_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js)

    #避铜（调用优化avoid_conductor_DFM_op）
    coverage_min = coverage_min * 25400 
    #coverage_opt = coverage_opt * 25400 
    coverage_opt = 0
    use_global = True
    viadrill2Cu = avoid_VIA * 25400
    pthdrill2Cu = avoid_PTH_size * 25400
    analysis_dfm.avoid_conductor_DFM_op(job, step, inner_list, 'erf', coverage_min, coverage_opt, 0, mending_copper_wire, manual_sliver_check, use_global,
                                        viadrill2Cu, pthdrill2Cu)  
    #输出参数
    f.write("avoid_conductor_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"coverage_min:"+str(coverage_min)+"\n"+ 
           "coverage_opt:"+str(coverage_opt)+"\n"+"radius_opt:"+str(0)+"\n"+ "mending_copper_wire:"+str(mending_copper_wire)+"\n" 
           + "fast_avoid_copper:"+str(manual_sliver_check)+"\n" + "use_global:"+str(use_global)+"\n" + "viadrill2Cu:"+str(viadrill2Cu)+"\n"
           + "pthdrill2Cu:"+str(pthdrill2Cu)+"\n")
    f.write("**************************\n")
    #人工检查补细丝
    if manual_sliver_check:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":inner_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js)

    #避 NPTH孔 和 VIA独立孔 和 profile线(调用优化avoid_features_DFM_op)
    avoid_NPTH_size = avoid_NPTH * 25400
    avoid_VIA_size = avoid_VIA * 25400
    avoid_profile_size = avoid_profile_size * 25400
    avoid_v_cut = avoid_v_cut * 25400
    analysis_dfm.avoid_features_DFM_op(job, step, inner_list, 'erf', True, avoid_profile_size, True, avoid_NPTH_size, True, 0, False, 0, avoid_v_cut)   
    #输出参数
    f.write("avoid_features_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"avoid_profile:"+str(True)+"\n"+ "avoid_profile_size:"+str(avoid_profile_size)+"\n"+ 
            "avoid_npth:"+str(True)+"\n"+ "avoid_npth_size:"+str(avoid_NPTH_size)+"\n"+ "avoid_alone_drill:"+str(True)+"\n"+
            "avoid_alone_drill_size:"+str(0)+"\n"+"npth_add_solder_mask:"+str(False)+"\n"+"npth_add_solder_mask_size:"+str(0)+"\n"+
            "avoid_v_cut:"+str(avoid_v_cut)+"\n")  
    f.write("**************************\n")   
    if avoid_features_DFM_op_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js)

    #避独立孔后合并负极性
    if ismergenegafteravoid:
        layer_info.reset_select_filter()
        layer_info.select_features_by_featuretype(job, step, inner_list, 104)
        accuracy = 0.25 * 25400
        separate_to_islands = True
        size = 3.0 * 25400
        mode = 0
        layer_info.contourize(job, step, inner_list, accuracy, separate_to_islands, size, mode)
        layer_info.reset_select_filter()
        mergeneg = fill_seam * 25400
        analysis_dfm.sliver_DFM_op(job, step, inner_list, 'erf', mergeneg, mergeneg)
        #削PAD(旧版)
        # analysis_dfm.signal_layer_DFM(job, step, inner_list, 'erf', drillpad_min_size, pthpad_dl_opt, via_dl_min, 
        #                               via_dl_opt, 0, 0, spacing_min, spacing_min, spacing_min, spacing_min, 254000, 
        #                               254000, 10, 127000, 203200, True, True, True, True, False, True, False, False, False, False, False, False)

    #削PAD(调用优化New_signal_layer_DFM)
    drill_to_pad = avoid_VIA * 25400
    analysis_dfm.New_signal_layer_DFM(job, step, inner_list, 'erf', False, drill_to_pad)
    #输出参数
    f.write("New_signal_layer_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"cut_pad_touch_pad:"+str(False)+"\n") 
    f.write("**************************\n")
    if New_signal_layer_DFM_show == True:
        data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
        js = json.dumps(data2)
        epcam.view_cmd(js)
    
    #补细丝(调用优化sliver_DFM_op)
    if fill_seam != 0:
        fill_seam = fill_seam * 25400
        analysis_dfm.sliver_DFM_op(job, step, inner_list, 'erf', fill_seam, fill_seam)
        #输出参数
        f.write("sliver_DFM_op:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
            "erf:"+'erf'+"\n"+"max_width:"+str(fill_seam)+"\n"+ "max_height:"+str(fill_seam)+"\n")
        if sliver_DFM_op_show == True:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js) 

    #加泪滴（调用优化teardrop_create_DFM）
    line2surface = line2surface * 25400   #最小间距
    min_add_tear = min_add_tear * 25400
    use_arc_tear = False
    if arc_angle > 0:
        use_arc_tear = True
    #teardrop_line_width_radio(0 ~ 1)
    if add_tear:
        analysis_dfm.teardrop_create_DFM(job, step, inner_list, 'erf', 0, True, True, min_add_tear, 0, 2032000, 
                                line2surface, 279400, 0, False, True, use_arc_tear, arc_angle, False, teardrop_line_width_radio)
        #输出参数
        f.write("teardrop_create_DFM:\njob:"+job+"\n"+"step:"+step+"\n"+"inner_list:"+str(inner_list)+"\n"+ 
           "erf:"+'erf'+"\n"+"sel_type:"+str(0)+"\n"+ "drilled_pads:"+str(True)+"\n"+"undrilled_pads:"+str(True)+"\n"+ 
           "ann_ring_min:"+str(min_add_tear)+"\n"+ "drill_size_min:"+str(0)+"\n"+"drill_size_max:"+str(2032000)+"\n"+ 
           "spacing_min:"+str(line2surface)+"\n"+ "drill_spacing:"+str(279400)+"\n"+"delete_old_teardrops:"+str(0)+"\n"+ 
           "apply_to:"+str(False)+"\n"+"work_mode:"+str(True)+"\n"+ "use_arc_tear:"+str(use_arc_tear)+"\n"+"arc_angle:"+str(arc_angle)+"\n"+ 
           "bga_pads:"+str(False)+"\n" + "tear_line_width_ratio:"+str(teardrop_line_width_radio)+"\n") 
        f.write("**************************\n")
        if teardrop_create_DFM_show == True:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": inner_list[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js) 

    #动态补偿（待集成）

    f.close()

    

