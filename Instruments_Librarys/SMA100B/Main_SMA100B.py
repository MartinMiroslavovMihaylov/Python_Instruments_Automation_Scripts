# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 09:52:51 2021

@author: Martin.Mihaylov
"""

import SMA100B
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import time

import pyvisa as visa


# import pyvisa
# rm = pyvisa.ResourceManager()
# rm.list_resources()


import vxi11
rm = vxi11.list_devices()
print(rm)



# Test Maxims Script
SA = SMA100B.SMA100B('169.254.2.20')
SA.set_freq_CW(12,"GHz")
SA.set_rf_power(2)
SA.set_frequency_mode("CW")


# SA.Close()


from SMA100B import SMA100B
import vxi11
rm = vxi11.list_devices()

for _ in rm:
    print(_)
    try:
         SMA = SMA100B(str(_))
         InstrSMA = _
         SMA.Close()
    except (visa.VisaIOError): 
        print('Serial Number dont match!')
# return MS4647B(Str_IP) 

