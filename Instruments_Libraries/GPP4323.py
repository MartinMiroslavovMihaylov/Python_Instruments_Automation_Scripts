# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:55:01 2023

@author: Martin.Mihaylov
"""


import serial
import time
import numpy as np

print(
    """
#####################################################################################
    To use the DC-Power Supply GW-Instek GPP4323 you need to install the USB Driver 
    from https://www.gwinstek.com/en-global/download/ - GPP USB Driver 
    Python Library needed: pip install pyserial
#####################################################################################
"""
)


class GPP4323:
    def __init__(self, resource_str):
        """
        This class is using python serial, time and io libraries. Please be sure to install pyserial.
        Connect to Device and print the Identification Number.
        """
        self._resource = serial.Serial(
            resource_str,
            baudrate=115200,
            bytesize=8,
            timeout=1,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            xonxoff=False,
        )

        self.eol_char = "\n"
        self.timeout = 0.2
        # Predefined Lists
        self._define_lists()
        print(self.getIdn())

    def write(self, message):
        self._resource.write((message + self.eol_char).encode("utf-8"))

    def query_values(self, message):
        self._resource.write((message + self.eol_char).encode("utf-8"))
        time.sleep(self.timeout)
        data = self._resource.read_until().decode("utf-8").strip()
        return data

    def Close(self):
        print("Instrument GPP4323 is closed!")
        return self._resource.close()

    def reset(self):
        self.write("*RST")

    def getIdn(self) -> str:
        """Returns the Instrument Identification: GW Instek,GPP-4323"""
        return self.query_values("*IDN?")

    # =============================================================================
    # Checks and Validations
    # =============================================================================

    def _define_lists(self):
        # Predefined Lists
        self._ChannelLS = [1, 2, 3, 4]
        self._mainChannelLS = [1, 2]
        self._StateLS_mapping = {
            "on": "ON",
            "off": "OFF",
            1: "ON",
            0: "OFF",
            "1": "ON",
            "0": "OFF",
            True: "ON",
            False: "OFF",
        }
        self._measurement_type_mapping = {
            "voltage": "Voltage",
            "volt": "Voltage",
            "v": "Voltage",
            "current": "Current",
            "amp": "Current",
            "a": "Current",
            "power": "Power",
            "watt": "Power",
            "p": "Power",
        }

    def _validate_channel(self, channel: int, mainChannel: bool = False) -> int:
        channel = int(channel)
        if mainChannel and channel not in self._mainChannelLS:
            raise ValueError("Invalid channel number given! Channel Number can be [1,2].")
        if channel not in self._ChannelLS:
            raise ValueError("Invalid channel number given! Channel Number can be [1,2,3,4].")
        return channel

    def _validate_state(self, state: int | str) -> str:
        state_normalized = self._StateLS_mapping.get(
            state.lower() if isinstance(state, str) else int(state)
        )
        if state_normalized is None:
            raise ValueError("Invalid state given! State can be [on,off,1,0,True,False].")
        return state_normalized

    def _validate_voltage(self, channel: int, voltage: int | float) -> str:
        if channel in self._mainChannelLS and voltage < 0 or voltage > 32:
            raise ValueError("Invalid voltage given! Voltage can be [0,32].")
        if channel == 3 and voltage < 0 or voltage > 5:
            raise ValueError("Invalid voltage given! Voltage on Channel 3 can be [0,5].")
        if channel == 4 and voltage < 0 or voltage > 15:
            raise ValueError("Invalid voltage given! Voltage on Channel 4 can be [0,15].")
        return f"{voltage:.3f}"

    def _validate_amp(self, channel: int, amp: int | float) -> str:
        if channel in self._mainChannelLS and amp < 0 or amp > 3:
            raise ValueError("Invalid current given! Current on Channels 1 and 2 can be [0,3].")
        if (channel == 3 or channel == 4) and amp < 0 or amp > 1:
            raise ValueError("Invalid current given! Current on Channels 3 and 4 can be [0,1].")
        return f"{amp:.4f}"

    def _validate_resistor(self, res: int | float) -> str:
        if res < 1 or res > 1000:
            raise ValueError("Invalid resistance given! Resistance can be [1,1000].")
        return f"{res:.3f}"

    def _validate_measurement_type(self, measurement_type: str) -> str:
        type_normalized = self._measurement_type_mapping.get(
            measurement_type.lower() if isinstance(measurement_type, str) else measurement_type
        )
        if type_normalized is None:
            raise ValueError("Invalid measurement type given! Type can be [voltage,current,power].")
        return type_normalized

    # =============================================================================
    # Set Values and Modes
    # =============================================================================

    def set_Volt(self, channel: int, voltage: int | float) -> None:
        """Set Voltage on the specified channel.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        voltage : int/float.
            Set Voltage on Channel.

        Returns
        -------
        None.

        """
        channel = self._validate_channel(channel)
        voltage = self._validate_voltage(channel, voltage)
        self.write(f"VSET{channel}:{voltage}")

    def set_Voltage(self, channel: int, voltage: int | float) -> None:
        """Alias for set_Volt()."""
        self.set_Volt(channel, voltage)

    def set_Amp(self, channel: int, amp: int | float) -> None:
        """


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        amp : int/float
            Set Current on Channel.

        Returns
        -------
        None.

        """
        channel = self._validate_channel(channel)
        amp = self._validate_amp(channel, amp)
        self.write(f"ISET{channel}:{amp}")

    def set_Current(self, channel: int, amp: int | float) -> None:
        """Alias for set_Amp()."""
        self.set_Amp(channel, amp)

    def set_CurrentLimit(self, channel: int, amp: int | float) -> None:
        """Alias for set_Amp()."""
        self.set_Amp(channel, amp)

    def set_ChannelToSerial(self, state: str | int) -> None:
        """Sets CH1/CH2 as Tracking series mode.


        Parameters
        ----------
        state : str
            Possible state ["ON", "OFF"].

        Returns
        -------
        None.

        """
        state_normalized = self._validate_state(state)
        self.write(f":OUTPut:SERies {state_normalized}")

    def set_ChannelToParallel(self, state: str | int) -> None:
        """Sets CH1/CH2 as Tracking parallel mode.


        Parameters
        ----------
        state : str
            Possible state ["ON", "OFF"].

        Returns
        -------
        None.

        """
        state_normalized = self._validate_state(state)
        self.write(f":OUTPut:PARallel {state_normalized}")

    def set_ChannelTracking(self, mode: int) -> None:
        """Selects the operation mode: independent, tracking series, or tracking parallel.
        GPP-1326 does not have this function. Series-parallel mode is not supported under LOAD.


        Parameters
        ----------
        mode : int
            Select 0 - Independent, 1 - Series or 2 - Parallel

        Returns
        -------
        None.

        """
        modeLS = [0, 1, 2]
        if mode not in modeLS:
            raise ValueError(
                "Invalid Mode Number. Select 0 - Independent, 1 - Series or 2 - Parallel"
            )
        self.write(f"TRACK{mode}")

    def set_ChannelLoadMode(self, channel: int, mode: str, state: str | int) -> None:
        """Sets CH1 or CH2 as Load CV, CC or CR mode.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        mode : str
            Select Load CV, CC or CR mode.
        state : str
            Possible state ["ON", "OFF"].

        Returns
        -------
        None.

        """
        modeLS = ["CC", "CV", "CR"]
        channel = self._validate_channel(channel, mainChannel=True)
        state_normalized = self._validate_state(state)
        if mode not in modeLS:
            raise ValueError("Invalid Mode Setting. Select Load CV, CC or CR mode.")
        self.write(f":LOAD{channel}:{mode} {state_normalized}")

    def set_LoadResistor(self, channel: int, res: float) -> None:
        """Sets the Load CR level.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        res : float
            Set resistance values from range 1-1000.

        Returns
        -------
        None.

        """
        channel = self._validate_channel(channel, mainChannel=True)
        res = self._validate_resistor(res)
        self.write(f":LOAD{channel}:RESistor {res}")

    def set_Out(self, channel: int, state: str | int) -> None:
        """Enable/Disable Output


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        state : str
            state of power Supple output. Could be ["ON", "OFF"]

        Returns
        -------
        None.

        """
        channel = self._validate_channel(channel)
        state_normalized = self._validate_state(state)
        self.write(f":OUTPut{channel}:STATe {state_normalized}")

    def set_AllOut(self, state: str | int) -> None:
        """Enable/Disable All Outputs


        Parameters
        ----------
        state : str
            state of power Supple output. Could be ["ON", "OFF"]

        Returns
        -------
        None.

        """
        state_normalized = self._validate_state(state)
        if state_normalized == "ON":
            self.write("ALLOUTON")
        else:
            self.write("ALLOUTOFF")

    # =============================================================================
    # Ask Commands
    # =============================================================================

    def ask_VoltageSetting(self, channel: int) -> float:
        """Returns the voltage setting, NOT the measured voltage!!!


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Voltage Setting.

        """

        channel = self._validate_channel(channel)
        return float(self.query_values("VSET" + str(channel) + "?"))

    def ask_CurrentSetting(self, channel: int) -> float:
        """Returns the current setting, NOT the measured current!!!


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Current Setting.

        """

        channel = self._validate_channel(channel)
        return float(self.query_values("ISET" + str(channel) + "?"))

    def read_Measurement(self, channel: int, type: str) -> float:
        """Performs a measurement and returns the measured value.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        Type : str
            Select measurement type:
            'volt', 'amp' or 'watt'.

        Returns
        -------
        float
            Return float with the measured value on the channel.

        """

        channel = self._validate_channel(channel)
        type = self._validate_measurement_type(type) 
        return float(self.query_values(f":MEASure{channel}:{type}?"))

    def ask_Current(self, channel: int) -> float:
        """Performs one current measurements and returns the value.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Current.

        """
        return self.read_Measurement(channel, "amp")

    def ask_Voltage(self, channel: int) -> float:
        """Performs one voltage measurements and returns the value.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Voltage.

        """
        return self.read_Measurement(channel, "volt")

    def ask_Power(self, channel: int) -> float:
        """Performs one power measurements and returns the value.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Power.

        """
        return self.read_Measurement(channel, "watt")

    def ask_ChannelLoadMode(self, channel: int) -> str:
        """Queries CH1 or CH2 work mode.
        6 modes: SERies/PARallel/INDE pendent, CV Load/CC Load/CR Load


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].

        Returns
        -------
        str
            SERies/PARallel/INDependent, CV Load/CC Load/CR Load

        """

        channel = self._validate_channel(channel, mainChannel=True)
        return self.query_values(":MODE" + str(channel) + "?")

    def ask_LoadResistor(self, channel: int) -> float:
        """


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].

        Returns
        -------
        float
            Set load Resistance Value for given channel.

        """

        channel = self._validate_channel(channel, mainChannel=True)
        return float(self.query_values(":LOAD" + str(channel) + ":RESistor?"))

    # def ask_Status(self):
    #     '''

    #     Returns
    #     -------
    #     TYPE
    #         Get the state of the output and CC/CV

    #     '''

    #     return float(self.query_values("STATUS?"))

    # =============================================================================
    # Get/Save Data
    # =============================================================================

    def get_data(self, channel: int) -> dict:
        """

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured voltage and current.

        """

        channel = self._validate_channel(channel)
        OutPut = {}
        Voltage = self.read_Measurement(channel, "Voltage")
        Current = self.read_Measurement(channel, "Current")
        Power = self.read_Measurement(channel, "Power")
        OutPut["Voltage/V"] = Voltage
        OutPut["Current/A"] = Current
        OutPut["Power/W"] = Power
        return OutPut
