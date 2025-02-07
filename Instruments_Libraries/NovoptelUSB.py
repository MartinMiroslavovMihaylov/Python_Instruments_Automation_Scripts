# Downloaded from https://www.novoptel.de/Home/Downloads_de.php on 07.02.2025
# Copyright Novoptel GmbH

from time import sleep
import sys, ftd2xx as ftd
from ctypes import *


class NovoptelUSB():

   
    # Parameters
    baudrate = 230400
    DEVNO = -1
    
    def __init__(self):
        
        self.isConnected = False
        self.d=0
    
        # list all connected ftdi devices
        dlist=ftd.listDevices(2)
        if len(dlist) > 0:
            counter=0
            for dev in dlist[:]:
                print("    " + str(counter) + ": " + dev.decode('UTF-8'))
                counter = counter + 1
            print("    Select Instrument (-1 to Quit):")
            self.DEVNO = int(input())
            if self.DEVNO>=0:
                self.connect()
        else:
             print("    No Instrument found")
        return
        
        
        
    def connect( self):
    
        self.d = ftd.open(self.DEVNO)    # Open selected FTDI device
        self.d.setBaudRate(self.baudrate)
        self.d.setDataCharacteristics(8, 0, 0)
        self.isConnected = True
        print( "Connected." )
        return
        
    def close( self ):
        self.d.close()
        self.isConnected = False
        print( "Closed." )
        return
        
        
    def write(self, addr, data):
        sleep(0.01)
        txstring = 'W' + '{:03X}'.format(addr) + '{:04X}'.format(data) + chr(13)
        tx = create_string_buffer(txstring.encode('utf-8'), 9)
        self.d.write(tx)
        return
        
    def read(self, addr):
    
        self.d.purge() # clear buffers
        #sleep(0.01)

        # send request command
        txstring = 'R' + '{:03X}'.format(addr) + '0000' + chr(13)
        #print(txstring)
        tx = create_string_buffer(txstring.encode('utf-8'), 9)
        self.d.write(tx)
        
        # wait for RX
        bytesavailable=0
        tries=0
        while bytesavailable<5 and tries<1000:
            bytesavailable=self.d.getQueueStatus()
            tries += 1
            #sleep(0.001)
        
        # get RX
        res=self.d.read(bytesavailable)
        
        #print(len(res))
        #print(type(res))
        #for ires in res[:]:
        #        print(ires)
        #print(tries)
        #print(res.decode("utf-8"))
        #print(int(res.decode("utf-8"),16))
        
        
        # return RX as integer
        if bytesavailable>4:
            val = int(res.decode("utf-8"),16)
        else:
            val = -1     
        return val
        
        
        
        
