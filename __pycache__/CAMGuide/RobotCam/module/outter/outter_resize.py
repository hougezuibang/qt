import os, sys
PyRecipe_module_outter_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_path + r'\epcam')
import layer_info as layer_info
import feature_resize as feature_resize
import job_operation
import epcam_api as api
import json
import epcam
import analysis_dfm as analysis_dfm

#统一涨LINE，ARC，PAD，TEXT，（SURFACE）
def outter_pre_resize(job, step, resize_delta, include_surface, outter_list):
    try:
        if include_surface:
            featuretype = 95
        else :
            featuretype = 87
        for i in range(0,len(outter_list)):
            layer = []
            layer.append(outter_list[i])
            #选中LINE、ARC、TEXT、PAD、（SURFACE）
            layer_info.select_features_by_featuretype(job, step, layer, featuretype)

            _resize = resize_delta * 25400
            feature_resize.resize_global(job, step, layer, 0, _resize)
            #取消选中
            layer_info.clear_select(job, step, outter_list[i])
            #epcam.show(r"C:/project/EPCAM/trunk/EPCAM/EP-CAM-Engineering/job",'odbjob_v6','pcb', inner_list[i])
    except:
        print('outter_pre_resize skip')

#涨孔PAD
def outter_drillpad_resize(job, step, drillpad_min_size, outter_list):
    try:
        min_size = drillpad_min_size * 25400
        #获取孔层列表
        drill_list = layer_info.get_drill_layer_name(job, step)   
        for t in range(0, len(drill_list)):
            drill_name = drill_list[t]
            api.open_layer(job, step, drill_name)
            #获取当前孔层的drill信息
            drill_pad_report = layer_info.get_all_drill_symbolname(job, step, drill_name)
            for a in range(0,len(drill_pad_report)):
                drill_symbol = drill_pad_report[a]

                #循环，在单层内按大小依次涨至MIN值
                for i in range(0,len(outter_list)):
                    #print('*'*30)
                    #print(outter_list[i]+'begin')
                    symbol_list = layer_info.get_drillpad_symbolname(job, step, outter_list[i], min_size, drill_symbol,drill_name)
                    if  symbol_list == []:
                        continue
                    for j in range(0,len(symbol_list)):
                        layer_info.set_include_symbol_filter([symbol_list[j][0]])
                        layer_info.set_featuretype_filter(65)
                        reference_layers = []
                        reference_layers.append(drill_name)
                        api.filter_by_mode(job, step, outter_list[i], reference_layers, 0, 127, 0, [drill_symbol[0]])
                        size = (drill_symbol[1] + min_size*2 - symbol_list[j][1])         
                        sel_layer = [outter_list[i]]

                        # ret = api.get_selected_features_report(jobname, step, inner_list[i])
                        # data = json.loads(ret)
                        # pad_list = data['paras']['pad_list']
                        # print(pad_list)

                        feature_resize.resize_global(job, step, sel_layer, 0, size)
    except:
        print('outter_drillpad_resize skip')

#smd pad
def smd_pad_resize(job, step, tolerance_smd, outter_list):
    soldermask_list = layer_info.get_soldermask_list(job)
    clearance_resize(job, step, outter_list, soldermask_list, {".smd": ""}, tolerance_smd)
    gascate_resize(job, step, outter_list, soldermask_list, {".smd": ""}, tolerance_smd)

#bga pad
def bga_pad_resize(job, step, tolerance_bga, outter_list):
    soldermask_list = layer_info.get_soldermask_list(job)
    clearance_resize(job, step, outter_list, soldermask_list, {".bga": ""}, tolerance_bga)
    gascate_resize(job, step, outter_list, soldermask_list, {".bga": ""}, tolerance_bga)

#PTH开窗处理至满足最小公差
def pth_pad_resize(job, step, pthpad_sm_min, outter_list):
    soldermask_list = layer_info.get_soldermask_list(job)
    clearance_resize(job, step, outter_list, soldermask_list, {".drill":"plated"}, pthpad_sm_min)

#smd pad
def smd_pad_resize_opt(job, step, tolerance_smd, outter_list, resize_delta):
    outter = layer_info.get_outter_list(job)
    soldermask = layer_info.get_soldermask_list(job)
    soldermask_list = []
    for p in range(len(outter_list)):
        index = outter.index(outter_list[p])
        soldermask_list.append(soldermask[index])
    clearance_resize_opt(job, step, outter_list, soldermask_list, {".smd": ""}, tolerance_smd)
    skylight_resize_opt(job, step, outter_list, soldermask_list, {".smd": ""}, tolerance_smd, resize_delta)
    #gascate_resize_opt(job, step, outter_list, soldermask_list, {".smd": ""}, tolerance_smd)

#bga pad
def bga_pad_resize_opt(job, step, tolerance_bga, outter_list, resize_delta):
    outter = layer_info.get_outter_list(job)
    soldermask = layer_info.get_soldermask_list(job)
    soldermask_list = []
    for p in range(len(outter_list)):
        index = outter.index(outter_list[p])
        soldermask_list.append(soldermask[index])
    clearance_resize_opt(job, step, outter_list, soldermask_list, {".bga": ""}, tolerance_bga)
    skylight_resize_opt(job, step, outter_list, soldermask_list, {".bga": ""}, tolerance_bga, resize_delta)
    #gascate_resize_opt(job, step, outter_list, soldermask_list, {".bga": ""}, tolerance_bga)


def clearance_resize(job, step, outter_list, soldermask_list, bga_or_smd, min_size):
    '''
    开窗大于pad处理，resize防焊层
    总共两对，分两次处理
    对于每一对：1.复制出外层new_layer；->（reference——layer）
                2.在new_layer中选中（bga/smd）且含有clearance属性的pad，并获得该层pad的symbol信息（symbolname,size信息）；
                3.反选，并删除选中的feature，new_layer变为只含有clearance属性的（bga/smd）pad的层；
                对应于new-layer中的每种symbol：
                    1.第一次touch（防焊层->new-layer），选中防焊层中对应于该大小的pad的开窗，并获得所有symbol信息（symbolname,size信息）；
                    2.第二次touch（防焊层->new-layer），将获得的symbolname填入filter，只筛选出一种大小的开窗，并进行resize
                4.删除new_layer
    '''
    try:
        outter_soldermask_pair = []                 #存储两对外层防焊对
        pair1 = [outter_list[0], soldermask_list[0]]
        pair2 = [outter_list[1], soldermask_list[1]]
        outter_soldermask_pair.append(pair1)
        outter_soldermask_pair.append(pair2)
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #复制出外层new_layer
            new_layer = job_operation.copy_layer(job, outter_layer)
            layer_info.change_layer_context(job, new_layer, 'misc')
            #在new_layer中选中（bga/smd）且含有clearance属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            attribute_list = [{".fiducial_name": "cle"}]
            attribute_list.append(bga_or_smd)
            #attribute_list = [{bga_or_smd: ""}]
            layer_info.select_features_by_attributes(job, step, [new_layer], 0, attribute_list)  #选中
            smd_or_bga_list = layer_info.get_smd_or_bga_symbolname(job, step, new_layer)                         #获取开窗孔的symbol信息
            #反选，并删除选中的feature，new_layer变为只含有clearance属性的（bga/smd）pad的层
            layer_info.reverse_select(job, step, new_layer)
            layer_info.delete_feature(job, step, [new_layer])
            #对应于new-layer中的每种symbol：
            for j in range(len(smd_or_bga_list)):
                #第一次touch
                layer_info.set_include_symbol_filter('')
                layer_info.set_attribute_filter(-1, '')
                layer_info.set_featuretype_filter(65)
                include_symbol = smd_or_bga_list[j][0]
                api.filter_by_mode(job, step, soldermask_layer, [new_layer], 0, 127, 0, [include_symbol])
                kaichuang_pad_symbollist = layer_info.get_soldermask_pad_symbol(job, step, soldermask_layer, min_size, smd_or_bga_list[j])
                #第二次touch
                for k in range(0,len(kaichuang_pad_symbollist)):
                    #layer_info.reset_select_filter()
                    layer_info.set_include_symbol_filter([kaichuang_pad_symbollist[k][0]])
                    layer_info.set_featuretype_filter(65)
                    api.filter_by_mode(job, step, soldermask_layer, [new_layer], 0, 127, 0, [smd_or_bga_list[j][0]])
                    try:
                        if smd_or_bga_list[j][0][0:4] == 'rect' or smd_or_bga_list[j][0][0:4] == 'oval':
                            symbolname = smd_or_bga_list[j][0]
                            str1 = symbolname[4:]
                            if 'r' in str1: 
                                index_r = str1.index('r')
                                str1 = str1[0:index_r-1]
                            index_x = str1.index('x')
                            number_1 = float(str1[:(index_x)])
                            number_2 = float(str1[(index_x+1):])
                            kaichuangname = kaichuang_pad_symbollist[k][0]
                            str2 = kaichuangname[4:]
                            if 'r' in str2: 
                                index_r = str2.index('r')
                                str2 = str2[0:index_r-1]
                            index_xx = str2.index('x')
                            number_11 = float(str2[:(index_xx)])
                            number_22 = float(str2[(index_xx+1):])
                            if (number_11-number_1)<(number_22-number_2):
                                size = (number_1 + min_size*2 - number_11) * 25400
                            else:
                                size = (number_2 + min_size*2 - number_22) * 25400
                        else:
                            size = smd_or_bga_list[j][1] + min_size*2 * 25400 - kaichuang_pad_symbollist[k][1] 
                        #epcam.show(r"C:/project/trunk/EPCAM/EP-CAM-Engineering/job", 'new1', 'step1', 'g')      
                        feature_resize.resize_global(job, step, [soldermask_layer], 0, size)
                        #epcam.show(r"C:/project/trunk/EPCAM/EP-CAM-Engineering/job", 'new1', 'step1', 'g')
                    except:
                        continue
            #删除复制出的newlayer
            layer_info.reset_select_filter()
            job_operation.delete_layer(job, new_layer)
    except:
        print('clearance_resize skip')

def gascate_resize(job, step, outter_list, soldermask_list, bga_or_smd, min_size):
    '''
    开窗小于pad处理，resize外层
    总共两对，分两次处理
    对于每一对：1.复制出外层new_layer；->（reference——layer）
                2.在new_layer中选中（bga/smd）且含有gascate属性的pad；
                3.反选，并删除选中的feature，new_layer变为只含有gascate属性的（bga/smd）pad的层；
                4.复制出防焊new_sm_layer;
                5.进行一次touch（new_sm_layer->new_layer），选中new_sm_layer中对应于new_layer中的pad的开窗，并获得被选中pad的symbol信息（symbolname,size信息）
                6.在new_sm_layer中反选，删除选中feature，使得new_sm_layer中只剩开窗；
                对应于new_sm_layer中的每种symbol：
                    1.第一次touch（外层->new_sm_layer），选中外层中对应于该大小的开窗的pad，并获得所有symbol信息（symbolname,size信息）；
                    2.第二次touch（外层->new_sm_layer），将获得的symbolname填入filter，只筛选出一种大小的pad，并进行resize
                7.删除new_layer,new_sm_layer
    '''
    try:
        outter_soldermask_pair = []                 #存储两对外层防焊对
        pair1 = [outter_list[0], soldermask_list[0]]
        pair2 = [outter_list[1], soldermask_list[1]]
        outter_soldermask_pair.append(pair1)
        outter_soldermask_pair.append(pair2)
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #复制出外层new_layer和防焊new_sm_layer
            new_layer = job_operation.copy_layer(job, outter_layer)
            new_sm_layer = job_operation.copy_layer(job, soldermask_layer)

            layer_info.change_layer_context(job, new_layer, 'misc')
            layer_info.change_layer_context(job, new_sm_layer, 'misc')
            #在new_layer中选中（bga/smd）且含有clearance属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            #attribute_list = [{bga_or_smd: ""}, {".fiducial_name": "gas"}]
            attribute_list = [{".fiducial_name": "gas"}]
            attribute_list.append(bga_or_smd)
            layer_info.select_features_by_attributes(job, step, [new_layer], 0, attribute_list)  #选中

            #反选，并删除选中的feature，new_layer变为只含有clearance属性的（bga/smd）pad的层
            layer_info.reverse_select(job, step, new_layer)
            layer_info.delete_feature(job, step, [new_layer])
            #进行一次touch（new_sm_layer->new_layer），选中new_sm_layer中对应于new_layer中的pad的开窗，并获得被选中pad的symbol信息（symbolname,size信息）
            layer_info.set_featuretype_filter(65)
            layer_info.set_include_symbol_filter('')
            layer_info.set_attribute_filter(-1, '')
            api.filter_by_mode(job, step, new_sm_layer, [new_layer], 0, 127, -1 , ['useless'])
            smd_or_bga_list = layer_info.get_smd_or_bga_symbolname(job, step, new_sm_layer) 
            #在new_sm_layer中反选，删除选中feature，使得new_sm_layer中只剩开窗
            layer_info.reverse_select(job, step, new_sm_layer)
            layer_info.delete_feature(job, step, [new_sm_layer])
            #对应于new_sm_layer中的每种symbol：
            for j in range(len(smd_or_bga_list)):
                #第一次touch
                api.filter_by_mode(job, step, outter_layer, [new_sm_layer], 0, 127, 0 , [smd_or_bga_list[j][0]])
                kaichuang_pad_symbollist = layer_info.get_soldermask_pad_symbol(job, step, outter_layer, min_size, smd_or_bga_list[j])
                #第二次touch
                for k in range(0,len(kaichuang_pad_symbollist)):
                    #layer_info.reset_select_filter()
                    layer_info.set_include_symbol_filter([kaichuang_pad_symbollist[k][0]])
                    layer_info.set_featuretype_filter(65)
                    api.filter_by_mode(job, step, outter_layer, [new_sm_layer], 0, 127, 0, [smd_or_bga_list[j][0]])
                    try:
                        if smd_or_bga_list[j][0][0:4] == 'rect' or smd_or_bga_list[j][0][0:4] == 'oval':
                            symbolname = smd_or_bga_list[j][0]
                            str1 = symbolname[4:]
                            if 'r' in str1: 
                                index_r = str1.index('r')
                                str1 = str1[0:index_r-1]
                            index_x = str1.index('x')
                            number_1 = float(str1[:(index_x)])
                            number_2 = float(str1[(index_x+1):])
                            kaichuangname = kaichuang_pad_symbollist[k][0]
                            str2 = kaichuangname[4:]
                            if 'r' in str2: 
                                index_r = str2.index('r')
                                str2 = str2[0:index_r-1]
                            index_xx = str2.index('x')
                            number_11 = float(str2[:(index_xx)])
                            number_22 = float(str2[(index_xx+1):])
                            if (number_11-number_1)<(number_22-number_2):
                                size = (number_1 + min_size*2 - number_11) * 25400
                            else:
                                size = (number_2 + min_size*2 - number_22) * 25400
                        else:
                            size = smd_or_bga_list[j][1] + min_size*2*25400- kaichuang_pad_symbollist[k][1]         
                        feature_resize.resize_global(job, step, [outter_layer], 0, size)   
                    except:
                        continue    
            #删除复制出的newlayer,new_sm_layer
            layer_info.reset_select_filter()
            job_operation.delete_layer(job, new_layer)
            job_operation.delete_layer(job, new_sm_layer)
    except:
        print('gascate_resize')


def gascate_resize_opt(job, step, outter_list, soldermask_list, bga_or_smd, opt_tol):
    try:
        # outter_soldermask_pair = []        #存储两对外层防焊对
        # pair1 = [outter_list[0], soldermask_list[0]]
        # pair2 = [outter_list[1], soldermask_list[1]]
        # #outter_soldermask_pair.append(pair2)
        # outter_soldermask_pair.append(pair1)
        # outter_soldermask_pair.append(pair2)
        if len(outter_list) != len(soldermask_list):
            return
        outter_soldermask_pair = []
        for p in range(len(outter_list)):
            pair = [outter_list[p], soldermask_list[p]]
            outter_soldermask_pair.append(pair)
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #在outter_layer中选中（bga/smd）且含有gas属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            attribute_list = [{".fiducial_name": "gas"}]
            attribute_list.append(bga_or_smd)
            layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
            #获取new_layer中每个pad的中心点
            point_list = []
            point_list = layer_info.get_selected_pad_point(job, step, outter_layer)
            #将选中的bga/smd cle pad 移动到new_layer
            new_layer = outter_layer + '-move'
            job_operation.create_layer(job, new_layer)
            layer_info.sel_move_other(job, step, [outter_layer], job, step, new_layer, False, 0, 0, 0, 0, 0, 0, 0)
            layer_info.clear_select(job, step, outter_layer)
            
            if len(point_list):
                for j in range(len(point_list)):
                    select_poligon = [[point_list[j][0] - 1000, point_list[j][1] - 1000],
                    [point_list[j][0] - 1000, point_list[j][1] + 1000],
                    [point_list[j][0] + 1000, point_list[j][1] + 1000],
                    [point_list[j][0] + 1000, point_list[j][1] - 1000],
                    [point_list[j][0] - 1000, point_list[j][1] - 1000]]
                    #获取new_layer中该pad与对应防焊层中开窗的最小公差
                    tol = []
                    tol = analysis_dfm.get_min_tolerance(job, step, new_layer, soldermask_layer, select_poligon)
                    if tol[0] == False:
                        continue
                    min_tol = abs(tol[1])                    
                    if min_tol >= opt_tol:
                        continue
                    layer_info.select_feature(job, step, new_layer, select_poligon, {}, 0, False)
                    #与范围内物件的最小间距为dis
                    dis = analysis_dfm.get_selected_feature_min_spacing(job, step, new_layer, opt_tol + 25400 - min_tol)
                    if dis == -1:
                        feature_resize.resize_global(job, step, [new_layer], 0, (opt_tol - min_tol) * 2)
                    else:
                        feature_resize.resize_global(job, step, [new_layer], 0, (dis - 25400) * 2)

                    layer_info.select_feature(job, step, new_layer, select_poligon, {}, 0, False)
                    layer_info.clear_select(job, step, new_layer)                  
            layer_info.sel_copy_other(job, step, [new_layer], [outter_layer], False, 0, 0, 0, 0, 0, 0, 0)
            #删除复制出的newlayer,new_sm_layer
            layer_info.reset_select_filter()
            #job_operation.delete_layer(job, new_layer)
            layer_info.clear_select(job, step, outter_layer)

    except:
        print('gascate_resize_opt')

#  


def clearance_resize_opt(job, step, outter_list, soldermask_list, bga_or_smd, opt_tol):
    try:
        if len(outter_list) != len(soldermask_list):
            return
        outter_soldermask_pair = []
        for p in range(len(outter_list)):
            pair = [outter_list[p], soldermask_list[p]]
            outter_soldermask_pair.append(pair)
        layer_info.reset_select_filter()
        attribute_list = [{".fiducial_name": "cle"}]
        attribute_list.append(bga_or_smd)
        layer_info.reset_select_filter()
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #在outter_layer中选中（bga/smd）且含有gas属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            layer_info.clear_select(job, step, outter_layer)
            layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
            #获取new_layer中每个pad的中心点
            point_list = []
            point_list = layer_info.get_selected_pad_point(job, step, outter_layer)
            feature_list = []
            #将选中的bga/smd cle pad 拷贝到new_layer
            if len(point_list):
                new_layer = outter_layer + '-selcopy'
                tem_layer = 'tem_layer'
                job_operation.create_layer(job, new_layer)
                job_operation.create_layer(job, tem_layer)
                layer_info.sel_copy_other(job, step, [outter_layer], [new_layer], False, 0, 0, 0, 0, 0, 0, 0)
                #用new_layer中的每个pad touch对应防焊层的pad
                layer_info.clear_select(job, step, outter_layer)
                layer_info.reset_select_filter()
                layer_info.set_featuretype_filter(73)
                api.filter_by_mode(job, step, soldermask_layer, [new_layer], 0, 65, -1 , ['useless'])
                #将touch到pad移动到new_mask_layer
                new_mask_layer = soldermask_layer + '-move'
                job_operation.create_layer(job, new_mask_layer)
                layer_info.sel_move_other(job, step, [soldermask_layer], job, step, new_mask_layer, False, 0, 0, 0, 0, 0, 0, 0)
                layer_info.reset_select_filter()
                layer_info.reset_selection()
                layer_info.clear_select(job, step, soldermask_layer)
                for j in range(len(point_list)):
                    select_poligon = [[point_list[j][0] - 1, point_list[j][1] - 1],
                    [point_list[j][0] - 1, point_list[j][1] + 1],
                    [point_list[j][0] + 1, point_list[j][1] + 1],
                    [point_list[j][0] + 1, point_list[j][1] - 1],
                    [point_list[j][0] - 1, point_list[j][1] - 1]]
                    #获取new_layer中该pad与对应防焊层中开窗的最小公差
                    tol = []
                    tol = analysis_dfm.get_min_tolerance(job, step, new_layer, new_mask_layer, select_poligon)
                    #min_tol = abs(tol[1]) 
                    min_tol = tol[1]     
                    if min_tol == opt_tol:
                        continue
                    #选中new_mask_layer层对应于new_layer中该pad的开窗，获取其中点
                    layer_info.clear_select(job, step, new_mask_layer)
                    layer_info.set_selection(True, True, True, True, True, False)
                    layer_info.select_feature(job, step, new_mask_layer, select_poligon, {}, 1, False)
                    pt_list = layer_info.get_selected_pad_point(job, step, new_mask_layer)
                    if pt_list in feature_list:
                        continue
                    feature_list.append(pt_list)
                    if len(pt_list) == 1:
                        # if min_tol < opt_tol:
                        #     real_tol = analysis_dfm.get_selected_feature_min_spacing(job, step, new_mask_layer, opt_tol - min_tol)
                        #     feature_resize.resize_global(job, step, [new_mask_layer], 0, real_tol * 2)
                        # if min_tol > opt_tol:
                                #layer_info.select_feature(job, step, new_mask_layer, select_poligon, {}, 1, False)
                        #real_tol = analysis_dfm.get_selected_feature_min_spacing(job, step, new_mask_layer, opt_tol - min_tol)
                        #feature_resize.resize_global(job, step, [new_mask_layer], 0, real_tol * 2)
                        feature_resize.resize_global(job, step, [new_mask_layer], 0, (opt_tol - min_tol) * 2)
                        layer_info.clear_select(job, step, new_mask_layer)
                        layer_info.reset_selection()
                    if len(pt_list) > 1:
                        layer_info.clear_select(job, step, new_mask_layer)
                        layer_info.select_feature(job, step, new_layer, select_poligon, {}, 1, False)
                        #拷贝到临时层
                        layer_info.sel_copy_other(job, step, [new_layer], [tem_layer], False, 0, 0, 0, 0, 0, 0, 0)#
                        layer_info.select_feature(job, step, tem_layer, select_poligon, {}, 1, False)#
                        #layer_info.clear_select(job, step, new_layer)
                        feature_resize.resize_global(job, step, [tem_layer], 0, opt_tol * 2)
                        # layer_info.select_feature(job, step, new_layer, select_poligon, {}, 1, False)
                        # layer_info.sel_copy_other(job, step, [new_layer], [soldermask_layer], False, 0, 0, 0, 0, 0, 0, 0)
                        layer_info.clear_select(job, step, new_layer)
                        layer_info.reset_selection()
                #layer_info.select_features_by_attributes(job, step, [new_layer], 0, attribute_list)  #选中
                layer_info.clear_select(job, step, new_mask_layer)
                layer_info.sel_copy_other(job, step, [new_mask_layer], [soldermask_layer], False, 0, 0, 0, 0, 0, 0, 0)
                layer_info.sel_copy_other(job, step, [tem_layer], [soldermask_layer], False, 0, 0, 0, 0, 0, 0, 0)#
                #删除复制出的newlayer
                layer_info.reset_select_filter()
                layer_info.reset_selection()
                job_operation.delete_layer(job, new_layer)
                job_operation.delete_layer(job, new_mask_layer)
                job_operation.delete_layer(job, tem_layer)   #删除临时层
                layer_info.clear_select(job, step, outter_layer)
                layer_info.clear_select(job, step, soldermask_layer)
    except:
        print('clearance_resize_opt')
        
    

def cle_mintol_resize(job, step, smd_tol, pth_tol, bga_tol, outter_list):
    try:
        outter = layer_info.get_outter_list(job)
        soldermask_list = layer_info.get_soldermask_list(job)
        pad_attribute = [{".smd": ""}, {".bga": ""}, {".pth_pad": ""}]
        pad_tol = [smd_tol, bga_tol, pth_tol]
        outter_soldermask_pair = []        #存储两对外层防焊对
        for p in range(len(outter_list)):
            index = outter.index(outter_list[p])
            pair = [outter_list[index], soldermask_list[index]]
            outter_soldermask_pair.append(pair)
        # pair1 = [outter_list[0], soldermask_list[0]]
        # pair2 = [outter_list[1], soldermask_list[1]]
        # #outter_soldermask_pair.append(pair2)
        # outter_soldermask_pair.append(pair1)
        # outter_soldermask_pair.append(pair2)
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #在outter_layer中选中（bga/smd/pth）且含有cle属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            for j in range(len(pad_attribute)):
                attribute_list = [{".fiducial_name": "cle"}]
                attribute_list.append(pad_attribute[j])
                layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
                point_list = []
                point_list = layer_info.get_selected_pad_point(job, step, outter_layer)
                if point_list==[]:
                    continue
                #将选中的bga/smd/pth cle pad 拷贝到new_layer
                new_layer = outter_layer + '-copy'
                job_operation.create_layer(job, new_layer)
                layer_info.sel_copy_other(job, step, [outter_layer], [new_layer], False, 0, 0, 0, 0, 0, 0, 0)
               
                feature_resize.resize_global(job, step, [new_layer], 1, pad_tol[j] * 25400 * 2)
                layer_info.clear_select(job, step, new_layer)

                layer_info.sel_copy_other(job, step, [new_layer], [soldermask_layer], False, 0, 0, 0, 0, 0, 0, 0)
                #删除复制出的newlayer
                layer_info.reset_select_filter()
                job_operation.delete_layer(job, new_layer)
                layer_info.clear_select(job, step, outter_layer)
    except:
        print('cle_mintol_resize skip')

#gas处理至最小值
def gas_mintol_resize(job, step, smd_tol, bga_tol, outter_list):
    try:
        outter = layer_info.get_outter_list(job)
        soldermask_list = layer_info.get_soldermask_list(job)
        pad_attribute = [{".smd": ""}, {".bga": ""}]
        pad_tol = [smd_tol, bga_tol]
        outter_soldermask_pair = []        #存储两对外层防焊对
        for p in range(len(outter_list)):
            index = outter.index(outter_list[p])
            pair = [outter_list[index], soldermask_list[index]]
            outter_soldermask_pair.append(pair)
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #在outter_layer中选中（bga/smd）且含有gas属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            for j in range(len(pad_attribute)):
                attribute_list = [{".fiducial_name": "gas"}]
                attribute_list.append(pad_attribute[j])
                layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
                point_list = []
                point_list = layer_info.get_selected_pad_point(job, step, outter_layer)
                if point_list == []:
                    continue
                new_layer = outter_layer + '-copy'
                job_operation.create_layer(job, new_layer)
                layer_info.sel_move_other(job, step, [outter_layer], job, step, new_layer, False, 0, 0, 0, 0, 0, 0, 0)
                layer_info.clear_select(job, step, outter_layer)

                for k in range(len(point_list)):
                    select_polygon = [[point_list[k][0] - 1000, point_list[k][1] - 1000],
                                    [point_list[k][0] - 1000, point_list[k][1] + 1000],
                                    [point_list[k][0] + 1000, point_list[k][1] + 1000],
                                    [point_list[k][0] + 1000, point_list[k][1] - 1000],
                                    [point_list[k][0] - 1000, point_list[k][1] - 1000]]
                    #获取outter_layer中该pad与对应防焊层中开窗的最小公差
                    tol = []
                    tol = analysis_dfm.get_min_tolerance(job, step, new_layer, soldermask_layer, select_polygon)
                    if tol[0] == False:
                        continue
                    min_tol = abs(tol[1])                    
                    if min_tol >= pad_tol[j] * 25400:
                        continue
                    layer_info.select_feature(job, step, new_layer, select_polygon, {}, 0, False)
               
                    feature_resize.resize_global(job, step, [new_layer], 0, pad_tol[j] * 25400 * 2)
                    layer_info.clear_select(job, step, new_layer)

                layer_info.sel_move_other(job, step, [new_layer], job, step, outter_layer, False, 0, 0, 0, 0, 0, 0, 0)               
                #删除复制出的newlayer
                layer_info.reset_select_filter()
                job_operation.delete_layer(job, new_layer)
                layer_info.clear_select(job, step, outter_layer)
    except:
        print('cle_mintol_resize skip')

#新涨孔PAD
def outter_resize_drillpad(job, step, drillpad_min_size, outter_list, drill_name):
    try:
        drillpad_attribute = [".pth_pad", ".via_pad", ".npth_pad"]
        drill_attribute = [{".drill": "pth"}, {".drill": "via"}, {".drill": "npth"}]
        for k in range(0,len(outter_list)):
        #依据属性选中孔盘
        #move至新层
            for i in range(len(drillpad_attribute)):
                layer_info.clear_select(job, step, outter_list[k])
                attribute_list = [{drillpad_attribute[i]: ""}]
                layer_info.select_features_by_attributes(job, step, [outter_list[k]], 0, attribute_list)  #选中
                point_list = []
                point_list = layer_info.get_selected_pad_point(job, step, outter_list[k])
                if point_list == []:
                    continue
                new_inner_layer = outter_list[k] + '-copy'
                job_operation.create_layer(job, new_inner_layer)
                layer_info.sel_move_other(job, step, [outter_list[k]], job, step, new_inner_layer, False, 0, 0, 0, 0, 0, 0, 0)
                layer_info.clear_select(job, step, outter_list[k])
                #layer_info.sel_move_other(job, step, [inner_list[k]], new_inner_layer, False, 0, 0, 0, 0, 0, 0, 0)
                #依据新内层touch孔层
                layer_info.reset_select_filter()
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
                        if 0<tol[1]<(drillpad_min_size*25400):
                            size = (drillpad_min_size*25400 - tol[1])* 2
                            layer_info.select_feature(job, step, new_inner_layer, select_polygon, {}, 0, False)
                            feature_resize.resize_global(job, step, [new_inner_layer], 0, size)
                            layer_info.clear_select(job, step, new_inner_layer)
                #之后copy回原内层，删除新层
                layer_info.sel_move_other(job, step, [new_inner_layer], job, step, outter_list[k], False, 0, 0, 0, 0, 0, 0, 0)
                job_operation.delete_layer(job, new_inner_layer)
    except:
        print('outter_drillpad_resize skip')

def skylight_resize_opt(job, step, outter_list, soldermask_list, bga_or_smd, opt_tol, resize_delta):
    try:
        if len(outter_list) != len(soldermask_list):
            return
        outter_soldermask_pair = []
        for p in range(len(outter_list)):
            pair = [outter_list[p], soldermask_list[p]]
            outter_soldermask_pair.append(pair)
        layer_info.reset_select_filter()
        attribute_list = [{".fiducial_name": "sky"}]
        attribute_list.append(bga_or_smd)
        layer_info.reset_select_filter()
        for i in range(len(outter_soldermask_pair)):
            outter_layer = outter_soldermask_pair[i][0]
            soldermask_layer = outter_soldermask_pair[i][1]
            #在outter_layer中选中（bga/smd）且含有gas属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            layer_info.clear_select(job, step, outter_layer)
            layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
            #获取new_layer中每个pad的中心点
            point_list = []
            point_list = layer_info.get_selected_pad_point(job, step, outter_layer)
            #将开天窗pad拷贝至新层
            new_layer = outter_layer + '-skycopy'
            job_operation.create_layer(job, new_layer)
            layer_info.sel_copy_other(job, step, [outter_layer], [new_layer], False, 0, 0, 0, 0, 0, 0, 0)
            #在outter_layer中选中（bga/smd）且含有gas属性的pad，并获得该层pad的symbol信息（symbolname,size信息）
            layer_info.clear_select(job, step, outter_layer)
            layer_info.select_features_by_attributes(job, step, [outter_layer], 0, attribute_list)  #选中
            feature_list = []
            #将选中的bga/smd cle pad 拷贝到new_layer
            if len(point_list):
                for j in range(len(point_list)):
                    select_poligon = [[point_list[j][0] - 1, point_list[j][1] - 1],
                    [point_list[j][0] - 1, point_list[j][1] + 1],
                    [point_list[j][0] + 1, point_list[j][1] + 1],
                    [point_list[j][0] + 1, point_list[j][1] - 1],
                    [point_list[j][0] - 1, point_list[j][1] - 1]]
                    #选中soldermask_layer层对应于outter_layer中该pad的开窗，获取其中点
                    layer_info.clear_select(job, step, soldermask_layer)
                    layer_info.select_feature(job, step, soldermask_layer, select_poligon, {}, 0, False)
                    pt_list = layer_info.get_selected_pad_point(job, step, soldermask_layer)
                    if pt_list in feature_list:
                        continue
                    feature_list.append(pt_list)
                    feature_resize.resize_global(job, step, [soldermask_layer], 0, resize_delta)
                    #获取new_layer中该pad与对应防焊层中开窗的最小公差
                    tol = []
                    tol = analysis_dfm.get_min_tolerance(job, step, new_layer, soldermask_layer, select_poligon)
                    #min_tol = abs(tol[1]) 
                    min_tol = tol[1]     
                    if min_tol >= opt_tol:
                        continue
                    layer_info.select_feature(job, step, soldermask_layer, select_poligon, {}, 0, False)
                    feature_resize.resize_global(job, step, [soldermask_layer], 0, (opt_tol - min_tol) * 2)
                    layer_info.clear_select(job, step, soldermask_layer)
                #删除复制出的newlayer
                layer_info.reset_select_filter()
                job_operation.delete_layer(job, new_layer)
                layer_info.clear_select(job, step, outter_layer)
                layer_info.clear_select(job, step, soldermask_layer)
    except:
        print('clearance_resize_opt')

