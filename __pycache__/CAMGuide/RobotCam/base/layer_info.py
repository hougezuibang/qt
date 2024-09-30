import os,sys
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import job_operation


def get_drill_layer_name(job):
    """
    #获取孔层layer名
    :param     job:
    :param     step:
    :return    drill_list:孔层名列表
    :raises    error:
    """
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        drill_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['type'] == 'drill' and layer_info[i]['context'] == 'board':
                drill_list.append(layer_info[i]['name'])
        return drill_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''


def set_attribute_filter(logic, attribute_list):
    """
    #设置属性筛选
    :param     logic:0 ：全部满足  1：有其一
    :param     attribute_list:要设置的属性列表
    :returns   :
    :raise    error:
    """
    try:
        epcam_api.filter_set_attribute(logic, attribute_list)
    except Exception as e:
        print(e)
    return 0


def set_size_filter(symbols):
    """
    #设置symbol大小筛选
    :param     symbols:symbolname 列表
    :return    :
    :raises    error:
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        #attributes_list = []
        #for i in range(0, len(select_param['attributes_value'])):
           # for key, value in select_param['attributes_value'][i].items():
                #attributes_list.append([key,value])
        epcam_api.set_select_param(select_param['featuretypes'], True, symbols, 
                                select_param['minline'], select_param['maxline'],
                                select_param['dcode'], select_param['attributes_flag'],
                                select_param['attributes_value'], select_param['profile_value'],
                                select_param['use_selection'])
    except Exception as e:
        print(e)
    return 0


def select_features_by_attributes(job, step, layers, logic, attribute_list):
    """
    #选中attributes属性的features
    :param     job:
    :param     step:
    :param     layer:
    :param     logic:0 ：全部满足  1：有其一
    :param     attribute_list:要设置的属性列表
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.filter_set_attribute(logic, attribute_list)
        e = epcam_api.get_select_param()
        epcam_api.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def select_features_by_filter(job, step, layers):
    """
    #根据筛选条件选择
    :param     job:
    :param     step:
    :param     layers:layer列表
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def get_all_drill_symbolname(job, step, layer):
    """
    #获取孔层的所有feature的symbolname
    :param     job:
    :param     step:
    :param     layer:
    :returns   symbol_list:当前层中pad的name和size
    :raises    error:
    """
    try:
        global _size
        ret = epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        drill_list = data['paras']['pad_list']
        symbol_list = []
        for i in range(0, len(drill_list)):
            if drill_list[i]['symbolname'] not in symbol_list:
                if drill_list[i]['symbolname'][0] == 'o':
                    str = drill_list[i]['symbolname']
                    str1 = str[4:]
                    index_x = str1.index('x')
                    number_1 = float(str1[:(index_x)])
                    number_2 = float(str1[(index_x+1):])
                    if number_1 >= number_2:
                        _size = number_2* 25400
                    else:
                        _size = number_1* 25400
                else:
                    _size = drill_list[i]['symbol_width']
            symbol_list.append([drill_list[i]['symbolname'], _size])
        return symbol_list
    except Exception as e:
        print(e)
    return ''   


def get_all_features_size(job, step, layer):
    """
    #获取当前层的所有drill的size
    :param     job:
    :param     step:
    :param     layer:
    :returns   size_list:
    :raises    error:
    """
    try:
        global _size
        ret =epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        drill_list = data['paras']['pad_list']
        size_list = []

        for i in range(0, len(drill_list)):
            if drill_list[i][0] == 'o':
                str = pad_list[i]['symbolname']
                str1 = str[4:]
                index_x = str1.index('x')
                number_1 = float(str1[:(index_x)])
                number_2 = float(str1[(index_x+1):])
                if number_1 >= number_2:
                    _size = number_2* 25400
                else:
                    _size = number_1* 25400
            else:
                _size = drill_list[i]['symbol_width']
            if _size not in size_list:
                size_list.append(_size)
        return size_list
    except Exception as e:
        print(e)
    return ''


def reset_select_filter():
    """
    #清空筛选条件
    :param     :
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
    except Exception as e:
        print(e)
    return 0


def clear_select(job, step, layer):
    """
    #清空选择
    :param     job:
    :param     step:
    :param     layer:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.clear_selected_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0

  
def get_inner_layer_list(job):
    """
    #获取内层layer_list
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        
        if len(board_layer_list) <= 2:
            print('no inner layer!')
            return []
        else:
            board_layer_list.pop(-1)
            board_layer_list.pop(0)
            inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return ''


def set_featuretype_filter(featuretype):
    """
    #设置feature type筛选
    :param     featuretype:代表筛选features的类型
    :returns   :
    :raises    error:
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        #print(data)  
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        symbols = select_param['symbols']
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        has_symbol = select_param['has_symbols']
        epcam_api.set_select_param(featuretype, has_symbol, symbols,minline, maxline,dcode, flag,value, pr_value,sele)
    except Exception as e:
        print(e)
    return 0


def select_features_by_featuretype(job, step, layer, featuretype):
    """
    #选中指定featuretype的features
    :param     job:
    :param     step:
    :param     layer:
    :param     featuretype:
    :returns   :
    :raises    error:
    """
    try:
        set_featuretype_filter(featuretype)
        epcam_api.select_features_by_filter(job, step, layer)
    except Exception as e:
        print(e)
    return 0


def set_include_symbol_filter(symbol_list):
    """
    #设置include symbol筛选
    :param     symbol_list:设置筛选include_symbol的list
    :returns   :
    :raises    error:
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        featuretype = select_param['featuretypes']
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        if symbol_list == '':
            epcam_api.set_select_param(featuretype, False, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)
        else :
            epcam_api.set_select_param(featuretype, True, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)

    except Exception as e:
        print(e)
    return 0


def get_drillpad_symbolname(jobname, step, layer, min_size, drill_symbol, drill_name):
    """
    #拿到当前层小于min_size的孔盘的symbolname list
    :param     jobname:
    :param     step:
    :param     layer:
    :param     min_size:最小润环值
    :param     drill_symbol:
    :param     drill_name:
    :returns   drillpad_list:
    :raises    error:
    """
    try:
        reference_layers = []
        reference_layers.append(drill_name)
        #恢复筛选条件
        set_include_symbol_filter('')
        set_featuretype_filter(65)
        include_symbol= []
        include_symbol.append(drill_symbol[0])
        epcam_api.filter_by_mode(jobname, step, layer, reference_layers, 0, 127, 0 ,include_symbol)
        #获取选中PAD的symbol信息
        global _size
        ret = epcam_api.get_selected_features_report(jobname, step, layer)
        data = json.loads(ret)
        pad_list = data['paras']['pad_list']
        symbol_list = []
        if pad_list == None:
            drillpad_list = []
            return drillpad_list
        else:
            for i in range(0, len(pad_list)):
                if pad_list[i]['symbolname'] not in symbol_list:
                    if pad_list[i]['symbolname'][0] == 'o' :
                        str = pad_list[i]['symbolname']
                        str1 = str[4:]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        if number_1 >= number_2:
                            _size = number_2 * 25400
                        else:
                            _size = number_1 * 25400
                    else:
                        _size = pad_list[i]['symbol_width']
                symbol_list.append([pad_list[i]['symbolname'], _size])

            drillpad_list=[]
            if symbol_list == []:
                return drillpad_list
            else:
                for j in range(0,len(symbol_list)):
                    ann_ring = (symbol_list[j][1] - drill_symbol[1])/2
                    if ann_ring < min_size  and  symbol_list[j] not in drillpad_list:
                        drillpad_list.append(symbol_list[j])
        return drillpad_list

    except Exception as e:
        print(e)
    return 0


def filter_set_include_syms(has_symbols, symbols):
    """
    #添加symbol筛选
    :param     has_symbols:
    :param     symbols:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.filter_set_include_syms(has_symbols, symbols)
    except Exception as e:
        print(e)
    return 0


def change_layer_context(jobname, layer, context):
    """
    #改变layer的context
    :param     jobname:
    :param     layer:
    :param     context:
    :returns   :
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['context'] = context
        epcam_api.change_matrix(jobname, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0


def delete_feature(job, step, layers):
    """
    #删除选中的feature
    :param     job:
    :param     step:
    :param     layers:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.sel_delete(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def reverse_select(job, step, layer):
    """
    #反选
    :param     job:
    :param     step:
    :param     layer:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return 0


def select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear):
    """
    #选中feature
    :param     job:
    :param     step:
    :param     layer:
    :param     selectpolygon:
    :param     featureInfo:
    :param     margin:0:单选 1：多选
    :param     clear:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear)
    except Exception as e:
        print(e)
    return 0


def change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror):
    """
    #修改文字
    :param     job:
    :param     step:
    :param     layers:
    :param     text:
    :param     font:
    :param     x_size:
    :param     y_size:
    :param     width:
    :param     polarity:
    :param     mirror:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror)
    except Exception as e:
        print(e)
    return 0


def sel_break(job, step, layers, sel_type):
    """
    #打散feature
    :param     job:
    :param     step:
    :param     layers:
    :param     sel_type:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.sel_break(job, step, layers, sel_type)
    except Exception as e:
            print(e)
    return 0


def layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height):
    """
    #layer_compare_bmp
    :param     jobname1:
    :param     stepname1:
    :param     layername1:
    :param     jobname2:
    :param     stepname2:
    :param     layername2:
    :param     tolerance:
    :param     grid_size:
    :param     savepath:
    :param     suffix:
    :param     bmp_width:
    :param     bmp_height:
    :returns   :
    :raises    error:
    """
    try:
        epcam_api.layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height)
    except Exception as e:
        print(e)
    return 0



def step_repeat(job, parentstep, childsteps):
    """
    #拼板
    :param     parentstep: panel
    :param     childsteps: 拼入panel的step
    :returns    :
    :raise error:
    """
    try:
        epcam_api.step_repeat(job, parentstep, childsteps)
    except Exception as e:
        print(e)
    return 0

"""
#设置基准点
:param     stepname: step名
:param     point_x: 基准点横坐标
:param     point_y: 基准点纵坐标
:returns    :
:raise error:
"""
def set_datum_point(job, stepname, point_x, point_y):
    try:
        epcam_api.set_datum_point(job, stepname, point_x, point_y)
    except Exception as e:
        print(e)
    return 0

#获取profile宽高
def get_profile_box(job, step):
    try:
        ret = epcam_api.get_profile_box(job, step)
        data = json.loads(ret)
        #print(data['paras']['Xmax'])
        width = data['paras']['Xmax'] - data['paras']['Xmin']
        height = data['paras']['Ymax'] - data['paras']['Ymin']
        pro = [width, height]
        return pro
    except Exception as e:
        print(e)
    return 0

#修改feature的叠放顺序
def sel_index(job, step, layers, mode):
    try:
        epcam_api.sel_index(job, step, layers, mode)
    except Exception as e:
        print(e)
    return 0

#新建profile线
def create_profile(jobname, stepname, layername):
    try:
        epcam_api.create_profile(jobname, stepname, layername)
    except Exception as e:
        print(e)
    return 0

#添加矩形(线)
def add_line_rectangle(job, step, layer, leftbottom_x, leftbottom_y, righttop_x, righttop_y):
    try:
        epcam_api.add_line(job, step, [], layer, 'r10', leftbottom_x, leftbottom_y, leftbottom_x, righttop_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', leftbottom_x, righttop_y, righttop_x, righttop_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', righttop_x, righttop_y, righttop_x, leftbottom_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', righttop_x, leftbottom_y, leftbottom_x, leftbottom_y, 1, 0, [])
    except Exception as e:
        print(e)
    return 0

#获取所有layer名
def get_all_layer_name(job):
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

#获取所有layer名
def get_all_board_name(job):
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                if layer_info[i]['context'] == 'board':
                    layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

#跨层复制layer
def sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    try:
        epcam_api.sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''

def get_soldermask_list(job):
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''


def get_smd_or_bga_symbolname(job, step, layer):
    """
    #拿到选中的smd/bga pad的symbol信息
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        #获取选中PAD的symbol信息
        global _size
        ret = epcam_api.get_selected_features_report(job, step, layer)
        data = json.loads(ret)
        pad_list = data['paras']['pad_list']
        symbol_list = []
        if pad_list == None:
            return symbol_list
        else:
            for i in range(0, len(pad_list)):
                if pad_list[i]['symbolname'] not in symbol_list:
                    try:
                        _size = 0
                        if pad_list[i]['symbol_width'] <= pad_list[i]['symbol_height']:
                            _size = pad_list[i]['symbol_width']
                        else:
                            _size = pad_list[i]['symbol_height']                            
                        symbol_list.append([pad_list[i]['symbolname'], _size])
                    except:
                        continue
        return symbol_list
    except Exception as e:
        print(e)
    return []


def get_soldermask_pad_symbol(job, step, layer, min_size, bga_or_smd_symbol):
    """
    #拿到选中的开窗中需要resize的symbol信息
    :param     job:
    :param     step:
    :param     layer:
    :param     min_size:最小公差
    :param     bga_or_smd_symbol:[(bga/smd)symbolname,size]
    :returns   soldermask_pad_list:需要resize的symbol信息[symbolname,size]
    :raises    error:
    """
    try:
        symbol_list = get_smd_or_bga_symbolname(job, step, layer)

        soldermask_pad_list=[]
        if symbol_list == []:
            return soldermask_pad_list
        else:
            for j in range(0,len(symbol_list)):
                try:
                    if bga_or_smd_symbol[0][0:4] == 'rect' :
                        symbolname = bga_or_smd_symbol[0]
                        str1 = symbolname[4:]
                        if 'r' in str1: 
                            index_r = str1.index('r')
                            str1 = str1[0:index_r-1]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        kaichuangname = symbol_list[j][0]
                        if kaichuangname[0:4] != 'rect':
                            continue
                        str2 = kaichuangname[4:]
                        if 'r' in str2: 
                            index_r = str2.index('r')
                            str2 = str2[0:index_r-1]
                        index_xx = str2.index('x')
                        number_11 = float(str2[:(index_xx)])
                        number_22 = float(str2[(index_xx+1):])
                        if (number_11-number_1)<(number_22-number_2):
                            ann_ring = (number_11-number_1)/2
                        else:
                            ann_ring = (number_22-number_2)/2
                    elif bga_or_smd_symbol[0][0:4] == 'oval' :
                        symbolname = bga_or_smd_symbol[0]
                        str1 = symbolname[4:]
                        if 'r' in str1: 
                            index_r = str1.index('r')
                            str1 = str1[0:index_r-1]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        kaichuangname = symbol_list[j][0]
                        if kaichuangname[0:4] != 'oval':
                            continue
                        str2 = kaichuangname[4:]
                        if 'r' in str2: 
                            index_r = str2.index('r')
                            str2 = str2[0:index_r-1]
                        index_xx = str2.index('x')
                        number_11 = float(str2[:(index_xx)])
                        number_22 = float(str2[(index_xx+1):])
                        if (number_11-number_1)<(number_22-number_2):
                            ann_ring = (number_11-number_1)/2
                        else:
                            ann_ring = (number_22-number_2)/2
                    else:
                        ann_ring = (symbol_list[j][1] - bga_or_smd_symbol[1])/(2*25400)
                    if ann_ring < min_size  and  symbol_list[j] not in soldermask_pad_list:
                        soldermask_pad_list.append(symbol_list[j])
                except:
                    continue
        return soldermask_pad_list

    except Exception as e:
        print(e)
    return 0

def create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin):
    """
    #profile线间新建layer
    :param     jobname:
    :param     stepname:
    :param     new_layername: 新建layer名
    :param     child_profile_margin: 避铜值
    :returns   
    :raises    error:
    """
    try:
        epcam_api.create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin)
    except Exception as e:
        print(e)
    return ''


def get_signal_layers_list(job):
    """
    #获取线路层layer_list
    :param     job:
    :returns   signal_layer_list： 线路层的layer名列表
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        signal_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and (layer_info[i]['type'] == 'signal' or layer_info[i]['type'] == 'power_ground'):
                signal_layer_list.append(layer_info[i]['name'])  
        return signal_layer_list
    except Exception as e:
        print(e)
    return []

def add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location):
    """
    #添加surface
    :param     job:
    :param     step:
    :param     layers:
    :param     layer:
    :param     polarity: 添加surface的极性
    :param     dcode: 自定义，默认0
    :param     isround: false
    :param     attributes:
    :param     points_location: 多边形坐标(首尾闭合)
    :returns   
    :raises    error:
    """
    try:
       epcam_api.add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location)
    except Exception as e:
        print(e)
    return ''

def clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype):
    """
    #区域切割(profile)
    :param     job:
    :param     step:
    :param     layers:
    :param     clipinside: 切割profile线内(外)
    :param     clipcontour: 是否轮廓化
    :param     margin: 0
    :param     featuretype: 筛选feature
    :returns   
    :raises    error:
    """
    try:
       epcam_api.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype)
    except Exception as e:
        print(e)
    return ''

def get_outter_list(job):
    """
    #获取外层list
    :param     job:
    :returns   outter_layer_list:外层layername列表
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        if index_list == []:
            print("no signal layer")
            return []
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        outter_layer_list = []
        outter_layer_list.append(board_layer_list[0])
        if len(board_layer_list) == 1:
            return outter_layer_list
        else: 
            outter_layer_list.append(board_layer_list[-1])
        return outter_layer_list
    except Exception as e:
        print(e)
    return ''

def get_selected_pad_point(job, step, layer):
    """
    #获取选中的中点和symbolname
    :param     job:
    :param     step:
    :param     layer:
    :param     
    :returns   padinfo: pad中点
    :raises    error:
    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        pad_center = []
        if data['paras'] != False:
            for i in range(len(data['paras'])):
               point_symbolname = [data['paras'][i]['X'] * 25400000, data['paras'][i]['Y'] * 25400000, data['paras'][i]['symbolname']]
               pad_center.append(point_symbolname)
        return pad_center
    except Exception as e:
        print(e)
    return []

def get_min_tol(bga_or_smd_symbol, windowing_symbol):
    """
    #拿到选中的开窗中需要resize的symbol信息
    :param     job:
    :param     step:
    :param     layer:
    :param     min_size:最小公差
    :param     bga_or_smd_symbol:[(bga/smd)symbolname,size]
    :returns   soldermask_pad_list:需要resize的symbol信息[symbolname,size]
    :raises    error:
    """
    try:
        symbolname = bga_or_smd_symbol
        kaichuangname = windowing_symbol
        if bga_or_smd_symbol[0:4] == 'rect' or bga_or_smd_symbol[0:4] == 'oval':
            str1 = symbolname[4:]
            if 'r' in str1: 
                index_r = str1.index('r')
                str1 = str1[0:index_r-1]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x+1):])
            if kaichuangname[0:4] != bga_or_smd_symbol[0:4]:
                return 0
            str2 = kaichuangname[4:]
            if 'r' in str2: 
                index_r = str2.index('r')
                str2 = str2[0:index_r-1]
            index_xx = str2.index('x')
            number_11 = float(str2[:(index_xx)])
            number_22 = float(str2[(index_xx+1):])
            if (number_11-number_1)<(number_22-number_2):
                ann_ring = (number_11-number_1)/2
            else:
                ann_ring = (number_22-number_2)/2
        else:
            number_3 = float(symbolname[1:])
            number_4 = float(kaichuangname[1:])
            ann_ring = (number_3 - number_4) / 2
        return ann_ring
    except Exception as e:
        print(e)
    return 0

#整理layer
def arrange_layer(job, backup_layer):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        board_layer_list=[]
        index_list = []
        layer_index = 0
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == '----------':
                layer_index = i 
            if layer_infos[i]['context'] == 'board' and (layer_infos[i]['type'] == 'signal' or layer_infos[i]['type'] == 'solder_mask' or layer_infos[i]['type'] == 'silk_screen'):
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_infos[j]['name'])

        NUM = layer_index+1
        for k in range(0, len(board_layer_list)):
            lenth = len(board_layer_list[k])
            for t in range(layer_index, len(layer_infos)):
                layername = layer_infos[t]['name']
                tt = layername[:lenth]
                if  board_layer_list[k] == layername[:lenth]:
                    if layername[lenth] == '_' or layername[lenth] == '-' or layername[lenth] == '+':
                        epcam_api.move_layer(job, t+1, NUM+1)
                        NUM = NUM + 1
                        ret2 = epcam_api.get_matrix(job)
                        data2 = json.loads(ret2)
                        layer_infos = data2['paras']['info']
        if backup_layer:
            ret3 = epcam_api.get_matrix(job)
            data3 = json.loads(ret3)
            layer_infos = data3['paras']['info']
            layer_index1 = 0
            for l in range(0, len(layer_infos)):
                if layer_infos[l]['name'] == '----------':
                    layer_index1 = l
            for m in range(layer_index1+1, len(layer_infos)):
                #if "_org" not in layer_infos[m]['name'] and "_net" not in layer_infos[m]['name']:
                if "_org" not in layer_infos[m]['name']:
                    pre_layername = layer_infos[m]['name']
                    job_operation.delete_layer(job, pre_layername)
    except Exception as e:
        print(e)
    return 0 

#contour to pad
def contour2pad(job, step, layers, tol, minsize, maxsize, suffix):
    try:
        epcam_api.contour2pad(job, step, layers, tol, minsize, maxsize, suffix)
    except Exception as e:
        print(e)
    return ''


#resize_polyline
def resize_polyline(job, step, layers, size, sel_type):
    try:
        epcam_api.resize_polyline(job, step, layers, size, sel_type)
    except Exception as e:
        print(e)
    return ''

def get_silkscreen_layer(job):
    """
    #获取丝印层layer_list        
    :param     job:     
    :returns   layer_list:丝印层layername列表     
    :raises    error:    
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'silk_screen':
                layer_list.append(layer_info[i]['name'])
        
        if len(layer_list) < 1:
            print("can't find silk_screen-layer!")

        return layer_list
    except Exception as e:
        print(e)
    return ''

#跨层移动feature
def sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    try:
        epcam_api.sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''

#设置显示模式
def set_display_widths(width):
    try:
        epcam_api.set_display_widths(width)
    except Exception as e:
        print(e)
    return ''

#设置文字显示模式
def set_display_text(disp):
    try:
        epcam_api.set_display_text(disp)
    except Exception as e:
        print(e)
    return ''

#设置单位
def set_units(units):
    try:
        epcam_api.set_units(units)
    except Exception as e:
        print(e)
    return ''

#设置是否显示profile线
def set_display_profile(mode):
    try:
        epcam_api.set_display_profile(mode)
    except Exception as e:
        print(e)
    return ''


#contourize
def contourize(job, step, layers, accuracy, separate_to_islands, size, mode):
    try:
        epcam_api.contourize(job, step, layers, accuracy, separate_to_islands, size, mode)
    except Exception as e:
        print(e)
    return ''

#判断gerber或odb
def gerber_or_odb_identify(path, type):
    try:
        if type == 'gerber':
            filelist = os.listdir(path)
            for file in filelist:
                _path = os.path.join(path, file)
                #path = path + '/' + file
                ret = epcam_api.file_identify(_path)
                data = json.loads(ret)
                file_format = data['paras']['format']
                if file_format == 'Gerber274x':
                    return True
            return False
        elif type == 'odb':
            file_path = os.path.dirname(path)
            file_name = os.path.basename(path)
            ret = epcam_api.open_job(file_path, file_name)
            data = json.loads(ret)
            return data['paras']['status']
        else:
            return False
    except Exception as e:
        print(e)
    return ''

#设置模式
def set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude):
    try:
        epcam_api.set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude)
    except Exception as e:
        print(e)
    return 0

#重置设置模式
def reset_selection():
    try:
        epcam_api.set_selection(False, False, False, False, False, False)
    except Exception as e:
        print(e)
    return 0

#通过symbolname获得孔的大小
def get_drillsize_by_symbolname(symbolname):
    try:
        _size = 0
        if symbolname[0:4] == 'oval':
            str1 = symbolname[4:]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x + 1):])
            if number_1 >= number_2:
                _size = number_2 * 25400
            else:
                _size = number_1 * 25400
        else:
            _size = float(symbolname[1:]) * 25400
        return _size
    except Exception as e:
        print(e)
    return 0

#添指定宽高的槽孔
def add_oval_pad(job, step, layer, width, height, location_x, location_y, polarity, dcode, orient, attributes):
    try:
        symbol = 'oval' + str(width) + 'x' + str(height)
        epcam_api.add_pad(job, step, [], layer, symbol, location_x, location_y, polarity, dcode, orient, attributes)
    except Exception as e:
        print(e)
    return 0

#通过symbolname获取槽孔宽高
def get_oval_width_and_height(symbolname):
    try:
        if symbolname[0] == 'o':
            str1 = symbolname[4:]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x + 1):])
            return [number_1, number_2]
    except Exception as e:
        print(e)
    return [] 

#获取选中feature的坐标，symbolname,极性, 角度, 是否镜像
def get_features_infos(job, step, layer):
    """
    #获取选中feature的所有信息
    :param     job:
    :param     step:
    :param     layer:
    :param     
    :returns   featureinfo: feature信息
    :raises    error:
    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            for i in range(len(data['paras'])):
               featureinfo = [data['paras'][i]['X'] * 25400000, data['paras'][i]['Y'] * 25400000, data['paras'][i]['symbolname'],
                              data['paras'][i]['polarity'], data['paras'][i]['angle'], data['paras'][i]['mirror'],
                              data['paras'][i]['XS'], data['paras'][i]['YS'], data['paras'][i]['XE'], data['paras'][i]['YE'],
                              data['paras'][i]['feature_index'], data['paras'][i]['attributes'], data['paras'][i]['xsize'],
                              data['paras'][i]['ysize']]
               featureinfos.append(featureinfo)
        return featureinfos
    except Exception as e:
        print(e)
    return []

#获取选中feature的坐标，symbolname,极性, 角度, 是否镜像
def get_selected_features_infos(job, step, layer):
    """
    #获取选中feature的所有信息
    :param     job:
    :param     step:
    :param     layer:
    :param     
    :returns   featureinfo: feature信息
    :raises    error:
    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return []

#取消选中
def unselect_features(job, step, layer):
    try:
        epcam_api.unselect_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0

#获取该层所有feature数量
def get_all_features_num(job, step, layer):
    try:
        num = 0
        epcam_api.load_layer(job, step, layer)
        ret = epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        if data['paras']['lines_list'] != None:
            if len(data['paras']['lines_list']):
                for i in range(len(data['paras']['lines_list'])):
                    num += data['paras']['lines_list'][i]['count']
        if data['paras']['pad_list'] != None:
            if len(data['paras']['pad_list']):
                for j in range(len(data['paras']['pad_list'])):
                    num += data['paras']['pad_list'][j]['count']
        if data['paras']['surface_list'] != None:
            if len(data['paras']['surface_list']):
                for k in range(len(data['paras']['surface_list'])):
                    num += data['paras']['surface_list'][k]['count']
        if data['paras']['arc_list'] != None:
            if len(data['paras']['arc_list']):
                for v in range(len(data['paras']['arc_list'])):
                    num += data['paras']['arc_list'][v]['count']
        if data['paras']['text_list'] != None:
            if len(data['paras']['text_list']):
                for t in range(len(data['paras']['text_list'])):
                    num += data['paras']['text_list'][t]['count']
        return num
    except Exception as e:
        print(e)
    return 0

#取消选中
def change_feature_symbols(job, step, layers, symbol):
    try:
        epcam_api.change_feature_symbols(job, step, layers, symbol, False)
    except Exception as e:
        print(e)
    return 0
  
#获取layer profile polygon
def get_profile(job, step):
    try:
        return epcam_api.get_profile(job, step)
    except Exception as e:
        print(e)
    return 0

#获取内外层 layer 名
def get_signal_layer_list(job):
    """
    #获取内外层layer 名
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])

        inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return ''

#将一个料号中某一layer的信息拷贝至另一料号中
def copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert):
    """
    #将一个料号中某一layer的信息拷贝至另一料号中
    :param     mode：true代表替换，flase代表追加
    :param     invert：true代表极性反转，flase代表极性不反转
    :returns   
    :raises    error:
    """
    try:
        epcam_api.copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert)
    except Exception as e:
        print(e)
    return ''

#依据polygon 建profile
def create_profile_by_polygon(job, step, layer, poly):
    """
    #依据polygon 建profile
    :param     poly:
    :returns   
    :raises    error:
    """
    try:
        for i in range(len(poly)-1):
            epcam_api.add_line(job, step, [], layer, 'r1', poly[i][0], poly[i][1], poly[i+1][0], poly[i+1][1], 1, 0, [])
        select_features_by_filter(job, step, [layer])
        create_profile(job, step, layer)
        select_features_by_filter(job, step, [layer])
        delete_feature(job, step, [layer])
    except Exception as e:
        print(e)
    return ''

#反选
def counter_election(job, step, layer):
    """
    #反选
    :returns   
    :raises    error:
    """
    try:
        epcam_api.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return ''

#创建阴阳step：
def create_flip(job,step):
    try:
        siglayer=get_signal_layer_list(job)
        smlayer=get_soldermask_list(job)
        drllayer=get_drill_layer_name(job)
        screenlayer=get_silkscreen_layer(job)
        splayer=[]
        allboard=get_all_board_name(job)
        for layer in allboard:
            if (layer not in siglayer) and (layer not in smlayer) and (layer not in drllayer) and (layer not in screenlayer):
                splayer.append(layer)
        stepname=step+'_flip'
        job_operation.create_step(job,stepname)
        poly=get_profile(job,step)
        poly  = json.loads(poly)
        poly = poly["points"]
        orig_poly = []      #左下角pcs profile polygon
        for i in range(len(poly)):
            per_point = []
            per_point.append(-poly[i]["ix"])
            per_point.append(poly[i]["iy"])
            orig_poly.append(per_point)
        create_profile_by_polygon(job, stepname,siglayer[0], orig_poly)
        
        for i in range(len(siglayer)):
            epcam_api.copy_layer_features(job, step, [siglayer[i]], job, stepname, [siglayer[len(siglayer)-1-i]], False, False)
        for i in range(len(smlayer)):
            epcam_api.copy_layer_features(job, step, [smlayer[i]], job, stepname, [smlayer[len(smlayer)-1-i]], False, False)
        for i in range(len(screenlayer)):
            epcam_api.copy_layer_features(job, step, [screenlayer[i]], job, stepname, [screenlayer[len(screenlayer)-1-i]], False, False)   
        for i in range(len(splayer)):
            epcam_api.copy_layer_features(job, step, [splayer[i]], job, stepname, [splayer[len(splayer)-1-i]], False, False)
        for drl in drllayer:    
            num1=drl[3:]
            g=num1.find('-')
            first=int(num1[0:g])
            second=int(num1[g+1:])
            if first==1 and second ==len(siglayer):
                epcam_api.copy_layer_features(job, step, [drl], job, stepname, [drl], False, False)
            else:
                newdrl='drl'+str(len(siglayer)-second+1)+'-'+str(len(siglayer)-first+1)
                if newdrl not in drllayer:
                    job_operation.create_layer(job, newdrl)
                    allboard.append(newdrl)
                    epcam_api.copy_layer_features(job, step, [drl], job, stepname, [newdrl], False, False)
                else:
                    epcam_api.copy_layer_features(job, step, [drl], job, stepname, [newdrl], False, False)

        for layer in allboard:
            epcam_api.transform(job,stepname,layer,0,False,False,True,False,False,{'ix':0,'iy':0},0,1,1,0,0)
    except Exception as e:
        print(e)
    return ''

#改变Matrix
def change_layer_matrix(jobname, layer, context,Type,layname):
    """
    #改变layer的context
    :param     jobname:
    :param     layer:
    :param     context:
    :returns   :
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['context'] = context
                    layer_infos[i]['type'] = Type
                    layer_infos[i]['name']=layname 
        epcam_api.change_matrix(jobname, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0

#获取料号的usersymbol列表
def get_usersymbol_list(job):
    try:
        ret = epcam_api.get_usersymbol_list(job)
        data = json.loads(ret)
        user_list = data['paras']
        return user_list
    except Exception as e:
        print(e)
    return []
