"""
Created on Wed Dec  1 13:11:32 2021

@author: Martin.Mihaylov
"""

import logging
import re
from time import sleep, time

import numpy as np

from .BaseInstrument import BaseInstrument

class MS2760A(BaseInstrument):
    """
    Driver for Anritsu MS2760A Spectrum Analyzer using BaseInstrument.
    Handles the socket-specific read/write terminations.
    """

    def __init__(self, ip="127.0.0.1", port=59001, visa_library="@py") -> None:
        resource_str = f"TCPIP::{ip}::{port}::SOCKET"

        # Initialize using BaseInstrument
        super().__init__(resource_str, visa_library=visa_library)

        # Set socket-specific attributes manually
        try:
            self._resource.read_termination = "\n"
            self._resource.write_termination = "\n"
            self._resource.query_delay = 0.5
        except Exception as e:
            self.logger.warning(f"Failed to set VISA socket parameters: {e}")

        # Test connection
        try:
            idn = self._resource.query("*IDN?")
            self.logger.info(f"Connected to {idn}")
        except Exception as e:
            self.logger.error(f"Failed to query *IDN?: {e}")
            raise

        # Internal variables
        self._freq_Units_List = ["HZ", "KHZ", "MHZ", "GHZ"]
        self._trace_List = [1, 2, 3, 4, 5, 6]
        self._marker_List = list(range(1, 13))
        self._exeption_state = 0
        self._dataFormat = None

        self.set_data_format("ASCii")

    # =============================================================================
    # General functions
    # =============================================================================
    def clear(self) -> None:
        """
        Clears input and output buffers

        """
        # Overriding BaseInstrument.clear (which does *CLS)
        # because the original code used self._resource.clear() (VI_CLEAR).
        self._resource.clear()

    def get_opc_status(self, delay: float = 5.0) -> int:
        """
        Places a 1 into the output queue when all device operations have been completed.

        Parameters
        ----------
        delay : float, optional
            Delay between write and read in seconds. Default: 5.0.

        Returns
        -------
        int
            ``1`` if operation is completed, ``0`` otherwise.
        """
        if self._exeption_state >= 1:
            self.clear()
        try:
            state = self.query_ascii_values("*OPC?", converter="d", delay=delay)[0]
        except Exception:
            self._exeption_state = 1
            logging.warning(
                """An Execption occured in the OPC function. Setting 
                            exeption state to 1."""
            )
            return 0
        return state

    def get_operation_status(self) -> int:
        """
        Returns the operation status of the instrument.

        Returns
        -------
        int
            ``256`` if operation is completed, ``0`` otherwise.
        """
        return self.query_ascii_values(":STATus:OPERation?", converter="d")[0]

    def abort(self) -> None:
        """
        Resets the trigger system. This has the effect of aborting the sweep or
        any measurement that is currently in progress.
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

    def init(self) -> None:
        """Initialize measurement."""
        self.write(":INITiate:IMMediate")

    def clear_trace(self, trace_num: int = 1) -> None:
        """
        Clear the trace.

        Parameters
        ----------
        trace_num : int, optional
            Trace number to clear. Default: 1.
        """

        if trace_num in self._trace_List:
            self.write(f":TRACe:CLEar {trace_num}")
        else:
            raise ValueError(f"Invalid trace number. Valid arguments are {self._trace_List}")

    # =============================================================================
    # Ask/Query Functions
    # =============================================================================

    def get_start_frequency(self) -> float:
        """
        Query for the start frequency in Hz.
        """

        return self.query_ascii_values(":SENSe:FREQuency:STARt?")[0]

    def get_stop_frequency(self) -> float:
        """
        Query for the stop frequency in Hz.
        """

        return self.query_ascii_values(":SENSe:FREQuency:STOP?")[0]

    def get_resolution_bandwidth(self) -> float:
        """
        Query the resolution bandwidth in Hz.
        """

        return self.query_ascii_values(":SENSe:BANDwidth:RESolution?")[0]

    def get_continuous(self) -> int:
        """
        Query whether the instrument is in continuous or single sweep mode.

        Returns
        -------
        int
            ``1`` for continuous sweep, ``0`` for single sweep.
        """

        return self.query_ascii_values(":INITiate:CONTinuous?", converter="d")[0]

    def get_configuration(self) -> str:
        """
        Query the instrument configuration information.
        This command returns a quoted string of characters readable only by
        Anritsu Customer Service. Only instrument configuration information is returned.
        No setup information is included.
        """

        return self.query(":SYSTem:OPTions:CONFig?")

    def get_sweep_time(self) -> float:
        """
        Query the measured sweep time (in milliseconds).

        Returns
        -------
        float
            Measured sweep time in ms. Returns ``nan`` if not available.
        """

        return self.query_ascii_values(":DIAGnostic:SWEep:TIME?")[0]

    # def ask_TraceData(self, trace_num):
    #     '''
    #     !!!!!DONT USE IT!!!!!
    #
    #     Parameters
    #     ----------
    #     trace_num : int
    #         Description: This command transfers trace data from the instrument to the controller.
    #         Data are transferred from the instrument as an IEEE definite length arbitrary block
    #         response, which has the form <header><block>.
    #
    #     Returns
    #     -------
    #     str
    #        Trace Data
    #
    #     '''
    #
    #     trace_num = str(trace_num)
    #     return self.query(':TRACe:DATA? ' + trace_num)

    def get_resolution_bandwidth_auto(self) -> int:
        """
        Query the automatic resolution bandwidth setting.

        Returns
        -------
        int
            ``1`` if in automatic mode (ON), ``0`` if not (OFF).
        """

        return self.query_ascii_values(":SENSe:BANDwidth:RESolution:AUTO?", converter="d")[0]

    def get_sweep_points(self) -> int:
        """
        Query the display point count.
        """

        return self.query_ascii_values(":DISPlay:POINtcount?", converter="d")[0]

    def get_marker_excursion_state(self) -> int:
        """
        Query the peak marker excursion state. (1=on, 0=off).
        """

        return self.query_ascii_values(":CALCulate:MARKer:PEAK:EXCursion:STATe?", converter="d")[0]

    def get_marker_excursion(self) -> str:
        """
        Query the marker excursion data.
        The excursion is the vertical distance from the peak to the next highest valley which must
        be exceeded for a peak to be considered a peak in marker max commands.
        """

        return self.query(":CALCulate:MARKer:EXCursion?")

    def get_marker_values(self, marker_num: int | None = None) -> list | tuple:
        """
        Query the marker values.

        Parameters
        ----------
        marker_num : int, optional
            Marker number (1 to 12). If omitted, returns all markers. Default: None.
        """

        s = self.query(":CALCulate:MARKer:DATA:ALL?")

        # Find all occurrences of a group inside parentheses
        pairs = re.findall(r"\(([^)]+)\)", s)

        # Convert each pair into a tuple of floats
        result = []
        for pair in pairs:
            a_str, b_str = pair.split(",")
            result.append((float(a_str), float(b_str)))

        if marker_num is not None:
            if marker_num in self._marker_List:
                return result[marker_num - 1]
            else:
                logging.warning(
                    """Marker number is not one of the 12 markers. Returning all
                                marker values."""
                )
                return result
        else:
            return result

    def get_ch_power_state(self) -> int:
        """
        Query the channel power measurement state.

        Returns
        -------
        int
            ``1`` if State is ON, ``0`` if OFF.
        """

        return self.query_ascii_values(":SENSe:CHPower:STATe?", converter="d")[0]

    def get_data_format(self) -> str:
        """
        Returns a string indicating the data format.
        """
        self._dataFormat = self.query(":FORMat:TRACe:DATA?")
        return self._dataFormat

    def get_center_frequency(self) -> float:
        """
        Query the center frequency in Hz.
        """

        return self.query_ascii_values(":SENSe:FREQuency:CENTer?")[0]

    def get_span(self) -> float:
        """
        Query the frequency span in Hz.
        """
        return self.query_ascii_values(":SENSe:FREQuency:SPAN?")[0]

    def get_trace_mode(self, trace_number: int = 1, **kwargs) -> str:
        """
        Query the trace mode for a given trace number.

        Parameters
        ----------
        trace_number : int
            Trace number (1 to 6).

        Returns
        -------
        str
            Trace mode (e.g., NORM, MIN, MAX, AVER, RMAX, RMIN, RAV).
        """

        if trace_number in self._trace_List:
            return self.query(":TRACe" + str(trace_number) + ":TYPE?")
        else:
            raise ValueError("Number must be between 1 and 6")

    def get_trace_selected(self) -> int:
        """
        Returns the currently selected trace. The max number of
        traces available to select is model specific.
        """

        return self.query_ascii_values(":TRACe:SELect?", converter="d")[0]

    def get_trace_state(self, trace_number: int = 1) -> int:
        """
        Query the display state of a given trace. If it is OFF, the :TRAC:DATA?
        command will return nan.

        Parameters
        ----------
        trace_number : int
            Trace number (1 to 6).
        """

        if trace_number in self._trace_List:
            return self.query_ascii_values(f":TRACe{trace_number}:DISPlay:STATe?", converter="d")[0]
        else:
            raise ValueError("Number must be between 1 and 6")

    def get_reference_level(self) -> float:
        """
        Query the reference level in dBm.
        """
        return self.query_ascii_values(":DISPlay:TRACe:Y:SCALe:RLEVel?")[0]

    def get_if_gain_state(self) -> int:
        """
        Query the IF gain state (1=on, 0=off).
        """
        return self.query_ascii_values(":POWer:IF:GAIN:STATe?", converter="d")[0]

    def get_detector_type(self, trace_number: int = 1) -> str:
        """
        Query the detector type.

        Parameters
        ----------
        trace_number : int
            Trace number (1 to 6).

        Returns
        -------
        str
            Detector type (e.g., POS, RMS, NEG).
        """
        if trace_number in self._trace_List:
            return self.query(":TRACe" + str(trace_number) + ":DETector?")
        else:
            raise ValueError("Trace Number must be between 1 and 6")

    def get_capture_time(self) -> float:
        """
        Returns the capture time in ms. Range 0 ms to 10000 ms.
        """
        return self.query_ascii_values(":CAPTure:TIMe?")[0]

    # =============================================================================
    #  Write Functions
    # =============================================================================

    def set_sweep_points(self, datapoints: int = 501) -> None:
        """
        Changes the number of display points the instrument currently measures.
        Increasing the number of display points can improve the resolution of
        measurements but will also increase sweep time.

        Parameters
        ----------
        datapoints : int
            Number of points. Range: 10 to 10001. Default: 501.
        """
        if isinstance(datapoints, int):
            if 10 <= datapoints <= 10001:
                self.write(f":DISPlay:POINtcount {datapoints}")
            else:
                raise ValueError(f"Value must be between 10 and 10001, not {datapoints}")
        else:
            raise ValueError("Unknown input! Value must be an integer.")

    def set_start_frequency(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the start frequency. Note that in the spectrum analyzer, changing the
        value of the start frequency will change the value of the coupled parameters,
        Center Frequency and Span.

        Parameters
        ----------
        value : int | float
            Sets the start frequency.

        unit : str
            Default: ``HZ``. Options: {``HZ`` | ``KHZ`` | ``MHZ`` | ``GHZ``}

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:STARt {value} {unit}")
        else:
            raise ValueError("Unknown unit! Should be HZ, KHZ, MHZ or GHZ")

    def set_stop_frequency(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the stop frequency. Note that in the spectrum analyzer, changing the
        value of the start frequency will change the value of the coupled parameters,
        Center Frequency and Span.

        Parameters
        ----------
        value : int | float
            Sets the stop frequency.

        unit : str
            Default: ``HZ``. Options: {``HZ`` | ``KHZ`` | ``MHZ`` | ``GHZ``}

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:STOP {value} {unit}")
        else:
            raise ValueError("Unknown unit! Should be HZ, KHZ, MHZ or GHZ")

    def set_resolution_bandwidth(self, res_bw: int | float, unit: str = "Hz") -> None:
        """
        Sets the resolution bandwidth. Note that using this command turns
        the automatic resolution bandwidth setting OFF.
        In Zero Span, the range will change to allow a minimum of 5 KHz to
        the maximum of 20 MHz.

        Parameters
        ----------
        res_bw : int | float
            Sets the resolution bandwidth.

        unit : str
            Default: ``HZ``. Options: {``HZ`` | ``KHZ`` | ``MHZ`` | ``GHZ``}

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:BANDwidth:RESolution {res_bw} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_resolution_bandwidth_auto(self, state: str | int) -> None:
        """
        Sets the automatic resolution bandwidth state. Setting the value to ON or 1 will
        result in the resolution bandwidth being coupled to the span. That is, when the
        span changes, the resolution bandwidth changes. When this command is issued,
        the resolution bandwidth setting itself will not change.

        Parameters
        ----------
        state : int | str
            Coupling state of resolution bandwidth to span. Default: ``ON``.
            Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        """

        state = self._parse_state(state)
        self.write(f":SENSe:BANDwidth:RESolution:AUTO {state}")

    def set_center_frequency(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the center frequency. Note that changing the value of the center frequency will
        change the value of the coupled parameters Start Frequency and Stop Frequency. It
        might also change the value of the span.

        Parameters
        ----------
        value : int | float
            Sets the center frequency.

        unit : str
            Default: ``HZ``. Options: {``HZ`` | ``KHZ`` | ``MHZ`` | ``GHZ``}

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:CENTer {value} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_span(self, value: int | float, unit: str = "Hz") -> None:
        """
        Sets the frequency span. Setting the value of <freq> to 0 Hz is the
        equivalent of setting the span mode to zero span. Note that changing
        the value of the frequency span will change the value of the coupled
        parameters Start Frequency and Stop Frequency and might change the
        Center Frequency.

        Parameters
        ----------
        value : int | float
            Sets the frequency span.

        unit : str
            Default: ``HZ``. Options: {``HZ`` | ``KHZ`` | ``MHZ`` | ``GHZ``}

        """

        unit = unit.upper() if isinstance(unit, str) else unit
        if unit in self._freq_Units_List:
            self.write(f":SENSe:FREQuency:SPAN {value} {unit}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_continuous(self, state: str | int) -> None:
        """
        Specifies whether the sweep/measurement is triggered continuously. If
        the value is set to ON or 1, another sweep/measurement is triggered as
        soon as the current one completes. If continuous is set to OFF or 0,
        the instrument remains initiated until the current sweep/measurement
        completes, then enters the 'idle' state and waits for the
        :INITiate[:IMMediate] command or for :INITiate:CONTinuous ON.

        Parameters
        ----------
        state : str | int
            Sets the continuous measurement state. Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        """

        state = self._parse_state(state)
        self.write(f":INITiate:CONTinuous {state}")

    def set_data_format(self, state: str = "ASCii") -> None:
        """
        Sets the data format. Only ASCii works!!!

        Parameters
        ----------
        state : str
            Set Data Format. Options: {``ASCii`` | ``INTeger`` | ``REAL``}
        """

        valid_format = self._check_scpi_param(state, ["ASCii", "INTeger", "REAL"])
        self.write(f":FORMat:TRACe:DATA {valid_format}")
        self.get_data_format()

    def set_marker_excursion_state(self, state: str | int) -> None:
        """
        Turn on/off marker excursion state.

        Parameters
        ----------
        state : str | int
            Marker excursion state. Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        """
        state = self._parse_state(state)
        self.write(f":CALCulate:MARKer:PEAK:EXCursion:STATe {state}")

    def set_marker_excursion(self, value: int | float) -> None:
        """
        Sets the excursion for a marker. The excursion is the vertical distance
        from the peak to the next highest valley which must be exceeded for a
        peak to be considered a peak in marker max commands.

        Parameters
        ----------
        value : int | float
            Excursion for a marker in dB. Range: 0.0 to 200.0.
        """
        if 0 <= value <= 200:
            self.write(f":CALCulate:MARKer:PEAK:EXCursion {value} DB")
        else:
            raise ValueError(f"Allowed range is 0dB to 200dB. Current value is {value}dB")

    def set_next_peak(self, marker_num: int = 1) -> None:
        """
        Moves the marker to the next highest peak.

        Parameters
        ----------
        marker_num : int
            Marker number (1 to 12). Default: 1.
        """
        if isinstance(marker_num, int) and marker_num in self._marker_List:
            self.write(f":CALCulate:MARKer{marker_num}:MAXimum:NEXT")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_max_peak(self, marker_num: int = 1) -> None:
        """
        Moves the marker to the highest peak.

        Parameters
        ----------
        marker_num : int
            Marker number (1 to 12). Default: 1.
        """

        if isinstance(marker_num, int) and marker_num in self._marker_List:
            self.write(f":CALCulate:MARKer{marker_num}:MAXimum")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_marker_preset(self) -> None:
        """Presets all markers to their preset values."""
        self.write(":CALCulate:MARKer:APReset")

    def set_ch_power_state(self, state: str | int) -> None:
        """
        Sets the channel power measurement state.
        Sets the state of the channel power measurement, ON or OFF. When using
        :CONFigure:CHPower, the state is automatically set to ON.

        Parameters
        ----------
        state : str | int
            Channel power measurement state. Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        """

        state = self._parse_state(state)
        self.write(f":SENSe:CHPower:STATe {state}")

    def set_trace_mode(self, mode: str = "NORM", trace_number: int = 1, **kwargs) -> None:
        """
        Sets the trace mode.

        Parameters
        ----------
        mode : str
            * Normal - ``NORM`` or ``WRITE``
            * Hold the Minimum - ``MIN`` or ``MINHOLD``
            * Hold the Maximum - ``MAX`` or ``MAXHOLD``
            * Average - ``AVER`` or ``AVERAGE``
            * Rolling Max Hold - ``RMAX``
            * Rolling Min Hold - ``RMIN``
            * Rolling Average - ``RAV``
        trace_number : int
            Trace number (1 to 6). Default: 1.
        """
        mode_map = {
            "WRITE": "NORM",
            "NORM": "NORM",
            "MAXHOLD": "MAX",
            "MAX": "MAX",
            "MINHOLD": "MIN",
            "MIN": "MIN",
            "AVERAGE": "AVER",
            "AVER": "AVER",
            "RMAX": "RMAX",
            "RMIN": "RMIN",
            "RAV": "RAV",
        }
        
        mode_upper = mode.strip().upper()
        if mode_upper in mode_map:
            valid_trace_type = mode_map[mode_upper]
        else:
            valid_list = ["NORM", "MIN", "MAX", "AVER", "RMAX", "RMIN", "RAV"]
            valid_trace_type = self._check_scpi_param(mode, valid_list)
            
        if trace_number in self._trace_List:
            self.write(f":TRACe{trace_number}:TYPE {valid_trace_type}")
        else:
            raise ValueError("Number must be between 1 and 6")

    def set_trace_selected(self, trace_number: int = 1) -> None:
        """
        The selected trace will be used by operations that use a single trace.
        The max number of traces available to select is model specific.

        Parameters
        ----------
        trace_number : int
            Trace number (1 to 6). Default: 1.
        """

        if trace_number in self._trace_List:
            self.write(f":TRACe:SELect {trace_number}")
        else:
            raise ValueError(f"Allowed range is 1 to 6. Current value is {trace_number}")

    def set_trace_state(self, state: str | int = "ON", trace_number: int = 1) -> None:
        """
        The trace visibility state status. If it is OFF, the :TRAC:DATA?
        command will return NaN.

        Parameters
        ----------
        state : str | int
            Trace visibility state. Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        trace_number : int
            Trace number (1 to 6). Default: 1.
        """

        state = self._parse_state(state)
        if trace_number in self._trace_List:
            self.write(f":TRACe{trace_number}:DISPlay:STATe {state}")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_reference_level(self, level: float) -> None:
        """
        Set the reference level in dBm.

        Parameters
        ----------
        level : float
            Reference level in dBm.

        """
        if -150 <= level <= 30:
            self.write(f":DISPlay:TRACe:Y:SCALe:RLEVel {level} dBm")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_if_gain_state(self, state: str | int) -> None:
        """
        Sets the state of the IF gain ON or OFF. ON is only possible
        when reference level is set to <-10 dBm.

        Parameters
        ----------
        state : str | int
            IF gain state. Options: {``1`` | ``0`` | ``ON`` | ``OFF``}
        """

        state = self._parse_state(state)
        self.write(f":POWer:IF:GAIN:STATe {state}")

    def set_detector_mode(
        self,
        mode: str = "POSitive",
        trace_number: int = 1,
        **kwargs
    ) -> None:
        """
        Sets the detector mode.

        Parameters
        ----------
        mode : str
            Detector mode. Options: {``POSitive`` | ``RMS`` | ``NEGative``}
        trace_number : int
            Trace number (1 to 6). Default: 1.
        """

        valid_state = self._check_scpi_param(mode, ["POSitive", "RMS", "NEGative"])
        if trace_number in self._trace_List:
            self.write(f":TRACe{trace_number}:DETector {valid_state}")
        else:
            raise ValueError("Trace Number must be between 1 and 6.")

    def set_capture_time(self, capture_time: float = 0, unit: str = "ms") -> None:
        """
        Determines how much time to spend taking samples for each portion of the spectrum.

        Parameters
        ----------
        capture_time : float, optional
            Capture time. Range: 0.0 to 10000.0. Default: 0.0.
        unit : str, optional
            Default: ``MS``. Options: {``PS`` | ``NS`` | ``US`` | ``MS`` | ``S`` | ``MIN`` | ``HR``}
        """
        valid_unit = self._check_scpi_param(unit, ["PS", "NS", "US", "MS", "S", "MIN", "HR"])
        self.write(f":CAPTure:TIMe {capture_time} {valid_unit}")

    # =============================================================================
    #   get/Save Data
    # =============================================================================

    def get_data(self, marker_num: int = 1, return_array: bool = False) -> dict | np.ndarray:
        """
        This function will stop temporally set Continuous Measurement to OFF, extract
        the max. peak value and frequency and restore the Continuous Measurement to ON.

        Returns
        -------
        dict | np.ndarray
            Measured frequency in Hz and peak power in dBm.
        """

        self.set_continuous("OFF")
        try:
            self.set_marker_preset()
            self.set_max_peak()
            marker_values = self.get_marker_values(marker_num)
            freq = marker_values[0]
            power = marker_values[1]
        finally:
            self.set_marker_preset()
            self.set_continuous("ON")

        if return_array:
            return np.array([freq, power])
        else:
            return {"Frequency/Hz": freq, "Power/dBm": power}

    def extract_trace_data_legacy(self, trace_num: int = 1) -> np.ndarray:
        """
        Old function to keep legacy scripts working.
        Better use: ExtractTraceData()

        !!!!!USE IT AT YOUR OWN RISK is not an official function, but a workaround!!!!!
            1 - This Function will set the continues Measurement to 'OFF'.
            2 - Will set the Data Format to ASCii. This is needed since
            :TREACE:DATA? <num> is defect!!
            3 - Will write TRACE:DATA? <num>. Will return only 3 bits. The rest
            will be packed in the next command asked.
            4 - Will ask for the Data Format. This is dummy command that will
            have the data and the Data Format.
            5 - Make manupulations to separate the actual data from the rest and
            return the data in Output np.array() form.

        Parameters
        ----------
        trace_num : int
            Trace Number from which the data is taken:
            Can be set to [1,2,3,4,5,6].

        Returns
        -------
        np.ndarray
            Measured spectrum on the given trace.
        """

        self.set_continuous("OFF")
        self.set_data_format("ASCii")
        self.write(f":TRACe:DATA? {trace_num}")
        data = self.get_data_format()
        num_header = int(data[1]) + 2  # get the header size
        new_str = data[num_header:-5]  # truncate the header block and end block
        data_arr = new_str.split(",")
        output = [float(item) for item in data_arr]
        output = np.array(output)
        self.set_continuous("ON")
        return output

    def get_trace_xy(self, trace_number: int = 1) -> tuple[np.ndarray, np.ndarray]:
        """
        Queries both X (Frequency) and Y (Amplitude) trace data.
        Calculates X data based on start/stop frequency and sweep points.

        Parameters
        ----------
        trace_number : int
            Trace number (1-6).

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            (x_array, y_array)
        """
        # Get Y data (Amplitudes) - non-blocking query of current trace data
        # Note: We use the direct SCPI command here to avoid the overhead/locking
        # of the helper methods if they exist, similar to FSWP50's get_trace_xy

        if trace_number not in self._trace_List:
            raise ValueError(f"Invalid trace number: {trace_number}.")

        # Ensure correct format before query
        if self._dataFormat != "ASC,8":
            self.set_data_format("ASCii")

        self.write(f":TRACe:DATA? {trace_number}")
        data = self.get_data_format()
        num_header = int(data[1]) + 2
        new_str = data[num_header:-5]
        data_arr = new_str.split(",")
        y_array = np.array([float(item) for item in data_arr])

        # Calculate X data (Frequencies)
        points = len(y_array)
        start_freq = self.get_start_frequency()
        stop_freq = self.get_stop_frequency()

        if points > 1:
            x_array = np.linspace(start_freq, stop_freq, points)
        else:
            x_array = np.array([start_freq])

        return x_array, y_array

    def measure_and_get_trace(
        self, trace_number: int = 1, clear_trace: bool = True, timeout: float = 20
    ) -> np.ndarray:
        """
        Initiate a new measurement and return the trace Y-data (Blocking).
        Renamed from 'extract_trace_data' to match FSWP50 interface.

        Parameters
        ----------
        trace_number : int
            Trace Number: Can be set to [1,2,3,4,5,6].
        clear_trace : bool, optional
            Clears the trace before taking the data measurement. The default is True.
        timeout : float, optional
            Defines the timeout for the operation. The default is 20s.

        Raises
        ------
        TimeoutError

        Returns
        -------
        np.ndarray
            Amplitude data.
        """

        if trace_number not in self._trace_List:
            raise ValueError(
                f"Invalid trace number: {trace_number}. Must be in {self._trace_List}."
            )

        self.set_continuous("OFF")

        # Check the data format
        if self._dataFormat != "ASC,8":
            self.set_data_format("ASCii")

        if clear_trace:
            self.abort()
            # self.clear_trace(trace_number)
            self.init()
            start_time = time()
            complete = 0
            while complete == 0:
                sleep(0.1)
                complete = self.get_operation_status()
                if time() - start_time > timeout:
                    raise TimeoutError(f"Operation did not complete within {timeout:.2f} seconds.")

        self.write(f":TRACe:DATA? {trace_number}")
        data = self.get_data_format()
        num_header = int(data[1]) + 2  # get the header size
        new_str = data[num_header:-5]  # truncate the header block and end block
        data_arr = new_str.split(",")
        output = np.array([float(item) for item in data_arr])

        return output

    def extract_trace_data(
        self,
        trace: int = 1,
        window: int = 1,  # Ignored for MS2760A but kept for compatibility
        points: bool = False,
        num_of_points: int | None = None,
        export: bool = False,
        filename: str = "trace_export.csv",
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Advanced extraction: Gets X and Y data, with optional downsampling and CSV export.
        Matches FSWP50 interface. Does NOT trigger a new measurement
        (use measure_and_get_trace for that).

        Parameters
        ----------
        trace : int
            Trace number (1-6)
        window : int
            Window number (Ignored for MS2760A)
        points : bool
            Whether to limit number of points in output (downsample)
        num_of_points : int, optional
            Desired number of output points if points=True
        export : bool
            If True, saves the data to a CSV file
        filename : str
            Output CSV file name (used if export=True)
        """
        x_array, y_array = self.get_trace_xy(trace)

        if points:
            if num_of_points is None:
                raise ValueError("When points=True, 'num_of_points' must be specified.")
            if num_of_points < len(x_array):
                indices = np.linspace(0, len(x_array) - 1, num=num_of_points, dtype=int)
                x_array = x_array[indices]
                y_array = y_array[indices]

        # Logging only if logger exists (BaseInstrument usually has it)
        if hasattr(self, "logger"):
            self.logger.info(f"Extracted {len(x_array)} points from TRACE{trace}.")

        if export:
            pass  # TODO: Add pandas import if we really want export functionality.
            # For now, to avoid breaking, we will just return data.

        return x_array, y_array

