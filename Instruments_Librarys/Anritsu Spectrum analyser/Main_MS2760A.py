# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 09:52:51 2021

@author: Martin.Mihaylov
"""

import MS2760A
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import time


# =============================================================================
# Connect to Instrument by TCP/IP
# =============================================================================
SA = MS2760A.MS2760A('127.0.0.1')

SA.ask_DataFormat()
SA.set_DataFormat('ASCii')
SA.set_Counter('OFF')
SA.Init()
complite = 0
while complite == '1':
    complite = SA.OPC()
    time.sleep = 0.1
    
data = SA.ExtractTtraceData(1)
data = SA.write(':TRACe:DATA? 1')
data = SA.read_bytes(3)



SA.ask_ResBwidth()
SA.set_ResBWidth(400,'Hz')
SA.set_freq_Stop(10,'MHz')
data = SA.ask_TraceData(1)
# =============================================================================
# 
# # =============================================================================
# =============================================================================
# # # Small Test 
# =============================================================================
print('Stop Frequency = ',SA.ask_freq_Stop())
print('Start Frequency = ',SA.ask_freq_Start())



import vxi11
rm = vxi11.list_devices()
print(rm)
instr =  vxi11.Instrument('tcpip://127.0.0.1:9001')
print(instr.ask("*IDN?"))


















# =============================================================================
# Anritsu,MS2760A-0110,1722006,V2019.9.1
# =============================================================================



import pyvisa
rm = pyvisa.ResourceManager()
#Connect
inst = rm.open_resource('TCPIP0::127.0.0.1::9001::SOCKET',query_delay  = 0.5)


#set write and read 
inst.write_termination = '\n'
inst.read_termination = '\n'
print('Instrument Connected: ',inst.query("*IDN?"))


#Example from Spectrum_Analyzer_Anristsu.pdf
print(inst.query('DISP:WIND:TRAC:Y:SCAL:RLEV?'))
inst.write('DISP:WIND:TRAC:Y:SCAL:RLEV 0')

inst.write('INIT:CONT OFF')

inst.write(':INITiate:IMMediate')
while inst.query('*OPC?') == '0':
    print('W8')

inst.write(':TRACe:DATA? 1')
data = inst.read_bytes(4014)
plot_data = inst.read()

inst.query('MMEMory:CATalog:MSUSs?')
inst.write(':MMEMory:STORe:TRACe '"ALL"','"C:/Users/SCT-Labor/Desktop/Python Automation skipts/Anritsu Spectrum analyser/TestData"','"Internal"'')


#Binary
tdsData1 = inst.query_binary_values(':TRACE:DATA? 1', datatype='d',is_big_endian=False)
while inst.query('*OPC?') == '0':
    print('W8')
    
    
#Ascii
tdsData2 = inst.query_ascii_values(":TRACe:DATA? 1")
while inst.query('*OPC?') == '0':
    print('W8') 

inst.close()

# =============================================================================
# Anritsu,MS2760A-0110,1722006,V2019.9.1
# =============================================================================






from pyvisa.resources.serial import SerialInstrument
rm = pyvisa.ResourceManager()

inst = rm.open_resource("ASRL10::INSTR", resource_pyclass=SerialInstrument,read_termination = '\n')

inst.query("*IDN?")





import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
dmm = rm.open_resource('TCPIP0::127.0.0.1::9001::SOCKET',query_delay  = 0.5)

dmm.write_termination = '\n'
dmm.read_termination = '\n'
print(dmm.query("*IDN?"))



print('Where the data will be saved: ',dmm.query(':MMEMory:CATalog:MSUSs?'))
print('Select Device to save the data: Internal',dmm.write(':MMEMory:MSIS: Internal'))
print('',dmm.query(':MMEMory:CDIRectory?'))


dmm.write(':SENSe:FREQuency:STOP 25 MHz')
dmm.encoding   

dmm.timeout = 20000 
dmm.chunk_size = 8204800 


dmm.write(':FORMat:TRACe:DATA ASCii')
dmm.write(':SENSe:BANDwidth:RESolution 400 kHz')
dmm.write('INIT:CONT OFF')

print(dmm.query(':TRACe:DISPlay:STATe?'))
print(dmm.query(':FORMat:TRACe:DATA?'))
dmm.

dmm.query_ascii_values(":TRACe:DATA? 1",container=bytearray)

tdsData = dmm.query_binary_values(':TRACE:DATA? 1', datatype='d',is_big_endian=True ,container=bytearray)

data = dmm.query(':TRACe:DATA? 1')

print(dmm.query('BAND:RES?'))
dmm.write('BAND:RES 30 KHz')

print(dmm.query('DISP:WIND:TRAC:Y:SCAL:RLEV?'))
dmm.write('DISP:WIND:TRAC:Y:SCAL:RLEV 0')

dmm.write('INIT:CONT OFF')
dmm.write(':INITiate:IMMediate')
while dmm.query('*OPC?') == '0':
    print('W8')

#dmm.write('*OPC')
tdsData1 = dmm.query_binary_values(':TRACE:DATA? 1', datatype='d',is_big_endian=False)
while dmm.query('*OPC?') == '0':
    print('W8')
    


   
#Ascii
tdsData2 = dmm.query_ascii_values(":TRACe:DATA? 1")
while dmm.query('*OPC?') == '0':
    print('W8')


dmm.query('DISP:POIN?')


dmm.write(':DISPlay:POINtcount 100')
dmm.query(':DISPlay:POINtcount?')






from pymeasure.instruments.anritsu import AnritsuMS9710C


magnet = AnritsuMS9710C("TCPIP::127.0.0.1::9001::SOCKET")
magnet.query('*IDN?')



