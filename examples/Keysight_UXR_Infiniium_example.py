# %%
# =============================================================================
# Import and Definitions
# =============================================================================
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

sys.path.append("../Instruments_Libraries/")
from UXR import UXR

# %%===========================================================================
# Select Instruments and Load Instrument Libraries
# =============================================================================
my_UXR = UXR("TCPIP0::KEYSIGH-Q75EBO9.local::hislip0::INSTR")


# %%===========================================================================
# Setup the Measurement
# =============================================================================
my_UXR.system_header("off")  # Defaltis off and should stay off!!!
my_UXR.waveform_byteorder("LSBFirst")
my_UXR.waveform_format("WORD")  # Data Aquisition is only implemented for WORD yet.
my_UXR.waveform_streaming("off")

# %%===========================================================================
# Aquire Data
# =============================================================================
my_UXR.digitize()  # All
# my_UXR.digitize(1) # Channel 1
# my_UXR.single() #

# Display Channel1
my_UXR.channel_display(1, True, "on")  # (Channel1, write, on)

# Get the waveform data.
my_UXR.waveform_source("Chan", 1)  # select the data source e.g. 'CHAN' or 'FUNC'
data = my_UXR.waveform_data()

# %%===========================================================================
# Increment Values
# =============================================================================
data_points = my_UXR.waveform_points()
x_increment = my_UXR.waveform_x_increment()
x_origin = my_UXR.waveform_x_origin()
y_increment = my_UXR.waveform_y_increment()
y_origin = my_UXR.waveform_y_origin()

# %%===========================================================================
# plot
# =============================================================================
xvals = np.arange(data_points) * x_increment + x_origin
yvals = data * y_increment + y_origin

plt.figure()
plt.plot(xvals, yvals)
plt.xlim(-1e-9, 1e-9)
plt.ylim(-1, 1)

# %%
