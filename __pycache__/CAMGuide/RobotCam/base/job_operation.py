import os,sys,shutil,time
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import tarfile as tf
#import rarfile as rf
import zipfile as zf

#打开料号
def open_job(path, job):
    try:
       return  epcam_api.open_job(path, job)
        
    except Exception as e:
        print(e)

#保存料号
def save_job(job):
    try:
        epcam_api.save_job(job)
    except Exception as e:
        print(e)

#创建step
def create_step(job, step):
    try:
        index = -1                  #默认创建在末尾
        epcam_api.create_step(job, step, index)
    except Exception as e:
        print(e)

#创建layer
def create_layer(job, layer):
    try:
        index = -1                  #默认创建在末尾
        step = ''                   #在所有层创建
        epcam_api.create_new_layer(job, step, layer, index)
    except Exception as e:
        print(e)

#job重命名
def rename_job(old_jobname, new_jobname):
    try:
        epcam_api.job_rename(old_jobname, new_jobname)
    except Exception as e:
        print(e)

#step重命名
def rename_step(jobname, old_step_name, new_step_name):
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        old_step_index = step_infos.index(old_step_name) + 1
        old_layer_index = -1
        new_layer_info = ''
        epcam_api.change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info)
    except Exception as e:
        print(e)

#layer重命名
def rename_layer(jobname, old_layer_name, new_layer_name, context = ''):
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        new_step_name = ''
        old_step_index = -1
        old_layer_info = {}
        old_layer_index = -1
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == old_layer_name:
                old_layer_info = layer_infos[i]
                old_layer_index = i + 1
            if layer_infos[i]['start_name'] == old_layer_name:
                new_info = layer_infos[i]
                new_info['start_name'] = new_layer_name
                epcam_api.change_matrix(jobname, old_step_index, i+1, new_step_name, new_info)  
            if layer_infos[i]['end_name'] == old_layer_name:
                new_info = layer_infos[i]
                new_info['end_name'] = new_layer_name
                epcam_api.change_matrix(jobname, old_step_index, i+1, new_step_name, new_info)  
        old_layer_info['name']  = new_layer_name
        if context != '':
            old_layer_info['context'] = context
        new_layer_info = old_layer_info
        epcam_api.change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info)   
        
    except Exception as e:
        print(e)

#加载layer
def open_layer(job, step, layer):
    try:
        epcam_api.open_layer(job, step, layer)
    except Exception as e:
        print(e)
        return 0

#拷贝Layer
def copy_layer(jobname, old_layer_name):#jobname, org_layer_index, dst_layer, poi_layer_index
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == old_layer_name:
                old_layer_index = i + 1
        dst_layer = ''
        #新建空layer
        create_layer(jobname, 'jbz')
        ret2 = epcam_api.copy_layer(jobname, old_layer_index, dst_layer, len(layer_infos) + 1)
        data2 = json.loads(ret2)
        new_layer = data2['paras']['newname']
        #删除新层
        delete_layer(jobname, 'jbz')
        return new_layer
    except Exception as e:
        print(e)
        print('123456')
    return ''

#删除料号
def delete_job(jobname):
    try:
        epcam_api.job_delete(jobname)
    except Exception as e:
        print(e)

#读json文件
def load_json(path):
    try:
        with open(path, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            return json_data
    except Exception as e:
        print(e)
    return ""

#读到的range值转为float
def transform_range_data(json_data):
    try:
        data = json_data['rangesList']
        for i in range(len(data)):
            data[i]['RedLv'] = float(data[i]['RedLv'])
            data[i]['YellowLv'] = float(data[i]['YellowLv'])
            data[i]['GreenLv'] = float(data[i]['GreenLv'])
        return json_data
    except Exception as e:
        print(e)
    return ""

#插入layer(matrix)
def insert_layer(job, poi_layer_index):
    try:
        epcam_api.insert_layer(job, poi_layer_index)
    except Exception as e:
        print(e)
    return 0  

#删除copy之后的layer文件夹下的.Z文件
def delete_Z_file(path, job):
    layers_path = path + '\\' + job + r'\steps\pcb\layers'
    filelist = os.listdir(layers_path)
    for file in filelist:
        _path = layers_path + '\\' + file + '\\features.Z'
        if os.path.isfile(_path):
            os.remove(_path)
  
#复制Step
def copy_step(job, old_step_name):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        
        for i in range(0, len(step_infos)):
            if step_infos[i] == old_step_name:
                old_step_index = i + 1
        epcam_api.insert_step(job, old_step_index+1)
        dst_step = ''
        #新建空
        create_step(job, 'jbz')
        ret2 = epcam_api.copy_step(job, old_step_index, dst_step, len(step_infos) + 1)
        data2 = json.loads(ret2)
        new_step = data2['paras']['newname']
        #删除新层
        delete_step(job, 'jbz')
        # ret2 = epcam_api.copy_step(job, old_step_index, dst_step, old_step_index+1)
        # data2 = json.loads(ret2)
        # new_step = data2['paras']['newname']
        return new_step
    except Exception as e:
        print(e)
    return ''

#插入step(matrix)
def insert_step(job, poi_step_index):
    try:
        epcam_api.insert_step(job, poi_step_index)
    except Exception as e:
        print(e)
    return 0 

#压缩文件夹为tgz
def maketgz(ifn, out_path, file_name):
    try:
        ifn = ifn.split(sep = '"')[1]
    except:
        pass
    file_real_name = file_name.split('.')[0]
    ofn = out_path + '\\' + file_name #+ '.tgz'
    #最外层后缀也为tar, 然后再rename为tgz
    out_ofn = out_path + '\\' + file_real_name + '.tar'
    #with tf.open(ofn, 'w:gz') as tar:
    with tf.open(out_ofn, 'w:gz') as tar:
        tar.add(ifn, arcname = os.path.basename(ifn))
    if os.path.exists(ofn):
        os.remove(ofn)
    os.rename(out_ofn, ofn)
    print('compress success!')
        #os.system('pause')

    return 0 

#删除layer
def delete_layer(job, layername):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layername:
                layer_index = i + 1
                epcam_api.delete_layer(job, layer_index)
                break
    except Exception as e:
        print(e)
    return 0 

#解压tgz文件到指定目录
def untgz(ifn, untgz_path):
    try:
        ifn = ifn.split(sep = '"')[1]
    except:
        pass
    ofn = untgz_path
    #with tf.open(ifn, 'r:gz') as tar:
    tar = tf.open(ifn)
    for tarinfo in tar:
        if os.path.exists(os.path.join(ofn, tarinfo.name)):
            for root, dirs, files in os.walk(os.path.join(ofn, tarinfo.name), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        tar.extract(tarinfo.name, ofn)
    print('uncompress success!')
    return os.path.dirname(tarinfo.name)
    #os.system('pause')
    return 

#遍历文件夹下所有子文件夹
def traverse_dirs(ifn):
    try:
        dirs = os.listdir(ifn)
        return dirs
    except Exception as e:
        print(e)
    return 0 


#遍历文件夹下指定文件类型文件名
def traverse_files(ifn, filetype):
    try:
        file_name = []
        for root, dirs, files in os.walk(ifn):
            for name in files:
                if filetype in name:
                    file_name.append(name)
        return file_name
    except Exception as e:
        print(e)
    return 0 

#删除step
def delete_step(job, stepname):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == stepname:
                step_index = i + 1
        epcam_api.delete_step(job, step_index)
    except Exception as e:
        print(e)
    return 0 

#删除指定目录下的指定文件名的料
def job_delete(ofn, jobname):
    try:
        if os.path.exists(os.path.join(ofn, jobname)):
            for root, dirs, files in os.walk(os.path.join(ofn, jobname), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(os.path.join(ofn, jobname))
    except Exception as e:
        print(e)
    return 0 

#load layer
def load_layer(jobname, stepname, layername):
    try:
        epcam_api.load_layer(jobname, stepname, layername)
    except Exception as e:
        print(e)
    return 0 

#获取step列表
def get_all_steps(job):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        steps = data['paras']['steps']
        return steps
    except Exception as e:
        print(e)
    return []

#获取layer列表
def get_all_layers(job):
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
    return []

#identify
def file_identify(path):
    try:
        epcam_api.file_identify(path)
    except Exception as e:
        print(e)

#料号另存为
def file_identify(path):
    try:
        epcam_api.file_identify(path)
    except Exception as e:
        print(e)

#打开eps
def open_eps(job, path):
    try:
        return epcam_api.open_eps(job, path)
    except Exception as e:
        print(e)

# #解压rar文件
# def unrar(file_path, dest_path):
#     try:
#         rar_file = rf.RarFile(file_path)
#         rar_file.extractall(dest_path)
#         #rar_file.close()
#     except Exception as e:
#         print(e)

#解压zip文件
def unzip(file_path, dest_path):
    try:
        zip_file = zf.ZipFile(file_path)
        zip_file.extractall(dest_path)
        zip_file.close()
    except Exception as e:
        print(e)

#创建料号（无路径）
def job_create(job):
    try:
        epcam_api.job_create(job)
    except Exception as e:
        print(e)

#打开eps
def identify_eps(job, path):
    try:
        return epcam_api.identify_eps(job, path)
    except Exception as e:
        print(e)

def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def Traverse_Gerber(job, step, file_path,index):
    for root, dirs, files in os.walk(file_path):
        epcam_api.file_translate_init(job)
        for file in files:
            if is_chinese(file):
                os.rename(file_path+r'/'+file,file_path+r'/''unknow'+str(index))
                file='unknow'+str(index)
                index=index+1
            ret = epcam_api.file_identify(os.path.join(root, file))
            data = json.loads(ret)
            file_format = data['paras']['format']
            file_param = data['paras']['parameters']
            #file_param['text_line_width'] = '{:.2f}'.format(file_param['text_line_width'])
            if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
                print(file)
                re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '', [])    #translate
                
                # job_operation.save_job(job)
        for dir_name in dirs:
            Traverse_Gerber(job, step, os.path.join(root,dir_name),index)

# 按步骤保存job
def job_save_by_num(job,path,num):
    num=str(num)
    filepath=path+'/'+num
    if os.path.exists(filepath):
        shutil.rmtree(filepath)
        os.makedirs(filepath)
        epcam_api.save_job_as(job,filepath)
    else:
        os.makedirs(filepath)
        epcam_api.save_job_as(job,filepath)

#打开回退步骤的job
def open_job_by_num(job,path,currentnum,backnum):
    for i in range(backnum+1,currentnum):
        filepath=path+'/'+str(i)
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
    backnum=str(backnum)
    filepath=path+'/'+backnum
    epcam_api.open_job(filepath,job)

def show_layer(job,step):
    ret = api.get_matrix(job)
    data = json.loads(ret)
    layer_list = []
    layer_info = data['paras']['info']
    if len(layer_info):#遍历获取layer_name
        for i in range(0, len(layer_info)):
            layer_list.append(layer_info[i]['name'])
    layer=layer_list[0]
    datashow = {"cmd":"show_layer", "job":job, "step": step, "layer":layer}
    js = json.dumps(datashow)
    epcam.view_cmd(js)