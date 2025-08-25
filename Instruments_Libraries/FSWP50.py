"""
Created on Wed Feb 26 20:21:23 2025

@author: Maxim Weizel
"""

try:
    from RsInstrument import *
except ImportError:
    raise ImportError("To use this Class you need to install 'RsInstrument': pip install RSInstrument")
import numpy as np
from time import time, sleep
import logging

class FSWP50:
    '''
    This class is using RsInstrument to connect. Please install RsInstrument before using it.
    '''
    def __init__(self, address: str) -> None:
        self._resource = RsInstrument(f"TCPIP::{address}::hislip0", id_query=True, reset=False)
        print(self._resource.query_str('*IDN?'))
        
        #Internal Variables
        self._freq_Units_List = ['HZ', 'KHZ', 'MHZ', 'GHZ']
        self._state_List = ['OFF', 'ON', 1 , 0]
        self._trace_List = [1, 2, 3, 4, 5, 6] # <t> in documentation
        self._window_List = [1, 2, 3, 4, 5, 6, 7, 8,
                             9, 10, 11, 12, 13, 14, 15, 16] # <n> in documentation
    
    def write_str(self, command: str) -> None:
        try:
            self._resource.write_str(command)
        except Exception as e:
            logging.error(e)

    def write_float(self, command: str, value: float) -> None:
        try:
            self._resource.write_float(command, value)
        except Exception as e:
            logging.error(e)

    def query_str(self, command: str) -> str:
        try:
            return self._resource.query_str(command)
        except Exception as e:
            logging.error(e)
    
    def query_str_list(self, command: str) -> list:
        try:
            return self._resource.query_str_list(command)    
        except Exception as e:
            logging.error(e)
    
    def query_float(self, command: str) -> float:
        try:
            return self._resource.query_float(command)
        except Exception as e:
            logging.error(e)
    
    def query_float_list(self, command: str) -> list:
        try:
            return self._resource.query_bin_or_ascii_float_list(command)
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
        self._resource.reset()

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
# Set Functions
# =============================================================================

    def list_channels(self) -> str:
        '''
        Queries all active channels. The query is useful to obtain the names of the existing
        channels, which are required to replace or delete the channels.
        '''
        return self.query_str_list("INSTrument:LIST?")


    def create_new_channel(self, ChannelType:str, ChannelName:str) -> None:
        '''
        Adds a measurement channel. You can configure up to 10 measurement channels at
        the same time (depending on available memory)

        Parameters
        ----------
        ChannelType : str
            One of: [PNOise, SMONitor, SANalyzer]
        ChannelName : str
            Set a meantingful name for the channel.
        
        Raises
        ------
        ValueError
            Error message
        '''
        chType_List = ['PNOISE', 'PNO', 'SMONITOR', 'SMON', 'SANALYZER', 'SAN']
        ChannelType = ChannelType.upper() if isinstance(ChannelType, str) else ChannelType
        if ChannelType in chType_List:
            self.write_str(f":INST:CRE:NEW {ChannelType}, '{ChannelName}'")
        else:
            raise ValueError('Invalid ChannelType Selected')


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
    set_freq_Start = set_start_frequency # alias


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
    set_freq_Stop = set_stop_frequency # alias

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
    set_ResBwidth = set_resolution_bandwidth # alias


    def set_reference_level(self, ref_level: float) -> None:
        '''
        This command defines the maximum level displayed on the y-axis.

        Parameters
        ----------
        ref_level : float
            Default unit: Depending on the selected diagram.
        '''
        self.write_float(":DISP:WIND:TRAC:Y:SCAL:RLEV", ref_level)
    set_RefLevel = set_reference_level # alias


    def set_reference_level_lower(self, ref_level: float = 0) -> None:
        '''
        This command defines the minimum level displayed on the y-axis.

        Parameters
        ----------
        ref_level : float, optional
            Default unit: Depending on the selected diagram.
        '''
        self.write_float(":DISP:WIND:TRAC:Y:SCAL:RLEV:LOW", ref_level)

        
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