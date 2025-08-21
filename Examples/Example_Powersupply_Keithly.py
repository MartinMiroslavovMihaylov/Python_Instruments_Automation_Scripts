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

# from Instruments_Libraries.KEITHLEY2612 import KEITHLEY2612
from Instruments_Libraries.InstrumentSelect import SourceMeter

# %% ==========================================================================
# Select Instruments and Load Instrument Libraries
# =============================================================================
# myKEITHLEY2612 = KEITHLEY2612('COMXX') # replace with your COM Port
myKEITHLEY2612 = SourceMeter()
myKEITHLEY2612.reset()

# %% ==========================================================================
# Setup the Measurement
# =============================================================================
num_of_points = 10
sleep_time = 0.5
vcc_ch_num = 'a' # channel for VCC
vcc = 4.7 # V
vcc_current_limit = 0.140 # A

# %% ==========================================================================
# Configure the Instrument
# =============================================================================
myKEITHLEY2612.set_Voltage(vcc_ch_num, vcc)
myKEITHLEY2612.set_CurrentLimit(vcc_ch_num, vcc_current_limit)

# or convenience method: Configure Instrument as Voltage Source (measuring current)
myKEITHLEY2612.setup_voltage_source(vcc_ch_num, vcc, vcc_current_limit)

# %% ==========================================================================
# Measurement
# =============================================================================
myKEITHLEY2612.set_Out(channel=vcc_ch_num, state='ON') # turn on the channel

records = [] # Empty list to store data and meta data
for i in tqdm(range(num_of_points)):
    rec = {} # single record
    rec["VCC_Voltage"] = myKEITHLEY2612.ask_Voltage(vcc_ch_num)
    rec["VCC_Current"] = myKEITHLEY2612.ask_Current(vcc_ch_num)
    rec["Timestamps"] = datetime.datetime.now()
    records.append(rec)
    time.sleep(sleep_time)

# %% ==========================================================================
# Create Dataframe
# =============================================================================
meas_df = pd.DataFrame.from_records(records)

# %% ==========================================================================
# Plot the Measurement
# =============================================================================
t0 = meas_df["Timestamps"].iloc[0]
relative_time = (meas_df["Timestamps"] - t0).dt.total_seconds()

plt.plot(relative_time, meas_df["VCC_Current"])
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
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
myKEITHLEY2612.Close()
