# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 13:52:13 2022

@author: Martin.Mihaylov
"""


import CoBrite 


CO = CoBrite.CoBrite('ASRL34::INSTR')

#Turn ON/OFF query status
CO.set_LaserOutout(1,1)
CO.ask_LaserOutout(1)
CO.set_LaserOutout(1,'0')
CO.ask_LaserOutout(1)

CO.set_LaserOutout(2,1)
CO.ask_LaserOutout(2)
CO.set_LaserOutout(2,'OFF')
CO.ask_LaserOutout(2)


#Set Power Ask Power
CO.set_Power(1,10)
CO.ask_Power(1)
CO.set_Power(2,11)
CO.ask_Power(2)

#Set Frequency in THz Ask Freq
CO.set_FreqTHz(1,0.111)
CO.ask_FreqTHz(1)
CO.set_FreqTHz(2,193.46)
CO.ask_FreqTHz(2)


#Set Wavelenght ask wav
CO.set_Wavelength(1,1554.0)
CO.ask_Wavelength(1)
CO.set_Wavelength(2,1553.56)
CO.ask_Wavelength(2)




#Dither OPLL
CO.ask_DitherLoop(2)

#Configurations+
data = CO.ask_Configuration(1)

CO.set_Configuration(1,191.5432,9.8,1,0)
CO.Close()



import pyvisa 
rm = pyvisa.ResourceManager()
rm.list_resources()
dmm = rm.open_resource('ASRL34::INSTR',query_delay  = 0.5)


print(dmm.query("*IDN?"))

dmm.write('OFF 1,1,1,4')
dmm.write('FREQ 1,1,1,193.10')
