# -*- coding: utf-8 -*-
# 
__author__='KEYONE'

from socket import *

def OneScan(ip, port):


    cmd="cc01000b4002000047ee" #获取设备信息的payload

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    

    s.connect((ip,port))

    
    s.send(cmd.decode('hex')) #TCP发包


    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[12:44]) #取特定字节范围
 
    s.close()    

    print "IP: " , ip
    print "Port: ", port
    print "Ladder Logic Runtime: " , info
    print "Protocol: " , 'proconos'


if __name__=="__main__":
    try:
        OneScan('104.167.101.164',20547)
    except KeyboardInterrupt:
        pass