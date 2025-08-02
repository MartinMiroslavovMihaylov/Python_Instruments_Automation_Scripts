# -*- coding: utf-8 -*-
"""
Created on Mon Jul  21 18:56:32 2025

@author: Maxim Weizel
"""


import numpy as np
import pyvisa as visa


class M8070B:
    """
    Start the M8070B Software. Go to Utilities-> SCPI Server Information.
    Copy the VISA resource string (usually localhost).
    """

    def __init__(self, resource_str="TCPIP0::localhost::hislip0::INSTR"):
        self._resource = visa.ResourceManager().open_resource(str(resource_str), query_delay=0.5)
        self._channelLS = [1, 2]  #
        self.state_mapping = {"on": 1, "off": 0, 1: 1, 0: 0, "1": 1, "0": 0}
        print(self.getIdn())

    def query(self, command):
        return self._resource.query(command)

    def write(self, command):
        return self._resource.write(command)

    def Close(self):
        self._resource.close()

    def getIdn(self):
        return self.query("*IDN?").strip()

    # =============================================================================
    # Check functions
    # =============================================================================

    def _validate_channel(self, channel: int) -> int:
        channel = int(channel)
        if channel not in self._channelLS:
            raise ValueError("Channel must be 1 or 2")
        return channel

    # =============================================================================
    # Get Values and Modes
    # =============================================================================

    def get_amplitude(self, channel: int = 1) -> float:
        """Returns the differential amplitude setting for the selected channel.

        Parameters
        ----------
        channel : int, optional
            1 or 2, by default 1

        Returns
        -------
        float
            Differential amplitude setting.
        """
        channel = self._validate_channel(channel)
        return float(self.query(f":SOURce:VOLTage:AMPLitude? 'M2.DataOut{channel}'"))

    # =============================================================================
    # Set Values and Modes
    # =============================================================================

    def set_amplitude(self, channel: int, value: float) -> None:
        """Differential amplitude setting for the selected channel.

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        value : float
            Amplitude setting in V. Must be between 0.1 and 2.7 V
        """
        channel = self._validate_channel(channel)
        if 0.1 <= value <= 2.7:
            self.write(f":SOURce:VOLTage:AMPLitude 'M2.DataOut{channel}', {value}")
        else:
            raise ValueError(f"Value must be between 0.1 and 2.7 V. You entered: {value} V")

    def set_output(self, channel: int, state: int | str) -> None:
        """Activate or deactivate the selected channel output.

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        state : int | str
            One of: 0, 1, "off", "on"

        Raises
        ------
        ValueError
            Channel must be 1 or 2.
            State must be 0 or 1.
        """
        channel = self._validate_channel(channel)
        state_normalized = self.state_mapping.get(
            state.lower() if isinstance(state, str) else int(state)
        )
        if state_normalized is None:
            raise ValueError("Value must be 0 or 1")

        self.write(f":OUTPut:STATe 'M2.DataOut{channel}', {state_normalized}")

    def set_rf_output(self, channel: int, state: int | str) -> None:
        """Activate or deactivate the selected channel output.
        Alias for set_output().
        """
        self.set_output(channel, state)
