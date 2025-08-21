#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:11:32 2021

@author: Martin.Mihaylov
"""

import pyvisa as visa
import numpy as np
import re
import logging
from time import time, sleep


class MS2760A:
    """
    This function is using pyvisa to connect to Instruments. Please install PyVisa before using it.
    """

    def __init__(self, resource_str: str = "127.0.0.1", port: int = 59001) -> None:

        self._resource = visa.ResourceManager().open_resource(
            f"TCPIP0::{resource_str}::{port}::SOCKET",
            read_termination="\n",
            query_delay=0.5,
        )
        # self._resource = visa.ResourceManager().open_resource(str(resource_str), read_termination='\n', query_delay=0.5)
        print(self._resource.query("*IDN?"))

        # Internal Variables
        self._freq_Units_List = ["HZ", "KHZ", "MHZ", "GHZ"]
        self._state_List = ["OFF", "ON", 1, 0]
        self._trace_List = [1, 2, 3, 4, 5, 6]
        self._marker_List = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self._exeption_state = 0  # indicates that an exception occured
        self._dataFormat = None
        self.set_DataFormat("ASCii")

    def query(self, message):
        return self._resource.query(message)

    def query_ascii_values(self, message, **kwargs):
        return self._resource.query_ascii_values(message, **kwargs)

    def write(self, message):
        return self._resource.write(message)

    def read(self):
        return self._resource.read()

    def Close(self):
        self._resource.close()

    # =============================================================================
    # General functions
    # =============================================================================
    def Idn(self) -> str:
        """
        Identify the Insturment.

        Returns
        -------
        str
            A string with the Instrument name.
        """
        return self.query("*IDN?")

    def reset(self) -> None:
        """
        Resets the instrument.

        """
        self.write("*RST")

    def clear(self) -> None:
        """
        Clears input and output buffers

        """
        self._resource.clear()

    def OPC(self, delay: float = 5.0) -> int:
        """
        Places a 1 into the output queue when all device operations have been completed.

        Parameters
        ----------
        delay : float, optional
            DESCRIPTION. The default is 5s delay between write and read.

        Returns
        -------
        int
            1 if device operation is completed.
            0 if device operation is not completed.
        """
        if self._exeption_state >= 1:
            self.clear()
        try:
            state = self.query_ascii_values("*OPC?", converter="d", delay=delay)[0]
        except:
            self._exeption_state = 1
            logging.warning(
                """An Execption occured in the OPC function. Setting 
                            exeption state to 1."""
            )
            return 0
        return state

    def StatusOperation(self) -> int:
        """
        Returns the operation status of the instrument

        Returns
        -------
        int
            256 if device operation is completed.
            0 if device operation is not completed.
        """
        return self.query_ascii_values(":STATus:OPERation?", converter="d")[0]

    def abort(self):
        """
        Description: Resets the trigger system. This has the effect of aborting the sweep or any measurement
        that is currently in progress.
        Additionally, any pending operation flags that were set by initiation of the trigger system
        will be set to false.
        If :INITiate:CONTinuous is OFF (i.e. the instrument is in single sweep mode), send the
        command :INITiate[:IMMediate] to trigger the next sweep.
        If :INITiate:CONTinuous is ON (i.e. the instrument is in continuous sweep mode) a new
        sweep will start immediately
        """
        self.write(":ABORt")

    # =============================================================================
    # Start Measurment
    # =============================================================================

    def Init(self) -> None:
        """Initialize measurement."""
        self.write(":INITiate:IMMediate")

    def ClearTrace(self, traceNumber: int = 1) -> None:
        """
        Clear the trace.

        Parameters
        ----------
        traceNumber : int, optional
            DESCRIPTION. The default is 1.
        """

        if traceNumber in self._trace_List:
            self.write(f":TRACe:CLEar {traceNumber}")
        else:
            raise ValueError(f"Invalid trace number. Valid arguments are {self._trace_List}")

    # =============================================================================
    # Ask/Query Functions
    # =============================================================================

    def ask_freq_Start(self) -> float:
        """
        Query for the start frequency.

        Returns
        -------
        float
            Start Frequency in Hz.

        """

        return self.query_ascii_values(":SENSe:FREQuency:STARt?")[0]

    def ask_freq_Stop(self) -> float:
        """
        Query for the stop frequency.

        Returns
        -------
        str
            Stop Frequency in Hz.

        """

        return self.query_ascii_values(":SENSe:FREQuency:STOP?")[0]

    def ask_ResBwidth(self) -> float:
        """
        Query the resolution bandwidth.

        Returns
        -------
        float
            Resolution Bandwidth in Hz

        """

        return self.query_ascii_values(":SENSe:BANDwidth:RESolution?")[0]

    def ask_SingleOrContinuesMeas(self) -> int:
        """
        Query whether the instrument is in continuous or single sweep mode.

        Returns
        -------
        int
            1 if the instrument is in continuously sweeping/measuring.
            0 if the instrument is in single sweep/measurement mode.

        """

        return self.query_ascii_values(":INITiate:CONTinuous?", converter="d")[0]

    def ask_Configuration(self) -> str:
        """
        Query the instrument configuration information.

        Returns
        -------
        str
            Description: This command returns a quoted string of characters readable only by Anritsu Customer
            Service. Only instrument configuration information is returned. No setup information is
            included.

        """

        return self.query(":SYSTem:OPTions:CONFig?")

    def ask_sweepTime(self) -> float:
        """
        Query the measured sweep time (in milliseconds).

        Returns
        -------
        float
            measured sweep time in milliseconds.
            "nan" if no measured sweep time is available.

        """

        return self.query_ascii_values(":DIAGnostic:SWEep:TIME?")[0]

    # def ask_TraceData(self, traceNumber):
    #     '''
    #     !!!!!DONT USE IT!!!!!

    #     Parameters
    #     ----------
    #     traceNumber : int
    #         Description: This command transfers trace data from the instrument to the controller. Data are
    #         transferred from the instrument as an IEEE definite length arbitrary block response,
    #         which has the form <header><block>.

    #     Returns
    #     -------
    #     str
    #        Trace Data

    #     '''

    #     traceNumber = str(traceNumber)
    #     return self.query(':TRACe:DATA? ' + traceNumber)

    def ask_ResBwidthAuto(self) -> int:
        """
        Query the automatic resolution bandwidth setting.

        Returns
        -------
        int
            1 if in automatic mode ("ON")
            0 if not in automatic mode ("OFF")

        """

        return self.query_ascii_values(":SENSe:BANDwidth:RESolution:AUTO?", converter="d")[0]

    def ask_DataPointCount(self) -> int:
        """
        Query the display point count.

        Returns
        -------
        int
            Query the data point count.

        """

        return self.query_ascii_values(":DISPlay:POINtcount?", converter="d")[0]

    def ask_MarkerExcursionState(self) -> int:
        """
        Query the peak marker excursion state.

        Returns
        -------
        int
            Excursion on/off

        """

        return self.query_ascii_values(":CALCulate:MARKer:PEAK:EXCursion:STATe?", converter="d")[0]

    def ask_MarkerExcursion(self) -> str:
        """
        Query the marker excursion data.

        Returns
        -------
        str
            Query the excursion for a marker. The excursion is the vertical distance from the peak to
            the next highest valley which must be exceeded for a peak to be considered a peak in
            marker max commands

        """

        return self.query(":CALCulate:MARKer:EXCursion?")

    def ask_MarkerValues(self, markerNumber: int = None) -> list | tuple:
        """
        Query the marker values.

        Parameters
        ----------
        markerNumber : int, optional
            Marker Number between 1 - 12. The default is None.

        Returns
        -------
        list
            List of tuples with all marker values.
            Tuple with the specified marker value

        """

        s = self.query(":CALCulate:MARKer:DATA:ALL?")

        # Find all occurrences of a group inside parentheses
        pairs = re.findall(r"\(([^)]+)\)", s)

        # Convert each pair into a tuple of floats
        result = []
        for pair in pairs:
            a_str, b_str = pair.split(",")
            result.append((float(a_str), float(b_str)))

        if markerNumber is not None:
            if markerNumber in self._marker_List:
                return result[markerNumber - 1]
            else:
                logging.warning(
                    """Marker number is not one of the 12 markers. Returning all
                                marker values."""
                )
                return result
        else:
            return result

    def ask_CHPowerState(self) -> int:
        """
        Query the channel power measurement state.

        Returns
        -------
        str
            1 if State is ON.
            0 if State is OFF

        """

        return self.query_ascii_values(":SENSe:CHPower:STATe?", converter="d")[0]

    def ask_DataFormat(self) -> str:
        """
        Query the data format.

        Returns
        -------
        str
            A string indicating the data format.

        """
        self._dataFormat = self.query(":FORMat:TRACe:DATA?")
        return self._dataFormat

    def ask_CenterFreq(self) -> float:
        """
        Query the center frequency.

        Returns
        -------
        float
            Center Frequency in Hz
        """

        return self.query_ascii_values(":SENSe:FREQuency:CENTer?")[0]

    def ask_FreqSpan(self) -> float:
        """
        Query the frequency span.

        Returns
        -------
        float
            Frequency Span in Hz
        """
        return self.query_ascii_values(":SENSe:FREQuency:SPAN?")[0]

    def ask_TraceType(self, traceNumber: int = 1) -> str:
        """
        Query the trace type for a given trace number.

        Parameters
        ----------
        traceNumber : int
            Trace number (1 to 6).

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        str
            Trace Type: NORM|MIN|MAX|AVER|RMAX|RMIN|RAV

        """

        if traceNumber in self._trace_List:
            return self.query(":TRACe" + str(traceNumber) + ":TYPE?")
        else:
            raise ValueError("Number must be between 1 and 6")

    def ask_TraceSelected(self) -> int:
        """
        Query the currently selected trace. The max number of
        traces available to select is model specific.

        Returns
        -------
        str
            Returns selected trace.

        """

        return self.query_ascii_values(":TRACe:SELect?", converter="d")[0]

    def ask_TraceState(self, traceNumber: int = 1) -> int:
        """
        Query the display state of a given trace. If it is OFF, the :TRAC:DATA?
        command will return nan.

        Parameters
        ----------
        traceNumber : int
            Trace number (1 to 6).

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        int
            1 if State is ON.
            0 if State is OFF.

        """

        if traceNumber in self._trace_List:
            return self.query_ascii_values(f":TRACe{traceNumber}:DISPlay:STATe?", converter="d")[0]
        else:
            raise ValueError("Number must be between 1 and 6")

    def ask_RefLevel(self) -> float:
        """
        Query the reference level.

        Returns
        -------
        float
            Reference Level in dBm

        """
        return self.query_ascii_values(":DISPlay:TRACe:Y:SCALe:RLEVel?")[0]

    def ask_IFGainState(self) -> int:
        """
        Query the IF gain state.

        Returns
        -------
        int
            1 if State is ON.
            0 if State is OFF.

        """
        return self.query_ascii_values(":POWer:IF:GAIN:STATe?", converter="d")[0]

    def ask_DetectorType(self, traceNumber: int = 1) -> str:
        """
        Query the detector type.

        Parameters
        ----------
        traceNumber : int
            Trace number (1 to 6).

        Returns
        -------
        str
            Detector Type: POS|RMS|NEG

        """
        if traceNumber in self._trace_List:
            return self.query(":TRACe" + str(traceNumber) + ":DETector?")
        else:
            raise ValueError("Trace Number must be between 1 and 6")

    def ask_CaptureTime(self) -> float:
        """
        Query the capture time in ms.

        Returns
        -------
        float
            Capture Timte in ms. Range 0 ms to 10000 ms.
        """
        return self.query_ascii_values(f":CAPTure:TIMe?")[0]

    # =============================================================================
    #  Write Functions
    # =============================================================================

    def set_DataPointCount(self, dataPoints: int = 501) -> None:
        """
        Changes the number of display points the instrument currently measures.
        Increasing the number of display points can improve the resolution of
        measurements but will also increase sweep time.

        Parameters
        ----------
        dataPoints : int
               Default Value: 501
               Range: 10 to 10001

        Raises
        ------
        ValueError
            Error message

        """
        if isinstance(dataPoints, int):
            if 10 <= dataPoints <= 10001:
                self.write(f":DISPlay:POINtcount {dataPoints}")
            else:
                raise ValueError(f"Value must be between 10 and 10001, not {dataPoints}")
        else:
            raise ValueError("Unknown input! Value must be an integer.")

    def set_freq_Start(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the start frequency. Note that in the spectrum analyzer, changing the
        value of the start frequency will change the value of the coupled parameters,
        Center Frequency and Span.

        Parameters
        ----------
        value : int/float
            Sets the start frequency.

        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}

        Raises
        ------
        ValueError
            Error message

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:STARt {value} {unit}")
        else:
            raise ValueError("Unknown unit! Should be HZ, KHZ, MHZ or GHZ")

    def set_freq_Stop(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the stop frequency. Note that in the spectrum analyzer, changing the
        value of the start frequency will change the value of the coupled parameters,
        Center Frequency and Span.

        Parameters
        ----------
        value : int/float
                Sets the stop frequency.

        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}

        Raises
        ------
        ValueError
            Error message

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:STOP {value} {unit}")
        else:
            raise ValueError("Unknown unit! Should be HZ, KHZ, MHZ or GHZ")

    def set_ResBwidth(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the resolution bandwidth. Note that using this command turns
        the automatic resolution bandwidth setting OFF.
        In Zero Span, the range will change to allow a minimum of 5 KHz to
        the maximum of 20 MHz.

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

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:BANDwidth:RESolution {value} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_ResBwidthAuto(self, state: str | int) -> None:
        """
        Sets the automatic resolution bandwidth state. Setting the value to ON or 1 will
        result in the resolution bandwidth being coupled to the span. That is, when the
        span changes, the resolution bandwidth changes. Setting the value to OFF or 0 will
        result in the resolution bandwidth being decoupled from the span. That is, changing
        the span will not change the resolution bandwidth. When this command is issued,
        the resolution bandwidth setting itself will not change.

        Parameters
        ----------
        state : int/str
            Sets the state of the coupling of the resolution bandwidth to the frequency span.
            Parameters:<1 | 0 | ON | OFF>
            Default Value: ON

        Raises
        ------
        ValueError
             Error message

        """

        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write(f":SENSe:BANDwidth:RESolution:AUTO {state}")
        else:
            raise ValueError(f"Unknown input! Must be ON, OFF, 1 or 0 instead of {state}")

    def set_CenterFreq(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the center frequency. Note that changing the value of the center frequency will
        change the value of the coupled parameters Start Frequency and Stop Frequency. It
        might also change the value of the span.

        Parameters
        ----------
        value : float
            Sets the center frequency.

        unit : str
            Unit value. Can be ['HZ','KHZ','MHZ','GHZ']

        Raises
        ------
        ValueError
            Error message

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:CENTer {value} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_FreqSpan(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the frequency span. Setting the value of <freq> to 0 Hz is the
        equivalent of setting the span mode to zero span. Note that changing
        the value of the frequency span will change the value of the coupled
        parameters Start Frequency and Stop Frequency and might change the
        Center Frequency.

        Parameters
        ----------
        value : float
            Sets the frequency span.

        unit : str
            Unit value. Can be ['HZ','KHZ','MHZ','GHZ']

        Raises
        ------
        ValueError
            Error message

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:SPAN {value} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_Continuous(self, state: str | int) -> None:
        """
        Specifies whether the sweep/measurement is triggered continuously. If
        the value is set to ON or 1, another sweep/measurement is triggered as
        soon as the current one completes. If continuous is set to OFF or 0,
        the instrument remains initiated until the current sweep/measurement
        completes, then enters the 'idle' state and waits for the
        :INITiate[:IMMediate] command or for :INITiate:CONTinuous ON.

        Parameters
        ----------
        state : str/int
             Sets the continuous measurement state. <1 | 0 | ON | OFF>

        Raises
        ------
        ValueError
             Error message

        """

        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write(f":INITiate:CONTinuous {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # Define an alias
    set_ContinuousMeas = set_Continuous

    def set_DataFormat(self, state: str = "ASCii") -> None:
        """
        Sets the data format. Only ASCii works!!!

        Parameters
        ----------
        state : str
            Set Data Format =  ['ASCii','INTeger','REAL']

        Raises
        ------
        ValueError
            Error message

        """

        format_List = ["ASCII", "INTEGER", "REAL"]
        state = state.upper() if isinstance(state, str) else state
        if state in format_List:
            self.write(f":FORMat:TRACe:DATA {state}")
            self.ask_DataFormat()
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_MarkerExcursionState(self, state: str | int) -> None:
        """
        Turn on/off marker excursion state.

        Parameters
        ----------
        state : str/int
            Can be state = ['ON','OFF',1,0]

        Raises
        ------
        ValueError
            Error message

        """
        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write(f":CALCulate:MARKer:PEAK:EXCursion:STATe {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_MarkerExcursion(self, value: int | float) -> None:
        """
        Sets the excursion for a marker. The excursion is the vertical distance
        from the peak to the next highest valley which must be exceeded for a
        peak to be considered a peak in marker max commands.

        Parameters
        ----------
        value : int/float
            Sets the excursion for a marker in dB. Range 0dB to 200 dB.

        """
        if 0 <= value <= 200:
            self.write(f":CALCulate:MARKer:PEAK:EXCursion {value} DB")
        else:
            raise ValueError(f"Allowed range is 0dB to 200dB. Current value is {value}dB")

    def set_NextPeak(self, markerNum: int = 1) -> None:
        """
        Moves the marker to the next highest peak.

        Parameters
        ----------
        markerNum : int
            Marker number. Can be 1 to 12.

        Raises
        ------
        ValueError

        """
        if isinstance(markerNum, int) and markerNum in self._marker_List:
            self.write(f":CALCulate:MARKer{markerNum}:MAXimum:NEXT")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_MaxPeak(self, markerNum: int = 1) -> None:
        """
        Moves the marker to the highest peak.

        Parameters
        ----------
        markerNum : int
            Marker number. Can be 1 to 12.

        Raises
        ------
        ValueError

        """

        if isinstance(markerNum, int) and markerNum in self._marker_List:
            self.write(f":CALCulate:MARKer{markerNum}:MAXimum")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_MarkerPreset(self) -> None:
        """Presets all markers to their preset values."""
        self.write(":CALCulate:MARKer:APReset")

    def set_CHPowerState(self, state: str | int) -> None:
        """
        Sets the channel power measurement state.
        Sets the state of the channel power measurement, ON or OFF. When using
            :CONFigure:CHPower,the state is automatically set to ON

        Parameters
        ----------
        state :str
            state = ['ON','OFF',1,0]

        Raises
        ------
        ValueError
            Error message

        """

        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write(f":SENSe:CHPower:STATe {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_TraceType(self, state: str = "NORM", traceNumber: int = 1) -> None:
        """
        Sets the trace type.

        Parameters
        ----------
        state : str
             Sets Trace Type:
                            Normal - NORM
                            Hold the Minimum - MIN
                            Hold the Maximum - MAX
                            Average - AVER
                            Rolling Max Hold - RMAX
                            Rolling Min Hold - RMIN
                            Rolling Average - RAV
        number : int
            Trace number:
                        Can be set to [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        """

        stList = ["NORM", "MIN", "MAX", "AVER", "RMAX", "RMIN", "RAV"]
        state = state.upper() if isinstance(state, str) else state
        if state in stList and traceNumber in self._trace_List:
            self.write(f":TRACe{traceNumber}:TYPE {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_TraceSelected(self, traceNumber: int = 1) -> None:
        """
        The selected trace will be used by operations that use a single trace.
        The max number of traces available to select is model specific.

        Parameters
        ----------
        traceNumber : int
            Trace number:
                        Can be set to [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        """

        if traceNumber in self._trace_List:
            self.write(f":TRACe:SELect {traceNumber}")
        else:
            raise ValueError(f"Allowed range is 1 to 6. Current value is {traceNumber}")

    def set_TraceState(self, state: str | int = "ON", traceNumber: int = 1) -> None:
        """
        The trace visibility state status. If it is OFF, the :TRAC:DATA?
        command will return NaN.

        Parameters
        ----------
        state : str
            ['ON','OFF',0,1]
        traceNumber : int
            Trace Number:
                Can be set to  [1,2,3,4,5,6]

        Raises
        ------
        ValueError
             Error message

        """

        state = state.upper() if isinstance(state, str) else state
        if traceNumber in self._trace_List and state in self._state_List:
            self.write(f":TRACe{traceNumber}:DISPlay:STATe {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_RefLevel(self, level: float) -> None:
        """
        Set the reference level in dBm.

        Parameters
        ----------
        level : float
            Reference level in dBm.

        Raises
        ------
        ValueError
            Error message

        """
        if -150 <= level <= 30:
            self.write(f":DISPlay:TRACe:Y:SCALe:RLEVel {level} dBm")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_IFGainState(self, state: str | int) -> None:
        """
        Sets the state of the IF gain ON or OFF. ON is only possible
        when reference level is set to <-10 dBm.

        Parameters
        ----------
        state :str/int
            state = ['ON','OFF',1,0]

        Raises
        ------
        ValueError
            Error message

        """

        state = state.upper() if isinstance(state, str) else int(state)
        if state in self._state_List:
            self.write(f":POWer:IF:GAIN:STATe {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_DetectorType(
        self,
        state: str = "POSitive",
        traceNumber: int = 1,
    ) -> None:
        """
        Sets the detector type.

        Parameters
        ----------
        state : str
            state = ['POSitive', 'RMS', 'NEGative']
        traceNumber : int
            Trace Number:
                Can be set to  [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        """

        stList = ["POSITIVE", "POS", "RMS", "NEGATIVE", "NEG"]
        state = state.upper() if isinstance(state, str) else state
        if traceNumber in self._trace_List and state in stList:
            self.write(f":TRACe{traceNumber}:DETector {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_CaptureTime(self, captureTime: float = 0, unit: str = "ms") -> None:
        """
        Determines how much time to spend taking samples for each portion of the spectrum.

        Parameters
        ----------
        captureTime : float, optional
            default: 0 ms, Range: 0 ms to 10000 ms
        unit : str, optional
            default: 'ms'

        Raises
        ------
        ValueError
            Error message

        """
        unit_List = ["PS", "NS", "US", "MS", "S", "MIN", "HR"]
        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in unit_List:
            self.write(f":CAPTure:TIMe {captureTime} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # =============================================================================
    #   get/Save Data
    # =============================================================================

    def get_Data(self, markerNumber: int = 1, returnArray: bool = False) -> dict | np.ndarray:
        """
        This function will stop temporally set Continuous Measurement to OFF, extract
        the max. peak value and frequency and restore the Continuous Measurement to ON.

        Returns
        -------
        OutPut : dict/np.ndarray
            Return a dictionary with the measured frequency in Hz and peak power in dBm.

        """

        self.set_Continuous("OFF")
        try:
            self.set_MarkerPreset()
            self.set_MaxPeak()
            marker_values = self.ask_MarkerValues(markerNumber)
            freq = marker_values[0]
            power = marker_values[1]
        finally:
            self.set_MarkerPreset()
            self.set_Continuous("ON")

        if returnArray:
            return np.array([freq, power])
        else:
            return {"Frequency/Hz": freq, "Power/dBm": power}

    def ExtractTtraceData(self, traceNumber: int = 1) -> np.ndarray:
        """
        Old function to keep legacy scripts working.
        Better use: ExtractTraceData()

        Parameters
        ----------
        traceNumber : int

        !!!!!USE IT AT YOUR OWN RISK is not an official function, but a workaround!!!!!

            Trace Number from which the data is taken:
                Can be set to  [1,2,3,4,5,6].
            1 - This Function will set the continues Measurement to 'OFF'.
            2 - Will set the Data Format to ASCii. This is needed since
            :TREACE:DATA? <num> is defect!!
            3 - Will write TRACE:DATA? <num>. Will return only 3 bits. The rest
            will be packed in the next command asked.
            4 - Will ask for the Data Format. This is dummy command that will
            have the data and the Data Format.
            5 - Make manupulations to separate the actual data from the rest and
            return the data in Output np.array() form.

        Returns
        -------
        Output : np.ndarray
            Measured Spectrum on Trace {num}.

        """

        self.set_Continuous("OFF")
        self.set_DataFormat("ASCii")
        data = self.write(f":TRACe:DATA? {traceNumber}")
        data = self.ask_DataFormat()
        num_header = int(data[1]) + 2  # get the header size
        new_str = data[num_header:-5]  # truncate the header block and end block
        data_arr = new_str.split(",")
        Output = [float(item) for item in data_arr]
        Output = np.array(Output)
        self.set_Continuous("ON")
        return Output

    def ExtractTraceData(
        self, traceNumber: int = 1, clearTrace: bool = True, timeout: float = 20
    ) -> np.ndarray:
        """
        Uses a workaround to read the trace data.
        Clears the Trace before taking the measurement and returns the data.
        Set Continuous Measurement to 'OFF'.

        Parameters
        ----------
        traceNumber : int
            Trace Number: Can be set to [1,2,3,4,5,6].
        clearTrace : bool, optional
            Clears the trace before taking the data measurement. The default is True.
        timeout : float, optional
            Defines the timeout for the operation. The default is 20s.

        Raises
        ------
        TimeoutError

        Returns
        -------
        Output : np.array

        """

        if traceNumber not in self._trace_List:
            raise ValueError(f"Invalid trace number: {traceNumber}. Must be in {self._trace_List}.")

        self.set_Continuous("OFF")

        # Check the data format
        if self._dataFormat != "ASC,8":
            self.set_DataFormat("ASCii")

        if clearTrace:
            self.abort()
            # self.ClearTrace(traceNumber)
            self.Init()
            start_time = time()
            complete = 0
            while complete == 0:
                sleep(0.1)
                complete = self.StatusOperation()
                if time() - start_time > timeout:
                    raise TimeoutError(f"Operation did not complete within {timeout:.2f} seconds.")

        data = self.write(f":TRACe:DATA? {traceNumber}")
        data = self.ask_DataFormat()
        num_header = int(data[1]) + 2  # get the header size
        new_str = data[num_header:-5]  # truncate the header block and end block
        data_arr = new_str.split(",")
        Output = np.array([float(item) for item in data_arr])

        return Output
