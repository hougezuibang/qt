import import_path
import os, sys, json
import ui_inner_module
import time
from PyQt5.Qt import *
import epcam
import epcam_api
import layer_info
import job_operation
import epcam_log
import prepare_check

returndata = {'result':True,"status":"","request":""}
showdialog_data = {'request_name':"","step":""}
showlayers_data = {'show_layers':""}

data = {
    "config": {
        "isDeletePrepare": False,
        "is_delete_backuplayer": True,
        "is_okstep_check": False,
        "mergegerber": False,
        "save_ok": False,
        "stepList": [
        ],
        "token": "",
        "userid": 0,
        "userinfo": {
        }
    },
    "drill": {
        "IsEnDismeter": True,
        "Laser_ring": 0,
        "aspect_ratio": 0,
        "big_drill": 0,
        "big_slot": 0,
        "buried_ring": 0,
        "drillInfoList": {
        },
        "drill_insidehole": {
            "angle_error": 5,
            "aperture": 39.37,
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
        "npthdrill_size": 2,
        "pthdrill_size": 4,
        "short_aspect_ratio": 1.5,
        "short_slot_resize": 0,
        "slotnpthRing_heigth": 2,
        "slotnpthRing_width": 2,
        "slotpthRing_heigth": 4,
        "slotpthRing_width": 4,
        "ultrashort_slot_resize": 0,
        "viadrill_size": 2
    },
    "impedance": {
        "avoid_cu_global": 0,
        "clearance": 0,
        "differential_line_info": [
        ],
        "flag": False,
        "min_cu_width": 0,
        "npth_size": 0,
        "profile_box_high": 0,
        "profile_box_wide": 0,
        "pth_ring": 0,
        "pth_size": 0,
        "pth_to_gnd_drill": 0,
        "single_end_line_info": [
        ],
        "spacing": 0
    },
    "inner": {
        "New_signal_layer_DFM_show": False,
        "TDResize_inner": 0,
        "add_tear": False,
        "arc_angle": 0,
        "avoid_NPTH": 10,
        "avoid_PTH": 8,
        "avoid_Profile": 16,
        "avoid_VIA": 7,
        "avoid_features_DFM_op_show": False,
        "avoid_v_cut": 0,
        "blind_min": 0,
        "blind_opt": 0,
        "buried_min": 0,
        "buried_opt": 0,
        "coverage_min": 4,
        "drillpad_pth": 0,
        "drillpad_via": 0,
        "fill_seam": 0,
        "flag": False,
        "include_innerlayer": [
        ],
        "isolated_show": False,
        "laser_to_laser": 3,
        "line_resize_list": [
        ],
        "line_size": 1,
        "line_to_laser": 3,
        "line_to_laser_artio": 1,
        "line_to_line": 3,
        "line_to_pth": 3,
        "line_to_pth_artio": 0,
        "line_to_surface": 5,
        "line_to_surface_artio": 0,
        "line_to_via": 3,
        "line_to_via_artio": 0,
        "manual_sliver_work_inner": False,
        "mending_copper_wire": True,
        "mergenegafteravoid": False,
        "min_add_tear": 4,
        "pth_to_laser": 3,
        "pth_to_laser_artio": 1,
        "pth_to_pth": 3,
        "pth_to_via": 3,
        "pth_to_via_artio": 1,
        "pthpad_dl_min": 5,
        "pthpad_dl_opt": 7,
        "remove_island_pad": True,
        "signal_layer_DFM_show": False,
        "sliver_DFM_op_show": False,
        "surface_size": 0,
        "surface_to_laser": 6,
        "surface_to_laser_artio": 1,
        "surface_to_pth": 5,
        "surface_to_pth_artio": 1,
        "surface_to_surface": 7,
        "surface_to_via": 5,
        "surface_to_via_artio": 1,
        "teardrop_create_DFM_show": False,
        "teardrop_line_width_radio": 0.8,
        "via_to_laser": 3,
        "via_to_laser_artio": 1,
        "via_to_via": 3,
        "viapad_dl_min": 3,
        "viapad_dl_opt": 6
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
        "add_outline": True,
        "add_tear": True,
        "arc_angle": 0,
        "avoid_NPTH": 10,
        "avoid_Profile": 16,
        "avoid_features_DFM_op_show": False,
        "avoid_v_cut": 0,
        "bga_pads": True,
        "bga_resize_list": [
        ],
        "bga_size": 2,
        "bga_to_bga": 3,
        "bga_to_laser": 3,
        "bga_to_laser_artio": 1,
        "bga_to_pth": 3,
        "bga_to_pth_artio": 1,
        "bga_to_via": 3,
        "bga_to_via_artio": 1,
        "bgapad_sm_min": 0.5,
        "bgapad_sm_opt": 2,
        "blind_min": 0,
        "blind_opt": 0,
        "blocking_point": True,
        "blocking_point_resize": 8,
        "blocking_point_surface": "正背面",
        "bridge_sm_min": 3,
        "bridge_sm_opt": 4,
        "copper_sufacepad": 0,
        "coverage_min": 4,
        "coverage_sm_min": 2,
        "coverage_sm_opt": 2,
        "cut_surplus_height": 2,
        "cut_surplus_width": 0.5,
        "drillpad_pth": 0,
        "drillpad_via": 0,
        "fan_shaped": True,
        "fill_seam": 0,
        "flag": True,
        "gas_isdrill": 0,
        "gas_nodrill": 0,
        "include_outterlayer": [
        ],
        "intersect_width": 4,
        "is_round": 0,
        "laser_to_laser": 3,
        "line_resize_list": [
        ],
        "line_size": 1,
        "line_to_bga": 2.8,
        "line_to_bga_artio": 0,
        "line_to_laser": 2.8,
        "line_to_laser_artio": 0,
        "line_to_line": 2.8,
        "line_to_pth": 2.8,
        "line_to_pth_artio": 0,
        "line_to_smd": 2.8,
        "line_to_smd_artio": 0,
        "line_to_surface": 5,
        "line_to_surface_artio": 0,
        "line_to_via": 2.8,
        "line_to_via_artio": 0,
        "manual_sliver_work_outter": False,
        "mark_size": 3,
        "max_oversize_clearance": 6,
        "mending_copper_wire": True,
        "min_add_tear": 4,
        "outline_width": 0,
        "pad_covered_clearance": 1,
        "prevent_vertical_flow": False,
        "profile_line_width": 0,
        "pth_fan_shave": False,
        "pth_to_laser": 3,
        "pth_to_laser_artio": 1,
        "pth_to_pth": 6,
        "pth_to_via": 3,
        "pth_to_via_artio": 1,
        "pthpad_dl_min": 5,
        "pthpad_dl_opt": 7,
        "pthpad_sm_min": 0.5,
        "pthpad_sm_opt": 2,
        "signal_layer_DFM_show": False,
        "sliver_DFM_op_show": False,
        "smd_resize_list": [
        ],
        "smd_size": 2,
        "smd_to_bga": 3,
        "smd_to_bga_artio": 1,
        "smd_to_laser": 3,
        "smd_to_laser_artio": 1,
        "smd_to_pth": 3,
        "smd_to_pth_artio": 1,
        "smd_to_smd": 6,
        "smd_to_via": 3,
        "smd_to_via_artio": 1,
        "smdbga_compensate": 0,
        "smdbga_less": 0,
        "smdpad_sm_min": 0.5,
        "smdpad_sm_opt": 2,
        "soldermask_dig": 0,
        "soldermask_window": 0,
        "soldermaskflag": False,
        "surface_size": 0,
        "surface_to_bga": 6,
        "surface_to_bga_artio": 1,
        "surface_to_laser": 6,
        "surface_to_laser_artio": 1,
        "surface_to_pth": 6,
        "surface_to_pth_artio": 1,
        "surface_to_smd": 6,
        "surface_to_smd_artio": 1,
        "surface_to_surface": 6,
        "surface_to_via": 6,
        "surface_to_via_artio": 1,
        "tap_hole": True,
        "tap_hole_resize": 10,
        "tap_hole_surface": "正背面",
        "teardrop_create_DFM_show": False,
        "teardrop_line_width_radio": 0.8,
        "v_cut": 0,
        "via_to_laser": 3,
        "via_to_laser_artio": 1,
        "via_to_via": 3,
        "viapad_dl_min": 3,
        "viapad_dl_opt": 6
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
            "flag": False,
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
        "silk_size": 6,
        "sk_height": 25,
        "sk_line_width": 5,
        "sk_spacing": 2,
        "sk_width": 20
    }
}

class Mycal(QThread):
    finished = pyqtSignal()
    def _init_(self):
        super().__init__()
        self.jobname = ''
        self.stepname = ''
        self.data = ''
    def run(self):
        '''
        执行内层去尖角
        '''
        inner_param = self.data
        radius = inner_param['inner']['coverage_min'] * 25400
        inner_list = []
        inner_list = layer_info.get_inner_layer_list(self.jobname)
        epcam_api.remove_sharp_angle(self.jobname, self.stepname, inner_list, 1, radius, 2, 1)
        time.sleep(1)
        self.finished.emit() 


def pre_check(jobname):
    job = jobname
    step = 'pcs'
    epcam.init()
    ret = prepare_check.step_is_exist(job, step)
    if not ret['result']:
        return json.dumps(ret)
    return json.dumps(ret)

def main(jobname):
    try:
        job = jobname
        step = 'pcs'
        epcam.init()

        params = epcam_api.getParameter()
        #epcam_log.logger.info(params)

        params = json.loads(params)

        drill_paras = params['paras']['parameter']

        drill_paras = json.loads(drill_paras)

        if 'inner' not in drill_paras:
            return

        b = Mycal()
        b.jobname = job
        b.stepname = step
        b.data = drill_paras
        a = ui_inner_module.processbar_UI(b)
        a.exec_()
    
        showdialog_data['request_name'] = 'Update_job'
        showdialog_data['step'] = 'pcs'
        returndata['request'] = showdialog_data
        return json.dumps(returndata)
    except Exception as e:
        epcam_log.logger.exception(sys.exc_info())
        returndata["result"]=False
        #returndata["status"]=e
        return json.dumps(returndata)


if __name__ == "__main__":
    app=QApplication(sys.argv)
    epcam.init()
    epcam_api.open_job(r'C:\project\EPCAM\trunk\EPCAM\EP-CAM-Engineering\job', '760tbv_pre1')
    xxx = json.dumps(data)
    epcam_api.setParameter(xxx)
    job = '760tbv_pre1'
    main(job)

    step = 'pre'
