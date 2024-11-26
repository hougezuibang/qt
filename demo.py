# from http.cookiejar import debug
from epkernel import BASE
# from epkernel.MI import stackup
from epkernel.Action import Information,Selection
# from epkernel import Application
from epkernel import Configuration, Input, GUI,Guide
from epkernel.Edition import Matrix,Layers
import math
# 初始化配置，指定配置文件路径
JobName ='6328037'
step=['orig']
Configuration.init(r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release')
# 打开指定的工作任务
Input.open_job(JobName, r'C:\Users\MLB\Downloads\EPCAM_1.2.8.4_release_jiami_3\Release\job')
 
# 设置自定义特征
Information.get_origin_point(JobName, step[0])


#重命名以及设置属性
def rename_layers():
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
        Matrix.change_matrix_row(JobName, layer, type_, feature, new_value, polarity=True)
#设置排序        
def sort():
    move_layers = [
            (9, 1),
            (13, 2),
            (3, 17),
            (12, 9),
            (14, 11),
            (15, 12)
        ]

    for src, dst in move_layers:
        Matrix.move_layer(JobName, src, dst)





#钻孔补偿 查询
def reset_filter():
    _extracted_from_reset_filter_2('via', 6)
    _extracted_from_reset_filter_2('plated', 3)
    _extracted_from_reset_filter_2('non_plated', 1)
    GUI.show_layer(JobName, step[0], 'drill.out')
# TODO Rename this here and in `reset_filter`
def _extracted_from_reset_filter_2(arg0, arg1):
    Selection.reset_select_filter()
    # 设置包含符号过滤器并选择特征
    Selection.set_attribute_filter(0, [{'.drill': arg0}])
    # 将筛选出来的进行选中
    Selection.select_features_by_filter(JobName, step[0], ['drill.out'])
    # 调整孔径
    Layers.resize_global(JobName, step[0], ["drill.out"], 1, arg1 * 25400)



def find_layer(layername):
    try:
        list_layers = Information.get_layers(JobName)
        print(list_layers)
    # 使用列表解析查找 'rout' 的下标
        layer_index = next((index+1 for index, layer in enumerate(list_layers) if layer == layername), -1)

    # 判断结果
        if layer_index != -1:
            print(f"层级 'rout' 的下标是: {layer_index}")
        else:
            print("没有找到层级 'rout'")
    except Exception as e:
        print(f"发生错误: {e}")
    # return list_layers
    return layer_index

# 重命名图层函数调用
rename_layers()
# 移动图层函数调用
sort()


# 复制图层到另一层
Layers.copy2other_layer(JobName, step[0], 'drill.pin', 'drill.out', False, 0, 0, 0, 0, 0, 0, 0)
#删除原来多余图层
Matrix.delete_layer(JobName, 'drill.pin')


# 复制图层
# Matrix.copy_layer(jobname,'rout')
# 重命名图层
# Application.rename_layer_jwApp(jobname,'rout+1', 'rou')
# 移动图层
# Matrix.move_layer(jobname, find_layer('rou') ,find_layer('rout'))


# 选中图层
Selection.reverse_select(JobName, step[0], 'rout')
# 创建profile
Layers.create_profile(JobName, step[0], 'rout')

#创建一个分隔层名字为------并放在最后
# Matrix.create_layer(jobname,"------", -1)
# 获取指定料号所有层别(layer)名称，存放在层列表中
# list_layers = Information.get_layers(jobname)
#备份所有层别
# Matrix.backup_layer(jobname, step[0],list_layers, '+1')

#创建新step
# region
# 复制step
# new_step = Matrix.copy_step(jobname, step[0])
#重命名
# Matrix.change_matrix_column(jobname, new_step, "net")
# step数组追加新元素
# step.append(new_step)  # 追加新元素
# 选中新step并打开
# GUI.show_layer(jobname, step[1], 'l4')
# GUI.show_layer(jobname, "net", 'l4')
#endregion

# 获取指定料号所有层别(layer)名称，存放在层列表中
list_layers = Information.get_layers(JobName)
# try:
#     # 使用列表推导式创建新的层列表，仅保留需要的层
#     list_layers = [layer for layer in list_layers if layer.get('context') == "board"]
# except Exception as e:
#     print(f"发生错误: {e}")
# 依据profile范围去除板内外feature
# Layers.clip_area_use_profile(jobname, step[0], list_layers, False, False, 0,True, True, True, True, True)

# 设置排除属性过滤器并选择特征
# 设置筛选器，positive为正面，negative为负面，text为文本，surface为表面，arc为圆弧，line为线，pad为孔
def find_center_point(jobname, step, layer_name):
    try:
        Selection.reset_select_filter()
        Selection.set_featuretype_filter(True, True, True, True, True, True, True)
        
        # 选择特征
        Selection.select_features_by_filter(jobname, step[0], [layer_name])
        into = Information.get_selected_features_infos(jobname, step[0], layer_name)
        print(into)
        print("intointointointointointointointo")
        if not into:
            print(f"没有找到层级 '{layer_name}' 的物件信息")
            return 


# 使用列表推导式提取坐标
        x_coords = [item['XE'] for item in into] + [item['XS'] for item in into]
        y_coords = [item['YE'] for item in into] + [item['YS'] for item in into]

# 计算中心点坐标
        center_x = (min(x_coords) + max(x_coords)) / 2
        center_y = (min(y_coords) + max(y_coords)) / 2

        print(f"中心点坐标: ({center_x * 25.400}, {center_y * 25.400})")
        return (center_x * 25.400, center_y * 25.400)  # 返回中心点坐标值
    except Exception as e:
        print(f"发生错误: {e}")


# 调用优化后的函数
center_point = find_center_point(JobName, step, 'gbo')
center_point1 = find_center_point(JobName, step, 'rout')
# print(f"中心点 gbo: {center_point}")
# print(f"中心点 rout: {center_point1}")
# 计算偏差
skew_x = (center_point1[0] - center_point[0])  * 1000000
skew_y = (center_point1[1] - center_point[1])  * 1000000
# print(f"偏差 X: {skew_x}")
# print(f"偏差 Y: {skew_y}")
# 检查返回值并打印结果
Layers.transform_features(
    JobName, step[0], 'gto', 0,
    False, False, False, False, False,
    {'ix': 0, 'iy': 0}, 0, 0, 0, skew_x, skew_y
)
Layers.transform_features(
    JobName, step[0], 'gbo', 0,
    False, False, False, False, False,
    {'ix': 0, 'iy': 0}, 0, 0, 0, skew_x, skew_y
)
# print(skew_x)
# print(skew_y)
# 检查返回值并打印结果
Layers.transform_features(JobName, step[0], 'gto', 0,
        False, False, False, False, False,{'ix': 0, 'iy': 0}, 0, 0, 0, skew_x, skew_y)
Layers.transform_features(JobName, step[0], 'gbo', 0,
        False, False, False, False, False,{'ix': 0, 'iy': 0}, 0, 0, 0, skew_x, skew_y)

# GUI.show_layer(jobname, step[0], 'gto')





# (127.40120824999997, 107.74350549999998)
# (112.4999905, 93.93749299999999)













def type_filter():
    # GUI.show_layer(jobname, step[0], 'l3')
    # 根据所需要筛选的feature类型设置筛选器，需配合select_features_by_filter使用
    # 设置筛选器，positive为正面，negative为负面，text为文本，surface为表面，arc为圆弧，line为线，pad为孔
    Selection.set_featuretype_filter(True, False, False, True, False, False, False)
    # 依据筛选器当前设置的筛选条件进行物件筛选
    Selection.select_features_by_filter(JobName, step[0], ["l3"])
    # 转换成pad 并复制出一层
    Layers.contour2pad(JobName, step[0], ["l3"], 1*25400, 5*25400, 99999*25400,  "+++++")
# type_filter()

# GUI.show_layer(JobName, step[0], 'l3')


# region
# Selection.reset_select_filter()
# # 设置包含符号过滤器并选择特征
# Selection.set_include_symbol_filter(['r9.84'])
# Selection.select_features_by_filter(jobname, step[0], ['l2'])
# 显示图层
# GUI.show_layer(jobname, step[0], 'l2')

#endregion





# #创建新step
#region
# 复制step
# new_step1 = Matrix.copy_step(jobname, step[0])
#重命名
# Matrix.change_matrix_column(jobname, new_step1, "edit")
# step数组追加新元素
# step.append(new_step1)  # 追加新元素
# 选中新step并打开
# GUI.show_layer(jobname, "edit", 'l5')
#endregion


#生成孔属性
BASE.auto_classify_attribute(JobName, step[0], [['drill.out']])
# bool_value =  stackup.auto_drill_belts(jobname,step[0])
# print("++++++++++123321123++++++++++++++++++++++")
# print(bool_value)

#生成线路层属性
# for layer in list_layers:
#     BASE.auto_classify_attribute(jobname, step[0], [layer])





#钻孔补偿 查询
# reset_filter()


#选择pad转成外形线
def padtoline():
# 复制图层
# Matrix.copy_layer(jobname,'gtl')
# GUI.show_layer(jobname, step[0], 'gtl')
# 重命名图层
# Application.rename_layer_jwApp(jobname,'gtl+2', 'gtl++')
# 对图层进行轮廓化处理
    Layers.contourize(JobName, step[0], ['gtl'], 6350, True, 7620, 1)
# 将表面转换为轮廓
    Layers.surface2outline(JobName, step[0], ['gtl'], 5 * 25400)
# 移动到另一图层
    Layers.move2other_layer(JobName, step[0], ['gtl'], JobName, step[0], 'rout', False, 0, 0, 0, 0, 0, 0, 0)
# 删除新图层
# Matrix.delete_layer(jobname, 'gtl++')
# 显示最终图层
    GUI.show_layer(JobName, step[0], 'rout')


#线转成pad
def linetopad():
    Layers.outline2surface(JobName, step[0], ["rout"], False)
    GUI.show_layer(JobName, step[0], 'rout')
# 对图层进行轮廓化处理
    # Layers.contourize(jobname, step[0], ['gtl'], 6350, True, 7620, 1)
# 将表面转换为轮廓
    Layers.surface2outline(JobName, step[0], ['rout'], 5 * 25400)
    
# 移动到另一图层
    Layers.move2other_layer(JobName, step[0], ['rout'], JobName, step[0], 'drill.out', False, 0, 0, 0, 0, 0, 0, 0)
# 删除新图层
# Matrix.delete_layer(jobname, 'gtl++')
# 显示最终图层
    GUI.show_layer(JobName, step[0], 'drill.out')
# padtoline()
# linetopad()

# Selection.set_symbol_range_filter([{'symbol_type':'r', 'min_value':140, 'max_value':200000000, 'attr_name':'r'}])
# #Selection.set_exclude_attr_range_filter([{'symbol_type':'r', 'min_value':140, 'max_value':2000000, 'attr_name':'r'}])
# Selection.select_features_by_filter(jobname, step[0], ['drill.out'])
# Selection.reverse_select(jobname, step[0], 'drill.out')

def caokong(jobname, step):
    try:
        Selection.select_feature_by_id(jobname, step[0], 'drill.out', [3155])
        print("----------选中物件3155----------")
        GUI.show_layer(jobname, step[0], 'drill.out')
        selectFeatureInfo = Information.get_selected_features_infos(jobname, step[0], 'drill.out')
        
        if not selectFeatureInfo:
            print("没有找到选中的物件信息")
            return
        
        print("--------------------------获取选中物件信息----------")
        feature_info = selectFeatureInfo[0]  # 获取第一个（也是唯一的）字典
        
        # 从 feature_info 中提取必要参数并进行单位转换
        XS, XE = feature_info['XS'] * 25.4, feature_info['XE'] * 25.4
        YS, YE = feature_info['YS'] * 25.4, feature_info['YE'] * 25.4
        D = round(feature_info['linewidth'] / 1_000_000, 5)  # 假设线宽代表原来的圆柱直径
        angle = feature_info['angle']  # 角度
        
        print(XS, YS)
        print(XE, YE)
        print(D)

        # 计算槽孔长度
        delta_d = round(math.sqrt((XE - XS) ** 2 + (YE - YS) ** 2), 5)
        slot_length = round(delta_d + D, 5)

        # 计算导引孔大小
        guiding_hole_size = (slot_length - 0.05) / 2
        print("槽孔长度:", slot_length)
        print("导引孔大小:", guiding_hole_size)

        # 将角度转换为弧度并计算导引孔位置
        angle_rad = math.radians(angle)
        if XE<XS:
            guiding_hole_position_start_x = XS + abs((guiding_hole_size - D) / 2 * math.cos(angle_rad))
            guiding_hole_position_start_y = YS + (guiding_hole_size - D) * math.sin(angle_rad) / 2
            guiding_hole_position_end_x = XE - abs((guiding_hole_size - D) / 2 * math.cos(angle_rad))
            guiding_hole_position_end_y = YE - (guiding_hole_size - D) * math.sin(angle_rad) / 2
        else:
            guiding_hole_position_start_x = XS - abs((guiding_hole_size - D) / 2 * math.cos(angle_rad))
            guiding_hole_position_start_y = YS - (guiding_hole_size - D) * math.sin(angle_rad) / 2
            guiding_hole_position_end_x = XE + abs((guiding_hole_size - D) / 2 * math.cos(angle_rad))
            guiding_hole_position_end_y = YE + (guiding_hole_size - D) * math.sin(angle_rad) / 2

        guiding_hole_size_str = f'r{str(guiding_hole_size * 1000 / 25.4)}'
        
        # 添加导引孔
        Layers.add_pad(jobname, step[0], ['drill.out'], guiding_hole_size_str,
                       int(guiding_hole_position_start_x * 1_000_000),
                       int(guiding_hole_position_start_y * 1_000_000), True, 0, [], 0)

        Layers.add_pad(jobname, step[0], ['drill.out'], guiding_hole_size_str,
                       int(guiding_hole_position_end_x * 1_000_000),
                       int(guiding_hole_position_end_y * 1_000_000), True, 0, [], 0)

        GUI.show_layer(jobname, step[0], 'drill.out')
    
    except Exception as e:
        print(f"发生错误: {e}")

caokong(JobName, step)
def kong_15(jobname, step):
    try:
        x_6 = 10000000
        y_6 = 10000000
        # r_6 = 6000000
        r_6 = 6000000   # 转换为毫米 (单位)
        # 添加第一层 Pad
        r_size= f"r{round(r_6 / 1000 / 25.4, 2)}"
        Layers.add_pad(jobname, step[0], ['drill.out'], r_size, x_6, y_6, True, 0, [], 0)

        # 计算 Pad 的偏移量，避免重复计算
        offset = 1500000 / 2 + 200000 - r_6 / 2
        
        # 计算其他 Pad 的位置
        positions = [
            (x_6 + offset, y_6,0),
            (x_6 - offset, y_6,90),
            (x_6, y_6 + offset,180),
            (x_6, y_6 - offset,270)
        ]
        
        # 添加剩余的 Pads
        for pos in positions:
            Layers.add_pad(jobname, step[0], ['drill.out'], "r59", pos[0], pos[1], True, 0, [], pos[2])
    
    except Exception as e:
        print(f"发生错误: {e}")


kong_15(JobName, step)

def kong_20(jobname, step):
    try:
        x_6 = 20000000#坐标
        y_6 = 10000000#坐标
        r_6 = 6000000#大小
        r_size= f"r{round(r_6 / 1000 / 25.4, 2)}"
        # 添加第一层 Pad
        Layers.add_pad(jobname, step[0], ['drill.out'], r_size, x_6, y_6, True, 0, [], 0)
        
        # 计算 Pad 的位置
        offset = (2000000 / 2 + 200000 - r_6 / 2)
        # 添加剩余的 Pads
        for dx in [offset, -offset]:
            Layers.add_pad(jobname, step[0], ['drill.out'], "r78.74", x_6 + dx, y_6, True, 0, [], 0)
            Layers.add_pad(jobname, step[0], ['drill.out'], "r78.74", x_6, y_6 + dx, True, 0, [], 0)
    except Exception as e:
        print(f"发生错误: {e}")

kong_20(JobName, step)


# Layers.add_pad(jobname,step[0],['drill.out'],"r15",x_6+200000,y_6,True,0,[],0)
print('--------------按道理------------添加导引孔-')
GUI.show_layer(JobName, step[0], 'drill.out')







# Layers.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, text, surface, arc, line, pad)

# 依据profile范围去除板内外feature
# Layers.flatten_step(job, step, flatten_layer, dst_layer)

# 将指定工作单元的指定层及其子step层中的所有资料备份至目标层，目标层需先创建


# Information.get_layers(job)

# 获取指定料号所有层别(layer)名称，存放在层列表中
# Information.get_datum_point(job,step)

# 获取指定工作单元基准点坐标











# affected_layers  = Information.get_board_layers(jobname)
# print(affected_layers)

# Guide.display_layer(jobname, step[0],, ,, affectedlayers=affected_layers )
# Guide.display_layers(jobname, step[0], clayer='', snaplayer='', displaylayers=[], affectedlayers=affected_layers)
# Guide.display_layers(jobname, step[0], 'l3', 'l2', ['gto', 'gts', 'gtl', 'l2', 'l3', 'l4', 'l5', 'gbl', 'gbs', 'gbo', 'drill.out'], ['gto', 'gts', 'gtl', 'l2', 'l3', 'l4', 'l5', 'gbl', 'gbs', 'gbo', 'drill.out'])
#设置层别，可将层别设置为工作层、影响层、显示层和吸附层
# GUI.show_layer(jobname, step[0], 'l3')

Guide.get_affected_layers(JobName)
# 获取指定料号当前选择的影响层





# Information.get_profile_box(job, step)

#获取指定料号工作单元(step)中profile的最小外接正矩形的左上及右下顶点坐标信息

# print('--------------------------获取图层属性-')
Information.get_layer_attributes(JobName, step[0],'drillmap')
print('--------------------------获取图层属性-++++')

print(Information.get_layer_attributes(JobName, step[0],'drillmap'))
print('--------------------------删除图层----------------------------')
Matrix.delete_layer(JobName, 'get_layer_attributes')
# GUI.show_layer(jobname, step[0], 'rout')


print('--------------------------------------------------------')

# Application.set_featuretype_filter_jwApp(types=['line','pad','surface','arc','text'],polarity= ['pos','neg'])
# 根据所需要筛选的feature类型设置筛选器

# Layers.move2same_layer(job, step, layers, offset_x, offset_y)
# 将指定料号指定层中选中的feature在同层移动，若无选中feature则整层移动

# Information.get_all_features_info(job, step, layer)
# 获取指定层所有物件的信息(包含物件形状大小、中心坐标、极性、是否镜像、旋转角度等)
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
# Layers.c(job, step, layers, type, size)
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