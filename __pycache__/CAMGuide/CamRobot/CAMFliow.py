import os, sys, json
import import_camflow_path
import epcam_log
import job_operation
import layer_info 
import drill_process
import analysis_dfm
import epcam
import epcam_api

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

def start_cam_flow(job, pre_step, json_str):
    times_json = {
            'paras': {
                        'times': 1
                      }                    
            }  
    times_str = json.dumps(times_json)
    epcam.set_use_times(times_str)

    epcam.init()
    data = json.loads(json_str)
    rules = json.dumps(data)

    analysis_dfm.setParameter(rules)  #设置机器人参数

    step_list = []
    layer_list = []
    step_list = job_operation.get_all_steps(job)
    layer_list = job_operation.get_all_layers(job)
    if len(step_list) and len(layer_list):
        for i in range(len(step_list)):
            for j in range(len(layer_list)):
                job_operation.load_layer(job, step_list[i], layer_list[j])
    else :
        print('no step or layer in this job')
        returndata["result"] = False
        return json.dumps(returndata)

    rob_rules = epcam_api.getParameter()
    rob_rules = json.loads(rob_rules)
    rob_rule = rob_rules['paras']['parameter']
    if rob_rule != '':
        data = json.loads(rob_rule)

    steplist = job_operation.get_all_steps(job)
    if pre_step not in  steplist:
        returndata["result"] = False
        return json.dumps(returndata)
    step = 'pcs'
    new_step_name = job_operation.copy_step(job, pre_step)     #拷贝prepare至pcs
    job_operation.rename_step(job, new_step_name, step)

    all_layer_list = []            #所有层名
    all_layer_list = layer_info.get_all_layer_name(job)
    signal_layer = []                                    #所有线路层名，用于计算通孔层名
    signal_layer = layer_info.get_signal_layer_list(job)
    board_layer_list = []            #所有层名
    board_layer_list = layer_info.get_all_board_name(job)

    # if '----------' not in all_layer_list:
        # job_operation.create_layer(job, 'xmq')
        # job_operation.rename_layer(job, 'xmq', '----------')
        
    drill_show = False
    long_resize_size = data['drill']['long_slot_resize'] * 25400
    short_resize_size = data['drill']['short_slot_resize'] * 25400
    pthdrill_size = data['drill']['pthdrill_size'] * 25400
    npthdrill_size = data['drill']['npthdrill_size'] * 25400
    viadrill_size = data['drill']['viadrill_size'] * 25400
    laserdrill_size = data['drill']['Laser_ring'] * 25400
    burieddrill_size = data['drill']['buried_ring'] * 25400
    short_aspect_ratio = data['drill']['short_aspect_ratio']
    ultrashort_slot_resize = data['drill']['ultrashort_slot_resize'] * 25400

    pth_oval_size = [data['drill']['slotpthRing_width'], data['drill']['slotpthRing_heigth']]
    npth_oval_size = [data['drill']['slotnpthRing_width'], data['drill']['slotnpthRing_heigth']]
    attribute_size = []
    attribute_size = [{"attribute": [{".drill": "plated"}], "size": pthdrill_size, "oval_size": pth_oval_size},
                        {"attribute": [{".drill": "non_plated"}], "size": npthdrill_size, "oval_size": npth_oval_size},
                        {"attribute": [{".drill": "via"}], "size": viadrill_size, "oval_size": [0, 0]},
                        {"attribute": [{".via_type": "laser"}], "size": laserdrill_size, "oval_size": [0, 0]},
                        {"attribute": [{".fiducial_name": "plated"}], "size": burieddrill_size, "oval_size": [0, 0]}]
    isEnDiameter = data['drill']['IsEnDismeter']
    drill_satellitehole = data['drill']['drill_satellitehole']    #辅助孔
    aspect_ratio = data['drill']['aspect_ratio']                  #长短槽比
    drill_shortgroove = data['drill']['drill_shortgroove']        #短槽引导孔
    oval_range = data['drill']['big_slot']                        #锣槽（槽孔）的范围
    drill_range = data['drill']['big_drill']                      #锣槽（圆孔）的范围
    drill_info_json = data['drill']['drillInfoList']
    #孔层
    if data['drill']['flag']:
        if len(drill_info_json) == 0:
            drill_process.drill_resize_to(job, step, attribute_size, drill_show, long_resize_size, short_resize_size, isEnDiameter, drill_satellitehole,
                                        aspect_ratio, drill_shortgroove, oval_range, drill_range, short_aspect_ratio, ultrashort_slot_resize)
    #加辅助孔
    drill_layer = []
    drill_layer = layer_info.get_drill_layer_name(job)
    #槽孔导孔
    drill_process.line_drill_add_pad(job, step, drill_layer, aspect_ratio, drill_shortgroove, isEnDiameter, oval_range)
    showdialog_data['request_name'] = 'Update_job'
    return json.dumps(returndata)
