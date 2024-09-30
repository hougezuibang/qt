import os,sys,time,shutil,re
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import job_operation
import epcam_api
import epcam as epcam
import layer_info
import feature_resize
import math

def is_orig(job):
    try: 
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        #job_operation.get_all_steps(job)
        for i in range(0, len(step_infos)):
            if step_infos[i] == 'orig':
                #print('true')
                return True
            else:
                #print('false')
                return False
    except Exception as e:
        print(e)
    return ''

def is_layer(job):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        if len(layer_list) == 0:
            #print('false')
            return False
        else:
            #print('true')
            return True
    except Exception as e:
        print(e)
    return ''

def is_net(job):
    try: 
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        #job_operation.get_all_steps(job)
        for i in range(0, len(step_infos)):
            if step_infos[i] == 'net':
                #print('true')
                return True
            else:
                #print('false')
                return False
    except Exception as e:
        print(e)
    return ''

def is_net(job):
    try: 
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        #job_operation.get_all_steps(job)
        for i in range(0, len(step_infos)):
            if step_infos[i] == 'prepare':
                #print('true')
                return True
            else:
                #print('false')
                return False
    except Exception as e:
        print(e)
    return ''

def copy_soldermask_to_silkscreen(job, step, size):
    try:
        solder_mask_list = layer_info.get_soldermask_list(job)
        layer_list = layer_info.get_silkscreen_layer(job)
        for i in range(0, len(solder_mask_list)):
            #新建空layer
            job_operation.create_layer(job, 'copy')
            sm_layer = solder_mask_list[i]
            layer_info.sel_copy_other(job, step, [sm_layer], ['copy'], 0, 0, 0, 
                0, 0, 0, 0, 0)
            layer_info.contourize(job, step, ['copy'], 6350, True, 76200, 0)
            feature_resize.resize_global(job, step, ['copy'], 1, size)            
            ss_layer=layer_list[i]
            layer_info.sel_copy_other(job, step, ['copy'], [ss_layer], 1, 0, 0, 
                0, 0, 0, 0, 0)
            #删除新层
            job_operation.delete_layer(job, 'copy')
    except Exception as e:
        print(e)
    return ''

def innerlayer_resize(job, step, linesize, surfacesize, pthsize, viasize, tdsize, inner_layer_list):
    try:
        linesize = linesize * 25400
        surfacesize = surfacesize * 25400
        pthsize = pthsize * 25400
        viasize = viasize * 25400
        tdsize = tdsize * 25400
        #inner_layer_list = layer_info.get_inner_layer_list(job)
        #蚀刻补偿line
        if(linesize!=0):
            #清空筛选
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(0, [{".fiducial_name": "trace"}])
            layer_info.select_features_by_featuretype(job, step, inner_layer_list, 127)
            feature_resize.resize_global(job, step, inner_layer_list, 0, linesize)
        #蚀刻补偿泪滴
        if(tdsize!=0):
            #清空筛选
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".tear_drop": ""}])
            layer_info.select_features_by_featuretype(job, step, inner_layer_list, 127)
            feature_resize.resize_global(job, step, inner_layer_list, 0, tdsize)
        #蚀刻补偿surface
        if(surfacesize!=0):
            #清空筛选
            layer_info.reset_select_filter()   
            layer_info.set_attribute_filter(1, [{".pattern_fill": ""}])
            layer_info.select_features_by_featuretype(job, step, inner_layer_list, 127)
            feature_resize.resize_global(job, step, inner_layer_list, 0, surfacesize)
        #蚀刻补偿pth
        if(pthsize!=0):
            layer_info.reset_select_filter()   
            layer_info.set_attribute_filter(1, [{".pth_pad": ""}])
            layer_info.select_features_by_featuretype(job, step, inner_layer_list, 127)
            feature_resize.resize_global(job, step, inner_layer_list, 0, pthsize)    
        #蚀刻补偿via
        if(viasize!=0):
            layer_info.reset_select_filter()   
            layer_info.set_attribute_filter(1, [{".via_pad": ""}])
            layer_info.select_features_by_featuretype(job, step, inner_layer_list, 127)
            feature_resize.resize_global(job, step, inner_layer_list, 0, viasize)    
        # data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":'l1'}
        # js = json.dumps(data2)
        # epcam.view_cmd(js)
    except Exception as e:
        print(e)

def outterlayer_resize(job, step, less, compensate, linesize, surfacesize, smdsize, bgasize, marksize, pthsize, viasize, tdsize):
    try:
        linesize = linesize * 25400
        surfacesize = surfacesize * 25400
        smdsize = smdsize * 25400
        bgasize = bgasize * 25400
        marksize = marksize * 25400
        pthsize = pthsize * 25400
        viasize = viasize * 25400
        tdsize = tdsize * 25400
        outter_layer_list = layer_info.get_outter_list(job)
        #蚀刻补偿line
        if(linesize != 0):
            #清空筛选
            layer_info.reset_select_filter()   
            layer_info.set_attribute_filter(0, [{".fiducial_name": "trace"}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, linesize)
        #蚀刻补偿泪滴
        if(tdsize!=0):
            #清空筛选
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".tear_drop": ""}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, tdsize)
        #蚀刻补偿surface
        if(surfacesize != 0):
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".pattern_fill": ""}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, surfacesize)
        #蚀刻补偿smd
        if smdsize != 0 or compensate != 0:
            for _layer in outter_layer_list:
                layer_info.reset_select_filter()
                layer_info.set_attribute_filter(1, [{".smd": ""}])
                layer_info.select_features_by_filter(job, step, [_layer])

                ret = epcam_api.get_selected_feature_infos(job, step, _layer)    #获取所有smd的信息
                info_list = json.loads(ret)
                layer_info.reset_select_filter()
                layer_info.clear_select(job, step, _layer)  #清除选中并对每一个smd进行选中判断  
                if info_list["paras"] == False:
                    continue   
                if len(info_list["paras"]):
                    for _point in info_list["paras"]:                       
                        epcam_api.select_feature_by_id(job, step, _layer, [_point['feature_index']])
                        infos = layer_info.get_smd_or_bga_symbolname(job, step, _layer)
                        resize_size = 0
                        if len(infos):
                            if less > 0 and infos[0][1] <= less:
                                resize_size = smdsize + compensate
                            elif infos[0][1] > less:
                                resize_size = smdsize
                            feature_resize.resize_global(job, step, [_layer], 0, resize_size)
                        layer_info.clear_select(job, step, _layer)

        #蚀刻补偿bga
        if bgasize != 0 or compensate != 0:
            for _layer in outter_layer_list:
                layer_info.reset_select_filter()
                layer_info.set_attribute_filter(1, [{".bga": ""}])
                layer_info.select_features_by_filter(job, step, [_layer])
                ret = epcam_api.get_selected_feature_infos(job, step, _layer)    #获取所有smd的信息
                info_list = json.loads(ret)
                layer_info.reset_select_filter()
                layer_info.clear_select(job, step, _layer)   
                if info_list["paras"] == False:
                    continue                    #清除选中并对每一个smd进行选中判断
                if len(info_list["paras"]):
                    for _point in info_list["paras"]:                       
                        epcam_api.select_feature_by_id(job, step, _layer, [_point['feature_index']])
                        infos = layer_info.get_smd_or_bga_symbolname(job, step, _layer)
                        resize_size = 0
                        if len(infos):
                            if less > 0 and infos[0][1] <= less:
                                resize_size = bgasize + compensate
                            elif infos[0][1] > less:
                                resize_size = bgasize
                            feature_resize.resize_global(job, step, [_layer], 0, resize_size)
                        layer_info.clear_select(job, step, _layer)
        #蚀刻补偿mark
        if(marksize != 0):
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".fiducial_mark": ""}, {".fiducial_name": "mark"}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, marksize)
        #蚀刻补偿pth
        if(pthsize != 0):
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".pth_pad": ""}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, pthsize)
        #蚀刻补偿via
        if(viasize != 0):
            layer_info.reset_select_filter()
            layer_info.set_attribute_filter(1, [{".via_pad": ""}])
            layer_info.select_features_by_featuretype(job, step, outter_layer_list, 127)
            feature_resize.resize_global(job, step, outter_layer_list, 0, viasize)
        # data2 = {"cmd":"show_layer", "job":job, "step": step, "layer":'l1'}
        # js = json.dumps(data2)
        # epcam.view_cmd(js)
    except Exception as e:
        print(e)

#比对drillmap添加槽孔
def add_drill_by_drillmap(job, step):
    layer_info.reset_select_filter()
    #判断drillmap是否存在，不存在则不执行此功能
    all_layer = layer_info.get_all_layer_name(job)
    if 'drillmap' not in all_layer:
        return
    signal_layers = layer_info.get_signal_layer_list(job)
    drill_layer = 'drl1-' + str(len(signal_layers))
    if drill_layer not in all_layer:
        return
    #复制drillmap
    drill_layer_save = job_operation.copy_layer(job, drill_layer)
    job_operation.rename_layer(job, drill_layer_save, drill_layer + '_1', 'misc')  
    new_layer = job_operation.copy_layer(job, 'drillmap')
    layer_info.clip_area_use_profile(job, step, [new_layer], False, False, 0, 127)    #删除复制出来的drillmap的板外资料
    #将drillmap层所有的outline转成pad
    layer_info.set_featuretype_filter(70)    #选中所有line和arc
    layer_info.select_features_by_filter(job, step, [new_layer])
    line_infos = layer_info.get_features_infos(job, step, new_layer)
    layer_info.clear_select(job, step, new_layer)                            
    line_list = []
    #遍历所有线和弧获得symbolname
    for _line in line_infos:
        if _line[2] in line_list:
            continue         
        line_list.append(_line[2])
    for line_name in line_list:     
        layer_info.reset_select_filter()
        layer_info.set_featuretype_filter(70)           #选中所有line和arc                     
        layer_info.set_include_symbol_filter([line_name])    
        layer_info.select_features_by_filter(job, step, [new_layer])
        epcam_api.outline2surface(job, step, [new_layer], True)
        epcam_api.contour2pad(job, step, [new_layer], 0, 0, 9999*25400, '+surface')
        job_operation.delete_layer(job, new_layer+'+surface')
        layer_info.clear_select(job, step, new_layer)
    #选中所有feature
    layer_info.reset_select_filter()
    layer_info.set_featuretype_filter(127)    #选中所有feature
    layer_info.select_features_by_filter(job, step, [new_layer])
    feature_infos = layer_info.get_features_infos(job, step, new_layer) 
    symbol_list = []                   #当前层的所有symbolname下的symbol信息      
    for _info in feature_infos:
        if _info in symbol_list:
            continue
        symbol_list.append(_info)
        # if math.fabs(_info[12] - _info[13]) > 2540 :           
        #     symbol_list.append(_info)
    layer_info.clear_select(job, step, new_layer)
    layer_info.reset_select_filter()

    for _symbol in symbol_list:                     #遍历用每一个symbol的坐标去通孔层找feature,找不到则添加
        #epcam_api.select_feature_by_id(job, step, new_layer, [_symbol[10]])
        x_min = _symbol[0] - _symbol[12] / 2
        x_max = _symbol[0] + _symbol[12] / 2
        y_min = _symbol[1] - _symbol[13] / 2
        y_max = _symbol[1] + _symbol[13] / 2
        select_poligon = [[x_min, y_min], 
                         [x_min, y_max], 
                         [x_max, y_max], 
                         [x_max, y_min], 
                         [x_min, y_min]]                                      #选框的box
        layer_info.select_feature(job, step, drill_layer, select_poligon, {}, 1, False)
        ret = epcam_api.get_selected_features_box(job, step, [drill_layer])   #获取选中feature的box
        layer_info.clear_select(job, step, drill_layer)                       #清除两层选中
        data = json.loads(ret)
        _box_xmin = data['xmin']
        _box_ymin = data['ymin']
        _box_xmax = data['xmax']
        _box_ymax = data['ymax']
        if _box_xmax != 0 or _box_ymax != 0:
            continue
        pad_name = ''
        if _symbol[12] / _symbol[13] >= 0.9 and _symbol[12] / _symbol[13] <= 1.1:
            pad_name = 'r' + str(round(_symbol[12]/25400, 2))
        else:
            pad_name = 'oval' + str(round(_symbol[12]/25400, 2)) + 'x' + str(round(_symbol[13]/25400, 2))

        if _symbol[0] == 0 and _symbol[1] == 0:
            xxx = 123
        epcam_api.add_pad(job, step, [], drill_layer, pad_name, _symbol[0], _symbol[1], 1, 0, 0, [])
    job_operation.delete_layer(job, new_layer)
        
#正负片合并
def pos_and_neg_merge(job, step, layers):
    for _layer in layers:
        layer_info.reset_select_filter()
        layer_info.set_featuretype_filter(63)    #先选中负的所有feature
        layer_info.select_features_by_filter(job, step, [_layer])
        layer_info.reset_select_filter()
        layer_info.set_featuretype_filter(72)    #再选中正的所有surface
        layer_info.select_features_by_filter(job, step, [_layer])  
        select_infos = layer_info.get_features_infos(job, step, _layer)  #获取选中信息 如果为空 则跳过
        if len(select_infos) == 0:
            continue
        layer_info.contourize(job, step, [_layer], 0, True, 76200, 0)
        layer_info.reset_select_filter()
        layer_info.clear_select(job, step, _layer)

#前处理步骤
def prepare_operation(job, step):
    #删除板外资料(锡膏层不要删)
    layer_list = []
    drill_list = []
    signal_list = []
    all_list = []
    ret = epcam_api.get_graphic(job)
    data = json.loads(ret)
    _layer_info = data['paras']['info']
    for _info in _layer_info:
        if _info['context'] == 'board':
            if _info['type'] != 'solder_paste':
                layer_list.append(_info['name'])
            if _info['type'] == 'drill':
                drill_list.append(_info['name'])
            if _info['type'] == 'signal':
                signal_list.append(_info['name'])
        all_list.append(_info['name'])
    layer_info.clip_area_use_profile(job, step, layer_list, False, False, 0, 127)
    if 'outline' in all_list:
        layer_info.clip_area_use_profile(job, step, 'outline', False, False, 127000, 127)
    #正负片整合
    pos_and_neg_merge(job, step, layer_list)
    #比对drillmap添加槽孔
    add_drill_by_drillmap(job, step)
    #surface转pad
    epcam_api.contour2pad(job, step, drill_list, 0, 1, 9999 * 25400, '+++')
    all_layer_list = []            #所有层名
    all_layer_list = layer_info.get_all_layer_name(job)
    for _drill in drill_list:
        _drill_name = _drill + '+++'
        if _drill_name in all_layer_list:
            job_operation.delete_layer(job, _drill_name)      
    #自动定属性(net孔)
    epcam_api.auto_classify_attribute(job, step, drill_list)

#前处理全流程
def all_prepare(job):
    step = 'pre'
    steplist = job_operation.get_all_steps(job)
    layer_list = job_operation.get_all_layers(job)
    while 'net' not in steplist:
        datashow = {"cmd":"show_layer", "job":job, "step": steplist[0], "layer":layer_list[0]}
        js = json.dumps(datashow)
        epcam.view_cmd(js)
        steplist = job_operation.get_all_steps(job)                  #net前的处理

    prepare_operation(job, 'net')                                    #处理net
        
    steplist = job_operation.get_all_steps(job)
    layer_list = job_operation.get_all_layers(job)
    while step not in steplist:
        datashow = {"cmd":"show_layer", "job":job, "step": 'net', "layer":layer_list[0]}
        js = json.dumps(datashow)
        epcam.view_cmd(js)
        steplist = job_operation.get_all_steps(job)                  #prepare前的处理

    all_layer_list = []            #所有层名
    all_layer_list = layer_info.get_all_layer_name(job)
    signal_layer = []                                    #所有线路层名，用于计算通孔层名
    signal_layer = layer_info.get_signal_layer_list(job)
    drill_layer = 'drl1-' + str(len(signal_layer))
    drill_layer_save = drill_layer + '_1'
    if  drill_layer_save in all_layer_list:
        job_operation.delete_layer(job, drill_layer_save)      
    epcam_api.auto_classify_attribute(job, step, signal_layer)     #prepare线路层定属性

    #前处理最后的show
    datashow = {"cmd":"show_layer", "job":job, "step": step, "layer":layer_list[0]}
    js = json.dumps(datashow)
    epcam.view_cmd(js)

def import_multigerber(jobname,gerberpath,outpath):
    job=jobname
    path=outpath
    if os.path.exists(os.path.join(path,job)):
        shutil.rmtree(os.path.join(path,job))
    epcam_api.create_job(path, job)
    gerbepath=gerberpath
    gerbename=os.path.basename(gerbepath)
    dd=str(int(time.time()))+'zw'
    copypath=os.path.join(path,dd)
    shutil.copytree(gerbepath,copypath)
    aaa=os.listdir(copypath)
    index11=0
    for step in aaa:
        job_operation.create_step(job,step)
        job_operation.save_job(job)
        file_path=os.path.join(copypath,step)
        filedir=os.listdir(file_path)
        signum=0
        for layer in filedir:
            if 'conductor' in layer:
                signum=signum+1
        for layer in filedir:
            if 'pastemask' in layer and 'bottom' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'spb')
            elif 'pastemask' in layer and 'top' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'spt')
            elif 'np' in layer and 'drilling' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'np')
            elif 'np' not in layer and 'drilling' in layer:
                layname=layer.split('_')[2]
                os.rename(file_path+r'/'+layer,file_path+r'/'+'drl'+layname)
            elif 'conductor' in layer and 'top' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'l1')
            elif 'conductor' in layer and 'bottom' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'l'+str(signum))
            elif 'via' in layer and 'top' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'via1')
            elif 'via' in layer and 'bottom' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'via2')
            elif 'milling' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'slot')
            elif 'outline' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'outline')
            elif 'silkscreen' in layer and 'top' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'sst')
            elif 'silkscreen' in layer and 'bottom' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'ssb')
            elif 'soldermask' in layer and 'bottom' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'smb')
            elif 'soldermask' in layer and 'top' in layer:
                os.rename(file_path+r'/'+layer,file_path+r'/'+'smt')
        index =1
        job_operation.Traverse_Gerber(job, step, file_path,index)
        index11=index
        job_operation.save_job(job)
    shutil.rmtree(copypath)
    all_layer=layer_info.get_all_layer_name(job)
    numsig=0
    numdrl=0
    for layer in all_layer:
        if len(layer)>=3:
            if layer[0:3]=='smt':
                layer_info.change_layer_matrix(job, layer, 'board','solder_mask','smt')
            elif layer[0:3]=='smb':
                layer_info.change_layer_matrix(job, layer, 'board','solder_mask','smb')
            elif layer[0:3]=='drl':
                layname=layer.split('.')[0]
                layer_info.change_layer_matrix(job, layer, 'board','drill',layname)  
                numdrl=numdrl+1
            elif layer[0:3]=='sst':
                layer_info.change_layer_matrix(job, layer, 'board','silk_screen','sst')  
            elif layer[0:3]=='ssb':
                layer_info.change_layer_matrix(job, layer, 'board','silk_screen','ssb') 
            elif layer[0:3]=='spt':
                layer_info.change_layer_matrix(job, layer, 'board','solder_paste','spt') 
            elif layer[0:3]=='spb':
                layer_info.change_layer_matrix(job, layer, 'board','solder_paste','spb') 
            elif layer[0:1]=='l':
                num=re.match('l([0-9]+)[\a]*',layer)
                if num:
                    layname=layer.split('.')[0]
                    layname=layname.split('-')[0]
                    layname=layname.split('_')[0]
                    layer_info.change_layer_matrix(job, layer, 'board','signal',layname)
                    numsig=numsig+1
        elif len(layer)==2:
            if(layer[0:1]=='l'):
                num=re.match('l([0-9]+)[\a]*',layer)
                if num:
                    layname=layer
                    layer_info.change_layer_matrix(job, layer, 'board','signal',layname)
                    numsig=numsig+1
    
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    i=1
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='spt':
                src=_info['row']
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='sst':
                src=_info['row']
                # _info['row']=i
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='smt':
                src=_info['row']
                # layer_info['row']=i
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    for j in range(numsig):
        for _info in layer_infos:
            if _info['name']=='l'+str(j+1):
                src=_info['row']
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='smb':
                src=_info['row']
                # layer_info['row']=i
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='ssb':
                src=_info['row']
                # _info['row']=i
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']
    for _info in layer_infos:
        if len(_info['name'])>=3:
            if _info['name'][0:3]=='spb':
                src=_info['row']
                # layer_info['row']=i
                epcam_api.move_layer(job,src,i)
                i=i+1
                break
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_infos = data['paras']['info']

    for j in range(len(layer_infos)):
        if layer_infos[j]['context']=='board' and layer_infos[j]['type']=='drill':
            src=layer_infos[j]['row']
            # layer_info['row']=i
            epcam_api.move_layer(job,src,i)
            ret = epcam_api.get_matrix(job)
            data = json.loads(ret)
            layer_infos = data['paras']['info']
            i=i+1
    
    aaa=os.listdir(gerbepath)
    for step in aaa:
        file_path=os.path.join(gerbepath,step)
        job_operation.Traverse_Gerber(job, step, file_path,index11)
    job_operation.save_job(job)