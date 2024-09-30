import os, sys
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_silkscreen_path = os.path.dirname(PyRecipe_base_path) + r'\module\silkscreen'
sys.path.append(PyRecipe_module_silkscreen_path)
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
import layer_info as layer_info
import silkscreen_resize
import job_operation
import feature_resize
import json
import epcam
import epcam_api


def silkscreen_process_resize(job, step, silk_line_width, silk_tall, silk_width, size, addJobText):
    try:
        silkscreen_list = layer_info.get_silkscreen_layer(job)
        if len(silkscreen_list)==0:
            return 
        #删除文字所有属性
        epcam_api.modify_attributes(job, step, silkscreen_list, 1, [])

        for _layer in silkscreen_list:
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
                    if line_width < 152400:
                        layer_info.change_feature_symbols(job, step, [_layer], 'r6')
                    layer_info.clear_select(job, step, _layer)
        layer_info.reset_select_filter()
        # silkscreen_list = layer_info.get_silkscreen_layer(job)
        # if len(silkscreen_list)==0:
        #     return 0
        # #备份原layer
        # for v in range(len(silkscreen_list)):
        #     prepare_layer = job_operation.copy_layer(job, silkscreen_list[v])
        #     sk_layer = silkscreen_list[v] + '-pre'
        #     job_operation.rename_layer(job, prepare_layer, sk_layer, 'misc')

        # #调整TEXT和LINE、ARC的线宽
        # silkscreen_resize.silkscreen_linearc_resize(job, step, silk_line_width)
        # silkscreen_resize.silkscreen_text_resize(job, step, silk_tall, silk_width, silk_line_width)
        #整体resize防焊负片贴到丝印层
        solder_mask_list = layer_info.get_soldermask_list(job)
            #layer_list = layer_info.get_silkscreen_layer(job)
        for i in range(0, len(silkscreen_list)):
            #新建空layer
            job_operation.create_layer(job, 'copy')
            sm_layer = solder_mask_list[i]
            layer_info.sel_copy_other(job, step, [sm_layer], ['copy'], 0, 0, 0, 
                0, 0, 0, 0, 0)
            layer_info.contourize(job, step, ['copy'], 6350, True, 76200, 0)
            feature_resize.resize_global(job, step, ['copy'], 1, size*25400)            
            ss_layer=silkscreen_list[i]
            layer_info.sel_copy_other(job, step, ['copy'], [ss_layer], 1, 0, 0, 
                0, 0, 0, 0, 0)
            #删除新层
            job_operation.delete_layer(job, 'copy')

            if i < 1:
                if addJobText['isaddJobText']:
                    add_job_text(job, step, ss_layer, addJobText)
            #surface涨0.1mm
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, ss_layer)
            layer_info.set_featuretype_filter(72)
            layer_info.select_features_by_filter(job, step, [ss_layer])  
            feature_resize.resize_global(job, step, [ss_layer], 0, 100000)
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, ss_layer)
    except Exception as e:
        print(e)
    return ''

#添加料号名
def add_job_text(job, step, layer, addJobText):
    try:
        text_width = addJobText['jobText_width'] * 25400        #字宽
        text_height = addJobText['jobText_height'] * 25400      #字高
        line_width =  addJobText['jobText_linewidth'] * 25400   #线宽
        if text_width == 0 or text_height == 0 or line_width == 0:
            return
        add_str = job                            #判断添加文字长度是否大于7 大于7则取后七位
        if len(add_str) > 7:
            str_list = list(add_str) 
            str_list = str_list[-7:]
            add_str = ''.join(str_list)          #需要添加的字符串
        str_length = len(add_str)                                   #料号名长度
        str_width = str_length * text_width                     #字串宽度
        str_height = text_height                                #字串高度
        # profile_param = []
        # profile_param = layer_info.get_profile_box(job, step)
        # if len(profile_param) == 0:
        #     return
        ret = epcam_api.get_profile_box(job, step)
        data = json.loads(ret)
        profile_xmin = data['paras']['Xmin']    #profile线的box
        profile_ymin = data['paras']['Ymin']
        profile_xmax = data['paras']['Xmax']
        profile_ymax = data['paras']['Ymax']

        signal_layer = []                                       #所有线路层名，用于计算通孔层名
        signal_layer = layer_info.get_signal_layer_list(job)
        drill_layer = []                                        #所有孔层名
        drill_layer = layer_info.get_drill_layer_name(job)
        if len(signal_layer) > 1:  
            drl_name = 'drl1-' + str(len(signal_layer))
        # profile_width = profile_param[0]                        #profile宽度
        # profile_height = profile_param[1]                       #profile高度
        x_offset = 0
        y_offset = 0
        x_min = profile_xmin
        y_min = profile_ymin
        x_max = str_width + 50800
        y_max = str_height + 50800
        break_flag = True
        layer_info.set_selection(True, True, True, True, True, False)
        num_y = 0    #记录上一次的纵向位移
        while((x_max + x_offset) <= profile_xmax): 
            _x_max_list = []
            y_offset = 0
            num_y = 0
            while((y_max + y_offset) <= profile_ymax):
                select_poligon = [[x_min + x_offset, y_min + y_offset], 
                        [x_min + x_offset, y_max + y_offset], 
                        [x_max + x_offset, y_max + y_offset], 
                        [x_max + x_offset, y_min + y_offset], 
                        [x_min + x_offset, y_min + y_offset]]              #选框的box
                layer_info.select_feature(job, step, layer, select_poligon, {}, 1, False)
                layer_info.select_feature(job, step, drl_name, select_poligon, {}, 1, False)
                ret = epcam_api.get_selected_features_box(job, step, [layer, drl_name])   #获取选中feature的box
                layer_info.clear_select(job, step, layer)                     #清除两层选中
                layer_info.clear_select(job, step, drl_name)
                data = json.loads(ret)
                _box_xmin = data['xmin']
                _box_ymin = data['ymin']
                _box_xmax = data['xmax']
                _box_ymax = data['ymax']
                if _box_xmax == 0 or _box_ymax == 0:
                    break_flag = False
                    break
                _x_max_list.append(_box_xmax)
                if _box_ymax - _box_ymin > y_max:
                    y_offset = y_offset + y_max
                else:                   
                    y_offset = _box_ymax
                if y_offset == num_y:
                    y_offset = y_offset + str_height + 25400
                num_y = y_offset
            if(len(_x_max_list)):
                _x_max_list.sort(reverse=True)
                #x_offset = _x_max_list[0]
                x_offset = x_offset + x_max
            if break_flag == False:
                break
        layer_info.reset_selection()
        #得到文字框左下角的坐标
        location_x = x_min + x_offset + 25400# - str_width/2
        location_y = y_min + y_offset + 25400# - str_height/2
        text_name = add_str
        epcam_api.add_text(job, step, layer, '', 'standard', text_name, text_width, text_height, line_width, location_x, location_y, 1, 0, 0, [], [])   
        # data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":layer}
        # js = json.dumps(data2)
        # epcam.view_cmd(js)
    except Exception as e:
        print(e)
    return ''

#outline层添加料号编号
def outline_add_job_id(job, step, layer, routaddId):
    try:
        text_width = routaddId['rout_text_width'] * 25400        #字宽
        text_height = routaddId['rout_text_height'] * 25400      #字高
        line_width =  routaddId['rout_text_linewidth'] * 25400   #线宽
        if text_width == 0 or text_height == 0 or line_width == 0:
            return
        add_str = job                            #判断添加文字长度是否大于7 大于7则取后七位
        if len(add_str) > 7:
            str_list = list(add_str) 
            str_list = str_list[-7:]
            add_str = ''.join(str_list)          #需要添加的字符串
        str_length = len(add_str)                                   #料号名长度
        str_width = str_length * text_width                     #字串宽度
        str_height = text_height                                #字串高度
        ret = epcam_api.get_profile_box(job, step)
        data = json.loads(ret)
        profile_xmin = data['paras']['Xmin']    #profile线的box
        profile_ymin = data['paras']['Ymin']
        profile_xmax = data['paras']['Xmax']
        profile_ymax = data['paras']['Ymax']

        x_offset = 0
        y_offset = 0
        x_min = profile_xmin
        y_min = profile_ymin
        x_max = str_width + 50800
        y_max = str_height + 50800
        break_flag = True
        layer_info.set_selection(True, True, True, True, True, False)
        num_y = 0    #记录上一次的纵向位移
        while((x_max + x_offset) <= profile_xmax): 
            _x_max_list = []
            y_offset = 0
            num_y = 0
            while((y_max + y_offset) <= profile_ymax):
                select_poligon = [[x_min + x_offset, y_min + y_offset], 
                        [x_min + x_offset, y_max + y_offset], 
                        [x_max + x_offset, y_max + y_offset], 
                        [x_max + x_offset, y_min + y_offset], 
                        [x_min + x_offset, y_min + y_offset]]              #选框的box
                layer_info.select_feature(job, step, layer, select_poligon, {}, 1, False)
                ret = epcam_api.get_selected_features_box(job, step, [layer])   #获取选中feature的box
                layer_info.clear_select(job, step, layer)                     #清除选中
                data = json.loads(ret)
                _box_xmin = data['xmin']
                _box_ymin = data['ymin']
                _box_xmax = data['xmax']
                _box_ymax = data['ymax']
                if _box_xmax == 0 or _box_ymax == 0:
                    break_flag = False
                    break
                _x_max_list.append(_box_xmax)
                if _box_ymax - _box_ymin > y_max:
                    y_offset = y_offset + y_max
                else:                   
                    y_offset = _box_ymax
                if y_offset == num_y:
                    y_offset = y_offset + str_height + 25400
                num_y = y_offset
            if(len(_x_max_list)):
                _x_max_list.sort(reverse=True)
                #x_offset = _x_max_list[0]
                x_offset = x_offset + x_max
            if break_flag == False:
                break
        layer_info.reset_selection()
        #得到文字框左下角的坐标
        location_x = x_min + x_offset + 25400# - str_width/2
        location_y = y_min + y_offset + 25400# - str_height/2
        text_name = add_str
        epcam_api.add_text(job, step, layer, '', 'standard', text_name, text_width, text_height, line_width, location_x, location_y, 1, 0, 0, [], [])   
    except Exception as e:
        print(e)
    return ''

# i_max =  profile_width / (str_width + 25400)
# i_max = int(i_max)
# j_max =  profile_height / (str_height + 25400)
# j_max = int(j_max)
# if i_max < 1 or j_max < 1:
#     return
# location_x = 0
# location_y = 0
# for i in range(i_max - 1):
#     for j in range(j_max - 1):
#         select_poligon = [[(str_width + 25400) * i, (str_height + 25400) * j], 
#                           [(str_width + 25400) * i, (str_height + 25400) * (j + 1)], 
#                           [(str_width + 25400) * (i + 1), (str_height + 25400) * (j + 1)], 
#                           [(str_width + 25400) * (i + 1), (str_height + 25400) * j], 
#                           [(str_width + 25400) * i, (str_height + 25400) * j]]              #选框的box
#         layer_info.select_feature(job, step, layer, select_poligon, {}, 0, False)
#         data = epcam_api.get_selected_feature_infos(job, step, layer)
#         data = json.loads(data)
#         if data['paras'] == False:
#             location_x = (str_width + 25400) * i + 12700
#             location_y = (str_height + 25400) * j + 12700
#             break 2