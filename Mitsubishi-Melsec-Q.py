# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    
    s.connect((ip,port))

    cmd="57000000001111070000ffff030000fe03000014001c080a0800000000000000040101010000000001"
    
    s.send(cmd.decode('hex')) #TCP发包

    #recv0_data=s.recvfrom(1024)

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    cpuinfo = ''.join(res_list[41:56]) #取特定字节范围 CPUINFO

    #print cpuinfo
    s.close()
    
    print "IP: " , ip
    print "Port: ", port
    print "CPUINFO: " , cpuinfo
    print "Device: " , 'melsec-q'

if __name__=="__main__":
    try:
        OneScan('211.194.130.54',5007)
    except KeyboardInterrupt:
        pass