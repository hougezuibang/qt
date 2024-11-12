from http.cookiejar import debug

from epkernel.Action import Information,Selection
from epkernel import Configuration, Input, GUI, Output,Application,Guide
from epkernel.Edition import Matrix,Layers
# 初始化配置，指定配置文件路径
Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
jobname ='6328037'
step=['orig']
# 打开指定的工作任务
Input.open_job(jobname, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')
 
# 设置自定义特征
Information.get_origin_point(jobname, step[0])
# Selection.get_origin_point('6345022c1', step[0])

def rename_layers(jobname):

    changes = [
        ('etchlayer1top.gdo', 'board', 'signal', 'gtl'),
        ('etchlayer2.gdo', 'board', 'signal', 'l2'),
        ('etchlayer3.gdo', 'board', 'signal', 'l3'),
        ('etchlayer4.gdo', 'board', 'signal', 'l4'),
        ('etchlayer5.gdo', 'board', 'signal', 'l5'),
        ('etchlayer6bottom.gdo', 'board', 'signal', 'gbl'),
        ('generatedsilkscreenbottom.gdo', 'board', 'silk_screen', 'gbo'),
        ('generatedsilkscreentop.gdo', 'board', 'silk_screen', 'gto'),
        ('solderpastebottom.gdo', 'misc', 'signal', 'gbp'),
        ('solderpastetop.gdo', 'misc', 'signal', 'gtp'),
        ('soldermaskbottom.gdo', 'board', 'solder_mask', 'gbs'),
        ('soldermasktop.gdo', 'board', 'solder_mask', 'gts'),
        ('antisilk_top.gdo', 'misc', 'signal', 'antisilk_top.gdo'),
        ('thruholenonplated.ncd', 'board', 'drill', 'drill.out'),
        ('thruholeplated.ncd', 'board', 'drill', 'drill.pin'),
    ]

    for layer, type_, feature, new_value in changes:
        Matrix.change_matrix_row(jobname, layer, type_, feature, new_value, polarity=True)
        
def sort(jobname):
    move_layers = [
            (9, 1),
            (13, 2),
            (3, 17),
            (12, 9),
            (14, 11),
            (15, 12)
        ]

    for src, dst in move_layers:
        Matrix.move_layer(jobname, src, dst)


# 重命名图层的请求
rename_layers(jobname)
# 移动图层的请求
sort(jobname)
# 复制图层到另一层的请求
Layers.copy2other_layer(jobname, step[0], 'drill.pin', 'drill.out', False, 0, 0, 0, 0, 0, 0, 0)
print('----------复制图层到另一层-')
Matrix.delete_layer(jobname, 'drill.pin')
print('--------------------------删除图层----------------------------')
# GUI.show_layer(jobname, step[0], 'l3')
# 复制图层
Matrix.copy_layer(jobname,'rout')
# 重命名图层
Application.rename_layer_jwApp(jobname,'rout+1', 'rou')
# 反选
Selection.reverse_select(jobname, step[0], 'rout')
# 创建profile
Layers.create_profile(jobname, step[0], 'rout')
print('----------创建profile------')

affected_layers  = Information.get_board_layers(jobname)
print(affected_layers)



# Guide.display_layer(jobname, step[0],, ,, affectedlayers=affected_layers )
# Guide.display_layers(jobname, step[0], clayer='', snaplayer='', displaylayers=[], affectedlayers=affected_layers)
Guide.display_layers(jobname, step[0], 'l3', 'l2', ['gto', 'gts', 'gtl', 'l2', 'l3', 'l4', 'l5', 'gbl', 'gbs', 'gbo', 'drill.out'], ['gto', 'gts', 'gtl', 'l2', 'l3', 'l4', 'l5', 'gbl', 'gbs', 'gbo', 'drill.out'])
#设置层别，可将层别设置为工作层、影响层、显示层和吸附层
GUI.show_layer(jobname, step[0], 'l3')

Guide.get_affected_layers(jobname)
# 获取指定料号当前选择的影响层





# Information.get_profile_box(job, step)

#获取指定料号工作单元(step)中profile的最小外接正矩形的左上及右下顶点坐标信息

# print('--------------------------获取图层属性-')
Information.get_layer_attributes(jobname, step[0],'drillmap')
print('--------------------------获取图层属性-++++')

print(Information.get_layer_attributes(jobname, step[0],'drillmap'))
print('--------------------------删除图层----------------------------')
Matrix.delete_layer(jobname, 'get_layer_attributes')
GUI.show_layer(jobname, step[0], 'rout')


print('--------------------------------------------------------')

# Matrix.copy_layer(job, old_layer_name)
# print('--------------------------复制图层-')
# Matrix.create_step(job, step, col_index=-1)
# print('----------创建步长-')
# Layers.create_profile(job, step, layer)
# print('----------创建profile-')
# Layers.copy2other_layer(src_job, src_step, src_layer, dst_layer, invert, offset_x, offset_y, mirror, resize, rotation, x_anchor, y_anchor)
# print('----------复制图层到另一层-')
# Layers.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, text, surface, arc, line, pad)
# print('----------依据profile范围去除板内外features')
# Layers.resize_global(job, step, layers, type, size)
# print('----------对指定料号所有层中物件进行涨缩------')
# Information.get_profile_box(job, step)

# 获取指定料号工作单元(step)中profile的最小外接正矩形的左上及右下顶点坐标信息
# Information.get_selected_features_box(job, step, layers)

# 获取指定层选中features的最小外接正矩形的左下和右上坐标点，若无选中feature，则结果均为零
# Guide.get_clicked_point(job, step)

# 获取点击的中心点坐标


























# print(Selection.get_origin_point('6345022c1', step[0]))
# Selection.set_attribute_filter(0,[{'.drill':'plated'},{'.orig_size_mm':'1550009'}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')

 # 设置属性过滤器并选择特征
# Selection.set_attribute_filter(0,[{'.drill':'plated'},{'.orig_size_mm':'1550009'}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# 设置排除属性过滤器并选择特征
# Selection.set_exclude_attr_filter([{'.drill':'plated'}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 设置包含符号过滤器并选择特征
# Selection.set_include_symbol_filter(['r55.118'])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 通过ID选择特征并显示图层
# Selection.select_feature_by_id('6345022c1', step[0], 'gtl', [56])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 通过模式过滤并显示图层
# Selection.filter_by_mode('6345022c1', step[0], 'gbs', ['drill.out'], 0, True, True, True, True, True, True, True, -1, [], -1, 0, [])
# GUI.show_layer('6345022c1', step[0], 'gbs')
 
# # 设置属性范围过滤器并选择特征
# Selection.set_attr_range_filter(0, [{'attr_name':'.orig_size_mm', 'min_value':1300000, 'max_value':2000000}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 设置符号范围过滤器并选择特征
# Selection.set_symbol_range_filter([{'symbol_type':'r', 'min_value':1400000, 'max_value':2000000, 'attr_name':'r'}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 设置排除属性过滤器并选择特征
# Selection.set_exclude_attr_filter([{'.drill':'plated'}])
# Selection.select_features_by_filter('6345022c1', step[0], ['drill.out'])
# GUI.show_layer('6345022c1', step[0], 'drill.out')
 
# # 设置内轮廓过滤器并选择特征
# Selection.set_inprofile_filter(1)
# Selection.select_features_by_filter('6345022c1', 'panel', ['gtl'])
# GUI.show_layer('6345022c1', 'panel', 'gtl')
 
# # 通过点选择特征并显示图层
# Selection.select_feature_by_point('6345022c1', step[0], 'gtl', 0, 0)
# GUI.show_layer('6345022c1', step[0], 'gtl')
 
# # 获取选择参数和信息
# selectParam = Information.get_select_param()
# selectSymbolInfo = Information.get_selected_symbol_info('6345022c1', step[0], 'gtl')
# selectFeatureInfo = Information.get_selected_features_infos('6345022c1', step[0], 'gtl')
# innerLayer = Information.get_inner_layers('6345022c1')
# profile = Information.get_profile('6345022c1', step[0])
# usersymbolList = Information.get_usersymbol_list('6345022c1')
# restRate = Information.get_rest_cu_rate('6345022c1', step[0], 'gtl', 25400)
# layerInformation = Information.get_layer_information('6345022c1')
# layerReport = Information.get_layer_report('6345022c1', 'gtl')
# allSymbolInfo = Information.get_all_symbol_info('6345022c1', step[0], 'l2')
# datumPoint = Information.get_datum_point('6345022c1', step[0])
# layerAttr = Information.get_layer_attributes('6345022c1', step[0], 'drill.out')
# exposed = Information.get_exposed_area('6345022c1', step[0], {'gtl': ['gts'], 'gbl': ['gbs']}, ['drill.out'],
#                                     25400, 0, 0, True, True, False, True, 1, True)
 
# # 初始化变量
# a = 0