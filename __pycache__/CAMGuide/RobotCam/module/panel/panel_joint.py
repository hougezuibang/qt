import os, sys
PyRecipe_module_pannel_path = os.path.dirname(__file__)
PyRecipe_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\base'
PyRecipe_epcam_path = PyRecipe_base_path + r'\epcam'
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_epcam_path)
import job_operation
import layer_info
import epcam_api
import epcam
import json

#拼板

def step_joint(job, parentstep, childsteps, layername):
    #分析childsteps 若有阴阳拼版信息 则创建flip step
    for childstep in childsteps:
        if not childstep["NAME"] == 'pcs':
            layer_info.create_flip(job, 'pcs')
    layer_info.step_repeat(job, parentstep, childsteps)
    # layer_info.create_layer_between_profile(job, parentstep, layername, 127000)
    # layer_list = []
    # layer_list = layer_info.get_signal_layer_list(job)
    # if len(layer_list):
    #     for i in range(0, len(layer_list)):
    #         layer_info.sel_copy_other(job, parentstep, [layername], [layer_list[i]], False, 0, 0, 0, 0, 0, 0, 0)
    # job_operation.delete_layer(job, 'pcs_array_panel')
    get_set_edge_info(job, parentstep, childsteps)
    #获取板边信息

def get_set_edge_info(job, parentstep, childsteps):
    #获取board layer
    signallayer = layer_info.get_signal_layer_list(job)
    size=len(signallayer)
    solderlayer = layer_info.get_soldermask_list(job)
    drilllayer = layer_info.get_drill_layer_name(job)
    boardlayer = signallayer
    for m in range(len(solderlayer)):
        boardlayer.append(solderlayer[m])
    for ly in range(len(drilllayer)):
        boardlayer.append(drilllayer[ly])

    #区分dxfoutline or setoutline
    all_name = layer_info.get_all_layer_name(job)
    if "set-outline" in all_name:
        #copy orig step
        new_step_name = job_operation.copy_step(job, 'orig')
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
        for v in range(len(boardlayer)):
            layer_info.copy_layer_features(job, new_step_name, [boardlayer[v]], job, "set", [boardlayer[v]], False, False)
        #获取set 防焊层的线
        layer_info.select_features_by_attributes(job, "prepare", ['set-outline'], 1, [{".fiducial_name": "v-cut"}])
        layer_info.counter_election(job, "prepare", 'set-outline')
        layer_info.delete_feature(job, "prepare", ['set-outline'])
        layer_info.copy_layer_features(job, "prepare", ["set-outline"], job, "set", solderlayer, False, False)
        job_operation.delete_step(job, new_step_name)
    elif "dxf-outline" in all_name:
        layer_info.set_selection(True, True, True, True, True, False)
        #按从下到上 从左至右 的顺序依次产生每个pcs profile polygon信息
        pcss_poly = []
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
                    pcss_poly.append(cur_poly)
        for i in range(len(pcss_poly)):
            layer_info.select_feature(job, "prepare", "dxf-outline", pcss_poly[i], {}, 1, False)
            layer_info.delete_feature(job, "prepare", ["dxf-outline"])
        setpoly = layer_info.get_profile(job, 'orig')
        setpoly  = json.loads(setpoly)
        setpoly = setpoly["points"]
        set_poly = []      #左下角pcs profile polygon
        for i in range(len(setpoly)):
            per_point = []
            per_point.append(setpoly[i]["ix"])
            per_point.append(setpoly[i]["iy"])
            set_poly.append(per_point)
        # for t in range(len(set_poly)-1):
        #     epcam_api.add_line(job, "prepare", [], "drl1-4", "r1", set_poly[t][0], set_poly[t][1], set_poly[t+1][0], set_poly[t+1][1], 1, 0, [])
        layer_info.set_featuretype_filter(68)
        layer_info.select_feature(job, "prepare", "dxf-outline", set_poly, {}, 1, False)
        layer_info.reset_select_filter()
        # data2 = {"cmd":"show_layer", "job":job, "step": "prepare", "layer":"dxf-outline"}
        # js = json.dumps(data2)
        # epcam.view_cmd(js)
        ret = epcam_api.get_selected_feature_infos(job, "prepare", "dxf-outline")
        layer_info.clear_select(job, "prepare", "dxf-outline")
        ret=json.loads(ret)
        arcinfo=ret['paras']
        if not arcinfo:
            return
        arclists=[]
        arcss=[]
        b=False
        for arc in arcinfo:
            if arc['XE']==arc['XS'] and arc['YE']==arc['YS']:
                arclists.append(arc)
        for arc in arclists:
            if arcss==[]:
                arcs=[]
                arcs.append(arc)
                arcss.append(arcs)
            else:
                for arcs in arcss:
                    ac1=arcs[0]['XC']-0.001
                    ac2=arcs[0]['XC']+0.001
                    bc1=arcs[0]['YC']-0.001
                    bc2=arcs[0]['YC']+0.001
                    if (arc['XC']>=ac1 and arc['XC']<=ac2)  and (arc['YC']>=bc1 and arc['YC']<=bc2 ):
                        for a in arcs:
                            if arc['D']==a['D']:
                                b=True
                        if b==False:
                            arcs.append(arc)
                            b=True
                            break
                if b==True:
                    b=False
                else:
                    arcs=[]
                    arcs.append(arc)
                    arcss.append(arcs)
                
        #ret = epcam_api.get_selected_features_report(job, "prepare", "dxf-outline")
        outterlayer = layer_info.get_outter_list(job)

        for item in arcss:
            if 1 == len(item):
                D = item[0]["D"]*1000
                linesymbol = item[0]["symbolname"]
                #linwidth = (int)(split(linesymbol)[1])
                # linwidth = (int)(linesymbol[1:])
                symbol1 = "r"+(str)(D)
                symbol2 = "r"+(str)(D+10)
                if len(drilllayer)==1:
                    epcam_api.add_pad(job, "set", [], drilllayer[0], symbol1, (int)(item[0]["XC"]*25400000), (int)(item[0]["YC"]*25400000), 1, 0, 0, [{".drill": "non_plated"}])
                elif len(drilllayer)>1:
                    drlname='drl'+'1'+'-'+str(size)
                    epcam_api.add_pad(job, "set", [], drlname, symbol1, (int)(item[0]["XC"]*25400000), (int)(item[0]["YC"]*25400000), 1, 0, 0, [{".drill": "non_plated"}])
                epcam_api.add_pad(job, "set", solderlayer, solderlayer[0], symbol2, (int)(item[0]["XC"]*25400000), (int)(item[0]["YC"]*25400000), 1, 0, 0, [])
            elif 2 == len(item):
                D1 = item[0]["D"]*1000
                D2 = item[1]["D"]*1000
                # linwidth1 = (int)(item[0]["symbolname"][1:])
                # linwidth2 = (int)(item[1]["symbolname"][1:])
                symbol1 = "r"+(str)(D1)
                symbol2 = "r"+(str)(D2)
                if D1>D2:
                    epcam_api.add_pad(job, "set", outterlayer, outterlayer[0], symbol2, (int)(item[1]["XC"]*25400000), (int)(item[1]["YC"]*25400000), 1, 0, 0, [])
                    epcam_api.add_pad(job, "set", solderlayer, solderlayer[0], symbol1, (int)(item[0]["XC"]*25400000), (int)(item[0]["YC"]*25400000), 1, 0, 0, [])
                else:
                    epcam_api.add_pad(job, "set", outterlayer, outterlayer[0], symbol1, (int)(item[0]["XC"]*25400000), (int)(item[0]["YC"]*25400000), 1, 0, 0, [])
                    epcam_api.add_pad(job, "set", solderlayer, solderlayer[0], symbol2, (int)(item[1]["XC"]*25400000), (int)(item[1]["YC"]*25400000), 1, 0, 0, [])
        # data2 = {"cmd":"show_layer", "job":job, "step": "set", "layer":"l1"}
        # js = json.dumps(data2)
        # epcam.view_cmd(js)