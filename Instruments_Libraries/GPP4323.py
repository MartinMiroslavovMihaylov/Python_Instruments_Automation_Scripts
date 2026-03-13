"""
Created on Wed Feb  1 15:55:01 2023

@author: Martin.Mihaylov

Install Driver:
    To use the DC-Power Supply GW-Instek GPP4323 you need to install the USB Driver
    from https://www.gwinstek.com/en-global/download/ - GPP USB Driver
    Python Library needed: ``pip install pyserial``
"""
from .BaseInstrument import BaseInstrument
import pyvisa.constants as visa_const

class GPP4323(BaseInstrument):
    """
    Driver for GW-Instek GPP-4323 Power Supply using BaseInstrument (PyVISA).
    """

    def __init__(self, resource_str: str, visa_library: str = "@py", **kwargs):
        """
        Initialize the GW-Instek GPP-4323 Power Supply.

        Parameters
        ----------
        resource_str : str
            The VISA resource string (e.g., 'COMXX').
        **kwargs : dict
            Additional keyword arguments passed to the BaseInstrument constructor.
        """
        # PyVISA-compatible serial parameters
        kwargs.setdefault("baud_rate", 115200)
        kwargs.setdefault("data_bits", 8)
        kwargs.setdefault("stop_bits", visa_const.StopBits.one)  # <-- enum
        kwargs.setdefault("parity", visa_const.Parity.none)      # <-- enum
        kwargs.setdefault("read_termination", "\n")
        kwargs.setdefault("write_termination", "\n")
        kwargs.setdefault("timeout", 2000)  # 2s

        super().__init__(resource_str, visa_library=visa_library, **kwargs)

        # Internal variables
        self._ChannelLS = [1, 2, 3, 4]
        self._mainChannelLS = [1, 2]
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

    # =============================================================================
    # Checks and Validations
    # =============================================================================

    def _validate_channel(self, channel: int, main_channel: bool = False) -> int:
        channel = int(float(channel))
        if main_channel and channel not in self._mainChannelLS:
            raise ValueError("Invalid channel number given! Channel Number can be [1,2].")
        if channel not in self._ChannelLS:
            raise ValueError("Invalid channel number given! Channel Number can be [1,2,3,4].")
        return channel

    def _validate_voltage(self, channel: int, voltage: int | float) -> str:
        if channel in self._mainChannelLS and (voltage < 0 or voltage > 32):
            raise ValueError("Invalid voltage given! Voltage can be 0V - 32V.")
        if channel == 3 and (voltage < 0 or voltage > 5):
            raise ValueError("Invalid voltage given! Voltage on Channel 3 can be 0V - 5V.")
        if channel == 4 and (voltage < 0 or voltage > 15):
            raise ValueError("Invalid voltage given! Voltage on Channel 4 can be 0V - 15V.")
        return f"{voltage:.3f}"

    def _validate_amp(self, channel: int, amp: int | float) -> str:
        if channel in self._mainChannelLS and (amp < 0 or amp > 3):
            raise ValueError("Invalid current given! Current on Channels 1 and 2 can be 0A - 3A.")
        if (channel == 3 or channel == 4) and (amp < 0 or amp > 1):
            raise ValueError("Invalid current given! Current on Channels 3 and 4 can be 0A - 1A.")
        return f"{amp:.4f}"

    def _validate_resistor(self, res: int | float) -> str:
        if res < 1 or res > 1000:
            raise ValueError("Invalid resistance given! Resistance can be 1Ω - 1000Ω.")
        return f"{res:.3f}"

    def _validate_measurement_type(self, measurement_type: str) -> str:
        type_str = self._check_scpi_param(
            str(measurement_type).strip().upper(),
            ["VOLTage", "CURRent", "V", "A", "AMP", "POWer", "WATT", "P"],
        )
        return self._measurement_type_mapping.get(type_str.lower(), type_str.title())

    # =============================================================================
    # Set Values and Modes
    # =============================================================================

    def set_voltage(self, channel: int, voltage: int | float) -> None:
        """Set Voltage on the specified channel.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        voltage : int/float.
            Set Voltage on Channel.
        """
        channel = self._validate_channel(channel)
        voltage_str = self._validate_voltage(channel, voltage)
        self.write(f"VSET{channel}:{voltage_str}")

    def set_current(self, channel: int, amp: int | float) -> None:
        """
        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        amp : int/float
            Set Current on Channel.
        """
        channel = self._validate_channel(channel)
        amp_str = self._validate_amp(channel, amp)
        self.write(f"ISET{channel}:{amp_str}")

    set_current_limit = set_current

    def set_channel_tracking_series(self, state: str | int) -> None:
        """Sets CH1/CH2 as Tracking series mode.

        Parameters
        ----------
        state : str
            Possible state ["ON", "OFF"].
        """
        state_normalized = self._parse_state(state)
        self.write(f":OUTPut:SERies {state_normalized}")

    def set_channel_tracking_parallel(self, state: str | int) -> None:
        """Sets CH1/CH2 as Tracking parallel mode.

        Parameters
        ----------
        state : str
            Possible state ["ON", "OFF"].
        """
        state_normalized = self._parse_state(state)
        self.write(f":OUTPut:PARallel {state_normalized}")

    def set_channel_tracking(self, mode: int) -> None:
        """Selects the operation mode: independent, tracking series, or tracking parallel.
        GPP-1326 does not have this function. Series-parallel mode is not supported under LOAD.

        Parameters
        ----------
        mode : int
            Select 0 - Independent, 1 - Series or 2 - Parallel
        """
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid Mode. Select 0 - Independent, 1 - Series, 2 - Parallel")
        self.write(f"TRACK{mode}")

    def set_channel_load_mode(self, channel: int, mode: str, state: str | int) -> None:
        """Sets CH1 or CH2 as Load CV, CC or CR mode.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        mode : str
            Select Load CV, CC or CR mode.
        state : str
            Possible state ["ON", "OFF"].
        """
        valid_mode = self._check_scpi_param(mode, ["CC", "CV", "CR"])
        channel = self._validate_channel(channel, main_channel=True)
        state_normalized = self._parse_state(state)
        self.write(f":LOAD{channel}:{valid_mode} {state_normalized}")

    def set_load_resistor(self, channel: int, res: float) -> None:
        """Sets the Load CR level.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        res : float
            Set resistance values from range 1-1000.
        """
        channel = self._validate_channel(channel, main_channel=True)
        res_str = self._validate_resistor(res)
        self.write(f":LOAD{channel}:RESistor {res_str}")

    def set_output(self, channel: int, state: str | int) -> None:
        """Enable/Disable Output

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        state : str
            state of power Supple output. Could be ["ON", "OFF"]
        """
        channel = self._validate_channel(channel)
        state_normalized = self._parse_state(state)
        self.write(f":OUTPut{channel}:STATe {state_normalized}")

    set_out = set_output

    def set_all_outputs(self, state: str | int) -> None:
        """Enable/Disable All Outputs

        Parameters
        ----------
        state : str
            state of power Supple output. Could be ["ON", "OFF"]
        """
        state_normalized = self._parse_state(state)
        if state_normalized == "ON":
            self.write("ALLOUTON")
        else:
            self.write("ALLOUTOFF")

    # =============================================================================
    # Ask Commands
    # =============================================================================

    def get_voltage_setting(self, channel: int) -> float:
        """Returns the voltage setting, NOT the measured voltage!!!

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        channel = self._validate_channel(channel)
        return float(self.query(f"VSET{channel}?"))

    def get_current_setting(self, channel: int) -> float:
        """Returns the current setting, NOT the measured current!!!

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        channel = self._validate_channel(channel)
        return float(self.query(f"ISET{channel}?"))

    def measure(self, channel: int, measurement_type: str) -> float:
        """Performs a measurement and returns the measured value.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        Type : str
            Select measurement type:
            'volt', 'amp' or 'watt'.
        """
        channel = self._validate_channel(channel)
        type_norm = self._validate_measurement_type(measurement_type)
        return float(self.query(f":MEASure{channel}:{type_norm}?"))

    def measure_current(self, channel: int) -> float:
        """Performs one current measurements and returns the value.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        return self.measure(channel, "amp")

    def measure_voltage(self, channel: int) -> float:
        """Performs one voltage measurements and returns the value.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        return self.measure(channel, "volt")

    def measure_power(self, channel: int) -> float:
        """Performs one power measurements and returns the value.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        return self.measure(channel, "watt")

    def get_channel_load_mode(self, channel: int) -> str:
        """Queries CH1 or CH2 work mode.
        6 modes: SERies/PARallel/INDE pendent, CV Load/CC Load/CR Load

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        """
        channel = self._validate_channel(channel, main_channel=True)
        return self.query(f":MODE{channel}?")

    def get_load_resistor(self, channel: int) -> float:
        """
        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        """
        channel = self._validate_channel(channel, main_channel=True)
        return float(self.query(f":LOAD{channel}:RESistor?"))

    # =============================================================================
    # Get/Save Data
    # =============================================================================

    def get_data(self, channel: int) -> dict:
        """
        Return a dictionary with the measured voltage and current.

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        """
        channel = self._validate_channel(channel)
        result = {}
        result["Voltage/V"] = self.measure_voltage(channel)
        result["Current/A"] = self.measure_current(channel)
        result["Power/W"] = self.measure_power(channel)
        return result