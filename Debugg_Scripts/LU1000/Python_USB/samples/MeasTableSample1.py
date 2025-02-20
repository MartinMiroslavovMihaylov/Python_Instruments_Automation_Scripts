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

nsamplesIn = matlab.double([30], size=(1, 1))
normalizationIn = matlab.double([1], size=(1, 1))
dout1Out, dout2Out, dout3Out, dout4Out = my_Python_USB.MeasTable(nsamplesIn, normalizationIn, nargout=4)
print(dout1Out, dout2Out, dout3Out, dout4Out, sep='\n')

my_Python_USB.terminate()
