# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 08:19:41 2024

@author: Martin.Mihaylov
"""

import numpy as np 
import matplotlib.pyplot as plt
from SMA100B import SMA100B



SMA = SMA100B("169.254.2.20")


SMA.set_frequency_mode("CW")
SMA.set_freq_CW(1, "GHz")



SMA.Close()