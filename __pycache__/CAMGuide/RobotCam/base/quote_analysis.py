import os,sys
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import layer_info

def get_min_line_width(job,step,layer):
    """
    获取最小线宽，需要先load layer
    return         最小线宽，若没有正极性line则返回-1
    """
    try:
        isfirst = True
        min_line_width = -1
        ret = epcam_api.get_all_features_report(job,step,layer)
        data = json.loads(ret)
        lines_param = data['paras']['lines_list']
        if lines_param is not None:
                for line in lines_param:
                    if line['polarity'] == 'POS':
                        if isfirst3:
                            min_line_width = float(re.split('[a-zA-z]+',line['symbolname'])[1])
                            isfirst3 = False
                        line_width = float(re.split('[a-zA-z]+',line['symbolname'])[1])
                        if line_width<min_line_width:
                            min_line_width = line_width
        return min_line_width
    except Exception as e:
        print(e)

def get_min_pad_diam(job,step,layer):
    """
    获取最小pad直径，需要先load layer
    return         最小pad直径，若没有正极性line则返回-1
    """
    try:
        isfirst = True
        min_pad_diam = -1
        ret = epcam_api.get_all_features_report(job,step,layer)
        data = json.loads(ret)
        pads_param = data['paras']['lines_list']
        if pads_param is not None:
                for pad in pads_param:
                    if pad['polarity'] == 'POS':
                        if isfirst:
                            min_pad_diam = float(re.split('[a-zA-z]+',pad['symbolname'])[1])
                            isfirst = False
                        pad_diam = float(re.split('[a-zA-z]+',pad['symbolname'])[1])
                        if pad_diam<min_pad_diam:
                            min_pad_diam = pad_diam
        return min_pad_diam
        pass
    except Exception as e:
        print(e)

def get_gold_finger_info(job,step):
    """
    获取gold_finger信息
    return         面积，数量，X方向最大长度，Y方向最大长度
    """
    try:
        signal_layer = layer_info.get_signal_layers_list(job)
        layer_info.reset_select_filter()
        epcam_api.filter_set_attribute(1, [{".gold_finger": ""}])
        epcam_api.select_features_by_filter(job, step, [signal_layer[0],signal_layer[-1]])
        gold_finger_areas_list = []
        gold_finger_num_list = []
        gold_finger_maxX_list = []
        gold_finger_maxY_list = []
        for i in [0,-1]:
            #gold_finger_area
            area_ret = epcam_api.get_selected_feature_areas(job, step, signal_layer[i])
            area_data = json.loads(area_ret)
            area = area_data['result']
            gold_finger_areas_list.append(area)

            rpt_ret = epcam_api.get_selected_features_report(job,step,signal_layer[i])
            rpt_data = json.loads(rpt_ret)
            pad_list = rpt_data['paras']['pad_list']
            #gold_finger_box,gold_finger_num
            num,maxX,maxY = 0,0,0
            if pad_list is not None:
                for temp in pad_list:
                    num += temp['count']
                    if temp['symbol_height'] > maxY:
                        maxY = temp['symbol_height']
                    if temp['symbol_width'] > maxX:
                        maxX = temp['symbol_width']
            gold_finger_num_list.append(num)
            gold_finger_maxX_list.append(maxX)
            gold_finger_maxY_list.append(maxY)  
        return gold_finger_areas_list,gold_finger_num_list,gold_finger_maxX_list,gold_finger_maxY_list
    except Exception as e:
        print(e)

def get_bga_info(job,step):    
    """
    获取bga信息
    return         最小直径，bga面积总和
    """
    try:
        signal_layer = layer_info.get_signal_layers_list(job)
        layer_info.reset_select_filter()
        epcam_api.filter_set_attribute(1, [{".bga": ""}])
        epcam_api.select_features_by_filter(job, step, [signal_layer[0],signal_layer[-1]])
        isfirst = True
        min_bga_list = []
        bga_areas_list = []
        for i in [0,-1]:
            min_bga_diam = -1
            #bga_diam
            bga_ret = epcam_api.get_selected_features_report(job, step, signal_layer[i])
            data = json.loads(bga_ret)
            bga_list = data['paras']['pad_list']
            #bga_area
            bga_area_ret = epcam_api.get_selected_feature_areas(job, step, signal_layer[i])
            area_data = json.loads(bga_area_ret)
            bga_area = area_data['result']
            bga_areas_list.append(bga_area)
            if bga_list is not None:
                for bga in bga_list:
                    bga_diam = float(re.split('[a-zA-z]+',bga['symbolname'])[1])
                    if isfirst:
                        min_bga_diam = bga_diam
                        isfirst = False
                    if bga_diam<min_bga_diam:
                        min_bga_diam = bga_diam
            min_bga_list.append(min_bga_diam)
        return min_bga_list,bga_areas_list
    except Exception as e:
        print(e)

#获取钻程信息
#[0层名 1起始层名 2结束层名   3起始层row  4结束层row  5孔类型(through/bury/blind) 6孔信息[0刀类型1导通类型2总数3孔径信息[0[孔径大小,孔数量]]] ]-3signal_row_list  -2layer_name_row -1layer_row_name
def get_drl_program_info(job,step):
    try:
        # def sort_drl_prog(layer,signal_row_list,matrix_data):

        matrix_ret = epcam_api.get_matrix(job)
        matrix_data = json.loads(matrix_ret)
        drls_info,signal_row_list = [],[]
        layer_name_row = {}
        layer_row_name = {}
        for layer in matrix_data['paras']['info']:
            temp1 = {layer['name']:layer['row']}
            temp2 = {layer['row']:layer['name']}
            layer_name_row.update(temp1)
            layer_row_name.update(temp2)
            if layer['context'] == 'board' and layer['type'] == 'drill':
                drl_info = [layer['name'],layer['start_name'],layer['end_name']]
                drls_info.append(drl_info)
            if(layer['context'] == 'board' and (layer['type'] == 'signal' or layer['type'] == 'power_ground')):
                signal_row_list.append(layer['row'])
        
        for drl1 in drls_info:
            up,down = -1,-1
            if (drl1[1] == '' or layer_name_row[drl1[1]] <= min(signal_row_list)):
                start_row = min(signal_row_list)
                drl1.append(start_row)
                up = 0
            elif (layer_name_row[drl1[1]] >= max(signal_row_list)):
                start_row = max(signal_row_list)
                drl1.append(start_row)
                up = 0
            else :
                drl1.append(layer_name_row[drl1[1]])
                up = 1
            if (drl1[2] == '' or layer_name_row[drl1[2]] >= max(signal_row_list)):
                end_row = max(signal_row_list)
                drl1.append(end_row)
                down = 0
            elif (layer_name_row[drl1[2]] <= min(signal_row_list)):
                end_row = min(signal_row_list)
                drl1.append(end_row)
                down = 0
            else :
                drl1.append(layer_name_row[drl1[2]])
                down = 1
            if (up == 0 and down == 0):
                drl1.append('through')
            elif ((up == 0 and down == 1) or(up == 1 and down == 0)):
                drl1.append('blind')
            elif (up == 1 and down == 1):
                drl1.append('bury')
            else:
                drl1.append('error')
            laser_pth = ['laser','pth',0,[]]
            slot_pth = ['nc_slot','pth',0,[]]
            slot_npth = ['nc_slot','npth',0,[]]
            round_pth = ['nc_round','pth',0,[]]
            round_npth = ['nc_round','npth',0,[]]
            drl1.append([laser_pth,slot_pth,slot_npth,round_pth,round_npth])
        #排序
        drls_info.sort(key = lambda x: (x[3],-x[4]))

        for drl2 in drls_info:
            #laser
            epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
            epcam_api.clear_selected_features(job,step,drl2[0])
            epcam_api.filter_set_attribute(0 , [{".drill": "via"},{".via_type":"laser"}])
            epcam_api.select_features_by_filter(job, step, [drl2[0]])
            laser_ret = epcam_api.get_selected_features_report(job,step,drl2[0])
            laser_data = json.loads(laser_ret)
            laser_num = 0
            if laser_data['paras']['pad_list'] is not None:
                for pad in laser_data['paras']['pad_list']:
                    laser_num+= pad['count']
                    drl2[6][0][3].append([pad['symbolname'],pad['count']])
                drl2[6][0][2]+=laser_num
            #pth
            epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
            epcam_api.clear_selected_features(job,step,drl2[0])
            epcam_api.filter_set_attribute(0 , [{".drill": "plated"}])
            epcam_api.select_features_by_filter(job, step, [drl2[0]])
            epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
            epcam_api.filter_set_attribute(0 , [{".drill": "via"}])
            epcam_api.select_features_by_filter(job, step, [drl2[0]])
            epcam_api.filter_set_attribute(0 , [{".drill": "via"},{".via_type":"laser"}])
            aaa = epcam_api.unselect_features(job, step, drl2[0])
            pth_ret = epcam_api.get_selected_features_report(job,step,drl2[0])
            pth_data = json.loads(pth_ret)
            slot_pth_num = 0
            round_pth_num = 0
            if pth_data['paras']['lines_list'] is not None:
                for line in pth_data['paras']['lines_list']:
                    slot_pth_num += line['count']
                    drl2[6][1][3].append([line['symbolname'],line['count']])
                drl2[6][1][2] += slot_pth_num
            if pth_data['paras']['pad_list'] is not None:
                for pad in pth_data['paras']['pad_list']:
                    if 'oval' in pad['symbolname']:
                        slot_pth_num += pad['count']
                        drl2[6][1][3].append([pad['symbolname'],pad['count']])
                    else:
                        round_pth_num += pad['count']
                        drl2[6][3][3].append([pad['symbolname'],pad['count']])
                drl2[6][1][2]+= slot_pth_num
                drl2[6][3][2] += round_pth_num
            #npth
            epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
            epcam_api.clear_selected_features(job,step,drl2[0])
            epcam_api.filter_set_attribute(0 , [{".drill": "non_plated"}])
            epcam_api.select_features_by_filter(job, step, [drl2[0]])
            npth_ret = epcam_api.get_selected_features_report(job,step,drl2[0])
            npth_data = json.loads(npth_ret)
            slot_npth_num = 0
            round_npth_num = 0
            if npth_data['paras']['lines_list'] is not None:
                for line in npth_data['paras']['lines_list']:
                    slot_pth_num += line['count']
                    drl2[6][2][3].append([line['symbolname'],line['count']] )
                drl2[6][2][2] += slot_pth_num
            if npth_data['paras']['pad_list'] is not None:
                for pad in npth_data['paras']['pad_list']:
                    if 'oval' in pad['symbolname']:
                        slot_pth_num += pad['count']
                        drl2[6][2][3].append([pad['symbolname'],pad['count']])
                    else:
                        round_pth_num += pad['count']
                        drl2[6][4][3].append([pad['symbolname'],pad['count']])
                drl2[6][2][2]+= slot_pth_num
                drl2[6][4][2] += round_pth_num
        #merge
        unrepeat = []
        repeat = []
        for ii in range(len(drls_info)):
            temp_list = [drls_info[ii][3],drls_info[ii][4]]
            if temp_list not in unrepeat:
                unrepeat.append(temp_list)
            else:
                repeat.append(ii)
                merger_index = ii-1
                while(merger_index in repeat):
                    merger_index = merger_index-1
                for i_info in range(5):
                    drls_info[merger_index][6][i_info][2]+=drls_info[ii][6][i_info][2]
                    for i1 in range(len(drls_info[ii][6][i_info][3])):
                        if drls_info[merger_index][6][i_info][3] == []:
                            drls_info[merger_index][6][i_info][3].append(drls_info[ii][6][i_info][3][i1])
                        else:
                            for i2 in range(len(drls_info[merger_index][6][i_info][3])):
                                if drls_info[ii][6][i_info][3][i1][0] == drls_info[merger_index][6][i_info][3][i2][0]:
                                    drls_info[merger_index][6][i_info][3][i2][1]+=drls_info[ii][6][i_info][3][i1][1]
                                if (drls_info[ii][6][i_info][3][i1][0] != drls_info[merger_index][6][i_info][3][i2][0]) and (i2 == len(drls_info[merger_index][6][i_info][3])-1):
                                    drls_info[merger_index][6][i_info][3].append(drls_info[ii][6][i_info][3][i1])
        return_list = []
        for i3 in range(len(drls_info)):
            if i3 not in repeat:
                return_list.append(drls_info[i3])
        return_list.append(signal_row_list)
        return_list.append(layer_name_row)
        return_list.append(layer_row_name)
        return return_list
    except Exception as e:
        print(e)

def get_silk_surface(job):
    """
    获取丝印层面
    return         [顶层丝印层数，底层丝印层数]
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        signal = True
        info = data['paras']['info']
        silk = 0
        silk_list = []
        if info == '':
            print('get matrix false')
            return silk_list
        for layer in info:
            if layer['context'] == 'board':
                if signal:
                    if layer['type'] == 'signal':
                        signal = False
                        silk_list.append(silk)
                        silk = 0
                    elif layer['type'] == 'silk_screen':
                        silk +=1
                elif layer['type'] == 'silk_screen':
                    silk += 1
        silk_list.append(silk)
        return silk_list
    except Exception as e:
        print(e)

def get_min_silk_linewidth(job,step,silklayers):
    try:
        min_silk_linewidth = 0
        min_silk_linewidth_list = []
        if silklayers ==[]:
            return min_silk_linewidth_list
        for silk in silklayers:
            isfirst3 = True
            job_operation.load_layer(job, step, silk)
            ret2 = epcam_api.get_all_features_report(job,step,silk)
            data2 = json.loads(ret2)
            slik_lines_param = data2['paras']['lines_list']
            slik_arcs_param = data2['paras']['arcs_list']
            slik_texts_param = data2['paras']['texts_list']
            layer_min_silk_width = -1
            if slik_lines_param is not None:
                for line in slik_lines_param:
                    if line['polarity'] == 'POS':
                        if isfirst3:
                            layer_min_silk_width = float(re.split('[a-zA-z]+',line['symbolname'])[1]) 
                            min_silk_width = layer_min_silk_width
                            isfirst3 = False
                        line_width = float(re.split('[a-zA-z]+',line['symbolname'])[1])
                        if line_width<layer_min_silk_width:
                            layer_min_silk_width = line_width
            if slik_arcs_param is not None:
                for arc in slik_arcs_param:
                    if arc['polarity'] == 'POS':
                        if isfirst3:
                            layer_min_silk_width = float(re.split('[a-zA-z]+',arc['symbolname'])[1]) 
                            min_silk_width = layer_min_silk_width
                            isfirst3 = False
                        line_width = float(re.split('[a-zA-z]+',line['symbolname'])[1])
                        if line_width<layer_min_silk_width:
                            layer_min_silk_width = line_width
            if slik_texts_param is not None:
                epcam_api.set_select_param(0x50, False, [], 0, 0, -1, -1, [], 0, True)
                epcam_api.select_features_by_filter(job, step, [silk])
                textret = epcam_api.get_selected_feature_infos(job,step,silk)
                textdata = json.loads(textret)

            if layer_min_silk_width>0:
                # min_silk_line_width_list.append(layer_min_silk_width*25400)
                min_silk_linewidth_list.append(layer_min_silk_width)
            else :
                min_silk_linewidth_list.append(layer_min_silk_width)
        
        return min_silk_linewidth_list
        pass
    except Exception as e:
        print (e)

def apart_drl(drl_row_list_bef,signal_row_list):
    try:
        after = []
        for drl_row in drl_row_list_bef:
            _first = drl_row[0]
            _second = drl_row[1]
            comp = 1
            if _second < _first:
                _first = drl_row[1]
                _second = drl_row[0]
            for i in range(len(signal_row_list)):
                if abs(signal_row_list.index(_first) - signal_row_list.index(_second)) >= 1:            #判断不相邻
                    if (len(signal_row_list)&1) != 0:                 #判断奇数
                        if [_first,signal_row_list[signal_row_list.index(_first)+1],False] not in after:
                            after.append([_first,signal_row_list[signal_row_list.index(_first)+1],False])
                            _first = signal_row_list[signal_row_list.index(_first)+1]
                    else:                                                       #偶数
                        not_mir = True
                        for _after in after :                              
                            if (len(signal_row_list)-2) == (signal_row_list.index(_after[0]) + signal_row_list.index(_first)):        #判断是否镜像
                                if ([_first,signal_row_list[signal_row_list.index(_first)+1],True] not in after) and\
                                    ([_first,signal_row_list[signal_row_list.index(_first)+1],False] not in after):
                                    after.append([_first,signal_row_list[signal_row_list.index(_first)+1],True])
                                    _first = signal_row_list[signal_row_list.index(_first)+1]
                                    not_mir = False
                                    break
                            else:
                                continue
                        if not_mir:
                            second = signal_row_list[signal_row_list.index(_first)+comp]
                            if ([_first,second,False] not in after) and \
                                ([_first,second,True] not in after):
                                after.append([_first,second,False])
                                _first = second
                else:
                    break
        return after
    except Exception as e:
        print(e)

def get_hdi_level(job,step,drls_info):
    try:
        hdi_level = 0
        hdi_level_list_bef = []
        for drl in drls_info:
            if drl == drls_info[-3]:
                break
            if drl[6][0][2] > 0:
                hdi_level_list_bef.append([drl[3],drl[4],False])
        hdi_level_list_aft = apart_drl(hdi_level_list_bef,drls_info[-3])
        for hdi in hdi_level_list_aft:
            if False == hdi[2]:
                hdi_level += 1
        return hdi_level,hdi_level_list_aft 
    except Exception as e:
        print(e)














