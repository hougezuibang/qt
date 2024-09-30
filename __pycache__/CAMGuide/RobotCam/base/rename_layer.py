import os,sys
epcam_path=os.path.dirname(__file__)+r"\base\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import job_operation
import epcam_api
import epcam as epcam
import layer_info
import feature_resize
import configparser


# def read_file(path):
#     with open(path) as fp:
#         content = fp.read()
#     return content

# ret = read_file()

# def alter(file, old_str):
#     try:
#         file_data = ""
#         new_str = ""
#         conf = configparser.ConfigParser()
#         # with open(file, "r", encoding = "utf-8-sig") as f:
#         #     for line in f:
#         #         if old_str in line:
#         #             key, new_str = line.strip().split(':', 1)
#         #             line = line.replace(old_str, old_str)
#         #             # line = old_str
#         #         file_data += line
#         # with open(file, "w", encoding = "utf-8-sig") as f:
#         #     f.write(file_data)
#         # return new_str
#         conf.read(file)
#         new_str = conf.get("layer", old_str)
#         return new_str
#     except Exception as e:
#         print(e)
#     return ''


# def rename(job):
#     try:
#         layer_list = layer_info.get_all_layer_name(job)
#         for i in range(len(layer_list)):
#             old_layer = layer_list[i]
#             new_layer = alter(file, layer_list[i])
#             job_operation.rename_layer(job, old_layer, new_layer)
#             # alter(file, old_layer)
#     except Exception as e:
#         print(e)
#     return ''
    # alter(file, 'sst')
    # inner_layer_list = layer_info.get_inner_layer_list(job)
    # for i in range(len(inner_layer_list)):
    #     job_operation.rename_layer(job, layer_list[i], alter(file, layer_list[i]))
    #     # alter(file, 'l'+str(i+2))
    # # outter_layer_list = layer_info.get_outter_list(job)
    # alter(file, 'l1')
    # alter(file, 'l'+str(len(inner_layer_list)+2))

def layerlist_rename(job, layer_json):
    try:
        #修改step名
        step_list = job_operation.get_all_steps(job)
        if layer_json['pcs'] != '':
            job_operation.rename_step(job, 'pcs', layer_json['pcs'])
        # if layer_json['orig'] != '':
        #     if 'orig' in step_list:
        #         job_operation.rename_step(job, 'orig', layer_json['orig'])
        #     else:
        #         if 'org' in step_list:
        #             job_operation.rename_step(job, 'org', layer_json['orig'])
        #修改layer名
        layer_list = layer_info.get_all_layer_name(job)
        if layer_json['sst'] != '':
            job_operation.rename_layer(job, "sst", layer_json['sst'])
            job_operation.rename_layer(job, "sst-pre", layer_json['sst'] + '+1')
        if layer_json['ssb'] != '':
            job_operation.rename_layer(job, "ssb", layer_json['ssb'])
            job_operation.rename_layer(job, "ssb-pre", layer_json['ssb'] + '+1')
        if layer_json['smt'] != '':
            job_operation.rename_layer(job, "smt", layer_json['smt'])
            job_operation.rename_layer(job, "smt-pre", layer_json['smt'] + '+1')
        if layer_json['smb'] != '':
            job_operation.rename_layer(job, "smb", layer_json['smb'])
            job_operation.rename_layer(job, "smb-pre", layer_json['smb'] + '+1')
        if layer_json['spt'] != '':   
            job_operation.rename_layer(job, "spt", layer_json['spt'])
            job_operation.rename_layer(job, "spt-pre", layer_json['spt'] + '+1')
        if layer_json['spb'] != '':   
            job_operation.rename_layer(job, "spb", layer_json['spb'])
            job_operation.rename_layer(job, "spb-pre", layer_json['spb'] + '+1')
        if layer_json['outline'] != '':   
            job_operation.rename_layer(job, "outline", layer_json['outline']) 
            job_operation.rename_layer(job, "outline-pre", layer_json['outline'] + '+1')                     
        #内层
        inner_layer_list = layer_info.get_inner_layer_list(job)
        if layer_json['l'] != '' or layer_json['back'] != '':  
            if len(inner_layer_list) > 0:
                for i in range(len(inner_layer_list)):
                    job_operation.rename_layer(job, "l"+str(i+2), layer_json['l']+str(i+2)+layer_json['back'])
                    job_operation.rename_layer(job, "l"+str(i+2) + '-pre', layer_json['l']+str(i+2)+layer_json['back'] + '+1')
        #外层
        outter_layer_list = layer_info.get_outter_list(job)
        if layer_json['gtl'] != '':  
            job_operation.rename_layer(job, "l1", layer_json['gtl'])
            job_operation.rename_layer(job, "l1-pre", layer_json['gtl'] + '+1')
        if layer_json['gbl'] != '':  
            job_operation.rename_layer(job, 'l'+str(len(inner_layer_list)+2), layer_json['gbl'])
            job_operation.rename_layer(job, 'l'+str(len(inner_layer_list)+2) + '-pre', layer_json['gbl'] + '+1')
        #孔层
        drill_list = layer_info.get_drill_layer_name(job)
        if layer_json['drl'] != '':  
            job_operation.rename_layer(job, 'drl1-'+str(len(inner_layer_list)+2), layer_json['drl'])
            job_operation.rename_layer(job, 'drl1-'+str(len(inner_layer_list)+2) + '-pre', layer_json['drl'] + '+1')
    except Exception as e:
        print(e)
    return ''


def delete_prepare_step(job):
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        steps = []
        steps = data['paras']['steps']
        # if 'net' in steps:
        #     job_operation.delete_step(job, 'net')
        if 'prepare' in steps:
            job_operation.delete_step(job, 'prepare')
        if 'pre' in steps:
            job_operation.delete_step(job, 'pre')
    except Exception as e:
        print(e)
    return ''