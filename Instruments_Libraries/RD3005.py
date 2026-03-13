"""
Created on Mon Aug  1 12:14:47 2022
The script is taken from https://github.com/uberdaff/kd3005p/blob/master/kd3005p.py
and heavily modified by:
@author: Martin.Mihaylov
@author: Maxim.Weizel

#  Copyright 2017 uberdaff
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
# Requirement: pyvisa (migrated from pyserial)
#
# get_idn() - Get instrument identification
# set_voltage(voltage) - Set the voltage on the output
# get_voltage_setting() - Get the 'set' voltage
# measure_voltage() - Get a measurement of the voltage
# set_current(current) - Set the current limit
# get_current_setting() - Get the 'set' current limit
# measure_current() - Get a measurement of the output current
# set_output(state) - Set the state of the output
# set_ocp(bool) - Set the state of the over current protection
# get_status() - Get the state of the output and CC/CV
"""

import time
from typing import Any

import pyvisa
import pyvisa.constants

from .BaseInstrument import BaseInstrument


class RD3005(BaseInstrument):
    def __init__(self, resource_str: str, visa_library: str = "@py", **kwargs):
        """
        Parameters
        ----------
        resource_str : str
            COM Port
        """

        # Automatically convert COM ports
        if resource_str.upper().startswith("COM"):
            resource_str = BaseInstrument.com_to_asrl(resource_str)
            
            
        # Let BaseInstrument handle the pyvisa connection.
        # We enforce serial settings required by RD3005 inline.
        kwargs.setdefault("baud_rate", 9600)
        kwargs.setdefault("data_bits", 8)
        kwargs.setdefault("parity", pyvisa.constants.Parity.none)
        kwargs.setdefault("stop_bits", pyvisa.constants.StopBits.one)
        kwargs.setdefault("read_termination", "")
        kwargs.setdefault("write_termination", "")
        super().__init__(resource_str, visa_library=visa_library, **kwargs)
        self.status = self.get_status()

    def query(self, command: str, delay: float = 0.05) -> str:
        """
        Send a query and return the response string.
        Override for Korad supplies to read buffer without termination characters.
        """
        self.write(command)
        time.sleep(delay)
        target_bytes = getattr(self._resource, "bytes_in_buffer", 0)
        if target_bytes > 0:
            return self._resource.read_bytes(target_bytes).decode().strip()
        raise TimeoutError(f"No response for command '{command}'")

    def _query_float(self, command: str, delay: float = 0.05) -> float:
        return float(self.query(command, delay))

    def get_idn(self) -> str:
        """
        Returns instrument identification.
        """
        return self.query("*IDN?", 0.3)

    def set_voltage(self, channel: Any = None, voltage: float = 0.0, **kwargs) -> None:
        """
        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
            Included for interface compatibility.
        voltage : float
            Set the voltage on the Display
        **kwargs : dict
            Optional keyword arguments like 'delay'.
        """
        delay = kwargs.get("delay", 0.01)
        self.write(f"VSET1:{voltage:1.2f}")
        time.sleep(delay)

    def get_voltage_setting(self, channel: Any = None) -> float:
        """
        Returns the set voltage.
        
        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
        """
        return self._query_float("VSET1?")

    def measure_voltage(self, channel: Any = None) -> float:
        """
        Returns the measured voltage.

        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
        """
        return self._query_float("VOUT1?")

    def set_current(self, channel: Any = None, current: float = 0.0, **kwargs) -> None:
        """
        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
            Included for interface compatibility.
        current : float
            Set the current on the Display
        **kwargs : dict
            Optional keyword arguments like 'delay'.
        """
        delay = kwargs.get("delay", 0.01)
        self.write(f"ISET1:{current:1.3f}")
        time.sleep(delay)

    set_current_limit = set_current

    def get_current_setting(self, channel: Any = None) -> float:
        """
        Returns the set current.

        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
        """
        return self._query_float("ISET1?")

    def measure_current(self, channel: Any = None) -> float:
        """
        Returns the measured current.

        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
        """
        return self._query_float("IOUT1?")

    def measure_power(self, channel: Any = None) -> float:
        """
        Returns the calculated measured power (voltage * current).

        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
        """
        voltage = self.measure_voltage()
        current = self.measure_current()
        return voltage * current

    def set_output(self, channel: Any = None, state: str = "OFF") -> None:
        """
        Parameters
        ----------
        channel : Any, optional
            Ignored for RD3005 as it is a single-channel instrument.
            Included for interface compatibility.
        state : str (ON/OFF)
            Turn Output ON and OFF
        """
        state_norm = self._parse_state(state)
        if state_norm == "ON":
            self.write("OUT1")
        elif state_norm == "OFF":
            self.write("OUT0")

    def set_ocp(self, state: str) -> None:
        """
        Parameters
        ----------
        state : str (ON/OFF)
            Set the state of the overcurrent protection ON and OFF
        """
        state_norm = self._parse_state(state)
        if state_norm == "ON":
            self.write("OCP1")
        elif state_norm == "OFF":
            self.write("OCP0")

    def get_status(self) -> dict[str, str]:
        """
        Returns a dictionary with the state of the output and CC/CV.
        """
        resp = self.query("STATUS?", 0.05)
        stat = ord(resp[0])
        self.status = {}
        if (stat & (1 << 0)) == 0:
            self.status["Mode"] = "CC"
        else:
            self.status["Mode"] = "CV"
        if (stat & (1 << 6)) == 0:
            self.status["Output"] = "Off"
        else:
            self.status["Output"] = "On"
        return self.status

    def get_data(self) -> dict[str, float]:
        """
        Returns a dictionary with the measured voltage and current.
        """
        output = {}
        voltage = self.measure_voltage()
        current = self.measure_current()
        output["Voltage/V"] = voltage
        output["Current/A"] = current

        return output
