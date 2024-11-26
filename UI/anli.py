# from http.cookiejar import debug
from epkernel import BASE
from epkernel.MI import stackup
from epkernel.Action import Information,Selection
from epkernel import Configuration, Input, GUI,Application,Guide
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





#生成孔属性
BASE.auto_classify_attribute(JobName, step[0], [['drill.out']])


def find_hole_sizes(jobname, step):
    try:
        Selection.reset_select_filter()
        Selection.set_featuretype_filter(True, True, True, True, True, True, True)
        
        # 选择特征
        Selection.select_features_by_filter(jobname, step[0], ['drill.out'])
        all_features = Information.get_selected_features_infos(jobname, step[0], 'drill.out')
        print(all_features)
        
        if not all_features:
            print("没有找到任何孔特征")
            return None, None

        # 初始化最小和最大孔大小
        min_hole_size = float('inf')
        max_hole_size = float('-inf')

        # 遍历所有特征以查找最小和最大孔大小
        for feature in all_features:
            hole_size_str = feature['symbolname']  # 假设 'symbolname' 表示孔的大小
            hole_size = float(hole_size_str[1:])  # 去掉 'r' 并转换为浮点数
            
            if hole_size < min_hole_size:
                min_hole_size = hole_size
            
            if hole_size > max_hole_size:
                max_hole_size = hole_size

        if min_hole_size == float('inf') or max_hole_size == float('-inf'):
            print("没有找到有效的孔特征")
            return None, None

        # 将孔大小转换为适当的单位并输出
        min_hole_size_mm = min_hole_size * 25.4  # 假设以微米为单位
        max_hole_size_mm = max_hole_size *25.4  # 假设以微米为单位
        
        return min_hole_size_mm, max_hole_size_mm

    except Exception as e:
        print(f"发生错误: {e}")
# 调用查找最小和最大孔大小的函数
min_hole_size, max_hole_size = find_hole_sizes(JobName, step)
print(f"最小孔大小: {min_hole_size} mm")
print(f"最大孔大小: {max_hole_size} mm")


liangkongjianju=0.006
liangbianjianju=0.002#两面 两个边总距离

def caokong(jobname, step):
    
    try:
        Selection.reset_select_filter()
        Selection.reverse_select(jobname, step[0], 'drill.out')
        GUI.show_layer(JobName, step[0], 'drill.out')
        Selection.select_feature_by_id(jobname, step[0], 'drill.out', [3157])
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
        delta_d = round(math.sqrt((XE - XS) ** 2 + (YE - YS) ** 2)+D, 5)
        # slot_length = round(delta_d + D, 5)
        print("槽孔长度:", delta_d)
        if delta_d > 0.008:
            guiding_hole_size=(delta_d-liangkongjianju-liangbianjianju)/2
        # 计算导引孔大小
        # guiding_hole_size = (slot_length - 0.05) / 2
            print("槽孔长度:", delta_d)
            print("导引孔大小:", guiding_hole_size)

            # 将角度转换为弧度并计算导引孔位置
            angle_rad = math.radians(angle)
            if XE<XS:
                guiding_hole_position_start_x = XS + abs((guiding_hole_size - D+liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_start_y = YS + (guiding_hole_size - D+liangbianjianju) * math.sin(angle_rad) / 2
                guiding_hole_position_end_x = XE - abs((guiding_hole_size - D+liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_end_y = YE - (guiding_hole_size - D+liangbianjianju) * math.sin(angle_rad) / 2
            else:
                guiding_hole_position_start_x = XS - abs((guiding_hole_size - D+liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_start_y = YS - (guiding_hole_size - D+liangbianjianju) * math.sin(angle_rad) / 2
                guiding_hole_position_end_x = XE + abs((guiding_hole_size - D+liangbianjianju) / 2 * math.cos(angle_rad))
                guiding_hole_position_end_y = YE + (guiding_hole_size - D+liangbianjianju) * math.sin(angle_rad) / 2

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

# caokong(JobName, step)
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
def calculate_small_r(SmallToSmall, length_waibian):
    return (SmallToSmall * 2) / length_waibian
def yuzuankong(jobname, step):
    try:
        x_6 = 20000000#坐标
        y_6 = 10000000#坐标
        r_6 = 60000000#大小
        
        
        
        count = 5;#个数
        SmallToLarge = 2000000;#1为小到大距离
        SmallToSmall = 10000000;#2为小到小距离
        Selection.reset_select_filter()
        Selection.reverse_select(jobname, step[0], 'drill.out')
        # GUI.show_layer(JobName, step[0], 'drill.out')
        # Selection.select_feature_by_id(jobname, step[0], 'drill.out', [3157])
        r_size= f"r{round(r_6 / 1000 / 25.4, 2)}"
        # 添加第一层 Pad
        Layers.add_pad(jobname, step[0], ['drill.out'], r_size, x_6, y_6, True, 0, [], 0)
        jiaodu=360/count
        # 创建空列表来存储 x_i 和 y_i
        x_values = []
        y_values = []
        for i in range(1,count+1):
            x_i=x_6+r_6/2*math.cos(math.radians(jiaodu*i))-SmallToLarge*math.cos(math.radians(jiaodu*i))
            y_i=y_6+r_6/2*math.sin(math.radians(jiaodu*i))-SmallToLarge*math.sin(math.radians(jiaodu*i))
            # 将计算得到的 x_i 和 y_i 存储到列表中
            x_values.append(x_i)
            y_values.append(y_i)
            print("x_i")
            print(jiaodu*i)
            print(x_i,y_i)
            
            # 输出存储的数组
        print("所有 x 值: ", x_values)
        print("所有 y 值: ", y_values)
        len_1=calculate_distance(x_values[0],y_values[0],x_values[1], y_values[1] )
        # yuan_1_x=x_6
        # yuan_1_y=y_6+r_6/2-SmallToLarge
        # yuan_2_x=x_6+r_6/2-SmallToLarge
        # yuan_2_y=y_6
        # len_1=calculate_distance(yuan_1_x, yuan_1_y, yuan_2_x, yuan_2_y)
        print("得到长度")
        print(len_1)
        
        xiaobanjing=(len_1*r_6/2-len_1*SmallToLarge-(r_6/2-SmallToLarge)*SmallToSmall)/(r_6-SmallToLarge*2+len_1)
        
        print("得到小半径")
        print(xiaobanjing)
        print("得到坐标")
        banjing=xiaobanjing/1000/25.4
        # print(yuan_1_x,yuan_1_y-xiaobanjing)
        # print(yuan_2_x-xiaobanjing,yuan_2_y)

        print("得到半径")
        print(banjing)
        #region
        # # 计算 mall_r
        # numerator = (r_6 / 2 - SmallToLarge) * len_1 - SmallToSmall * (r_6 / 2 - SmallToLarge)
        # denominator = 2 * (r_6 / 2 - SmallToLarge) + len_1

        # # 避免除以零的情况
        # if denominator != 0:
        #     mall_r = numerator / denominator
        # else:
        #     mall_r = None  # 或者设置为其他值或进行错误处理

        # # 输出计算结果
        # print(f"计算得到的 mall_r: {mall_r}")
        #endregion
        
        
# 假设 jiaodu 已经定义并是一个有效值

        # 这里进行循环遍历 x_values 和 y_values，同时动态获取 i 的值
        for i, (x, y) in enumerate(zip(x_values, y_values), start=1):
            # 计算新的 x 和 y 值
            adjusted_x = x - xiaobanjing * math.cos(math.radians(jiaodu * i))
            adjusted_y = y - xiaobanjing * math.sin(math.radians(jiaodu * i))
            # 计算半径
            double_banjing = banjing * 2  # 计算两倍的 banjing

            # 将结果转换为字符串并拼接
            r_value = f"r{double_banjing}"  # 使用 f-string 进行字符串拼接
            # 调用 Layers.add_pad
            Layers.add_pad(jobname, step[0], ['drill.out'], r_value, adjusted_x, adjusted_y, True, 0, [], 0)
            # 打印输出以便调试
            print(f"第 {i} 个 pad 添加在位置: ({adjusted_x}, {adjusted_y})")

        
        # Layers.add_pad(jobname, step[0], ['drill.out'], "r760", yuan_1_x, yuan_1_y-xiaobanjing, True, 0, [], 0)
        # Layers.add_pad(jobname, step[0], ['drill.out'], "r760", yuan_2_x-xiaobanjing, yuan_2_y, True, 0, [], 0)
        # Layers.add_pad(jobname, step[0], ['drill.out'], "r760", yuan_1_x, y_6-r_6/2+SmallToLarge+xiaobanjing, True, 0, [], 0)
        # Layers.add_pad(jobname, step[0], ['drill.out'], "r760", x_6-r_6/2+SmallToLarge+xiaobanjing, yuan_2_y, True, 0, [], 0)
    
    except Exception as e:
        print(f"发生错误: {e}")

yuzuankong(JobName, step)


# Layers.add_pad(jobname,step[0],['drill.out'],"r15",x_6+200000,y_6,True,0,[],0)
GUI.show_layer(JobName, step[0], 'drill.out')


Guide.get_affected_layers(JobName)
