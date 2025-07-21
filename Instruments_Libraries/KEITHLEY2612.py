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

    def __init__(self, resource_str):
        """
        Connect to Device and print the Identification Number.
        """
        self._resource = visa.ResourceManager().open_resource(resource_str)
        print(self._resource.query("*IDN?").strip())

        # Internal Variables
        self._chList = ["a", "b"]

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
    # Reset to Default
    # =============================================================================

    def Reset(self, channel):
        """


        Parameters
        ----------
        channel : str
            Select Channel A or B and restore to default channel settings.

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            self.write("smu" + str(channel) + ".reset()")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def clear(self):
        self.write("*CLS")

    def clear_eror_queue(self):
        self.write("errorqueue.clear()")

    # =============================================================================
    # ASK
    # =============================================================================

    def ask_LimitReached(self, channel: str) -> bool:
        """This attribute contains the state of source compliance.


        Parameters
        ----------
        channel : str
            This output indicates that a configured limit has been reached.
            (voltage, current, or power limit)

        Returns
        -------
        bool
            DESCRIPTION.

        """

        channel = channel.lower()
        if channel in self._chList:
            v = self.query("print(smu" + str(channel) + ".source.compliance)").strip().lower()
            return True if v == "true" else False

    def ask_Current(self, channel: str) -> float:
        """Performs one current measurements and returns the value.


        Parameters
        ----------
        channel : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Return float with the measured current value on the channel.

        """

        channel = channel.lower()
        if channel in self._chList:
            return float(self.query("print(smu" + str(channel) + ".measure.i())"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def ask_Voltage(self, channel: str) -> float:
        """This function performs one voltage measurements and returns the value.


        Parameters
        ----------
        channel : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        float
            Return float with the measured voltage value on the channel.

        """

        channel = channel.lower()
        if channel in self._chList:
            return float(self.query("print(smu" + str(channel) + ".measure.v())"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def ask_Power(self, channel: str) -> float:
        """This function performs one power measurements and returns the value.


        Parameters
        ----------
        channel : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        float
            Return float with the measured power value on the channel.

        """

        channel = channel.lower()
        if channel in self._chList:
            return float(self.query("print(smu" + str(channel) + ".measure.p())"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def ask_Resistance(self, channel: str) -> float:
        """This function performs one resistance measurements and returns the value.


        Parameters
        ----------
        channel : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        float
            Return float with the measured resistance value on the channel.

        """

        channel = channel.lower()
        if channel in self._chList:
            return print(self.query("print(smu" + str(channel) + ".measure.r())"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def read_Measurement(self, channel: str, type: str) -> float:
        """This function performs one measurements and returns the value.


        Parameters
        ----------
        channel : str
            Select channel A or B
        type : str
            Select measurement type:
            'volt', 'amp', 'ohm', or 'watt'.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Return float with the measured value on the channel.

        """

        channel = channel.lower()
        type_mapping = {
            "voltage": "v",
            "volt": "v",
            "current": "i",
            "amp": "i",
            "power": "p",
            "watt": "p",
            "resistance": "r",
            "ohm": "r",
        }
        type = type_mapping.get(type.lower() if isinstance(type, str) else type)
        if channel in self._chList and type is not None:
            return float(self.query("print(smu" + str(channel) + ".measure." + str(type) + "())"))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def ask_readBuffer(self, channel, start, stop):
        """TODO: This function should be checked. Also is doesn't return anything at the moment.


        Parameters
        ----------
        channel : str
            Select channel A or B
        start : int
            select start value
        stop : int
            select stop value

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Print the source function used
        for 'start' - 'stop' readings stored in
        source-measure unit (SMU)
        channel A, buffer 1.

        """

        channel = channel.lower()
        if channel in self._chList:
            self.query("printbuffer(" + str(start) + "," + str(stop) + ",smu" + str(channel) + ")")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # =============================================================================
    # SET
    # =============================================================================

    def set_SourceOutput(self, channel: str, state: int | str) -> None:
        """This attribute sets source output state (on or off)

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
            Set source output (channel A/B) ON or OFF

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """
        # Normalize channel and state inputs
        channel = channel.lower()
        state_mapping = {
            "on": "ON",
            "off": "OFF",
            1: "ON",
            0: "OFF",
            2: "HIGH_Z",
            "1": "ON",
            "0": "OFF",
        }
        state_normalized = state_mapping.get(state if isinstance(state, int) else state.lower())

        # Validate inputs
        if channel in self._chList and state_normalized is not None:
            self.write(
                "smu"
                + str(channel)
                + ".source.output = smu"
                + str(channel)
                + ".OUTPUT_"
                + str(state_normalized)
            )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_Out(self, channel: str, state: int | str) -> None:
        """Alias for set_SourceOutput()."""
        self.set_SourceOutput(channel, state)

    def set_MeasOutput(self, channel: str, state: int | str) -> None:
        """Alias for set_SourceOutput()."""
        self.set_SourceOutput(channel, state)

    def set_AutoVoltageRange(self, channel: str, state: int | str) -> None:
        """This attribute contains the state of the source autorange control (on/off).

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
           ON/OFF voltage source automatic range

        Raises
        ------
        ValueError
           Error message

        Returns
        -------
        None.

        """
        # Normalize channel and state inputs
        channel = channel.lower()
        state_mapping = {"on": "ON", "off": "OFF", 1: "ON", 0: "OFF", "1": "ON", "0": "OFF"}
        state_normalized = state_mapping.get(state if isinstance(state, int) else state.lower())

        # Validate inputs
        if channel in self._chList and state_normalized is not None:
            self.write(
                "smu"
                + str(channel)
                + ".source.autorangev = smu"
                + str(channel)
                + ".AUTORANGE_"
                + str(state_normalized)
            )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_AutoCurrentRange(self, channel: str, state: int | str) -> None:
        """This attribute contains the state of the source autorange control (on/off).

        Parameters
        ----------
        channel : str
            Select channel A or B
        state : str
           ON/OFF current source automatic range

        Raises
        ------
        ValueError
           Error message

        Returns
        -------
        None.

        """
        # Normalize channel and state inputs
        channel = channel.lower()
        state_mapping = {"on": "ON", "off": "OFF", 1: "ON", 0: "OFF", "1": "ON", "0": "OFF"}
        state_normalized = state_mapping.get(state if isinstance(state, int) else state.lower())

        # Validate inputs
        if channel in self._chList and state_normalized is not None:
            self.write(
                "smu"
                + str(channel)
                + ".source.autorangei = smu"
                + str(channel)
                + ".AUTORANGE_"
                + str(state_normalized)
            )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_VoltageRange(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value
            of the measure range for voltage

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set voltage source voltage limit

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            value = "{:.0e}".format(value)
            self.write("smu" + str(channel) + ".measure.rangev = " + value)
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_CurrentRange(self, channel: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value
            of the measure range for current

        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set current source voltage limit

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            value = "{:.0e}".format(value)
            self.write("smu" + str(channel) + ".measure.rangei = " + str(value))

        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_VoltageLimit(self, channel: str, value: int | float) -> None:
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

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList and 20e-3 < value < 200:
            value = "{:.4e}".format(value)
            self.write("smu" + str(channel) + ".source.limitv = " + str(value))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_CurrentLimit(self, channel: str, value: int | float) -> None:
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

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList and 10e-9 < value < 3:
            value = "{:.4e}".format(value)
            self.write("smu" + str(channel) + ".source.limiti = " + str(value))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_Voltage(self, channel: str, value: int | float) -> None:
        """This attribute sets the source level voltage.


        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set voltage on channels A and B

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            value = "{:.4e}".format(value)
            self.write("smu" + str(channel) + ".source.levelv = " + str(value))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_Current(self, channel: str, value: int | float) -> None:
        """This attribute sets the source level current.


        Parameters
        ----------
        channel : str
            Select Channel A or B
        value : int/float
            Set Current on channels A and B

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            value = "{:.4e}".format(value)
            self.write("smu" + str(channel) + ".source.leveli = " + str(value))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_ChannelDisplay(self, channel: str | None = None) -> None:
        """


        Parameters
        ----------
        channel : str | None
            Select channel A or B. If None, displays SMU A and SMU B.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        if channel is None:
            self.write("display.screen = display.SMUA_SMUB")
        else:
            channel = channel.lower()
            if channel in self._chList:
                self.write("display.screen = display.SMU" + str(channel.upper()))
            else:
                raise ValueError("Unknown input! See function description for more info.")

    def set_OutputSourceFunction(self, channel: str, type: str) -> None:
        """This attribute sets the source function (V source or I source).


        Parameters
        ----------
        channel : str
            Select channel A or B
        type : str
            The source function. Set to one of the following values:
            type = 'volt' Selects voltage source function
            type = 'amp'  Selects current source function

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        type = type.lower()
        tList = ["volt", "amp"]
        if channel in self._chList and type in tList:
            if type == "volt":
                self.write(
                    "smu" + str(channel) + ".source.func = smu" + str(channel) + ".OUTPUT_DCVOLTS"
                )
            elif type == "amp":
                self.write(
                    "smu" + str(channel) + ".source.func = smu" + str(channel) + ".OUTPUT_DCAMPS"
                )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_DisplayMeasurementFunction(self, channel: str, type: str) -> None:
        """This attribute specifies the type of measurement being displayed.


        Parameters
        ----------
        channel : str
            Select channel A or B
        type : str
            Selects the displayed measurement function:
            volt, amp, ohm, or watt.
            SMU A and SMU B can be set for different measurement functions!

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        type = type.lower()
        tList = ["volt", "amp", "ohm", "watt"]
        if channel in self._chList and type in tList:
            if type == "volt":
                self.write("display.smu" + str(channel) + ".measure.func = display.MEASURE_DCVOLTS")
            elif type == "amp":
                self.write("display.smu" + str(channel) + ".measure.func = display.MEASURE_DCAMPS")
            elif type == "ohm":
                self.write("display.smu" + str(channel) + ".measure.func = display.MEASURE_OHMS")
            elif type == "watt":
                self.write("display.smu" + str(channel) + ".measure.func = display.MEASURE_WATTS")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_MeasurementRange(self, channel: str, type: str, value: int | float) -> None:
        """This attribute contains the positive full-scale value of the measure range for voltage or current.
        Same as set_CurrentRange and set_VoltageRange.

        Parameters
        ----------
        channel : str
            Select channel A or B
        type : str
            Selects the measurement function:
            'volt' or 'amp'.
            SMU A and SMU B can be set for different measurement functions!
        value : int/float
            Set to the maximum expected voltage or current to be measured.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        type = type.lower()
        value = "{:.0e}".format(value)
        tList = ["volt", "amp"]
        if channel in self._chList and type in tList:
            if type == "volt":
                self.write("smu" + str(channel) + ".measure.rangev = " + str(float(value)))
            elif type == "amp":
                self.write("smu" + str(channel) + ".measure.rangei = " + str(float(value)))
            else:
                raise ValueError("Unknown input! See function description for more info.")
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_PulseMeasured(
        self, channel: str, value: int | float, ton: int | float, toff: int | float
    ) -> None:
        """

        Parameters
        ----------
        channel : str
            Select channel A or B
        value : int/float or list with curly braces for example {1,2,3....}.
        ton : int/float
             X ms pulse on
        toff : int/float
            X ms pulse off

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        """

        channel = channel.lower()
        if channel in self._chList:
            self.write(
                "ConfigPulseIMeasureV(smu"
                + str(channel)
                + ","
                + str(value)
                + ","
                + str(ton)
                + ","
                + str(toff)
                + ")"
            )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_offmode(self, channel: str, type: int | str) -> None:
        """This attribute sets the source output-off mode

        Parameters
        ----------
        channel : str
            Channel A or B
        type : int | str
            0 or NORMAL: Configures the source function according to
                smuX.source.offfunc attribute
            1 or ZERO: Configures source to output 0 V
            2 or HIGH_Z: Opens the output relay when the output is turned off

        Raises
        ------
        ValueError
            Channel not in Channel list or Type not in Type list
        """
        # Normalize channel and state inputs
        channel = channel.lower()
        type_mapping = {0: "NORMAL", 1: "ZERO", 2: "HIGH_Z", "normal": "NORMAL", "zero": "ZERO"}
        type_normalized = type_mapping.get(type if isinstance(type, int) else type.lower())

        # Validate inputs
        if channel in self._chList and type_normalized is not None:
            self.write(
                "smu"
                + str(channel)
                + ".source.offmode = smu"
                + str(channel)
                + ".OUTPUT_"
                + str(type_normalized)
            )
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # =============================================================================
    # Get/Save Data
    # =============================================================================
    def get_Data(self, channel: str | None = None) -> dict:
        """


        Parameters
        ----------
        channel : str
            Select channel A or B
            If no channel is selected, all channels are measured

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured voltage and current.

        """
        if channel is None:
            Current = []
            Voltage = []
            for channel in self._chList:
                Current.append(self.ask_Current(channel))
                Voltage.append(self.ask_Voltage(channel))
            OutPut = {}
            OutPut["Voltage/V"] = Voltage
            OutPut["Current/A"] = Current
        else:
            channel = channel.lower()
            Current = self.ask_Current(channel)
            Voltage = self.ask_Voltage(channel)
            OutPut = {}
            OutPut["Voltage/V"] = Voltage
            OutPut["Current/A"] = Current

        return OutPut
