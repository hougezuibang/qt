import os, sys, json
PyRecipe_base_epcam_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base\epcam'
PyRecipe_module_drill_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\module\drill'
sys.path.append(PyRecipe_base_epcam_path)
sys.path.append(PyRecipe_module_drill_path)
import epcam as epcam
import epcam_api
import drill_classify as drill_classify
import drill_resize as drill_resize
import layer_info as layer_info
import job_operation as job_operation
import analysis_dfm
import feature_resize
from bisect import bisect_left, insort
import math

# def drill_resize_delta(job, step, attributes, size):
#     #获取孔层
#     layer_name = layer_info.get_drill_layer_name(job)
#     new_layer = job_operation.copy_layer(job, layer_name)
#     layers = [new_layer]
#     job_operation.open_layer(job, step, new_layer)
#     #对孔层分类
#     symbols = []
#     drill_classify.classify(job, step, layers, 0, attributes, symbols)
#     #根据指定大小涨孔
#     drill_resize.resize_specify(job, step, 0, size)
    #layer_info.clear_select(job, step, new_layer)


# def drill_resize_to(job, step, attribute_size):
#     #获取刀径表
#     diameter_list = get_drill_diameter_list(0.1, 6.5, 0.05, [])    #单位：毫米
#     #获取孔层
#     drill_layer = []
#     drill_layer = layer_info.get_drill_layer_name(job)
#     if len(drill_layer):
#        for i in range(0, len(drill_layer)): 
#             layer_name = drill_layer[i]
#             job_operation.open_layer(job, step, layer_name)
#             new_layer = job_operation.copy_layer(job, layer_name)
#             layer_info.change_layer_context(job, new_layer, 'misc')
#             #layers = [layer_name]
#             layers = [layer_name]
#             job_operation.open_layer(job, step, layer_name)
#             #获取所有孔的大小
#             #drill_list = layer_info.get_all_features_symbolname(job, step, layer_name)
#             #drill_list = layer_info.get_all_drill_symbolname(job, step, layer_name)
#             #分属性操作
#             if len(attribute_size):
#                 for k in range(0, len(attribute_size)):
#                     #for j in range(0, len(drill_list)):       
#                     #symbols = [drill_list[j][0]]
#                     #对孔层分类
#                     attribute_name = attribute_size[k]['attribute']
#                     drill_classify.classify(job, step, layers, 0, attribute_name)#, symbols)
#                     #根据指定大小涨孔
#                     _size = attribute_size[k]['size']# - drill_list[j][1s
#                     #获取每一个选中的孔的坐标和symbolname
#                     pad_list = layer_info.get_selected_pad_point(job, step, layer_name)
#                     if len(pad_list):
#                         for m in range(len(pad_list)):
#                             #获得每个孔的坐标和大小
#                             coord_x = pad_list[m][0]
#                             coord_y = pad_list[m][1]
#                             drill_name = pad_list[m][2]
#                             drill_size = layer_info.get_drillsize_by_symbolname(drill_name)  #已做过单位换算
#                             #分属性考虑刀径
#                             if attribute_name == [{".drill": "via"}]:
#                                 #via先和传入值比较大于这个值就不管，小于这个值先做补偿
#                                 via_size = 0.5 * 25400
#                                 if drill_size < via_size:
#                                     good_size = drill_size + _size
#                                 else:
#                                     good_size = drill_size
#                             else:
#                                 #pth和npth要先补偿，用补偿后的值
#                                 good_size = drill_size + _size
#                                 #刀径表单位是毫米 先转换单位
#                             real_size = get_drill_diameter_size(diameter_list, good_size / 1000000, attribute_name)
#                             real_delta = real_size * 1000000 - drill_size
#                             #drill_resize.resize_specify(job, step, layer_name, 0, _size) 
#                             layer_info.clear_select(job, step, layer_name)
#                             #坐标的box
#                             select_poligon = [[coord_x - 1, coord_y - 1],
#                                 [coord_x - 1, coord_y + 1], [coord_x + 1, coord_y + 1],
#                                 [coord_x + 1, coord_y - 1], [coord_x - 1, coord_y - 1]]
#                             layer_info.select_feature(job, step, layer_name, select_poligon, {}, 0, False)
#                             drill_resize.resize_specify(job, step, layer_name, 0, real_delta)
#                             layer_info.clear_select(job, step, layer_name)
#                     layer_info.reset_select_filter()
#                     layer_info.clear_select(job, step, layer_name)
#     data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":'l1'}
#     js = json.dumps(data2)
#     epcam.view_cmd(js)
#     #孔分析
#     #analysis_dfm.drill_check(job, step, drill_layer, 'erf', 5080000, True, True, True, True, True, 
#     #                            True, True, False, True, 3)

def get_diameter_list(isEnDiameter):
    if isEnDiameter:
        diameter_list = [3.9, 5.9, 7.9, 9.8, 11.8, 13.8, 15.7, 17.7, 19.7, 21.7, 23.6, 25.6, 27.6, 29.5, 31.5, 33.5, 35.4, 37.4, 
                        39.4, 41.3, 43.3, 45.3, 47.2, 49.2, 51.2, 53.1, 55.1, 57.1, 59.1, 61.0, 63.0, 65.0, 66.9, 68.9, 70.9, 72.8,
                        74.8, 76.8, 78.7, 80.7, 82.7, 84.6, 86.6, 88.6, 90.6, 92.5, 94.5, 96.5, 98.4, 100.4, 102.4, 104.3, 106.3, 
                        108.3, 110.2, 112.2, 114.2, 116.1, 118.1, 120.1, 122.0, 124.0, 126.0, 128.0, 129.9, 131.9, 133.9, 135.8, 
                        137.8, 139.8, 141.7, 143.7, 145.7, 147.6, 149.6, 151.6, 153.5, 155.5, 157.5, 159.4, 161.4, 163.4, 165.4, 
                        167.3, 169.3, 171.2, 173.2, 175.2, 177.2, 179.1, 181.1, 183.1, 185.0, 187.0, 189.0, 190.9, 192.9, 194.9,
                        196.9, 198.8, 200.8, 202.8, 204.7, 206.7, 208.7, 210.6, 212.6, 214.5, 216.5, 218.5, 220.5, 222.4, 224.4, 
                        226.4, 228.3, 230.3, 232.3, 234.2, 236.2, 238.2, 240.2, 242.1, 244.1, 246.1, 248.0, 250.0, 252.0, 253.9, 
                        255.9]    #单位：mil  
    else:
        diameter_list = get_drill_diameter_list(100000, 6500000, 50000, [])    #单位：纳米  
    return diameter_list

def drill_resize_to(job, step, attribute_size, drill_show, long_resize_size, short_resize_size, isEnDiameter, drill_satellitehole, 
                    aspect_ratio, drill_shortgroove, oval_range, drill_range, short_aspect_ratio, ultrashort_slot_resize):
    if short_aspect_ratio >= 2:
        short_aspect_ratio = 1.5
    #max_value = max_value * 25400
    #获取刀径表  
    diameter_list = get_diameter_list(isEnDiameter)
    # if isEnDiameter:
    #     diameter_list = [3.9, 5.9, 7.9, 9.8, 11.8, 13.8, 15.7, 17.7, 19.7, 21.7, 23.6, 25.6, 27.6, 29.5, 31.5, 33.5, 35.4, 37.4, 
    #                     39.4, 41.3, 43.3, 45.3, 47.2, 49.2, 51.2, 53.1, 55.1, 57.1, 59.1, 61.0, 63.0, 65.0, 66.9, 68.9, 70.9, 72.8,
    #                     74.8, 76.8, 78.7, 80.7, 82.7, 84.6, 86.6, 88.6, 90.6, 92.5, 94.5, 96.5, 98.4, 100.4, 102.4, 104.3, 106.3, 
    #                     108.3, 110.2, 112.2, 114.2, 116.1, 118.1, 120.1, 122.0, 124.0, 126.0, 128.0, 129.9, 131.9, 133.9, 135.8, 
    #                     137.8, 139.8, 141.7, 143.7, 145.7, 147.6, 149.6, 151.6, 153.5, 155.5, 157.5, 159.4, 161.4, 163.4, 165.4, 
    #                     167.3, 169.3, 171.2, 173.2, 175.2, 177.2, 179.1, 181.1, 183.1, 185.0, 187.0, 189.0, 190.9, 192.9, 194.9,
    #                     196.9, 198.8, 200.8, 202.8, 204.7, 206.7, 208.7, 210.6, 212.6, 214.5, 216.5, 218.5, 220.5, 222.4, 224.4, 
    #                     226.4, 228.3, 230.3, 232.3, 234.2, 236.2, 238.2, 240.2, 242.1, 244.1, 246.1, 248.0, 250.0, 252.0, 253.9, 
    #                     255.9]    #单位：mil  
    # else:
    #     diameter_list = get_drill_diameter_list(100000, 6500000, 50000, [])    #单位：纳米  
    #获取孔层
    drill_layer = []
    drill_layer = layer_info.get_drill_layer_name(job)
    #epcam_api.line2pad_new(job, step, drill_layer)      #线转pad后属性丢失
    if len(drill_layer):
        for i in range(0, len(drill_layer)): 
            _layer_name = drill_layer[i]
            job_operation.open_layer(job, step, _layer_name)
            # new_layer = job_operation.copy_layer(job, _layer_name)
            # layer_info.change_layer_context(job, new_layer, 'misc')
            #临时层
            tem_layer = _layer_name + '-temp'
            job_operation.create_layer(job, tem_layer)
            final_layer = _layer_name + '-final'
            job_operation.create_layer(job, final_layer)
            noatr_layer = _layer_name + '-noatr'
            job_operation.create_layer(job, noatr_layer)
            #对无属性的孔单独操作
            all_drills = []               #存放所有孔的信息
            noatr_ids = []                #存放没属性的孔的id
            layer_info.reset_select_filter()
            layer_info.reverse_select(job, step, _layer_name)     #先选中所有孔，获取信息得到没有属性的孔的id
            all_drills = layer_info.get_features_infos(job, step, _layer_name)
            for _drill in all_drills:
                if _drill[11] == []:
                    noatr_ids.append(_drill[10])
            epcam_api.clear_selected_features(job, step, _layer_name)
            if noatr_ids != []:
                epcam_api.select_feature_by_id(job, step, _layer_name, noatr_ids)
                layer_info.sel_move_other(job, step, [_layer_name], job, step, noatr_layer, False, 0, 0, 0, 0, 0, 0, 0)
                epcam_api.clear_selected_features(job, step, _layer_name)
            #移动到最终层
            layer_info.reset_select_filter()
            drill_classify.classify(job, step, [_layer_name], 0, [], 65)#, symbols)
            layer_info.sel_move_other(job, step, [_layer_name], job, step, final_layer, False, 0, 0, 0, 0, 0, 0, 0)
            #layers = [layer_name]
            layer_name = final_layer
            layers = [final_layer]
            job_operation.open_layer(job, step, layer_name)
            #分属性操作
            if len(attribute_size):
                for k in range(0, len(attribute_size)):
                    #对孔层分类
                    attribute_name = attribute_size[k]['attribute']
                    drill_classify.classify(job, step, layers, 0, attribute_name, 65)#, symbols)
                    #将盲孔和埋孔取消选中
                    if attribute_name == [{".drill": "plated"}]:
                        layer_info.reset_select_filter()
                        layer_info.set_attribute_filter(0, [{".fiducial_name": "plated"}])
                        layer_info.unselect_features(job, step, layer_name)
                        layer_info.reset_select_filter()
                        layer_info.set_attribute_filter(0, [{".drill": "plated"}])
                    if attribute_name == [{".drill": "via"}]:
                        layer_info.reset_select_filter()
                        layer_info.set_attribute_filter(0, [{".via_type": "laser"}])
                        layer_info.unselect_features(job, step, layer_name)
                        layer_info.set_attribute_filter(0, [{".drill": "via"}])
                    #根据指定大小涨孔
                    _size = attribute_size[k]['size']# - drill_list[j][1s
                    #槽孔的resize信息
                    oval_size = attribute_size[k]['oval_size']
                    # #特殊大小的孔
                    # _special_list = attribute_size[k]['special']
                    # #特殊大小的槽孔
                    # oval_special_list = attribute_size[k]['oval_special']
                    #获取每一个选中的孔的坐标和symbolname
                    pad_list = layer_info.get_selected_pad_point(job, step, layer_name)
                    #存放symbolname和对应的需要补偿的size
                    drill_name_list = []
                    # #存放特殊symbolname
                    # special_name_list = []
                    #存放所有原始的symbolname
                    orig_symbols = []
                    #存放所有槽孔的symbolname
                    oval_name_list = []
                    #存放所有usersymbol
                    drill_user_symbols = []
                    #获取该job内所有的usersymbol
                    user_symbol_list = layer_info.get_usersymbol_list(job)
                    if len(pad_list):
                        for x in range(len(pad_list)):
                            #获得每个孔symbolname
                            drill_name = pad_list[x][2]
                            #user symbol简单resize一下 拷回原层
                            if drill_name in user_symbol_list and drill_name not in drill_user_symbols:
                                drill_user_symbols.append(drill_name)
                            #如果symbolname在orig_symbols中出现，则跳过
                            if drill_name in orig_symbols:
                                continue
                            if drill_name[0:4] == 'oval' and drill_name not in user_symbol_list:
                                if drill_name not in oval_name_list:
                                    oval_name_list.append(drill_name)
                                continue
                            orig_symbols.append(drill_name)
                    # if len(_special_list):
                    #     for v in range(len(_special_list)):
                    #         _special_name_size = _special_list[v]
                    #         #如果传入的special symbolname不存在
                    #         if _special_name_size[0] not in orig_symbols:
                    #             continue
                    #         if _special_name_size in drill_name_list:
                    #             continue
                    #         if _special_name_size[0][0:4] == 'oval':
                    #             continue
                    #         drill_name_list.append([_special_name_size[0], _special_name_size[1] * 25400])
                    #         special_name_list.append(_special_name_size[0])
                    if len(orig_symbols):
                        for m in range(len(orig_symbols)):
                            _name = orig_symbols[m]
                            #如果symbolname在special_name_list中出现，则跳过
                            # if _name in special_name_list:
                            #     continue
                            if [_name, _size] in drill_name_list:
                                 continue
                            if _name[0:4] == 'oval':
                                continue
                            if _name in user_symbol_list:
                                continue
                            drill_name_list.append([_name, _size])
                    for _user in drill_user_symbols:
                        layer_info.reset_select_filter()
                        layer_info.clear_select(job, step, layer_name)
                        layer_info.set_include_symbol_filter(_user)
                        layer_info.select_features_by_filter(job, step, [layer_name])
                        layer_info.sel_move_other(job, step, [final_layer], job, step, tem_layer, False, 0, 0, 0, 0, 0, 0, 0)
                        drill_resize.resize_specify(job, step, tem_layer, 1, _size)
                        layer_info.sel_move_other(job, step, [tem_layer], job, step, _layer_name, False, 0, 0, 0, 0, 0, 0, 0)
                    layer_info.reset_select_filter()
                    layer_info.clear_select(job, step, layer_name)
                    if len(drill_name_list):
                        for t in range(len(drill_name_list)):
                            #镭射孔不考虑刀径表
                            if attribute_name == [{".via_type": "laser"}]:
                                layer_info.sel_move_other(job, step, [final_layer], job, step, tem_layer, False, 0, 0, 0, 0, 0, 0, 0)
                                drill_resize.resize_specify(job, step, tem_layer, 1, drill_name_list[t][1])
                                layer_info.sel_move_other(job, step, [tem_layer], job, step, _layer_name, False, 0, 0, 0, 0, 0, 0, 0)
                                #drill_resize.resize_specify(job, step, layer_name, 0, drill_name_list[t][1])
                                continue
                            #获取孔径
                            drill_size = layer_info.get_drillsize_by_symbolname(drill_name_list[t][0])  #已做过单位换算
                            if attribute_name == [{".drill": "non_plated"}]: 
                                layer_info.reset_select_filter()
                                layer_info.clear_select(job, step, layer_name) 
                                if drill_range > 0:
                                    if drill_size > drill_range * 25400:
                                        layer_info.set_featuretype_filter(65)
                                        layer_info.set_attribute_filter(0, attribute_name)
                                        select_name = drill_name_list[t][0]
                                        layer_info.set_include_symbol_filter([select_name])
                                        epcam_api.select_features_by_filter(job, step, [layer_name])
                                                                                                            #锣槽不补偿
                                        layer_info.sel_move_other(job, step, [final_layer], job, step, _layer_name, False, 0, 0, 0, 0, 0, 0, 0)
                                        continue
                            #原孔径加上补偿值后与刀径比较
                            good_size = drill_size + drill_name_list[t][1]
                            # #与特殊值去比较，若是大于特殊值则删除原孔用一圈小孔代替
                            # if good_size > max_value:
                            #     replace_drill_by_hole(job, step, layer_name, drill_name_list[t][0], good_size, hole_size, angle, attribute_name)
                            #     continue
                            real_size = 0
                            if isEnDiameter:
                                #刀径表单位是mil 先转换单位
                                good_size =  good_size / 25400
                                good_size = round(good_size, 2)
                                real_size = get_drill_diameter_size(diameter_list, good_size, attribute_name)
                                real_delta = real_size * 25400 - drill_size
                            else:
                                #刀径表单位是纳米 不用转换单位
                                real_size = get_drill_diameter_size(diameter_list, good_size, attribute_name)
                                real_delta = real_size - drill_size
                                real_size = round(real_size / 25400, 3)
                            #drill_resize.resize_specify(job, step, layer_name, 0, _size) 
                            layer_info.clear_select(job, step, layer_name)
                            layer_info.reset_select_filter()
                            #按symbolname筛选
                            layer_info.set_featuretype_filter(65)
                            layer_info.set_attribute_filter(0, attribute_name)
                            select_name = drill_name_list[t][0]
                            layer_info.set_include_symbol_filter([select_name])
                            epcam_api.select_features_by_filter(job, step, [layer_name])

                            layer_info.sel_move_other(job, step, [final_layer], job, step, tem_layer, False, 0, 0, 0, 0, 0, 0, 0)
                            drill_resize.resize_specify(job, step, tem_layer, 1, real_delta)
                            #判断孔是否需要添加小孔
                            if len(drill_satellitehole):
                                for h in range(len(drill_satellitehole)):
                                    if real_size >= drill_satellitehole[h]['drill_min'] and real_size <= drill_satellitehole[h]['drill_max']:                      
                                        #切刀径后的值来进行判断
                                        replace_drill_by_hole(job, step, tem_layer, real_size, drill_satellitehole[h], attribute_name)
                            layer_info.sel_move_other(job, step, [tem_layer], job, step, _layer_name, False, 0, 0, 0, 0, 0, 0, 0)
                            layer_info.reset_select_filter()
                            layer_info.clear_select(job, step, tem_layer)
                            layer_info.clear_select(job, step, _layer_name)
                            #drill_resize.resize_specify(job, step, layer_name, 0, real_delta)
                            layer_info.clear_select(job, step, layer_name)                   
                    #处理槽孔
                    add_new_oval_drill(job, step, layer_name, oval_name_list, attribute_name, oval_size, diameter_list, long_resize_size, short_resize_size, _layer_name, isEnDiameter, oval_range, short_aspect_ratio, ultrashort_slot_resize)
                    add_new_line_drill(job, step, _layer_name, attribute_name, oval_size, _size, diameter_list, long_resize_size, short_resize_size, isEnDiameter, oval_range, short_aspect_ratio, ultrashort_slot_resize)
                    layer_info.reset_select_filter()
                    layer_info.sel_move_other(job, step, [noatr_layer], job, step, _layer_name, False, 0, 0, 0, 0, 0, 0, 0)
                    layer_info.clear_select(job, step, layer_name)
                    layer_info.sel_break(job, step, [_layer_name], 1)
            job_operation.delete_layer(job, noatr_layer)
            job_operation.delete_layer(job, tem_layer)
            job_operation.delete_layer(job, final_layer)   #删除临时层
        if drill_show:
            data2 = {"cmd":"show_layer", "job":job, "step": step, "layer": drill_layer[0]}
            js = json.dumps(data2)
            epcam.view_cmd(js)

#获取贴近刀径表的值
def get_drill_diameter_size(size_list, drill_size, attribute):
    if len(size_list):
        if drill_size <= size_list[0]:
            return size_list[0]
        elif drill_size > size_list[len(size_list) - 1]:
            return drill_size
        else:
            index = bisect_left(size_list, drill_size)
            if index > 0:
                left_delta = drill_size - size_list[index - 1]
                right_delta = size_list[index] - drill_size 
                if left_delta < right_delta:
                    return size_list[index - 1]
                elif left_delta > right_delta:
                    return size_list[index]
                else:
                    if attribute == [{".drill": "via"}]:
                        return size_list[index - 1]
                    else:
                        return size_list[index]
    return -1

#获取刀径表  
def get_drill_diameter_list(min_size, max_size, tol, special_list):   
    #min_size：刀径最小值 max_size：刀径最大值 tol：刀径公差 special_list：额外新添刀径(数组)
    list_size = (max_size - min_size) / tol + 1
    diameter_list = []
    for i in range(int(list_size)):
        diameter = round(min_size + tol * i, 2)
        diameter_list.append(diameter)
    if len(special_list) > 0:
        for k in range(len(special_list)):
            insort(diameter_list, special_list[k])    
    return diameter_list

#获取孔层的最小刀径孔
def get_min_drill(job, step, layer):
    layer_info.set_featuretype_filter(127)
    layer_info.select_features_by_filter(job, step, [layer])
    info_list = layer_info.get_features_infos(job, step, layer)    #获取所有孔的信息
    layer_info.reset_select_filter()
    layer_info.clear_select(job, step, layer)  #清除选中并对每一个line进行选中判断  
    drill_name_list = []     #存放符合标准的symbolname
    for _info in info_list:   
        if len(_info):
            drill_name = _info[2]
            if drill_name in drill_name_list:
                continue
            drill_name_list.append(drill_name)
    if drill_name_list == []:
        return 0
    size_list = []
    for _name in drill_name_list:
        _size = layer_info.get_drillsize_by_symbolname(_name)   #通过symbolname获取线宽
        size_list.append(_size)
    if size_list == []:
        return 0
    size_list.sort()
    return size_list[0]

#线属性槽孔添加导引孔
def line_drill_add_pad(job, step, drill_list, aspect_ratio, drill_shortgroove, isEnDiameter, oval_range):
    aspect_ratio = aspect_ratio    #长槽短槽比
    _offset = drill_shortgroove['offset']          #偏移量
    min_space = drill_shortgroove['guide_hole_spacing']
    min_guide_hole = 300000
    if 'min_hole' in drill_shortgroove:
        min_guide_hole = drill_shortgroove['min_hole']   #导引孔小于孔层最小孔时，添加该值的孔
        min_guide_hole = min_guide_hole * 25400
    ratio = aspect_ratio  
    if ratio == 0:
        return
    _offset = _offset * 25400
    min_space = min_space * 25400
    line_list = []       #存放所有line的信息
    if drill_shortgroove['middle']:
        min_space = 0
    if len(drill_list):
        for _drill in drill_list:
            layer = _drill
            layer_info.reset_select_filter()
            layer_info.set_featuretype_filter(66)
            layer_info.select_features_by_filter(job, step, [layer])
            #获取每一个选中的线的坐标和symbolname和基本属性
            line_list = layer_info.get_features_infos(job, step, layer)
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, layer)
            if len(line_list):
                for line_info in line_list:
                    line_name = line_info[2]
                    line_attribute = line_info[11]
                    line_XS = line_info[6] * 25400000
                    line_YS = line_info[7] * 25400000
                    line_XE = line_info[8] * 25400000
                    line_YE = line_info[9] * 25400000  #line起始点坐标
                    line_x = (line_XS + line_XE) / 2
                    line_y = (line_YS + line_YE) / 2  #line的坐标
                    line_len2 = math.pow((line_YE - line_YS), 2) + math.pow((line_XE - line_XS), 2)     
                    final_dis = round(math.sqrt(line_len2), 2)     #线两端圆心间的距离        
                    line_width = layer_info.get_drillsize_by_symbolname(line_name)   #通过symbolname获取线宽
                    if line_attribute == [{".drill": "non_plated"}]:
                        if line_width > oval_range * 25400 and oval_range > 0:
                            continue
                    line_len = final_dis + round(line_width, 2)        #线长为起始点长度+线宽  
                    if final_dis == 0:
                        continue
                    offset_final_x = (line_len / 2) * (line_XE - line_x) / (final_dis / 2)     
                    offset_final_y = (line_len / 2) * (line_YE - line_y) / (final_dis / 2)    #线端点相对于线中心的偏移
                    final_XS = line_x + offset_final_x
                    final_YS = line_y + offset_final_y
                    final_XE = line_x - offset_final_x
                    final_YE = line_y - offset_final_y
                    long_slot_size = line_len
                    short_slot_size = line_width
                    if long_slot_size > short_slot_size * 2:
                        continue
                    hole_size = round(line_len / ratio, 2) - _offset    #计算孔径
                    if line_len <= min_space + 2 * _offset:
                        continue                       
                    max_hole = line_len / 2 - min_space / 2 - _offset     #计算最大孔径
                    if max_hole > line_width:
                        max_hole = line_width
                    if hole_size >= max_hole:
                        hole_size = max_hole
                    
                    diameter_list = get_diameter_list(isEnDiameter)       #获取刀径表
                    max_size = hole_size
                    real_size = 0
                    if isEnDiameter:
                        #刀径表单位是mil 先转换单位
                        hole_size =  hole_size / 25400
                        hole_size = round(hole_size, 2)
                        hole_size = get_drill_diameter_size(diameter_list, hole_size, line_attribute)
                        hole_size = hole_size * 25400
                        if hole_size > max_size:
                            hole_size = round(hole_size / 25400, 2)
                            hole_size = hole_size - 2
                            hole_size = get_drill_diameter_size(diameter_list, hole_size, line_attribute)
                            hole_size = hole_size * 25400
                    else:
                        #刀径表单位是纳米 不用转换单位
                        hole_size = get_drill_diameter_size(diameter_list, hole_size, line_attribute)   
                        if hole_size > max_size:
                            hole_size = hole_size - 50000
                    min_size = get_min_drill(job, step, layer)            #如果孔径小于该层的最小孔径则不添加小孔
                    if hole_size < min_size:
                        if min_guide_hole == 0:
                            continue
                        hole_size = min_guide_hole
                    #hole_dis = min_space / 2 + hole_size / 2               #计算小孔距离线中心的距离
                    hole_dis = line_len / 2 - _offset - hole_size / 2
                    if line_len == 0:
                        continue
                    offset_x = (final_XE - line_x) * hole_dis / (line_len / 2)    #小孔圆心横坐标相对于线中心在正方向的偏移
                    offset_y = (final_YE - line_y) * hole_dis / (line_len / 2)    #小孔圆心纵坐标相对于线中心在正方向的偏移
                    hole_x1 = line_x + offset_x
                    hole_y1 = line_y + offset_y             #相对于圆心正方向上的小孔坐标
                    hole_x2 = line_x - offset_x
                    hole_y2 = line_y - offset_y             #相对于圆心负方向上的小孔坐标
                    hole_size = round(hole_size / 25400, 3)   #切换英制symbolname
                    hole_symbol_nme = 'r' + str(hole_size)
                    epcam_api.add_pad(job, step, [], layer, hole_symbol_nme, hole_x1, hole_y1, 1, 0, 0, line_attribute)  #添加小孔
                    epcam_api.add_pad(job, step, [], layer, hole_symbol_nme, hole_x2, hole_y2, 1, 0, 0, line_attribute)

#添加去毛刺孔
def add_rm_glitch_drill(job, step, expend_radius, end_number): #expend_radius 单边增加长度; end_number 作区分的引孔尾数。单位均为mm
    drill_list = layer_info.get_drill_layer_name(job)
    if len(drill_list):
        for drill_ in drill_list:
            layer = drill_
            layer_info.reset_select_filter()
            layer_info.set_featuretype_filter(127)
            layer_info.select_features_by_filter(job, step, [layer])
            pad_list = []
            pad_list = layer_info.get_features_infos(job, step, layer)
            if len(pad_list):
                for j in range(len(pad_list)):
                    pad_x = pad_list[j][0]
                    pad_y = pad_list[j][1]
                    pad_syb = pad_list[j][2]
                    pad_polarity = pad_list[j][3]
                    pad_angle = pad_list[j][4]
                    pad_mirror = pad_list[j][5]
                    polarity = 0
                    #判断polarity
                    if pad_polarity == 'POS':
                        polarity = 1
                    else:
                        polarity = 0
                    orient = pad_angle
                    layer_info.clear_select(job, step, layer)
                    layer_info.reset_select_filter()
                    pad_r = layer_info.get_drillsize_by_symbolname(pad_syb) * 0.5
                    select_poligon = [[pad_x - pad_r , pad_y - pad_r], [pad_x - pad_r, pad_y + pad_r],
                                     [pad_x + pad_r, pad_y + pad_r], [pad_x + pad_r, pad_y - pad_r],
                                     [pad_x - pad_r, pad_x - pad_r]]
                    layer_info.set_selection(True, True, True, True, True, False)
                    layer_info.select_feature(job, step, layer, select_poligon, {}, 1, False) 
                    features = []
                    features = layer_info.get_features_infos(job, step, layer)
                    if len(features) == 2:
                        attributes = features[0][11]
                        c1_x = features[0][0]
                        c1_y = features[0][1]
                        c1_name = features[0][2]
                        r1 = 0.5 * layer_info.get_drillsize_by_symbolname(c1_name)  # r1 半径

                        c2_x = features[1][0]
                        c2_y = features[1][1]
                        c2_name = features[1][2]
                        r2 = 0.5 * layer_info.get_drillsize_by_symbolname(c2_name)  # r2 半径

                        l = round(math.sqrt((c2_x - c1_x) * (c2_x - c1_x)  + (c2_y - c1_y) * (c2_y - c1_y)), 2)
                        l1 = (l*l - r2*r2 + r1*r1) * 0.5/l
                        c_x = l1/l * (c2_x - c1_x) + c1_x  # 计算预钻孔圆心
                        c_y = l1/l * (c2_y - c1_y) + c1_y
                        d = (math.sqrt(r1*r1 - l1*l1) + expend_radius*1000000)* 2 + end_number*1000000       
                        hole_symbol_nme = 'r' + str(round(d/25400, 3))
                        epcam_api.add_pad(job, step, [], drill_, hole_symbol_nme, c_x, c_y, 1, 0, 0, attributes)  #添加小孔

#扩孔预钻孔
def pre_add_drill_before_expand(job, step, need_pre_add_drill, hole_size, pre_add_size): # bool need_pre_add_drill; hole_size 扩孔预钻最小值; 
    drill_list = layer_info.get_drill_layer_name(job)                                    # pre_add_size 大孔减去此值为预钻孔径
    if len(drill_list):                                                                  # 单位mm
        for drill_ in drill_list:
            layer = drill_
            layer_info.reset_select_filter()
            layer_info.set_featuretype_filter(127)
            layer_info.select_features_by_filter(job, step, [layer])
            pad_list = []
            pad_list = layer_info.get_features_infos(job, step, layer)
            if len(pad_list):
                for j in range(len(pad_list)):
                    attributes = pad_list[j][11]
                    pad_x = pad_list[j][0]
                    pad_y = pad_list[j][1]
                    name = pad_list[j][2]
                    d = layer_info.get_drillsize_by_symbolname(name)
                    if need_pre_add_drill == True and d >= hole_size * 1000000:           
                        hole_symbol_nme ='r' + str(round((d - pre_add_size*1000000)/25400, 3))
                        epcam_api.add_pad(job, step, [], drill_, hole_symbol_nme, pad_x, pad_y, 1, 0, 0, attributes)  #添加小孔


#短槽添加导引孔
def short_slot_add_pad(job, step, drill_list, aspect_ratio, drill_shortgroove):
    aspect_ratio = aspect_ratio    #长槽短槽比
    _offset = drill_shortgroove['offset']          #偏移量
    hole_size =  0
    min_space = drill_shortgroove['guide_hole_spacing']
    ratio = drill_shortgroove['ratio']
    hole_symbol_name = 'r' + str(hole_size)
    _offset = _offset * 25400
    hole_size = hole_size * 25400
    min_space = min_space * 25400
    shrot_list = []       #存放所有line的信息
    if drill_shortgroove['middle']:
        min_space = 0
    if len(drill_list):
        for _drill in drill_list:
            layer = _drill 
            layer_info.reset_select_filter()
            layer_info.set_featuretype_filter(65)
            layer_info.select_features_by_filter(job, step, [layer])
            #获取每一个选中的线的坐标和symbolname和基本属性
            pad_list = []
            pad_list = layer_info.get_features_infos(job, step, layer)
            oval_list = []
            if len(pad_list):
                for _pad in pad_list:
                    if _pad['symbolname'][0:4] == 'oval':
                        oval_list.append(_pad)                #将oval信息存入列表
            if len(oval_list):
                for oval_info in oval_list:
                    line_name = oval_info['symbolname']
                    line_x = oval_info['X']
                    line_y = oval_info['Y']            #oval的坐标
                    width_height = layer_info.get_oval_width_and_height(line_name)
                if len(width_height):
                    oval_width = width_height[0]       #symbolname英制
                    oval_height = width_height[1]
                    if oval_width >= oval_height:
                        long_slot_size = oval_width
                        short_slot_size = oval_height
                    else:
                        short_slot_size = oval_width
                        long_slot_size = oval_height
                    if long_slot_size < long_slot_size * 2:
                        continue
                    line_len = long_slot_size * 25400         #线长为起始点长度+线宽   
                    line_width = short_slot_size * 25400  

                    if line_len <= min_space + 2 * _offset:
                        return
                    max_hole = line_len / 2 - min_space / 2 - _offset     #计算最大孔径
                    if max_hole > line_width:
                        max_hole = line_width
                    hole_dis = min_space / 2 + max_hole / 2               #计算小孔距离线中心的距离
                    offset_x = (line_XE - line_x) * hole_dis / (line_len / 2)    #小孔圆心横坐标相对于线中心在正方向的偏移
                    offset_y = (line_YE - line_y) * hole_dis / (line_len / 2)    #小孔圆心纵坐标相对于线中心在正方向的偏移
                    hole_x1 = line_x + offset_x
                    hole_y1 = line_y + offset_y             #相对于圆心正方向上的小孔坐标
                    hole_x2 = line_x - offset_x
                    hole_y2 = line_y - offset_y             #相对于圆心负方向上的小孔坐标
                    epcam_api.add_pad(job, step, [], layer, hole_symbol_nme, hole_x1, hole_y1, 1, 0, 0, attributes)  #添加小孔
                    epcam_api.add_pad(job, step, [], layer, hole_symbol_nme, hole_x2, hole_y2, 1, 0, 0, attributes)

#删除槽孔重新添加
# def add_new_oval_drill(job, step, layer, oval_name_list, attributes, oval_size, oval_special_list, diameter_list):  
def add_new_oval_drill(job, step, layer, oval_name_list, attributes, oval_size, diameter_list, long_resize_size, short_resize_size,
                        orig_drill_layer, isEnDiameter, oval_range, short_aspect_ratio, ultrashort_slot_resize):  
    #存放symbolname和resize信息
    drill_name_list = [] 
    # #存放特殊尺寸symbolname
    # special_name_list = []
    # #遍历特殊尺寸列表
    # if len(oval_special_list):
    #     for v in range(len(oval_special_list)):
    #         _special_name_size = oval_special_list[v]
    #         #如果传入的special symbolname不存在
    #         if _special_name_size[0] not in oval_name_list:
    #             continue
    #         if _special_name_size in drill_name_list:
    #             continue
    #         if _special_name_size[0][0:4] != 'oval':
    #             continue
    #         drill_name_list.append([_special_name_size[0], _special_name_size[1], _special_name_size[2]])
    #         special_name_list.append(_special_name_size[0])
    #将普通oval的resize信息存入drill_name_list
    if len(oval_name_list):
        for n in range(len(oval_name_list)):
            _name = oval_name_list[n]
            # #如果symbolname在special_name_list中出现，则跳过
            # if _name in special_name_list:
            #     continue
            if [_name, oval_size[0], oval_size[1]] in drill_name_list:
                continue
            if _name[0:4] != 'oval':
                continue
            drill_name_list.append([_name, oval_size[0], oval_size[1]])
    #获取所有选中的槽孔信息
    if len(drill_name_list):
        for i in range(len(drill_name_list)):
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, layer)
            #按symbolname筛选
            layer_info.set_include_symbol_filter([drill_name_list[i][0]])
            layer_info.set_attribute_filter(0, attributes)
            layer_info.select_features_by_filter(job, step, [layer])
            #获取每一个选中的槽孔的坐标和symbolname和基本属性
            oval_list = layer_info.get_features_infos(job, step, layer)
            #获取该symbolname槽孔的宽高
            width_height = layer_info.get_oval_width_and_height(drill_name_list[i][0])   #英制单位
            if len(width_height):
                oval_width = width_height[0]   #symbolname英制
                oval_height = width_height[1]
            if attributes == [{".drill": "non_plated"}]:
                if oval_range > 0:
                    if oval_width > oval_range:
                        layer_info.reset_select_filter()
                        layer_info.clear_select(job, step, layer)
                        layer_info.set_featuretype_filter(65)
                        layer_info.set_attribute_filter(0, attributes)
                        select_name = drill_name_list[i][0]
                        layer_info.set_include_symbol_filter([select_name])
                        epcam_api.select_features_by_filter(job, step, [layer])                                                                                           
                        layer_info.sel_move_other(job, step, [layer], job, step, orig_drill_layer, False, 0, 0, 0, 0, 0, 0, 0)
                        continue
            #删除原槽孔
            epcam_api.sel_delete(job, step, [layer])
            #原孔径加上补偿值后与刀径比较
            good_size_width = oval_width + drill_name_list[i][1]
            good_size_height = oval_height + drill_name_list[i][2]
            resize_width =  False
            if good_size_width < good_size_height:
                good_size = good_size_width
                resize_width = True
            else:
                good_size = good_size_height
                resize_width = False           
            if isEnDiameter:
                #刀径表单位是mil 不用转换单位
                real_size = get_drill_diameter_size(diameter_list, good_size, attributes)
            else:
                #刀径表单位是纳米 先转换单位
                real_size = get_drill_diameter_size(diameter_list, good_size * 25400, attributes)
                real_size = round(real_size / 25400, 2)
            if resize_width:
                new_width_height = [real_size, round(good_size_height, 2)]
            else:
                new_width_height = [round(good_size_width, 2), real_size]
            #一个一个添加槽孔
            if len(oval_list):
                for j in range(len(oval_list)):
                    oval_x = oval_list[j][0]
                    oval_y = oval_list[j][1]
                    oval_polarity = oval_list[j][3]
                    oval_angle = oval_list[j][4]
                    oval_mirror = oval_list[j][5]
                    polarity = 0
                    #判断polarity
                    if oval_polarity == 'POS':
                        polarity = 1
                    else:
                        polarity = 0
                    orient = oval_angle
                    layer_info.clear_select(job, step, layer)
                    # layer_info.add_oval_pad(job, step, layer, new_width_height[0], new_width_height[1], oval_x, oval_y, polarity, 0, orient, attributes)
                    # select_poligon = [[oval_x - 1, oval_y - 1], [oval_x - 1, oval_y + 1],
                    #                  [oval_x + 1, oval_y + 1], [oval_x + 1, oval_y - 1],
                    #                  [oval_x - 1, oval_y - 1]]
                    # layer_info.select_feature(job, step, layer, select_poligon, {}, 0, False)
                    #添加槽孔
                    layer_info.add_oval_pad(job, step, orig_drill_layer, new_width_height[0], new_width_height[1], oval_x, oval_y, polarity, 0, orient, attributes)
                    select_poligon = [[oval_x - 1, oval_y - 1], [oval_x - 1, oval_y + 1],
                                     [oval_x + 1, oval_y + 1], [oval_x + 1, oval_y - 1],
                                     [oval_x - 1, oval_y - 1]]
                    layer_info.select_feature(job, step, orig_drill_layer, select_poligon, {}, 0, False)

                    #分长短槽操作
                    oval_long_size = 0
                    oval_short_size = 0
                    if new_width_height[0] >= new_width_height[1]:
                        oval_long_size = new_width_height[0]
                        oval_short_size = new_width_height[1]
                    else:
                        oval_long_size = new_width_height[1]
                        oval_short_size = new_width_height[0]
                    #长短槽添加尾数
                    if oval_long_size > oval_short_size * 2:
                        feature_resize.resize_global(job, step, [orig_drill_layer], 0, long_resize_size)
                    else:
                        if oval_long_size < oval_short_size * short_aspect_ratio:
                            feature_resize.resize_global(job, step, [orig_drill_layer], 0, ultrashort_slot_resize)
                        else:
                            feature_resize.resize_global(job, step, [orig_drill_layer], 0, short_resize_size)
                    layer_info.clear_select(job, step, orig_drill_layer)
        layer_info.clear_select(job, step, orig_drill_layer)
        layer_info.clear_select(job, step, layer)

#删除原孔用一圈小孔替代
#def replace_drill_by_hole(job, step, layer, drill_symbol_name, drill_size, hole_size, angle, attributes):  
def replace_drill_by_hole(job, step, layer, drill_size, drill_satellitehole, attributes): 
    #参数赋值
    drill_size_str = "%.3f"%drill_size
    drill_symbol_name = 'r' + drill_size_str
    drill_size = drill_size * 25400
    hole_size = drill_satellitehole['drill_diam']     #小孔直径（英制）
    hole_size = round(hole_size, 3)
    hole_size_str = "%.3f"%hole_size
    hole_symbol_nme = 'r' + hole_size_str
    hole_num = drill_satellitehole['drill_num']       #小孔数量
    if hole_num == 0:
        return
    angle = round(360 / hole_num, 2)                  #小孔间的角度
    hole_dis = drill_satellitehole['drill_dis']       #小孔距大孔边的距离（英制）
    hole_size = hole_size * 25400 
    hole_dis = hole_dis * 25400 
    #存放该drill_symbol_name下所有原孔的坐标
    drill_point_list = []
    #通过原孔的symbolname来获取所有该symbolname下所有孔的坐标
    layer_info.clear_select(job, step, layer)
    #layer_info.set_include_symbol_filter([])
    layer_info.select_features_by_featuretype(job, step, [layer], 65)
    layer_info.set_include_symbol_filter([drill_symbol_name])
    layer_info.select_features_by_filter(job, step, [layer])

    drill_point_list = layer_info.get_selected_pad_point(job, step, layer)
    #选中原孔，删除
    if len(drill_point_list):
        for t in range(len(drill_point_list)):
            drill_x = drill_point_list[t][0]
            drill_y = drill_point_list[t][1]
            #坐标的box
            select_poligon = [[drill_x - 1, drill_y - 1],
                            [drill_x - 1, drill_y + 1], [drill_x + 1, drill_y + 1],
                            [drill_x + 1, drill_y - 1], [drill_x - 1, drill_y - 1]]
            layer_info.clear_select(job, step, layer)
            #layer_info.select_feature(job, step, layer, select_poligon, {}, 0, False)
            #删除原孔
            #epcam_api.sel_delete(job, step, [layer])
            #小孔圆心所在圆弧的半径
            _r = drill_size / 2 - hole_size / 2 - hole_dis
            if _r <= 0:
                return
            #创建数组，存放小孔圆心
            hole_location = []
            for i in range(hole_num):
                # hole_x = drill_x + _r * math.sin(angle * i)
                # hole_y = drill_y + _r * math.cos(angle * i)
                #hole_x = (drill_x - drill_x)* math.cos(angle * i*math.pi/180)-(_r)*math.sin(angle * i*math.pi/180)+drill_x
                #hole_y = (drill_x - drill_x)*math.sin(angle * i*math.pi/180)+_r* math.cos(angle * i*math.pi/180)+drill_y

                hole_x = (-1)*_r*math.sin(angle * i* (math.pi)/180) + drill_x
                hole_y = _r* math.cos(angle * i* (math.pi)/180) + drill_y                
                hole_location.append([hole_x, hole_y])
            if len(hole_location):
                for j in range(len(hole_location)):
                    epcam_api.add_pad(job, step, [], layer, hole_symbol_nme, hole_location[j][0], hole_location[j][1], 1, 0, 0, attributes)
    layer_info.set_include_symbol_filter([])

#对线性的孔进行补偿
def add_new_line_drill(job, step, layer, attributes, oval_size, round_size, diameter_list, long_resize_size, short_resize_size, 
                        isEnDiameter, oval_range, short_aspect_ratio, ultrashort_slot_resize):  
    layer_info.reset_select_filter()
    layer_info.set_featuretype_filter(66)
    layer_info.set_attribute_filter(0, attributes)
    layer_info.select_features_by_filter(job, step, [layer])   
    #获取每一个选中的线的坐标和symbolname和基本属性
    line_list = []
    line_list = layer_info.get_features_infos(job, step, layer)
    if len(line_list):
        epcam_api.sel_delete(job, step, [layer])
        epcam_api.clear_selected_features(job, step, layer)
        for line_info in line_list:
            line_name = line_info[2]        #线的symbolname
            line_XS = line_info[6] * 25400000
            line_YS = line_info[7] * 25400000
            line_XE = line_info[8] * 25400000
            line_YE = line_info[9] * 25400000  #line起始点坐标
            line_x = (line_XS + line_XE) / 2
            line_y = (line_YS + line_YE) / 2  #line的坐标
            line_len2 = math.pow((line_YE - line_YS), 2) + math.pow((line_XE - line_XS), 2)     
            final_dis = round(math.sqrt(line_len2), 2)     #线两端圆心间的距离        
            line_width = layer_info.get_drillsize_by_symbolname(line_name)   #通过symbolname获取线宽
            line_len = final_dis + round(line_width, 2)        #线长为起始点长度+线宽  
            if final_dis == 0:                              #线的圆孔
                new_line_width = line_width + round_size         #补偿后的孔的大小
                if isEnDiameter:
                    #刀径表单位是mil 不用转换单位
                    real_size = get_drill_diameter_size(diameter_list, round(new_line_width / 25400, 3), attributes)
                    new_line_width = real_size      #单位是mil
                else:
                    #刀径表单位是纳米 先转换单位
                    real_size = get_drill_diameter_size(diameter_list, new_line_width, attributes)
                    new_line_width = real_size      #单位是nm
                    new_line_width = round(new_line_width / 25400, 3)
                new_line_name = 'r' + str(new_line_width)
                epcam_api.add_line(job, step, [], layer, new_line_name, line_XS, line_YS, line_XE, line_YE, 1, 0, attributes) #添加线              
                continue
            if attributes == [{".drill": "non_plated"}]:
                if oval_range > 0:
                    if line_width > oval_range * 25400:
                        epcam_api.add_line(job, step, [], layer, line_name, line_XS, line_YS, line_XE, line_YE, 1, 0, attributes) #添加线
                        continue
            #计算补偿后的线长宽
            new_line_len = line_len + oval_size[1] * 25400       #新的线长
            new_line_width = line_width + oval_size[0] * 25400   #新的线宽

            if isEnDiameter:
                #刀径表单位是mil 不用转换单位
                real_size = get_drill_diameter_size(diameter_list, round(new_line_width / 25400, 2), attributes)
                new_line_width = real_size * 25400
            else:
                #刀径表单位是纳米 先转换单位
                real_size = get_drill_diameter_size(diameter_list, new_line_width, attributes)
                new_line_width = real_size

            #添加尾数
            if new_line_len >= new_line_width * 2:
                new_line_len = new_line_len                             #纳米单位
                new_line_width = new_line_width + long_resize_size      #纳米单位
            elif new_line_len < new_line_width * 2:
                new_line_len = new_line_len                             #纳米单位
                if  new_line_len < new_line_width * short_aspect_ratio:  
                    new_line_width = new_line_width + ultrashort_slot_resize  
                else:              
                    new_line_width = new_line_width + short_resize_size     #纳米单位
            
            new_line_len = new_line_len - new_line_width          #线长减去线宽
            offset_final_x = (new_line_len / 2) * (line_XE - line_x) / (final_dis / 2)    
            offset_final_y = (new_line_len / 2) * (line_YE - line_y) / (final_dis / 2)    #计算补偿完的线端点相对于线中心的偏移
            final_XS = line_x + offset_final_x
            final_YS = line_y + offset_final_y
            final_XE = line_x - offset_final_x
            final_YE = line_y - offset_final_y
 
            new_line_name = 'r' + str(round(new_line_width / 25400, 3))        #线长为起始点长度+线宽  
            epcam_api.add_line(job, step, [], layer, new_line_name, final_XS, final_YS, final_XE, final_YE, 1, 0, attributes) #添加线                        
    layer_info.reset_select_filter()
    epcam_api.clear_selected_features(job, step, layer)

#锣槽移到外形线层
def oval2outline(job, step, oval_range, round_range, outline_size):  
    try:
        #获取孔层
        oval_range = oval_range * 25400
        outline_size = outline_size * 25400
        round_range = round_range * 25400
        all_layer_list = []            #所有层名
        all_layer_list = layer_info.get_all_layer_name(job)
        if 'outline' not in all_layer_list:
            return
        drill_layer = []
        drill_layer = layer_info.get_drill_layer_name(job)
        for _layer in drill_layer:
            #新建临时层
            tem_layer = _layer + '-temp'
            job_operation.create_layer(job, tem_layer)
            if oval_range > 0:
                #对线操作
                layer_info.reset_select_filter()
                layer_info.set_featuretype_filter(66)
                layer_info.set_attribute_filter(0, [{".drill": "non_plated"}])
                layer_info.select_features_by_filter(job, step, [_layer])
                info_list = layer_info.get_features_infos(job, step, _layer)    #获取所有line的信息
                layer_info.reset_select_filter()
                layer_info.clear_select(job, step, _layer)  #清除选中并对每一个line进行选中判断  
                outline_list = []     #存放符合标准的symbolname
                for _line_info in info_list:   
                    if len(_line_info):
                        line_name = _line_info[2]
                        if line_name in outline_list:
                            continue
                        line_width = layer_info.get_drillsize_by_symbolname(line_name)   #通过symbolname获取线宽
                        if line_width > oval_range:
                            outline_list.append(line_name)
                if outline_list != []:
                    #symbolname筛选
                    layer_info.set_featuretype_filter(66)
                    layer_info.set_attribute_filter(0, [{".drill": "non_plated"}])
                    layer_info.set_include_symbol_filter(outline_list)
                    layer_info.select_features_by_filter(job, step, [_layer])
                    layer_info.sel_move_other(job, step, [_layer], job, step, tem_layer, False, 0, 0, 0, 0, 0, 0, 0)
                    layer_info.reset_select_filter()
            #对圆孔操作
            if round_range > 0:
                layer_info.set_featuretype_filter(65)
                layer_info.set_attribute_filter(0, [{".drill": "non_plated"}])
                layer_info.select_features_by_filter(job, step, [_layer])
                drill_info_list = layer_info.get_features_infos(job, step, _layer)    #获取所有line的信息
                layer_info.reset_select_filter()
                layer_info.clear_select(job, step, _layer)  #清除选中并对每一个line进行选中判断  
                drill_outline_list = []     #存放符合标准的symbolname
                for _drill_info in drill_info_list:   
                    if len(_drill_info):
                        drill_name = _drill_info[2]
                        if drill_name in drill_outline_list:
                            continue
                        drill_width = layer_info.get_drillsize_by_symbolname(drill_name)   #通过symbolname获取线宽
                        if drill_width > round_range:
                            drill_outline_list.append(drill_name)
                if drill_outline_list != []:
                    #symbolname筛选
                    layer_info.set_featuretype_filter(65)
                    layer_info.set_attribute_filter(0, [{".drill": "non_plated"}])
                    layer_info.set_include_symbol_filter(drill_outline_list)
                    layer_info.select_features_by_filter(job, step, [_layer])
                    layer_info.sel_move_other(job, step, [_layer], job, step, tem_layer, False, 0, 0, 0, 0, 0, 0, 0)
                    layer_info.reset_select_filter()
            accuracy = 0.25 * 25400
            separate_to_islands = True
            size = 3.0 * 25400
            mode = 0
            layer_info.contourize(job, step, [tem_layer], accuracy, separate_to_islands, size, mode) 
            epcam_api.surface2outline(job, step, [tem_layer], outline_size)
            layer_info.sel_move_other(job, step, [tem_layer], job, step, 'outline', False, 0, 0, 0, 0, 0, 0, 0)  
            job_operation.delete_layer(job, tem_layer)                      
    except Exception as e:
        print(e)
    return ''



 
     
    

    
