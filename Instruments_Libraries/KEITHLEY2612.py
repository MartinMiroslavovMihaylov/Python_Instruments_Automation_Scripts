# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 08:39:48 2021

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa
from time import sleep


class KEITHLEY2612:
    """
    This class is using pyvisa. Please install PyVisa before you use it.
    """

    def __init__(self, resource_str: str):
        """
        Connect to Device and print the Identification Number.
        """
        self._resource = visa.ResourceManager().open_resource(resource_str)
        idn = self.getIdn()
        # Verify this is a Keithley 2612
        if "2612" not in idn:
            print("Device may not be a Keithley 2612")
        else:
            print(idn)

        # Internal Variables
        self._ChannelLS = ["a", "b"]
        self._Measurement_Types = {
            "voltage": "v",
            "volt": "v",
            "v": "v",
            "current": "i",
            "amp": "i",
            "i": "i",
            "power": "p",
            "watt": "p",
            "p": "p",
            "resistance": "r",
            "ohm": "r",
            "r": "r",
        }

        # Voltage and current limits for safety
        self._absolute_Voltage_Limits = {"min": 20e-3, "max": 200}
        self._Voltage_Limits = {"min": 20e-3, "max": 10}
        self._Current_Limits = {"min": 10e-9, "max": 3}

    def query(self, message):
        return self._resource.query(message)

    def write(self, message):
        return self._resource.write(message)

    def Close(self):
        self._resource.close()
        print("Instrument Keithley Instruments Inc., Model 2612, 1152698, 1.4.2 is closed!")

    def getIdn(self):
        """

        Returns
        -------
        str
            Instrument identification

        """
        return str(self.query("*IDN?")).strip()

    # =============================================================================
    # Checks and Validations
    # =============================================================================

    def _validate_channel(self, channel: str) -> str:
        """Validate and normalize channel input"""
        channel = channel.lower().strip()
        if channel not in self._ChannelLS:
            raise ValueError(f"Invalid channel '{channel}'. Must be one of: {self._ChannelLS}")
        return channel

    def _validate_state(self, state: int | str, output: bool = False) -> str:
        """Validate and normalize state input"""
        # The Output can also be set to High-Z
        if output:
            state_mapping = {
                "on": "ON",
                "off": "OFF",
                "high_z": "HIGH_Z",
                1: "ON",
                0: "OFF",
                2: "HIGH_Z",
                "1": "ON",
                "0": "OFF",
                "2": "HIGH_Z",
                True: "ON",
                False: "OFF",
            }
        else:
            state_mapping = {
                "on": "ON",
                "off": "OFF",
                1: "ON",
                0: "OFF",
                "1": "ON",
                "0": "OFF",
                True: "ON",
                False: "OFF",
            }

        normalized = state_mapping.get(
            state if isinstance(state, (int, bool)) else str(state).lower()
        )
        if normalized is None:
            raise ValueError(f"Invalid state '{state}'. Valid options: on/off/high_z or 1/0/2")
        return normalized

    def _format_scientific(self, value: int | float, precision: int = 4) -> str:
        """Format number in scientific notation consistently"""
        return f"{float(value):.{precision}e}"

    # =============================================================================
    # Reset and Clear
    # =============================================================================

    def Reset(self, channel: str) -> None:
        """Reset channel to default settings

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        self.write(f"smu{channel}.reset()")

    def clear(self):
        self.write("*CLS")

    def clear_error_queue(self):
        self.write("errorqueue.clear()")

    # =============================================================================
    # Measurement/ASK Methods
    # =============================================================================

    def ask_Current(self, channel: str) -> float:
        """Performs one current measurements and returns the value.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.i())"))

    def ask_Voltage(self, channel: str) -> float:
        """This function performs one voltage measurements and returns the value.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.v())"))

    def ask_Power(self, channel: str) -> float:
        """This function performs one power measurements and returns the value.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.p())"))

    def ask_Resistance(self, channel: str) -> float:
        """This function performs one resistance measurements and returns the value.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.r())"))

    def read_Measurement(self, channel: str, type: str) -> float:
        """This function performs one measurements and returns the value.

        Parameters
        ----------
        channel : str
            Select channel A or B
        type : str
            Select measurement type:
            'volt', 'amp', 'ohm', or 'watt'.

        """
        channel = self._validate_channel(channel)
        meas_type = self._Measurement_Types.get(type.lower())
        if meas_type is None:
            raise ValueError("Unknown input! See function description for more info.")

        return float(self.query(f"print(smu{channel}.measure.{meas_type}())"))

    def ask_VoltageRangeMeasure(self, channel: str) -> float:
        """This attribute contains the smuX.measure.rangeY voltage setting. Look up the datasheet!

        If the source function is the same as the measurement function (for example, sourcing voltage and measuring
        voltage), the measurement range is locked to be the same as the source range. However, the setting for the
        measure range is retained. If the source function is changed (for example, from sourcing voltage to sourcing
        current), the retained measurement range will be used.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.rangev)"))

    def ask_CurrentRangeMeasure(self, channel: str) -> float:
        """This attribute contains the smuX.measure.rangeY current setting. Look up the datasheet!

        If the source function is the same as the measurement function (for example, sourcing voltage and measuring
        voltage), the measurement range is locked to be the same as the source range. However, the setting for the
        measure range is retained. If the source function is changed (for example, from sourcing voltage to sourcing
        current), the retained measurement range will be used.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.measure.rangei)"))

    def ask_AutoVoltageRangeMeasure(self, channel: str) -> int:
        """This attribute contains the smuX.measure.autorangeY voltage setting.
        You might want to keep it on auto i.e. 1 or "ON"!

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return int(float(self.query(f"print(smu{channel}.measure.autorangev)")))

    def ask_AutoCurrentRangeMeasure(self, channel: str) -> int:
        """This attribute contains the smuX.measure.autorangeY current setting.
        You might want to keep it on auto i.e. 1 or "ON"!

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return int(float(self.query(f"print(smu{channel}.measure.autorangei)")))

    # =============================================================================
    # Source/ASK Methods
    # =============================================================================

    def ask_LimitReached(self, channel: str) -> bool:
        """This attribute contains the state of source compliance.
        A configured limit has been reached. (voltage, current, or power limit)

        Parameters
        ----------
        channel : str
            Select channel A or B
            This output indicates that a configured limit has been reached.
            (voltage, current, or power limit)

        """
        channel = self._validate_channel(channel)
        response = self.query(f"print(smu{channel}.source.compliance)").strip().lower()
        return True if response == "true" else False

    def ask_AutoVoltageRange(self, channel: str) -> int:
        """This attribute contains the state of (smuX.source.autorangeY) the source autorange
        voltage control. You might want to keep it on auto i.e. 1 or "ON"!

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return int(float(self.query(f"print(smu{channel}.source.autorangev)").strip()))

    def ask_AutoCurrentRange(self, channel: str) -> int:
        """This attribute contains the state of (smuX.source.autorangeY) the source autorange
        current control. You might want to keep it on auto i.e. 1 or "ON"!

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return int(float(self.query(f"print(smu{channel}.source.autorangei)").strip()))

    def ask_VoltageRange(self, channel: str) -> float:
        """This attribute contains the source voltage range.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.rangev)").strip())

    def ask_CurrentRange(self, channel: str) -> float:
        """This attribute contains the source current range.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.rangei)").strip())

    def ask_VoltageLimit(self, channel: str) -> float:
        """This attribute contains the source voltage limit.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.levelv)").strip())

    def ask_CurrentLimit(self, channel: str) -> float:
        """This attribute contains the source current limit.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.leveli)").strip())

    def ask_VoltageSetting(self, channel: str) -> float:
        """This attribute contains the source voltage setting.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.levelv)").strip())

    def ask_CurrentSetting(self, channel: int) -> float:
        """This attribute contains the source current setting.

        Parameters
        ----------
        channel : str
            Select channel A or B

        """
        channel = self._validate_channel(channel)
        return float(self.query(f"print(smu{channel}.source.leveli)").strip())

    def ask_OutputSourceFunction(self, channel: int) -> str:
        """This attribute contains the source output function.
        Returns: 1 = voltage, 0 = current

        Parameters
        ----------
        channel : str
            Select channel A or B

        Returns
        -------
        int
            1 = voltage, 0 = current

        """
        channel = self._validate_channel(channel)
        if int(float(self.query(f"print(smu{channel}.source.func)").strip())) == 1:
            return "voltage"
        elif int(float(self.query(f"print(smu{channel}.source.func)").strip())) == 0:
            return "current"
        
    # =============================================================================
    # Further ASK Methods
    # =============================================================================

    def ask_readBuffer(self, channel, start, stop):
        """TODO: This function should be checked. Also is doesn't return anything at the moment.
        Print the source function used for 'start' - 'stop' readings stored in source-measure unit (SMU)
        channel A, buffer 1.

        Parameters
        ----------
        channel : str
            Select channel A or B
        start : int
            select start value
        stop : int
            select stop value

        """
        channel = self._validate_channel(channel)
        if channel in self._ChannelLS:
            self.query(f"printbuffer({str(start)},{str(stop)},smu{str(channel)})")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # =============================================================================
    # Source/SET Methods
    # =============================================================================

    def set_SourceOutput(self, channel: str, state: int | str | bool) -> None:
        """This attribute sets source output state (on or off)

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
            Set source output (channel A/B) ON or OFF

        """
        # Normalize channel and state inputs
        channel = self._validate_channel(channel)
        state_normalized = self._validate_state(state, output=True)
        self.write(f"smu{channel}.source.output = smu{channel}.OUTPUT_{state_normalized}")

    def set_Out(self, channel: str, state: int | str | bool) -> None:
        """Alias for set_SourceOutput()."""
        self.set_SourceOutput(channel, state)

    def set_MeasOutput(self, channel: str, state: int | str | bool) -> None:
        """Alias for set_SourceOutput()."""
        self.set_SourceOutput(channel, state)

    def set_AutoVoltageRange(self, channel: str, state: int | str | bool) -> None:
        """This attribute contains the state of the source autorange control (on/off).

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
           ON/OFF voltage source automatic range

        """
        channel = self._validate_channel(channel)
        state_normalized = self._validate_state(state)
        self.write(f"smu{channel}.source.autorangev = smu{channel}.AUTORANGE_{state_normalized}")

    def set_AutoCurrentRange(self, channel: str, state: int | str | bool) -> None:
        """This attribute contains the state of the source autorange control (on/off).

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
           ON/OFF current source automatic range

        """
        channel = self._validate_channel(channel)
        state_normalized = self._validate_state(state)
        self.write(f"smu{channel}.source.autorangei = smu{channel}.AUTORANGE_{state_normalized}")

    def set_VoltageRange(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value
            of the source range for voltage.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set voltage source voltage range

        """
        channel = self._validate_channel(channel)
        value = self._format_scientific(value=value, precision=0)
        self.write(f"smu{channel}.source.rangev = {value}")

    def set_CurrentRange(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value
            of the source range for current

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set current source current range

        """
        channel = self._validate_channel(channel)
        value = self._format_scientific(value=value, precision=0)
        self.write(f"smu{channel}.source.rangei = {value}")

    def set_VoltageLimit(self, channel: str, limit: int | float, highVoltage: bool = False) -> None:
        """Sets voltage source compliance. Use to limit the voltage output
        when in the current source mode. This attribute should be set in the
        test sequence before turning the source on.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Sets the voltage limit of channel X to V. Using a limit value of 0
            will result in a "Parameter Too Small" error message (error 1102)

        """
        channel = self._validate_channel(channel)
        if highVoltage:  # You want more than 10V
            if not (
                self._absolute_Voltage_Limits["min"] <= limit <= self._absolute_Voltage_Limits["max"]
            ):
                raise ValueError(
                    f"Voltage limit must be between {self._absolute_Voltage_Limits['min']} and {self._absolute_Voltage_Limits['max']} V"
                )
        else:  # You want less than 10V
            if not (self._Voltage_Limits["min"] <= limit <= self._Voltage_Limits["max"]):
                raise ValueError(
                    f"""Voltage limit must be between {self._Voltage_Limits['min']} and {self._Voltage_Limits['max']} V.
                    If you want more than 10V, use highVoltage = True. Up to 200V is possible."""
                )

        limit_str = self._format_scientific(value=limit, precision=4)
        self.write(f"smu{channel}.source.limitv = {limit_str}")

    def set_CurrentLimit(self, channel: str, limit: int | float) -> None:
        """Sets current source compliance. Use to limit the current output
        when in the voltage source mode. This attribute should be set in the
        test sequence before turning the source on.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Sets the current limit of channel X to A. Using a limit value of 0
            will result in a "Parameter Too Small" error message (error 1102)

        """
        channel = self._validate_channel(channel)
        if not (self._Current_Limits["min"] < limit < self._Current_Limits["max"]):
            raise ValueError(
                f"Current limit must be between {self._Current_Limits['min']} and {self._Current_Limits['max']} A"
            )

        limit_str = self._format_scientific(value=limit, precision=4)
        self.write(f"smu{channel}.source.limiti = {limit_str}")

    def set_Voltage(self, channel: str, voltage: int | float, highVoltage: bool = False) -> None:
        """This attribute sets the source level voltage.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        voltage : int/float
            Set voltage on channels A and B

        """
        channel = self._validate_channel(channel)
        if highVoltage:  # You want more than 10V
            if not (
                self._absolute_Voltage_Limits["min"]
                <= voltage
                <= self._absolute_Voltage_Limits["max"]
            ):
                raise ValueError(
                    f"Voltage limit must be between {self._absolute_Voltage_Limits['min']} and {self._absolute_Voltage_Limits['max']} V"
                )
        else:  # You want less than 10V
            if not (self._Voltage_Limits["min"] <= voltage <= self._Voltage_Limits["max"]):
                raise ValueError(
                    f"""Voltage limit must be between {self._Voltage_Limits['min']} and {self._Voltage_Limits['max']} V.
                    If you want more than 10V, use highVoltage = True. Up to 200V is possible."""
                )

        voltage_str = self._format_scientific(value=voltage, precision=4)
        self.write(f"smu{channel}.source.levelv = {voltage_str}")

    def set_Current(self, channel: str, current: int | float) -> None:
        """This attribute sets the source level current.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        current : int/float
            Set Current on channels A and B

        """
        channel = self._validate_channel(channel)
        if not (self._Current_Limits["min"] < current < self._Current_Limits["max"]):
            raise ValueError(
                f"Current must be between {self._Current_Limits['min']} and {self._Current_Limits['max']} A"
            )
        current_str = self._format_scientific(value=current, precision=4)
        self.write(f"smu{channel}.source.leveli = {current_str}")

    def set_OutputSourceFunction(self, channel: str, function: str) -> None:
        """This attribute sets the source function (V source or I source).

        Parameters
        ----------
        channel : str
            Select channel A or B
        function : str
            The source function. Set to one of the following values:
            function = 'volt' Selects voltage source function
            function = 'amp'  Selects current source function

        """
        channel = self._validate_channel(channel)
        function = function.lower()

        if function in ["volt", "voltage"]:
            self.write(f"smu{channel}.source.func = smu{channel}.OUTPUT_DCVOLTS")
        elif function in ["amp", "current"]:
            self.write(f"smu{channel}.source.func = smu{channel}.OUTPUT_DCAMPS")
        else:
            raise ValueError("Function must be 'volt'/'voltage' or 'amp'/'current'")

    def set_PulseMeasured(
        self, channel: str, value: int | float, ton: int | float, toff: int | float
    ) -> None:
        """
        TODO: function should be checked

        Parameters
        ----------
        channel : str
            Select channel A or B
        value : int/float or list with curly braces for example {1,2,3....}.
        ton : int/float
             X ms pulse on
        toff : int/float
            X ms pulse off

        """

        channel = self._validate_channel(channel)
        if channel in self._ChannelLS:
            self.write(f"ConfigPulseIMeasureV(smu{channel},{str(value)},{str(ton)},{str(toff)})")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_offmode(self, channel: str, mode: int | str) -> None:
        """This attribute sets the source output-off mode

        Parameters
        ----------
        channel : str
            Channel A or B
        mode : int | str
            0 or NORMAL: Configures the source function according to
                smuX.source.offfunc attribute
            1 or ZERO: Configures source to output 0 V
            2 or HIGH_Z: Opens the output relay when the output is turned off

        """
        channel = self._validate_channel(channel)

        mode_mapping = {
            0: "NORMAL",
            1: "ZERO",
            2: "HIGH_Z",
            "normal": "NORMAL",
            "zero": "ZERO",
            "high_z": "HIGH_Z",
        }

        mode_normalized = mode_mapping.get(mode if isinstance(mode, int) else str(mode).lower())
        if mode_normalized is None:
            raise ValueError("Mode must be 0/1/2 or 'normal'/'zero'/'high_z'")

        self.write(f"smu{channel}.source.offmode = smu{channel}.OUTPUT_{mode_normalized}")

    # =============================================================================
    # Measure/SET Methods
    # =============================================================================

    def set_VoltageRangeMeasure(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value of the measure range for voltage.
        Look up the datasheet! -> smuX.measure.rangeY.  You might want to keep it on auto!

        If the source function is the same as the measurement function (for example, sourcing voltage and measuring
        voltage), the measurement range is locked to be the same as the source range. However, the setting for the
        measure range is retained. If the source function is changed (for example, from sourcing voltage to sourcing
        current), the retained measurement range will be used.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set measure voltage range

        """
        channel = self._validate_channel(channel)
        value = self._format_scientific(value=value, precision=0)
        self.write(f"smu{channel}.measure.rangev = {value}")

    def set_CurrentRangeMeasure(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value of the measure range for current.
        Look up the datasheet! -> smuX.measure.rangeY.  You might want to keep it on auto!

        If the source function is the same as the measurement function (for example, sourcing voltage and measuring
        voltage), the measurement range is locked to be the same as the source range. However, the setting for the
        measure range is retained. If the source function is changed (for example, from sourcing voltage to sourcing
        current), the retained measurement range will be used.

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set current measure range

        """
        channel = self._validate_channel(channel)
        value = self._format_scientific(value=value, precision=0)
        self.write(f"smu{channel}.measure.rangei = {value}")

    def set_MeasurementRange(
        self, channel: str, measurement_type: str, range_value: int | float
    ) -> None:
        """This attribute contains the positive full-scale value of the measure range for voltage orcurrent.
        Look up the datasheet! -> smuX.measure.rangeY.  You might want to keep it on auto!
        Same as set_CurrentRangeMeasure and set_VoltageRangeMeasure.

        If the source function is the same as the measurement function (for example, sourcing voltage and measuring
        voltage), the measurement range is locked to be the same as the source range. However, the setting for the
        measure range is retained. If the source function is changed (for example, from sourcing voltage to sourcing
        current), the retained measurement range will be used.

        Parameters
        ----------
        channel : str
            Select channel A or B
        measurement_type : str
            Selects the measurement function:
            'volt' or 'amp'.
        range_value : int/float
            Set to the maximum expected voltage or current to be measured.

        """
        channel = self._validate_channel(channel)
        measurement_type = measurement_type.lower()

        range_str = self._format_scientific(range_value, precision=0)

        if measurement_type in ["volt", "voltage"]:
            self.write(f"smu{channel}.measure.rangev = {range_str}")
        elif measurement_type in ["amp", "current"]:
            self.write(f"smu{channel}.measure.rangei = {range_str}")
        else:
            raise ValueError("Measurement type must be 'volt'/'voltage' or 'amp'/'current'")

    # =============================================================================
    # Display Control
    # =============================================================================

    def set_ChannelDisplay(self, channel: str | None = None) -> None:
        """Set which channel(s) to display.

        Parameters
        ----------
        channel : str | None
            Select channel A or B. If None, displays SMU A and SMU B.

        """

        if channel is None:
            self.write("display.screen = display.SMUA_SMUB")
        else:
            channel = self._validate_channel(channel)
            self.write(f"display.screen = display.SMU{channel.upper()}")

    def set_DisplayMeasurementFunction(self, channel: str, measurement_type: str) -> None:
        """This attribute specifies the type of measurement being displayed.

        Parameters
        ----------
        channel : str
            Select channel A or B
        measurement_type : str
            Selects the displayed measurement function:
            volt, amp, ohm, or watt.
            SMU A and SMU B can be set for different measurement functions!

        """
        channel = self._validate_channel(channel)
        measurement_type = self._Measurement_Types.get(measurement_type.lower())

        display_mapping = {
            "v": "_DCVOLTS",
            "i": "_DCAMPS",
            "r": "_OHMS",
            "p": "_WATTS",
        }

        display_func = display_mapping.get(measurement_type)
        if display_func is None:
            raise ValueError(
                f"Invalid measurement type. Valid options: {list(display_mapping.keys())}"
            )

        self.write(f"display.smu{channel}.measure.func = display.MEASURE{display_func}")

    # =============================================================================
    # Get/Save Data
    # =============================================================================
    def get_Data(self, channel: str | None = None) -> dict:
        """Get voltage and current measurements.

        Parameters
        ----------
        channel : str
            Select channel A or B
            If no channel is selected, all channels are measured.

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured voltage and current.

        """
        if channel is None:
            voltages = []
            currents = []
            for channel in self._ChannelLS:
                voltages.append(self.ask_Voltage(channel))
                currents.append(self.ask_Current(channel))
            return {
                "voltage_V": voltages,
                "current_A": currents,
                "channels": [channel.upper() for channel in self._ChannelLS],
            }
        else:
            channel = self._validate_channel(channel)
            currents = self.ask_Current(channel)
            voltages = self.ask_Voltage(channel)
            return {
                "voltage_V": self.ask_Voltage(channel),
                "current_A": self.ask_Current(channel),
                "channel": channel.upper(),
            }

    # =============================================================================
    # Convenience Methods
    # =============================================================================

    def setup_voltage_source(self, channel: str, voltage: float, current_limit: float) -> None:
        """Convenience method to setup voltage source with current limit"""
        channel = self._validate_channel(channel)

        self.set_ChannelDisplay(channel)
        self.set_OutputSourceFunction(channel, "voltage")
        self.set_DisplayMeasurementFunction(channel, "current")
        self.set_Voltage(channel, voltage)
        self.set_CurrentLimit(channel, current_limit)

    def setup_current_source(self, channel: str, current: float, voltage_limit: float) -> None:
        """Convenience method to setup current source with voltage limit"""
        channel = self._validate_channel(channel)

        self.set_ChannelDisplay(channel)
        self.set_OutputSourceFunction(channel, "current")
        self.set_DisplayMeasurementFunction(channel, "voltage")
        self.set_Current(channel, current)
        self.set_VoltageLimit(channel, voltage_limit)
