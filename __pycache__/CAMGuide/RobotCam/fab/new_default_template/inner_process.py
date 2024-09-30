import os, sys, json
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_inner_path = os.path.dirname(os.path.dirname(__file__)) + r'\module\inner'
sys.path.append(PyRecipe_module_inner_path)
import layer_info
import job_operation
import analysis_dfm

module_inner_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+r"\module\inner"
sys.path.append(module_inner_path)
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

class InnerProcess():
    def __init__(self):
        pass

    def __del__(self):
        pass
    
    def get_inner_layer_list(job, data):
        include_innerlayer = []
        if 'include_innerlayer' in data['inner']:
            include_innerlayer = data['inner']['include_innerlayer']
        inner_list = []
        if (include_innerlayer):
            inner_list = include_innerlayer
        else:
            inner_list = layer_info.get_inner_layer_list(job) 

        if inner_list == []:
            return 0
        inner_list = layer_info.get_inner_layer_list(job) 
        return inner_list

    #线路优化
    def signal_layer_DFM(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        drillpad_min_size = paras['inner']['pthpad_dl_min'] * 25400
        pthpad_dl_opt = paras['inner']['pthpad_dl_opt'] * 25400
        via_dl_min = paras['inner']['viapad_dl_min'] * 25400
        via_dl_opt = paras['inner']['viapad_dl_opt'] * 25400
        laser_dl_min = paras['inner']['blind_min'] * 25400
        laser_dl_opt = paras['inner']['blind_opt'] * 25400
        buried_min = paras['inner']['buried_min'] * 25400
        buried_opt = paras['inner']['buried_opt'] * 25400
        spacingmin = 0.5 * 25400
        analysis_dfm.signal_layer_DFM(job, step, inner_list, 'erf', drillpad_min_size, pthpad_dl_opt, via_dl_min, 
                                via_dl_opt, 0, 0, spacingmin, 
                                spacingmin, spacingmin, spacingmin, 25400, 254000, 10, 127000, 203200, 
                                True, True, True, True, True, 
                                False, False, False, False, False, False, False, laser_dl_min, laser_dl_opt,
                                buried_min, buried_opt)
        return 0  
    
    #删除独立pad(调用优化NFP_removal_DFM)
    def NFP_removal_DFM(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        #isolated = paras['inner']['remove_island_pad']
        analysis_dfm.NFP_removal_DFM(job, step, inner_list, 'erf', True, False, False, False, True, True, False, True, 
                False, True, False, False, True, True)    
        return 0

    #内层蚀刻补偿（resize global）
    def innerlayer_resize(self, job, step, paras):
        line_resize = paras['inner']['line_size']                                      
        # surface_resize = paras['inner']['surface_size']
        # pthsize = paras['inner']['drillpad_pth']
        # viasize = paras['inner']['drillpad_via']
        # tdsize = paras['inner']['TDResize_inner']
        surface_resize = 0
        pthsize = 0
        viasize = 0
        tdsize = 0
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        job_input.innerlayer_resize(job, step, line_resize, surface_resize, pthsize, viasize, tdsize, inner_list)
        return 0

    
    #避铜（调用优化avoid_conductor_DFM_op）
    def avoid_conductor_DFM_op(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        coverage_min = paras['inner']['coverage_min'] * 25400 
        coverage_opt = 0
        mending_copper_wire = paras['inner']['mending_copper_wire']
        manual_sliver_check = paras['inner']['manual_sliver_work_inner']
        use_global = True
        viadrill2Cu = paras['inner']['avoid_VIA'] * 25400 
        pthdrill2Cu = paras['inner']['avoid_PTH'] * 25400 

        rules = paras
        rules = json.dumps(rules)
        analysis_dfm.setParameter(rules)  #设置机器人参数

        analysis_dfm.avoid_conductor_DFM_op(job, step, inner_list, 'erf', coverage_min, coverage_opt, 0, mending_copper_wire, manual_sliver_check, use_global,
                                    viadrill2Cu, pthdrill2Cu)
        return 0

    #避 NPTH孔 和 VIA独立孔 和 profile线(调用优化avoid_features_DFM_op)
    def avoid_features_DFM_op(self, job, step, paras, _type):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        avoid_profile_size = paras['inner']['avoid_Profile'] * 25400
        avoid_VIA_size = paras['inner']['avoid_VIA'] * 25400
        avoid_NPTH_size =  paras['inner']['avoid_NPTH']* 25400
        avoid_v_cut = paras['inner']['avoid_v_cut'] * 25400

        if _type == 'npth':
            analysis_dfm.avoid_features_DFM_op(job, step, inner_list, 'erf', False, 0, True, avoid_NPTH_size, True, 0, False, 0, avoid_v_cut)   
        else:
            analysis_dfm.avoid_features_DFM_op(job, step, inner_list, 'erf', True, avoid_profile_size, False, 0, True, 0, False, 0, 0)   

        return 0

    #避独立孔后合并负极性
    def contourize(self, job, step, inner_list, accuracy, separate_to_islands, size, mode):
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
        return 0

    #补细丝(调用优化sliver_DFM_op)
    def sliver_DFM_op(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        fill_seam = paras['inner']['fill_seam'] * 25400
        if fill_seam != 0:
            analysis_dfm.sliver_DFM_op(job, step, inner_list, 'erf', fill_seam, fill_seam)
        return 0

    #削PAD(调用优化New_signal_layer_DFM)
    def New_signal_layer_DFM(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        avoid_VIA = paras['inner']['avoid_VIA'] * 25400
        rules = paras
        rules = json.dumps(rules)
        analysis_dfm.setParameter(rules)  #设置机器人参数
        analysis_dfm.New_signal_layer_DFM(job, step, inner_list, 'erf', False, avoid_VIA)
        return 0

    #加泪滴（调用优化teardrop_create_DFM）
    def teardrop_create_DFM(self, job, step, paras):
        inner_list = InnerProcess.get_inner_layer_list(job, paras)
        add_tear = paras['inner']['add_tear']
        min_add_tear = paras['inner']['min_add_tear'] * 25400
        line2surface = paras['inner']['line_to_surface'] * 25400
        use_arc_tear = False
        arc_angle = paras['inner']['arc_angle']
        teardrop_line_width_radio = paras['inner']['teardrop_line_width_radio']

        if add_tear:
            analysis_dfm.teardrop_create_DFM(job, step, inner_list, 'erf', 0, True, True, min_add_tear, 0, 2032000, 
                        line2surface, 279400, 0, False, True, use_arc_tear, arc_angle, False, teardrop_line_width_radio)             
        return 0