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

addrIn = matlab.uint32([64], size=(1, 1))
numaddrIn = matlab.uint32([64], size=(1, 1))
dout1Out, dout2Out, dout3Out, dout4Out, okOut = my_Python_USB.readhspm(addrIn, numaddrIn, nargout=5)
print(dout1Out, dout2Out, dout3Out, dout4Out, okOut, sep='\n')

my_Python_USB.terminate()
