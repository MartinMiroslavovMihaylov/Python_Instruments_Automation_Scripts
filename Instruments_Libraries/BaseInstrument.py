"""
Created on Tue Feb 27 2025

@author: Refactoring Bot
"""

import logging
from typing import Any, cast

import pyvisa
from pyvisa.resources import MessageBasedResource


class BaseInstrument:
    """
    Base class for all instrument drivers.
    Handles VISA connection, communication, logging, and error handling.
    """

    def __init__(self, resource_str: str, visa_library: str = "@py", **kwargs):
        """
        Initialize the instrument connection.

        Parameters
        ----------
        resource_str : str
            The VISA resource string (e.g., 'TCPIP::192.168.1.1::INSTR') or just an IP address.
        visa_library : str, optional
            VISA library to use (e.g., '@ivi', '@py'). Default is '@py'.
        **kwargs : dict
            Additional arguments passed to `open_resource`.
        """
        import re

        # Auto-format IP address or localhost to TCPIP VISA string if needed
        # We assume it's an IP/locahost if it perfectly matches an IPv4 format or 'localhost'
        ip_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^localhost$", re.IGNORECASE)

        # If the user just gave an IP, add the TCPIP...INSTR decorators
        if ip_pattern.match(resource_str):
            resource_str = f"TCPIP::{resource_str}::INSTR"
        # If it's an IP with a port (socket), example: 192.168.1.1:5025
        elif re.match(r"^(\d{1,3}\.){3}\d{1,3}:\d+$|^localhost:\d+$", resource_str, re.IGNORECASE):
            ip, port = resource_str.split(":")
            resource_str = f"TCPIP::{ip}::{port}::SOCKET"

        self.resource_str = resource_str
        self.logger = logging.getLogger(f"{self.__class__.__name__}({resource_str})")

        # Ensure a basic handler exists if none are configured
        if not self.logger.hasHandlers() and not logging.getLogger().handlers:
            logging.basicConfig(level=logging.INFO)

        try:
            self._rm = pyvisa.ResourceManager(visa_library)
            self._resource = cast(
                MessageBasedResource, self._rm.open_resource(resource_str, **kwargs)
            )
            self.logger.info(f"Connected to {resource_str}")
        except Exception as e:
            self.logger.error(f"Failed to connect to {resource_str}: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    @staticmethod
    def com_to_asrl(com_port: str) -> str:
        """
        Convert a Windows COM port string to a PyVISA ASRL resource string.

        Parameters
        ----------
        com_port : str
            Windows COM port (e.g., "COM3").

        Returns
        -------
        str
            VISA ASRL string (e.g., "ASRL3::INSTR").
        """
        return f"ASRL{com_port.upper().replace('COM','')}::INSTR"

    # =============================================================================
    # Communication Wrappers
    # =============================================================================

    def write(self, command: str) -> None:
        """
        Send a command to the instrument.

        Parameters
        ----------
        command : str
            SCPI command string.
        """
        try:
            self.logger.debug(f"Write: {command}")
            self._resource.write(command)
        except Exception as e:
            self.logger.error(f"Write failed: '{command}', Error: {e}")
            raise

    def query(self, command: str) -> str:
        """
        Send a query and return the response string.
        The instrument's response is stripped of whitespace.

        Parameters
        ----------
        command : str
            SCPI query string.
        """
        try:
            self.logger.debug(f"Query: {command}")
            response = self._resource.query(command).strip()
            self.logger.debug(f"Response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Query failed: '{command}', Error: {e}")
            raise

    def read(self) -> str:
        """
        Read raw response string from the instrument.
        """
        try:
            self.logger.debug("Reading from instrument...")
            response = self._resource.read()
            self.logger.debug(f"Read: {response.strip()}")
            return response
        except Exception as e:
            self.logger.error(f"Read failed: {e}")
            raise

    def query_ascii_values(self, command: str, **kwargs) -> list[Any]:
        """
        Query for a list of ASCII values (e.g., trace data).

        Parameters
        ----------
        command : str
            SCPI query command.
        **kwargs : dict
            Additional arguments passed to `query_ascii_values`.
        """
        try:
            self.logger.debug(f"Query ASCII: {command}")
            return cast(list[Any], self._resource.query_ascii_values(command, **kwargs))
        except Exception as e:
            self.logger.error(f"Query ASCII failed: '{command}', Error: {e}")
            raise

    def query_str_list(self, command: str) -> list[str]:
        """
        Query the instrument and return a list of strings.
        Automatically removes SCPI quotes (' or ") and strips whitespace.
        """
        response = self.query(command)
        if not response or response.upper() == "NONE":
            return []
        return [s.strip().strip("'").strip('"') for s in response.split(",")]

    def query_float(self, command: str) -> float:
        """
        Convenience method to query and parse a single float value.

        Parameters
        ----------
        command : str
            SCPI query string.
        """
        return float(self.query(command))

    def query_int(self, command: str) -> int:
        """
        Convenience method to query and parse a single integer value.

        Parameters
        ----------
        command : str
            SCPI query string.
        """
        return int(float(self.query(command)))

    # =============================================================================
    # Common Instrument Commands
    # =============================================================================

    def get_idn(self) -> str:
        """
        Get the instrument identification string (``*IDN?``).
        """
        return self.query("*IDN?")

    def reset(self) -> None:
        """
        Reset the instrument (``*RST``).
        """
        self.write("*RST")
        self.logger.info("Instrument reset (*RST)")

    def clear(self) -> None:
        """
        Clear the instrument status (``*CLS``).
        """
        self.write("*CLS")

    def get_opc(self) -> int:
        """
        Wait until operation complete (``*OPC?``).

        Returns
        -------
        int
            1 when operation is complete.
        """
        return self.query_int("*OPC?")

    def wait(self) -> None:
        """
        Wait for operation to complete (``*WAI``).
        """
        self.write("*WAI")

    def close(self) -> None:
        """
        Close the connection to the instrument.
        """
        try:
            if hasattr(self, "_resource"):
                self._resource.close()
            if hasattr(self, "_rm"):
                self._rm.close()
            self.logger.info(f"Connection to {self.resource_str} closed.")
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")

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
    # Common aliases
    # =============================================================================

    Close = close
    idn = get_idn
    IDN = get_idn
    opc = get_opc
    OPC = get_opc