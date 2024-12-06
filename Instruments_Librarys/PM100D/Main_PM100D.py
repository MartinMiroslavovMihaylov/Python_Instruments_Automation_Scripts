# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 09:46:56 2021

@author: MartinMihaylov
"""


import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import PM100D
import time
import pyvisa as visa

# =============================================================================
# Connect to Instrument by TCP/IP
# =============================================================================


#Serian Number = 'P0024970' From Matlab
#What i have Serial Number = 'P0033858'


Serien_Nummer = ['P0024970','P0033858']
for _ in Serien_Nummer:
    try:
        PD = PM100D.PM100D(_)
        break
    except (visa.VisaIOError): 
       print('Serial Number dont match!')
        

    



# =============================================================================
# Run some simple checks
# =============================================================================

print('Read the Meas.configurations: ',PD.ReadConfig())



#Defoult Measurments whit pre given params
data = PD.DefaultPowerMeas()
print(data)

#Custom Measurments 
CustData = PD.PowerMeas()
print(CustData)

