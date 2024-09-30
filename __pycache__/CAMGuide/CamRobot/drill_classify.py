import os, sys, json
import import_camflow_path
import layer_info
import epcam

#孔分类选中
def classify(job, step, layers, logic, attributes, featuretype):#, symbols):  
    if len(layers):
        #清空所有筛选
        layer_info.reset_select_filter()
        #属性筛选
        layer_info.set_attribute_filter(logic, attributes)
        #feature类型筛选
        layer_info.select_features_by_featuretype(job, step, layers, featuretype)
        #layer_info.select_features_by_attributes(job, step, layers, logic, attributes)
        #清空所有选择 
        #layer_info.clear_select(job, step, layers[0])
        #大小筛选
        #layer_info.set_size_filter(symbols)
        #选中feature
        layer_info.select_features_by_filter(job, step, layers)

        #epcam.show(r'C:\project\EPCAM\trunk\EPCAM\EP-CAM-Engineering\job',job,step,layers[0])

        #layer_info.clear_select(job, step, layers[0])
    
    









