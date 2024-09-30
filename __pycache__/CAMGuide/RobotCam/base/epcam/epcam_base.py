# #!/usr/bin/python3
import epcam as epcam
import json
import sqlite3
import sys


# get data from sqlite3
def get_paras(session_id, func):
    conn = sqlite3.connect(r'C:\epcam_db\testcam.db')
    cursor = conn.cursor()
    cursor.execute('select * from funlog')
    data = cursor.fetchall()
    print(data)
    select = 'select * from funlog where sessionid={} and funname=\'{}\''.format(session_id, func)
    cursor.execute(select)
    values = cursor.fetchall()
    print(values)
    print(values[0][4])
    return values[0][4]

# Func:process
def process(data, session_id, rebuild):
    func = data['func']
    if rebuild == 1:
        json_str = get_paras(session_id, func)
    else:
        json_str = json.dumps(data)  # json 编码
    print(type(json_str), json_str)
    epcam.init_func_map()
    ret = epcam.process(json_str)
    print(type(ret))
    print(ret)

def auto_rebuild(session_id):
    conn = sqlite3.connect(r'C:\epcam_db\testcam.db')
    cursor = conn.cursor()
    cursor.execute('select * from funlog where sessionid={}'.format(session_id))
    data = cursor.fetchall()
    count = len(data)
    print(count)
    epcam.init_func_map()
    i = 0
    while i < count:
        print(data[i][4])
        ret = epcam.process(data[i][4])
        print("process", data[i][3], ret)
        i+=1
    print("auto rebuild finished")
