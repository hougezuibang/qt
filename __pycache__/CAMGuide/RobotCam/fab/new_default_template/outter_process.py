import os, sys, json
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
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

class OutterProcess():
    def __init__(self):
        pass
    def __del__(self):
        pass

    def get_outter_list(job, paras):
        include_outterlayer = []
        if 'include_outterlayer' in paras['outter']:
            include_outterlayer = paras['outter']['include_outterlayer']
        outter_list = []
        if len(include_outterlayer) > 0:
            outter_list = include_outterlayer
        else:  
            outter_list = layer_info.get_outter_list(job)
        return outter_list

    # def get_soldermask_list(job):
    #     try:
    #         soldermask = layer_info.get_soldermask_list(job)
    #     return 0

    #外层蚀刻补偿（resize_global）
    def outterlayer_resize(self, job, step, paras):
        smdbga_less = paras['outter']['smdbga_less'] * 25400
        smdbga_compensate = paras['outter']['smdbga_compensate'] * 25400
        line_resize = paras['outter']['line_size']                             
        surface_resize = paras['outter']['surface_size'] 
        smd_resize = paras['outter']['smd_size']
        bga_resize = paras['outter']['bga_size'] 
        mark_resize = paras['outter']['mark_size']
        pthsize = paras['outter']['drillpad_pth']
        viasize = paras['outter']['drillpad_via']
        tdsize = paras['outter']['TDResize_outter']
        
        job_input.outterlayer_resize(job, step, smdbga_less, smdbga_compensate, line_resize, surface_resize, smd_resize, bga_resize, mark_resize, pthsize, viasize, tdsize)
        return 0

    #涨PTH_Pad和VIA_Pad（调用优化signal_layer_DFM）
    def signal_layer_DFM(self, job, step, paras):
        outter_list = OutterProcess.get_outter_list(job, paras)
        pthpad_dl_min = paras['outter']['pthpad_dl_min'] * 25400  
        pth_dl_opt = paras['outter']['pthpad_dl_opt'] * 25400  
        via_dl_min = paras['outter']['viapad_dl_min'] * 25400  
        via_dl_opt = paras['outter']['viapad_dl_opt'] * 25400  
        spacingmin = 0.5 * 25400  
        laser_dl_min = paras['outter']['blind_min'] * 25400
        laser_dl_opt = paras['outter']['blind_opt'] * 25400 

        analysis_dfm.signal_layer_DFM(job, step, outter_list, 'erf', pthpad_dl_min, pth_dl_opt, via_dl_min, via_dl_opt, 
                            0, 0, spacingmin, spacingmin, spacingmin, spacingmin, 25400, 254000, 10, 127000, 203200, 
                            True, True, True, True, True, False, False, False, False, False, False, False, laser_dl_min, laser_dl_opt, 0, 0)
        return 0

    #避铜(调用优化avoid_conductor_DFM_op)
    def avoid_conductor_DFM_op(self, job, step, paras):
        outter_list = OutterProcess.get_outter_list(job, paras)
        coverage_min = paras['outter']['coverage_min'] * 25400
        coverage_opt = 0
        mending_copper_wire = paras['outter']['mending_copper_wire']
        manual_sliver_check = paras['outter']['manual_sliver_work_outter']
        use_global = True

        
        rules = paras
        rules = json.dumps(rules)
        analysis_dfm.setParameter(rules)  #设置机器人参数

        analysis_dfm.avoid_conductor_DFM_op(job, step, outter_list, 'erf', coverage_min, coverage_opt, 0, mending_copper_wire, manual_sliver_check, use_global, 0, 0) 

        return 0
    
    #避NPTH孔和profile线（调用优化avoid_features_DFM_op）（外层做NPTH开窗）（外层无VIA独立孔）
    def avoid_features_DFM_op(self, job, step, paras, _type):  
        outter_list = OutterProcess.get_outter_list(job, paras)
        avoid_profile_size = paras['outter']['avoid_Profile'] * 25400
        avoid_NPTH = paras['outter']['avoid_NPTH'] * 25400
        sm_NPTH_size1 = paras['outter']['NPTH'] * 25400
        avoid_v_cut = paras['outter']['avoid_v_cut'] * 25400
        if _type == 'npth':    
            analysis_dfm.avoid_features_DFM_op(job, step, outter_list, 'erf', False, 0, True, avoid_NPTH, False, 0, True, sm_NPTH_size1, avoid_v_cut)
        else:
            analysis_dfm.avoid_features_DFM_op(job, step, outter_list, 'erf', True, avoid_profile_size, False, 0, False, 0, False, 0, 0)
        return 0
    #削PAD(调用优化New_signal_layer_DFM)
    def New_signal_layer_DFM(self, job, step, paras):
        outter_list = OutterProcess.get_outter_list(job, paras)
        rules = paras
        rules = json.dumps(rules)
        analysis_dfm.setParameter(rules)  #设置机器人参数
        analysis_dfm.New_signal_layer_DFM(job, step, outter_list, 'erf', False, 0)
        return 0
    #补细丝
    def sliver_DFM_op(self, job, step, paras):
        outter_list = OutterProcess.get_outter_list(job, paras)
        fill_seam = paras['outter']['fill_seam'] * 25400
        #补细丝（调用优化sliver_DFM_op）
        if fill_seam != 0:
            analysis_dfm.sliver_DFM_op(job, step, outter_list, 'erf', fill_seam, fill_seam)    #2.5
        return 0

    #加泪滴（调用优化teardrop_create_DFM）（BGA可选是否添加泪滴）
    def teardrop_create_DFM(self, job, step, paras):                      
        outter_list = OutterProcess.get_outter_list(job, paras)
        min_add_tear = paras['outter']['min_add_tear'] * 25400
        line2surface = paras['outter']['line_to_surface'] * 25400
        use_arc_tear = False
        arc_angle = paras['outter']['arc_angle']
        if arc_angle > 0:
            use_arc_tear = True
        bga_pads = paras['outter']['bga_pads'] * 25400
        teardrop_line_width_radio = paras['outter']['teardrop_line_width_radio']
        add_tear = paras['outter']['add_tear']
        #teardrop_line_width_radio(0 ~ 1)
        if add_tear:
            analysis_dfm.teardrop_create_DFM(job, step, outter_list, 'erf', 0, True, True, min_add_tear, 0, 2032000, 
                                    line2surface, 279400, 0, False, True, use_arc_tear, arc_angle, bga_pads, teardrop_line_width_radio)
        return 0
    #pth npth开窗
    def npth_and_pth_prepare_op(self, job, step, paras):
        sm_clearance = paras['outter']['PTH'] * 25400 * 0.5
        sm_np_clearance = paras['outter']['NPTH'] * 25400 * 0.5
        add_sm_pads = True
        add_signal_pads = False

        analysis_dfm.npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads)

        return 0