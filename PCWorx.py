# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):


    cmd1="0101001a0000000078800003000c494245544830314e305f4d00" #第一次发包开始创建会话

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    

    s.connect((ip,port))

    
    s.send(cmd1.decode('hex')) #TCP发包


    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    #sid = ''.join(res_list[17]).encode('hex') #获取会话sid的hex字符
    sid = cur_data[17].encode('hex')
    #print "sid:",sid

    cmd2 = "0105001600010000788000"+sid+"00000006000402950000"

    s.send(cmd2.decode('hex')) #第二次发包建立会话认证

    cur_data2, _ = s.recvfrom(1024)#第二次收包

    cmd3 = "0106000e00020000000000"+sid+"0400"

    s.send(cmd3.decode('hex')) #第三次发包开始获取PLC信息

    res_list3 = []

    cur_data3, _ = s.recvfrom(1024)#第三次收包

    for cur_chr3 in cur_data3:
        res_list3.append(cur_chr3)

    info = ''.join(res_list3[30:41]) #获取PLC信息，可根据需要自行添加其他详情 

    s.close()    

    print "IP: " , ip
    print "Port: ", port
    print "PLC type: " , info
    print "Protocol: " , 'PCWorx'


if __name__=="__main__":
    try:
        OneScan('2.194.129.128',1962)
    except KeyboardInterrupt:
        pass