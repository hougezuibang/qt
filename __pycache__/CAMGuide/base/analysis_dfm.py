import os, sys
epcam_path=os.path.dirname(os.path.realpath(__file__))+r"\epcam"
if epcam_path not in sys.path:
    sys.path.append(epcam_path)
import job_operation
import epcam_api
import json
import epcam_log

def drill_check(job, step, layers, erf, rout_distance, hole_size, extra_holes, hole_seperation, power_ground_short, missing_hole, 
                npth_to_rout, use_pth, use_npth, use_via, compensated_rout):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        drill_ranges_path = ranges_path + r'\DrillChecks\DrillRanges.json'
        epcam_api.drill_check(job, step, layers, erf, rout_distance, hole_size, extra_holes, hole_seperation, power_ground_short, missing_hole, 
                npth_to_rout, use_pth, use_npth, use_via, compensated_rout, job_operation.transform_range_data(job_operation.load_json(drill_ranges_path)))        
    except Exception as e:
        print(e)


def signal_layer_DFM(job, step, layers, erf, pth_ar_min, pth_ar_opt, via_ar_min, via_ar_opt, mvia_ar_min, mvia_ar_opt, spacing_min, spacing_opt,
				pad_to_pad_spacing_min, pad_to_pad_spacing_opt, lre_range_fr, lre_range_to, reduction, abs_min, drill_to_cu,
			    apply_to, pads, smds, drills, padup, shave, paddn, rerout, linedn, reshape, padup_can_touch_pad, cut_pad_touch_pad,
                laser_ar_min, laser_ar_opt, buried_min, buried_opt):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        signal_layer_DFM_ranges_path = ranges_path + r'\DFM_SignalLayerOpt\SignalLayerOptRanges.json'
        epcam_api.signal_layer_DFM(job, step, layers, erf, pth_ar_min, pth_ar_opt, via_ar_min, via_ar_opt, mvia_ar_min, mvia_ar_opt, spacing_min, spacing_opt,
				pad_to_pad_spacing_min, pad_to_pad_spacing_opt, lre_range_fr, lre_range_to, reduction, abs_min, drill_to_cu,
			    apply_to, pads, smds, drills, padup, shave, paddn, rerout, linedn, reshape, padup_can_touch_pad, cut_pad_touch_pad, 
                laser_ar_min, laser_ar_opt, buried_min, buried_opt,
                job_operation.transform_range_data(job_operation.load_json(signal_layer_DFM_ranges_path)))      
    except Exception as e:
        print(e)

def signal_layer_check(job, step, layers, erf, pp_spacing, drill2cu, rout2cu, sliver_min, min_pad_overlap, spacing, stubs, 
                        drill, center, rout, smd, size, bottleneck, sliver, pad_connection_check,
                        apply_to, check_missing, use_compensated_rout, sort_spacing):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        signal_layer_check_ranges_path = ranges_path + r'\SignalLayerChecks\SignalLayerRanges.json'
        ret = epcam_api.signal_layer_check(job, step, layers, erf, pp_spacing, drill2cu, rout2cu, sliver_min, min_pad_overlap, spacing, stubs, 
                        drill, center, rout, smd, size, bottleneck, sliver, pad_connection_check,
                        apply_to, check_missing, use_compensated_rout, sort_spacing, job_operation.transform_range_data(job_operation.load_json(signal_layer_check_ranges_path)))
        return ret
               
    except Exception as e:
        print(e)
        return ''

def teardrop_create_DFM(job, step, layers, erf, sel_type, drilled_pads, undrilled_pads, ann_ring_min, drill_size_min, drill_size_max, 
                        cu_spacing, drill_spacing, delete_old_teardrops, apply_to, work_mode, use_arc_tear, arc_angle, bga_pads,
                        tear_line_width_ratio):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        teardrop_create_DFM_ranges_path = ranges_path + r'\DFM_Teardrops\TeardropsRanges.json'
        epcam_api.teardrop_create_DFM(job, step, layers, erf, sel_type, drilled_pads, undrilled_pads, ann_ring_min, drill_size_min, drill_size_max, 
                                        cu_spacing, drill_spacing, delete_old_teardrops, apply_to, work_mode, use_arc_tear, arc_angle, bga_pads,
                                        tear_line_width_ratio, job_operation.transform_range_data(job_operation.load_json(teardrop_create_DFM_ranges_path)))      
    except Exception as e:
        print(e)

#避铜
def avoid_conductor_DFM_op(jobname, stepname, layernames, erf, coverage_min, coverage_opt, radius_opt, mending_copper_wire, is_fast, use_global,
                        viadrill2cu, pthdrill2cu):
    try:
        epcam_api.avoid_conductor_DFM_op(jobname, stepname, layernames, erf, coverage_min, coverage_opt, radius_opt, mending_copper_wire, is_fast, use_global, viadrill2cu, pthdrill2cu)      
    except Exception as e:
        print(e)

#去尖角
def remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round):
    try:
        epcam_api.remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round)      
    except Exception as e:
        print(e)

#防焊优化
def solder_mask_DFM(job, step, layers, erf, clearance_min, clearance_opt, coverage_min, coverage_opt, bridge_size, 
                        apply_to, use_existing_mask, use_shaves, do_resize, max_oversized_clearance, intersect_width, 
                    cut_surplus_width, cut_surplus_height, is_round, fan_shaved, prevent_vertical_flow_add_sm, 
                    prevent_vertical_flow_del_sm, 
                    drill_clearance_min , drill_clearance_opt , smd_clearance_min,
				    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, pth_fan_shave, pad_covered_clearance,
                    he_hong_resize_sm_in_surface = 0,
                    resize_gas_sm_no_drill = 0, resize_gas_sm_has_drill = 0, 
                    add_v_cut_sm_size = 0, resize_sm_surface_size = 0):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        solder_mask_DFM_ranges_path = ranges_path + r'\DFM_SolderMaskOpt\SolderMaskOptRanges.json'
        epcam_log.logger.info(solder_mask_DFM_ranges_path)
        epcam_api.solder_mask_DFM(job, step, layers, erf, clearance_min, clearance_opt, coverage_min, coverage_opt, 
                                    bridge_size, apply_to, use_existing_mask, use_shaves, do_resize, max_oversized_clearance, 
                                    intersect_width, cut_surplus_width, cut_surplus_height, is_round, fan_shaved, prevent_vertical_flow_add_sm, 
                                    prevent_vertical_flow_del_sm, 
                                    drill_clearance_min , drill_clearance_opt , smd_clearance_min,
				                    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, 
                                    he_hong_resize_sm_in_surface, 
                                    resize_gas_sm_no_drill, resize_gas_sm_has_drill, add_v_cut_sm_size, resize_sm_surface_size,
                                    pth_fan_shave, pad_covered_clearance,
                                    job_operation.transform_range_data(job_operation.load_json(solder_mask_DFM_ranges_path)))      
    except Exception as e:
        print(e)
#求一个范围内最小距离
def get_selected_feature_min_spacing(jobname, stepname, layername, search_radium):
    try:
        ret = epcam_api.get_selected_feature_min_spacing(jobname, stepname, layername, search_radium, 0)  
        data = json.loads(ret)
        return  data['paras']['min_spacing']
    except Exception as e:
        print(e)
    return ''

#求最小公差
def get_min_tolerance(jobname, stepname, layername1, layername2, selectbox):
    try:
        ret = epcam_api.get_min_tolerance(jobname, stepname, layername1, layername2, selectbox)  
        data = json.loads(ret)
        tol = []
        tol = [data['paras']['is_resize'], data['paras']['min_tol']]
        return tol
    except Exception as e:
        print(e)
    return []

#smd_bga pad 优化
def smd_bga_DFM_op(jobname, stepname, layernames, erf, smd_bga_spacing_opt, max_padup_value):
    try:
        epcam_api.smd_bga_DFM_op(jobname, stepname, layernames, erf, smd_bga_spacing_opt, max_padup_value)  
    except Exception as e:
        print(e)
    return ''

#避npth孔和profile线 优化
def avoid_features_DFM_op(jobname, stepname, layernames, erf, avoid_profile, avoid_profile_size, avoid_npth, avoid_npth_size, 
                            avoid_alone_drill, avoid_alone_drill_size, npth_add_solder_mask, npth_add_solder_mask_size, avoid_v_cut):
    try:
        epcam_api.avoid_features_DFM_op(jobname, stepname, layernames, erf, avoid_profile, avoid_profile_size, avoid_npth, avoid_npth_size, 
                                            avoid_alone_drill, avoid_alone_drill_size, npth_add_solder_mask, npth_add_solder_mask_size, avoid_v_cut)  
    except Exception as e:
        print(e)
    return ''

#sliver 优化
def sliver_DFM_op(jobname, stepname, layernames, erf, max_width, max_height):
    try:
        epcam_api.sliver_DFM_op(jobname, stepname, layernames, erf, max_width, max_height)  
    except Exception as e:
        print(e)
    return ''

#去除独立pad优化
def NFP_removal_DFM(job, step, layers, erf, isolated, drill_over, duplicate, covered, work_on, pth, pth_pressfit, npth, 
                    via_laser, via, via_photo, remove_undrilled_pads, apply_to, remove_mark_NFP):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        NFP_removal_DFM_ranges_path = ranges_path + r'\DFM_NFPRemoval\NFPRemoval.json'
        epcam_api.NFP_removal_DFM(job, step, layers, erf, isolated, drill_over, duplicate, covered, work_on, pth, pth_pressfit, npth, 
                    via_laser, via, via_photo, remove_undrilled_pads, apply_to, remove_mark_NFP, 
                    job_operation.transform_range_data(job_operation.load_json(NFP_removal_DFM_ranges_path)))   
    except Exception as e:
        print(e)
    return ''

#新的削PAD
def New_signal_layer_DFM(job, step, layers, erf, cut_pad_touch_pad, drill_to_cu):
    try:
        epcam_api.New_signal_layer_DFM(job, step, layers, erf, cut_pad_touch_pad, drill_to_cu)      
    except Exception as e:
        print(e)

#设置梯形图relationship
def setRelationship(colname, rowname, relation_value, relation_ratio):
    try:
        epcam_api.setRelationship(colname, rowname, relation_value, relation_ratio)      
    except Exception as e:
        print(e)

#获取梯形图relationship
def getRelationship(isoutter):
    try:
        return epcam_api.getRelationship(isoutter)      
    except Exception as e:
        print(e)

#设置梯形图Introduction
def setIntroduction(attributename, min_resize, min_ring, opt_resize, opt_ring, is_shave):
    try:
        epcam_api.setIntroduction(attributename, min_resize, min_ring, opt_resize, opt_ring, is_shave)      
    except Exception as e:
        print(e)

#设置机器人参数
def setParameter(rules):
    try:
        epcam_api.setParameter(rules)   
    except Exception as e:
        print(e)

#获取机器人参数
def getParameter():
    try:
        return epcam_api.getParameter()   
    except Exception as e:
        print(e)

#pth npth开窗
def npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads):
    try:
        epcam_api.npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads)      
    except Exception as e:
        print(e)

# #获取梯形图Introduction
# def getIntroduction():
#     try:
#         return epcam_api.getIntroduction()      
#     except Exception as e:
#         print(e)

#Mrc分析
def Mrc_check(job, step, layers):
    try:
        epcam_api.Mrc_check(job, step, layers)        
    except Exception as e:
        print(e)

#Prepare分析
def Prepare_check(job):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        prepare_check_ranges_path = ranges_path + r'\PrepareChecks\PrePareRanges.json'
        epcam_api.Prepare_check(job, job_operation.transform_range_data(job_operation.load_json(prepare_check_ranges_path)))        
    except Exception as e:
        print(e)
        
        
#防焊分析
def solder_mask_check(job, step, layers, erf, sm_ar, sm_coverage, sm_to_rout, sliver_min, spacing_min, bridge_min, overlap,
                        drill, silver, pads, missing, coverage, spacing, rout, clearance_connection, bridge, apply_to,
                        use_compensated_rout, min_sliver_len, dist2sliver_ratio, apply_range, classify_pad_ar):
    try:
        ranges_path=os.path.dirname(__file__) + r'\rangesconfig'
        solder_mask_check_ranges_path = ranges_path + r'\SolderMaskChecks\SolderMaskRanges.json'
        epcam_api.solder_mask_check(job, step, layers, erf, sm_ar, sm_coverage, sm_to_rout, sliver_min, spacing_min, bridge_min, overlap,
                                    drill, silver, pads, missing, coverage, spacing, rout, clearance_connection, bridge, apply_to,
                                    use_compensated_rout, min_sliver_len, dist2sliver_ratio, apply_range, classify_pad_ar,
                                    job_operation.transform_range_data(job_operation.load_json(solder_mask_check_ranges_path)))      
    except Exception as e:
        print(e)

        
        

