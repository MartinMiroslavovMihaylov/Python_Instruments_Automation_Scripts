"""
Created on Wed Feb 26 20:21:23 2025

@author: Maxim Weizel
@contributor: Rakibul Islam
"""


import numpy as np
from time import time, sleep
import logging
import pyvisa
import pandas as pd 
import csv


class FSWP50:
    '''
    This class is using PyVISA to connect. Requires NI-VISA or Keysight VISA backend.
    '''
    def __init__(self, address: str):
        rm = pyvisa.ResourceManager()
        self.address =address
        self._resource = rm.open_resource(f"TCPIP::{address}::INSTR")
        self._resource.timeout = 10000  # in milliseconds
        print(self._resource.query('*IDN?'))

        # Internal Variables
        self._freq_Units_List = ['HZ', 'KHZ', 'MHZ', 'GHZ']
        self._state_List = ['OFF', 'ON', 1 , 0]
        self._trace_List = [1, 2, 3, 4, 5, 6]  # <t> in documentation
        self._window_List = list(range(1, 17))  # <n> in documentation
    
    
    
    def write_str(self, command: str):
        try:
            self._resource.write(command)
        except Exception as e:
            logging.error(e)

    def write_float(self, command: str, value: float) -> None:
        try:
            self._resource.write(f"{command} {value}")
        except Exception as e:
            logging.error(e)

    def query_str(self, command: str) -> str:
        try:
            return self._resource.query(command).strip()
        except Exception as e:
            logging.error(e)

    def query_str_list(self, command: str) -> list:
        try:
            response = self._resource.query(command)
            return [s.strip() for s in response.split(',')]
        except Exception as e:
            logging.error(e)

    def query_float(self, command: str) -> float:
        try:
            return float(self._resource.query(command))
        except Exception as e:
            logging.error(e)

    def query_float_list(self, command: str) -> list:
        try:
            response = self._resource.query(command)
            return list(map(float, response.strip().split(',')))
        except Exception as e:
            logging.error(e)
        
# =============================================================================
# Basic Functions
# =============================================================================

    def Idn(self) -> str:
        '''Identify the Insturment.

        Returns
        -------
        str
            A string with the Instrument name.
        '''
        return self.query_str('*IDN?')

    def reset(self) -> None:
        '''Reset the instrument (execute ``*RST`` command).'''
        self.write_str("*RST")

    def clear(self) -> None:
        '''Clear the instrument status (execute ``*CLS`` command).'''
        self.write_str("*CLS")

    def wait(self) -> None:
        '''
        Wait to continue. Prevents servicing of the subsequent commands until 
        all preceding commands have been executed and all signals have settled 
        (see also command synchronization and ``*OPC`` command).
        '''
        self.write_str("*WAI")

    def operation_complete(self) -> int:
        '''Wait until the operation is complete (execute ``*OPC`` command).'''
        return int(self.query_float("*OPC?"))

    def abort(self) -> None:
        '''Abort the measurement (execute ABORT command).'''
        self.write_str("ABORt")
        self.wait()


    def Close(self):
        """Closes the connection to the instrument."""
        self._resource.close()
        print(f"Connection to {self.address} closed.")

# =============================================================================
# Start Measurment
# =============================================================================
    def set_continuous(self, state: int|str) -> None:
        '''
        Controls the measurement mode for an individual channel.

        Parameters
        ----------
        state : int or str
            ``ON | OFF | 1 | 0``
        '''
        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write_str(f"INITiate:CONT {state}")
        else:
            raise ValueError('Invalid State Selected')
    set_Continuous = set_continuous # alias
        
    def init_single_measurement(self) -> None:
        '''
        Restarts a (single) measurement that has been stopped (using ABORt) 
        or finished in single measurement mode.
        The measurement is restarted at the beginning, not where the previous 
        measurement was stopped.
        As opposed to INITiate<n>[:IMMediate], this command does not reset traces in
        maxhold, minhold or average mode. Therefore it can be used to continue 
        measurements using maxhold or averaging functions.
        '''
        self.write_str("INITiate:CONMeas")


    def Init(self) -> None:
        '''
        Starts a (single) new measurement.
        With measurement count or average count > 0, this means a restart of the 
        corresponding number of measurements. With trace mode MAXHold, MINHold and 
        AVERage, the previous results are reset on restarting the measurement.
        '''
        self.write_str("INITiate:IMMediate")

# =============================================================================
#                    Selecting mode and applications RAKIBUL SECTION
# =============================================================================



    def set_multiview_tab(self, state):
        """
        Toggles the MultiView tab display.

        Parameters
        ----------
        state : bool or int
            True/1 to enable MultiView (ON), False/0 to disable (OFF).

        Raises
        ------
        ValueError if the input is not valid.
        """
        if state in [True, 1]:
            value = 'ON'
        elif state in [False, 0]:
            value = 'OFF'
        else:
            raise ValueError("Invalid input: use True/False or 1/0")

        self.write_str(f'DISPlay:ATAB {value}')


    def duplicate_selected_channel(self, channel_name):
        """
        Docstring for duplicate_selected_channel
        
        Parameters
        ----------
        channel_name : str
            Duplicates the channel. For example if channel named 'PhaseNoise' is selected 
            then new copy of the selected channel with named 'PhaseNoise 2' will be created.

        Raises
        ------
        ValueError if the input is not valid.
        
        """
      
        #channel_name = input("Enter the channel name to duplicate (e.g., PhaseNoise): ").strip()

        # Select the channel
        try:
            self.write_str(f"INSTrument:SELect '{channel_name}'")
            sleep(0.1)  # Ensure the selection is registered
        except Exception as e:
            raise RuntimeError(f"Failed to select channel '{channel_name}': {e}")

        # Duplicate the selected channel
        try:
            self.write_str("INSTrument:CREate:DUPLicate")
            print(f"Channel '{channel_name}' duplicated successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to duplicate channel '{channel_name}': {e}")


    def create_channel(self, channel_type: str, channel_name: str) -> None:
        """
        Creates a new measurement channel.

        Parameters
        ----------
        channel_type : str
            Channel type . Available type are : 
                                        'PNOISE': 'Phase Noise',
                                        'SMONITOR': 'Spectrum Monitor',
                                        'SANALYZER': 'Spectrum (R&S FSWP-B1)',
                                        'IQ': 'I/Q Analyzer',
                                        'PULSE': 'Pulse Measurement',
                                        'ADEMOD': 'Analog modulation analysis',
                                        'NOISE': 'Noise Figure Measurements',
                                        'SPUR': 'Fast Spur Search',
                                        'TA': 'Transient Analysis',
                                        'DDEM': 'VSA - Vector Signal Analysis'
        channel_name : str
            Unique name for the new channel.

        Raises
        ------
        ValueError
            If channel type is invalid or name already exists.
        RuntimeError
            If instrument command fails.
        """

        available_types = {
            'PNOISE': 'Phase Noise',
            'SMONITOR': 'Spectrum Monitor',
            'SANALYZER': 'Spectrum (R&S FSWP-B1)',
            'IQ': 'I/Q Analyzer',
            'PULSE': 'Pulse Measurement',
            'ADEMOD': 'Analog modulation analysis',
            'NOISE': 'Noise Figure Measurements',
            'SPUR': 'Fast Spur Search',
            'TA': 'Transient Analysis',
            'DDEM': 'VSA - Vector Signal Analysis'
        }

        # --- Normalize input ---
        if not isinstance(channel_type, str):
            raise ValueError("channel_type must be a string")

        if not isinstance(channel_name, str) or not channel_name.strip():
            raise ValueError("channel_name must be a non-empty string")

        channel_type = channel_type.strip().upper()
        channel_name = channel_name.strip()

        # --- Validate channel type ---
        if channel_type not in available_types:
            valid = ", ".join(available_types.keys())
            raise ValueError(f"Invalid channel type '{channel_type}'. Valid types: {valid}")

        # --- Check existing channel names ---
        try:
            existing_channels = self.query_str("INSTrument:LIST?").replace("'", "").split(",")
            existing_names = [
                name.strip()
                for i, name in enumerate(existing_channels)
                if i % 2 == 1
            ]

            if channel_name in existing_names:
                raise ValueError(f"Channel name '{channel_name}' already exists.")

            # --- Create channel ---
            self.write_str(f"INSTrument:CREate {channel_type}, '{channel_name}'")

        except Exception as e:
            raise RuntimeError(f"Failed to create channel '{channel_name}': {e}")


    def list_channels(self) -> str:
        '''
        Queries all active channels. The query is useful to obtain the names of the existing
        channels, which are required to replace or delete the channels.
        '''
        return self.query_str_list("INSTrument:LIST?")



    def delete_channel(self, ChannelName:str) -> None:
        '''
        Deletes a channel.
        If you delete the last channel, the default "Phase Noise" channel is activated.

        Parameters
        ----------
        ChannelName : str
            Your Channel Name.
        '''
        self.write_str(f":INST:DEL '{ChannelName}'")

    
    
    def set_center_frequency(self, center_freq: int | float, unit: str = 'Hz') -> None:
        """
        Sets the center frequency for pulsed and VCO measurements
    
        Parameters
        ----------
        center_freq : int | float
            Frequency value (e.g., 1, 2.5) to be combined with unit.
        unit : str, optional
            Unit of frequency: HZ, KHZ, MHZ, or GHZ. Default is 'Hz'.
    
        Raises
        ------
        ValueError if unit is invalid.
        """
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write_str(f"FREQ:CENT {center_freq} {unit}")
            print(f"Center frequency set to {center_freq} {unit}")
        else:
            raise ValueError("Unknown unit! Use one of: HZ, KHZ, MHZ, GHZ")    

###############
# Not Tested 
###############
    def ask_center_frequency(self, center_freq: int | float, unit: str = 'Hz') -> None:
        """
        Query the center frequency for pulsed and VCO measurements
    
        Parameters
        ----------
    
        Raises
        ------
        ValueError if unit is invalid.
        """
        return self.query_str_list("FREQ:CENT?")  
      


    def set_start_frequency(self, start_freq: int|float, unit:str = 'Hz') -> None:
        '''
        This command defines the start frequency offset of the measurement range.

        Parameters
        ----------
        start_freq : float
            Start frequency.
        '''
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write_str(f":SENS:FREQ:STAR {start_freq}{unit}")
        else:
            raise ValueError(
                'Unknown unit! Should be HZ, KHZ, MHZ or GHZ')


    def set_stop_frequency(self, stop_freq: int|float, unit:str = 'Hz') -> None:
        '''
        This command defines the stop frequency offset of the measurement range.

        Parameters
        ----------
        start_freq : float
            Stop frequency.
        '''
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write_str(f":SENS:FREQ:STOP {stop_freq}{unit}")
        else:
            raise ValueError(
                'Unknown unit! Should be HZ, KHZ, MHZ or GHZ')
        

    def set_span(self, span: int | float, unit: str = 'Hz') -> None:
        """
        Sets the frequency span for the spectrum analyzer.

        Parameters
        ----------
        span : int | float
        Span value (e.g., 100 for 100 MHz).
        unit : str
        Frequency unit: HZ, KHZ, MHZ, or GHZ. Default is 'Hz'.
        """
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write_str(f"FREQ:SPAN {span}{unit}")
            print(f"Span set to {span}{unit}")
        else:
            raise ValueError("Unknown unit! Should be HZ, KHZ, MHZ, or GHZ.")


    
    def get_span(self, unit: str = 'MHz') -> float:
        """
        Queries the current frequency span and returns it in the desired unit.

        Parameters
        ----------
        unit : str, optional
            Output unit: 'Hz', 'kHz', 'MHz', or 'GHz'. Default is 'MHz'.

        Returns
        -------
        float
            Span in the selected unit.

        Raises
        ------
        ValueError
            If the unit is not recognized.
        RuntimeError
            If querying fails.
        """
        unit = unit.upper()
        conversion_factors = {
            'HZ': 1,
            'KHZ': 1e-3,
            'MHZ': 1e-6,
            'GHZ': 1e-9
        }

        if unit not in conversion_factors:
            raise ValueError("Invalid unit! Use one of: Hz, kHz, MHz, GHz.")

        try:
            span_hz = float(self.query_str("FREQ:SPAN?"))
            converted = span_hz * conversion_factors[unit]
            print(f"Current span: {converted} {unit}")
            return converted
        except Exception as e:
            raise RuntimeError(f"Failed to query span: {e}")
    
                                     
####################
# Not Tested
####################                                                    
             
    def set_resolution_bandwidth(self, res_bw:int|float, unit:str = 'Hz') -> None:
        '''
        Sets the resolution bandwidth.

        Parameters
        ----------
        value : int/float
            Sets the resolution bandwidth.
            
        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}
            Default Unit: Hz

        Raises
        ------
        ValueError
            Error message
        '''
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write_float(":SENS:BAND:RES", res_bw)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


#########################
# Not Tested
#########################

    def set_reference_level(self, ref_level: float) -> None:
        '''
        This command defines the maximum level displayed on the y-axis.

        Parameters
        ----------
        ref_level : float
            Default unit: Depending on the selected diagram.
        '''
        self.write_float(":DISP:WIND:TRAC:Y:SCAL:RLEV", ref_level)



 ##############################
 # Function not available but somehow the input is taken from the device!!!
 ############################## 
    def set_reference_level_lower(self, ref_level: float = 0) -> None:
        '''
        This command defines the minimum level displayed on the y-axis.

        Parameters
        ----------
        ref_level : float, optional
            Default unit: Depending on the selected diagram.
        '''
        self.write_float(":DISP:WIND:TRAC:Y:SCAL:RLEV:LOW", ref_level)



  ##############################
 # Function not available but somehow the input is taken from the device!!!
 ##############################        
    def set_input_attenuation_auto(self, state: str|int) -> None:
        '''Set the input attenuation auto mode to ON or OFF.

        Parameters
        ----------
        state : str | int
            Can be: [ON, 1, OFF, 0]

        Raises
        ------
        ValueError
            Error Message
        '''
        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write_str(f":INP:ATT:AUTO {state}")
        else:
            raise ValueError('Invalid State Selected')


 ##############################
 # Function not available but somehow the input is taken !!!
 ##############################        
    def set_input_attenuation(self, atten: float) -> None:
        '''Set the input attenuation.

        Parameters
        ----------
        atten : float
            Attenuation value.
        '''
        self.write_float(":INP:ATT", atten)

        
    def set_detection_function(self, det_func: str, trace_number: int = 1,
                               window_number: int = 1) -> None:
        '''
        Defines the trace detector to be used for trace analysis

        Parameters
        ----------
        det_func : str
            detector function: APEAK|NEGATIVE|POSITIVE|RMS|AVERAGE|SAMPLE

        Raises
        ------
        ValueError
            Error Message
        '''
        det_func_List = ['APEAK', 'APE', 'NEGATIVE', 'NEG', 'POSITIVE', 'POS', 'RMS',
                         'AVERAGE', 'AVER', 'SAMPLE', 'SAMP']
        det_func = det_func.upper() if isinstance(det_func, str) else det_func
        if det_func in det_func_List:
            self.write_str(f":SENS:WIND{window_number}:DET{trace_number}:FUNC {det_func}")
        else:
            raise ValueError('Unknown input! See function description for more info.')
        

 ##############################
 # Function have an potential error in the code 
 ############################## 

    def set_trace_mode(self, trace_mode: str, trace_number: int = 1, window_number: int = 1) -> None:
        '''Selects the trace mode.

        Parameters
        ----------
        trace_mode : str
            WRITE|WRIT|AVERAGE|AVER|MAXHOLD|MAXH|MINHOLD|MINH|VIEW|BLANK|BLAN
        trace_number : int, optional
            Trace Number, by default 1
        window_number : int, optional
            Window Number, by default 1

        Raises
        ------
        ValueError
            Error Message
        '''
        trace_mode_List = ['WRITE', 'WRIT', 'AVERAGE', 'AVER', 'MAXHOLD', 'MAXH', 'MINHOLD'
                           'MINH', 'VIEW', 'BLANK', 'BLAN']
        trace_mode = trace_mode.upper() if isinstance(trace_mode, str) else trace_mode
        if trace_mode in trace_mode_List:
            self.write_str(f"DISPlay:WINDOW{window_number}:TRACE{trace_number}:MODE {trace_mode}")
        else:
            raise ValueError('Unknown input! See function description for more info.')
        



    def set_sweep_points(self, datapoints: int) -> None:
        """
        This command defines the number of measurement points to analyze after a measurement.
        
        Parameters:
            datapoints (int): Number of data points.
        """
        if isinstance(datapoints, int):
            if 101 <= datapoints <= 100001:
                self.write_float(":SENS:SWE:WIND:POIN", datapoints)
            else:
                raise ValueError(f'Value must be between 10 and 10001, not {datapoints}')
        else:
            raise ValueError(f'Value must be an integer, not {datapoints}')
    set_DataPointCount = set_sweep_points



# =============================================================================
# Get Data
# =============================================================================
 ##############################
 # No data to be tested!
 ############################## 


    def get_trace_data(self, trace_number: int, window_number: int = 1) -> np.ndarray:
        '''
        This command queries current trace data and measurement results.

        Parameters
        ----------
        trace_number : int
            Trace number between 1 and 6
        window_number : int, optional
            Window number between 1 and 16, by default 1

        Returns
        -------
        np.ndarray
            Trace Data.

        Raises
        ------
        ValueError
        '''
        if trace_number not in self._trace_List or not isinstance(trace_number, int):
            raise ValueError(
                f'Unknown trace number! Should be between 1 and 6, but you wrote {trace_number}')
        if window_number not in self._window_List or not isinstance(window_number, int):
            raise ValueError(
                f'Unknown window number! Should be between 1 and 16, but you wrote {window_number}')
        data = self.query_float_list(f":TRAC{window_number}:DATA? TRACE{trace_number}")
        return np.array(data)


 ##############################
 # No data to be tested!
 ############################## 
    def ExtractTraceData(self, traceNumber:int = 1, clearTrace:bool = True,
                         timeout:float = 20, window_number: int = 1) -> np.ndarray:
        '''
        Initiate a measurement and return the trace data.

        Parameters
        ----------
        traceNumber : int
            Trace Number:
                Can be set to  [1,2,3,4,5,6].
        clearTrace : bool, optional
            Clears the trace before taking the data measurement. The default is True.
        timeout : float, optional
            Defines the timeout for the operation. The default is 20s.
        window_number : int, optional
            Window number between 1 and 16, by default 1

        Raises
        ------
        TimeoutError

        Returns
        -------
        Output : np.array

        '''
        
        if traceNumber not in self._trace_List:
            raise ValueError(
                f"Invalid trace number: {traceNumber}. Must be in {self._trace_List}.")
        if window_number not in self._window_List or not isinstance(window_number, int):
            raise ValueError(
                f'Unknown window number! Should be between 1 and 16, but you wrote {window_number}')
        
        
        self.set_continuous('OFF')
        
        #Check the data format
        # if self._dataFormat != 'ASC,8':
        #     self.set_DataFormat('ASCii')

        if clearTrace:
            self.abort()
            self.Init()
            self.wait()
            start_time = time()
            complete = 0
            while complete == 0:
                sleep(0.1)
                complete = self.operation_complete()
                if time() - start_time > timeout:
                    raise TimeoutError(f"Operation did not complete within {timeout:.2f} seconds.")

        return self.get_trace_data(traceNumber, window_number)



 ##############################
 # No data to be tested!
 ############################## 
    def export_trace_to_csv(self, data: np.ndarray, filename: str = "trace_output.csv"):
        """
        Exports the given trace data to a CSV file.

        Parameters
        ----------
        data : np.ndarray
            The trace data to export.
        filename : str, optional
            The name of the CSV file. Default is 'trace_output.csv'.
        """
        if not isinstance(data, np.ndarray):
            raise TypeError("Data must be a numpy array.")

        try:
            df = pd.DataFrame({
                "Index": np.arange(len(data)),
                "Amplitude (dB)": data
            })

            df.to_csv(filename, index=False)

            print(f"Trace data exported successfully to '{os.path.abspath(filename)}'")

        except Exception as e:
            raise RuntimeError(f"Failed to write CSV: {e}")
            
    
    
# =============================================================================
# Phase Noise 
# =============================================================================


    def set_start_offset(self, start_offset: int | float, unit: str = 'Hz') -> None:
        """
        Sets the start offset frequency for phase noise measurement.
    
      Reference: User manual, page number 481
    
        Parameters
        ----------
        start_offset : int or float
            The numeric value of the start offset.

    
        unit : str, optional
            Unit of the offset. Accepted values: 'Hz', 'kHz', 'MHz', 'GHz'.
            Default is 'Hz'.
    
        Raises
        ------
        ValueError
            If an invalid unit is provided.
    
        """
        unit = unit.upper()
        if unit not in self._freq_Units_List:
            raise ValueError("Unknown unit! Use HZ, KHZ, MHZ, or GHZ.")
        self.write_str(f"SENSe:FREQuency:STARt {start_offset}{unit}")
        print(f"Start offset set to {start_offset}{unit}")




    def ask_start_offset(self, unit: str = 'Hz') -> float:
        """
        Queries the current start offset frequency for phase noise measurement.
    
    
        Parameters
        ----------
        unit : str, optional
            Output unit. Accepted values: 'Hz', 'kHz', 'MHz', 'GHz'. Default is 'Hz'.
    
        Returns
        -------
        float
            Start offset frequency in the specified unit.
    
        Raises
        ------
        ValueError
            If an invalid unit is requested.
        """
        unit = unit.upper()
        if unit not in self._freq_Units_List:
            raise ValueError("Invalid unit. Choose from Hz, kHz, MHz, GHz.")
    
        freq_hz = float(self.query_str("SENSe:FREQuency:STARt?"))
    
        conversion = {
            'HZ': 1,
            'KHZ': 1e3,
            'MHZ': 1e6,
            'GHZ': 1e9
        }
    
        value = freq_hz / conversion[unit]
        print(f"Start offset: {value} {unit}")
        return value
    



    def set_stop_offset(self, stop_offset: int | float, unit: str = 'Hz') -> None:
        """
        Sets the stop offset frequency for phase noise measurement.
      
           Reference: User manual, page number 482
    
        Parameters
        ----------
        stop_offset : int or float
            The numeric value of the stop offset.
    
        unit : str, optional
            Unit of the offset. Accepted values: 'Hz', 'kHz', 'MHz', 'GHz'.
            Default is 'Hz'.
    
        Raises
        ------
        ValueError
            If an invalid unit is provided.
      
        """
        unit = unit.upper()
        if unit not in self._freq_Units_List:
            raise ValueError("Unknown unit! Use HZ, KHZ, MHZ, or GHZ.")
        self.write_str(f"SENSe:FREQuency:STOP {stop_offset}{unit}")
        print(f"Stop offset set to {stop_offset}{unit}")
    
 
    
    def ask_stop_offset(self, unit: str = 'Hz') -> float:
        """
        Queries the stop offset frequency for phase noise measurement.
    
        Parameters
        ----------
        unit : str, optional
            Output unit. One of 'Hz', 'kHz', 'MHz', 'GHz'. Default is 'Hz'.
    
        Returns
        -------
        float
            The stop offset frequency in the selected unit.
        """
        unit = unit.upper()
        scale_factors = {
            'HZ': 1,
            'KHZ': 1e-3,
            'MHZ': 1e-6,
            'GHZ': 1e-9
        }
    
        if unit not in scale_factors:
            raise ValueError("Invalid unit! Choose from 'Hz', 'kHz', 'MHz', or 'GHz'.")
    
        try:
            response = self.query_str("SENSe:FREQuency:STOP?")
            stop_hz = float(response)
            converted = stop_hz * scale_factors[unit]
            print(f"Stop offset frequency: {converted} {unit}")
            return converted
        except Exception as e:
            raise RuntimeError(f"Failed to query stop offset frequency: {e}")

    
 ##############################
 # Need to be tested. It was rewriten from original function
 ############################## 

    def set_rbw_ratio(self, percentage: float) -> None:
        """
        Set RBW as a ratio (%) of start offset (automatic mode).

        Parameters
        ----------
        percentage : float
            RBW ratio in percent (0.1 to 30).

        Raises
        ------
        ValueError
            If percentage is out of range.
        RuntimeError
            If instrument command fails.
        """

        try:
            if not isinstance(percentage, (int, float)):
                raise ValueError("percentage must be numeric")

            if not (0.1 <= float(percentage) <= 30):
                raise ValueError("Percentage must be between 0.1 and 30.")

            self.write_str("SWE:MODE NORM")
            self.write_float("LIST:BWID:RAT", float(percentage))

        except Exception as e:
            raise RuntimeError(f"Failed to set RBW ratio: {e}")       


 ##############################
 # Need to be tested. It was rewriten from original function
 ############################## 

    def set_rbw_absolute(self, half_decade: int, bandwidth: float, unit: str) -> None:
        """
        Set absolute RBW for a specific half-decade (manual mode).

        Parameters
        ----------
        half_decade : int
            Half-decade index (1 ... N depending on sweep range).
        bandwidth : float
            RBW value.
        unit : str
            One of: Hz, kHz, MHz

        Raises
        ------
        ValueError
            If parameters are invalid.
        RuntimeError
            If instrument command fails.
        """

        try:
            if not isinstance(half_decade, int) or half_decade < 1:
                raise ValueError("half_decade must be integer >= 1")

            if not isinstance(bandwidth, (int, float)) or bandwidth <= 0:
                raise ValueError("bandwidth must be positive number")

            if not isinstance(unit, str):
                raise ValueError("unit must be string")

            unit = unit.strip().upper()

            if unit not in ["HZ", "KHZ", "MHZ"]:
                raise ValueError("Invalid unit. Use Hz, kHz, or MHz.")

            self.write_str("SWE:MODE MAN")
            self.write_str(f"LIST:RANG{half_decade}:BWID {float(bandwidth)}{unit}")

        except Exception as e:
            raise RuntimeError(f"Failed to set manual RBW: {e}")
                


 ##############################
 # Working for % case. The other cannot be tested!
 ############################## 

    def ask_rbw(self):
        """
        Queries the current Resolution Bandwidth (RBW) setting for phase noise.
    
        - Automatically detects if the mode is 'NORM' (automatic ratio) or 'MAN' (manual).
        - Returns the RBW ratio (%) or manual RBW values per half-decade.
    
        Reference:
            - RBW Ratio: LIST:BWID:RAT? (Page 485)
            - Manual RBW: LIST:RANG<ri>:BWID? (Page 485)
            - Mode: SWE:MODE? (Page 488)
        """
        try:
            mode = self.query_str("SWE:MODE?").strip().upper()
    
            if mode == "NORM":
                percentage = float(self.query_str("LIST:BWID:RAT?"))
                print(f"RBW Mode: Automatic Ratio → {percentage}% of start offset")
                return percentage
    
            elif mode == "MAN":
                rbw_values = {}
                for ri in range(1, 11):  # Half-decades 1 to 10
                    try:
                        val = self.query_str(f"LIST:RANG{ri}:BWID?")
                        rbw_values[ri] = val
                    except:
                        continue
                print("RBW Mode: Manual (Absolute values per half-decade):")
                for k, v in rbw_values.items():
                    print(f"  Half-decade {k}: {v}")
                return rbw_values
    
            else:
                raise RuntimeError(f"Unknown RBW mode detected: '{mode}'")
    
        except Exception as e:
            raise RuntimeError(f"Failed to query RBW setting: {e}")
    


            
            
    
    def set_xcorr_factor_auto(self, factor: int = 1):
        """
        Sets the cross-correlation factor in automatic (normal) mode for phase noise.
        
    
        Reference:
            User Manual, page 490.
            Defining cross-correlation parameters: page 169
    
        Parameters
        ----------
        factor : int
            Cross-correlation factor. Must be an integer >= 1.
    
        Raises
        ------
        ValueError
            If the factor is not an integer or less than 1.
        """
        if not isinstance(factor, int) or factor < 1:
            raise ValueError("XCORR factor must be an integer >= 1.")
    
        self.write_str("SWE:MODE NORM")        # Switch to automatic configuration mode
        self.write_float("SWE:XFAC", factor)   # Set cross-correlation factor
        print(f"Automatic XCORR factor set to {factor}")



 ##############################
 # Need to be tested. Function was rewriten !
 ############################## 

    def set_xcorr_optimization(self, enable: bool, threshold: float = None) -> None:
        """
        Configure XCORR optimization and optional threshold.

        Parameters
        ----------
        enable : bool
            Enable (True) or disable (False) XCORR optimization.
        threshold : float, optional
            Optional threshold in dB. Only used if enable=True.

        Raises
        ------
        ValueError
            If threshold is invalid (non-numeric) or provided when optimization is disabled.
        RuntimeError
            If SCPI command fails.
        """

        try:
            # --- Enable or disable optimization ---
            state_str = "ON" if enable else "OFF"
            self.write_str(f"SWE:XOPT {state_str}")

            # --- Optional threshold ---
            if enable and threshold is not None:
                if not isinstance(threshold, (int, float)):
                    raise ValueError("threshold must be numeric (float or int).")
                self.write_float("SWE:XOPT:THR", float(threshold))

        except Exception as e:
            raise RuntimeError(f"Failed to configure XCORR optimization: {e}")



 ##############################
 # Need to be tested. It was rework
 ############################## 

    def set_capture_range(self, mode: str) -> None:
        """
        Set the Capture Range for Phase Noise measurement.

        Parameters
        ----------
        mode : str
            Capture Range mode. Options:
            - "Normal" or "NORM" → Normal range (stable DUTs)
            - "Wide" or "WIDE"   → Wide range (fast-drifting DUTs)
            - "40MHz" or "R40MHZ" → ±40 MHz around center frequency

        Raises
        ------
        ValueError
            If an invalid mode is provided.
        RuntimeError
            If SCPI command fails.
        """

        # --- Normalize input ---
        if not isinstance(mode, str):
            raise ValueError("mode must be a string")

        mode_map = {
            "NORMAL": "NORM",
            "NORM": "NORM",
            "WIDE": "WIDE",
            "40MHZ": "R40MHZ",
            "R40MHZ": "R40MHZ"
        }

        mode_key = mode.strip().upper()
        if mode_key not in mode_map:
            valid_modes = ", ".join(["Normal", "Wide", "40MHz"])
            raise ValueError(f"Invalid mode '{mode}'. Valid options: {valid_modes}")

        # --- Set capture range ---
        try:
            self.write_str(f"SWE:CAPT:RANG {mode_map[mode_key]}")
        except Exception as e:
            raise RuntimeError(f"Failed to set Capture Range: {e}")


# =============================================================================
# Integrated Measurements
# =============================================================================


    def set_integration_manual(self, range_index: int, start_freq: str, stop_freq: str):
        """
        Sets a custom integration range for the Integrated Measurement tab.
    
        Parameters
        ----------
        range_index : int
            Integration range index (1–10).
        start_freq : str
            Start frequency with unit (e.g., '10Hz', '1kHz', '100MHz').
        stop_freq : str
            Stop frequency with unit (e.g., '100kHz', '1MHz').

    
        Manual Reference:
            - Page 173–174: Defining the integration range
            - Page 490+: SCPI syntax
    
        Raises
        ------
        ValueError
            If range_index is not between 1 and 10.
        RuntimeError
            On communication failure.
        """
        try:
            if range_index not in range(1, 11):
                raise ValueError("Invalid range index. Must be between 1 and 10.")
    
            self.write_str(f"CALC1:RANG{range_index}:EVAL:STAT OFF")
            self.write_str(f"CALC1:RANG{range_index}:EVAL:STAR {start_freq}")
            self.write_str(f"CALC1:RANG{range_index}:EVAL:STOP {stop_freq}")
    
            print(f"Integration range {range_index} set from {start_freq} to {stop_freq}.")
    
        except Exception as e:
            raise RuntimeError(f"Failed to configure integration range: {e}")
    
      
    
    
    def reset_integration_range_to_meas(self, range_index: int):
        """
        Resets the integration range to default full measurement range (MEAS) for a given range index.
    
        Parameters
        ----------
        range_index : int
            The index of the integration range to reset (1–10).
      
        Manual Reference:
            - Pages 173–174: Defining the integration range
            - Page 490+: Command syntax
    
        Raises
        ------
        ValueError
            If the range index is not within 1–10.
        RuntimeError
            If the SCPI command fails.
        """
        try:
            if range_index not in range(1, 11):
                raise ValueError("Invalid range index. Must be between 1 and 10.")
    
            self.write_str(f"CALC1:RANG{range_index}:EVAL:STAT ON")
            print(f"Integration range {range_index} reset to full MEAS.")
    
        except Exception as e:
            raise RuntimeError(f"Failed to reset integration range: {e}")




# =============================================================================
# Spot Noise RAKIBUL ISLAM
# =============================================================================

    def disable_spot_noise(self):
        """
        Turns off all spot noise information, including custom/user-defined and 10x markers.
    
        Reference:
            - R&S FSWP User Manual, Page 496
    
        Notes:
            - Applies to all traces and modes (e.g., Spot Noise vs Tune).
            - Automatically blanks all trace displays in the Spot Noise view.
        """
        try:
            self.write_str("CALC:SNO:AOFF")
            print("All spot noise information turned OFF.")
        except Exception as e:
            raise RuntimeError(f"Failed to disable spot noise info: {e}")




    def set_decade_spot_noise(self, state: str, trace: int = 1, display: bool = True):
        """
        Enables or disables decade spot noise and assigns it to a trace.
    
        Parameters
        ----------
        state : str
            "ON" or "OFF" to enable or disable decade spot noise markers.
        trace : int, optional
            Trace number (1–6) to which the spot noise info is linked. Default is 1.
        display : bool, optional
            Whether to show spot noise markers in the diagram. Default is True.
    

    
        Reference:
            - Manual pages 496–499 (spot noise)
            - Manual page 175 (display)
        """
        try:
            state = state.strip().upper()
            if state not in ["ON", "OFF"]:
                raise ValueError("State must be 'ON' or 'OFF'.")
            if trace not in range(1, 7):
                raise ValueError("Trace must be between 1 and 6.")
    
            self.write_str(f"CALC:SNO:DEC {state}")
            self.write_str(f"DISP:SNIN {'ON' if display else 'OFF'}")
            self.write_str(f"DISP:SNIN:TRAC {trace}")
    
            print(f"Decade spot noise set to {state}, display={'ON' if display else 'OFF'}, trace={trace}")
    
        except Exception as e:
            raise RuntimeError(f"Decade spot noise configuration failed: {e}")


    def set_manual_spot_noise(self, marker: int, offset: str, enable: bool = True, display: bool = True, trace: int = 1):
        """
        Enables or disables a custom (manual) spot noise marker and sets its frequency offset.
    
        Parameters
        ----------
        marker : int
            Spot noise marker index (1–6).
        offset : str
            Frequency offset with unit (e.g., "100kHz", "1MHz").
        enable : bool, optional
            True to enable the marker, False to disable it. Default is True.
        display : bool, optional
            Whether to display the spot noise info on the diagram. Default is True.
        trace : int, optional
            Trace number (1–6) to which the spot noise info is linked. Default is 1.
    
    
        Reference:
            - Manual pages 496–499 (spot noise)
            - Manual page 175 (display)
        """
        try:
            if marker not in range(1, 7):
                raise ValueError("Marker index must be between 1 and 6.")
            if trace not in range(1, 7):
                raise ValueError("Trace number must be between 1 and 6.")
    
            self.write_str("CALC:SNO:USER ON")
            if enable:
                self.write_str(f"CALC:SNO{marker}:STAT ON")
                self.write_str(f"CALC:SNO{marker}:X {offset}")
                print(f"Spot noise marker {marker} enabled at {offset}.")
            else:
                self.write_str(f"CALC:SNO{marker}:STAT OFF")
                print(f"Spot noise marker {marker} disabled.")
    
            self.write_str(f"DISP:SNIN {'ON' if display else 'OFF'}")
            self.write_str(f"DISP:SNIN:TRAC {trace}")
            print(f"Spot noise display: {'ON' if display else 'OFF'}, linked to trace {trace}.")
    
        except Exception as e:
            raise RuntimeError(f"Manual spot noise configuration failed: {e}")


# =============================================================================
#   Spurious       
# =============================================================================

    
    def enable_spur_removal(self, window: int = 1, trace: int = 1, state: int | str = 1) -> None:
        """
        Enables or disables spur removal for a specific trace.
    
        Parameters
        ----------
        window : int
            Window number (1–16).
        trace : int
            Trace number (1–6).
        state : int | str
            ON | OFF | 1 | 0
    
        Reference: Page 500, FSWP User Manual v16
        """
        state = state.upper() if isinstance(state, str) else int(state)
        if state in ['ON', 1]:
            value = 'ON'
        elif state in ['OFF', 0]:
            value = 'OFF'
        else:
            raise ValueError("Invalid state: use ON/OFF or 1/0")
    
        self.write_str(f"DISP:WIND{window}:TRAC{trace}:SPUR:SUPP {value}")
        print(f"Spur removal for TRACE{trace} in WINDOW{window} set to {value}.")
         
    
    def set_spur_threshold(self, window: int = 1, trace: int = 1, threshold_dB: float = 10.0) -> None:
        """
        Sets the detection threshold for spur removal in dB.
    
        Parameters
        ----------
        window : int
            Window number (1–16).
        trace : int
            Trace number (1–6).
        threshold_dB : float
            Threshold in dB.
    
        Reference: Page 500, FSWP User Manual v16
        """
        self.write_float(f"DISP:WIND{window}:TRAC{trace}:SPUR:THR", threshold_dB)
        print(f"Spur threshold for TRACE{trace} in WINDOW{window} set to {threshold_dB} dB.")

    
    
    def set_spur_sort_order(self, order: str = 'POWer') -> None:
        """
        Sets the sorting order of the spurs.
    
        Parameters
        ----------
        order : str
            "POWer" or "OFFSet"
    
        Reference: Page 501, FSWP User Manual v16
        """
        order = order.upper()
        if order not in ['POWER', 'OFFSET']:
            raise ValueError("Invalid sort order: use 'POWer' or 'OFFSet'")
        self.write_str(f"SPUR:SORT {order}")
        print(f"Spur sort order set to {order}.")

    

    def set_spur_filter_mode(self, mode: str = 'OFF') -> None:
        """
        Sets the spurious filter mode.
    
        Parameters
        ----------
        mode : str
            OFF | SUPPress | SHOW
    
            OFF     → No spurious filter is applied.
            SUPPress → Spurs in the filter are removed from list and diagram.
            SHOW    → Only filtered spurs are shown in list and diagram.
    
        Reference: Page 177, FSWP User Manual v16
        """
        self.write_str("INST:SEL 'PNOISE'")  # Ensure correct app context
        mode = mode.upper()
        if mode not in ['OFF', 'SUPPRESS', 'SHOW']:
            raise ValueError("Invalid mode: use 'OFF', 'SUPPress', or 'SHOW'")
        self.write_str(f"SENS:SPUR:FILT:MODE {mode}")
        print(f"Spurious filter mode set to {mode}.")
  
    
  
    def ask_spur_filter_mode(self) -> str:
        """
        Queries the current spur filter mode.
    
        Returns
        -------
        str
            Current mode: OFF | SUPPress | SHOW
    
        Reference: Page 502, FSWP User Manual v16
        """
        # Ensure Phase Noise app is selected
        self.write_str("INST:SEL 'PNOISE'")
        
        # Then query
        mode = self.query_str("SENS:SPUR:FILT:MOD?")
        print(f"Current spur filter mode: {mode}")
        return mode


    
    def set_spur_filter_harmonics(self, state: str | int = 'OFF') -> None:
        """
        Sets whether harmonics are included in the spurious filter.
    
        Parameters
        ----------
        state : str | int
            ON | OFF | 1 | 0
    
        Reference: Page 502, FSWP User Manual v16
        """
        state = state.upper() if isinstance(state, str) else int(state)
        if state in ['ON', 1]:
            value = 'ON'
        elif state in ['OFF', 0]:
            value = 'OFF'
        else:
            raise ValueError("Invalid state: use ON/OFF or 1/0")
        self.write_str(f"SENS:SPUR:FILT:HARM {value}")
        print(f"Spur filter harmonics set to {value}.")

    

    
    
    def get_spur_filter_harmonics(self) -> str:
        """
        Queries whether harmonics are included in the spurious filter.
    
        Returns
        -------
        str
            'ON' or 'OFF'
    
        Reference: Page 502, FSWP User Manual v16
        """
        raw = self.query_str("SENS:SPUR:FILT:HARM?")
        state = 'ON' if raw.strip() in ['1', 'ON'] else 'OFF'
        print(f"Harmonics in spurious filter: {state}")
        return state




    def get_spur_filter_name(self) -> str:
        """
        Queries the name of the currently selected spurious filter.
    
        Returns
        -------
        str
            Name of the spurious filter (e.g., 'DefaultFilter1')
    
        Reference: Page 502, FSWP User Manual v16
        """
        name = self.query_str("SENS:SPUR:FILT:NAME?")
        print(f"Current spurious filter name: {name}")
        return name


# =============================================================================
# Trace 
# =============================================================================



    def set_trace_mode(self, window: int = 1, trace: int = 1, mode: str = "WRIT") -> None:
        """
        Sets the trace display mode.
    
        Valid modes (abbreviated): WRIT, MAXH, MINH, AVER, VIEW, BLAN, WHOL
    
       
        """
        valid_modes = ['WRIT', 'MAXH', 'MINH', 'AVER', 'VIEW', 'BLAN', 'WHOL']
        mode = mode.upper()
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Valid options: {valid_modes}")
        self.write_str(f"DISP:WIND{window}:TRAC{trace}:MODE {mode}")

        print(f"Set TRACE{trace} mode to {mode} in WINDOW{window}.")



    def set_trace_smoothing(self, window: int = 1, trace: int = 1, state: str | int = "ON") -> None:
        """
        Enables or disables smoothing for a trace.
    
        SCPI Reference: DISP:WIND<n>:TRAC<t>:SMO:STAT
        """
        state = str(state).upper()
        if state not in ["ON", "OFF", "1", "0"]:
            raise ValueError("State must be ON, OFF, 1, or 0")
        self.write_str(f"DISP:WIND{window}:TRAC{trace}:SMO:STAT {state}")
        print(f"Smoothing set to {state} for TRACE{trace} in WINDOW{window}.")
 
  
 
    def set_spur_hide(self, window: int = 1, trace: int = 1, state: str | int = "ON") -> None:
        """
        Enables or disables hiding of spurs in display
    
        SCPI Reference: DISP:WIND<n>:TRAC<t>:SPUR:SUPP
        """
        state = str(state).upper()
        value = "ON" if state in ["ON", "1"] else "OFF"
        self.write_str(f"DISP:WIND{window}:TRAC{trace}:SPUR:SUPP {value}")
        print(f"Spur hiding set to {value} for TRACE{trace} in WINDOW{window}.")

    
    
 ##############################
 # Cannot be tested becouse of no data at the moment
 ##############################  
    def copy_trace_virtual(self, source_trace: int = 1, target_trace: int = 2, window: int = 1) -> tuple[np.ndarray, np.ndarray]:
        """
        Copies trace data from source to target (in software), only valid under PNOISE application.
    
        Returns
        -------
        Tuple of X and Y numpy arrays.
        """
        self.write_str("INST:SEL 'PNOISE'")  # Ensure correct context
    
        trace_str = f"TRACe{source_trace}"
    
        try:
            x = self.query_float_list(f"TRACe{window}:DATA:X? {trace_str}")
            y = self.query_float_list(f"TRACe{window}:DATA:Y? {trace_str}")
    
            if x is None or y is None or len(x) != len(y):
                raise RuntimeError("Failed to retrieve or match trace data lengths.")
    
            print(f"Copied data from TRACE{source_trace} to virtual TRACE{target_trace} (software copy).")
            return np.array(x), np.array(y)
    
        except Exception as e:
            raise RuntimeError(f"Error copying trace data: {e}")
    


# =============================================================================
# Extract Trace and save it to CSV
# =============================================================================


 ##############################
 # Cannot be tested becouse of no data at the moment
 ############################## 

    def extract_trace_data(
        self,
        trace: int = 1,
        window: int = 1,
        points: bool = False,
        num_of_points: int = None,
        export: bool = False,
        filename: str = "trace_export.csv"
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Extracts X (offset frequency) and Y (phase noise or amplitude) trace data,
        with optional downsampling and export to CSV.
    
        Parameters
        ----------
        trace : int
            Trace number (1–6)
        window : int
            Window number (1–16)
        points : bool
            Whether to limit number of points in output (downsample)
        num_of_points : int, optional
            Desired number of output points if points=True
        export : bool
            If True, saves the data to a CSV file
        filename : str
            Output CSV file name (used if export=True)
    
        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Tuple of (X data in Hz, Y data in dBc/Hz)
    
        Raises
        ------
        ValueError
            If points=True and num_of_points is not provided.
        RuntimeError
            If data is missing or X and Y lengths mismatch.
    
        Reference
        ---------
        - TRACe<n>[:DATA]:X? TRACE<t>
        - TRACe<n>[:DATA]:Y? TRACE<t>
        - TRACe<n>:POINts? TRACE<t>  (query only)
        """
        import csv
    
        trace_str = f"TRACE{trace}"
    
        # Query full trace data
        x_data = self.query_float_list(f"TRAC{window}:DATA:X? {trace_str}")
        y_data = self.query_float_list(f"TRAC{window}:DATA:Y? {trace_str}")
    
        if x_data is None or y_data is None:
            raise RuntimeError("Failed to retrieve trace data from instrument.")
        if len(x_data) != len(y_data):
            raise RuntimeError("Mismatch between X and Y data lengths.")
    
        x_array = np.array(x_data)
        y_array = np.array(y_data)
    
        if points:
            if num_of_points is None:
                raise ValueError("When points=True, 'num_of_points' must be specified.")
            if num_of_points >= len(x_array):
                print("Requested points exceed or match total points — returning full trace.")
            else:
                # Downsample using linear spacing of indices
                indices = np.linspace(0, len(x_array) - 1, num=num_of_points, dtype=int)
                x_array = x_array[indices]
                y_array = y_array[indices]
    
        print(f"Extracted {len(x_array)} points from WINDOW{window}, TRACE{trace}.")
    
        if export:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Offset Frequency (Hz)", "Amplitude / Phase Noise (dBc/Hz)"])
                writer.writerows(zip(x_array, y_array))
            print(f"Trace data exported to '{filename}'.")
    
        return x_array, y_array
