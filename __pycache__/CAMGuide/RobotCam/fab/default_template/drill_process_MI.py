import os, sys, json
PyRecipe_base_epcam_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + r'\base\epcam'
PyRecipe_module_drill_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'\module\drill'
sys.path.append(PyRecipe_base_epcam_path)
sys.path.append(PyRecipe_module_drill_path)
import epcam as epcam
import epcam_api
import drill_classify as drill_classify
import drill_resize as drill_resize
import layer_info as layer_info
import job_operation as job_operation
import analysis_dfm
import feature_resize
from bisect import bisect_left, insort
import math

#drill_tool_manager
"""
:param     count: 孔的数量
:param     slot_len: 槽长
:param     drill_type: 孔属性（Plated, Nplated, Via, Laser）
:param     via_type: via类型（Via None, Close Hole, Same Net Close Hole, BGA Area）
:param     finish_size: 原始孔径
:param     min_tol: 最小公差
:param     max_tol: 最大公差
:param     drill_size: 刀径
"""
# drill_info_list = {
#     "drillInfoList": [
#         {
#             "count": 1320,
#             "drill_size": 302000,
#             "drill_type": "Via",
#             "finish_size": 302000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 1,
#             "via_type": "Via None"
#         },
#         {
#             "count": 38,
#             "drill_size": 303000,
#             "drill_type": "Via",
#             "finish_size": 303000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 2,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 350000,
#             "drill_type": "Plated",
#             "finish_size": 350000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 3,
#             "via_type": "Via None"
#         },
#         {
#             "count": 11,
#             "drill_size": 350000,
#             "drill_type": "NPlated",
#             "finish_size": 350000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 4,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1632,
#             "drill_size": 450000,
#             "drill_type": "Via",
#             "finish_size": 450000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 5,
#             "via_type": "Via None"
#         },
#         {
#             "count": 5,
#             "drill_size": 452000,
#             "drill_type": "Via",
#             "finish_size": 452000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 6,
#             "via_type": "Via None"
#         },
#         {
#             "count": 84,
#             "drill_size": 600000,
#             "drill_type": "NPlated",
#             "finish_size": 600000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 7,
#             "via_type": "Via None"
#         },
#         {
#             "count": 8,
#             "drill_size": 700000,
#             "drill_type": "Plated",
#             "finish_size": 700000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 8,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 910000,
#             "drill_type": "Plated",
#             "finish_size": 910000,
#             "max_tol": 100000,
#             "min_tol": -100000,
#             "slot_len": 1680000,
#             "tool_idx": 9,
#             "via_type": "Via None"
#         },
#         {
#             "count": 3,
#             "drill_size": 951000,
#             "drill_type": "Plated",
#             "finish_size": 951000,
#             "max_tol": 100000,
#             "min_tol": -100000,
#             "slot_len": 410000,
#             "tool_idx": 10,
#             "via_type": "Via None"
#         },
#         {
#             "count": 2,
#             "drill_size": 951000,
#             "drill_type": "Plated",
#             "finish_size": 951000,
#             "max_tol": 100000,
#             "min_tol": -100000,
#             "slot_len": 580000,
#             "tool_idx": 11,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 951000,
#             "drill_type": "Plated",
#             "finish_size": 951000,
#             "max_tol": 100000,
#             "min_tol": -100000,
#             "slot_len": 1630000,
#             "tool_idx": 12,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 1000000,
#             "drill_type": "NPlated",
#             "finish_size": 1000000,
#             "max_tol": 100000,
#             "min_tol": -100000,
#             "slot_len": 0,
#             "tool_idx": 13,
#             "via_type": "Via None"
#         },
#         {
#             "count": 8,
#             "drill_size": 1000000,
#             "drill_type": "Plated",
#             "finish_size": 1000000,
#             "max_tol": 200000,
#             "min_tol": -200000,
#             "slot_len": 0,
#             "tool_idx": 14,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 1010000,
#             "drill_type": "Plated",
#             "finish_size": 1010000,
#             "max_tol": 200000,
#             "min_tol": -200000,
#             "slot_len": 1180000,
#             "tool_idx": 15,
#             "via_type": "Via None"
#         },
#         {
#             "count": 78,
#             "drill_size": 1100000,
#             "drill_type": "Plated",
#             "finish_size": 1100000,
#             "max_tol": 200000,
#             "min_tol": -200000,
#             "slot_len": 0,
#             "tool_idx": 16,
#             "via_type": "Via None"
#         },
#         {
#             "count": 9,
#             "drill_size": 1200000,
#             "drill_type": "Plated",
#             "finish_size": 1200000,
#             "max_tol": 200000,
#             "min_tol": -200000,
#             "slot_len": 0,
#             "tool_idx": 17,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 200000,
#             "min_tol": -200000,
#             "slot_len": 730000,
#             "tool_idx": 18,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 125000,
#             "min_tol": -125000,
#             "slot_len": 730000,
#             "tool_idx": 19,
#             "via_type": "Via None"
#         },
#         {
#             "count": 6,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 125000,
#             "min_tol": -125000,
#             "slot_len": 730000,
#             "tool_idx": 20,
#             "via_type": "Via None"
#         },
#         {
#             "count": 2,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 125000,
#             "min_tol": -125000,
#             "slot_len": 910000,
#             "tool_idx": 21,
#             "via_type": "Via None"
#         },
#         {
#             "count": 8,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 125000,
#             "min_tol": -125000,
#             "slot_len": 1380000,
#             "tool_idx": 22,
#             "via_type": "Via None"
#         },
#         {
#             "count": 2,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 125000,
#             "min_tol": -125000,
#             "slot_len": 1380000,
#             "tool_idx": 23,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 150000,
#             "min_tol": -150000,
#             "slot_len": 1480000,
#             "tool_idx": 24,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 150000,
#             "min_tol": -150000,
#             "slot_len": 1480000,
#             "tool_idx": 25,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 150000,
#             "min_tol": -150000,
#             "slot_len": 1480000,
#             "tool_idx": 26,
#             "via_type": "Via None"
#         },
#         {
#             "count": 1,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 150000,
#             "min_tol": -150000,
#             "slot_len": 2080000,
#             "tool_idx": 27,
#             "via_type": "Via None"
#         },
#         {
#             "count": 2,
#             "drill_size": 1210000,
#             "drill_type": "Plated",
#             "finish_size": 1210000,
#             "max_tol": 150000,
#             "min_tol": -150000,
#             "slot_len": 2380000,
#             "tool_idx": 28,
#             "via_type": "Via None"
#         },
#         {
#             "count": 16,
#             "drill_size": 1400000,
#             "drill_type": "Plated",
#             "finish_size": 1400000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 29,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 1500000,
#             "drill_type": "Plated",
#             "finish_size": 1500000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 30,
#             "via_type": "Via None"
#         },
#         {
#             "count": 5,
#             "drill_size": 1600000,
#             "drill_type": "NPlated",
#             "finish_size": 1600000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 31,
#             "via_type": "Via None"
#         },
#         {
#             "count": 24,
#             "drill_size": 1800000,
#             "drill_type": "Plated",
#             "finish_size": 1800000,
#             "max_tol": 50000,
#             "min_tol": -50000,
#             "slot_len": 0,
#             "tool_idx": 32,
#             "via_type": "Via None"
#         },
#         {
#             "count": 2,
#             "drill_size": 2000000,
#             "drill_type": "NPlated",
#             "finish_size": 2000000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 33,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 2300000,
#             "drill_type": "Plated",
#             "finish_size": 2300000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 34,
#             "via_type": "Via None"
#         },
#         {
#             "count": 4,
#             "drill_size": 3400000,
#             "drill_type": "NPlated",
#             "finish_size": 3400000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 35,
#             "via_type": "Via None"
#         },
#         {
#             "count": 5,
#             "drill_size": 3800000,
#             "drill_type": "NPlated",
#             "finish_size": 3800000,
#             "max_tol": 75000,
#             "min_tol": -75000,
#             "slot_len": 0,
#             "tool_idx": 36,
#             "via_type": "Via None"
#         }
#     ]
# }

drill_info_list = {
    "drillInfoList": [
        {
            "count": 1320,
            "drill_size": 302000,
            "drill_type": "Via",
            "finish_size": 302000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 1,
            "via_type": "Via None"
        },
        {
            "count": 38,
            "drill_size": 303000,
            "drill_type": "Via",
            "finish_size": 303000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 2,
            "via_type": "Via None"
        },
        {
            "count": 11,
            "drill_size": 350000,
            "drill_type": "NPlated",
            "finish_size": 350000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 3,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 350000,
            "drill_type": "Plated",
            "finish_size": 350000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 4,
            "via_type": "Via None"
        },
        {
            "count": 1632,
            "drill_size": 450000,
            "drill_type": "Via",
            "finish_size": 450000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 5,
            "via_type": "Via None"
        },
        {
            "count": 5,
            "drill_size": 452000,
            "drill_type": "Via",
            "finish_size": 452000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 6,
            "via_type": "Via None"
        },
        {
            "count": 84,
            "drill_size": 600000,
            "drill_type": "NPlated",
            "finish_size": 600000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 7,
            "via_type": "Via None"
        },
        {
            "count": 8,
            "drill_size": 700000,
            "drill_type": "Plated",
            "finish_size": 700000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 8,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 910000,
            "drill_type": "Plated",
            "finish_size": 910000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 1679980,
            "tool_idx": 9,
            "via_type": "Via None"
        },
        {
            "count": 3,
            "drill_size": 951000,
            "drill_type": "Plated",
            "finish_size": 951000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 410000,
            "tool_idx": 10,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 951000,
            "drill_type": "Plated",
            "finish_size": 951000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 580000,
            "tool_idx": 11,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 951000,
            "drill_type": "Plated",
            "finish_size": 951000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 1630000,
            "tool_idx": 12,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 951000,
            "drill_type": "Plated",
            "finish_size": 951000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 1630000,
            "tool_idx": 13,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 1000000,
            "drill_type": "NPlated",
            "finish_size": 1000000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 0,
            "tool_idx": 14,
            "via_type": "Via None"
        },
        {
            "count": 8,
            "drill_size": 1000000,
            "drill_type": "Plated",
            "finish_size": 1000000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 0,
            "tool_idx": 15,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 1010000,
            "drill_type": "Plated",
            "finish_size": 1010000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 1180000,
            "tool_idx": 16,
            "via_type": "Via None"
        },
        {
            "count": 78,
            "drill_size": 1100000,
            "drill_type": "Plated",
            "finish_size": 1100000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 0,
            "tool_idx": 17,
            "via_type": "Via None"
        },
        {
            "count": 9,
            "drill_size": 1200000,
            "drill_type": "Plated",
            "finish_size": 1200000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 0,
            "tool_idx": 18,
            "via_type": "Via None"
        },
        {
            "count": 11,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 75000,
            "min_tol": -75000,
            "slot_len": 730000,
            "tool_idx": 19,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 910000,
            "tool_idx": 20,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 1379980,
            "tool_idx": 21,
            "via_type": "Via None"
        },
        {
            "count": 8,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 1380000,
            "tool_idx": 22,
            "via_type": "Via None"
        },
        {
            "count": 1,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 1479980,
            "tool_idx": 23,
            "via_type": "Via None"
        },
        {
            "count": 1,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 1480000,
            "tool_idx": 24,
            "via_type": "Via None"
        },
        {
            "count": 1,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 80000,
            "min_tol": -80000,
            "slot_len": 1480000,
            "tool_idx": 25,
            "via_type": "Via None"
        },
        {
            "count": 1,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 2080000,
            "tool_idx": 26,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 1210000,
            "drill_type": "Plated",
            "finish_size": 1210000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 2380000,
            "tool_idx": 27,
            "via_type": "Via None"
        },
        {
            "count": 16,
            "drill_size": 1400000,
            "drill_type": "Plated",
            "finish_size": 1400000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 0,
            "tool_idx": 28,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 1500000,
            "drill_type": "Plated",
            "finish_size": 1500000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 0,
            "tool_idx": 29,
            "via_type": "Via None"
        },
        {
            "count": 5,
            "drill_size": 1600000,
            "drill_type": "NPlated",
            "finish_size": 1600000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 0,
            "tool_idx": 30,
            "via_type": "Via None"
        },
        {
            "count": 24,
            "drill_size": 1800000,
            "drill_type": "Plated",
            "finish_size": 1800000,
            "max_tol": 100000,
            "min_tol": -100000,
            "slot_len": 0,
            "tool_idx": 31,
            "via_type": "Via None"
        },
        {
            "count": 2,
            "drill_size": 2000000,
            "drill_type": "NPlated",
            "finish_size": 2000000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 32,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 2300000,
            "drill_type": "Plated",
            "finish_size": 2300000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 33,
            "via_type": "Via None"
        },
        {
            "count": 4,
            "drill_size": 3400000,
            "drill_type": "NPlated",
            "finish_size": 3400000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 34,
            "via_type": "Via None"
        },
        {
            "count": 5,
            "drill_size": 3800000,
            "drill_type": "NPlated",
            "finish_size": 3800000,
            "max_tol": 50000,
            "min_tol": -50000,
            "slot_len": 0,
            "tool_idx": 35,
            "via_type": "Via None"
        }
    ]
}



#属性,公差对应的涨缩值
# attribute_tol_size_json = [
#     {'drill_type':'Plated', 'min_tol':-3, 'max_tol':3, 'type':'drill', 'resize_size':3},
#     {'drill_type':'Plated', 'min_tol':-3, 'max_tol':3, 'type':'slot', 'resize_size':[3, 3]]}
# ]

#判断drill能否执行
def drill_process_judge(drill_json):
    if not isinstance(drill_json, list):
        return False
    for _json in drill_json:
        if not 'slot_len' in _json:
            return False
        if not 'drill_type' in _json:
            return False
        if not 'via_type' in _json:
            return False
        if not 'finish_size' in _json:
            return False
        if not 'min_tol' in _json:
            return False
        if not 'max_tol' in _json:
            return False       
        if not 'drill_size' in _json:
            return False
    return True

#获取孔属性
def get_drill_attribute(drill_type, via_type):
    if drill_type == 'Plated' and via_type == 'Via None':
        return [{'.drill':'plated'}]
    elif drill_type == 'Nplated' and via_type == 'Via None':
        return [{'.drill':'non_plated'}]
    elif drill_type == 'Via' and via_type == 'Via None':
        return [{'.drill':'via'}]
    elif drill_type == 'Laser' and via_type == 'Via None':
        return [{'.drill':'via'}, {'.via_type':'laser'}]
    elif drill_type == 'Via' and via_type == 'Close Hole':
        return [{'.drill':'via'}, {'.via_type':'different_close'}]
    elif drill_type == 'Via' and via_type == 'Same Net Close Hole':
        return [{'.drill':'via'}, {'.via_type':'same_close'}]
    elif drill_type == 'Via' and via_type == 'BGA Area':
        return [{'.drill':'via'}, {'.via_type':'bga_area'}]
    else:
        return []

#获取刀径表（公制）
def get_drill_diameter_list(min_size, max_size, tol, special_list):   
    #min_size：刀径最小值 max_size：刀径最大值 tol：刀径公差 special_list：额外新添刀径(数组)
    list_size = (max_size - min_size) / tol + 1
    diameter_list = []
    for i in range(int(list_size)):
        diameter = round(min_size + tol * i, 2)
        diameter_list.append(diameter)
    if len(special_list) > 0:
        for k in range(len(special_list)):
            insort(diameter_list, special_list[k])    
    return diameter_list


#获取贴近刀径表的值
#size_list：刀径表, drill_size:孔径
def get_drill_diameter_size(size_list, drill_size):
    if len(size_list):
        if drill_size <= size_list[0]:
            return size_list[0]
        elif drill_size > size_list[len(size_list) - 1]:
            return drill_size
        else:
            index = bisect_left(size_list, drill_size)
            if index > 0:
                left_delta = drill_size - size_list[index - 1]
                right_delta = size_list[index] - drill_size 
                if left_delta < right_delta:
                    return size_list[index - 1]
                else:
                    return size_list[index]
    return -1

#按属性,孔类型,公差获取当前feature的涨缩值
def get_resize_size(attribute_tol_size_json, drill_info):
    drill_type = drill_info['drill_type']
    slot_len = drill_info['slot_len']
    min_tol = drill_info['min_tol']
    max_tol = drill_info['max_tol']
    if drill_type == 'Via':
        drill_type = 'Plated'
    if slot_len > 0:
        slot_type = 'slot'
    else:
        slot_type = 'drill'
    for info in attribute_tol_size_json:
        if (info['drill_type'] == drill_type) and (info['type'] == slot_type):
            if (info['min_tol'] * 1000000 == min_tol) and (info['max_tol'] * 1000000 == max_tol):      
                if isinstance(info['resize_size'], list):
                    resize_size_list = info['resize_size']
                    return [resize_size_list[0] * 1000000, resize_size_list[1] * 1000000]
                else: 
                    resize_size = info['resize_size']
                    return resize_size * 1000000
    return 0

#通过线宽和线长来选中line,删除原line,返回所有选中line的featureinfo
def select_line_by_length_width(job, step, layer, length, width, tol, include_attributes):
    drill_name = 'r' + get_symbol_name(width)  #line的symbolname, 使用symbolname筛选
    #清除原层所有选中, 并重置当前筛选条件 
    layer_info.clear_select(job, step, layer)        
    layer_info.reset_select_filter()  
    layer_info.set_featuretype_filter(66)      #正片的line
    layer_info.set_attribute_filter(0, include_attributes)
    layer_info.set_include_symbol_filter([drill_name])
    layer_info.select_features_by_filter(job, step, [layer])
    #获取所有筛选到的line
    line_infos = []
    line_infos = layer_info.get_selected_features_infos(job, step, layer)
    #清除原层所有选中, 并重置当前筛选条件 
    layer_info.clear_select(job, step, layer)        
    layer_info.reset_select_filter()  
    #符合条件的line的坐标
    line_locations = []
    #遍历
    for line_info in line_infos:
        start_x = line_info['XS'] * 25400000
        start_y = line_info['YS'] * 25400000
        end_x = line_info['XE'] * 25400000
        end_y = line_info['YE'] * 25400000
        line_len2 = math.pow((end_x - start_x), 2) + math.pow((end_y - start_y), 2)     
        line_len = round(math.sqrt(line_len2), 2)     #线两端圆心间的距离 
        if line_len - length >= (-1 * tol) and  line_len - length <= tol:
            line_locations.append(line_info)
    #遍历坐标进行选中,每次选择时，不清除上一次选中
    for line_location in line_locations:
        center_x = (line_location['XS'] + line_location['XE']) * 25400000 / 2
        center_y = (line_location['YS'] + line_location['YE']) * 25400000 / 2
        select_poligon = [[center_x - 1, center_y - 1], 
        [center_x - 1, center_y + 1], 
        [center_x + 1, center_y + 1], 
        [center_x + 1, center_y - 1], 
        [center_x - 1, center_y - 1]]              #单选的box
        epcam_api.select_feature(job, step, layer, select_poligon, {}, 0, False)
    return line_locations

#对mm进位修正
def carry_correction(size, attribute, slot_type):
    if attribute == [{'.drill':'npth'}]:
        #纳米转毫米, 保留两位小数
        size = round(size / 25400, 2)
        value = float('%.1f'%(size))    #截取到小数点后1位转float
        #取出小数点后第二位
        dif = size - value
        dif = round(dif, 2) * 100
        if dif == 0:
            dif = 0
        elif dif >= 1 and dif <= 2:
            dif = 0
        elif dif >= 3 and dif <= 5:
            dif = 5
        elif dif >= 6 and dif <= 7:
            dif = 5
        elif dif >= 8 and dif <= 9:
            dif = 10
        dif = round(dif / 100, 2)
        value = value + dif
        return round(value * 25400)
    return size


#重新计算line在len进行resize后的起始点坐标
def get_resize_line_start_end(start_x, start_y, end_x, end_y, resize_size, line_wdith):
    line_locations = []
    center_x = (start_x + end_x) / 2
    center_y = (start_y + end_y) / 2
    dis2 = math.pow((end_x - start_x), 2) + math.pow((end_y - start_y), 2)     
    dis = round(math.sqrt(dis2), 2)     #线两端圆心间的距离 
    dis = line_wdith + dis
    final_dis = dis + resize_size            #resize后的线长
    orig_x_offset = abs((end_x - start_x) / 2)
    orig_y_offset = abs((end_y - start_y) / 2)
    x_offset = (final_dis / dis) * orig_x_offset
    y_offset = (final_dis / dis) * orig_y_offset
    final_start_x = center_x + x_offset
    final_end_x = center_x - x_offset
    final_start_y = center_y + y_offset
    final_end_y = center_y - y_offset
    line_locations = [final_start_x, final_start_y, final_end_x, final_end_y]
    return line_locations

#公制尺寸转symbolname(纳米)
def get_symbol_name(size):
    size = size / 25400
    integer = int(size)
    decimal = size - integer
    symbol_str = ''
    if decimal == 0:
        symbol_str = str(integer)
    else:       
        decimal = round(decimal * 1000)
        symbol_str = str(integer) + '.' + str(decimal)
    return symbol_str

#按属性进行圆孔补偿
def resize_drill_by_attribute(job, step, layer, resize_layer, temp_layer, drill_info, attribute_tol_size_json): 
    #获取刀径表（公制）
    diameter_list = get_drill_diameter_list(100000, 6500000, 50000, [3175000])    #单位：纳米 （添加工具孔, 刀径为3.175mm） 
    drill_type = drill_info['drill_type']
    via_type = drill_info['via_type']
    #获取当前孔的属性
    include_attributes = get_drill_attribute(drill_type, via_type)
    #获取当前孔的补偿值(公制)
    resize_size = get_resize_size(attribute_tol_size_json, drill_info)    
    #获取当前孔的大小
    drill_size = drill_info['drill_size']     #公制
    drill_name = 'r' + get_symbol_name(drill_size)    #孔的symbolname, 使用symbolname筛选
    #添加筛选选中所有符合条件的孔
    layer_info.clear_select(job, step, layer)        
    layer_info.reset_select_filter()   
    layer_info.set_featuretype_filter(65)      #正片的pad
    layer_info.set_attribute_filter(0, include_attributes)
    layer_info.set_include_symbol_filter([drill_name])
    layer_info.select_features_by_filter(job, step, [layer])
    pad_list = layer_info.get_selected_pad_point(job, step, layer)
    if len(pad_list) <= 0:
        return
    #将选中的孔移动到中间层进行resize, 防止resize完, 孔变大后干扰后续孔的处理 
    layer_info.sel_move_other(job, step, [layer], job, step, resize_layer, False, 0, 0, 0, 0, 0, 0, 0)
    #清除原层所有选中, 并重置当前筛选条件
    layer_info.clear_select(job, step, layer)        
    layer_info.reset_select_filter()            
    #原孔径加上涨缩值与刀径表进行比较, 并进行进位修正, 重新确定新的涨缩值
    good_size = resize_size + drill_size    #单位：纳米
    real_size = get_drill_diameter_size(diameter_list, good_size)
    if real_size == 450020:
        a = 0
    #进行进位修正
    ######################
    #real_size = carry_correction(real_size, include_attributes, 'drill')
    ######################
    real_delta = real_size - drill_size
    #进行resize, 不选中, 该层整体resize
    feature_resize.resize_global(job, step, [resize_layer], 1, real_delta)
    #resize结束后, 将中间层所有feature移动到临时层
    layer_info.sel_move_other(job, step, [resize_layer], job, step, temp_layer, False, 0, 0, 0, 0, 0, 0, 0)
    #进入下一次循环

 #按属性进行槽孔补偿
def resize_slot_by_attribute(job, step, layer, resize_layer, temp_layer, drill_info, attribute_tol_size_json): 
    #获取刀径表（公制）
    diameter_list = get_drill_diameter_list(100000, 6500000, 50000, [3175000])    #单位：纳米 （添加工具孔, 刀径为3.175mm） 
    drill_type = drill_info['drill_type']
    via_type = drill_info['via_type']
    #获取当前孔的属性
    include_attributes = get_drill_attribute(drill_type, via_type)
    #获取当前孔的补偿值(公制) 数组[槽宽, 槽长]
    resize_size = get_resize_size(attribute_tol_size_json, drill_info)    
    #获取当前槽孔的大小(该层所有oval全部打散成线, drill_size为线宽)
    drill_size = drill_info['drill_size']   #公制
    slot_len = drill_info['slot_len']        #公制
    drill_name = 'r' + get_symbol_name(drill_size)  #槽孔的symbolname, 使用symbolname筛选
    #添加筛选选中所有符合条件的槽孔
    line_locations = []
    line_locations = select_line_by_length_width(job, step, layer, slot_len, drill_size, 1, include_attributes)
    #判断当前是否有选中的feature, 没有则return
    if len(line_locations) == 0:
        return
    infos = layer_info.get_selected_features_infos(job, step, layer)
    if len(infos) == 0:
        return
    #删除选中line
    epcam_api.sel_delete(job, step, [layer])
    # #将选中的孔移动到中间层进行resize, 防止resize完, 孔变大后干扰后续孔的处理 
    # layer_info.sel_move_other(job, step, [layer], job, step, resize_layer, False, 0, 0, 0, 0, 0, 0, 0)
    #清除原层所有选中, 并重置当前筛选条件 
    layer_info.clear_select(job, step, layer)        
    layer_info.reset_select_filter()            
    #原孔径加上涨缩值与刀径表进行比较, 并进行进位修正, 重新确定新的涨缩值
    if resize_size == 0:
        return
    good_size = resize_size[0] + drill_size    #单位：纳米
    real_size = get_drill_diameter_size(diameter_list, good_size)
    #加尾数
    t = real_size / 50000 
    if t % 2 == 0:
        real_size = real_size + 10000
    else:
        real_size = real_size + 1000
    #进行进位修正
    ######################
    #real_size = carry_correction(real_size, include_attributes, 'slot')
    ######################
    #在中间层重新添加line
    new_drill_name = 'r' + get_symbol_name(real_size)
    for line_location in line_locations:
        line_info = get_resize_line_start_end(line_location['XS'] * 25400000, line_location['YS'] * 25400000, 
                    line_location['XE'] * 25400000, line_location['YE'] * 25400000, resize_size[1], drill_size)
        if len(line_info) >= 4:
            epcam_api.add_line(job, step, [], resize_layer, new_drill_name, line_info[0], line_info[1], line_info[2], line_info[3], 1, 0, include_attributes)
    #resize结束后, 将中间层所有feature移动到临时层
    layer_info.sel_move_other(job, step, [resize_layer], job, step, temp_layer, False, 0, 0, 0, 0, 0, 0, 0)
    #进入下一次循环           

def drill_process(job, step, attribute_tol_size_json):
    #获取孔层
    drill_layers = layer_info.get_drill_layer_name(job)
    if len(drill_layers) == 0:
        print('no drill layer')
        return
    for drill_layer in drill_layers:
        #获取tol信息
        # drill_info_list = epcam_api.get_drill_info(job, step, drill_layer)
        # drill_info_list = json.loads(drill_info_list)
        # drill_info_json = drill_info_list['paras']['drillInfoList']
        drill_info_json = drill_info_list['drillInfoList']
        if not drill_process_judge(drill_info_json):
            continue
        #将所有oval打散成线
        layer_info.sel_break(job, step, [drill_layer], 1)
        #新建空层，处理feature时，将feature移动到该层进行处理 
        resize_layer = drill_layer + '_resize'
        job_operation.create_layer(job, resize_layer) 
        #新建空层，用于临时存放所有处理过的feature 
        temp_layer = drill_layer + '_temp'
        job_operation.create_layer(job, temp_layer)  
        for drill_info in drill_info_json:
            drill_type = drill_info['drill_type']
            via_type = drill_info['via_type']
            slot_len = drill_info['slot_len']    
            #分圆孔和槽孔进行补偿, slot_len为0, 则为圆孔
            if slot_len == 0:    
                #圆孔补偿
                resize_drill_by_attribute(job, step, drill_layer, resize_layer, temp_layer, drill_info, attribute_tol_size_json)
            elif slot_len > 0: 
                #槽孔补偿
                resize_slot_by_attribute(job, step, drill_layer, resize_layer, temp_layer, drill_info, attribute_tol_size_json)
            #清除原层所有选中, 并重置当前筛选条件 
            layer_info.clear_select(job, step, drill_layer)        
            layer_info.reset_select_filter()
        #从临时从层拷贝到原层 
        layer_info.sel_move_other(job, step, [temp_layer], job, step, drill_layer, False, 0, 0, 0, 0, 0, 0, 0)
        layer_info.clear_select(job, step, drill_layer)
        #删除所有临时层
        job_operation.delete_layer(job, resize_layer)
        job_operation.delete_layer(job, temp_layer)   