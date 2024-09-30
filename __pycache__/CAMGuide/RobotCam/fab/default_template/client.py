#!/usr/bin/python3

import sys
import socket
import os
from ftplib import FTP

def sethost():
    try:
        global host
        myhostname = socket.gethostname()
        myhost = socket.gethostbyname(myhostname)
        myhostlist = myhost.split('.')
        if myhostlist[2]=='80':
            host = '10.97.80.136'
        elif myhostlist[2]=='90':
            host = '10.97.90.145'
        # host = '10.97.80.136'     #外部环境
        # host = '10.97.90.145'       #内部环境
    except expression as identifier:
        pass


def Ftp_connect():
    ftp = FTP()
    ftp_port = 21
    ftp.connect(host,ftp_port)
    username = 'zhuwei'
    password = '123456'
    ret = ftp.login(username,password)

def Run(file_path, outpath):
    try:
        sethost()
        filepath = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        #FTP connect
        ftp = FTP()
        ftp_port = 21
        ftp.connect(host,ftp_port)
        username = 'zhuwei'
        password = '123456'
        ret = ftp.login(username,password)

        while True:
            fileinfo = ftp.nlst()
            if len(fileinfo) == 0:
                break
        
        #TCP connect
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_port = 6666
        s.connect((host,tcp_port))

        fp1 = open(file_path,'rb')
        filename_list = filename.split('.')
        ret1 = ftp.storbinary(r'STOR ./aaa.%s'%filename_list[-1],fp1)
        fp1.close()

        run_msg = "Run!!!".format(filename)
        s.send(run_msg.encode('utf-8'))
        #TCP receive message
        msg = s.recv(1024)
        if len(msg) >0:
            if msg.decode('utf_8') == 'False!':
                return False
            print(msg.decode('utf_8'))

        #FTP receive file
        filebasename = filename.split('.')
        outfilename =''
        for i in range(len(filebasename)-1):
            outfilename+=filebasename[i]+'.'
        outfilename+='tgz'
        fp2 = open(os.path.join(outpath, outfilename),'wb')
        ret2 = ftp.retrbinary(r'RETR aaa.tgz',fp2.write)

        success_msg = "success"
        s.send(success_msg.encode('utf-8'))
        s.close()

        ftp.set_debuglevel(0)
        fp2.close()
        ftp.quit()
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':



    file_path = r'C:\Users\wei.zhu\Desktop\WiFi.PcbDoc'
    outpath = r'C:\Users\wei.zhu\Desktop'
    Run(file_path, outpath)
