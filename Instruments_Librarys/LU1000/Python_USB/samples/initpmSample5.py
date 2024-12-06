#!/usr/bin/env python
"""
Sample script that uses the Python_USB package created using
MATLAB Compiler SDK.

Refer to the MATLAB Compiler SDK documentation for more information.
"""

from __future__ import print_function
import Python_USB
import matlab

my_Python_USB = Python_USB.initialize()

selIn = matlab.uint16([2], size=(1, 1))
LastDevDescrIn = "PM1000-100M-XL-FA-NN-D 44"
okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut = my_Python_USB.initpm(selIn, LastDevDescrIn, nargout=5)
print(okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut, sep='\n')

my_Python_USB.terminate()
