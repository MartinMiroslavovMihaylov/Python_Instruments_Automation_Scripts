# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:29:34 2021

@author: Martin.Mihaylov
"""


import MG3694C
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 


# =============================================================================
# Connect to Instrument by TCP/IP
# =============================================================================
'''
Ethernet Reset: Cycling power while shorting 
Pin 19 to a grounded pin (Pin 2, 8 or 24 or 

chassis ground) resets the Ethernet Interface 
Card (A13) IP address to the factory default 

STATIC IP address of 192.168.0.254.
'''

G = MG3694C.MG3694C('192.168.0.254')
G.Close()

# =============================================================================
# Small Test 
# =============================================================================
print('Output Impedance = ',G.ask_output_impedance())
print('Frequency Mode: ',G.ask_freq_mode())
print(G.ask_freq_CW())
print('Center Frequency: ',G.ask_freq_centerFreq())
G.set_output(1)
G.set_output_protection('ON')
G.set_output_protection('OFF')
G.set_output('OFF')
G.set_freq_cent(110,'MHz')

G.set_freq_step(0.1,'Hz')



G.set_freq_CW(11,'MHz')

#Freq Span
G.set_freq_span(100,'MHz')

#Start Freq
G.set_freq_start(10,'MHz')

#Stop Freq
G.set_freq_stop(17,'MHz')


#max PowerOutput
print('Max Power Output id = ',G.ask_MaximalPowerLevel())

#Current POutput 
print('Current Putput Power = ',G.ask_OutputPowerLevel())

#set Power Output 
G.set_OutputPowerLevel(-1)

#Current POutput 
print('Current Putput Power = ',G.ask_OutputPowerLevel())



# =============================================================================
# 
# 
# 
# # =============================================================================
# # Test
# # =============================================================================
# import vxi11
# rm = vxi11.list_devices()
# instr =  vxi11.Instrument('192.168.0.254')
# print(instr.ask("*IDN?"))
# 
# 
# 
# 
# 
# 
# # =============================================================================
# # PyVisa Test
# # =============================================================================
# import pyvisa
# rm = pyvisa.ResourceManager()
# print(rm.list_resources())
# print(len((rm.list_resources())))
# 
# 
# 
# 
# 
# =============================================================================


