# -*- coding: utf-8 -*-

__author__ = 'KEYONE'

from socket import *


def OneScan(ip, port):


    cmd1="680443000000" # testfr sent

    cmd2="680407000000" # startdt sent

    cmd3="680e0000000064010600ffff00000000" # c_ic_na_1 sent

    s = socket(AF_INET,SOCK_STREAM) #TCP发包
    
    s.connect((ip,port))
    
    s.send(cmd1.decode('hex')) #TCP发包

    cur_data1, _ = s.recvfrom(1024)

    info1 = cur_data1.encode('hex') 


    s.send(cmd2.decode('hex')) #TCP发包

    cur_data2, _ = s.recvfrom(1024)

    info_2 = cur_data2.encode('hex') 


    s.send(cmd3.decode('hex')) #TCP发包

    cur_data3, _ = s.recvfrom(1024)

    info_3 = cur_data3.encode('hex') 

    s.close()    

    info="testfr sent / recv: "+cmd1+"/"+info1+"\n"+"startdt sent / recv: "+cmd2+"/"+info_2+"\n"+"c_ic_na_1 sent / recv: "+cmd3+"/"+info_3
    
    print "IP: " , ip
    print "Port: ", port
    print "Info: ", info
    print "Protocol: " , 'IEC 60870-5-104'


if __name__=="__main__":
    try:
        OneScan('176.118.9.164',2404)
    except KeyboardInterrupt:
        pass