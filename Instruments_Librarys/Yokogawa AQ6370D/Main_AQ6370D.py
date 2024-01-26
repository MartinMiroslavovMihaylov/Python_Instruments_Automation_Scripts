# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:58:26 2021

@author: Martin.Mihaylov
"""

import AQ6370D
import pandas as pd
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size':22})

OSA = AQ6370D.AQ6370D('131.234.87.198')

# =============================================================================
# 
# 
# OSA.ask_SweepMode()
# OSA.set_SweepMode('AUTO')
# OSA.StartSweep()
# OSA.Stop()
# 
# 
# 
# OSA.get_ParamsOSA()
# 
# 
# OSA.set_TraceActive('TRC')
# OSA.ask_TraceAttribute('TRBgfh')
# OSA.set_TraceAttribute('TRB','MAX')
# 
# 
# 
# 
# OSA.ask_DisplayAutoY()
# OSA.ask_WavelenghtStart()
# OSA.ask_WavelenghtStop()
# OSA.set_WavelenghtStop(155,'NM')
# 
# 
# OSA.set_BWResolution(50,'PM')
# OSA.ask_BWResolution()
# 
# 
# OSA.ask_CentralWavelength()
# OSA.set_CentralWavelength(1550.000,'NM')
# 
# 
# OSA.ask_Sensitivity()
# OSA.set_Sensitivity('NAUT')
# 
# 
# test2 = OSA.ask_TraceResolution('TRA')
# OSA.Stop()
# 
# 
# OSA.ask_WavelenghtStart()
# OSA.ask_WavelenghtStop()
# OSA.set_WavelenghtStop(1.57e-6,'M')
# 
# OSA.ask_AverageCount()
# OSA.set_AverageCount(100)
# 
# OSA.ask_SamplePoints()
# OSA.set_SamplePoints(1001)
# 
# OSA.ask_SegmentPoints()
# OSA.set_SegmentPoints(100)
# 
# OSA.ask_SweepSpeed()
# OSA.set_SweepSpeed(2)
# 
# 
# OSA.ask_SamplePointsAuto()
# OSA.set_SamplePointsAuto('ON')
# 
# OSA.ask_TraceActive()
# OSA.set_TraceActive('TRA')
# OSA.set_TraceActive('TRC')
# 
# 
# OSA.set_DisplayYUnit('dBm')
# HeaderX = OSA.ask_UnitX()
# HeaderY = OSA.ask_DisplayYUnit()
# 
# OSA.ask_TraceAttribute()
# OSA.set_TraceAttribute('MAX')
# 
# 
# 
# 
# 
# TestDataFunc = OSA.get_Data('TRA')
# TestDataFunc = OSA.get_Data('TRB')
# 
# 
# plt.figure()
# plt.plot(TestDataFunc['WAVelength'],TestDataFunc['dBm'])
# plt.xlabel('WAVelength')
# plt.ylabel('dBm')
# plt.grid()
# plt.show()
# 
# 
# 
# OSA.Close()
# 
# 
# 
# 
# =============================================================================
