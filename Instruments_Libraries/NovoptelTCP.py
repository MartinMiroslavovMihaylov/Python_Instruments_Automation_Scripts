# Downloaded from https://www.novoptel.de/Home/Downloads_de.php on 07.02.2025
# Copyright Novoptel GmbH

import socket
import math
from struct import unpack
import numpy as np
import time

class NovoptelTCP():

    #Parameters
    ip = '127.0.0.1'
    port = 5025
    s = None
    debug = False
    
    def __init__(self, ip='127.0.0.1', port=5025, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        self.connect()
        
    def connect(self):
        if (self.s!=None):
            self.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        try:
            self.s.connect((self.ip, self.port))
            #print("connected: ", self.s)
        except socket.error as e:
            print("Error during socket connect: %s" % e)
        

    def close(self):
        self.s.close()
        self.s = None

    def reconnect(self):
        print("Reconnecting!")
        self.s.close()
        time.sleep(0.5)
        self.connect() 
        
    def socket_write(self, data: bytes):
        rxok = False
        tries = 0
        while (rxok==False) and (tries<10):
            try:
                self.s.send(data)
                time.sleep(0.001) # sleep 1 ms
                rxok = True
            except:
                tries = tries + 1
                if tries>5:
                    self.reconnect()
        return
        
    def socket_read(self, data: bytes):
        rxok = False
        tries = 0
        while (rxok==False) and (tries<10):
            self.socket_write(data)
            try:
                ans = self.s.recv(2)
                res = int.from_bytes(ans, byteorder='big')
                rxok = True
            except:
                res = 0
                tries = tries + 1
                if tries>5:
                    self.reconnect()

        return res    

    def read(self, addr: int):
        cmd=[0x52] # 'R'
        cmd.append((addr>>8)&0xFF)
        cmd.append(addr&0xFF)
        res = self.socket_read(bytes(cmd))
        return res

    def write(self, addr: int, data: int):
        cmd=[0x57] # 'W'
        cmd.append((addr>>8)&0xFF)
        cmd.append(addr&0xFF)
        cmd.append((data>>8)&0xFF)
        cmd.append(data&0xFF)
        self.socket_write(bytes(cmd))

    
    


 
    
    def readsdram_sendrequest(self, startaddrseq: int, packetsinthissequence: int, cycles: int):
        
        # set transfer parameters in one command
        
        cmdlist = [ [512 + 105, startaddrseq & 0xFFFF],
                    [512 + 106, int((startaddrseq >> 16) + math.log2(cycles) * 2**12)],
                    [512 + 107, round(packetsinthissequence/cycles)],
                    [512 + 104, 39294]]
        #print(cmdlist)
        #print("cycles: ", cycles)
        
        cmd = []
        for i in range(len(cmdlist)):
            cmd.append(0x57) # 'W'
            for x in range(2):
                cmd.append((cmdlist[i][x]>>8)&0xFF)
                cmd.append(cmdlist[i][x]&0xFF)
                
         #print(cmd)
        self.socket_write(bytes(cmd))
        

    def readsdram_getpackets_raw(self, startaddrseq: int, packetsinthissequence: int, cycles: int):
        
        try:
            self.readsdram_sendrequest(startaddrseq, packetsinthissequence, cycles)
        except:
            return b''
        
        #print("packetsinthissequence %d" % (packetsinthissequence))
        debug = False
        
        rx_len = 0
        rxbytes = b''
        while (rx_len<packetsinthissequence):
            newbytes = b''
            try:
                newbytes = self.s.recv(2**14)
                rxbytes += newbytes
                if debug:
                    print("newbytes length: %d" % len(newbytes)) 
                if newbytes==0:
                    return b''
            except:
                #print("newbytes length: %d" % len(newbytes))  
                #print("rxbytes length: %d" % len(rxbytes)) 
                #input("Exception in self.s.recv!")
                ## test communication
                #print("ATE: %d" % self.read(512+1))
                #self.readsdram_sendrequest(startaddrseq, packetsinthissequence, cycles)
                #rxbytes = b''
                #debug = True
                return b''
                
            rx_len = len(rxbytes) / 8
            #print("rx_len %d" % (rx_len))
        
        #print("data length: %d" % len(rxbytes))
        
        #print(rxbytes)
        
        return rxbytes
        
    def readsdram_getpackets(self, startaddrseq: int, packetsinthissequence: int, cycles: int):
        
        packetsreceived = 0
        rxbytes = b''
        while packetsreceived<packetsinthissequence:
            try:
                rxbytes = self.readsdram_getpackets_raw(startaddrseq, packetsinthissequence, cycles)
                #print("readsdram_getpackets_raw length: %d" % len(rxbytes))  
                packetsreceived = len(rxbytes) / 8
                if packetsreceived==0:
                    #input("readsdram_getpackets_raw returned 0 bytes!")
                    self.reconnect()  
            except:
                print("Exception in readsdram_getpackets_raw!")
                self.reconnect()  
            
        
        try:
            data = unpack('>'+'H'*(len(rxbytes)//2),rxbytes)  # bytes to uint16
        except:
            print("data length: %d" % len(rxbytes))   
            print("Exception in readsdram_getpackets_raw!")
            
        arr = np.array(list(data))
        rows = arr.shape[0] // 4
        if rows * 4 != arr.shape[0]:
            rows -= 1
            arr = arr[0:rows * 4].reshape(rows, 4)
        arr = arr[0:rows * 4].reshape(rows, 4)
        
        return arr
        
        
        
        
    def readsdram_raw(self, startaddr: int, numaddr: int):
        buffersize_bytes = 2**14;
        cycles = max(1, min(32, math.ceil(numaddr*8/buffersize_bytes)))
        cycles = 2**math.ceil(math.log2(cycles))
        numaddr = math.ceil(numaddr/cycles)*cycles
        buffersize_addr = int(round(buffersize_bytes/8*cycles))
        
        packets_transferred = 0
        
        res = np.empty((0, 4))
        
        while (packets_transferred<numaddr):
            packetsinthissequence = min(buffersize_addr, numaddr-packets_transferred)
            startaddrseq = startaddr + packets_transferred
            rx = self.readsdram_getpackets(startaddrseq, packetsinthissequence, cycles)
            packets_transferred = packets_transferred+packetsinthissequence;
            res = np.concatenate((res, rx), axis=0)
            
        return res
            
