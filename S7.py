# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    
    s.connect((ip,port))

    cmd="320700000000000800080001120411440100ff090004001c0001"
    
    s.send(cmd.decode('hex')) #TCP发包

    #recv0_data=s.recvfrom(1024)

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[66:96]) #取特定字节范围 CPUINFO

    s.close()
    
    print "IP: " , ip
    print "Port: ", port
    print "INFO: " , info
    print "Protocol: " , 'S7'

if __name__=="__main__":
    try:
        OneScan('212.199.134.35',102)
    except KeyboardInterrupt:
        pass