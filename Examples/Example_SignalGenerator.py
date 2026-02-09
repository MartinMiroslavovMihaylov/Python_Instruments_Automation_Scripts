# %% ==========================================================================
# Import and Definitions
# =============================================================================
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm



# Instrument Libraries Github: https://github.com/MartinMiroslavovMihaylov/Python_Instruments_Automation_Scripts
# Install with:
# pip install git+https://github.com/MartinMiroslavovMihaylov/Python_Instruments_Automation_Scripts.git

from Instruments_Libraries.MG3694C import MG3694C  # Anritsu SigGen
from Instruments_Libraries.SMA100B import SMA100B  # Rohde&Schwarz SigGen

# %% ==========================================================================
# Select Instruments and Load Instrument Libraries
# =============================================================================
# Anritsu MG3694C Signal Generator
SignalGenerator = MG3694C("169.254.236.243")
# Find the IP adress by running "arp -a" in a terminal and search for the 
# MAC-Address of the MG3694C (written on top/back-side of the instrument). If 
# it does not show up open NI-Max or Keysight Connection Expert and try to 
# auto-discover the instrument. NI-Max works somewhat better. Do !!!NOT!!! 
# change your Network Adapter to a static IP! As of 13.01.2026 the MG3694C is 
# set up in dynamic DHCP mode.

# Rhode und Schwarz SMA100B Signal Generator
# SignalGenerator = SMA100B("169.254.2.20")
# The SMA100B is in dynamic mode. It typically shows you its IP address on the 
# instrument screen.

SignalGenerator.reset()
# %% ==========================================================================
# Setup the Measurement
# =============================================================================
sleep_time = 1 # in seconds
test_frequencies = np.linspace(1e9, 40e9, 10) # frequencies in Hz
test_powerlevels = np.atleast_1d([-4,-2]) # powerlevels in dBm

SigGen_freq_init = test_frequencies[0]
SigGen_power_init = test_powerlevels[0]

# %% ==========================================================================
# Configure the Instrument
# =============================================================================
SignalGenerator.set_freq_CW(test_frequencies[0])
SignalGenerator.set_rf_power(test_powerlevels[0])

# %% ==========================================================================
# Measurement
# =============================================================================
num_of_measurements = len(test_frequencies) * len(test_powerlevels) + 1  # 1 reference trace

# SG_Anritsu.set_output("ON") # turn on the Signal Generator

records = [] # Empty list to store data and meta data
# Loop frequencies*powerlevels
for idx in tqdm(range(num_of_measurements)):
    rec = {} # single record

    if idx < num_of_measurements - 1:
        # Do some changes, like change input frequency and power
        power_idx = int(np.floor(idx / len(test_frequencies)))
        freq_idx = np.mod(idx, len(test_frequencies))
        rec["Signal_Power"] = test_powerlevels[power_idx]
        rec["Signal_Frequency"] = test_frequencies[freq_idx]

        SignalGenerator.set_rf_power(test_powerlevels[power_idx]) # Set Power
        SignalGenerator.set_freq_CW(test_frequencies[freq_idx]) # Set Frequency
    else:  # Capture a reference measurement with no signal applied
        SignalGenerator.set_output(0) # turn OFF
        rec["Signal_Power"] = -100
        rec["Signal_Frequency"] = 0

    # Take the Measurement
    time.sleep(sleep_time)
    # rec["data_peak"] = mySpecAnalyser.ExtractTraceData(SA_TraceNum,True)
    rec["data_peak"] = idx # measure something, this is just an example

    # Write Meta Data
    rec["VCC"] = 4 # V
    
    # append the record
    rec["Timestamps"] = datetime.datetime.now()
    records.append(rec)

########################### Measurement Ends ###########################
SignalGenerator.set_output("OFF") # turn off the Signal Generator
    

# %% ==========================================================================
# Create Dataframe
# =============================================================================
meas_df = pd.DataFrame.from_records(records)

# %% ==========================================================================
# Plot the Measurement (Using only Dataframe)
# =============================================================================
plt.figure(figsize=(10, 6))

# 1. Optional: Filter out the "Reference" trace (where Freq was set to 0) 
# so it doesn't mess up the X-axis scaling.
plot_df = meas_df[meas_df["Signal_Frequency"] > 0].copy()

# 2. Group the data by 'Signal_Power'
# This automatically finds all unique power levels in the column
grouped = plot_df.groupby("Signal_Power")

# 3. Iterate through each group and plot
for power, frame in grouped:
    # 'power' is the unique value (e.g., -4)
    # 'frame' is the dataframe subset for that power
    
    # Sort by frequency to ensure lines are drawn in order
    frame = frame.sort_values(by="Signal_Frequency")
    
    plt.plot(frame["Signal_Frequency"], frame["data_peak"], 
             label=f'Power: {power} dBm', 
             marker='.')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Measured Data') 
plt.title('Frequency vs Measured Data')
plt.legend()
plt.grid(True)
plt.show()
# %% ==========================================================================
# Save Dataframe
# =============================================================================
# Save DataFrame to HDF5 (better than CSV)
meas_df.to_hdf("measurements.h5", key="data", mode="w")
# key="data" is like a "dataset name" inside the HDF5 file 
# (you can store multiple DataFrames in one file with different keys).
# mode="w" overwrites the file. Use mode="a" if you want to append new datasets.

# Later: Load it back
loaded_df = pd.read_hdf("measurements.h5", key="data")
print(loaded_df.head())

#or

# Save DataFrame to CSV
meas_df.to_csv("measurements.csv", index=False)

# Load it back, auto-parsing the "Timestamps" column as datetime
loaded_df = pd.read_csv("measurements.csv", parse_dates=["Timestamps"])
print(loaded_df.head())

# %% ==========================================================================
# Close Instrument
# =============================================================================
SignalGenerator.Close()