# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:04:21 2021

@author: Martin.Mihaylov
"""

import LU1000
import tkinter as tk 
from tkinter import filedialog
import time


# =============================================================================
# Select the Paths to COM and OCT6
# =============================================================================

# #Path COM
# root = tk.Tk()
# COM = filedialog.askdirectory(parent = root,title = 'Select COM Diretory: ')
# root.destroy()



# #Path OCT6
# root = tk.Tk()
# OCT6 = filedialog.askdirectory(parent = root,title = 'Select COM Diretory: ')
# root.destroy()


# =============================================================================
# 
# =============================================================================

LU = LU1000.LU1000()

LU.ask_LaserChannel(1)
LU.set_LaserOutput(1,'OFF')

LU.ask_Whispermode(1)
LU.ask_Power(1)
LU.set_Power(1,6.5)

LU.set_LaserOutput(1,'ON')
LU.set_Whispermode(1,'ON')


LU.ask_Frequency(1)
LU.set_Frequency(1,193.87)

LU.ask_Gridspacing(1)
LU.set_Gridspacing(1,100)
LU.set_Whispermode(1,'OFF')




# LU.set_LaserOutput(1,'OFF')
# LU.ask_LaserOutput(2)
# LU.set_LaserOutout(2,'ON')
# LU.ask_LaserOutout(2)
# LU.set_LaserOutout(2,'OFF')



# LU.ask_MaxOpticalOutputPower()
# LU.ask_MinOpticalOutputPower()
# LU.ask_Power(2)
# LU.ask_LaserMinGridFreq()


# #ungenauer eingabe
# LU.ask_Freq(1)








# LU.Close()

