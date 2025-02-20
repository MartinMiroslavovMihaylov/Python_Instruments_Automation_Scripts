# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:22:51 2022

@author: Martin.Mihaylov
"""


import vxi11
rm = vxi11.list_devices()
print(rm)



import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()

instr =  vxi11.Instrument('ASRL10::INSTR')
print(instr.ask("*IDN?"))
