import os, sys
PyRecipe_module_pannel_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
sys.path.append(PyRecipe_base_path)
import job_operation
import layer_info
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
sys.path.append(PyRecipe_epcam_path)
import epcam
import json

#创建拼板的step,画出profile线
def create_step(job, step, leftbottom_x, leftbottom_y, righttop_x, righttop_y):
    layer_info.reset_select_filter()
    job_operation.create_step(job, step)
    layerlist = []
    layerlist = layer_info.get_all_layer_name(job)
    if len(layerlist):
        #set profile 线
        poly = layer_info.get_profile(job, 'orig')
        poly  = json.loads(poly)
        if len(poly) == 1:
            return
        poly = poly["points"]
        set_poly = []      #set profile polygon
        for i in range(len(poly)):
            per_point = []
            per_point.append(poly[i]["ix"])
            per_point.append(poly[i]["iy"])
            set_poly.append(per_point)
        layer_info.create_profile_by_polygon(job, step, layerlist[0], set_poly)

        # layer_info.add_line_rectangle(job, step, layerlist[0], leftbottom_x, leftbottom_y, righttop_x, righttop_y)
        # select_poligon = [[leftbottom_x - 2540000, leftbottom_y - 2540000],
        #                   [leftbottom_x - 2540000, righttop_y + 2540000],
        #                   [righttop_x + 2540000, righttop_y + 2540000],
        #                   [righttop_x + 2540000, leftbottom_y - 2540000],
        #                   [leftbottom_x - 2540000, leftbottom_y - 2540000]]
        # layer_info.select_feature(job, step, layerlist[0], select_poligon, {}, 1, False)
        # layer_info.create_profile(job, step, layerlist[0])
        # layer_info.select_feature(job, step, layerlist[0], select_poligon, {}, 1, False)
        # layer_info.delete_feature(job, step, [layerlist[0]])

#panel向外铺铜
def paveCu_outward(job, step, leftbottom_x, leftbottom_y, righttop_x, righttop_y, out_x, out_y):
    job_operation.create_layer(job, 'pavecu_outward_area')
    select_poligon = [[leftbottom_x - out_x, leftbottom_y - out_y],
                     [leftbottom_x - out_x, righttop_y + out_y],
                     [righttop_x + out_x, righttop_y + out_y],
                     [righttop_x + out_x, leftbottom_y - out_y],
                     [leftbottom_x - out_x, leftbottom_y - out_y]]
    layer_info.add_surface(job, step, [], 'pavecu_outward_area', 1, 0, False, [], select_poligon)
    layer_info.clip_area_use_profile(job, step, ['pavecu_outward_area'], True, True, 0, 127)
    layer_list = []
    layer_list = layer_info.get_signal_layer_list(job)
    if len(layer_list):
        for i in range(0, len(layer_list)):
            layer_info.sel_copy_other(job, step, ['pavecu_outward_area'], [layer_list[i]], False, 0, 0, 0, 0, 0, 0, 0)
