# -*- coding: utf-8 -*-

"""
File: modbus.py
Desc: partial implementation of modbus protocol
Version: 0.1

Copyright (c) 2012 Dmitry Efanov (Positive Research)
"""
# 此脚本由开源项目plcscan中的modbus.py修改而来，感谢原作者的开源
# 
__author__ = 'KEYONE'

from struct import pack,unpack
import socket
import string


__FILTER = "".join([' '] + [' ' if chr(x) not in string.printable or chr(x) in string.whitespace else chr(x) for x in range(1,256)])
def StripUnprintable(msg):
    return msg.translate(__FILTER)

class ModbusProtocolError(Exception):
    def __init__(self, message, packet=''):
        self.message = message
        self.packet = packet
    def __str__(self):
        return "[Error][ModbusProtocol] %s" % self.message

class ModbusError(Exception):
    _errors = {
        0:      'No reply',
        # Modbus errors
        1:      'ILLEGAL FUNCTION',
        2:      'ILLEGAL DATA ADDRESS',
        3:      'ILLEGAL DATA VALUE',
        4:      'SLAVE DEVICE FAILURE',
        5:      'ACKNOWLEDGE',
        6:      'SLAVE DEVICE BUSY',
        8:      'MEMORY PARITY ERROR',
        0x0A:   'GATEWAY PATH UNAVAILABLE',
        0x0B:   'GATEWAY TARGET DEVICE FAILED TO RESPOND'
    }
    def __init__(self,  code):
        self.code = code
        self.message = ModbusError._errors[code] if code in ModbusError._errors else 'Unknown Error'
    def __str__(self):
        return "[Error][Modbus][%d] %s" % (self.code, self.message)

class ModbusPacket:
    def __init__(self, transactionId=0, unitId=0, functionId=0, data='',flag=1):
        self.transactionId = transactionId
        self.unitId = unitId
        self.functionId = functionId
        self.data = data
        self.flag = flag
    def pack(self):
        if self.flag == 1:
            return pack('!HHHBB',
                self.transactionId,          # transaction id
                0,                           # protocol identifier (reserved 0)
                len(self.data)+2,            # remaining length
                self.unitId,                 # unit id
                self.functionId              # function id
            )
        elif self.flag == 2:

            return pack('!HHHBBBBB',
                self.transactionId,  # transaction id
                0,  # protocol identifier (reserved 0)
                len(self.data) + 2,  # remaining length
                self.unitId,  # unit id
                self.functionId,  # function id
                0x0e,
                0x01,
                0x00
                )
    def unpack(self,packet):
        if len(packet)<8:
            raise ModbusProtocolError('Response too short', packet)

        self.transactionId, self.protocolId, length, self.unitId, self.functionId = unpack('!HHHBB',packet[:8])
        if len(packet) < 6+length:
            raise ModbusProtocolError('Response too short', packet)

        self.data = unpack("%dB" % (len(packet[8:])), packet[8:])

        return self

class Modbus:
    def __init__(self, ip, port=502, uid=0, timeout=8):
        self.ip = ip
        self.port = port
        self.uid = uid
        self.timeout = timeout

    def Request(self, functionId, data='',flag=1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        sock.connect((self.ip,self.port))

        sock.send(ModbusPacket(0, self.uid, functionId, data,flag).pack())

        reply = sock.recv(1024)
        if not reply:
            raise ModbusError(0)

        response = ModbusPacket().unpack(reply)
#        print(response)
        if response.unitId != self.uid:
            raise ModbusProtocolError('Unexpected unit ID or incorrect packet', reply)

        if response.functionId != functionId:

            raise ModbusError((response.data[0]))

        return response.data

    def DeviceInfo(self):
        res = self.Request(0x2b, '\x0e\x01\00',2)

        if res and len(res)>5:
            objectsCount = res[5]

            data = res[6:]

            info = ''
            for i in range(0, objectsCount):
                for j in data[2:2+(data[1])]:
                    info += chr(j)
                info += ' '
                data = data[2+(data[1]):]
            return info
        else:
            raise ModbusProtocolError('Packet format (reply for device info) wrong', res)

def ScanUnit(ip, port, uid, timeout, function=None, data=''):
    con = Modbus(ip, port, uid, timeout)

    unitInfo = []
    if function:
        try:
            response = con.Request(function, data,1)
            info = ''
            for i in response:
                info += chr(i)
            unitInfo.append("Slave ID Data: %s" % (StripUnprintable(info)))
            #unitData.append("2:%s" % StripUnprintable(info))
        except ModbusError as e:
            if e.code:
                #unitData.append("2:%s" % e.message)
                unitInfo.append("Slave ID Data: %s" % e.message)
            else:
                return unitInfo

    try:
        deviceInfo = con.DeviceInfo()
        unitInfo.append("Device Identification: %s" % deviceInfo)
        #unitData.append("3:%s" % deviceInfo)
    except ModbusError as e:
        if e.code:
            #unitData.append("3:%s" % e.message)
            unitInfo.append("Device Identification: %s" % e.message)
        else:
            return unitInfo

    return unitInfo

def OneScan(ip, port):
    res = False
    unitData = []
    try:
        data = ''

        uids = [0,255] + [x for x in range(1,4)]
        modbus_function = 0x11
        modbus_timeout = 60
        for uid in uids:
            unitData.append("Unit ID: %d," % (uid))
            unitInfo = ScanUnit(ip, port, uid, modbus_timeout, modbus_function, data)

            if unitInfo:
                if not res:
#                    print ("%s:%d Modbus/TCP" % (ip, port))
                    res = True
#                print ("  Unit ID: %d," % uid)
                for line in unitInfo:
#                    print ("    %s" % line)
                    unitData.append(line)

        # product will mostly be ILLEGAL FUNCTION lol
        product = unitData[1][15:]
#        print(product)

        resStr = '\n'.join(unitData)
#       print(resStr)
        
        print "IP: " , ip
        print "Port: ", port
        print "Product: ", product
        print "Info: ", resStr
        print "Protocol: " , 'Modbus'

        #return xmlUtil.getString()

    except ModbusProtocolError as e:
        print ("%s:%d Modbus protocol error: %s (packet: %s)" % (ip, port, e.message, e.packet.encode('hex')))
#        str = writeInfToXml(unitData)
        return 'fail'
    except socket.error as e:
        print ("%s:%d %s" % (ip, port, e))
 #       str = writeInfToXml(unitData)
        return 'fail'
if __name__=="__main__":
    try:

        OneScan('140.112.83.194', 502)
    except KeyboardInterrupt:
        pass
