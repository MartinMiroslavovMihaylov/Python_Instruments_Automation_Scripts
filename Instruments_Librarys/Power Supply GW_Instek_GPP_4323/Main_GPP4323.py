# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:59:45 2023

@author: Martin.Mihaylov
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import vxi11
import time 
from GPP4323 import GPP4323


PS = GPP4323('COM40')
# PS.getIdn()
# PS.set_Volt(1,4.3)
# PS.ask_Volt(1)
# PS.set_Amp(1, 0.01)
# PS.ask_Amp(1)
PS.set_Out(1, 'ON')
PS.set_Out(2, 'OFF')
# PS.set_ChannelLoadMode(1, 'CV', 'OFF')
# PS.read_Measurment(1, 'Power')
# PS.ask_Status()
# PS.Close()
# stat = PS.ask_Status().split('\n')[0]
data = PS.get_data(1)


spannung = 2
current = np.arange(0,0.1,0.01)
PS.set_Out(1, 'ON')
PS.set_Volt(3, spannung)
for i in range(len(current)):
    PS.set_Amp(3,current[i])
    print('Current = ', current[i])
    time.sleep(1)
    
PS.set_Volt(3,0)
PS.set_Amp(3,0)
PS.set_Out(1, 'OFF')



PS.set_ChannelToSerial(4,'ON')
PS.set_ChannelToParallel(4,'OFF')
PS.set_ChannelTracking(7)
PS.set_ChannelLoadMode(1,'CR','OFF')
PS.set_LoadResistor(2,100)
PS.ask_LoadResistor(2)
PS.ask_ChannelLoadMode(1)
PS.Close()



# import io
# import serial
# import time
# import sys

# ser = serial.Serial('COM40',
#                 baudrate = 115200,
#                 bytesize=8,
#                 timeout=1,
#                 stopbits = serial.STOPBITS_ONE,
#                 parity = serial.PARITY_NONE,
#                 xonxoff = False)

# eol_char = '\r\n'
# sio = io.TextIOWrapper(io.BufferedReader(ser),newline=eol_char)

# while True:
#     sending = input("type:\n")
#     ser.write((sending + eol_char).encode('utf-8'))
#     time.sleep(0.2)
#     ans = sio.read()
#     sys.stdout.write('received: ' + str(ans))
#     print('\ntry again\n')