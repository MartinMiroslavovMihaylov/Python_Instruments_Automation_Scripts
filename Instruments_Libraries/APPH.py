"""
Created on Tue Feb 15 10:57:49 2022

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa

class APPH:
    def __init__(self, resource_str):

        self._resource = visa.ResourceManager().open_resource(str(resource_str),query_delay  = 0.5,read_termination = '\n')
        print(self._resource.query('*IDN?'))

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        print('AnaPico AG,APPH20G is closed!')
        self._resource.close()

    # =============================================================================
    # Initiate System
    # =============================================================================
    def init(self) -> None:
        """
        Initialize the measurement
        """
        self.write(":INITiate:IMMediate")

    # =============================================================================
    # Abort
    # =============================================================================

    def abort(self) -> None:
        """
        Abort measurement
        """
        self.write(":ABORt")
    
    # =============================================================================
    # Validate Variables
    # =============================================================================

    def _parse_state(self, state: str | int | float | bool) -> str:
        """
        Helper to parse various input types into SCPI 'ON' or 'OFF' strings.
        Supports bool (True/False), numeric (1/0, 1.0/0.0), and strings ('ON'/'OFF', '1'/'0').
        """
        if isinstance(state, bool):
            return "ON" if state else "OFF"

        if isinstance(state, (int, float)):
            if state == 1:
                return "ON"
            elif state == 0:
                return "OFF"

        s = str(state).strip().upper()
        if s in ["ON", "1", "1.0"]:
            return "ON"
        elif s in ["OFF", "0", "0.0"]:
            return "OFF"
        else:
            raise ValueError(f"Invalid state: '{state}'. Use True/False, 1/0, or 'ON'/'OFF'.")
        
    def _check_scpi_param(self, user_input: str, allowed_params: list[str]) -> str:
        """
        Validates user input against a list of allowed SCPI parameters.
        Supports SCPI short forms (e.g., 'PHOT' for 'PHOTodiode') and is case-insensitive.
        Returns the exact parameter string as provided in allowed_params.
        """
        user_input_upper = str(user_input).strip().upper()

        for param in allowed_params:
            # Handle optional characters like [] if they exist
            clean_param = param.replace("[", "").replace("]", "")

            # Extract the mandatory short form, represented by uppercase letters
            short_form = "".join(c for c in param if c.isupper())
            if not short_form:
                short_form = clean_param.upper()

            long_form = clean_param.upper()

            # Input must be at least the short form length, and match the long form's prefix
            if len(user_input_upper) >= len(short_form) and long_form.startswith(user_input_upper):
                return param

        raise ValueError(
            f"Invalid input '{user_input}'. Allowed parameters are: {allowed_params} "
            "(case-insensitive, abbreviation allowed up to the capital letters)."
        )

    # =============================================================================
    # ASK
    # =============================================================================

    def get_calc_freq(self) -> float:
        """
        Reads back the detected frequency from a frequency search.
        """
        return float(self.query(':CALCulate:FREQuency?').split('\n')[0])

    def get_calc_power(self) -> float:
        """
        Reads back the detected power level from a frequency search.
        """
        return float(self.query(':CALCulate:POWer?').split('\n')[0])  

    def get_dut_port_voltage(self) -> float:
        """
        Sets/gets the voltage at the DUT TUNE port. Returns the configured value. If the output
        is turned off, it doesn't necessarily return 0, as an internal voltage may be configured.
        """
        return float(self.query(':SOURce:TUNE:DUT:VOLT?').split('\n')[0])

    def get_dut_port_status(self) -> str:
        """
        Query the status of the DUT TUNE port.
        """
        stat = self.query("SOURce:TUNE:DUT:STAT?").split('\n')[0]
        if stat == "0":
            stat = "OFF"
        else:
            stat = "ON"
        return stat

    def get_sys_meas_mode(self) -> str:
        """
        Gets the active measurement mode.
        """
        return self.query("SENSe:MODE?")

    def get_system_error(self) -> str:
        """
        Return parameters: List of integer error numbers. This query is a request for all
        entries in the instrument's error queue. Error messages in the queue contain an
        integer in the range [-32768,32768] denoting an error code and associated descriptive
        text. This query clears the instrument's error queue.
        """
        return self.query(":SYSTem:ERRor:ALL?")

    # =============================================================================
    # Ask Phase Noise
    # =============================================================================

    def get_pm_trace_jitter(self) -> str:
        """
        Returns the RMS jitter of the current trace.
        """
        return self.query(":CALCulate:PN:TRACE:SPURious:JITTer?")

    def get_pm_trace_noise(self) -> str:
        """
        Returns a list of phase noise points of the most recent measurement as block data.
        """
        return self.query(":CALCulate:PN:TRACe:NOISe?")

    def get_pn_if_gain(self) -> float:
        """
        Range: 0-60
        Query the IF gain for the measurement.
        """
        return float(self.query(":SENSe:PN:IFGain?"))

    def get_pn_start_freq(self) -> float:
        """
        Query the start offset frequency
        """
        return float(self.query(':SENSe:PN:FREQuency:STARt?').split('\n')[0])

    def get_pn_stop_freq(self) -> float:
        """
        Query the stop offset frequency
        """
        return float(self.query(':SENSe:PN:FREQuency:STOP?').split('\n')[0])

    def get_pn_spot(self, value: float) -> str:
        """
        Returns the phase noise value of the last measurement at the offset frequency
        defined in <value>. The parameter is given as offset frequency in [Hz]
        Unit Hz
        Value - float

        Parameters
        ----------
        value : float
            The parameter is given as offset frequency in [Hz]
            Unit Hz
            Value - float
        """
        return self.query("CALCulate:PN:TRACE:SPOT? " + str(value))

    # =============================================================================
    # Ask Amplitude Noise
    # =============================================================================

    def get_an_trace_freq(self) -> str:
        """
        Returns a list of offset frequency values of the current measurement as block data.
        Hz
        """
        return self.query(":CALCulate:AN:TRACe:FREQuency?")

    def get_an_trace_noise(self) -> str:
        """
        Returns a list of amplitude noise spectrum values of the current measurement
        as block data. Unit dBc/Hz
        """
        return self.query("CALCulate:AN:TRACe:NOISe?")

    def get_an_trace_spur_freq(self) -> str:
        """
        Returns a list of offset frequencies of the spurs in the active trace as block data.
        Unit Hz
        """
        return self.query(":CALCulate:AN:TRACe:SPURious:FREQuency?")

    def get_an_trace_spur_power(self) -> str:
        """
        Returns a list of power values of the spurs in the active trace as block data.
        Unit dBc
        """
        return self.query(":CALCulate:AN:TRACe:SPURious:POWer?")

    def get_an_spot(self, value: float) -> str:
        """
        Returns the phase noise value of the last measurement at the offset frequency
        defined in <value>. The parameter is given as offset frequency in [Hz]
        Unit Hz
        Value - float

        Parameters
        ----------
        value : float
            The parameter is given as offset frequency in [Hz]
            Unit Hz
            Value - float
        """
        return self.query("CALCulate:AN:TRACE:SPOT? " + str(value))

    # =============================================================================
    # Ask Frequency Noise
    # =============================================================================

    def get_fn_trace_freq(self) -> str:
        """
        Returns a list of offset frequency values of the current measurement as block data.
        Unit Hz
        """
        return self.query(":CALCulate:FN:TRACe:FREQuency?")

    def get_fn_trace_noise(self) -> str:
        """
        Returns a list of phase noise spectrum values of the current measurement as block data.
        Units are in Hz.
        """
        return self.query(":CALCulate:FN:TRACe:NOISe?")

    def get_fn_trace_spur_freq(self) -> str:
        """
        Returns a list of offset frequencies of the spurs in the active trace as block data.
        Units are in Hz.
        """
        return self.query(":CALCulate:FN:TRACe:SPURious:FREQuency?")

    def get_fn_trace_spur_power(self) -> str:
        """
        Returns a list of power values of the spurs in the active trace as block data.
        Units are in Hz
        """
        return self.query(":CALCulate:FN:TRACe:SPURious:POWer?")

    def get_fn_spot(self, value: float) -> str:
        """
        Returns the spot noise value at the specified offset frequency.

        Parameters
        ----------
        value : float
            The parameters defines the spot noise offset frequency in [Hz].
            Units are in Hz.
            Value - float
        """
        return self.query("CALCulate:FN:TRACE:SPOT? " + str(value))

    # =============================================================================
    # Ask Voltage controlled Oscillator
    # =============================================================================

    def get_vco_trace_freq(self) -> str:
        """
        Returns a list of frequency values measured at each tune voltage point of the
        current measurement as block data2.
        """
        return self.query("CALCulate:VCO:TRACE:FREQuency?")

    def get_vco_trace_p_noise(self, chan: list) -> str:
        """
        Returns a list of phase noise values measured at each tune voltage point of
        the current measurement as block data. The parameter 1-4 selects the offset
        frequency from the set defined by the SENS:VCO:TEST:PN:OFFS <list> command

        Parameters
        ----------
        chan : list
            Can be set to [1,2,3,4]

        Raises
        ------
        ValueError
            Error massage
        """
        chan_list = [1, 2, 3, 4]
        if chan in chan_list:
            return self.query("CALCulate:VCO:TRACE:PNoise? " + str(chan))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_vco_trace_power(self) -> str:
        """
        Returns a list of power values measured at each tune voltage point of the current
        measurement as block data.
        """
        return self.query("CALCulate:VCO:TRACE:POWer?")

    def get_vco_trace_voltage(self) -> str:
        """
        Returns a list of tune voltage values measured at each tune voltage point of the
        current measurement as block data.
        """
        return self.query("CALCulate:VCO:TRACE:VOLTage?")

    def get_vso_test_freq(self) -> str:
        """
        Query the frequency parameter for the measurement.
        """
        return self.query(":SENSe:VCO:TEST:FREQuency?")

    def get_vso_test_noise(self) -> str:
        """
        Query the phase noise parameter for the measurement.
        """
        return self.query(":SENSe:VCO:TEST:PNoise?")

    def get_vco_test_power(self) -> str:
        """
        Query the power parameter for the measurement.
        """
        return self.query(":SENSe:VCO:TEST:POWer?")

    def get_vco_test_start(self) -> str:
        """
        Query the start tuning voltage for the measurement.
        Units are in V.
        """
        return self.query(":SENSe:VCO:VOLTage:STARt?")

    def get_vco_test_stop(self) -> str:
        """
        Query the stop tuning voltage for the measurement.
        Units are in V
        """
        return self.query(":SENSe:VCO:VOLTage:STOP?")

    def get_vco_test_i_supply(self) -> str:
        """
        Query the supply current parameter for the measurement
        """
        return self.query(":SENSe:VCO:TEST:ISUPply?")

    def get_vcok_pu_shing(self) -> str:
        """
        Query the pushing parameter for the measurement
        """
        return self.query(":SENSe:VCO:TEST:KPUShing?")

    def get_vcokvco(self) -> str:
        """
        Query the tune sensitivity parameter for the measurement.
        """
        return self.query(":SENSe:VCO:TEST:KVCO?")

    def get_vcotype(self) -> str:
        """
        Query the DUT type for the measurement.
        """
        return self.query(":SENSe:VCO:TYPE?")

    def get_vco_test_p_noise(self) -> str:
        """
        Query the phase noise parameter for the measurement.
        """
        return self.query(":SENSe:VCO:TEST:PNoise?")

    def get_vco_test_pnoise_off_set(self, state: int) -> str:
        """
        Query the 4 offset frequencies at which the phase noise is measured

        Parameters
        ----------
        state : int
            Can be set to [1,2,3,4]

        Raises
        ------
        ValueError
            Error massage
        """
        state_list = [1, 2, 3, 4]
        if state in state_list:
            return self.query(":SENSe:VCO:TEST:Pnoise:OFFSet" + str(state) + "?")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def get_vco_test_point(self) -> str:
        """
        Query the number rof voltage points to use in the measurement
        """
        return self.query(":SENSe:VCO:VOLTage:POINts?")

    # =============================================================================
    # SET
    # =============================================================================

    def set_output(self, status: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        status : str
            Set Output ON and OFF.  CAn be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage
        """
        valid_status = self._parse_state(status)
        self.write(":OUTput " + valid_status)

    def set_sys_meas_mode(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str
            Sets/gets the active measurement mode. Can be ['PN','AN','FN','BB','TRAN','VCO']
                • PN: phase noise measurement
                • AN: amplitude noise measurement
                • FN: frequency noise measurement (results are converted to phase noise)
                • BB: base band measurement (not yet available)
                • TRAN: transient analysis (not yet available)
                • VCO: voltage controlled oscillator characterization

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._check_scpi_param(state, ["PN", "AN", "FN", "BB", "TRAN", "VCO"])
        self.write("SENSe:MODE " + valid_state)

    def set_freq_execute(self) -> None:
        """
        Starts the frequency search. See function calculate subsystem on how to read out the result.
        """
        self.write("SENSe:FREQuency:EXECute?")

    def set_power_execute(self) -> None:
        """
        Starts the power measurement. When performing SENS:FREQ:EXEC, this measurement
        will be automatically run at the end (if a signal is detected
        """
        self.write("SENSe:POWer:EXECute?")

    def set_calc_average(self, event: str) -> None:
        """
        Parameters
        ----------
        event : str
                Waits for the defined event
                NEXT: next iteration complete
                ALL: measurement complete
                <value>: specified iteration complete
                Optionally, a timeout in milliseconds can be specified as a second parameter.
                This command will block further SCPI requests until the specified event or the
                specified timeout has occurred. If no timeout is specified, the timeout will be
                initiated.
        """
        self.write("CALCulate:WAIT:AVERage " + str(event))

    def set_dut_port_voltage(self, value: float) -> None:
        """
        Sets the voltage at the DUT TUNE port. Returns the configured value.
        If the output is turned off, it doesn't necessarily return 0, as an internal
        voltage may be configured

        Parameters
        ----------
        value : float
            Sets the voltage at the DUT TUNE port. Returns the configured value.
            If the output is turned off, it doesn't necessarily return 0, as an internal
            voltage may be configured
        """
        self.write(":SOURce:TUNE:DUT:VOLT " + str(value))

    def set_dut_port_status(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/disables the DUT TUNE port. Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SOURce:TUNE:DUT:STAT " + valid_state)

    # =============================================================================
    # Set Phase Noise
    # =============================================================================

    def set_pnif_gain(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
            Range: 0-60
            Sets the IF gain for the measurement.

        Raises
        ------
        ValueError
            Error massage
        """
        if value > 60.0:
            raise ValueError("Unknown input! See function description for more info.")
        else:
            self.write(":SENSe:PN:IFGain " + str(value))

    def set_pn_start_freq(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
                    Unit HZ
                    Sets the start offset frequency.
        """
        self.write(":SENSe:PN:FREQuency:STARt " + str(value))

    def set_pn_stop_freq(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
            Unit HZ
            Sets the stop offset frequency.
        """
        self.write(":SENSe:PN:FREQuency:STOP " + str(value))

    # =============================================================================
    # Set Voltage controlled Oscillators
    # =============================================================================

    def set_vco_wait(self, state: str, value: float) -> str | None:
        """
        Parameters
        ----------
        state : str
            Can be ['ALL','NEXT']
        value : float
            This command requests a preliminary result during the measurement and blocks until
            the result is ready. The first parameter (required) specifies the target iteration
            to be saved. NEXT specifies the next possible iteration, ALL specifies the last
            iteration of the measurement (i.e. waits for the measurement to finish) and an
            integer specifies the specific iteration requested.The second parameter (optional)
            defines a timeout in milliseconds. If the command terminates without generating a
            preliminary result. It will produce an error. This error can be queried with
            SYST:ERR? or SYST:ERR:ALL?.
        """
        valid_state = self._check_scpi_param(state, ["ALL", "NEXT"])
        return self.query("CALCulate:VCO:WAIT " + valid_state + " " + str(value))

    def set_vco_test_freq(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/Disables the frequency parameter for the measurement.
            Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:FREQuency " + valid_state)

    def set_vco_test_noise(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/Disables the phase noise parameter for the measurement.
            Can be  ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:PNoise " + valid_state)

    def set_vco_test_power(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/Disables the power parameter for the measurement.
            Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:POWer " + valid_state)

    def set_vco_test_start(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
            Sets the start tuning voltage for the measurement.
            Unit V
        """
        self.write(":SENSe:VCO:VOLTage:STARt " + str(value))

    def set_vco_test_stop(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
            Sets the stop tuning voltage for the measurement.
            Units are in V.
        """
        self.write(":SENSe:VCO:VOLTage:STOP " + str(value))

    def set_vco_test_i_supply(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/disables the supply current parameter for the measurement.
            Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:ISUPply " + valid_state)

    def set_vcok_pu_shing(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/disables the pushing parameter for the measurement.
            Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:KPUShing " + valid_state)

    def set_vcokvco(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
           Enables/disables the tune sensitivity parameter for the measurement
           Can be ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:KVCO " + valid_state)

    def set_vcotype(self, typ: str) -> None:
        """
        Parameters
        ----------
        typ : str
            Select the DUT type for the measurement. Distinguish between slow (VCXO) and fast
            (VCO) tuning sensitivities. Can be ['VCO','VCXO']

        Raises
        ------
        ValueError
            Error massage
        """
        valid_typ = self._check_scpi_param(typ, ["VCO", "VCXO"])
        self.write(":SENSe:VCO:TYPE " + valid_typ)

    def set_vco_test_p_noise(self, state: str | int | float | bool) -> None:
        """
        Parameters
        ----------
        state : str | int | float | bool
            Enables/Disables the phase noise parameter for the measurement.
            Can be set to ['ON','OFF'] or [1,0] or [True,False].

        Raises
        ------
        ValueError
            Error massage
        """
        valid_state = self._parse_state(state)
        self.write(":SENSe:VCO:TEST:PNoise " + valid_state)

    def set_vco_test_pnoise_off_set(
        self, value1: float = 0, value2: float = 0, value3: float = 0, value4: float = 0
    ) -> None:
        """
        Sets up to 4 offset frequencies at which the phase noise is measured.
        At least 1 parameter is required. Blank parameters are set to 0
        (disabled). The query returns the set frequency for the specified
        offset. The offset can be specified with the <sel> parameter and can
        be chosen from 1|2|3|4

        Unit HZ

        Parameters
        ----------
        value1 : float
            freq val 1
        value2 : float
            freq val 2
        value3 : float
            freq val 3
        value4 : float
            freq val 4
        """
        self.write(
            ":SENSe:VCO:TEST:Pnoise:OFFSet "
            + str(value1)
            + ","
            + str(value2)
            + ","
            + str(value3)
            + ","
            + str(value4)
        )

    def set_vco_test_point(self, value: float) -> None:
        """
        Parameters
        ----------
        value : float
            Sets the number rof voltage points to use in the measurement
        """
        self.write(":SENSe:VCO:VOLTage:POINts " + str(value))

    # =============================================================================
    # Get Functions
    # =============================================================================

    # =============================================================================
    # Measurments Examples
    # =============================================================================

    def pn_meas_example(self, value):
        """
        This is a small example how to make a phase noise measurement.
        """

        self.set_sys_meas_mode("PN")  # select phase noise measurement
        self.init()  # start measurement
        self.set_calc_average("ALL")  # wait for the measurement to finish
        err = self.get_system_error()  # check if measurement was successful
        val = self.get_pn_spot(value)  # request spot noise value at 1MHz offset
        result_dict = {}
        result_dict["Error Value"] = err  # Write Error status if 0 no errors!
        result_dict["Spot Phase Noise @ " + str(value)] = val
        return result_dict

    def an_meas_example(self, value):
        """
        This is a small example how to make a phase noise measurement.
        """
        self.set_sys_meas_mode("AN")  # select amplitude noise measurement
        self.init()  # start measurement
        err = self.get_system_error()  # check if measurement was successful
        val = self.get_an_spot(value)  # request spot noise value at 1MHz offset
        result_dict = {}
        result_dict["Error Value"] = err  # Write Error status if 0 no errors!
        result_dict["Spot Amplitude Noise @ " + str(value)] = val
        return result_dict

    def fn_meas_example(self, value):
        """
        This is a small example how to make a frequency noise measurement.
        """
        self.set_sys_meas_mode("FN")  # select amplitude noise measurement
        self.init()  # start measurement
        err = self.get_system_error()  # check if measurement was successful
        val = self.get_fn_spot(value)  # request spot noise value at 1MHz offset
        result_dict = {}
        result_dict["Error Value"] = err  # Write Error status if 0 no errors!
        result_dict["Spot Frequency Noise @ " + str(value)] = val
        return result_dict

    def vco_meas_example(
        self,
        noise_offset_1,
        noise_offset_2,
        meas_points,
        tun_range_min,
        tun_range_max,
        supply_voltage,
        delay,
    ):
        """
        This is a small example how to make a Voltage controlled oscillator noise measurement.
        """

        # Config
        self.set_sys_meas_mode("VCO")  # Select VCO characterization
        self.set_vco_test_freq("ON")  # Enable frequency parameter
        self.set_vco_test_i_supply("ON")  # Enable supply current parameter
        self.set_vcok_pu_shing("ON")  # Enable pushing parameter
        self.set_vcokvco("ON")  # Enable Kvco parameter
        self.set_vco_test_p_noise("ON")  # Enable spot noise parameter
        self.set_vco_test_pnoise_off_set(
            noise_offset_1, noise_offset_2
        )  # Set two spot noise offsets: 1.2kHz, 100kHz
        self.set_vco_test_power("ON")  # Enable power parameter

        # Measurement
        self.set_vcotype("VCO")  # Set DUT Type (VCO or VCXO)
        self.set_vco_test_point(meas_points)  # Set 11 measurement points
        self.set_vco_test_start(tun_range_min)  # Set tuning range minimum to 0.5V
        self.set_vco_test_stop(tun_range_max)  # Set tuning range maximum to 10V
        self.set_dut_port_voltage(supply_voltage)  # Set supply voltage to 6V
        self.set_dut_port_status("ON")  # Enable supply voltage
        self.init()  # Start measurement

        # Loop
        self.set_vco_wait("ALL", delay)  # Wait for the measurement to finish
        err = self.get_system_error()  # Check if measurement was successful
        result_dict = {}

        # Read results
        result_dict["control voltage"] = (
            self.get_vco_trace_voltage()
        )  # request control voltage data array
        result_dict["frequency data"] = self.get_vco_trace_freq()  # Request frequency data array
        result_dict["Kvco data"] = self.get_vcokvco()  # Request Kvco data array
        result_dict["pushing data"] = self.get_vcok_pu_shing()  # Request pushing data array
        result_dict["supply current data"] = (
            self.get_vco_test_i_supply()
        )  # Request supply current data array
        result_dict["power level"] = self.get_vco_trace_power()  # Request power level data array
        result_dict["spot noise data array @offset #1 (1.2kHz)"] = self.get_vco_test_pnoise_off_set(
            1
        )  # Request spot noise data array @offset #1 (1.2kHz)
        result_dict["Error Value"] = err  # Write Error status if 0 no errors!


 