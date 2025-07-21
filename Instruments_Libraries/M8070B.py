# -*- coding: utf-8 -*-
"""
Created on Mon Jul  21 18:56:32 2025

@author: Maxim Weizel
"""


import numpy as np
import pyvisa as visa


class M8070B:
    def __init__(self, resource_str="TCPIP0::localhost::hislip0::INSTR"):
        self._resource = visa.ResourceManager().open_resource(str(resource_str), query_delay=0.5)
        self._channelLS = [1, 2]
        print(self.getIdn())

    def query(self, command):
        return self._resource.query(command)

    def write(self, command):
        return self._resource.write(command)

    def Close(self):
        self._resource.close()

    def getIdn(self):
        return self.query("*IDN?")

    # =============================================================================
    # Get Values and Modes
    # =============================================================================

    def get_amplitude(self, channel: int = 1) -> float:
        channel = int(channel)
        if channel not in self._channelLS:
            raise ValueError("Channel must be 1 or 2")
        return float(self.query(f":SOURce:VOLTage:AMPLitude? 'M2.DataOut{channel}'"))

    def set_Output(self, channel: int = 1, state: int = 0):
        channel = int(channel)
        if channel not in self._channelLS:
            raise ValueError("Channel must be 1 or 2")
        if state not in [0, 1]:
            raise ValueError("Value must be 'ON' or 'OFF'")
        self.write(f":OUTPut:STATe 'M2.DataOut{channel}', {state}")

    # =============================================================================
    # Set Values and Modes
    # =============================================================================

    def set_amplitude(self, channel: int = 1, value: float = 0.1):
        channel = int(channel)
        if channel not in self._channelLS:
            raise ValueError("Channel must be 1 or 2")
        self.write(f":SOURce:VOLTage:AMPLitude 'M2.DataOut{channel}', {value}")
