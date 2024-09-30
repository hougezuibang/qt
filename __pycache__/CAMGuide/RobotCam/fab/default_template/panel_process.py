import os, sys, json
PyRecipe_fab_default_template_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
PyRecipe_module_panel_path = os.path.dirname(PyRecipe_base_path) + r'\module\panel'
sys.path.append(PyRecipe_module_panel_path)
import epcam
import epcam_api
import layer_info
import job_input
import panel_create
import panel_joint
import drill_process
import analysis_dfm
import job_operation
import functools

def array_process_joint(job, step, profile_x, profile_y, childsteps, layername, keep_x, keep_y):
    #创建拼板的step
    panel_create.create_step(job, step, 0, 0, profile_x, profile_y)
    #拼板
    panel_joint.step_joint(job, step, childsteps, layername)

def panel_process_joint(job, step, profile_x, profile_y, childsteps, layername, keep_x, keep_y, out_x, out_y):
    #创建拼板的step
    panel_create.create_step(job, step, 0, 0, profile_x, profile_y)
    #拼板
    panel_joint.step_joint(job, step, childsteps, layername)
    #panel向外铺铜
    panel_create.paveCu_outward(job, step, 0, 0, profile_x, profile_y, out_x, out_y)

#set流程
def set_process(job, step, params):
    #***************************参数提取**************************
    setParams = params['panel']['set_params']
    #拼板参数
    #set_width = setParams['sizeX'] * 25400              #set宽
    #set_height = setParams['sizeY'] * 25400             #set高
    #set的宽和高为org的宽高
    #工艺边参数（用来判断拼板方式）
    keep_left = setParams['sideLeft'] * 25400           #工艺边左
    keep_right = setParams['sideRight'] * 25400         #工艺边右        
    keep_top = setParams['sideUp'] * 25400              #工艺边上             
    keep_bottom = setParams['sideDown'] * 25400         #工艺边下
    set_type = 0                                        #拼板方式, 0为有set_outline, 1为需要自己建set_outline
    if keep_left == 0 and keep_right == 0:
        if keep_top == 0 and keep_bottom == 0:
            set_type = 0
        else:
            set_type = 1
    else:
        set_type = 1
    ##############################
    set_nx = setParams['numberX']                              #x方向pcs数量
    set_ny = setParams['numberY']                              #y方向pcs数量
    pcs_data = epcam_api.get_profile_box(job, 'pcs')           #pcs的宽高
    pcs_data = json.loads(pcs_data)
    pcs_width = pcs_data['paras']['Xmax'] - pcs_data['paras']['Xmin'] 
    pcs_height = pcs_data['paras']['Ymax'] - pcs_data['paras']['Ymin']
    space_x = setParams['spacingX'] * 25400      #x方向pcs间距，不同边
    space_y = setParams['spacingY'] * 25400      #y方向pcs间距，不同边
    set_dx = space_x + pcs_width         #x方向pcs间距,同边
    set_dy = space_y + pcs_height        #y方向pcs间距,同边
    if set_type == 0:
        org_box = layer_info.get_profile_box(job, 'org')
        set_width = org_box[0] 
        set_height = org_box[1]
    else:
        set_width = keep_left + keep_right + set_nx * (pcs_width + space_x) - space_x
        set_height = keep_top + keep_bottom + set_ny * (pcs_height + space_y) - space_y
    #拼板参数字典
    set_params = {"width":set_width, "height":set_height, "nx":set_nx, "ny":set_ny, "dx":set_dx, "dy":set_dy, 
                  "space_x":space_x, "space_y":space_y }
    #工艺边参数
    #通过获取pcs的datum点位置和profile的box来计算
    pcs_step_data = epcam_api.get_step_header_infos(job, 'pcs')    
    pcs_step_data = json.loads(pcs_step_data)  #pcs step的基本参数
    datum_x = pcs_step_data['x_datum']
    datum_y = pcs_step_data['y_datum']
    if set_type == 0:
        if keep_left == 0 and keep_right == 0:
            keep_left = pcs_data['paras']['Xmin'] - datum_x
            keep_right = set_width - keep_left - (set_nx * (pcs_width + space_x) - space_x)
            if keep_left <= 25400:
                keep_left = 0
            if keep_right <= 25400:
                keep_right = 0
        if keep_top == 0 and keep_bottom == 0:  
            keep_bottom = pcs_data['paras']['Ymin'] - datum_y 
            keep_top = set_height - keep_bottom - (set_ny * (pcs_height + space_y) - space_y) 
            if keep_top <= 25400:
                keep_top = 0
            if keep_bottom <= 25400:
                keep_bottom = 0
    #工艺边参数字典
    keep_params = {"left":keep_left, "right":keep_right, "top":keep_top, "bottom":keep_bottom}
    #铺铜
    profile_resize = setParams['profileExtend'] * 25400                #外扩
    child_profile_resize = setParams['childProfileExtend'] * 25400     #子profile外扩
    avoid_drill_size = setParams['avoidDrillSize'] * 25400             #避孔值
    copper_layers = setParams['bigCuLayer']                                   #铺铜皮的层
    #铜皮参数
    copper_params = {'profile_resize':profile_resize, 'child_profile_resize':child_profile_resize, 'copper_layers':copper_layers,
                     'avoid_drill_size':avoid_drill_size} 
    copper_pad_name = setParams['dummyPadSymbol']                       #铜点的symbolname
    copper_pad_dx = setParams['dummyPadDx'] * 25400              #铜点的dx
    copper_pad_dy = setParams['dummyPadDy'] * 25400              #铜点的dy
    copper_pad_layers = setParams['DummyCuLayer']                         #铺铜点的层
    #铜点参数
    copper_pad_params = {'copper_pad_name':copper_pad_name, 'copper_pad_dx':copper_pad_dx, 'copper_pad_dy':copper_pad_dy,
                             'copper_pad_layers':copper_pad_layers} 
    #铺铜参数
    fill_profile_params = {'copper_params':copper_params, 'copper_pad_params':copper_pad_params}
    #定位孔参数
    drill_flag = setParams['AddToolingHole']                         #是否添加定位孔
    drill_size = setParams['sizeToolingHole'] * 25400                #定位孔尺寸(mil)
    drill_sm_size = setParams['winToolingHole'] * 25400              #定位孔开窗尺寸(mil)
    drill_x1 = setParams['LeftUpX1'] * 25400                  #左上
    drill_y1 = setParams['LeftUpY1'] * 25400
    drill_center1 = setParams['LeftUpCenter']
    drill_x2 = setParams['RightUpX2'] * 25400                 #右上
    drill_y2 = setParams['RightUpY2'] * 25400
    drill_center2 = setParams['RightUpCenter']
    drill_x3 = setParams['LeftDownX3'] * 25400                #左下
    drill_y3 = setParams['LeftDownY3'] * 25400
    drill_center3 = setParams['LeftDownCenter']
    drill_x4 = setParams['RightDownX4'] * 25400              #右下
    drill_y4 = setParams['RightDownY4'] * 25400               #四个定位孔的坐标
    drill_center4 = setParams['RightDownCenter']
    #定位孔的坐标参数
    drill_points = {"x1":drill_x1, "y1":drill_y1, "x2":drill_x2, "y2":drill_y2, "x3":drill_x3, "y3":drill_y3, 
                    "x4":drill_x4, "y4":drill_y4, "center1":drill_center1, "center2":drill_center2, 
                    "center3":drill_center3, "center4":drill_center4}
    #光学点
    mark_flag = setParams['AddFdMark']
    FdMarkCenter = setParams['FdMarkCenter']                         #光学点居中
    mark_ring_flag = setParams['AddFdMarkRing']
    mark_size = setParams['sizeFdMark'] * 25400                      #光学点尺寸
    mark_sm_size = setParams['winFdMark'] * 25400                    #光学点开窗尺寸
    mark2drill = setParams['FdMarkToHole'] * 25400            #光学点距孔（正数在里面， 负数在外面）
    mark2keep = setParams['FdMarkToPrcessEdge'] * 25400       #光学点距工艺内边
    mark_ring_type = setParams['typeFdMarkRing']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 #光学点保护环类型
    mark_outter_ring = setParams['outSizeFdMarkRing'] * 25400        #光学点保护环外环尺寸
    mark_inner_ring = setParams['innerSizeFdMarkRing'] * 25400       #光学点保护环内环尺寸
    v_test_flag = setParams['addVtest']                               #添加v_cut测点
    #光学点参数字典
    mark_params = {"mark_size":mark_size, "mark_sm_size":mark_sm_size, "mark2drill":mark2drill, "mark2keep":mark2keep,
                   "mark_ring_type":mark_ring_type, "mark_outter_ring":mark_outter_ring, "mark_inner_ring":mark_inner_ring,
                   "mark_flag":mark_flag, "mark_ring_flag":mark_ring_flag, "v_test_flag":v_test_flag, "FdMarkCenter":FdMarkCenter}
    #文字测点
    text_test_flag = setParams['addTextTest']    
    #添加厂编
    factory_num_flag = setParams['AddFactoryNumber']   
    factory_layer = setParams['layerFactoryNumber']     
    #************************************************************
    #判断set是否存在, 不在则创建
    step_list = job_operation.get_all_steps(job)
    if not 'set' in step_list:
        job_operation.create_step(job, 'set')
    #添加usersymbol
    add_usersymbol(job, step, v_test_flag, text_test_flag)
    #创建set的profile线
    #拼板
    set_function(job, step, params, keep_params, set_params, set_type, datum_x, datum_y)
    #去除板外杂物
    layers = layer_info.get_all_layer_name(job)
    layer_info.clip_area_use_profile(job, step, layers, False, False, 254000, 127)    #margin默认为10mil
    #如果原稿存在定位孔, 获取其参数
    if not drill_flag:
        drill_infos = get_drill_points(job, step)
        drill_points = drill_infos['drill_points']
        drill_size = drill_infos['size']
    #添加定位孔, 并添加开窗, 添加辅助孔并添加开窗
    add_locating_drill(job, step, drill_size, drill_sm_size, drill_points, set_params, keep_params, drill_flag)          #已测
    #添加尖角孔并添加开窗
    #add_sharp_corner_drill(job, step, params)
    #添加邮票孔
    #钻孔补偿
    drill_operation(job, step, params)  #辅助孔开窗暂时没加 (已测)
    #添加npth的辅助孔在防焊层的开窗
    #删除touch到npth孔在外层的pad
    delete_outter_touch_npth_pad(job, step)           #(已测)
    #内外层添加铜（铜皮, 铜点, 网铜）并避开相关物件
    signal_layer_fill_profile(job, step, fill_profile_params)
    #添加内层流胶条
    add_inner_flow_tape(job, step, keep_params, set_params)      #已测
    #添加光学点, 光学点保护圈, 光学点开窗, 光学点下避铜
    add_mark_points(job, step, keep_params, mark_params, drill_points, set_params, params)   #已测
    #删除多余铜点
    delete_touch_dummy_pad(job, step, copper_pad_layers, copper_pad_name)
    #外层补偿（使用pcs的外层补偿参数）
    outter_resize(job, step, params)                            #已测
    #添加本厂料号名
    if factory_num_flag:
        add_job_text(job, step, keep_params, set_params, factory_layer)             #已测
    #防焊添加成型v-cut线
    add_v_cut_sm(job, step, params, set_params, keep_params, set_type)
    #outline整理，自动整理外形线
    #直角导圆角
    #锣刀
    #避npth, profile, rout, v-cut
    avoid_cu(job, step, params)                                  #已测
    #添加文字测点 
    if v_test_flag:
        add_text_pad(job, step, keep_params, set_params)             #已测
    #添加v_cut测点
    if v_test_flag:
        add_v_pad_2(job, step, keep_params, set_params, mark_outter_ring, drill_points, mark_params)

#外层补偿
def outter_resize(job, step, params):
    smdbga_less = params['outter']['smdbga_less']
    smdbga_compensate = params['outter']['smdbga_compensate']
    line_resize = params['outter']['line_size']
    surface_resize = params['outter']['surface_size']
    smd_resize = params['outter']['smd_size']
    bga_resize = params['outter']['bga_size']
    mark_resize = params['outter']['mark_size']
    pthsize = params['outter']['drillpad_pth']
    viasize = params['outter']['drillpad_via']
    tdsize = params['outter']['TDResize_outter']
    job_input.outterlayer_resize(job, step, smdbga_less, smdbga_compensate, line_resize, surface_resize, smd_resize, bga_resize, mark_resize, pthsize, viasize, tdsize)

#删除touch到npth孔在外层的pad
def delete_outter_touch_npth_pad(job, step):
    drill_layers = layer_info.get_drill_layer_name(job)
    outter_layers = layer_info.get_outter_list(job)
    for outter_layer in outter_layers:
        #先清空该层选中和筛选条件
        layer_info.reset_select_filter()
        layer_info.clear_select(job, step, outter_layer)    
        # #选中该层的所有npth孔
        # layer_info.set_featuretype_filter(65)
        # layer_info.set_attribute_filter(0, [{".drill": "non_plated"}])
        # epcam_api.select_features_by_filter(job, step, [drill_layer])
        #用外层touch npth孔, 来选中
        epcam_api.filter_by_mode(job, step, outter_layer, drill_layers, 0, 65, 0 , [{".drill": "non_plated"}])
        #layer_info.clear_select(job, step, outter_layer) 
        layerInfos = layer_info.get_selected_features_infos(job, step, outter_layer)  
        if len(layerInfos) > 0:
            layer_info.delete_feature(job, step, [outter_layer])

#删除负片touch到的铜洞
def delete_touch_dummy_pad(job, step, layers, symbolname):
    for layer in  layers:
        #先清空筛选和选中
        layer_info.clear_select(job, step, layer)     
        layer_info.reset_select_filter()
        #设置feature筛选
        #选中该层的所有负片
        layer_info.set_featuretype_filter(63)
        epcam_api.select_features_by_filter(job, step, [layer])
        #拷贝至新建临时层
        layer_copy = layer + '_copy'
        job_operation.create_layer(job, layer_copy)
        epcam_api.sel_copy_other(job, step, [layer], [layer_copy], True, 0, 0, False, 0, 0, 0, 0)
        #清空筛选和选中
        layer_info.clear_select(job, step, layer)     
        layer_info.reset_select_filter()
        #设置symbolname和属性筛选
        layer_info.set_include_symbol_filter([symbolname])
        layer_info.set_attribute_filter(0, [{'.pattern_fill':''}])
        epcam_api.filter_by_mode(job, step, layer, [layer_copy], 0, 127, -1, [], -1, 0, [])
        layerInfos = layer_info.get_selected_features_infos(job, step, layer)  
        if len(layerInfos) > 0:
            layer_info.delete_feature(job, step, [layer])
        job_operation.delete_layer(job, layer_copy)
                #清空筛选和选中
        layer_info.clear_select(job, step, layer)     
        layer_info.reset_select_filter()

#内外层添加铜（铜皮, 铜点, 网铜）
def signal_layer_fill_profile(job, step, fill_profile_params):
    #将外层物件移到外层备份层
    outter_layers = layer_info.get_outter_list(job)
    for outter_layer in outter_layers:
        outter_save = outter_layer + '_save'
        job_operation.create_layer(job, outter_save)
        layer_info.clear_select(job, step, outter_layer)          #先清空选中
        epcam_api.sel_copy_other(job, step, [outter_layer], [outter_save], False, 0, 0, 
                    False, 0, 0, 0, 0)
    #铺铜皮
    copper_params = fill_profile_params['copper_params']
    copper_layers = copper_params['copper_layers']
    profile_resize = copper_params['profile_resize']             
    child_profile_resize = copper_params['child_profile_resize']
    avoid_drill_size = copper_params['avoid_drill_size']
    for copper_layer in copper_layers:  
        epcam_api.fill_profile(job, step, copper_layer, profile_resize, child_profile_resize, avoid_drill_size, False, '', 0, 0)
    #铺铜点
    copper_pad_params = fill_profile_params['copper_pad_params']
    copper_pad_name = copper_pad_params['copper_pad_name']             #铜点的symbolname
    copper_pad_dx = copper_pad_params['copper_pad_dx']                 #铜点的dx
    copper_pad_dy = copper_pad_params['copper_pad_dy']                 #铜点的dy
    copper_pad_layers = copper_pad_params['copper_pad_layers']         #铺铜点的层
    for copper_pad_layer in copper_pad_layers:  
        epcam_api.fill_profile(job, step, copper_pad_layer, profile_resize, child_profile_resize, True, True, copper_pad_name, 
                                copper_pad_dx, copper_pad_dy)

#添加定位孔, 并添加开窗, 添加辅助孔并添加开窗
def add_locating_drill(job, step, drill_size, drill_sm_size, drill_points, set_params, keep_params, drill_flag):
    #拼板, 工艺边参数
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    #判断在x方向还是y方向添加流胶条
    direction_type = 0      #0:x方向, 1:y方向
    if keep_left == 0 or keep_right == 0:
        direction_type = 1
    else:
        direction_type = 0
    #定位孔孔参数
    drill_x1 = drill_points["x1"]
    drill_x2 = drill_points["x2"]
    drill_x3 = drill_points["x3"]
    drill_x4 = drill_points["x4"]
    drill_y1 = drill_points["y1"]
    drill_y2 = drill_points["y2"]
    drill_y3 = drill_points["y3"]
    drill_y4 = drill_points["y4"]
    drill_center1 = drill_points["center1"]
    drill_center2 = drill_points["center2"]
    drill_center3 = drill_points["center3"]
    drill_center4 = drill_points["center4"]
    if direction_type == 0:
        if drill_center1:
            drill_x1 = keep_left / 2
        if drill_center2:
            drill_x2 = set_width - keep_right / 2
        if drill_center3:
            drill_x3 = keep_left / 2
        if drill_center4:
            drill_x4 = set_width - keep_right / 2
    else:
        if drill_center1:
            drill_y1 = set_height - keep_top / 2
        if drill_center2:
            drill_y2 = set_height - keep_top / 2
        if drill_center3:
            drill_y3 = keep_bottom / 2
        if drill_center4:
            drill_y4 = keep_bottom / 2
    drill_locations = [[drill_x1, drill_y1], [drill_x2, drill_y2], [drill_x3, drill_y3], [drill_x4, drill_y4]]
    drill_layers = layer_info.get_drill_layer_name(job)
    solderMask_layers = layer_info.get_soldermask_list(job)
    drill_pad_name = 'r' + (str)(round(drill_size / 25400, 3))
    solderMask_pad_name = 'r' + (str)(round(drill_sm_size / 25400, 3))
    for drill_layer in drill_layers:
        for drill_location in drill_locations:
            if drill_location[0] == 0 or drill_location[1] == 0:
                continue
            if drill_flag:
                epcam_api.add_pad(job, step, [], drill_layer, drill_pad_name, drill_location[0], drill_location[1], 1, 0, 0, [{".drill": "non_plated"}])
                for solderMask_layer in solderMask_layers:
                    epcam_api.add_pad(job, step, [], solderMask_layer, solderMask_pad_name, drill_location[0], drill_location[1], 1, 0, 0, [])
    #添加辅助孔

#孔补偿, 添加辅助孔
def drill_operation(job, step, data):
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
    drill_process.drill_resize_to(job, step, attribute_size, drill_show, long_resize_size, short_resize_size, isEnDiameter, drill_satellitehole,
                                    aspect_ratio, drill_shortgroove, oval_range, drill_range, short_aspect_ratio, ultrashort_slot_resize)

#添加光学点, 添加光学点保护圈, 光学点添加开窗, 光学点下避铜, 添加v-cut测点
def add_mark_points(job, step, keep_params, mark_params, drill_points, set_params, params):
    #拼板, 工艺边参数
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    #判断在x方向还是y方向添加流胶条
    direction_type = 0      #0:x方向, 1:y方向
    if keep_left == 0 or keep_right == 0:
        direction_type = 1
    else:
        direction_type = 0
    #计算光学点中心的坐标
    mark2drill = mark_params['mark2drill']
    mark2keep = mark_params['mark2keep']
    mark_flag = mark_params['mark_flag']
    mark_ring_flag = mark_params['mark_ring_flag']
    v_test_flag = mark_params['v_test_flag']
    FdMarkCenter = mark_params['FdMarkCenter']       #光学点居中
    mark_x1 = 0
    mark_x2 = 0
    mark_x3 = 0
    mark_x4 = 0
    mark_y1 = 0
    mark_y2 = 0
    mark_y3 = 0
    mark_y4 = 0
    mark_location_infos = get_mark_points(job, step, keep_params, mark_params, drill_points, set_params)
    mark_locations = mark_location_infos['location']
    # if not mark_locations[0] == []:
    #     mark_x1 = mark_locations[0][0]
    #     mark_y1 = mark_locations[0][1]
    # if not mark_locations[1] == []:
    #     mark_x2 = mark_locations[1][0]
    #     mark_y2 = mark_locations[1][1]
    # if not mark_locations[2] == []:
    #     mark_x2 = mark_locations[2][0]
    #     mark_y2 = mark_locations[2][1]
    # if not mark_locations[3] == []:
    #     mark_x4 = mark_locations[3][0]
    #     mark_y4 = mark_locations[3][1]
    # if direction_type == 0:
    #     mark_x1 = keep_left - mark2keep
    #     mark_x2 = set_width - keep_right + mark2keep
    #     mark_x3 = keep_left - mark2keep
    #     mark_x4 = set_width - keep_right + mark2keep
    #     mark_y1 = drill_points['y1'] - mark2drill
    #     mark_y2 = drill_points['y2'] - mark2drill
    #     mark_y3 = drill_points['y3'] + mark2drill
    #     mark_y4 = drill_points['y4'] + mark2drill
    #     if FdMarkCenter:
    #         mark_x1 = keep_left / 2
    #         mark_x2 = set_width - keep_right / 2
    #         mark_x3 = keep_left / 2
    #         mark_x4 = set_width - keep_right / 2
    # else:
    #     mark_y1 = set_height - keep_top + mark2keep
    #     mark_y2 = set_height - keep_top + mark2keep
    #     mark_y3 = keep_bottom - mark2keep
    #     mark_y4 = keep_bottom - mark2keep
    #     mark_x1 = drill_points['x1'] + mark2drill
    #     mark_x2 = drill_points['x2'] - mark2drill
    #     mark_x3 = drill_points['x3'] + mark2drill
    #     mark_x4 = drill_points['x4'] - mark2drill
    #     if FdMarkCenter:
    #         mark_y1 = set_height - keep_top / 2
    #         mark_y2 = set_height - keep_top / 2
    #         mark_y3 = keep_bottom / 2
    #         mark_y4 = keep_bottom / 2 
    #添加光学点
    #mark_size = mark_params['mark_size']     #光学点大小
    mark_size = 0
    mark_size = mark_location_infos['size']
    mark_pad_name = 'r' + (str)(round(mark_size / 25400, 3))
    mark_ring_type = mark_params['mark_ring_type']            #光学点保护环类型(donut_s 或 donut_r)
    mark_outter_ring = mark_params['mark_outter_ring']        #光学点保护环外环尺寸
    mark_inner_ring = mark_params['mark_inner_ring']          #光学点保护环内环尺寸
    mark_ring_name = mark_ring_type + (str)(round(mark_outter_ring / 25400, 3)) + 'x' + (str)(round(mark_inner_ring / 25400, 3))
    mark_inner_pad_name = 'r' + (str)(round(mark_outter_ring / 25400, 3))    #光学点下避铜负片
    mark_sm_size = mark_params['mark_sm_size']     #光学点开窗大小
    mark_sm_pad_name = 'r' + (str)(round(mark_sm_size / 25400, 3))
    outter_layers = layer_info.get_outter_list(job)
    inner_layers = layer_info.get_inner_layer_list(job)
    solderMask_layers = layer_info.get_soldermask_list(job)
    for outter_layer in outter_layers:
        outter_save = outter_layer + '_save'
        #先在外层开个洞并整合
        layer_info.clear_select(job, step, outter_layer)          #先清空选中
        mark_hole_name = 'r' + (str)(round((mark_outter_ring / 25400) + 20, 3))    #外层铜皮开洞
        if mark_flag:
            for mark_location in mark_locations:
                if not mark_location == []:
                    epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, mark_location[0], mark_location[1], -1, 0, 0, [])
        else:
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, outter_layer)
            #添加光学点属性筛选
            layer_info.set_attribute_filter(0, [{'.fiducial_mark':''}])
            layer_info.select_features_by_filter(job, step, [outter_save])
            mark_pad_infos = layer_info.get_selected_features_infos(job, step, outter_save)
            for mark_pad_info in mark_pad_infos:
                pad_x = mark_pad_info['X'] * 25400000
                pad_y = mark_pad_info['Y'] * 25400000
                if mark_pad_info['type'] == 3:
                    pad_x = mark_pad_info['XC'] * 25400000
                    pad_y = mark_pad_info['YC'] * 25400000
                epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, pad_x, pad_y, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, mark_x1, mark_y1, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, mark_x2, mark_y2, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, mark_x3, mark_y3, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], outter_layer, mark_hole_name, mark_x4, mark_y4, -1, 0, 0, [])
        layer_info.contourize(job, step, [outter_layer], 0.25 * 25400, True, 3.0 * 25400, 0)    #整合铜皮
        #将外层物件移回外层
        layer_info.clear_select(job, step, outter_save)          #先清空选中
        epcam_api.sel_copy_other(job, step, [outter_save], [outter_layer], False, 0, 0, 
                    False, 0, 0, 0, 0)
        job_operation.delete_layer(job, outter_save)
        if mark_flag:
            #添加光学点
            for mark_location in mark_locations:
                if not mark_location == []:
                    epcam_api.add_pad(job, step, [], outter_layer, mark_pad_name, mark_location[0], mark_location[1], 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_pad_name, mark_x1, mark_y1, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_pad_name, mark_x2, mark_y2, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_pad_name, mark_x3, mark_y3, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_pad_name, mark_x4, mark_y4, 1, 0, 0, [{".fiducial_name": "mark"}])
        if mark_ring_flag:
            #添加光学点保护圈
            if mark_flag:
                for mark_location in mark_locations:
                    if not mark_location == []:
                        epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, mark_location[0], mark_location[1], 1, 0, 0, [{".fiducial_name": "mark"}])
            else:
                layer_info.reset_select_filter()
                layer_info.clear_select(job, step, outter_layer)
                #添加光学点属性筛选
                layer_info.set_attribute_filter(0, [{'.fiducial_mark':''}])
                layer_info.select_features_by_filter(job, step, [outter_layer])
                mark_pad_infos = layer_info.get_selected_features_infos(job, step, outter_layer)
                for mark_pad_info in mark_pad_infos:
                    pad_x = mark_pad_info['X'] * 25400000
                    pad_y = mark_pad_info['Y'] * 25400000
                    if mark_pad_info['type'] == 3:
                        pad_x = mark_pad_info['XC'] * 25400000
                        pad_y = mark_pad_info['YC'] * 25400000
                    epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, pad_x, pad_y, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, mark_x1, mark_y1, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, mark_x2, mark_y2, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, mark_x3, mark_y3, 1, 0, 0, [{".fiducial_name": "mark"}])
            # epcam_api.add_pad(job, step, [], outter_layer, mark_ring_name, mark_x4, mark_y4, 1, 0, 0, [{".fiducial_name": "mark"}])
    #添加光学点内层避铜负片
    for inner_layer in inner_layers:
        for mark_location in mark_locations:
            if not mark_location == []:
                epcam_api.add_pad(job, step, [], inner_layer, mark_inner_pad_name, mark_location[0], mark_location[1], -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], inner_layer, mark_inner_pad_name, mark_x1, mark_y1, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], inner_layer, mark_inner_pad_name, mark_x2, mark_y2, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], inner_layer, mark_inner_pad_name, mark_x3, mark_y3, -1, 0, 0, [])
        # epcam_api.add_pad(job, step, [], inner_layer, mark_inner_pad_name, mark_x4, mark_y4, -1, 0, 0, [])
    #添加光学点开窗
    if mark_flag:
        for solderMask_layer in solderMask_layers:
            for mark_location in mark_locations:
                if not mark_location == []:
                    epcam_api.add_pad(job, step, [], solderMask_layer, mark_sm_pad_name, mark_location[0], mark_location[1], 1, 0, 0, [])
                # epcam_api.add_pad(job, step, [], solderMask_layer, mark_sm_pad_name, mark_x1, mark_y1, 1, 0, 0, [])
                # epcam_api.add_pad(job, step, [], solderMask_layer, mark_sm_pad_name, mark_x2, mark_y2, 1, 0, 0, [])
                # epcam_api.add_pad(job, step, [], solderMask_layer, mark_sm_pad_name, mark_x3, mark_y3, 1, 0, 0, [])
                # epcam_api.add_pad(job, step, [], solderMask_layer, mark_sm_pad_name, mark_x4, mark_y4, 1, 0, 0, [])
    #avoid_cu(job, step, params)
    user_symbol_list = layer_info.get_usersymbol_list(job)

#添加内层流胶条
def add_inner_flow_tape(job, step, keep_params, set_params):
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    #判断在x方向还是y方向添加流胶条
    flow_type = 0      #0:x方向, 1:y方向
    if keep_left == 0 or keep_right == 0:
        flow_type = 1
    else:
        flow_type = 0
    #获取outline的线宽
    line_width = 0
    line_width = get_outline_line_width(job, step)
    #计算流胶条的长宽, 四条工艺边的流胶条大小不同
    flow_left_width = keep_left - line_width * 2.2
    flow_left_height = 200 * 25400
    flow_right_width = keep_right - line_width * 2.2
    flow_right_height = 200 * 25400
    flow_top_width = 200 * 25400
    flow_top_height = keep_top - line_width * 2.2
    flow_bottom_width = 200 * 25400
    flow_bottom_height = keep_bottom - line_width * 2.2
    #x方向添加, 计算添加坐标
    flow_left_x = keep_left / 2
    flow_right_x = set_width - keep_right / 2
    flow_y_list = []
    for i in range(set_ny):
        flow_y_list.append(keep_bottom + set_dy * i)
    #y方向添加, 计算添加坐标
    flow_top_y = set_height - keep_top / 2
    flow_bottom_y = keep_bottom / 2
    flow_x_list = []
    for j in range(set_nx):
        flow_x_list.append(keep_left + set_dx * j)
    inner_layers = layer_info.get_inner_layer_list(job)
    if flow_type == 0:
        flow_left_pad_name = 'rect' + (str)(round(flow_left_width / 25400, 3)) + 'x' + (str)(round(flow_left_height / 25400, 3))
        flow_right_pad_name = 'rect' + (str)(round(flow_right_width / 25400, 3)) + 'x' + (str)(round(flow_right_height / 25400, 3))
        for flow_y in flow_y_list:
            if flow_y == 0:
                continue
            for inner_layer in  inner_layers:
                epcam_api.add_pad(job, step, [], inner_layer, flow_left_pad_name, flow_left_x, flow_y, -1, 0, 0, [])
                epcam_api.add_pad(job, step, [], inner_layer, flow_right_pad_name, flow_right_x, flow_y, -1, 0, 0, [])
    else:
        flow_top_pad_name = 'rect' + (str)(round(flow_top_width / 25400, 3)) + 'x' + (str)(round(flow_top_height / 25400, 3))
        flow_bottom_pad_name = 'rect' + (str)(round(flow_bottom_width / 25400, 3)) + 'x' + (str)(round(flow_bottom_height / 25400, 3))
        for flow_x in flow_x_list:
            if flow_x == 0:
                continue
            for inner_layer in  inner_layers:
                epcam_api.add_pad(job, step, [], inner_layer, flow_top_pad_name, flow_x, flow_top_y, -1, 0, 0, [])
                epcam_api.add_pad(job, step, [], inner_layer, flow_bottom_pad_name, flow_x, flow_bottom_y, -1, 0, 0, [])

#添加v_cut测点
def add_v_pad(job, step, keep_params, set_params, mark_outter_ring, drill_points, mark_params):
    #先打开EPLIB, 从EPLIB中拷贝用到的symbol
    try:
        #获得光学点坐标
        mark_location_infos = get_mark_points(job, step, keep_params, mark_params, drill_points, set_params)
        mark_locations = mark_location_infos['location']
        mark_x1 = 0
        mark_y1 = 0
        mark_x4 = 0
        mark_y4 = 0
        if not mark_locations[0] == []:
            mark_x1 = mark_locations[0][0]
            mark_y1 = mark_locations[0][1]
        if not mark_locations[3] == []:
            mark_x4 = mark_locations[3][0]
            mark_y4 = mark_locations[3][1]
        direction_type = mark_location_infos['direction_type']
        set_width = set_params['width']                 #set宽
        set_height = set_params['height']               #set高
        set_nx = set_params['nx']                       #x方向pcs数量
        set_ny = set_params['ny']                       #y方向pcs数量
        set_dx = set_params['dx']                       #x方向pcs间距
        set_dy = set_params['dy']                       #y方向pcs间距   
        keep_left = keep_params['left']                 #工艺边左
        keep_right = keep_params['right']               #工艺边右        
        keep_top = keep_params['top']                   #工艺边上             
        keep_bottom  = keep_params['bottom']            #工艺边下
        #计算v_cut测点坐标
        v_left_x = 0
        v_left_y = 0
        v_right_x = 0
        v_right_y = 0
        #获取outline的线宽
        line_width = 0
        line_width = get_outline_line_width(job, step)
        if direction_type == 0:
            v_left_x = keep_left + line_width / 2
            v_left_y = mark_y1 - mark_outter_ring / 2 - 90 * 25400
            v_right_x = set_width - keep_right - line_width / 2
            v_right_y = mark_y4 + mark_outter_ring / 2 + 90 * 25400
        else:
            v_left_x = mark_x1 + mark_outter_ring / 2 + 90 * 25400
            v_left_y = set_height - keep_top - line_width / 2
            v_right_x = mark_x4 - mark_outter_ring / 2 - 90 * 25400
            v_right_y = keep_bottom #+ line_width / 2
        outter_layers = layer_info.get_outter_list(job)
        solderMask_layers = layer_info.get_soldermask_list(job)
        for outter_layer in  outter_layers:
            #添加时注意pad旋转
            if direction_type == 0:
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_left_x, v_left_y, 1, 0, 3, []) 
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_right_x, v_right_y, 1, 0, 1, []) 
            else:
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_left_x, v_left_y, 1, 0, 0, []) 
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_right_x, v_right_y, 1, 0, 2, []) 
        for solderMask_layer in  solderMask_layers:
            #添加时注意pad旋转
            if direction_type == 0:
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_left_x, v_left_y, 1, 0, 3, []) 
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_right_x, v_right_y, 1, 0, 1, []) 
            else:
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_left_x, v_left_y, 1, 0, 0, []) 
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_right_x, v_right_y, 1, 0, 2, []) 
    except Exception as e:
        return 0

#添加v_cut测点2
def add_v_pad_2(job, step, keep_params, set_params, mark_outter_ring, drill_points, mark_params):
    #先打开EPLIB, 从EPLIB中拷贝用到的symbol
    try:       
        set_width = set_params['width']                 #set宽
        set_height = set_params['height']               #set高
        set_nx = set_params['nx']                       #x方向pcs数量
        set_ny = set_params['ny']                       #y方向pcs数量
        set_dx = set_params['dx']                       #x方向pcs间距
        set_dy = set_params['dy']                       #y方向pcs间距   
        space_x = set_params['space_x']                 #x方向间距   
        space_y = set_params['space_y']                 #y方向间距    
        pcs_width = set_dx - space_x                    #pcs宽   
        pcs_height = set_dy - space_y                   #pcs高  
        keep_left = keep_params['left']                 #工艺边左
        keep_right = keep_params['right']               #工艺边右        
        keep_top = keep_params['top']                   #工艺边上             
        keep_bottom  = keep_params['bottom']            #工艺边下
         #判断在x方向还是y方向添加
        direction_type = 0      #0:x方向, 1:y方向
        if keep_left == 0 or keep_right == 0:
            direction_type = 1
        else:
            direction_type = 0
        #计算v_cut测点坐标
        v_left_x = 0
        v_left_y = 0
        v_right_x = 0
        v_right_y = 0
        #获取outline的线宽
        line_width = 0
        line_width = get_outline_line_width(job, step)
        if direction_type == 0:
            v_left_x = keep_left# + line_width / 2
            v_right_x = set_width - keep_right# - line_width / 2
            if set_ny > 1:                
                v_left_y = set_height - keep_top - set_dy - pcs_height/ 2
                v_right_y = keep_bottom + set_dy + pcs_height/ 2
            else:
                v_left_y = keep_bottom + 90 * 25400 
                v_right_y = set_height - keep_top - 90 * 25400 
        else:
            v_left_y = set_height - keep_top
            v_right_y = keep_bottom #+ line_width / 2
            if set_nx > 1:      
                v_left_x = keep_left + set_dx + pcs_width / 2
                v_right_x = set_width - keep_right - set_dx - pcs_width / 2
            else:
                v_left_x = set_width - keep_right - 90 * 25400 
                v_right_x = keep_left + 90 * 25400 
        outter_layers = layer_info.get_outter_list(job)
        solderMask_layers = layer_info.get_soldermask_list(job)
        for outter_layer in  outter_layers:
            #添加时注意pad旋转
            if direction_type == 0:
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_left_x, v_left_y, 1, 0, 3, []) 
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_right_x, v_right_y, 1, 0, 1, []) 
            else:
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_left_x, v_left_y, 1, 0, 0, []) 
                epcam_api.add_pad(job, step, [], outter_layer, 'vcut_v', v_right_x, v_right_y, 1, 0, 2, []) 
        for solderMask_layer in  solderMask_layers:
            #添加时注意pad旋转
            if direction_type == 0:
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_left_x, v_left_y, 1, 0, 3, []) 
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_right_x, v_right_y, 1, 0, 1, []) 
            else:
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_left_x, v_left_y, 1, 0, 0, []) 
                epcam_api.add_pad(job, step, [], solderMask_layer, 'vcut_v_sm', v_right_x, v_right_y, 1, 0, 2, []) 
    except Exception as e:
        return 0

#添加文字测点
def add_text_pad(job, step, keep_params, set_params):
    #拼板, 工艺边参数
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    space_x = set_params['space_x'] 
    space_y = set_params['space_y']
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    #判断在x方向还是y方向添加文字测点
    direction_type = 0      #0:x方向, 1:y方向
    if keep_left == 0 or keep_right == 0:
        direction_type = 1
    else:
        direction_type = 0
    #x方向添加, 计算添加坐标
    text_left_x = keep_left / 2
    text_right_x = set_width - keep_right / 2
    text_y_list = []
    for i in range(set_ny):
        text_y_list.append(keep_bottom + set_dy * i)
    #y方向添加, 计算添加坐标
    text_top_y = set_height - keep_top / 2
    text_bottom_y = keep_bottom / 2
    text_x_list = []
    for j in range(set_nx):
        text_x_list.append(keep_left + set_dx * j)
    outter_layers = layer_info.get_outter_list(job)
    solderMask_layers = layer_info.get_soldermask_list(job)
    for outter_layer in outter_layers:
        if direction_type == 0:
            for text_y in text_y_list:
                if text_y == 0:
                    continue
                if keep_left > 0:
                    if space_y > 0:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_left_x - keep_left/6, text_y - space_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_left_x - keep_left/6, text_y - space_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_left_x - keep_left/6, text_y - space_y, 1, 0, 1, [])
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_left_x + keep_left/6, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_left_x + keep_left/6, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_left_x + keep_left/6, text_y, 1, 0, 1, [])  
                    else:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_left_x, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_left_x, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_left_x, text_y, 1, 0, 1, []) 
                else :
                    if space_y > 0:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_right_x - keep_right/6, text_y - space_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_right_x - keep_right/6, text_y - space_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_right_x - keep_right/6, text_y - space_y, 1, 0, 1, []) 
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_right_x + keep_right/6, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_right_x + keep_right/6, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_right_x + keep_right/6, text_y, 1, 0, 1, []) 
                    else:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_right_x, text_y, 1, 0, 1, [])
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_right_x, text_y, 1, 0, 1, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_right_x, text_y, 1, 0, 1, []) 
                         

        else:
            for text_x in text_x_list:
                if text_x == 0:
                    continue
                if keep_top > 0:
                    if space_x > 0:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x - space_x, text_top_y - keep_top/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x - space_x, text_top_y - keep_top/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x - space_x, text_top_y - keep_top/6, 1, 0, 0, [])
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x, text_top_y + keep_top/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x, text_top_y + keep_top/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x, text_top_y + keep_top/6, 1, 0, 0, [])  
                    else:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x, text_top_y, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x, text_top_y, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x, text_top_y, 1, 0, 0, []) 
                else :
                    if space_x > 0:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x - space_x, text_bottom_y - keep_bottom/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x - space_x, text_bottom_y - keep_bottom/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x - space_x, text_bottom_y - keep_bottom/6, 1, 0, 0, []) 
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x, text_bottom_y + keep_bottom/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x, text_bottom_y + keep_bottom/6, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x, text_bottom_y + keep_bottom/6, 1, 0, 0, []) 
                    else:
                        epcam_api.add_pad(job, step, [], outter_layer, 'vcut_l', text_x, text_bottom_y, 1, 0, 0, []) 
                        if len(solderMask_layers) > 0:
                            epcam_api.add_pad(job, step, [], solderMask_layers[0], 'vcut_l_sm', text_x, text_bottom_y, 1, 0, 0, []) 
                        if len(solderMask_layers) > 1:
                            epcam_api.add_pad(job, step, [], solderMask_layers[1], 'vcut_l_sm', text_x, text_bottom_y, 1, 0, 0, []) 

#添加本厂料号
def add_job_text(job, step, keep_params, set_params, factory_layer):
    #拼板, 工艺边参数
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下

    #判断在x方向还是y方向添加料号名
    direction_type = 0      #0:x方向, 1:y方向
    if keep_top > 0 and set_nx > 1:
        direction_type = 0
    else:
        if keep_bottom > 0 and set_nx > 1:
            direction_type = 1
        else:
            if keep_left > 0 and set_ny > 1:
                direction_type = 2
            else:
                if keep_left > 0 and set_ny > 1:
                    direction_type = 3
                else:
                    direction_type = 4
    if factory_layer == '':
        silkScreen_layers = []
        silkScreen_layers = layer_info.get_silkscreen_layer(job)
        if len(silkScreen_layers) == 0:
            return
        factory_layer = silkScreen_layers[0]
    #料号名左下角坐标
    job_text_x = 0
    job_text_y = 0
    #料号名字宽, 字高为所在工艺边一半宽度, 线宽8mil
    if direction_type == 0:
        job_text_x = keep_left + set_dx + 100 * 25400
        job_text_y = set_height - keep_top / 4 * 3
        text_size = keep_top / 2
        if (len(job) * keep_top / 2) > set_dx - 200 * 25400:
            text_size = (set_dx - 200 * 25400) / len(job)
        epcam_api.add_text(job, step, factory_layer, '', 'standard', job, text_size, text_size, 8 * 25400, job_text_x, job_text_y, 1, 0, 0, [], [])   
    elif direction_type == 1:
        job_text_x = keep_left + set_dx + 100 * 25400
        job_text_y = keep_bottom / 4
        text_size = keep_bottom / 2
        if (len(job) * keep_bottom / 2) > set_dx - 200 * 25400:
            text_size = (set_dx - 200 * 25400) / len(job)
        epcam_api.add_text(job, step, factory_layer, '', 'standard', job, text_size, text_size, 8 * 25400, job_text_x, job_text_y, 1, 0, 0, [], []) 
    elif direction_type == 2:
        job_text_x = keep_left / 4
        job_text_y = set_height - set_dy - 100 * 25400
        text_size = keep_left / 2
        if (len(job) * keep_left / 2) > set_dy - 200 * 25400:
            text_size = (set_dy - 200 * 25400) / len(job)
        epcam_api.add_text(job, step, factory_layer, '', 'standard', job, text_size, text_size, 8 * 25400, job_text_x, job_text_y, 1, 1, 0, [], [])
    elif direction_type == 3:
        job_text_x = set_height - keep_right / 4 * 3
        job_text_y = set_height - set_dy - 100 * 25400
        text_size = keep_right / 2
        if (len(job) * keep_right / 2) > set_dy - 200 * 25400:
            text_size = (set_dy - 200 * 25400) / len(job)
        epcam_api.add_text(job, step, factory_layer, '', 'standard', job, text_size, text_size, 8 * 25400, job_text_x, job_text_y, 1, 1, 0, [], [])
    elif direction_type == 4:
        return

#添加尖角孔
def add_sharp_corner_drill(job, step, params):
    all_layers = layer_info.get_all_layer_name(job)
    drill_layers = layer_info.get_drill_layer_name(job)
    outline_layer = ''
    if 'outline' in all_layers:
        outline_layer = 'outline'
    elif 'gko' in all_layers:
        outline_layer = 'gko'
    else:
        return
    #内角孔
    hole_size = params['drill']['drill_insidehole']['aperture']              #孔径
    angle_tol = params['drill']['drill_insidehole']['angle_error']          #角度误差
    side_space = params['drill']['drill_insidehole']['hole_side'] * 25400   #线内偏移   
    if hole_size > 0:
        if len(drill_layers) > 0:
            drl_name = drill_layers[0]
            hole_name = 'r' + str(hole_size)
            epcam_api.add_outline_drill(job, step, 'outline', drl_name, hole_name, side_space, angle_tol)
    
#内外层避铜
def avoid_cu(job, step, params):
    #避NPTH孔和profile线（调用优化avoid_features_DFM_op）（外层做NPTH开窗）（外层无VIA独立孔）
    inner_layers = layer_info.get_inner_layer_list(job)
    outter_layers = layer_info.get_outter_list(job)
    inner_avoid_NPTH = params['inner']['avoid_NPTH'] * 25400 
    outter_avoid_NPTH = params['inner']['avoid_NPTH'] * 25400 
    inner_avoid_profile_size = params['inner']['avoid_Profile'] * 25400
    outter_avoid_profile_size = params['outter']['avoid_Profile'] * 25400
    inner_avoid_v_cut = params['inner']['avoid_v_cut'] * 25400
    outter_avoid_v_cut = params['outter']['avoid_v_cut'] * 25400
    analysis_dfm.avoid_features_DFM_op(job, step, inner_layers, 'erf', True, inner_avoid_profile_size, True, inner_avoid_NPTH, False, 0, False, 0, inner_avoid_v_cut)
    analysis_dfm.avoid_features_DFM_op(job, step, outter_layers, 'erf', True, outter_avoid_profile_size, True, outter_avoid_NPTH, False, 0, False, 0, outter_avoid_v_cut)
    
#获取outline线宽
def get_outline_line_width(job, step):
    line_width = 0
    all_layers = layer_info.get_all_layer_name(job)
    outline_layer = ''
    if 'outline' in all_layers:
        outline_layer = 'outline'
    else:
        if 'gko' in all_layers:
            outline_layer = 'gko'
        else:
            line_width = 0
    if not outline_layer == '':
        layer_info.clear_select(job, step, outline_layer)  #清除选中并对每一个line进行选中判断   
        layer_info.reset_select_filter()
        layer_info.set_featuretype_filter(70)
        layer_info.select_features_by_filter(job, step, [outline_layer])
        info_list = layer_info.get_features_infos(job, step, outline_layer)    #获取所有line的信息
        layer_info.reset_select_filter()
        layer_info.clear_select(job, step, outline_layer)  #清除选中并对每一个line进行选中判断
        if len(info_list) > 0:
            line_name = info_list[0][2]      #线的symbolname
            line_width = layer_info.get_drillsize_by_symbolname(line_name)   #通过symbolname获取线宽 
    return line_width
    
#防焊添加v-cut开窗
def add_v_cut_sm(job, step, params, set_params, keep_params, set_type):
    soldermask_line_width = params['outter']['profile_line_width']
    v_cut_sm_size = params['outter']['v_cut']
    soldermask_line_name = 'r' + str(soldermask_line_width)
    v_cut_sm_name = 'r' + str(v_cut_sm_size)
    all_layers = layer_info.get_all_layer_name(job)
    solderMask_layers = layer_info.get_soldermask_list(job)
    outline_layer = ''
    if 'outline' in all_layers:
        outline_layer = 'outline'
    else:
        if 'gko' in all_layers:
            outline_layer = 'gko'
        else:
            return
    if set_type == 0:
        #从org拷贝set_outline至set的outline层
        if 'set-outline' in all_layers:
            epcam_api.copy_layer_features(job, 'org', ['set-outline'], job, step, [outline_layer], True, False)
    else:
        outline_width = params['outter']['outline_width']
        outline_add_v_cut(job, step, outline_layer, set_params, keep_params, outline_width)
    if not outline_layer == '':
        layer_info.clear_select(job, step, outline_layer)  #清除选中并对每一个line进行选中判断   
        layer_info.reset_select_filter()
        layer_info.set_featuretype_filter(70)
        #layer_info.set_attribute_filter(0, [{'.fiducial_name':'v-cut'}])
        layer_info.select_features_by_filter(job, step, [outline_layer])
        info_list = layer_info.get_features_infos(job, step, outline_layer)    #获取所有line的信息
        layer_copy = outline_layer + '_copy'
        job_operation.create_layer(job, layer_copy)
        if len(info_list) > 0:
            epcam_api.sel_copy_other(job, step, [outline_layer], [layer_copy], False, 0, 0, 
                                    False, 0, 0, 0, 0)
        layer_info.change_feature_symbols(job, step, [layer_copy], soldermask_line_name)
        layer_info.clear_select(job, step, layer_copy)  #清除选中并对每一个line进行选中判断
        epcam_api.sel_copy_other(job, step, [layer_copy], solderMask_layers, False, 0, 0, 
                                False, 0, 0, 0, 0)
        layer_info.reset_select_filter()
        layer_info.clear_select(job, step, outline_layer)  #清除选中并对每一个line进行选中判断
        job_operation.delete_layer(job, layer_copy)
        for solderMask_layer in solderMask_layers:
            layer_info.set_featuretype_filter(70)
            layer_info.set_attribute_filter(0, [{'.fiducial_name':'v-cut'}])
            layer_info.select_features_by_filter(job, step, [solderMask_layer])
            line_list = layer_info.get_features_infos(job, step, solderMask_layer)    #获取所有line的信息
            if len(line_list) > 0:
                layer_info.change_feature_symbols(job, step, [solderMask_layer], v_cut_sm_name)
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, solderMask_layer)  #清除选中并对每一个line进行选中判断

#在outline层添加v-cut线
def outline_add_v_cut(job, step, outline_layer, set_params, keep_params, outline_width):
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距  
    set_width = set_params['width'] 
    set_height = set_params['height'] 
    space_x = set_params['space_x']
    space_y = set_params['space_y']
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    line_name = 'r' + str(outline_width)
    #计算v_cut线位置, 并添加
    #横向  
    #line_y_list = []
    line_XS = 0
    line_XE = set_width
    epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, 0, line_XE, 0, 1, 0, []) #添加线
    epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, set_height, line_XE, set_height, 1, 0, []) #添加线
    if keep_top > 0:     
        epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, set_height-keep_top, line_XE, set_height-keep_top, 1, 0, []) #添加线
    if keep_bottom > 0:     
        epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, keep_bottom, line_XE, keep_bottom, 1, 0, []) #添加线
    for i in range(1, set_ny):
        line_y1 = keep_bottom + set_dy * i
        epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, line_y1, line_XE, line_y1, 1, 0, [{'.fiducial_name':'v-cut'}]) #添加线
        #line_y_list.append(line_y1)
        if space_y > 0:
            line_y2 = keep_bottom + set_dy * i - space_y
            epcam_api.add_line(job, step, [], outline_layer, line_name, line_XS, line_y2, line_XE, line_y2, 1, 0, [{'.fiducial_name':'v-cut'}]) #添加线
            #line_y_list.append(line_y2)
    #纵向
    #line_x_list = []
    line_YS = set_height
    line_YE = 0
    epcam_api.add_line(job, step, [], outline_layer, line_name, 0, line_YS, 0, line_YE, 1, 0, []) #添加线
    epcam_api.add_line(job, step, [], outline_layer, line_name, set_width, line_YS, set_width, line_YE, 1, 0, []) #添加线
    if keep_left > 0:     
        epcam_api.add_line(job, step, [], outline_layer, line_name, keep_left, line_YS, keep_left, line_YE, 1, 0, []) #添加线
    if keep_right > 0:     
        epcam_api.add_line(job, step, [], outline_layer, line_name, set_width-keep_right, line_YS, set_width-keep_right, line_YE, 1, 0, []) #添加线
    for j in range(1, set_nx):
        line_x1 = keep_left + set_dx * j
        epcam_api.add_line(job, step, [], outline_layer, line_name, line_x1, line_YS, line_x1, line_YE, 1, 0, [{'.fiducial_name':'v-cut'}]) #添加线
        #line_x_list.append(line_x1)
        if space_x > 0:
            line_x2 = keep_left + set_dx * j - space_x
            epcam_api.add_line(job, step, [], outline_layer, line_name, line_x2, line_YS, line_x2, line_YE, 1, 0, [{'.fiducial_name':'v-cut'}]) #添加线
            #line_x_list.append(line_x2)

#拼板
def set_function(job, step, params, keep_params, set_params, set_type, datum_x, datum_y):
    array_childsteps = params['panel']['panel_step']['childsteps']

    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下

    array_childsteps[0]['DX'] = set_dx
    array_childsteps[0]['DY'] = set_dy
    array_childsteps[0]['NX'] = set_nx
    array_childsteps[0]['NY'] = set_ny
    if set_type == 0:
        array_childsteps[0]['X'] = 0 #- datum_x + keep_left
        array_childsteps[0]['Y'] = 0 #- datum_y + keep_bottom
    else:
        array_childsteps[0]['X'] = 0 + keep_left
        array_childsteps[0]['Y'] = 0 + keep_bottom
    array_childsteps[0]['NAME'] = 'pcs'      

    all_layers = layer_info.get_all_layer_name(job)
    # outline_layer = ''
    # if 'outline' in all_layers:
    #     outline_layer = 'outline'
    # else:
    #     if 'gko' in all_layers:
    #         outline_layer = 'gko'
    #     else:
    #         return

    epcam_api.set_step_profile(job, step, [{'ix': 0, 'iy': 0}, {'ix': 0, 'iy': set_height}, {'ix': set_width, 'iy': set_height}, 
                                           {'ix': set_width, 'iy': 0}, {'ix': 0, 'iy': 0}])
    #epcam_api.set_panel_margin(job, step, keep_left, keep_right, keep_top, keep_bottom)
    layer_info.step_repeat(job, step, array_childsteps)
    copy_boardInfo_to_set(job, step, array_childsteps, set_type)

def add_usersymbol(job, step, v_test_flag, text_test_flag):
    lib_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\job'
    lib_name = 'eplib'
    epcam_api.open_job(lib_path, lib_name)
    user_symbol_list = layer_info.get_usersymbol_list(job)
    if v_test_flag:
        if not 'vcut_v' in user_symbol_list:
            epcam_api.copy_usersymbol_to_other_job(lib_name, job, 'vcut_v', 'vcut_v')
        if not 'vcut_v_sm' in user_symbol_list:
            epcam_api.copy_usersymbol_to_other_job(lib_name, job, 'vcut_v_sm', 'vcut_v_sm')
    if v_test_flag:
        if not 'vcut_l' in user_symbol_list:
            epcam_api.copy_usersymbol_to_other_job(lib_name, job, 'vcut_l', 'vcut_l')
        if not 'vcut_l_sm' in user_symbol_list:
            epcam_api.copy_usersymbol_to_other_job(lib_name, job, 'vcut_l_sm', 'vcut_l_sm')

#排序函数
def comp(x, y):
    if x[1] > y[1]:
        return -1
    elif x[1] < y[1]:
        return 1
    else:
        if x[0] < y[0]:
            return -1
        else:
            return 1

#计算光学点坐标, 当原稿存在光学点时, 获取其坐标点
def get_mark_points(job, step, keep_params, mark_params, drill_points, set_params):
    #拼板, 工艺边参数
    set_width = set_params['width']                 #set宽
    set_height = set_params['height']               #set高
    set_nx = set_params['nx']                       #x方向pcs数量
    set_ny = set_params['ny']                       #y方向pcs数量
    set_dx = set_params['dx']                       #x方向pcs间距
    set_dy = set_params['dy']                       #y方向pcs间距   
    keep_left = keep_params['left']                 #工艺边左
    keep_right = keep_params['right']               #工艺边右        
    keep_top = keep_params['top']                   #工艺边上             
    keep_bottom  = keep_params['bottom']            #工艺边下
    #判断在x方向还是y方向添加流胶条
    direction_type = 0      #0:x方向, 1:y方向
    if keep_left == 0 or keep_right == 0:
        direction_type = 1
    else:
        direction_type = 0
    #计算光学点中心的坐标
    mark_size = mark_params["mark_size"]
    mark2drill = mark_params['mark2drill']
    mark2keep = mark_params['mark2keep']
    mark_flag = mark_params['mark_flag']
    mark_ring_flag = mark_params['mark_ring_flag']
    v_test_flag = mark_params['v_test_flag']
    FdMarkCenter = mark_params['FdMarkCenter']       #光学点居中
    mark_x1 = 0
    mark_x2 = 0
    mark_x3 = 0
    mark_x4 = 0
    mark_y1 = 0
    mark_y2 = 0
    mark_y3 = 0
    mark_y4 = 0
    location = []
    pad_size = 0
    location_info = {'location':location, 'direction_type':direction_type, 'size':pad_size}
    #当没有勾选添加光学点坐标时, 从资料中获取
    if not mark_flag:
        #先清空筛选，和当前的选中
        outter_layers = layer_info.get_outter_list(job)
        for outter_layer in outter_layers:
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, outter_layer)
            #添加光学点属性筛选
            layer_info.set_attribute_filter(0, [{'.fiducial_mark':''}])
            layer_info.select_features_by_filter(job, step, [outter_layer])
            mark_pad_infos = layer_info.get_selected_features_infos(job, step, outter_layer)
            for mark_pad_info in mark_pad_infos:
                pad_size = mark_pad_info['xsize']
                pad_location = []
                pad_x = mark_pad_info['X'] * 25400000
                pad_y = mark_pad_info['Y'] * 25400000
                if mark_pad_info['type'] == 3:
                    pad_x = mark_pad_info['XC'] * 25400000
                    pad_y = mark_pad_info['YC'] * 25400000
                pad_location = [pad_x, pad_y]
                if pad_location not in location and len(location) < 4:
                    location.append(pad_location)
            layer_info.reset_select_filter()
            layer_info.clear_select(job, step, outter_layer)
        #排序
        location.sort(key=functools.cmp_to_key(comp))  #左上 右上 左下 右下     
        tol = 4 - len(location)    
        if tol > 0:
            for i in range(tol):
                location.append([])
        location_info['location'] = location
        location_info['pad_size'] = pad_size
        return location_info
    if direction_type == 0:
        mark_x1 = keep_left - mark2keep
        mark_x2 = set_width - keep_right + mark2keep
        mark_x3 = keep_left - mark2keep
        mark_x4 = set_width - keep_right + mark2keep
        mark_y1 = drill_points['y1'] - mark2drill
        mark_y2 = drill_points['y2'] - mark2drill
        mark_y3 = drill_points['y3'] + mark2drill
        mark_y4 = drill_points['y4'] + mark2drill
        if FdMarkCenter:
            mark_x1 = keep_left / 2
            mark_x2 = set_width - keep_right / 2
            mark_x3 = keep_left / 2
            mark_x4 = set_width - keep_right / 2
    else:
        mark_y1 = set_height - keep_top + mark2keep
        mark_y2 = set_height - keep_top + mark2keep
        mark_y3 = keep_bottom - mark2keep
        mark_y4 = keep_bottom - mark2keep
        mark_x1 = drill_points['x1'] + mark2drill
        mark_x2 = drill_points['x2'] - mark2drill
        mark_x3 = drill_points['x3'] + mark2drill
        mark_x4 = drill_points['x4'] - mark2drill
        if FdMarkCenter:
            mark_y1 = set_height - keep_top / 2
            mark_y2 = set_height - keep_top / 2
            mark_y3 = keep_bottom / 2
            mark_y4 = keep_bottom / 2 
    location = [[mark_x1, mark_y1], [mark_x2, mark_y2], [mark_x3, mark_y3], [mark_x4, mark_y4]]
    location_info['location'] = location
    location_info['size'] = mark_size
    return location_info

#从orig拷贝set的板边信息
def copy_boardInfo_to_set(job, step, childsteps, set_type):
    #重置筛选
    layer_info.reset_select_filter()
    #获取board layer
    signallayers = layer_info.get_signal_layer_list(job)
    size=len(signallayers)
    solderlayers = layer_info.get_soldermask_list(job)
    drilllayers = layer_info.get_drill_layer_name(job)
    silklayers = layer_info.get_silkscreen_layer(job)
    boardlayer = signallayers
    for solderlayer in solderlayers:
        boardlayer.append(solderlayer)
    for drilllayer in drilllayers:
        boardlayer.append(drilllayer)
    for silklayer in silklayers:
        boardlayer.append(silklayer)
    #copy orig step
    new_step_name = job_operation.copy_step(job, 'org')
    layer_info.set_selection(True, True, True, True, True, False)
    #产生每个pcs profile polygon信息
    for child in childsteps:
        NX = child["NX"]
        NY = child["NY"]
        DX = child["DX"]
        DY = child["DY"]
        X = child["X"]
        Y = child["Y"]
        poly = layer_info.get_profile(job, child["NAME"])
        poly  = json.loads(poly)
        poly = poly["points"]
        orig_poly = []      #左下角pcs profile polygon
        for i in range(len(poly)):
            per_point = []
            per_point.append(poly[i]["ix"]+X)
            per_point.append(poly[i]["iy"]+Y)
            orig_poly.append(per_point)
        for x in range(NX):
            for y in range(NY):
                cur_poly = []       #当前pcs profile polygon信息
                for idx in range(len(orig_poly)):
                    point = [orig_poly[idx][0]+x*DX, orig_poly[idx][1]+y*DY]
                    cur_poly.append(point) 
                for t in range(len(boardlayer)):
                    layer_info.select_feature(job, new_step_name, boardlayer[t], cur_poly, {}, 1, False)
                    layer_info.delete_feature(job, new_step_name, [boardlayer[t]])
    layer_info.set_selection(True, True, True, True, True, True)
    #copy 板边信息至 set
    #自动定属性(net孔)
    outter_layers = layer_info.get_outter_list(job)
    epcam_api.contour2pad(job, new_step_name, [outter_layers[0]], 25400, 5 * 25400, 99999 * 25400, '+++')
    epcam_api.auto_classify_attribute(job, new_step_name, boardlayer)
    for v in range(len(boardlayer)):
        layer_info.copy_layer_features(job, new_step_name, [boardlayer[v]], job, "set", [boardlayer[v]], False, False)
    job_operation.delete_step(job, new_step_name)

#当原稿存在定位孔时, 获取其坐标点
def get_drill_points(job, step):
    drill_x1 = 0
    drill_x2 = 0
    drill_x3 = 0
    drill_x4 = 0
    drill_y1 = 0
    drill_y2 = 0
    drill_y3 = 0
    drill_y4 = 0
    pad_size = 0
    #先清空筛选，和当前的选中
    drill_layers = layer_info.get_drill_layer_name(job)
    drill_layer = ''
    if len(drill_layers) > 0:
        drill_layer = drill_layers[0]
        layer_info.reset_select_filter()
        layer_info.clear_select(job, step, drill_layer)
        #添加光学点属性筛选
        layer_info.set_attribute_filter(0, [{'.drill':'non_plated'}])
        layer_info.select_features_by_filter(job, step, [drill_layer])
        drill_pad_infos = layer_info.get_selected_features_infos(job, step, drill_layer)
        location = []
        for drill_pad_info in drill_pad_infos:
            pad_size = drill_pad_info['xsize']
            pad_location = []
            pad_x = drill_pad_info['X'] * 25400000
            pad_y = drill_pad_info['Y'] * 25400000
            if drill_pad_info['type'] == 3:
                pad_x = drill_pad_info['XC'] * 25400000
                pad_y = drill_pad_info['YC'] * 25400000
            pad_location = [pad_x, pad_y]
            if pad_location not in location and len(location) < 4:
                location.append(pad_location)
        #排序
        location.sort(key=functools.cmp_to_key(comp))  #左上 右上 左下 右下     
        tol = 4 - len(location)    
        if tol > 0:
            for i in range(tol):
                location.append([])
                
        if not location[0] == []:
            drill_x1 = location[0][0]
            drill_y1 = location[0][1]
        if not location[1] == []:
            drill_x2 = location[1][0]
            drill_y2 = location[1][1]
        if not location[2] == []:
            drill_x3 = location[2][0]
            drill_y3 = location[2][1]
        if not location[3] == []:
            drill_x4 = location[3][0]
            drill_y4 = location[3][1]

    drill_points = {"x1":drill_x1, "y1":drill_y1, "x2":drill_x2, "y2":drill_y2, "x3":drill_x3, "y3":drill_y3, 
                    "x4":drill_x4, "y4":drill_y4, "center1":False, "center2":False, 
                    "center3":False, "center4":False}
    location_info = {'drill_points': drill_points, 'size': pad_size}
    return location_info

