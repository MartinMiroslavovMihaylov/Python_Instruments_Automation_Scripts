"""
Created on Tue Dec 14 12:58:27 2021

@author: Martin.Mihaylov
"""

import numpy as np
import pandas as pd
import pyvisa 

from .BaseInstrument import BaseInstrument


class AQ6370D(BaseInstrument):
    """
    This class uses BaseInstrument to connect to a Yokogawa AQ6370D.
    Need to have python 'pyvisa', 'pandas' and 'numpy' libraries installed!


    """

    def __init__(self, resource_str: str, visa_library: str = "@py", **kwargs):
        """
        Get name and identification.
        Make a restart of the instrument in the beginning to get the instrument
        to default settings.
        """
        super().__init__(resource_str, visa_library=visa_library, **kwargs)
        print(self.get_idn())

    # =============================================================================
    # Start Sweep
    # =============================================================================

    def start_sweep(self):
        """
        Makes a sweep
        """
        self.write(":INITIATE")

    # =============================================================================
    # Stop Measurment
    # =============================================================================

    def stop(self) -> None:
        """ """
        self.write("ABORt")

    # =============================================================================
    # ASK
    # =============================================================================

    def get_display_auto_y(self) -> str:
        """
        Queries the automatic setting function of
        the subscale of the level axis.
        Response 0 = OFF, 1 = ON
        """
        data = self.query(":DISPLAY:TRACE:Y2:AUTO?")
        if data == "0":
            return "OFF"
        else:
            return "ON"

    def get_display_y_unit(self) -> str | None:
        """
        Queries the units of the main scale of the level axis.
        DBM = dBm
        W = W
        DBM/NM = dBm/nm or dBm/THz
        W/NM = W/nm or W/THz
        """
        data = self.query(":DISPLAY:TRACE:Y1:UNIT?")
        if data == "0":
            return "dBm"
        elif data == "1":
            return "W"
        elif data == "2":
            return "DBM/NM"
        elif data == "3":
            return "W/NM"

    def get_wavelength_start(self) -> float:
        """
        Queries the measurement condition
        measurement start wavelength
        """
        return float(self.query(":SENSE:WAVELENGTH:START?"))

    def get_wavelength_stop(self) -> float:
        """
        Queries the measurement condition
        measurement start wavelength
        """
        return float(self.query(":SENSE:WAVELENGTH:STOP?"))

    def get_center_wavelenght(self) -> float:
        """
        Queries the synchronous sweep function.
        """
        return float(self.query(":SENSe:WAVelength:CENTer?"))

    def get_data_format(self) -> str:
        """
        Queries the format used for data transfer
        via GP-IB.

        ASCii = ASCII format (default)
        REAL[,64] = REAL format (64bits)
        REAL,32 = REAL format (32bits)
        """
        return self.query(":FORMat:DATA?")

    def get_unit_x(self) -> str | None:
        """
        Queries the units for the X axis.

        For AQ6370C, AQ6373 or AQ6373B
        WAVelength = Wavelength
        FREQuency = Frequency
        """
        data = self.query(":UNIT:X?")
        if data == "0":
            return "WAVelength"
        elif data == "1":
            return "FREQuency"
        elif data == "2":
            return "WNUMber"

    def get_trace_state(self) -> str:
        """
        Queries the display status of the specified
        trace.
        """
        data = self.query("TRACe:STATe?")
        if data == "0":
            return "Trace is OFF"
        else:
            return "Trace is ON"

    def get_trace_active(self) -> str:
        """
        Queries the trace to be transferred.

        Outputs - (TRA|TRB|TRC|TRD|TRE|TRF|TRG)
        """
        return self.query(":TRACe:ACTive?")

    def get_central_wavelenght(self) -> float:
        """
        Queries the center wavelength of the
        X-axis of the display scale
        """
        return float(self.query(":SENSE:WAVELENGTH:CENTER?"))

    def get_span(self) -> float:
        """
        Queries the measurement condition
        measurement span.
        """
        return float(self.query(":SENSE:WAVELENGTH:SPAN?"))

    def get_trace_resolution(self, state: str) -> list:
        """
        Queries the actual resolution data of the
        specified trace.

        Parameters
        ----------
        state : str
           Trace selected - ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            data = self.query("CALCULATE:ARESOLUTION? " + str(state)).split(",")
            data = list(np.array(data, dtype=np.float32))
            return data

        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_bw_resolution(self) -> float:
        """
        Queries the measurement resolution.
        """

        return float(self.query(":SENSE:BANDWIDTH?"))

    def get_sensitivity(self) -> str:
        """
        Queries the measurement sensitivity.
        """

        data = self.query(":SENSE:SENSE?")
        if data == "0":
            return "NHLD"
        elif data == "1":
            return "NAUT"
        elif data == "2":
            return "MID"
        elif data == "3":
            return "HIGH1"
        elif data == "4":
            return "HIGH2"
        elif data == "5":
            return "HIGH3"
        else:
            return "NORMAL"

    def get_average_count(self) -> float:
        """
        Queries the number of times averaging for
        each measured point.
        """

        return float(self.query(":SENSE:AVERAGE:COUNT?"))

    def get_segment_points(self) -> float:
        """
        Queries the number of sampling points
        to be measured at one time when performing
        SEGMENT MEASURE.
        """

        return float(self.query(":SENSE:SWEEP:SEGMENT:POINTS?"))

    def get_sample_points(self) -> float:
        """
        Queries the number of samples measured
        """

        return float(self.query(":SENSE:SWEEP:POINTS?"))

    def get_sample_points_auto(self) -> str:
        """
        Queries the function of automatically
        setting the sampling number to be measured

        Response 0 = OFF, 1 = ON
        """

        data = self.query(":SENSE:SWEEP:POINTS:AUTO?")
        if data == "0":
            return "OFF"
        else:
            return "ON"

    def get_sweep_speed(self) -> str:
        """
        Queries the sweep speed
        1x|0: Standard
        2x|1: Twice as fast as standard
        """

        data = self.query(":SENSE:SWEEP:SPEED?")
        if data == "0":
            return "Standard"
        else:
            return "Twice as fast as standard"

    def get_trace_data_x(self, state: str) -> list:
        """
        Queries the wavelength axis data of the
        specified trace.

        Parameters
        ----------
        state : str
             Name of the trace that should be extract/selected.
            state = [TRA|TRB|TRC|TRD|TRE|TRF|TRG]

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            data = self.query(":TRACE:X? " + str(state)).split(",")
            data = list(np.array(data, dtype=np.float32))
            return data
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_trace_data_y(self, state: str) -> list:
        """
        Queries the level axis data of specified trace.

        Parameters
        ----------
        state : str
            Name of the trace that should be extract/selected.
            state = [TRA|TRB|TRC|TRD|TRE|TRF|TRG]

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            data = self.query(":TRACE:Y? " + str(state)).split(",")
            data = list(np.array(data, dtype=np.float32))
            return data
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_sweep_mode(self) -> str | None:
        """
        Queries the sweep mode
        ['SINGle','REPeat','AUTO','SEGMent']
        """

        data = self.query(":INITiate:SMODe?")
        if data == "1":
            return "SINGle"
        elif data == "2":
            return "REPeat"
        elif data == "3":
            return "AUTO"
        elif data == "4":
            return "SEGMent"

    def get_trace_attribute(self, state: str) -> str:
        """
        Queries the attributes of the specified
        trace
        ['WRITe','FIX','MAX','MIN','RAVG','CALC']
        WRITe = WRITE
        FIX = FIX
        MAX = MAX HOLD
        MIN = MIN HOLD
        RAVG = ROLL AVG
        CALC = CALC

        Parameters
        ----------
        state : str
            Name of the trace that should be extract/selected.
            state_list = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            data = self.query(":TRACE:ATTRIBUTE:" + str(state) + "?")
        else:
            raise ValueError("Unknown input! See function description for more info.")
        if data == "0":
            return "WRITE"
        elif data == "1":
            return "FIX"
        elif data == "2":
            return "MAX HOLD"
        elif data == "3":
            return "MIN HOLD"
        elif data == "4":
            return "ROLL AVG"
        else:
            return "CALC"

    # =============================================================================
    # SET
    # =============================================================================

    def set_display_y_unit(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str
            Set the units of the main scale of the
            level axis
            ['dBm','W','DBM/NM','W/NM']

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["dBm", "W", "DBM/NM", "W/NM"]
        if state in state_list:
            self.write(":DISPLAY:TRACE:Y1:UNIT " + str(state))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_wavelength_start(self, value: float, unit: str) -> None:
        """
        Parameters
        ----------
        value : int/float
            Set the measurement condition
        unit : str
            units - [M|HZ].

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["M", "HZ"]
        if unit in unit_list:
            self.write(":SENSE:WAVELENGTH:START " + str(value) + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_wavelength_stop(self, value: float, unit: str) -> None:
        """
        Set the measurement condition
        measurement stop wavelength

        [M|HZ]
        """
        unit_list = ["M", "HZ"]
        if unit in unit_list:
            self.write(":SENSE:WAVELENGTH:STOP " + str(value) + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_data_format(self, unit: str) -> None:
        """
        Parameters
        ----------
        unit : str
            unit_list = ['ASCii', 'REAL[,64]', 'REAL,32']
            Sets the parameter format displayed in an SNP data file.

        Notes
        -----
        When the format is set to REAL (binary) using this command, the
        output data of the following commands is produced in REAL format:

        .. code-block:: none

            :CALCulate:DATA:CGAin?
            :CALCulate:DATA:CNF?
            :CALCulate:DATA:CPOWers?
            :CALCulate:DATA:CSNR?
            :CALCulate:DATA:CWAVelengths?
            :TRACe[:DATA]:X?
            :TRACe[:DATA]:Y?

        - The default is ASCII mode.
        - When the ``*RST`` command is executed, the format is reset to ASCII.
        - The ASCII format outputs a comma-delimited list of numerics (e.g., ``12345,12345,...``).
        - By default, the REAL format outputs 64-bit floating-point binary numbers.
          Specify ``REAL,32`` for 32-bit floating-point.
        - The fixed-length block is defined by IEEE 488.2 and starts with ``#``,
          followed by a digit indicating the number of bytes used to encode the
          length, then the length digits, then the binary payload, for example:

        .. code-block:: none

            #18<8-byte data>
            #280<80-byte data>
            #48008<8008-byte data>

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["ASCii", "REAL[,64]", "REAL,32"]
        if unit in unit_list:
            self.write("FORMAT:DATA " + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_unit_x(self, unit: str) -> None:
        """
        Parameters
        ----------
        unit : str
            Set the units for the X axis.
            unit_list = ['WAV','FREQ','WNUM']

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["WAV", "FREQ", "WNUM"]
        if unit in unit_list:
            self.write(":UNIT:X " + unit)
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_center_wavelenght(self, value: float, unit: str) -> None:
        """
        Parameters
        ----------
        value : int/float
            Set the center wavelength of the
            X-axis of the display scale
        unit : str
            Units = ['M','HZ']

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["M", "HZ"]
        if unit in unit_list:
            self.write(":SENSE:WAVELENGTH:CENTER " + str(value) + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_span(self, value: float, unit: str) -> None:
        """
        Parameters
        ----------
        value : int/float
            Set the measurement span.
        unit : str
            unit_lists = ['M','HZ']
        """

        unit_list = ["M", "HZ"]
        if unit in unit_list:
            self.write(":SENSE:WAVELENGTH:SPAN " + str(value) + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_bw_resolution(self, value: float, unit: str) -> None:
        """
        Parameters
        ----------
        value : int/float
            Set the measurement resolution.
        unit : str
            unit_list = ['M','HZ']

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["M", "HZ"]
        if unit in unit_list:
            self.write(":SENSE:BANDWIDTH:RESOLUTION " + str(value) + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_sensitivity(self, unit: str) -> None:
        """
        Parameters
        ----------
        unit : str
            Set the measurement sensitivity.
                NHLD = NORMAL HOLD
                NAUT = NORMAL AUTO
                NORMal = NORMAL
                MID = MID
                HIGH1 = HIGH1 or HIGH1/CHOP
                HIGH2 = HIGH2 or HIGH2/CHOP
                HIGH3 = HIGH3 or HIGH3/CHOP

        Raises
        ------
        ValueError
            Error message
        """

        unit_list = ["NHLD", "NAUT", "MID", "HIGH1", "HIGH2", "HIGH3", "NORMAL"]
        if unit in unit_list:
            self.write(":SENSE:SENSE " + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_average_count(self, value: int) -> None:
        """
        Parameters
        ----------
        value : int
            Set the number of times averaging for
            each measured point.
        """
        value = int(value)
        self.write(":SENSE:AVERAGE:COUNT " + str(value))

    def set_segment_points(self, value: int) -> None:
        """
        Parameters
        ----------
        value :int
            Set the number of sampling points
            to be measured at one time when performing
            SEGMENT MEASURE.
        """
        value = int(value)
        self.write(":SENSE:SWEEP:SEGMENT:POINTS " + str(value))

    def set_sample_points(self, value: int) -> None:
        """
        Parameters
        ----------
        value : int
            Set the number of samples measured
        """

        value = int(value)
        self.write(":SENSE:SWEEP:POINTS " + str(value))

    def set_sweep_speed(self, value: int) -> None:
        """
        Parameters
        ----------
        value : int
            Set the sweep speed.
            1 - Standard
            2 - Twice as fast as standard
        """

        value = int(value)
        if value == 1:
            self.write(":SENSE:SWEEP:SPEED 1x")
        elif value == 2:
            self.write(":SENSE:SWEEP:SPEED 2x")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_sample_points_auto(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str
            Set the function of automatically
            setting the sampling number to be measured
            ['ON'|'OFF']

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["ON", "OFF"]
        if state in state_list:
            self.write(" :SENSE:SWEEP:POINTS:AUTO " + str(state))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_trace_active(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str
            Sets the active trace.
            state_list = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message
        """

        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            self.write(":TRACE:ACTIVE " + str(state))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_sweep_mode(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str
            Set the sweep mode
            ['SINGle','REPeat','AUTO','SEGMent']

        Raises
        ------
        ValueError
            Error message
        """

        valid_state = self._check_scpi_param(state, ["SINGle", "REPeat", "AUTO", "SEGMent"])
        self.write("INITIATE:SMODE " + valid_state)

    def set_trace_attribute(self, trace: str, state: str) -> None:
        """
        Parameters
        ----------
        trace : str
            Sets the active trace.
            state_list = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        state : str
            Set the attributes of the specified
            trace
            ['WRITe','FIX','MAX','MIN','RAVG','CALC']

            WRITe = WRITE
            FIX = FIX
            MAX = MAX HOLD
            MIN = MIN HOLD
            RAVG = ROLL AVG
            CALC = CALC


        Raises
        ------
        ValueError
            Error message
        """

        valid_state = self._check_scpi_param(state, ["WRITe", "FIX", "MAX", "MIN", "RAVG", "CALC"])
        valid_trace = self._check_scpi_param(
            trace, ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        )
        self.write(f":TRACE:ATTRIBUTE:{valid_trace} {valid_state}")

    # =============================================================================
    # get Data
    # =============================================================================

    def get_data(self, state: str) -> pd.DataFrame:
        """
        Get data on X and Y Traces from OSA.
        Data Output is CST File.
        Data is Saved in X Column and Y Column
        state = 'TRA','TRB','TRC','TRD','TRE','TRF','TRG'
        """
        state_list = ["TRA", "TRB", "TRC", "TRD", "TRE", "TRF", "TRG"]
        if state in state_list:
            # Get Headers
            header_x = self.get_unit_x()
            header_y = self.get_display_y_unit()
            # Get Data
            data_x = self.get_trace_data_x(state)
            data_y = self.get_trace_data_y(state)

            # create CSV
            data = {str(header_x): data_x, str(header_y): data_y}
            data = pd.DataFrame(data, columns=[str(header_x), str(header_y)])

            return data
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def print_params_osa(self) -> None:
        """
        Parameters set on the Yokogawa AQ6370D
        """

        print("################ OSA Parameters ################")
        print("Y-Axis units = ", self.get_display_y_unit())
        print("X-Axis units = ", self.get_unit_x())
        print("Start Wavelength = ", self.get_wavelength_start())
        print("Stop Wavelength = ", self.get_wavelength_stop())
        print("Bandwidth Resolution = ", self.get_bw_resolution())
        print("Center Wavelength = ", self.get_center_wavelenght())
        print("Span = ", self.get_span())
        print("Output data format = ", self.get_data_format())
        print("Displayed trace = ", self.get_trace_state())
        print("Selected Trace = ", self.get_trace_active())
        print("Averaging Points = ", self.get_average_count())
        print("Sample Points = ", self.get_sample_points())
        print("Sweep speed = ", self.get_sweep_speed())
        print("Sweep Mode = ", self.get_sweep_mode())
        print("################ OSA Parameters ################")

    def get_params_osa(self) -> tuple[list[str], list]:
        """
        Parameters set on the Yokogawa AQ6370D
        """
        header = [
            "Y-Axis units",
            "X-Axis units",
            "Start Wavelength",
            "Stop Wavelength",
            "Bandwidth Resolution",
            "Center Wavelength",
            "Span",
            "Output data format",
            "Displayed trace",
            "Selected Trace",
            "Averaging Points",
            "Sample Points",
            "Sweep speed",
            "Sweep Mode",
        ]
        data: list = []

        data.append(self.get_display_y_unit())
        data.append(self.get_unit_x())
        data.append(self.get_wavelength_start())
        data.append(self.get_wavelength_stop())
        data.append(self.get_bw_resolution())
        data.append(self.get_center_wavelenght())
        data.append(self.get_span())
        data.append(self.get_data_format())
        data.append(self.get_trace_state())
        data.append(self.get_trace_active())
        data.append(self.get_average_count())
        data.append(self.get_sample_points())
        data.append(self.get_sweep_speed())
        data.append(self.get_sweep_mode())

        return header, data
