import os,sys
epcam_path=os.path.dirname(__file__)+r"\epcam"
sys.path.append(epcam_path)
import epcam_api as epcam_api

#resize选中的features
#sel_type：0：选中   1：全局
def resize_global(job, step, layers, sel_type, size):
    try:
        epcam_api.resize_global(job, step, layers, sel_type, size)
    except Exception as e:
        print(e)
    return 0

