import import_path
import sys
import os
import json
from PyQt5.Qt import *
import ui_drill_module
import epcam_api as epcam_api
import epcam

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

rules = {
    "config": {
		"isDefault": True,
        "isDeletePrepare": False,
        "is_delete_backuplayer": False,
        "is_okstep_check": False,
        "mergegerber": False,
        "save_ok": False,
        "stepList": [
        ],
        "token": "",
        "unit": "mil",
        "userid": 0,
        "userinfo": {
        }
    },
    "drill": {
        "IsEnDismeter": False,
        "Laser_ring": 0,
        "aspect_ratio": 0,
        "big_drill": 0,
        "big_slot": 0,
        "buried_ring": 0,
        "drillInfoList": {
        },
        "drill_insidehole": {
            "angle_error": 0,
            "aperture": 0,
            "hole_side": 0
        },
        "drill_satellitehole": [
        ],
        "drill_shortgroove": {
            "guide_hole_spacing": 0,
            "middle": False,
            "offset": 0
        },
        "drill_show": False,
        "flag": False,
        "long_slot_resize": 0,
        "min_hole": 0,
        "npthdrill_size": 0,
        "pthdrill_size": 0,
        "short_aspect_ratio": 1.5,
        "short_slot_resize": 0,
        "slotnpthRing_heigth": 0,
        "slotnpthRing_width": 0,
        "slotpthRing_heigth": 0,
        "slotpthRing_width": 0,
        "ultrashort_slot_resize": 0,
        "viadrill_size": 0
    },
    "inner": {
        "New_signal_layer_DFM_show": False,
        "TDResize_inner": 0,
        "add_tear": False,
        "arc_angle": 0,
        "avoid_NPTH": 8,
        "avoid_PTH": 0,
        "avoid_Profile": 0,
        "avoid_VIA": 6,
        "avoid_features_DFM_op_show": False,
        "avoid_v_cut": 0,
        "blind_min": 0,
        "blind_opt": 0,
        "buried_min": 0,
        "buried_opt": 0,
        "coverage_min": 0,
        "drillpad_pth": 0,
        "drillpad_via": 0,
        "fill_seam": 0,
        "flag": False,
        "include_innerlayer": [
        ],
        "isolated_show": False,
        "laser_to_laser": 2.5,
        "line_resize_list": [
        ],
        "line_size": 0.5,
        "line_to_laser": 2.5,
        "line_to_laser_artio": 0.1,
        "line_to_line": 2.5,
        "line_to_pth": 2.5,
        "line_to_pth_artio": 0.01,
        "line_to_surface": 2.5,
        "line_to_surface_artio": 0.01,
        "line_to_via": 2.5,
        "line_to_via_artio": 0.01,
        "manual_sliver_work_inner": False,
        "mending_copper_wire": False,
        "mergenegafteravoid": False,
        "min_add_tear": 0,
        "pth_to_laser": 2.5,
        "pth_to_laser_artio": 0.1,
        "pth_to_pth": 2.5,
        "pth_to_via": 2.5,
        "pth_to_via_artio": 0.1,
        "pthpad_dl_min": 0,
        "pthpad_dl_opt": 0,
        "remove_island_pad": False,
        "signal_layer_DFM_show": False,
        "sliver_DFM_op_show": False,
        "surface_size": 0,
        "surface_to_laser": 3,
        "surface_to_laser_artio": 0.1,
        "surface_to_pth": 3,
        "surface_to_pth_artio": 0.99,
        "surface_to_surface": 4,
        "surface_to_via": 3,
        "surface_to_via_artio": 0.99,
        "teardrop_create_DFM_show": False,
        "teardrop_line_width_radio": 0,
        "via_to_laser": 2.5,
        "via_to_laser_artio": 0.1,
        "via_to_via": 2.5,
        "viapad_dl_min": 0,
        "viapad_dl_opt": 0
    },
    "inner2": {
        "New_signal_layer_DFM_show": False,
        "TDResize_inner": 0,
        "add_tear": False,
        "arc_angle": 0,
        "avoid_NPTH": 8,
        "avoid_PTH": 8,
        "avoid_Profile": 8,
        "avoid_VIA": 6,
        "avoid_features_DFM_op_show": False,
        "avoid_v_cut": 0,
        "blind_min": 0,
        "blind_opt": 0,
        "buried_min": 0,
        "buried_opt": 0,
        "coverage_min": 0,
        "drillpad_pth": 0,
        "drillpad_via": 0,
        "fill_seam": 0,
        "flag": False,
        "include_innerlayer": [
        ],
        "isolated_show": False,
        "laser_to_laser": 2.5,
        "line_size": 0.5,
        "line_to_laser": 2.5,
        "line_to_laser_artio": 0.1,
        "line_to_line": 2.5,
        "line_to_pth": 2.5,
        "line_to_pth_artio": 0.01,
        "line_to_surface": 2.5,
        "line_to_surface_artio": 0.01,
        "line_to_via": 2.5,
        "line_to_via_artio": 0.01,
        "manual_sliver_work_inner": False,
        "mending_copper_wire": False,
        "mergenegafteravoid": False,
        "min_add_tear": 0,
        "pth_to_laser": 2.5,
        "pth_to_laser_artio": 0.1,
        "pth_to_pth": 2.5,
        "pth_to_via": 2.5,
        "pth_to_via_artio": 0.1,
        "pthpad_dl_min": 0,
        "pthpad_dl_opt": 0,
        "remove_island_pad": False,
        "signal_layer_DFM_show": False,
        "sliver_DFM_op_show": False,
        "surface_size": 0,
        "surface_to_laser": 3,
        "surface_to_laser_artio": 0.1,
        "surface_to_pth": 3,
        "surface_to_pth_artio": 0.99,
        "surface_to_surface": 4,
        "surface_to_via": 3,
        "surface_to_via_artio": 0.99,
        "teardrop_create_DFM_show": False,
        "teardrop_line_width_radio": 0,
        "via_to_laser": 2.5,
        "via_to_laser_artio": 0.1,
        "via_to_via": 2.5,
        "viapad_dl_min": 0,
        "viapad_dl_opt": 0
    },
    "input": {
    },
    "layername": {
        "back": "",
        "drl": "",
        "gbl": "",
        "gtl": "",
        "l": "",
        "orig": "",
        "outline": "",
        "pcs": "",
        "smb": "",
        "smt": "",
        "spb": "",
        "spt": "",
        "ssb": "",
        "sst": ""
    },
    "output": {
    },
    "outter": {
        "Dynamic_Compension_show": False,
        "NPTH": 10,
        "New_signal_layer_DFM_show": False,
        "PTH": 0,
        "TDResize_outter": 0,
        "add_outline": False,
        "add_tear": False,
        "arc_angle": 0,
        "avoid_NPTH": 8,
        "avoid_Profile": 0,
        "avoid_features_DFM_op_show": False,
        "avoid_v_cut": 0,
        "bga_pads": True,
        "bga_resize_list": [
        ],
        "bga_size": 2,
        "bga_to_bga": 2.5,
        "bga_to_laser": 2.5,
        "bga_to_laser_artio": 0.01,
        "bga_to_pth": 3.5,
        "bga_to_pth_artio": 0.01,
        "bga_to_via": 2.5,
        "bga_to_via_artio": 0.01,
        "bgapad_sm_min": 0,
        "bgapad_sm_opt": 0,
        "blind_min": 0,
        "blind_opt": 0,
        "blocking_point": True,
        "blocking_point_resize": 8,
        "blocking_point_surface": "正背面",
        "bridge_sm_min": 0,
        "bridge_sm_opt": 0,
        "copper_sufacepad": 0,
        "coverage_min": 0,
        "coverage_sm_min": 0,
        "coverage_sm_opt": 0,
        "cut_surplus_height": 0,
        "cut_surplus_width": 0,
        "drillpad_pth": 0,
        "drillpad_via": 0,
        "fan_shaped": True,
        "fill_seam": 0,
        "flag": False,
        "gas_isdrill": 0,
        "gas_nodrill": 0,
        "include_outterlayer": [
        ],
        "intersect_width": 0,
        "is_round": 0,
        "laser_to_laser": 2.5,
        "line_resize_list": [
        ],
        "line_size": 0.5,
        "line_to_bga": 2.5,
        "line_to_bga_artio": 0.5,
        "line_to_laser": 2.5,
        "line_to_laser_artio": 0.01,
        "line_to_line": 2.5,
        "line_to_pth": 2.5,
        "line_to_pth_artio": 0.01,
        "line_to_smd": 2.5,
        "line_to_smd_artio": 0.01,
        "line_to_surface": 3,
        "line_to_surface_artio": 0.01,
        "line_to_via": 2.5,
        "line_to_via_artio": 0.01,
        "manual_sliver_work_outter": False,
        "mark_size": 2,
        "max_oversize_clearance": 6,
        "mending_copper_wire": False,
        "min_add_tear": 0,
        "outline_width": 0,
        "pad_covered_clearance": 1,
        "prevent_vertical_flow": False,
        "profile_line_width": 0,
        "pth_fan_shave": False,
        "pth_to_laser": 2.5,
        "pth_to_laser_artio": 0.01,
        "pth_to_pth": 2.5,
        "pth_to_via": 2.5,
        "pth_to_via_artio": 0.2,
        "pthpad_dl_min": 0,
        "pthpad_dl_opt": 0,
        "pthpad_sm_min": 0,
        "pthpad_sm_opt": 0,
        "signal_layer_DFM_show": False,
        "sliver_DFM_op_show": False,
        "smd_resize_list": [
        ],
        "smd_size": 2,
        "smd_to_bga": 3.5,
        "smd_to_bga_artio": 0.99,
        "smd_to_laser": 2.5,
        "smd_to_laser_artio": 0.01,
        "smd_to_pth": 2.5,
        "smd_to_pth_artio": 0.3,
        "smd_to_smd": 4.5,
        "smd_to_via": 2.5,
        "smd_to_via_artio": 0.01,
        "smdbga_compensate": 0,
        "smdbga_less": 0,
        "smdpad_sm_min": 0,
        "smdpad_sm_opt": 0,
        "soldermask_dig": 0,
        "soldermask_window": 0,
        "soldermaskflag": False,
        "surface_size": 0,
        "surface_to_bga": 4,
        "surface_to_bga_artio": 0.99,
        "surface_to_laser": 3,
        "surface_to_laser_artio": 0.01,
        "surface_to_pth": 3,
        "surface_to_pth_artio": 0.99,
        "surface_to_smd": 3,
        "surface_to_smd_artio": 0.99,
        "surface_to_surface": 4,
        "surface_to_via": 3,
        "surface_to_via_artio": 0.99,
        "tap_hole": True,
        "tap_hole_resize": 10,
        "tap_hole_surface": "正背面",
        "teardrop_create_DFM_show": False,
        "teardrop_line_width_radio": 0,
        "v_cut": 0,
        "via_to_laser": 2.5,
        "via_to_laser_artio": 0.01,
        "via_to_via": 2.5,
        "viapad_dl_min": 0,
        "viapad_dl_opt": 0
    },
    "panel": {
        "array_step": {
            "array_rect_profile": True,
            "childsteps": [
            ],
            "flag": False,
            "profile_layer": "array_profile",
            "profile_x": 0,
            "profile_y": 0,
            "step": "set"
        },
        "panel_step": {
            "childsteps": [
                {
                    "ANGLE": 0,
                    "DX": 0,
                    "DY": 0,
                    "MIRROR": False,
                    "NAME": "pcs",
                    "NX": 0,
                    "NY": 0,
                    "X": 0,
                    "Y": 0
                }
            ],
            "flag": True,
            "panel_keep_x": 0,
            "panel_keep_y": 0,
            "panel_out_x": 0,
            "panel_out_y": 0,
            "profile_x": 0,
            "profile_y": 0,
            "step": "panel"
        },
        "set_params": {
            "AddCustomerNumber": False,
            "AddFactoryNumber": False,
            "AddFdMark": False,
            "AddFdMarkRing": False,
            "AddToolingHole": False,
            "DummyCuLayer": [
            ],
            "FdMarkCenter": True,
            "FdMarkToHole": 0,
            "FdMarkToPrcessEdge": 0,
            "LeftDownCenter": True,
            "LeftDownX3": 0,
            "LeftDownY3": 0,
            "LeftUpCenter": True,
            "LeftUpX1": 0,
            "LeftUpY1": 0,
            "RightDownCenter": True,
            "RightDownX4": 0,
            "RightDownY4": 0,
            "RightUpCenter": True,
            "RightUpX2": 0,
            "RightUpY2": 0,
            "VCUT": 0,
            "WebCuLayer": [
            ],
            "addTextTest": False,
            "addVtest": False,
            "avoidDrillSize": 40,
            "bigCuLayer": [
            ],
            "chamferRout": False,
            "childProfileExtend": 20,
            "dummyPadDx": 100,
            "dummyPadDy": 100,
            "dummyPadSymbol": "r50",
            "innerSizeFdMarkRing": 118.1,
            "intoBoardVtest": 0,
            "layerFactoryNumber": "",
            "numberX": 1,
            "numberY": 1,
            "outSizeFdMarkRing": 149.606,
            "profileExtend": -20,
            "roundAngleRout": 0,
            "sideDown": 0,
            "sideLeft": 0,
            "sideRight": 0,
            "sideUp": 0,
            "sizeFdMark": 39.37,
            "sizeRout": 0,
            "sizeToolingHole": 118.1,
            "sizeX": 0,
            "sizeY": 0,
            "spacingX": 0,
            "spacingY": 0,
            "typeFdMarkRing": "donut_r",
            "winFdMark": 114.173,
            "winToolingHole": 132.1,
            "withRoundAngle": False
        }
    },
    "silkscreen": {
        "addJobText": {
            "isaddJobText": True,
            "jobText_height": 0,
            "jobText_linewidth": 0,
            "jobText_width": 0
        },
        "flag": False,
        "routaddId": {
            "isroutaddId": True,
            "rout_text_height": 0,
            "rout_text_linewidth": 0,
            "rout_text_width": 0
        },
        "silk_size": 0,
        "sk_height": 0,
        "sk_line_width": 0,
        "sk_spacing": 0,
        "sk_width": 0
    }
}


class Mycal(QThread):
    finished = pyqtSignal()
    def _init_(self):
        super().__init__()
        self.name = ''
        self.path = ''
        self.rules = ''

    def run(self):
        # time.sleep(10)
        epcam.init()
        if os.path.exists(self.path):
            os.remove(self.path)
        #如果当前未设置厂规，则添加默认厂规
        params = epcam_api.getJobParameter(self.name)
        params = json.loads(params)
        ru = params['paras']['parameter']
        if ru == "":
           epcam_api.setJobParameter(self.name, self.rules)
        epcam_api.save_eps(self.name, self.path)
        self.finished.emit() 

def main(jobname):
    try:
        eps_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))),'job')
        if not os.path.exists(eps_path):
            os.makedirs(eps_path)
        eps_job = os.path.join(eps_path, jobname + '.eps')

        rules_str = json.dumps(rules)
              
        b = Mycal()
        b.name = jobname
        b.path = eps_job
        b.rules = rules_str
        a = ui_drill_module.processbar_UI(b)
        a.exec_() 
        return json.dumps(returndata)
    except Exception as e:
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)