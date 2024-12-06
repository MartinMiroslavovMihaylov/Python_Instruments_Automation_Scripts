# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:57:49 2022

@author: Martin.Mihaylov
"""

import APPH
# =============================================================================
# import pyvisa
# rm = pyvisa.ResourceManager()
# rm.list_resources()
# 
# =============================================================================


API = APPH.APPH('TCPIP0::131.234.87.204::inst0::INSTR')
API.ask_Freq()
API.ask_Power()
API.ask_TransNoise()
API.ask_PMTransJitter()
API.ask_DUTPortVoltage()
API.ask_DUTPortStatus()
API.ask_PN_StartFreq()
API.ask_PN_IFGain()
API.ask_PN_StopFreq()
API.set_Output('OFF')
API.set_Output('ON')
API.Close()
