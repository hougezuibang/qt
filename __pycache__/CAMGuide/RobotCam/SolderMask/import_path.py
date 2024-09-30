import sys
import os
import json
basepath =  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'base')
epcampath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'base/epcam')
if basepath not in sys.path:
    sys.path.append(basepath)
if epcampath not in sys.path:
    sys.path.append(epcampath)
RobotCamPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
New_Default_path = RobotCamPath + r"\fab\new_default_template"
if New_Default_path not in sys.path:
    sys.path.append(New_Default_path)