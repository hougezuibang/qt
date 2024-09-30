import os, sys, json
PyRecipe_module_outter_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_path + r'\epcam')
import layer_info
import feature_resize
import job_operation
import epcam_api
import epcam
import analysis_dfm 

def silkscreen_linearc_resize(job, step, silk_line_width):
    """
    #丝印层resize Line和Arc
    :param     job:
    :param     step:
    :param     silk_line_width:Line和Arc的宽度
    :returns   :
    :raises    error:
    """
    try:
        #获取丝印层
        silkscreen_layer = layer_info.get_silkscreen_layer(job)
        if silkscreen_layer == []:
            return 0
        for i in range (len(silkscreen_layer)):
            #根据属性筛选出Line
            epcam_api.open_layer(job, step, silkscreen_layer[i])
            layer_info.reset_select_filter()
            featuretype = 70
            layer_info.select_features_by_featuretype(job, step, [silkscreen_layer[i]], featuretype)
            #获取所有选中的线的信息
            data = epcam_api.get_selected_features_report(job, step, silkscreen_layer[i])
            report = json.loads(data)
            if report['paras']['lines_list']:
                line_report = report['paras']['lines_list']
            else:
                print('there is no line in silk_screen layer : ' + silkscreen_layer[i])
                continue
            symbol_info = []
            #判断是否需要resize
            for j in range(len(line_report)):
                symbol_info = [line_report[j]['symbolname'], line_report[j]['symbol_width']]
                epcam_api.clear_selected_features(job, step, silkscreen_layer[i])
                layer_info.reset_select_filter()
                layer_info.set_include_symbol_filter([symbol_info[0]])
                layer_info.select_features_by_filter(job, step, [silkscreen_layer[i]])   #选中
                size = ((silk_line_width * 25400) - symbol_info[1])
                if size > 0:
                    epcam_api.resize_global(job, step, [silkscreen_layer[i]], 0, size)
                epcam_api.clear_selected_features(job, step, silkscreen_layer[i])
    except:
        print('silkscreen_linearc_resize skip')

            
def silkscreen_text_resize(job, step, silk_tall, silk_width, silk_line_width):
    """
    #丝印层resize Text
    :param     job:
    :param     step:
    :param     silk_tall:字体的高度
    :param     silk_width:字体的宽度
    :returns   :
    :raises    error:
    """  
    try:
        #获取丝印层
        silkscreen_layer = layer_info.get_silkscreen_layer(job)
        if silkscreen_layer == []:
            return 0
        for i in range (len(silkscreen_layer)):
            #选中Text
            epcam_api.open_layer(job, step, silkscreen_layer[i])
            layer_info.reset_select_filter()
            featuretype = 80
            layer_info.select_features_by_featuretype(job, step, [silkscreen_layer[i]], featuretype)
            #获取选中的text信息
            data = epcam_api.get_selected_features_report(job, step, silkscreen_layer[i])
            data2 = epcam_api.get_selected_feature_infos(job, step, silkscreen_layer[i])
            report = json.loads(data)
            if report['paras']['text_list']:
                text_report = report['paras']['text_list']
            else:
                #print('there is no text in silk_screen layer : ' + silkscreen_layer[i])
                continue
            #resize
            epcam_api.change_text(job, step, [silkscreen_layer[i]], "", "standard", silk_width * 25400, silk_tall * 25400, silk_line_width * 25400, 0, 0)
    except:
        print('silkscreen_text_resize skip')
