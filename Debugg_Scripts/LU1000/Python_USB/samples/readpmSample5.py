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
resOut, okOut = my_Python_USB.readpm(addrIn, nargout=2)
print(resOut, okOut, sep='\n')

my_Python_USB.terminate()
