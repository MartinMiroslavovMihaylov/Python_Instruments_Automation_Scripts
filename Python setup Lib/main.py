import numpy as np
from InstrumentControl import *

# Print all the Laboratory Instruments available
obj =  InstrumentControl.InfoClass()

# Connect to Instrument by giving only the model initials
Inst = InstrumentControl.Instruments('MS2760A')


# Further information about the function can be found in the online documentation: https://martinmiroslavovmihaylov.github.io/Python_Documents/