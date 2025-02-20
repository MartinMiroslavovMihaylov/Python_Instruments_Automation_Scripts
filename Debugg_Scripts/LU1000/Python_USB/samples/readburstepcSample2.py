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

rdaddrIn = matlab.uint16([3], size=(1, 1))
addrstartIn = matlab.uint16([3], size=(1, 1))
addrstopIn = matlab.uint16([13], size=(1, 1))
wraddrIn = matlab.uint16([3], size=(1, 1))
dout1Out, OKOut = my_Python_USB.readburstepc(rdaddrIn, addrstartIn, addrstopIn, wraddrIn, nargout=2)
print(dout1Out, OKOut, sep='\n')

my_Python_USB.terminate()
