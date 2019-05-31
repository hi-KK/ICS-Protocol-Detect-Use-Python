# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):

   
    addr=(ip,port) #UDP发包
   
    s = socket(AF_INET,SOCK_DGRAM) #UDP发包
    
    s.connect(addr)

    cmd="63000000000000000000000000000000c1debed100000000" #发送payload
    
    s.sendto(cmd.decode('hex'),addr) #UDP发包

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[-16:-1]) #取特定字节范围 Product Name: 信息

    #print info
    
    s.close()
    
    print "IP: " , ip
    print "Port: ", port
    print "Product Name: " , info
    print "Protocol: " , 'EtherNet-IP'



if __name__=="__main__":
    try:
        OneScan('82.102.158.21',44818)
    except KeyboardInterrupt:
        pass