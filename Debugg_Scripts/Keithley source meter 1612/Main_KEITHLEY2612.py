# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:12:53 2021

@author: SCT-Labor
"""

import pyvisa as visa
import numpy as np 
import KEITHLEY2612
import time 

rm = visa.ResourceManager()
for i in range(len(list(rm.list_resources()))):
    try: 
        KE = KEITHLEY2612.KEITHLEY2612(rm.list_resources()[i])
        print('Instrument Connected as KA')
        break
    except (visa.VisaIOError): 
               print('Wrong Instrument!')
        

rm = visa.ResourceManager()
rm.list_resources()

# =============================================================================
# 
# 
# # =============================================================================
# # Measure set Voltage 
# # =============================================================================
# #Curent range 
# KE.set_CurrentRange('a',10)
# KE.set_DisplayMeasurementFunction('a','volt')
# 
# 
# 
# #Set Voltage
# KE.set_Voltage('b',10)
# KE.ask_Current('b')
# 
# 
# 
# # =============================================================================
# # Read Current, Voltage, Power, Resistance
# # =============================================================================
# KE.ask_Current('a')
# KE.ask_Voltage('a')
# KE.ask_Power('a')
# KE.ask_Resistance('a')
# 
# 
# 
# # =============================================================================
# # Initialize Channel
# # =============================================================================
# 
# KE.Reset('a')
# KE.set_OutputSourceFunction('a','volt')
# KE.set_VoltageRange('a',3)
# KE.set_SourceOutput('a','ON')
# 
# 
# 
# IRange = float(input('Current Range = '))
# KE.set_CurrentRange('a',IRange)
# KE.set_OutputSourceFunction('a','amp')
# 
# 
# KE.KE.set_VoltageRange('a',5)
# 
# KE.set_SourceOutput('a','OFF')
# 
# 
# 
# 
# # =============================================================================
# # Sweep Voltage
# # =============================================================================
# 
# KE.Reset('a')
# KE.set_OutputSourceFunction('a','volt')
# InitVolt = 1
# KE.set_VoltageRange('b',InitVolt)
# KE.set_SourceOutput('a','ON')
# 
# #make 10 step sweep
# for i in range(0,10):
#     KE.set_SourceOutput('a','OFF')
#     InitVolt += 0.5
#     time.sleep(0.3)
#     print('Voltage will be set to = ',InitVolt)
#     KE.set_VoltageRange('a',InitVolt)
#     KE.set_SourceOutput('a','ON')
#     KE.ask_Voltage('a')
# 
# KE.set_SourceOutput('a','OFF') 
#     
#     
# KE.ask_Voltage('b')
# 
# 
# =============================================================================
