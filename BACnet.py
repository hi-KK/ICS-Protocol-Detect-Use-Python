# -*- coding: utf-8 -*-

__author__ = 'KEYONE'


from socket import * 

def OneScan(ip, port):
   
    addr=(ip,port) #UDP发包
   
    s = socket(AF_INET,SOCK_DGRAM) #UDP发包
    
    s.connect(addr)

    id=['79',#vendor
    '78',#vendor_id
    '2c',#firmware
    '0c',#application
    '46',#model
    '4d',#object
    '4b',#object_id
    '1c',#description
    '3a',#location
    ]

    cmd="810a001101040005010c0c023fffff19"+id[0] #发送payload,根据需要自行取id
    
    s.sendto(cmd.decode('hex'),addr) #UDP发包

    res_list = []

    cur_data, _ = s.recvfrom(1024)

    for cur_chr in cur_data:
        res_list.append(cur_chr)

    info = ''.join(res_list[-19:-1]) #取特定字节范围 此处举例 vendor_name 信息 根据取id值改变范围

    #print info
    
    s.close()

    print "IP: " , ip
    print "Port: ", port
    print "Vendor Name: " , info
    print "Protocol: " , 'bacnet'
    


if __name__=="__main__":
    try:
        OneScan('69.70.31.138',47808)
    except KeyboardInterrupt:
        pass