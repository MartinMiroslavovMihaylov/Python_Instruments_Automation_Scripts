"""
Created on Mon Dec 13 10:40:31 2021

@author: Martin.Mihaylov
"""

import numpy as np

from .BaseInstrument import BaseInstrument


class MS4647B(BaseInstrument):
    """
    This class uses BaseInstrument to connect to an Anritsu MS4647B VNA.
    """

    def __init__(self, resource_str: str, visa_library: str = "@py", **kwargs):
        # Do not modify read_termination; pass exactly as in old script
        super().__init__(resource_str, visa_library=visa_library, **kwargs)
        print(self.get_idn())

    # =============================================================================
    # Validate functions
    # =============================================================================

    def _validate_channel_number(self, channel_num: int) -> None:
        """
        Validate channel number.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        if not isinstance(channel_num, int):
            raise ValueError("Channel number must be an integer.")

    # =============================================================================
    # Return to local
    # =============================================================================

    def rtl(self) -> None:
        """
        Send all devices to local operation. No query.
        """
        self.write("RTL")

    # =============================================================================
    # Ask
    # =============================================================================

    def get_sub_system(self) -> str:
        """
        The :SENSe:HOLD subsystem command sets the hold function for all
        channels on a per-instrument basis.
        """
        return self.query(":SENSe:HOLD:FUNCtion?")

    def get_sweep_count(self, channel_num: int) -> float:
        """
        Query only. Outputs the averaging sweep count for the indicated channel.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENS" + str(channel_num) + ":AVER:SWE?"))

    def get_test_set(self, channel_num: int) -> str:
        """
        Query State of TS3739.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return self.query(":SENS" + str(channel_num) + ":TS3739:STATe?")

    def get_sys_errors(self) -> str:
        """
        Query only. Outputs the number of errors in the error queue.
        """
        return self.query(":SYST:ERR:COUN?")

    def get_stat_operation(self) -> int:
        """
        Query only. Outputs the value of the operation status condition reg.
        Range: 0 to 32767
        Default Value: 0
        """
        return int(float(self.query(":STAT:OPER:COND?")))

    def get_stat_operation_register(self) -> int:
        """
        Sets the value of the operation status enable register.
        Outputs the value of the operation status enable register.
        """
        return int(float(self.query(":STATus:OPERation:ENABle?")))

    def get_freq_span(self, channel_num: int) -> float:
        """
        Optional query. Span is automatically calculated as Stop Frequency minus
        Start Frequency. The query returns the resulting span in Hertz.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENSe" + str(channel_num) + ":FREQuency:SPAN?"))

    def get_center_freq(self, channel_num: int) -> float:
        """
        Optional query. Center frequency is automatically calculated using Stop Frequency
        and Start Frequency as: Fc = ((Fstop - Fstart)/2) + Fstart

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENSe" + str(channel_num) + ":FREQuency:CENTer?"))

    def get_cw_freq(self, channel_num: int) -> float:
        """
        Sets the CW frequency of the indicated channel. Outputs the CW
        frequency of the indicated channel.
        The output parameter is in Hertz.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENS" + str(channel_num) + ":FREQ:CW?"))

    def get_data_freq(self, channel_num: int) -> str:
        """
        Outputs the frequency list for the indicated channel.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return self.query(":SENSe" + str(channel_num) + ":FREQuency:DATA?")

    def get_sweep_channel_status(self) -> str:
        """
        The query outputs the On/Off state of the option to sweep only the active
        channel
        """
        return self.query(":DISP:ACT:CHAN:SWE:STAT?")

    def get_assignet_data_port(self, value: int) -> str:
        """
        Outputs the data port pair assigned to use when creating an sNp data
        file on the indicated channel.

        Parameters
        ----------
        value : int/float
            the N(ports number) for the .sNp data output.
        """
        _value = str(value)
        if _value in ["1", "2", "3", "4"]:
            return self.query("FORMat:S" + str(_value) + "P:PORT?")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_param_form_in_file(self) -> str:
        """
        Outputs the parameter format displayed in an SNP data file.
        """
        return self.query(":FORMat:SNP:PARameter?")

    def get_rf_state(self) -> str:
        """
        Outputs the RF on/off state in Hold.
        """
        return self.query(":SYST:HOLD:RF?")

    def get_set_average_state(self, channel_num: int) -> str:
        """
        Outputs the averaging function on/off status on the indicated channel.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return self.query(":SENS" + str(channel_num) + ":AVER?")

    def get_average_function_type(self, channel_num: int) -> str:
        """
        Outputs the averaging function type of point-by-point or sweep-by-sweep.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return self.query(":SENS" + str(channel_num) + ":AVER:TYP?")

    def get_average_count(self, channel_num: int) -> float:
        """
        Outputs the averaging count for the indicated channel.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENS" + str(channel_num) + ":AVER:COUN?"))

    def get_transfer_data(self, name: str, port_num: int) -> str:
        """
        The query outputs the disk file data to the GPIB. The file must exist.
        Hard coded path on the VNA = 'C:/tmp/'

        Parameters
        ----------
        name : str
            File Name
        port_num : int
            the N(ports number) for the .sNp data output.
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.s" + str(port_num) + "p"
        return self.query(":MMEM:TRAN? " + '"' + path + '"')

    def get_transfer_data_csv(self, name: str) -> str:
        """
        The query outputs the disk file data to the GPIB. The file must exist.
        Hard coded path on the VNA = 'C:/tmp/'

        Parameters
        ----------
        name : str
            File Name
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.csv"
        return self.query(":MMEM:TRAN? " + '"' + path + '"')

    def get_resolution_bw(self, channel_num: int) -> float:
        """
        The command sets the IF bandwidth for the indicated channel. The query outputs the IF
        bandwidth for the indicated channel.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":SENS" + str(channel_num) + ":BAND?"))

    def get_power_on_port(self, segment: int, channel_num: int) -> float:
        """
        Outputs the power level of the indicated port on the indicated channel.

        Parameters
        ----------
        segment : int
            Selected Source. Can be from 1-16
        channel_num : int
            Channel Number 1,2,3...
        """
        segment_list = np.arange(1, 17, 1)
        channel_num_list = np.arange(1, 5, 1)
        if segment in segment_list and channel_num in channel_num_list:
            return float(self.query(":SOUR" + str(segment) + ":POW:PORT" + str(channel_num) + "?"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_smoothing_state(self, channel_num: int) -> float:
        """
        Query outputs the smoothing on/off status for the indicated channel and active trace.
        1 = ON
        2 = OFF

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        return float(self.query(":CALC" + str(channel_num) + ":SMO?"))

    def get_display_trace(self) -> str:
        """
        Query only. Outputs the Active Channel number.
        """
        return self.query(":DISPlay:WINDow:ACTivate?")

    def get_display_count(self) -> float:
        """
        Query the number of displayed channels.
        """
        return float(self.query(":DISP:COUN?"))

    def get_display_title(self) -> str:
        """
        Outputs the user title for the channel indicated.
        """
        return self.query(":DISP:WIND1:TITL?")

    def get_select_parameter(self) -> str:
        """
        The query outputs only the selected parameter.
        """
        return self.query(":CALC1:PAR1:DEF?")

    def get_sweep_delay(self) -> float:
        """
        Outputs the sweep delay time of the indicated channel.
        """
        return float(self.query(":SENS1:SWE:DEL?"))

    def get_sweep_time(self) -> float:
        """
        Outputs the Sweep Time of the indicated channel.
        """
        return float(self.query(":SENS1:SWE:TIM?"))

    # =============================================================================
    # Set
    # =============================================================================

    def set_clear_average(self, channel_num: int) -> None:
        """
        Clears and restarts the averaging sweep count of the indicated channel.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        self.write(":SENS" + str(channel_num) + ":AVER:CLE")

    def set_sub_system_hold(self) -> None:
        """
        Sets the hold function for all channels on a per-instrument basis.
        The sweep is stopped.
        """

        self.write(":SENS:HOLD:FUNC HOLD")

    def set_sub_system_sing(self) -> None:
        """
        The sweep restarts and sweeps until the end of the
        sweep, at which point it sets the end of sweep status bit and
        stops.
        """
        self.write(":SENS:HOLD:FUNC SING")

    def set_sub_system_cont(self) -> None:
        """
        The sweep is sweeping continuously.
        """
        self.write(":SENS:HOLD:FUNC CONT")

    def set_display_scale(self) -> None:
        """
        Auto scales all traces on all channels.
        """
        self.write(":DISPlay:Y:AUTO")

    def set_ts3739(self, channel_num: int, state: str | int) -> None:
        """
        The :SENSe{1-16}:TS3739 subsystem commands are used to configure and
        control the VectorStar ME7838x  Broadband/Millimeter-Wave 3738A Test Set.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        state : str/int
            ON/OFF or 1/0.
        """
        self._validate_channel_number(channel_num)
        parsed_state = self._parse_state(state)
        self.write(":SENS" + str(channel_num) + ":TS3739 " + parsed_state)

    def set_clear_error(self) -> None:
        """
        Clears the contents of the error queue.
        """
        self.write(":SYST:ERR:CLE")

    def set_display_color_reset(self) -> None:
        """
        Resets all colors and inverted colors to their normal default values.
        """
        self.write(":DISP:COL:RES")

    def set_stat_operation_register(self, value: int) -> None:
        """
        Sets the value of the operation status enable register.
        Outputs the value of the operation status enable register.

        Parameters
        ----------
        value : int
            The input parameter is a unitless number.
            Range: 0 to 65535
        """
        if isinstance(value, int) and 0 <= value <= 65535:
            self.write(":STAT:OPER:ENAB " + str(value))
        else:
            raise ValueError("Value must be an integer between 0 and 65535.")

    def set_start_freq(self, channel_num: int, value: int | str) -> None:
        """
        Sets the start value of the sweep range of the indicated channel.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
                The input parameter is in Hertz, Meters, or Seconds.
        """
        self._validate_channel_number(channel_num)
        self.write(":SENSe" + str(channel_num) + ":FREQuency:STARt " + str(value))

    def set_stop_freq(self, channel_num: int, value: int | str) -> None:
        """
        Sets the stop value of the sweep range of the indicated channel.
        The input parameter is in Hertz, Meters, or Seconds.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9

        """
        self._validate_channel_number(channel_num)
        self.write(":SENSe" + str(channel_num) + ":FREQuency:STOP " + str(value))

    def set_center_freq(self, channel_num: int, value: int | str) -> None:
        """
        Sets the center value of the sweep range of the indicated channel.
        Outputs the center value of the sweep range of the indicated channel

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9

        """
        self._validate_channel_number(channel_num)
        self.write(":SENS" + str(channel_num) + ":FREQ:CENT " + str(value))

    def set_cw_freq(self, channel_num: int, value: int | str) -> None:
        """
        Sets the CW frequency of the indicated channel.
        Outputs the CW frequency of the indicated channel.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
        """
        self._validate_channel_number(channel_num)
        self.write(":SENS" + str(channel_num) + ":FREQ:CW " + str(value))

    def set_sweep_channel_status(self, state: str | int) -> None:
        """
        The command turns On/Off the option to sweep only the active channel

        Parameters
        ----------
        state : str/int
                ON/OFF or 1/0.
        """
        parsed_state = self._parse_state(state)
        self.write(":DISP:ACT:CHAN:SWE:STAT  " + parsed_state)

    def set_assignet_data_port(self, channel_num: int, value1: int, value2: int) -> None:
        """
        The command assigns the data port pair to use when creating an sNp
        data file on the indicated channel. The use of Port 3 and/or Port 4
        requires a 4-port VNA instrument.
        PORT12 | PORT13 | PORT14 | PORT23 | PORT24 | PORT34

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value1 : int
        value2 : int
        """
        _value1 = str(value1)
        _value2 = str(value2)
        if isinstance(channel_num, int):
            if _value1 in ["1", "2", "3", "4"]:
                self.write(
                    ":CALC"
                    + str(channel_num)
                    + ":FORM:S"
                    + str(_value1)
                    + "P:PORT PORT"
                    + str(_value1)
                    + str(_value2)
                )
            else:
                raise ValueError("Unknown input! See function description for more info.")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_param_form_in_file(self, unit: str) -> None:
        """
        Sets the parameter format displayed in an SNP data file.

        Parameters
        ----------
        unit : str
            - LINPH = Linear and Phase
            - LOGPH = Log and Phase
            - REIM = Real and Imaginary Numbers
        """
        unit_parsed = self._check_scpi_param(unit, ["LINPH", "LOGPH", "REIM"])
        self.write(":FORM:SNP:PAR " + unit_parsed)

    def set_rf_state(self, state: str | int) -> None:
        """
        Sets the RF on/off state in Hold.

        Parameters
        ----------
        state : str/int
            Sets the RF on/off state in Hold.
        """
        parsed_state = self._parse_state(state)
        self.write(":SYST:HOLD:RF " + parsed_state)

    def set_set_average_state(self, channel_num: int, state: str | int) -> None:
        """
        Turns averaging on/off for the indicated channel
        (Turns ON and Off the averaging for all channels).

        Parameters
        ----------
        channel_num : int
                    Channel Number 1,2,3...
        state : int/str
                ON/OFF or 1/0.
        """
        self._validate_channel_number(channel_num)
        parsed_state = self._parse_state(state)
        self.write(":SENS" + str(channel_num) + ":AVER " + parsed_state)

    def set_average_function_type(self, channel_num: int, state: str) -> None:
        """
        Sets the averaging function type to point-by-point or sweep-by-sweep.

        Parameters
        ----------
        channel_num : int
                    Channel Number 1,2,3...
        state : str
            Sets the averaging function type to point-by-point or sweep-by-sweep.
            POIN | SWE
            Default Value: POIN
        """
        self._validate_channel_number(channel_num)
        state_parsed = self._check_scpi_param(state, ["POINt", "SWEep"])
        self.write(":SENS" + str(channel_num) + ":AVER:TYP " + state_parsed)

    def set_average_count(self, channel_num: int, value: int) -> None:
        """
        Sets the averaging count for the indicated channel. The channel must
        be turned on.

        Parameters
        ----------
        channel_num : int
                     Channel Number 1,2,3...
        value : int
            The input parameter is a unitless number. Range: 1 to 1024
            Default Value: 1
        """

        _value = str(value)
        self._validate_channel_number(channel_num)
        self.write(":SENS" + str(channel_num) + ":AVER:COUN " + str(_value))

    def set_resolution_bw(self, channel_num: int, value: int | float | str) -> None:
        """
        Sets the IF bandwidth for the indicated channel.

        Parameters
        ----------
        channel_num : int
                    Channel Number 1,2,3...
        value : int/floa/str
            IF Bandwidth in Hz
        """

        value = str(value)
        self._validate_channel_number(channel_num)
        self.write(":SENS" + str(channel_num) + ":BAND " + str(value))

    def set_power_on_port(self, segment: int, channel_num: int, value: int | float | str) -> None:
        """
        Sets the power level of the indicated port on the indicated channel.

        Parameters
        ----------
        segment : int
            Selected Source. Can be from 1-16
        channel_num : int
            Channel Number 1,2,3...
        value : int/floa/str
            Power level
        """

        segment_list = np.arange(1, 17, 1)
        channel_num_list = np.arange(1, 5, 1)
        if segment in segment_list and channel_num in channel_num_list:
            self.write(":SOUR" + str(segment) + ":POW:PORT" + str(channel_num) + " " + str(value))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_smoothing_state(self, channel_num: int, state: str | int) -> None:
        """
        Turns smoothing on/off for the indicated channel.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        state : str/int
            can be int or str form the list ['ON','OFF',1,0]
        """
        self._validate_channel_number(channel_num)
        parsed_state = self._parse_state(state)
        self.write(":CALC" + str(channel_num) + ":SMO " + parsed_state)

    def set_smoothing_ape_rture(self, channel_num: int, value: int) -> None:
        """


        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        value : int
            Percentage smoothing between 0 to 100
        """
        self._validate_channel_number(channel_num)
        self.write(":CALC" + str(channel_num) + "SMO:APER " + str(float(value)))

    def set_display_trace(self, channel_num: int) -> None:
        """
        The command sets the active channel to the indicated number. When the VNA is set to
        100,000 point mode, the number of channels is 1.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        self.write(":DISP:WIND" + str(channel_num) + ":ACT")

    def set_display_count(self, channel_num: int) -> None:
        """
        Sets the number of displayed channels. When the VNA is in 25,000 point mode, the
        number of channels can only be 1 (one), 2, 3, 4, 6, 8, 9, 10, 12, or 16 channels. If the
        channel display is set to a non-listed number (5, 7, 11, 13, 14, 15), the instrument is set
        to the next higher channel number. If a number of greater than 16 is entered, the
        instrument is set to 16 channels. If the instrument is set to 100,000 points, any input
        results in 1 (one) channel. Outputs the number of displayed channels.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """
        self._validate_channel_number(channel_num)
        self.write(":DISP:COUN " + str(channel_num))

    def set_display_title(self, channel_name: str) -> None:
        """
        Sets the user title for the channel indicated.

        Parameters
        ----------
        channel_num : int
            Channel Number 1,2,3...
        """

        if isinstance(channel_name, str):
            self.write(":DISP:WIND1:TITL " + channel_name)
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_select_parameter(self, s_param: str) -> None:
        """
        Select an S-Parameter. 16 S-Parameters for 4 Ports config can be selected.

        Parameters
        ----------
        s_param : str
            S-Parameter selected.
        """
        s_param_list = [
            "S11",
            "S12",
            "S13",
            "S14",
            "S21",
            "S22",
            "S23",
            "S24",
            "S31",
            "S32",
            "S33",
            "S34",
            "S41",
            "S42",
            "S43",
            "S44",
        ]
        if isinstance(s_param, str):
            if s_param in s_param_list:
                self.write(":CALC1:PAR1:DEF " + s_param)
            else:
                raise ValueError("Unknown input! See function description for more info.")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_sweep_delay(self, time: float) -> None:
        """
        Parameters
        ----------
        time : float
            Sets the sweep delay time of the indicated channel.
        """
        self.write(":SENS1:SWE:DEL " + str(time))

    def set_sweep_time(self, time: float) -> None:
        """
        Parameters
        ----------
        time : float
            Sets the Sweep Time of the indicated channel.
        """
        self.write(":SENS1:SWE:TIM " + str(time))

    # =============================================================================
    # Save
    # =============================================================================

    def save_data(self, name: str, port_num: int) -> None:
        """
        Parameters
        ----------
        name : str
            File Name
        port_num : TYPE
            The N(ports number) for the .sNp data output.
            Description: Stores a data file of the type specified by the filename
            extension.No query.
            Hard coded path on the VNA = 'C:/tmp/'
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.s" + str(port_num) + "p"
        self.write(":MMEM:STOR " + '"' + path + '"')

    def save_data_csv(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            File Name
            Description: Stores a data file of the type specified by the filename
            extension.No query.
            Hard coded path on the VNA = 'C:/tmp/'
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.csv"
        self.write(":MMEM:STOR " + '"' + path + '"')

    def save_image(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            File Name
            Description: Stores a data file of the type specified by the filename
            extension.No query.
            Hard coded path on the VNA = 'C:/tmp/'
        """
        path = "C:/tmp/Image/"
        path = str(path) + str(name) + "_.png"
        self.write(":MMEMory:STORe:IMAGe " + '"' + path + '"')

    def delete_data(self, name: str, port_num: int) -> None:
        """
        Parameters
        ----------
        name : str
            File Name
        port_num : TYPE
            The N(ports number) for the .sNp data output.
            Delete a disk, file, or directory. Use caution with this command as there is no
            recovery operation in case of a user mistake or error. No query
            Hard coded path on the VNA = 'C:/tmp/'
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.s" + str(port_num) + "p"
        self.write(":MMEMory:DEL " + '"' + path + '"')

    def delete_data_csv(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            File Name
            Delete a disk, file, or directory. Use caution with this command as there is no
            recovery operation in case of a user mistake or error. No query
            Hard coded path on the VNA = 'C:/tmp/'
        """
        path = "C:/tmp/"
        path = str(path) + str(name) + "_.csv"
        self.write(":MMEMory:DEL " + '"' + path + '"')

    def save_transfer_data(self, file: str, path: str, name: str, port_num: int) -> None:
        """
        Parameters
        ----------
        file : str
            File data extracted from function ask_TransferData
        path : str
            Where on the PC to save the data
        name : str
            Name of the File
        port_num : int/str
            The N(ports number) for the .sNp data output.
            Write a text File with the transferred data
        """
        readinglines = file.splitlines()
        with open(str(path) + "/" + str(name) + ".s" + str(port_num) + "p", "w") as f:
            for line in readinglines:
                f.write(line)
                f.write("\n")

    def save_transfer_data_csv(self, file: str, path: str, name: str) -> None:
        """
        Parameters
        ----------
        file : str
            File data extracted from function ask_TransferData
        path : str
            Where on the PC to save the data
        name : str
            Name of the File
            Write a text File with the transferred data
        """
        readinglines = file.splitlines()
        with open(str(path) + "/" + str(name) + ".csv", "w") as f:
            for line in readinglines:
                f.write(line)
                f.write("\n")

