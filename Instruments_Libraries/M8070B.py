# -*- coding: utf-8 -*-
"""
Created on Mon Jul  21 18:56:32 2025

@author: Maxim Weizel
"""


import numpy as np
import pyvisa as visa
import matlab


class M8070B:
    """
    Start the M8070B Software. Go to Utilities-> SCPI Server Information.
    Copy the VISA resource string (usually localhost).
    """

    def __init__(self, resource_str="TCPIP0::localhost::hislip0::INSTR"):
        self._resource = visa.ResourceManager().open_resource(str(resource_str), query_delay=0.5)
        self._channelLS = [1, 2]  #
        self._StateLS_mapping = {"on": 1, "off": 0, 1: 1, 0: 0, "1": 1, "0": 0, True: 1, False: 0}
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

    def _validate_state(self, state: int | str) -> int:
        state_normalized = self._StateLS_mapping.get(
            state.lower() if isinstance(state, str) else int(state)
        )
        if state_normalized is None:
            raise ValueError("Invalid state given! State can be [on,off,1,0,True,False].")
        return state_normalized

    # =============================================================================
    # M8199B - Get Values and Modes
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

    def get_output_state(self, channel: int) -> int:
        """Returns the output state for the selected channel.

        Parameters
        ----------
        channel : int
            Channel 1 or 2

        Returns
        -------
        int
            Output state. 0 or 1.
        """
        channel = self._validate_channel(channel)
        return int(self.query(f":OUTPut:STATe? 'M2.DataOut{channel}'"))

    def get_delay(self, channel: int) -> float:
        """Returns the delay for the selected channel in seconds.

        Parameters
        ----------
        channel : int
            Channel 1 or 2

        Returns
        -------
        float
            Delay in seconds.
        """
        channel = self._validate_channel(channel)
        return float(self.query(f":ARM:DELay? 'M2.DataOut{channel}'"))

    # =============================================================================
    # M8199B - Set Values and Modes
    # =============================================================================

    def set_amplitude(self, channel: int, amplitude: int | float) -> None:
        """Differential amplitude setting for the selected channel.

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        amplitude : int/float
            Amplitude setting in V. Must be between 0.1 and 2.7 V
        """
        channel = self._validate_channel(channel)
        if 0.1 <= amplitude <= 2.7:
            self.write(f":SOURce:VOLTage:AMPLitude 'M2.DataOut{channel}', {amplitude}")
        else:
            raise ValueError(f"Value must be between 0.1 and 2.7 V. You entered: {amplitude} V")

    def set_rf_power(self, channel: int, powerdBm: int | float) -> None:
        """Sets the Signal Generator Output Power in dBm.

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        power : int/float
            Output Power in dBm
        """
        power_watt = 10 ** (powerdBm / 10) * 1e-3
        V_rms = (50 * power_watt) ** 0.5  # 50 Ohm System
        amplitude = V_rms * np.sqrt(2)
        self.set_amplitude(channel, amplitude)

    def set_OutputPowerLevel(self, channel: int, powerdBm: int | float) -> None:
        """Sets the Signal Generator Output Power in dBm. Alias for set_rf_power().

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        value : int/float
            Output Power in dBm
        """
        self.set_rf_power(channel, powerdBm)

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
        state_normalized = self._validate_state(state)
        self.write(f":OUTPut:STATe 'M2.DataOut{channel}', {state_normalized}")

    def set_rf_output(self, channel: int, state: int | str) -> None:
        """Activate or deactivate the selected channel output.
        Alias for set_output().
        """
        self.set_output(channel, state)

    def set_delay(self, channel: int, delay: float) -> None:
        """Set the delay for the selected channel in seconds.

        Parameters
        ----------
        channel : int
            Channel 1 or 2
        delay : float
            Delay in seconds.
        """
        channel = self._validate_channel(channel)
        if not (-25e-9 <= delay <= 25e-9):
            raise ValueError(f"Delay must be between -25 and 25ns. You entered: {delay} s")
        self.write(f":ARM:DELay 'M2.DataOut{channel}',{delay}")

    # =============================================================================
    # M8008A Clock Module - Get Values and Modes
    # =============================================================================

    def get_sample_clk_out_frequency(self, channel: int = 1) -> float:
        """Returns the sample clock OUT1 or OUT2 frequency from the M8008A CLK module.
        Both freqeuncies are the same.

        Parameters
        ----------
        channel : int, optional
            1 or 2, by default 1

        Returns
        -------
        float
            Sample clock output frequency in Hz.
        """
        channel = self._validate_channel(channel)
        return float(self.query(f":OUTPut:FREQuency? 'M1.SampleClkOut{channel}'"))

    def get_sample_clk_out2_state(self) -> int:
        """Returns the sample clock OUT2 state from the M8008A CLK module.
        Sample clock OUT1 cannot be turned off.

        Returns
        -------
        int
            Sample clock output state. 0 or 1.
        """
        channel = self._validate_channel(channel)
        return int(self.query(f":OUTPut:STATe? 'M1.SampleClkOut2'"))

    def get_sample_clk_out2_power(self) -> float:
        """Returns the sample clock OUT2 Power in dBm from the M8008A CLK module.
        Sample clock OUT1 cannot be influenced.

        Returns
        -------
        float
            Sample Clock OUT2 Power in dBm.
        """
        return float(self.query(f":OUTPut:POWer? 'M1.SampleClkOut2'"))

    # =============================================================================
    # M8008A Clock Module - Set Values and Modes
    # =============================================================================

    def set_sample_clk_out2_state(self, state: int | str) -> None:
        """Sets the sample clock OUT2 state from the M8008A CLK module.
        Sample clock OUT1 cannot be turned off.

        Parameters
        ----------
        state : int | str
            One of: 0, 1, "off", "on"
        """
        state_normalized = self._validate_state(state)
        self.write(f":OUTPut:STATe 'M1.SampleClkOut2', {state_normalized}")

    def set_sample_clk_out2_power(self, power: int | float) -> None:
        """Sets the sample clock OUT2 Power in dBm from the M8008A CLK module.
        Sample clock OUT1 cannot be influenced.

        Parameters
        ----------
        power : int | float
            Sample Clock OUT2 Power in dBm.
            Must be between -5 and 12 dBm
        """
        if not (-5 <= power <= 12):
            raise ValueError(f"Power must be between -5 and 12 dBm. You entered: {power} dBm")
        self.write(f":SOURce:POWer 'M1.SampleClkOut2',{power}")

    # =============================================================================
    # M8199B Calling IQTools Functions
    # =============================================================================

    def set_freq_CW(
        self,
        matlab_engine,
        channel: int,
        frequency: float,
        correction: int = 0,
        run: int = 1,
        fs: float = 256e9,
    ) -> None:
        """Set the CW tone frequency on the AWG via MATLAB engine.

        Parameters
        ----------
        matlab_engine : matlab.engine
            An active MATLAB engine session.
        channel : int
            AWG channel (1 or 2).
        frequency : float
            Tone frequency in Hz.
        correction : int, optional
            Enable correction (default 0).
        run : int, optional
            AWG run number (default 1).
        fs : float, optional
            AWG sample rate (default 256e9).
        """
        # 1) Validate channel
        channel = self._validate_channel(channel)

        # 2) Define constants
        # magnitude is zeros(1,1) in MATLAB; make it a 1×1 double
        magnitude = matlab.double([[0]])  # in dB

        # fmt: off
        # 3) Build channelMapping
        # MATLAB expects numeric arrays, not raw Python lists
        if channel == 1:
            py_map = [[1, 0],
                    [0, 0]]
        else:
            py_map = [[0, 0],
                    [1, 0]]
        channel_mapping = matlab.double(py_map)

        # 4) Call iqtone to generate the IQ vector
        #    We ask for 5 outputs so that the last one is chMap.
        iqdata, _, _, _, chMap = matlab_engine.iqtone(
            'sampleRate',       fs,
            'numSamples',       0,
            'tone',             frequency,
            'phase',            'Random',
            'normalize',        1,
            'magnitude',        magnitude,
            'correction',       correction,
            'channelMapping',   channel_mapping,
            nargout=5
        )

        # 6) Push the generated IQ out to the AWG
        matlab_engine.iqdownload(
            iqdata,
            fs,
            'channelMapping', chMap,
            'segmentNumber',  1,
            'run',            run,
            nargout=0
        )
        # fmt: on

    def iqdownload(
        self,
        matlab_engine,
        iqdata,
        fs: float,
        *,
        segment_number: int = 1,
        normalize: bool = True,
        channel_mapping=None,
        sequence=None,
        marker=None,
        arb_config=None,
        keep_open: bool = False,
        run: bool = True,
        segment_length=None,
        segment_offset=None,
        lo_amplitude=None,
        lo_f_center=None,
        segm_name=None,
        rms=None,
    ) -> any:
        """
        Download a pre-generated IQ waveform to the AWG.

        Parameters
        ----------
        matlab_engine : matlab.engine
            Active MATLAB engine session.
        iqdata : array-like
            Real or complex samples (each column = one waveform).  Can be empty for a connection check.
        fs : float
            Sample rate in Hz.
        segment_number : int, optional
            Which segment to download into (default=1).
        normalize : bool, optional
            Auto-scale to DAC range (default=True).
        channel_mapping : array-like, optional
            2xM logical matrix mapping IQ data columns to AWG channels.
        sequence : any, optional
            Sequence table descriptor.
        marker : array-like of int, optional
            Marker bits per sample.
        arb_config : struct, optional
            AWG configuration struct (default from arbConfig file).
        keep_open : bool, optional
            If True, leave connection open after download (default=False).
        run : bool, optional
            If True, start AWG immediately after download (default=True).
        segment_length, segment_offset, lo_amplitude, lo_f_center, segm_name, rms :
            Other advanced options as per MATLAB doc.

        Returns
        -------
        result
            The output of the MATLAB `iqdownload` call (empty or status).
        """
        # fmt: off
        # Build the var/val list
        args = [
            'segmentNumber', int(segment_number),
            'normalize',   int(normalize),
            'keepOpen',    int(keep_open),
            'run',         int(run)
        ]
        # fmt: on
        if channel_mapping is not None:
            args += ["channelMapping", channel_mapping]
        if sequence is not None:
            args += ["sequence", sequence]
        if marker is not None:
            args += ["marker", marker]
        if arb_config is not None:
            args += ["arbConfig", arb_config]
        if segment_length is not None:
            args += ["segmentLength", segment_length]
        if segment_offset is not None:
            args += ["segmentOffset", segment_offset]
        if lo_amplitude is not None:
            args += ["loAmplitude", lo_amplitude]
        if lo_f_center is not None:
            args += ["loFcenter", lo_f_center]
        if segm_name is not None:
            args += ["segmName", segm_name]
        if rms is not None:
            args += ["rms", rms]

        # Call MATLAB
        result = matlab_engine.iqdownload(iqdata, fs, *args, nargout=1)
        return result
