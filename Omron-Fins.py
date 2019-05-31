# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *

def OneScan(ip, port):
   
    addr=(ip,port) #UDP发包
   
    s = socket(AF_INET,SOCK_DGRAM) #UDP发包
    
    s.connect(addr)

    cmd="800002000000006300ef050100" #发送payload
    
    s.sendto(cmd.decode('hex'),addr) #UDP发包

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[14:34]) #取特定字节范围 Controller model信息

    #print info
    
    s.close()
    
    print "IP: " , ip
    print "Port: ", port
    print "Controller model: " , info
    print "Protocol: " , 'omron-fins'


if __name__=="__main__":
    try:
        OneScan('83.48.14.162',9600)
    except KeyboardInterrupt:
        pass