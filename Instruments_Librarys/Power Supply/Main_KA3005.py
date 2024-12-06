# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 09:47:59 2021

@author: Martin.Mihaylov
"""


from KA3005 import kd3005pInstrument
from KA3005p import KA3005p




#Print all instruments connected to the COM-Ports.
#Needed to set later
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
list_Ports = []
for port, desc, hwid in sorted(ports):
        list_Ports.append(port)
        print("{}: {} [{}]".format(port, desc, hwid))
    

# Instrument = []  
# Ports = [list_Ports[1],list_Ports[3]]
# SerialNum = ['KORAD KA3005P V5.8 SN:03379314' , 'KORAD V5.8 SN:03379314' , 'RND 320-KA3005P V2.0']      
# for data1 in Ports:
#     PS = kd3005pInstrument(data1)
#     data = PS.getIdn()
#     if data in SerialNum:
#         if data == SerialNum[0]:
#             PS.Close()
#             PS1 = kd3005pInstrument(data1)
#             print('Power Supply KA3005P is connected as PS1')
#             Instrument.append(PS1)
#         elif data == SerialNum[1]:
#             PS.Close()
#             PS2 = kd3005pInstrument(data1)
#             print('Power Supply KA3005P is connected as PS2')
#             Instrument.append(PS2)
#         elif data == SerialNum[2]:
#             PS.Close()
#             PS3 = kd3005pInstrument(data1)
#             print('Power Supply KA3005 is connected as PS3')
#             Instrument.append(PS3)
   


# PA = kd3005pInst
# rument('COM38')      
# List_Names = ['KORAD KA3005P V5.8 SN:03379314' , 'RND 320-KA3005P V2.0']
 
# #Choose a correct COM port and change the string in the function
# PA = kd3005pInstrument('COM38')
# PS = kd3005pInstrument('COM3')
# PA.getIdn()
# PS.getIdn()


# # # =============================================================================
# # # Test
# # # =============================================================================
# PA.getIdn()
# PA.ask_Volt()
# PA.set_Volt(10)
# PA.set_Amp(2)
# PA.ask_Amp()
# PS.ask_Amp()
# PA.set_Out('ON')
# PA.set_Out('OFF')


# # =============================================================================
# # Important ! Dont forgedt to close the COM
# # =============================================================================
# PA.Close()
# PS.Close()




# =============================================================================
# Test 2 with pyVisa
# =============================================================================


# import time 
# import numpy as np


# PS = KA3005p('ASRL3::INSTR')
# PS.getIdn()
# PS.set_Out('ON')
# vec = np.arange(0,0.005,0.001)
# for i in range(len(vec)):       
#     PS.set_Amp(vec[i])
#     time.sleep(1)
# PS.set_Out('OFF')
    
# PS.set_Volt(0.5)
# time.sleep(1)
# PS.ask_Volt()
# PS.read_Volt()

# PS.set_Amp(0.005)
# PS.ask_Amp()
# PS.read_Amp()
# PS.set_Out('ON')
# PS.set_Out('OFF')
# PS.ask_Status()
# PS.Close()





