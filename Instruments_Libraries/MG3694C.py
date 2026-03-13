"""
Created on Wed Dec  1 07:00:19 2021

@author: Martin.Mihylov

Currently the Anritsu MG3694C Signal Generator is in dynamic DHCP mode!!!
    1) Make sure Instrument and PC are connected vie ethernet cable.
    2) In the Windows terminal run: arp -a
    3) Find the IP-Adress corresponding to the MAC:Adress printed on the device
    4) If it does not show up try opening NI-MAX and run auto-discover.
    5) Try "arp -a" again.

Legacy instructions (not applicable as of 13.01.2026):
    1) Go to Network Adapter Settings -> 'Internetprotocoll, Version 4(TCP/IPv4)'
    2) Change the IP-Address from 'automatic' to 'static' and give the IP:192.168.0.1
    3) DNS will be filled automatically! Press 'OK' and leave.
    4) The standard IP of the instrument is: 192.168.0.254
    5) After your measurement dont forget to change the IP back to 'automatic'!
"""

import functools
import time
from collections.abc import Callable
from typing import Any, cast

import pyvisa as visa
import pyvisa.constants as vi_const

from .BaseInstrument import BaseInstrument


def auto_reconnect(func: Callable) -> Callable:
    """
    Decorator that catches VISA errors, reconnects, and retries the command.
    """

    @functools.wraps(func)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        attempts = 3
        for i in range(attempts):
            try:
                # Try to execute the function (write/query)
                return func(self, *args, **kwargs)
            except (visa.errors.VisaIOError, OSError) as e:
                # If it's the last attempt, raise the error
                if i == attempts - 1:
                    print(f"Failed after {attempts} attempts. Error: {e}")
                    raise e

                print(
                    f"""Connection lost during {getattr(func, "__name__", "function")}. 
                    Reconnecting (Attempt {i + 1}/{attempts})..."""
                )
                try:
                    self.reconnect()
                except Exception as reconnect_err:
                    print(f"Reconnect failed: {reconnect_err}")
                    time.sleep(1)  # Wait a bit before next loop

    return wrapper


class MG3694C(BaseInstrument):
    """
    This class uses pyvisa to connect to an Anritsu MG3694C Signal Generator.
    """

    def __init__(self, resource_str: str = "169.254.20.95", visa_library: str = "@ivi", **kwargs):
        kwargs.setdefault("read_termination", "\n")
        kwargs.setdefault("query_delay", 0.5)
        self._pyvisa_kwargs = kwargs
        super().__init__(str(resource_str), visa_library=visa_library, **kwargs)
        self.visa_library = visa_library

        try:
            self._resource.set_visa_attribute(vi_const.VI_ATTR_TCPIP_KEEPALIVE, True)  # type: ignore
        except visa.errors.VisaIOError:
            pass

        print(f"Connected to: {self.get_idn()}")

    def connect(self):
        self._rm = visa.ResourceManager(self.visa_library)
        self._resource = cast(
            visa.resources.MessageBasedResource,
            self._rm.open_resource(str(self.resource_str), **self._pyvisa_kwargs),
        )
        try:
            self._resource.set_visa_attribute(vi_const.VI_ATTR_TCPIP_KEEPALIVE, True)  # type: ignore
        except visa.errors.VisaIOError:
            pass

    def reconnect(self):
        try:
            self._resource.close()
        except Exception:
            pass
        time.sleep(1)
        self.connect()

    @auto_reconnect
    def write(self, command: str) -> None:
        super().write(command)

    @auto_reconnect
    def query(self, command: str) -> str:
        return super().query(command)

    @auto_reconnect
    def read(self) -> str:
        return self._resource.read()

    # =============================================================================
    # Abort Command
    # =============================================================================
    def abort(self):
        """
        Forces the trigger system to the idle state. Any sweep in progress is aborted
        as soon as possible.

        Parameters: None
        """
        return self.write(":ABORt")

    # =============================================================================
    # Ask Instrument about Stats and Parameters
    # =============================================================================
    def get_output_protection(self) -> str:
        """
        Requests the currently programmed state of the MG369xC RF output during
        frequency changes in CW or step sweep mode.
        """
        return self.query(":OUTPut:PROTection?")

    def get_output_retrace(self) -> str:
        """
        Requests the currently programmed state of the MG369xC RF output during
        sweep retrace.
        """

        return self.query(":OUTPut:PROTection:RETRace?")

    def get_output_impedance(self) -> float:
        """
        Queries the MG369xC RF output impedance. The impedance is
        nominally 50 ohms and is not settable.
        """

        return float(self.query(":OUTPut:IMPedance?"))

    def get_output_power_level(self) -> float:
        """
        Requests the value currently programmed for the RF output power level.
        """

        return float(self.query(":SOURce:POWer:LEVel:IMMediate:AMPLitude?") or 0.0)

    def get_maximal_power_level(self) -> float:
        """
        Requests the maximum RF output power level value that can be programmed for the
        particular MG369xC model.
        """

        return float(self.query(":SOURce:POWer? MAX"))

    # =============================================================================
    # Ask Source Amplitude Modulation
    # =============================================================================
    def get_am_logsens(self) -> float:
        """
        Requests the currently programmed AM sensitivity value for the external AM Log mode.
        """

        return float(self.query(":SOURce:AM:LOGSens?"))

    def get_am_logdepth(self) -> float:
        """
        Requests the currently programmed modulation depth value for the internal
        AM Log mode.
        """

        return float(self.query(":SOURce:AM:LOGDepth?"))

    def get_am_internal_wave(self) -> str:
        """
        Requests the currently selected modulating waveform for the internal AM function.
        """

        return self.query(":SOURce:AM:INTernal:WAVE?")

    def get_am_internal_freq(self) -> float:
        """Requests the currently programmed modulating waveform frequency value for the
        internal AM function.
        """

        return float(self.query(":SOURce:AM:INTernal:FREQuency?"))

    def get_am_state(self) -> str:
        """Requests currently programmed amplitude modulation state (on/off)"""

        return self.query(":SOURce:AM:STATe?")

    def get_am_type(self) -> str:
        """Requests the currently programmed AM operating mode."""

        return self.query(":SOURce:AM:TYPE?")

    # =============================================================================
    # Frequency Modulation
    # =============================================================================
    def get_fm_internal_wave(self) -> str:
        """
        Requests the currently selected modulating waveform for the internal FM function.
        """

        return self.query(":SOURce:FM:INTernal:WAVE?")

    def get_fm_internal_freq(self) -> float:
        """
        Requests the currently programmed modulating waveform frequency value for the
        internal FM function.
        """
        return float(self.query(":SOURce:FM:INTernal:FREQuency?"))

    def get_fm_mode(self) -> str:
        """
        Requests the currently programmed synthesis mode used to generate the FM signal.
        """

        return self.query(":SOURce:FM:MODE?")

    def get_fm_bwidth(self) -> str:
        """
        Requests the currently programmed Unlocked FM synthesis mode of operation
        (narrow or wide).
        """

        return self.query(":SOURce:FM:BWIDth?")

    def get_fm_state(self) -> str:
        """
        Requests the currently programmed frequency modulation state (on/off).
        """

        return self.query(":SOURce:FM:STATe?")

    # =============================================================================
    # Frequency Commands
    # =============================================================================
    def get_freq_cw(self) -> float:
        """
        Requests the current value of the frequency parameter.
        """

        return float(self.query(":SOURce:FREQuency:CW?") or 0.0)

    def get_freq_step(self) -> float:
        """
        Requests the current step increment value of the frequency parameter.
        """

        return float(self.query(":SOURce:FREQuency:CW:STEP:INCRement?") or 0.0)

    def get_freq_center_freq(self) -> float:
        """
        Requests the current value of the RF output center frequency.
        """

        return float(self.query(":SOURce:FREQuency:CENTer?") or 0.0)

    def get_freq_mode(self) -> str:
        """
        Requests the currently selected programming mode for frequency control.
        """

        return self.query(":SOURce:FREQuency:MODE?")

    def get_freq_span(self) -> float:
        """
        Requests the current value for SWEep[1] sweep span.
        """

        return float(self.query(":SOURce:FREQuencySPAN:?") or 0.0)

    def get_freq_start(self) -> float:
        """
        Requests the current value for SWEep[1] start frequency.
        """

        return float(self.query(":SOURce:FREQuency:STARt?") or 0.0)

    def get_freq_stop(self) -> float:
        """
        Requests the current value for SWEep[1] stop frequency.
        """

        return float(self.query(":SOURce:FREQuency:STOP?") or 0.0)

    def get_freq_unit(self) -> str:
        """
        Requests the currently selected frequency unit.
        """
        return self.query("UNIT:FREQuency?")

    # =============================================================================
    # Pulse Modulation
    # =============================================================================
    def get_pm_bwidth(self) -> str:
        """
        Requests the currently programmed phase modulation operating mode.
        """

        return self.query(":SOURce:PM:BWIDth?")

    def get_pm_internal_wave(self) -> str:
        """
        Requests the currently selected modulating waveform for the internal phase
        modulation function.
        """

        return self.query(":SOURce:PM:INTernal:WAVE?")

    def get_pm_internal_freq(self) -> float:
        """
        Requests the currently programmed modulating waveform frequency value for the
        internal phase modulation function.
        """

        return float(self.query(":SOURce:PM:INTernal:FREQuency?") or 0.0)

    def get_pm_state(self) -> str:
        """
        Requests the currently programmed phase modulation state (on/off).
        """

        return self.query(":SOURce:PM:STATe?")

    # =============================================================================
    # Set Output
    # =============================================================================
    def set_rf_output(self, state: int | str) -> None:
        """Activates the Signal Genrator RF Output.

        Parameters
        ----------
        state : str | int
            ``ON`` | ``OFF`` | ``1`` | ``0``

        Raises
        ------
        ValueError
            Valid values are: ON, OFF, 1, 0
        """

        state = self._parse_state(state)
        self.write(f":OUTPut:STATe {state}")

    def set_output(self, state: int | str) -> None:
        """Activates the Signal Genrator RF Output.

        Parameters
        ----------
        state : str | int
            ``ON`` | ``OFF`` | ``1`` | ``0``

        Raises
        ------
        ValueError
            Valid values are: ON, OFF, 1, 0
        """
        self.set_rf_output(state)

    def set_output_protection(self, state: int | str) -> None:
        """
        ON causes the MG369xC RF output to be turned off (blanked) during frequency changes
        in CW or step sweep mode.
        OFF leaves RF output turned on (un blanked).

        Parameters
        ----------
        state : str | int
            Default: ``ON``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(f":OUTPut:PROTection {state}")

    def set_output_retrace(self, state: int | str) -> None:
        """
        ON causes the MG369xC RF output to be turned off during sweep retrace.
        OFF leaves RF output turned on.

        Parameters
        ----------
        state : str | int
            Default: ``OFF``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(":OUTPut:PROTection:RETRace " + str(state))

    # =============================================================================
    # SOURce:POWer subsystem
    # =============================================================================

    def set_rf_power(self, value: int | float):
        """Sets the Signal Generator Output Power in dBm.

        Parameters
        ----------
        value : int | float
            Output Power in dBm
        """
        min_val = -20.0
        max_val = 30.0
        if value > max_val or value < min_val:
            raise ValueError(
                f"Power out of range! You can set power between {min_val} and {max_val} dBm!"
            )

        self.write(f":SOURce:POWer:LEVel:IMMediate:AMPLitude {str(value)} dBm")

    def set_output_power_level(self, value: int | float) -> None:
        """Sets the Signal Generator Output Power in dBm. Alias for set_rf_power().

        Parameters
        ----------
        value : int | float
            Output Power in dBm
        """
        self.set_rf_power(value)

    # =============================================================================
    # Set Control system commands:
    #            Amplitude Modulation
    #            Correction Commands
    #            Frequency Modulation
    #            Frequency Commands
    #            Pulse Modulation
    #
    # =============================================================================
    # =============================================================================
    #   Source - AM
    # =============================================================================
    def set_am_logsens(self, value: int | float) -> None:
        """
        Sets the AM sensitivity for the external AM Log mode.


        Parameters
        ----------
        value : int | float
            Sensitivity (in dB/V)
            Range: 0 to 25 dB/V
            Default: 3 dB/V
        """

        if 0 <= int(value) <= 25:
            self.write(":SOURce:AM:LOGSens " + str(value) + " dB/V")
        else:
            raise ValueError(
                f"Invalid AM log sensitivity: {value} dB/V. Valid range is 0 to 25 dB/V."
            )

    def set_am_logdepth(self, value: int | float) -> None:
        """
        Sets the modulation depth of the AM signal in the internal AM Log mode.

        Parameters
        ----------
        value : int | float
            Modulation depth (in dB).
            Valid range is 0 to 25 dB.
            Default is 3 dB.
        """

        if 0 <= int(value) <= 25:
            self.write(f":SOURce:AM:LOGDepth {int(value)} dB")
        else:
            raise ValueError(f"Invalid AM log depth: {int(value)} dB. Valid range is 0 to 25 dB.")

    def set_am_internal_wave(self, state: str) -> None:
        """
        Selects the modulating waveform (from the internal AM generator)
        for the internal AM function.

        Parameters
        ----------
        state : str

            * ``'SINE'`` - Sine wave
            * ``'GAUSsian'`` - Gaussian noise
            * ``'RDOWn'`` - Negative ramp
            * ``'RUP'`` - Positive ramp
            * ``'SQUare'`` - Square wave
            * ``'TRIangle'`` - Triangle wave
            * ``'UNIForm'`` - Uniform noise
        """

        valid_list = ["SINE", "GAUSsian", "RDOWn", "RUP", "SQUare", "TRIangle", "UNIForm"]
        valid_state = self._check_scpi_param(state, valid_list)
        self.write(":SOURce:AM:INTernal:WAVE " + valid_state)

    def set_am_internal_freq(self, value: int | float, unit: str) -> None:
        """
        Sets the frequency of the modulating waveform for the internal AM function
        (see :AM:INTernal:WAVE).

        Parameters
        ----------
        value : int | float
            Frequency
            Range: 0.1 Hz to 1 MHz for sine wave.
            0.1 Hz to 100 kHz for square, triangle, and ramp waveforms.
            Default: 1 kHz
        unit : str
            Unit of the frequency (Hz, kHz, MHz)
        """

        wave = self.get_am_internal_wave().strip()

        multipliers = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6}
        if unit.upper() not in multipliers:
            raise ValueError(f"Invalid unit '{unit}'. Must be one of 'Hz', 'kHz', 'MHz'.")

        freq_hz = value * multipliers[unit.upper()]

        if wave == "SINE":
            if not (0.1 <= freq_hz <= 1e6):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 1 MHz) for SINE wave."
                )
        else:
            if not (0.1 <= freq_hz <= 100e3):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 100 kHz) for {wave} wave."
                )

        self.write(f":SOURce:AM:INTernal:FREQuency {value} {unit}")

    def set_am_state(self, state: str | int) -> None:
        """
        Enable/disable amplitude modulation of MG369xC RF output signal.

        Parameters
        ----------
        state : str | int
            Default: ``OFF``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(":SOURce:AM:STATe " + str(state))

    def set_am_type(self, state: str) -> None:
        """
        Selects the AM operating mode.

        Parameters
        ----------
        state : str
            Default: ``LINear``
            * ``LINear`` | ``LOGarithmic``
        """

        valid_state = self._check_scpi_param(state, ["LINear", "LOGarithmic"])
        self.write(":SOURce:AM:TYPE " + valid_state)

    # =============================================================================
    #     Correction Commands
    # =============================================================================
    def set_correction_commands(self, state: str | int) -> None:
        """
        Turns the selected user level flatness correction power-offset table on/off.

        Parameters
        ----------
        state : str | int
            Default: ``OFF``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(":SOURce:CORRection:STATe " + str(state))

    # =============================================================================
    # Frequency Modulation
    # =============================================================================
    def set_fm_internal_wave(self, state: str) -> None:
        """
        Selects the modulating waveform (from the internal FM generator)
        for the internal FM function.

        Parameters
        ----------
        state : str
            Default: SINE

            * ``SINE`` = Sine wave
            * ``GAUSsian`` = Gaussian noise
            * ``RDOWn`` = Negative ramp
            * ``RUP`` =Positive ramp
            * ``SQUare`` = Square wave
            * ``TRIangle`` = Triangle wave
            * ``UNIForm`` = Uniform noise
        """

        valid_list = ["SINE", "GAUSsian", "RDOWn", "RUP", "SQUare", "TRIangle", "UNIForm"]
        valid_state = self._check_scpi_param(state, valid_list)
        self.write(":SOURce:FM:INTernal:WAVE " + valid_state)

    def set_fm_internal_freq(self, value: int | float, unit: str) -> None:
        """
        Sets the frequency of the modulating waveform for the internal FM function
        (see :FM:INTernal:WAVE).

        Parameters
        ----------
        value : int | float
            Frequency
            Range: 0.1 Hz to 1 MHz for sine wave.
            0.1 Hz to 100 kHz for square, triangle, and ramp waveforms.
            Default: 1 kHz
        unit : str
            Unit of the frequency (Hz, kHz, MHz)
        """

        wave = self.get_fm_internal_wave().strip()

        multipliers = {"Hz": 1, "kHz": 1e3, "MHz": 1e6}
        if unit not in multipliers:
            raise ValueError(f"Invalid unit '{unit}'. Must be one of 'Hz', 'kHz', 'MHz'.")

        freq_hz = value * multipliers[unit]

        if wave == "SINE":
            if not (0.1 <= freq_hz <= 1e6):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 1 MHz) for SINE wave."
                )
        else:
            if not (0.1 <= freq_hz <= 100e3):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 100 kHz) for {wave} wave."
                )

        self.write(f":SOURce:FM:INTernal:FREQuency {value} {unit}")

    def set_fm_mode(self, state: str) -> None:
        """
        Selects the synthesis mode employed in generating the FM signal.
        If LOCKed[1] or LOCKed2 is set, the YIG phase-locked loop is used in synthesizing
        the FM signal. If UNLocked is set, the YIG phase-lock loop is disabled and the FM
        signal is obtained by applying the modulating signal to the tuning coils of the
        YIG-tuned oscillator.

        Parameters
        ----------
        state : str
            Default: UNLocked

            * ``LOCKed[1]`` = Locked Narrow FM
            * ``LOCKed2`` = Locked Narrow Low-Noise FM
            * ``UNLocked`` = Unlocked FM
        """

        valid_state = self._check_scpi_param(state, ["LOCKed[1]", "LOCKed2", "UNLocked"])
        self.write(":SOURce:FM:MODE " + valid_state)

    def set_fm_bwidth(self, state: str) -> None:
        """
        Sets the Unlocked FM synthesis mode to wide or narrow mode of operation.
        The Unlocked Wide FM synthesis mode allows maximum deviations of ±100 MHz for
        DC to 100 Hz rates.
        The Unlocked Narrow FM synthesis mode allows maximum deviations of ±10 MHz for
        DC to 8 MHz rates.

        Parameters
        ----------
        state : str
            * ``MIN`` = narrow mode
            * ``MAX`` = wide mode
            Default: MIN
        """

        valid_state = self._check_scpi_param(state, ["MIN", "MAX"])
        self.write(":SOURce:FM:BWIDth " + valid_state)

    def set_fm_state(self, state: str | int) -> None:
        """
        Enable/disable frequency modulation of MG369xC RF output signal.

        Parameters
        ----------
        state : str | int
            Default: ``OFF``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(":SOURce:FM:STATe " + str(state))

    # =============================================================================
    # Frequency Commands
    # =============================================================================
    def set_freq_cw(self, value: int | float, unit: str | None = None) -> None:
        """
        Parameters
        ----------
        value : int | float
            Continuous Wave Frequency.
            Range: 10 MHz to 40 GHz

        unit : str (optional)
            Frequency Unit: 'GHz' or 'MHz' or 'Hz'
        """

        min_freq = 10e6  # 10 MHz
        max_freq = 40e9  # 40 GHz

        if unit is None or unit.upper() == "HZ":
            unit = "Hz"
            if value <= max_freq and value >= min_freq:
                self.write(f":SOURce:FREQuency:CW {value} {unit}")
            else:
                raise ValueError("Minimum Frequency = 10 MHz and Maximum Frequency = 40 GHz")
        elif unit.upper() == "MHZ":
            if value * 1e6 <= max_freq and value * 1e6 >= min_freq:
                self.write(f":SOURce:FREQuency:CW {value} {unit}")
            else:
                raise ValueError("Minimum Frequency = 10 MHz and Maximum Frequency = 40 GHz")
        elif unit.upper() == "GHZ":
            if value * 1e9 <= max_freq and value * 1e9 >= min_freq:
                self.write(f":SOURce:FREQuency:CW {value} {unit}")
            else:
                raise ValueError("Minimum Frequency = 10 MHz and Maximum Frequency = 40 GHz")
        else:
            raise ValueError('Unknown input! Unit must be None or "Hz", "MHz", or "GHz"!')

    def set_freq_step(self, value: int | float, unit: str) -> None:
        """
        Sets the step increment size used with the :FREQuency:CW command.

        Parameters
        ----------
        value : int | float
            Step increment size
            Range: 0.01 Hz to (MAX  MIN)
            Default: 0.1 GHz
        unit : str
            Frequency Unit: 'Hz' or 'kHz' or 'MHz' or 'GHz'
        """

        multipliers = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
        if unit.upper() not in multipliers:
            raise ValueError('Unknown unit! Unit must be "Hz", "kHz", "MHz", or "GHz"')

        freq_hz = value * multipliers[unit.upper()]
        if freq_hz >= 0.01:
            self.write(f":SOURce:FREQuency:CW:STEP:INCRement {value} {unit}")
        else:
            raise ValueError(f"Frequency step must be >= 0.01 Hz. Got: {freq_hz} Hz")

    def set_freq_cent(self, value: int | float, unit: str) -> None:
        """
        Sets the MG369xC RF output center frequency to the value entered.
        :CENTER and :SPAN frequencies are coupled values. Entering the value for one
        will cause the other to be recalculated. (See notes under :FREQuency:SPAN)

        Parameters
        ----------
        value : int | float
            Center frequency
        unit : str
            Frequency Unit: 'Hz' or 'kHz' or 'MHz' or 'GHz'
        """

        multipliers = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
        if unit.upper() not in multipliers:
            raise ValueError('Unknown unit! Unit must be "Hz", "kHz", "MHz", or "GHz"')

        freq_hz = value * multipliers[unit.upper()]
        if freq_hz >= 0.01:
            self.write(f":SOURce:FREQuency:CENTer {value} {unit}")
        else:
            raise ValueError(f"Center frequency must be >= 0.01 Hz. Got: {freq_hz} Hz")

    def set_frequency_mode(self, mode):
        """
        Specifies which command subsystem controls the MG369xC frequency.

        Parameters
        ----------
        mode : str
            Default: ``CW``
            * ``CW`` | ``FIXed`` = [:SOURce]:FREQuency:CW|FIXed
            * ``SWEep[1]`` = [:SOURce]:SWEep[1] :SWEep and :SWEep1 may be used interchangeably
            * ``SWCW`` = (see notes)
            * ``ALSW`` = (see notes)
            * ``LIST<n>`` = [:SOURce]:LIST<n> (n=1-4)
        """

        valid_list = [
            "CW",
            "FIXed",
            "SWEep[1]",
            "SWCW",
            "ALSW",
            "LIST[1]",
            "LIST2",
            "LIST3",
            "LIST4",
        ]
        valid_state = self._check_scpi_param(mode, valid_list)
        self.write(":SOURce:FREQuency:MODE " + valid_state)

    def set_freq_span(self, value: int | float, unit: str) -> None:
        """
        Sets sweep span for SWEep[1] to value entered. :SPAN and :CENTer are coupled values.

        Parameters
        ----------
        value : int | float
            Range: 1 kHz to (MAX  MIN)
            Default: MAX  MIN
        unit : str
            Frequency Unit: 'Hz' or 'kHz' or 'MHz' or 'GHz'
        """

        unit_list = ["HZ", "KHZ", "MHZ", "GHZ"]
        if unit.upper() in unit_list:
            self.write(":SOURce:FREQuency:SPAN " + str(value) + " " + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_freq_start(self, value: int | float, unit: str) -> None:
        """
        Sets start frequency for SWEep[1] to the value entered.

        Parameters
        ----------
        value : int | float
            Range: MIN to MAX
            Default: MIN
        unit : str
            Frequency Unit: 'Hz' or 'kHz' or 'MHz' or 'GHz'
        """

        unit_list = ["HZ", "KHZ", "MHZ", "GHZ"]
        if unit.upper() in unit_list:
            self.write(":SOURce:FREQuency:STARt " + str(value) + " " + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    def set_freq_stop(self, value: int | float, unit: str) -> None:
        """
        Sets stop frequency for SWEep[1] to the value entered.

        Parameters
        ----------
        value : int | float
            Range: MIN to MAX
            Default: MAX
        unit : str
            Frequency Unit: 'Hz' or 'kHz' or 'MHz' or 'GHz'
        """

        unit_list = ["HZ", "KHZ", "MHZ", "GHZ"]
        if unit.upper() in unit_list:
            self.write(":SOURce:FREQuency:STOP " + str(value) + " " + str(unit))
        else:
            raise ValueError("Unknown input! See function description for more info.")

    # =============================================================================
    # Pulse Modulation
    # =============================================================================
    def set_pm_bwidth(self, state: str) -> None:
        """
        Selects the phase modulation (ΦM) operating mode.
        The Narrow ΦM mode allows maximum deviations of ±3 radians for DC to 8 MHz rates.
        The Wide ΦM mode allows maximum deviations of ±400 radians for DC to 1 MHz rates.

        Parameters
        ----------
        state : str
            Default: ``MIN``
            * ``MIN`` = narrow mode
            * ``MAX`` = wide mode
        """

        valid_state = self._check_scpi_param(state, ["MIN", "MAX"])
        self.write(":SOURce:PM:BWIDth " + valid_state)

    def set_pm_internal_wave(self, state: str) -> None:
        """
        Selects the modulating waveform (from the internal ΦM generator) for the internal
        phase modulation function.

        Parameters
        ----------
        state : str
            Default: ``SINE``
            * ``SINE`` = Sine wave
            * ``GAUSsian`` = Gaussian noise
            * ``RDOWn`` = Negative ramp
            * ``RUP`` = Positive ramp
            * ``SQUare`` = Square wave
            * ``TRIangle`` = Triangle wave
            * ``UNIForm`` = Uniform noise
        """

        valid_list = ["SINE", "GAUSsian", "RDOWn", "RUP", "SQUare", "TRIangle", "UNIForm"]
        valid_state = self._check_scpi_param(state, valid_list)
        self.write(":SOURce:PM:INTernal:WAVE " + valid_state)

    def set_pm_internal_freq(self, value: int | float, unit: str) -> None:
        """
        Sets the frequency of the modulating waveform for the internal
        phase modulation (see :PM:INTernal:WAVE)

        Parameters
        ----------
        value : int | float
            Frequency
            Range: 0.1 Hz to 1 MHz for sine wave;
            0.1 Hz to 100 kHz for square, triangle, and ramp waveforms.
            Default: 1 kHz
        unit : str
            Unit of the frequency (Hz, kHz, MHz)
        """

        wave = self.get_pm_internal_wave().strip()

        multipliers = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6}
        if unit.upper() not in multipliers:
            raise ValueError(f"Invalid unit '{unit}'. Must be one of 'Hz', 'kHz', 'MHz'.")

        freq_hz = value * multipliers[unit.upper()]

        if wave == "SINE":
            if not (0.1 <= freq_hz <= 1e6):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 1 MHz) for SINE wave."
                )
        else:
            if not (0.1 <= freq_hz <= 100e3):
                raise ValueError(
                    f"Frequency {value} {unit} is out of range (0.1 Hz to 100 kHz) for {wave} wave."
                )

        self.write(f":SOURce:PM:INTernal:FREQuency {value} {unit}")

    def set_pm_state(self, state: str | int) -> None:
        """
        Enable/disable phase modulation of the MG369xC RF output signal.

        Parameters
        ----------
        state : str | int
            Default: ``OFF``
            * ``ON`` | ``OFF`` | ``1`` | ``0``
        """

        state = self._parse_state(state)
        self.write(":SOURce:PM:STATe " + str(state))

    # =============================================================================
    # Get/Save Data
    # =============================================================================
    def get_data(self) -> dict[str, float]:
        """
        Return a dictionary with the measured Power and CW Frequency.
        """
        return {
            "Power/dBm": self.get_output_power_level(),
            f"CW Frequency/{self.get_freq_unit().strip()}": self.get_freq_cw(),
        }
