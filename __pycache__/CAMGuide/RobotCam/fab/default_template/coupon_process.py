import os,sys,json
#PyRecipe_path = os.path.dirname(os.path.realpath(__file__))
PyRecipe_path=os.getcwd()
PyRecipe_base_path=PyRecipe_path+r"\base"
PyRecipe_base_epcam_path=PyRecipe_path+r"\base\epcam"
sys.path.append(PyRecipe_base_path)
sys.path.append(PyRecipe_base_epcam_path)
import job_operation
import layer_info 
import epcam 
import epcam_api
import feature_resize

def draw_coupon(date,job):
    try:
        #date=job_operation.load_json(json_data)
        if date['profile_box_high']==0 or date['profile_box_wide']==0 or date['avoid_cu_global']==0 or date['npth_size']==0 or date['pth_size']==0 or date['pth_ring']==0 or date['pth_to_gnd_drill']==0\
            or (date['differential_line_info']==[] and date['single_end_line_info']==[]):
            return []
        x_margin=date['spacing']*25400
        y_margin=date['spacing']*25400
        npth_size=date['npth_size']*25400
        pth_size=date['pth_size']*25400
        pth_ring=date['pth_ring']*25400
        avoid_cu_global=date['avoid_cu_global']*25400
        clearance=date['clearance']*25400
        pth_to_gnd_drill=date['pth_to_gnd_drill']*25400
        min_cu_width=date['min_cu_width']*25400
        xmin=0
        ymin=0
        ymax=date['profile_box_high']*25400
        xmax=date['profile_box_wide']*25400
        # single_lines=[]
        # differential_lines=[]
        # for sig in date['single_end_line_info']:
        #     single_lines.append(sig)
        # for dif in date['differential_line_info']:
        #     single_lines.append(dif)
        single_lines=date['single_end_line_info']
        differential_lines=date['differential_line_info']


        sigs=[]
        difs=[]
        bo=False
        for sigline in single_lines:
            sigline['avoid_cu_spacing']=sigline['avoid_cu_spacing']*25400
            sigline['linewidth']=sigline['linewidth']*25400
            if(len(sigs)==0):
                sig=[]
                sig.append(sigline)
                sigs.append(sig)
            else:
                for sig in sigs:
                    if( len( sigline['reference_layers'] ) == len( sig[0]['reference_layers'] ) ):
                        if( len(sigline['reference_layers'])==1 ):
                            if(sigline['reference_layers'][0]==sig[0]['reference_layers'][0]):
                                sig.append(sigline)
                                bo=True
                                break

                        elif(len(sigline['reference_layers'])==2):
                            if( (sigline['reference_layers'][0]==sig[0]['reference_layers'][0] and sigline['reference_layers'][1]==sig[0]['reference_layers'][1])
                            or( sigline['reference_layers'][0]==sig[0]['reference_layers'][1] and sigline['reference_layers'][1]==sig[0]['reference_layers'][0])):
                                sig.append(sigline)
                                bo=True
                                break
                if(bo==True):
                    bo=False
                else:
                    sig=[]
                    sig.append(sigline)
                    sigs.append(sig)
                                                    
        for difline in differential_lines:
            difline['avoid_cu_spacing']=difline['avoid_cu_spacing']*25400
            difline['line_spacing']=difline['line_spacing']*25400
            difline['linewidth']=difline['linewidth']*25400
            if(len(difs)==0):
                dif=[]
                dif.append(difline)
                difs.append(dif)
            else:
                for dif in difs:
                    if( len( difline['reference_layers'] ) == len( dif[0]['reference_layers'] ) ):
                        if( len(difline['reference_layers'])==1 ):
                            if(difline['reference_layers'][0]==dif[0]['reference_layers'][0]):
                                dif.append(difline)
                                bo=True
                                break

                        elif(len(difline['reference_layers'])==2):
                            if( (difline['reference_layers'][0]==dif[0]['reference_layers'][0] and difline['reference_layers'][1]==dif[0]['reference_layers'][1])
                            or( difline['reference_layers'][0]==dif[0]['reference_layers'][1] and difline['reference_layers'][1]==dif[0]['reference_layers'][0])):
                                dif.append(difline)
                                bo=True
                                break
                if(bo==True):
                    bo=False
                else:
                    dif=[]
                    dif.append(difline)
                    difs.append(dif)

    
    
    
    
        sxmin=xmin
        symin=ymin
        sxmax=xmax
        symax=ymax
        points=[{'ix':sxmin,'iy':symin},{'ix':sxmin,'iy':symax},{'ix':sxmax,'iy':symax},{'ix':sxmax,'iy':symin},{'ix':sxmin,'iy':symin}]

        pointsur=[[sxmin+x_margin,symin+y_margin],[sxmin+x_margin,symax-y_margin],[sxmax-x_margin,symax-y_margin],[sxmax-x_margin,symin+y_margin],[sxmin+x_margin,symin+y_margin]]
    

        drill_layer = layer_info.get_drill_layer_name(job) #孔层的名字
        signal_layer=layer_info.get_signal_layer_list(job)  #信号层名字
        sm_layer=layer_info.get_soldermask_list(job)

        npth_x1=xmin+x_margin+avoid_cu_global+npth_size/2+20*25400
        npth_x2=xmax-x_margin-avoid_cu_global-npth_size/2-20*25400
        npth_y=int((ymax+ymin)/2)
        npthname='r'+str(npth_size/25400)



        xmin=xmin+x_margin+2*avoid_cu_global+npth_size+40*25400
        xmax=xmax-x_margin-2*avoid_cu_global-npth_size-40*25400        ##去除NPTH孔后的布孔矩形大小

        date1=epcam_api.get_coupon_single_end_drill_positions(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance, 
                                            pth_to_gnd_drill, min_cu_width, single_lines, differential_lines)
        
        date1 = json.loads(date1)
        if date1['paras'] == None:
            return []
        
        single_group_count=date1['paras']['single_drill']
        diff_group_count=date1['paras']['differntial_drill']
        if single_group_count==0 and diff_group_count==0:
            return []
        if 'drill_positions' not in date1['paras']:
            return []
        drill_positions=date1['paras']['drill_positions']
        date2=epcam_api.get_coupon_drill_line_relations(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance, 
                                            pth_to_gnd_drill, min_cu_width, single_lines, differential_lines, single_group_count, diff_group_count, drill_positions)
        
        date2 = json.loads(date2)
        steps=[]
        layers_feature_ids={}   #记录线的id 避铜
        map1={} #记录孔的参考层
        map2={} #记录线的名字
        for layer in signal_layer:
            map2[layer]=[]
        i=0
        k=0
        while(i<len(drill_positions)):   #add 孔
            step='coupon'+str(i+1)
            temp_steps=job_operation.get_all_steps(job)
            while step in temp_steps:
                i=i+1
                step='coupon'+str(i+1)
            steps.append(step)
            layers_feature_ids[step]={}
            for layer in signal_layer:
                layers_feature_ids[step][layer]=[]
            map1[step]={}
            job_operation.create_step(job,step)
            epcam_api.set_step_profile(job,step,points)
            epcam_api.add_surface(job,step,signal_layer,signal_layer[0],1,0,False,[],pointsur)
            epcam_api.add_pad(job, step,[],drill_layer[0], npthname, npth_x1, npth_y, 1, 0, 0, [{'.drill':'non_plated'}])
            #epcam_api.add_pad(job, step,signal_layer,signal_layer[0], npthname+'20', npth_x1, npth_y, 1, 0, -1, [{'.drill':'non_plated'}])
            epcam_api.add_pad(job, step,[],drill_layer[0], npthname, npth_x2, npth_y, 1, 0, 0, [{'.drill':'non_plated'}])
        # epcam_api.add_pad(job, step,signal_layer,signal_layer[0], npthname, npth_x2, npth_y, 1, 0, -1, [{'.drill':'non_plated'}])
    
            sig_drills=drill_positions[k]['single_end_line_drill_infos']
            dif_drills=drill_positions[k]['differential_line_drill_infos']
        
            for sig_drill in sig_drills:
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),sig_drill['bottom_point']['ix'],sig_drill['bottom_point']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),sig_drill['middle_point']['ix'],sig_drill['middle_point']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),sig_drill['top_point']['ix'],sig_drill['top_point']['iy'],1,0,0,[{'.drill':'plated'}])
            for dif_drill in dif_drills:
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['bottom_point_l']['ix'],dif_drill['bottom_point_l']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['bottom_point_r']['ix'],dif_drill['bottom_point_r']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['middle_point_l']['ix'],dif_drill['middle_point_l']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['middle_point_r']['ix'],dif_drill['middle_point_r']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['top_point_l']['ix'],dif_drill['top_point_l']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,[],drill_layer[0],'r'+str(pth_size/25400),dif_drill['top_point_r']['ix'],dif_drill['top_point_r']['iy'],1,0,0,[{'.drill':'plated'}])
            i=i+1
            k=k+1

        wid=int(pth_size+2*pth_ring+2*avoid_cu_global+min_cu_width)*0.8
        xsize=int((pth_size+2*pth_ring+2*avoid_cu_global+min_cu_width)/5)
        ysize=int(xsize*3/2)
        linewid=int(xsize/5)
        y=int((ymax-ymin)/2)
        index1=0   #step 个数
        index2=0   #一个step上单孔的组数
        drill_index=0
        for sig in sigs:
            i=0
            while(i<len(sig)):
                if(index2==len(drill_positions[index1]['single_end_line_drill_infos'])):
                    index1=index1+1
                    index2=0
                if(i<len(sig)-1):
                    toppoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['top_point'] 
                    midpoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['middle_point']
                    botpoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['bottom_point']
                    line_points=date2['paras'][index1]  #每层step的线
                    line_top=[]
                    line_bot=[]
                    for linepoint in line_points:
                        if linepoint['point']==toppoint:
                            line_top=linepoint['points']
                        if linepoint['point']==botpoint:
                            line_bot=linepoint['points']
                    stepname=steps[index1]
                    map1[stepname][midpoint['ix']]=[]
                    for ref in sig[i]['reference_layers']:
                        map1[stepname][midpoint['ix']].append(ref)
                
                    map1[stepname][midpoint['ix']].append(sig[i]['layername'])
                    #add两次\
                    j=0
                    k=0
                    while(j<(len(line_top)-1)):
                        epcam_api.add_line(job,steps[index1],[],sig[i]['layername'],'r'+str(sig[i]['linewidth']/25400),line_top[j]['ix'],line_top[j]['iy'],line_top[j+1]['ix'],line_top[j+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][sig[i]['layername']]==[]:
                            layername=sig[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][sig[i]['layername']][len(layers_feature_ids[steps[index1]][sig[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][sig[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        j=j+1
                    if map2[sig[i]['layername']]==[]:
                        map2[sig[i]['layername']].append(1)
                        textname=sig[i]['layername']+'-'+'1'
                        localx=toppoint['ix']-wid/2
                        localy=toppoint['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[sig[i]['layername']][len(map2[sig[i]['layername']])-1]
                        map2[sig[i]['layername']].append(id+1)
                        textname=sig[i]['layername']+'-'+str(id+1)
                        localx=toppoint['ix']-wid/2
                        localy=toppoint['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                        #epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                        
                    i=i+1
                    while(k<(len(line_bot)-1)):
                        epcam_api.add_line(job,steps[index1],[],sig[i]['layername'],'r'+str(sig[i]['linewidth']/25400),line_bot[k]['ix'],line_bot[k]['iy'],line_bot[k+1]['ix'],line_bot[k+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][sig[i]['layername']]==[]:
                            layername=sig[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][sig[i]['layername']][len(layers_feature_ids[steps[index1]][sig[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][sig[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        k=k+1
                
                    if map2[sig[i]['layername']]==[]:
                        map2[sig[i]['layername']].append(1)
                        textname=sig[i]['layername']+'-'+'1'
                        localx=toppoint['ix']-wid/2
                        localy=botpoint['iy']+pth_size+pth_ring+avoid_cu_global
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                        #epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[sig[i]['layername']][len(map2[sig[i]['layername']])-1]
                        map2[sig[i]['layername']].append(id+1)
                        textname=sig[i]['layername']+'-'+str(id+1)
                        localx=toppoint['ix']-wid/2
                        localy=botpoint['iy']+pth_size+pth_ring+avoid_cu_global
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                        #epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    index2=index2+1
                    i=i+1       
                else:
                    #add一次
                    toppoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['top_point'] 
                    midpoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['middle_point']
                    botpoint=drill_positions[index1]['single_end_line_drill_infos'][index2]['bottom_point']
                    stepname=steps[index1]
                    map1[stepname][midpoint['ix']]=[]
                    for ref in sig[i]['reference_layers']:
                        map1[stepname][midpoint['ix']].append(ref)
                    map1[stepname][midpoint['ix']].append(sig[i]['layername'])
                    line_points=date2['paras'][index1]  #每层step的线
                    line_top=[]
                    for linepoint in line_points:
                        if linepoint['point']==toppoint:
                            line_top=linepoint['points']
                    j=0
                    while(j<(len(line_top)-1)):
                        epcam_api.add_line(job,steps[index1],[],sig[i]['layername'],'r'+str(sig[i]['linewidth']/25400),line_top[j]['ix'],line_top[j]['iy'],line_top[j+1]['ix'],line_top[j+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][sig[i]['layername']]==[]:
                            layername=sig[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][sig[i]['layername']][len(layers_feature_ids[steps[index1]][sig[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][sig[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],sig[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[sig[i]['layername']],sig[i]['layername'],sig[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], sig[i]['layername']) 
                        j=j+1
                    if map2[sig[i]['layername']]==[]:
                        map2[sig[i]['layername']].append(1)
                        textname=sig[i]['layername']+'-'+'1'
                        localx=toppoint['ix']-wid/2
                        localy=toppoint['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[sig[i]['layername']][len(map2[sig[i]['layername']])-1]
                        map2[sig[i]['layername']].append(id+1)
                        textname=sig[i]['layername']+'-'+str(id+1)
                        localx=toppoint['ix']-wid/2
                        localy=toppoint['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    index2=index2+1
                    i=i+1


        index3=0  #一个step上差分孔的组数
        for dif in difs:
            i=0
            while(i<len(dif)):
                if(index3==len(drill_positions[index1]['differential_line_drill_infos'])):
                        index1=index1+1
                        index3=0
                if(i<len(dif)-1):  #add 两次
                    toppoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['top_point_l'] 
                    toppoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['top_point_r'] 
                    midpoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['middle_point_l']
                    midpoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['middle_point_r']
                    botpoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['bottom_point_l']
                    botpoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['bottom_point_r']
                    line_points=date2['paras'][index1]  #每层step的线
                    stepname=steps[index1]
                    map1[stepname][midpoint_l['ix']]=[]
                    map1[stepname][midpoint_r['ix']]=[]
                    for ref in dif[i]['reference_layers']:
                        map1[stepname][midpoint_l['ix']].append(ref)
                        map1[stepname][midpoint_r['ix']].append(ref)


                    map1[stepname][midpoint_l['ix']].append(dif[i]['layername'])

                    map1[stepname][midpoint_r['ix']].append(dif[i]['layername'])
                    line_top_l=[]
                    line_top_r=[]
                    line_bot_l=[]
                    line_bot_r=[]
                    for linepoint in line_points:
                        if linepoint['point']==toppoint_l:
                            line_top_l=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==botpoint_l:
                            line_bot_l=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==toppoint_r:
                            line_top_r=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==botpoint_r:
                            line_bot_r=linepoint['points']
                    
                    line_top_l[len(line_top_l)-1]['iy']=line_top_r[len(line_top_r)-1]['iy']+dif[i]['line_spacing']+dif[i]['linewidth']
                    line_top_l[len(line_top_l)-2]['iy']=line_top_r[len(line_top_r)-1]['iy']+dif[i]['line_spacing']+dif[i]['linewidth']

                    j=0
                    k=0
                    while(j<(len(line_top_l)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_top_l[j]['ix'],line_top_l[j]['iy'],line_top_l[j+1]['ix'],line_top_l[j+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        j=j+1
        
                    while(k<(len(line_top_r)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_top_r[k]['ix'],line_top_r[k]['iy'],line_top_r[k+1]['ix'],line_top_r[k+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        k=k+1
                    if map2[dif[i]['layername']]==[]:
                        map2[dif[i]['layername']].append(1)
                        textname=dif[i]['layername']+'-'+'1'
                        localx=toppoint_l['ix']
                        localy=toppoint_l['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[dif[i]['layername']][len(map2[dif[i]['layername']])-1]
                        map2[dif[i]['layername']].append(id+1)
                        textname=dif[i]['layername']+'-'+str(id+1)
                        localx=toppoint_l['ix']
                        localy=toppoint_l['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    i=i+1
                    line_bot_l[len(line_bot_l)-1]['iy']=line_bot_r[len(line_bot_r)-1]['iy']-dif[i]['line_spacing']-dif[i]['linewidth']
                    line_bot_l[len(line_bot_l)-2]['iy']=line_bot_r[len(line_bot_r)-1]['iy']-dif[i]['line_spacing']-dif[i]['linewidth']
                    j=0
                    k=0
                    while(j<(len(line_bot_l)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_bot_l[j]['ix'],line_bot_l[j]['iy'],line_bot_l[j+1]['ix'],line_bot_l[j+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        j=j+1

                    while(k<(len(line_bot_r)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_bot_r[k]['ix'],line_bot_r[k]['iy'],line_bot_r[k+1]['ix'],line_bot_r[k+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        k=k+1
                    if map2[dif[i]['layername']]==[]:
                        map2[dif[i]['layername']].append(1)
                        textname=dif[i]['layername']+'-'+'1'
                        localx=toppoint_l['ix']
                        localy=botpoint_l['iy']+pth_size+pth_ring+avoid_cu_global
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    # epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[dif[i]['layername']][len(map2[dif[i]['layername']])-1]
                        map2[dif[i]['layername']].append(id+1)
                        textname=dif[i]['layername']+'-'+str(id+1)
                        localx=toppoint_l['ix']
                        localy=botpoint_l['iy']+pth_size+pth_ring+avoid_cu_global
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    #  epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)               
                    i=i+1
                    index3=index3+1
                    # if(index3>len(drill_positions[index1]['differential_line_drill_infos'])):
                    #     index1=index1+1
                    #     index3=0
                else: #add yici
                    toppoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['top_point_l'] 
                    toppoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['top_point_r'] 
                    midpoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['middle_point_l']
                    midpoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['middle_point_r']
                    botpoint_l=drill_positions[index1]['differential_line_drill_infos'][index3]['bottom_point_l']
                    botpoint_r=drill_positions[index1]['differential_line_drill_infos'][index3]['bottom_point_r']
                    line_points=date2['paras'][index1]  #每层step的线
                    stepname=steps[index1]
                    map1[stepname][midpoint_l['ix']]=[]
                    map1[stepname][midpoint_r['ix']]=[]
                    for ref in dif[i]['reference_layers']:
                        map1[stepname][midpoint_l['ix']].append(ref)
                        map1[stepname][midpoint_r['ix']].append(ref)

                    map1[stepname][midpoint_l['ix']].append(dif[i]['layername'])
            
                    map1[stepname][midpoint_r['ix']].append(dif[i]['layername'])

                    line_top_l=[]
                    line_top_r=[]
                    line_bot_l=[]
                    line_bot_r=[]
                    for linepoint in line_points:
                        if linepoint['point']==toppoint_l:
                            line_top_l=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==botpoint_l:
                            line_bot_l=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==toppoint_r:
                            line_top_r=linepoint['points']
                    for linepoint in line_points:
                        if linepoint['point']==botpoint_r:
                            line_bot_r=linepoint['points']
                    
                    line_top_l[len(line_top_l)-1]['iy']=line_top_r[len(line_top_r)-1]['iy']+dif[i]['line_spacing']+dif[i]['linewidth']
                    line_top_l[len(line_top_l)-2]['iy']=line_top_r[len(line_top_r)-1]['iy']+dif[i]['line_spacing']+dif[i]['linewidth']

                    j=0
                    k=0
                    while(j<(len(line_top_l)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_top_l[j]['ix'],line_top_l[j]['iy'],line_top_l[j+1]['ix'],line_top_l[j+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        j=j+1
                    while(k<(len(line_top_r)-1)):
                        epcam_api.add_line(job,steps[index1],[],dif[i]['layername'],'r'+str(dif[i]['linewidth']/25400),line_top_r[k]['ix'],line_top_r[k]['iy'],line_top_r[k+1]['ix'],line_top_r[k+1]['iy'],1,0,[])
                        if layers_feature_ids[steps[index1]][dif[i]['layername']]==[]:
                            layername=dif[i]['layername']
                            layers_feature_ids[steps[index1]][layername].append(1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        else:
                            id=layers_feature_ids[steps[index1]][dif[i]['layername']][len(layers_feature_ids[steps[index1]][dif[i]['layername']])-1]
                            layers_feature_ids[steps[index1]][dif[i]['layername']].append(id+1)
                            epcam_api.select_feature_by_id(job,steps[index1],dif[i]['layername'],[id+1])
                            epcam_api.clip_area_use_reference(job,steps[index1],[dif[i]['layername']],dif[i]['layername'],dif[i]['avoid_cu_spacing'],True,0x48)
                            layer_info.clear_select(job, steps[index1], dif[i]['layername']) 
                        k=k+1
                    if map2[dif[i]['layername']]==[]:
                        map2[dif[i]['layername']].append(1)
                        textname=dif[i]['layername']+'-'+'1'
                        localx=toppoint_l['ix']
                        localy=toppoint_l['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    #  epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    else:
                        id=map2[dif[i]['layername']][len(map2[dif[i]['layername']])-1]
                        map2[dif[i]['layername']].append(id+1)
                        textname=dif[i]['layername']+'-'+str(id+1)
                        localx=toppoint_l['ix']
                        localy=toppoint_l['iy']-pth_size-pth_ring-avoid_cu_global-ysize/2
                        epcam_api.add_text(job,steps[index1],signal_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,-1,0,0,[],[])
                    #  epcam_api.add_text(job,steps[index1],sm_layer[0],'','standard',textname,xsize,ysize,linewid,localx,localy,1,0,0,[],[])
                        if len(layers_feature_ids[steps[index1]][signal_layer[0]])==0:
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(1)
                        else:
                            id=layers_feature_ids[steps[index1]][signal_layer[0]][len(layers_feature_ids[steps[index1]][signal_layer[0]])-1]
                            layers_feature_ids[steps[index1]][signal_layer[0]].append(id+1)
                    i=i+1
                    index3=index3+1
        i=0
        layer_info.set_featuretype_filter(65)
        while(i<len(drill_positions)):   #add 孔pad
            step=steps[i]
            sig_drills=drill_positions[i]['single_end_line_drill_infos']
            dif_drills=drill_positions[i]['differential_line_drill_infos']
            for sig_drill in sig_drills:
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),sig_drill['bottom_point']['ix'],sig_drill['bottom_point']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),sig_drill['top_point']['ix'],sig_drill['top_point']['iy'],1,0,0,[{'.drill':'plated'}])
            for dif_drill in dif_drills:
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),dif_drill['bottom_point_l']['ix'],dif_drill['bottom_point_l']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),dif_drill['bottom_point_r']['ix'],dif_drill['bottom_point_r']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),dif_drill['top_point_l']['ix'],dif_drill['top_point_l']['iy'],1,0,0,[{'.drill':'plated'}])
                epcam_api.add_pad(job,step,signal_layer,signal_layer[0],'r'+str(pth_size/25400+pth_ring/25400),dif_drill['top_point_r']['ix'],dif_drill['top_point_r']['iy'],1,0,0,[{'.drill':'plated'}])
            layer_info.select_features_by_filter(job, step, signal_layer)
            epcam_api.clip_area_use_reference(job, step, signal_layer, signal_layer[0], avoid_cu_global, True, 0x48)
            for layer in signal_layer:
                layer_info.clear_select(job, step, layer)
            i=i+1
        layer_info.reset_select_filter()
        for cname in map1:             #add 接地孔
            for layer in signal_layer:
                for px in map1[cname]:
                    if map1[cname][px].count(layer)!=0:
                        epcam_api.add_pad(job,cname,[],layer,'s'+str(pth_size/25400+pth_ring/25400),px,y,1,0,0,[])
                    else:
                        if layer==signal_layer[0]:
                        # epcam_api.add_pad(job,cname,[],sm_layer[0],'s'+str(pth_size/25400+pth_ring/25400+clearance/25400),px,y,1,0,0,[])
                            epcam_api.add_pad(job,cname,[],layer,'s'+str(pth_size/25400+pth_ring/25400),px,y,1,0,0,[])
                        elif layer ==signal_layer[len(signal_layer)-1]:
                        # epcam_api.add_pad(job,cname,[],sm_layer[len(sm_layer)-1],'s'+str(pth_size/25400+pth_ring/25400+clearance/25400),px,y,1,0,0,[])
                            epcam_api.add_pad(job,cname,[],layer,'s'+str(pth_size/25400+pth_ring/25400),px,y,1,0,0,[])
                        else:
                            epcam_api.add_pad(job,cname,[],layer,'r'+str(pth_size/25400+pth_ring/25400),px,y,-1,0,0,[])

        # for step in steps:
        #     for layer in signal_layer:
        #         layer_info.set_featuretype_filter(72)
        #         layer_info.select_features_by_filter(job, step, signal_layer)
        #         layer_info.reset_select_filter()
        #         layer_info.set_featuretype_filter(33)
        #         layer_info.select_features_by_filter(job, step, signal_layer)
        #         layer_info.reset_select_filter()
        #         accuracy = 0.25 * 25400
        #         separate_to_islands = True
        #         size = 3.0 * 25400
        #         mode = 0
        #         layer_info.contourize(job, step, [layer], accuracy, separate_to_islands, size, mode)
        #     for layer in signal_layer:
        #         layer_info.clear_select(job, step, layer)



        for step in steps:        #  防焊开窗
            layer_info.set_featuretype_filter(65)
            layer_info.select_features_by_filter(job,step,[signal_layer[0]])
            layer_info.sel_copy_other(job, step, [signal_layer[0]],[sm_layer[0]], False, 0, 0, 0, clearance, 0, 0, 0)
            layer_info.clear_select(job, step, signal_layer[0])
            layer_info.select_features_by_filter(job,step,[signal_layer[len(signal_layer)-1]])
            layer_info.sel_copy_other(job, step, [signal_layer[len(signal_layer)-1]],[sm_layer[len(sm_layer)-1]], False, 0, 0, 0, clearance, 0, 0, 0)
            layer_info.clear_select(job, step, [signal_layer[len(signal_layer)-1]])
            layer_info.reset_select_filter()

        for step in steps:
            epcam_api.add_pad(job, step,signal_layer,signal_layer[0], 'r'+str(npth_size/25400+20), npth_x1, npth_y, -1, 0, 0, [{'.drill':'non_plated'}])
            epcam_api.add_pad(job, step,signal_layer,signal_layer[0], 'r'+str(npth_size/25400+20), npth_x2, npth_y, -1, 0, 0, [{'.drill':'non_plated'}])
            epcam_api.add_pad(job, step,sm_layer,sm_layer[0], 'r'+str(npth_size/25400+10), npth_x1, npth_y, 1, 0, 0, [{'.drill':'non_plated'}])
            epcam_api.add_pad(job, step,sm_layer,sm_layer[0], 'r'+str(npth_size/25400+10), npth_x2, npth_y, 1, 0, 0, [{'.drill':'non_plated'}])
        

        # if len(steps)==1:
        #     epcam_api.get_graphic(job)
        #     data2 = {"cmd":"show_layer", "job":job, "step": 'coupon', "layer": 'l1'}
        #     js = json.dumps(data2)
        #     epcam.view_cmd(js)
        # else:
        #     epcam_api.get_graphic(job)
        #     data2 = {"cmd":"show_layer", "job":job, "step": steps[0], "layer": 'l1'}
        #     js = json.dumps(data2)
        #     epcam.view_cmd(js)
        
        return steps
    except Exception as e:
        return []


