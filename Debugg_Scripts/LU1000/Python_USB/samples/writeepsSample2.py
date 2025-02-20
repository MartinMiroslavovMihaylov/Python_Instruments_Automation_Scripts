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

addrIn = matlab.uint16([3], size=(1, 1))
dataIn = matlab.uint16([3], size=(1, 1))
okOut = my_Python_USB.writeeps(addrIn, dataIn)
print(okOut, sep='\n')

my_Python_USB.terminate()
