# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    
    s.connect((ip,port))


    cmd="666f7820612031202d3120666f782068656c6c6f0a7b0a666f782e76657273696f6e3d733a312e300a69643d693a310a7d3b3b0a"
    
    s.send(cmd.decode('hex')) #TCP发包

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[21:-3]) #取特定字节范围 INFO

    #print info
    s.close()

    print "IP: " , ip
    print "Port: ", port
    print "INFO: " , info
    print "Protocol: " , 'niagara-fox'


if __name__=="__main__":
    try:
        OneScan('159.63.135.141',1911)
    except KeyboardInterrupt:
        pass