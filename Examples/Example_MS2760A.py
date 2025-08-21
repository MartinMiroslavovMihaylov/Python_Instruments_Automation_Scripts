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

# from Instruments_Libraries.MS2760A import MS2760A  # SpectrumAnalyzer
from Instruments_Libraries.InstrumentSelect import SpecAnalyser

# %% ==========================================================================
# Select Instruments and Load Instrument Libraries
# =============================================================================
# mySpecAnalyser = MS2760A('127.0.0.1')
mySpecAnalyser = SpecAnalyser()
mySpecAnalyser.reset()

# %% ==========================================================================
# Setup the Measurement
# =============================================================================
num_of_points = 10
sleep_time = 1 # in seconds
freq = np.linspace(1e9, 40e9, num_of_points)

# Initial Spectrum Analyzer Sweep Settings
SA_TraceNum = 1  # only for Anrisu MS2760A
SA_f_min = 0
SA_f_max = 40e9
SA_resBW = 100e3
SA_ref_level = -10  # dBm
datapoints = 4001

# %% ==========================================================================
# Configure the Instrument
# =============================================================================
mySpecAnalyser.set_Continuous('OFF')
# time.sleep(0.5) # probably not needed
mySpecAnalyser.set_DataPointCount(datapoints)
mySpecAnalyser.set_RefLevel(SA_ref_level) # in dBm
mySpecAnalyser.set_IFGainState('ON') # Enable IF Gain (need ref level <= -10dBm)
mySpecAnalyser.set_ResBwidth(SA_resBW, 'HZ')
mySpecAnalyser.set_freq_Stop(SA_f_max, 'HZ')
mySpecAnalyser.set_freq_Start(SA_f_min, 'HZ')
mySpecAnalyser.set_TraceType('NORM', SA_TraceNum)
# Detector Type: POS -> Peak (default), others are: RMS, NEG
mySpecAnalyser.set_DetectorType('POS', SA_TraceNum) 

# %% ==========================================================================
# Measurement
# =============================================================================

records = [] # Empty list to store data and meta data
for i in tqdm(range(num_of_points)):
    rec = {} # single record

    # Do some changes, like change input frequency
    # SignalGenerator.set_freq_CW(freq[i])

    # Write Meta Data
    rec["SA f_min"] = SA_f_min
    rec["SA f_max"] = SA_f_max
    rec["SA ref level"] = SA_ref_level
    rec["SA Resolution BW"] = SA_resBW

    # Take the Measurement
    time.sleep(sleep_time)
    rec["data_peak"] = mySpecAnalyser.ExtractTraceData(SA_TraceNum,True)

    # append the record
    rec["Timestamps"] = datetime.datetime.now()
    records.append(rec)
    

# %% ==========================================================================
# Create Dataframe
# =============================================================================
meas_df = pd.DataFrame.from_records(records)

# %% ==========================================================================
# Plot the Measurement
# =============================================================================
freq_hz = SA_f_min + np.arange(datapoints) * (SA_f_max - SA_f_min) / (datapoints - 1)
power_dBm = np.vstack(meas_df["data_peak"])

plt.plot(freq_hz, meas_df["data_peak"][0])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dBm)')
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
mySpecAnalyser.Close()
