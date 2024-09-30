import sys
import os
import json
basepath =  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),'base')
epcampath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),'base/epcam')
if basepath not in sys.path:
    sys.path.append(basepath)
if epcampath not in sys.path:
    sys.path.append(epcampath)