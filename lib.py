#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import os
import psutil
import sys
import requests
import schedule
dirp=os.getcwd()
def timc():
    while True:
        schedule.run_pending()
def ggt(idu,ip,port):
    data={'message': idu}
    s=requests.post('https://'+ip+':'+str(port)+'/internet',json=data)
def processW():
    with open(os.path.join(dirp, 'PIDLiSt.txt'),'w+') as f:
        f.writelines(str(os.getpid())+' '+os.path.basename(sys.argv[0]))
        f.close()
def sck(idu,name,ip,port):
    url = 'https://'+ip+':'+str(port)+'/sendMessage'
    data = {'message': idu+';'+'Скрипт '+name+' был завершен.'}
    response = requests.post(url, json=data)
    #print(response.text)
def ProcessCheck(idu,ip,port):
    timcc=threading.Thread(target=timc)
    timcc.start()
    schedule.every().hour.at("14:00").do(ggt(idu,ip,port))
    schedule.every().hour.at("29:00").do(ggt(idu,ip,port))
    schedule.every().hour.at("44:00").do(ggt(idu,ip,port))
    schedule.every().hour.at("59:00").do(ggt(idu,ip,port))
    while True:
        f = open(os.path.join(dirp, 'PIDLiSt.txt'),'r')
        lines=f.readlines()
        for i in range(len(lines)):
            q=lines[i].split()
            if not(psutil.pid_exists(int(q[0]))):
                f.close()
                try:
                    sck(idu,q[1],ip,port)
                except:
                    pass
                lines.pop(i)
                f = open('PIDLiSt.txt','w')
                for w in range(len(lines)):
                    f.writelines(lines[w])
                f.close()

            


