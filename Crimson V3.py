# -*- coding: utf-8 -*-

__author__ = 'KEYONE'


from socket import *


def OneScan(ip, port):


    cmd="0004012b1b00" #获取设备信息的payload

    cmd2="0004012a1a00" # 获取具体型号

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    

    #----first fingerprint gets the manufacturer info
    s.connect((ip,port))

    
    s.send(cmd.decode('hex')) #TCP发包

    #recv0_data=s.recvfrom(1024)

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[6:-1]) #取特定字节范围
    
    #s.close()

    #--second fingerprint gets the model information
    
    s.send(cmd2.decode('hex')) #TCP发包

    res_list_2 = []

    cur_data_2, _ = s.recvfrom(1024)

    for cur_chr_2 in cur_data_2:
        res_list_2.append(cur_chr_2)

    info_2 = ''.join(res_list_2[6:-1]) #取特定字节范围

    s.close()    

    print "IP: " , ip
    print "Port: ", port
    print "Manufacturer: " , info
    print "Model: " , info_2
    print "Protocol: " , 'Crimson v3'


if __name__=="__main__":
    try:
        OneScan('173.166.75.241',789)
    except KeyboardInterrupt:
        pass