import os, sys
PyRecipe_module_inner_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_path + r'\epcam')
import layer_info as layer_info
import feature_resize as feature_resize
import epcam_api as api
import json
import epcam
import job_operation
import analysis_dfm

#选中line、arc，并进行resize
def inner_resize(job, step, inner_list, resize_delta, include_surface):
    try:
        #获取内层表
        # inner_list = layer_info.get_inner_layer_list(job)  
        if include_surface:
            featuretype = 95
        else :
            featuretype = 87
        for i in range(0,len(inner_list)):
            layer = []
            layer.append(inner_list[i])
            #选中LINE、ARC、TEXT、PAD、（SURFACE）
            layer_info.select_features_by_featuretype(job, step, layer, featuretype)
            #测试用
            # ret = api.get_selected_features_report(job, step, inner_list[i])
            # data = json.loads(ret)
            # print(data)
            #resize
            #epcam.show(r"C:/project/EPCAM/trunk/EPCAM/EP-CAM-Engineering/job",'odbjob_v6','pcb', inner_list[i])
            _resize = resize_delta * 25400
            feature_resize.resize_global(job, step, layer, 0, _resize)
            #取消选中
            layer_info.clear_select(job, step, inner_list[i])
            #epcam.show(r"C:/project/EPCAM/trunk/EPCAM/EP-CAM-Engineering/job",'odbjob_v6','pcb', inner_list[i])
    except:
        print('inner_resize skip')

#找出当前孔层不同大小的孔对应的孔盘，判断是否满足最小润环
def inner_resize_drillpad(jobname, step, inner_list, drill_name, drillpad_min_size):
    try:
        min_size = drillpad_min_size * 25400
        #获取内层表
        # inner_list = layer_info.get_inner_layer_list(jobname)  
        #测试数量用
        # num_list = []
        # num = 0

        #将孔层按size分类
        api.open_layer(jobname, step, drill_name)
        drill_pad_report = layer_info.get_all_drill_symbolname(jobname, step, drill_name)
        for a in range(0,len(drill_pad_report)):
            drill_symbol = drill_pad_report[a]

            #循环，在单层内按大小依次涨至MIN值
            for i in range(0,len(inner_list)):
                #print('*'*30)
                #print(inner_list[i]+'begin')
                symbol_list = layer_info.get_drillpad_symbolname(jobname, step, inner_list[i], min_size, drill_symbol,drill_name)
                if  symbol_list == []:
                #    num_list.append([inner_list[i], 0])
                    continue
                # num = num + len(symbol_list)
                # num_list.append([inner_list[i], len(symbol_list)])
                for j in range(0,len(symbol_list)):
                    layer_info.set_include_symbol_filter([symbol_list[j][0]])
                    layer_info.set_featuretype_filter(65)
                    reference_layers = []
                    reference_layers.append(drill_name)
                    api.filter_by_mode(jobname, step, inner_list[i], reference_layers, 0, 127, 0, [drill_symbol[0]])
                    size = (drill_symbol[1] + min_size*2 - symbol_list[j][1])         
                    sel_layer = [inner_list[i]]

                    ret = api.get_selected_features_report(jobname, step, inner_list[i])
                    data = json.loads(ret)
                    pad_list = data['paras']['pad_list']
                    #print(pad_list)

                    feature_resize.resize_global(jobname, step, sel_layer, 0, size)
                #print('*'*30)
                #print(inner_list[i]+'end')
    except:
        print('inner_resize_drillpad')
            

    # print(num)
    # print(num_list)

#新处理孔盘方式
def inner_drillpad_resize(job, step, inner_list, drill_name, drillpad_min_size):
    try:
        drillpad_attribute = [".pth_pad", ".via_pad", ".npth_pad"]
        drill_attribute = [{".drill": "plated"}, {".drill": "via"}, {".drill": "non_plated"}]
        for k in range(0,len(inner_list)):
            #依据属性选中孔盘
            #move至新层
            for i in range(len(drillpad_attribute)):
                layer_info.clear_select(job, step, inner_list[k])
                attribute_list = [{drillpad_attribute[i]: ""}]
                layer_info.select_features_by_attributes(job, step, [inner_list[k]], 0, attribute_list)  #选中
                point_list = []
                point_list = layer_info.get_selected_pad_point(job, step, inner_list[k])
                if point_list == []:
                    continue
                new_inner_layer = inner_list[k] + '-copy'
                job_operation.create_layer(job, new_inner_layer)
                layer_info.sel_move_other(job, step, [inner_list[k]], job, step, new_inner_layer, False, 0, 0, 0, 0, 0, 0, 0)
                layer_info.clear_select(job, step, inner_list[k])
                #layer_info.sel_move_other(job, step, [inner_list[k]], new_inner_layer, False, 0, 0, 0, 0, 0, 0, 0)
                #依据新内层touch孔层
                #layer_info.reset_select_filter()
                layer_info.set_attribute_filter(1, [drill_attribute[i]])
                api.filter_by_mode(job, step, drill_name, [new_inner_layer], 0, 127, -1, 'useless')
                layer_info.reset_select_filter()
                #获取孔层所有孔坐标，调用API，判断是否需要resize
                point_list = layer_info.get_selected_pad_point(job, step, drill_name)
                layer_info.clear_select(job, step, drill_name)
                for j in range(len(point_list)):       
                    select_polygon = [[point_list[j][0] - 1000, point_list[j][1] - 1000],
                                    [point_list[j][0] - 1000, point_list[j][1] + 1000],
                                    [point_list[j][0] + 1000, point_list[j][1] + 1000],
                                    [point_list[j][0] + 1000, point_list[j][1] - 1000],
                                    [point_list[j][0] - 1000, point_list[j][1] - 1000]]
                    tol = analysis_dfm.get_min_tolerance(job, step, drill_name, new_inner_layer, select_polygon)
                    #drillpad_min_size
                    if tol != [] and tol[0] == False:
                        a=1
                        #print([point_list[j][0],point_list[j][1]])
                    elif tol != [] and tol[0] == True:
                        if 0 < tol[1] < (drillpad_min_size*25400):
                            size = (drillpad_min_size*25400 - tol[1])* 2
                            layer_info.select_feature(job, step, new_inner_layer, select_polygon, {}, 0, False)
                            feature_resize.resize_global(job, step, [new_inner_layer], 0, size)
                            layer_info.clear_select(job, step, new_inner_layer)
                #之后copy回原内层，删除新层
                layer_info.sel_move_other(job, step, [new_inner_layer], job, step, inner_list[k], False, 0, 0, 0, 0, 0, 0, 0)
                job_operation.delete_layer(job, new_inner_layer)
    except:
        print('inner_drillpad_resize skip')