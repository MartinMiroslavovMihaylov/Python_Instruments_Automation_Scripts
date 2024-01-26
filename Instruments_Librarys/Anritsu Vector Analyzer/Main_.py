# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:40:31 2021

@author: Martin.Mihaylov
"""

import numpy as np
import MS4647B
import time as t


import vxi11
rm = vxi11.list_devices()
print(rm)



VA = MS4647B.MS4647B('TCPIP0::169.254.100.85::inst0::INSTR')


S = ['S11','S12','S13','S14','S21','S22','S23','S24','S31','S32','S33','S34','S41','S42','S43','S44']
for i in range(len(S)):
    VA.set_SelectParameter(S[i])
    t.sleep(1)
    VA.set_SmoothingState(1,'ON')
VA.RTL()

# VA.ask_SelectParameter()
# VA.set_SmoothingState(1,'ON')
# VA.ask_SmoothingState(1)
# VA.ask_SelectParameter()


# VA.set_SelectParameter('S11')
# VA.ask_SelectParameter()

# # VA.RTL()
# # VA.Close()


# # =============================================================================
# # Test Ask
# # =============================================================================

# VA.ask_SubSystemHold()
# VA.ask_TestSet()
# VA.ask_SubSystem()
# VA.ask_SweepCount()
# VA.ask_SysErrors()
# VA.ask_StatOperation()
# VA.ask_StatOperationRegister()
# VA.ask_FreqSpan()
# VA.ask_CenterFreq()
# VA.ask_CWFreq()
# VA.ask_DataFreq() 
# VA.ask_SweepChannelStatus()
# VA.ask_ParamFormInFile()
# VA.ask_RFState()
# VA.ask_SetAverageState()
# VA.ask_AverageFunctionType()
# VA.ask_AverageCount()
# VA.ask_ResolutionBW()

# # =============================================================================
# # Fail Ask
# # =============================================================================





# # =============================================================================
# # Test Set
# # =============================================================================
# VA.set_ClearAverage()
# VA.set_SubSystemHold()
# VA.set_SubSystemSing()
# VA.set_SubSystemCont()
# VA.set_DisplayScale()
# VA.set_TS3739('ON')
# VA.set_TS3739('OFF')
# VA.set_ClearError()
# VA.set_DisplayColorReset()
# VA.set_StatOperationRegister(0)
# VA.set_StartFreq(10000000)
# VA.set_StopFreq(70E9)
# VA.set_CenterFreq(3.50050000000E+010)
# VA.ser_CWFreq(5.00021410705E+010)
# VA.set_SweepChannelStatus('OFF')
# VA.set_AssignetDataPort(1,2)
# VA.set_ParamFormInFile('REIM')
# VA.set_RFState('OFF')
# VA.set_AverageFunctionType('SWE') #'swe'
# VA.set_SetAverageState('ON')
# VA.set_AverageCount(100)
# VA.set_ResolutionBW(1E+02)



# # =============================================================================
# # Fail Set
# # =============================================================================


# # =============================================================================
# # Test Mem
# # =============================================================================
# import tkinter as tk
# from tkinter import filedialog


# root = tk.Tk()
# folder_selected = filedialog.askdirectory(parent = root)
# root.destroy()


# VA.SaveData('TestMartin' ,3)


# file = VA.ask_TransferData('TestMartin',3)
# VA.SaveTransferData(file,folder_selected,'TestMartin',3)




