#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 20:17:32 2024

@author: Maxim Weizel
"""

import numpy as np
import pyvisa as visa


class UXR:
    """
    This class is using pyvisa to connect to Instruments. Please install PyVisa before using it.
    """

    def __init__(
        self,
        resource_str="TCPIP0::KEYSIGH-Q75EBO9.local::hislip0::INSTR",
        num_channel=2,
    ):
        self.instrument = visa.ResourceManager().open_resource(
            str(resource_str), read_termination="\n", query_delay=0.5
        )
        print(self.instrument.query("*IDN?"))

        # Internal Variables
        self._types_channel = list(range(1, num_channel + 1))
        self._waveform_format = "ASC"

    def query(self, message):
        return self.instrument.query(message)

    def query_binary_values(
        self, message, datatype="h", container=np.array, data_points=int(0), **kwargs
    ):
        return self.instrument.query_binary_values(
            message,
            datatype=datatype,
            container=container,
            data_points=data_points,
            **kwargs,
        )

    def write(self, message):
        return self.instrument.write(message)

    def Close(self):
        self.instrument.close()

    # =============================================================================
    # * (Common) Commands
    # =============================================================================

    def clear_status(self) -> None:
        """The *CLS command clears all status and error registers."""
        self.write("*CLS")

    def IDN(self) -> str:
        """The *IDN? query returns the company name, oscilloscope model number, serial
        number, and software version by returning this string:
        Keysight Technologies,<Model #>,<USXXXXXXXX>,<Rev #>[,<Options>]

            Returns
            -------
            str
                Keysight Technologies,DSO9404A,USXXXXXXXX,XX.XX.XXXX
        """
        return self.query("*IDN?")

    def OPC(self) -> int:
        """Places a “1” into the output queue when all device
        operations have been completed
        Returns
        -------
        TYPE str
            1 or 0
        """
        return int(self.query("*OPC?"))

    def reset(self) -> None:
        """The *RST command performs a default setup which is the same as pressing the
        oscilloscope front panel [Default Setup] key.
        """
        self.write("*RST")

    # =============================================================================
    # : (Root Level) Commands
    # =============================================================================
    def aquisition_done(self) -> int:
        """The :ADER? query reads the Acquisition Done Event Register and returns 1 or 0.
        After the Acquisition Done Event Register is read, the register is cleared. The
        returned value 1 indicates an acquisition completed event has occurred and 0
        indicates an acquisition completed event has not occurred.

        Returns
        -------
        int
            {1 | 0}
        """
        return int(self.query(":ADER?"))
    
    def aquisition_state(self) -> str:
        """The :ASTate? query returns the acquisition state.

        Returns
        -------
        str
            {ARM | TRIG | ATRIG | ADONE}
        """
        return self.query(":ASTate?")

    def autoscale(self) -> None:
        """The :AUToscale command causes the oscilloscope to evaluate all input waveforms
        and find the optimum conditions for displaying the waveform.
        """
        self.write(":AUToscale")

    def autoscale_channels(self, value: str | None = None) -> str:
        """The :AUToscale:CHANnels command selects whether to apply autoscale to all of
        the input channels or just the input channels that are currently displayed.
            Parameters
            ----------
            value : str, optional
                {ALL | DISPlayed}, if None then query

            Returns
            -------
            str
                {ALL | DISP}

            Raises
            ------
            ValueError
                Expected one of: {ALL | DISP | DISPlayed }
        """
        _types = ["ALL", "DISPLAYED", "DISP"]
        if value is not None:
            if value.upper() not in _types:
                raise ValueError("Invalid Argument. Expected one of: %s" % _types)
            self.write(f":AUToscale:CHANnels {value}")
        else:  # Query
            return self.query(":AUToscale:CHANnels?")

    def digitize(self, channel_num: int | None = None) -> None:
        """This command initializes the selected channels or functions, then acquires
        them according to the current oscilloscope settings. When all waveforms are
        completely acquired, the oscilloscope is stopped.
        To Do: input can be: [CHANnel<N> | DIFF<D> | COMMonmode<C>]

            Parameters
            ----------
            channel_num : int
                Number of the Channel

            Raises
            ------
            channel_numError
                Expected one of: channel number
        """
        if channel_num is not None:
            if int(channel_num) not in self._types_channel:
                raise ValueError(
                    "Invalid Argument. Expected one of: %s" % self._types_channel
                )
            self.write(f":DIGitize CHANnel{channel_num}")
        else:
            self.write(":DIGitize")

    def run_state(self) -> str:
        """The :RSTate? query returns the run state:

        Returns
        -------
        str
            {RUN | STOP | SING}
        """
        return self.query(":RSTate?")

    def run(self) -> None:
        """
        Set the scope in run mode.
        """

        self.write(":RUN")

    def single(self) -> None:
        """
        Take a single acquisition
        """
        self.write(":SING")

    def status(self, key: str | None = None, value: int | None = None) -> int:
        """The :STATus? query shows whether the specified channel, function, wmemory,
        histogram, measurement trend, measurement spectrum, or equalized waveform is
        on or off.
        To Do: Each type has a different range of values that is excepted. No Checking
        is implemented.

            Parameters
            ----------
            key : str, optional
                if None return status of Channel1
            value : int, optional
                For Channel [1,2], for Function <=16

            Returns
            -------
            int
                A return value of 1 means on and a return value of 0 means off

            Raises
            ------
            ValueError
                Expected one of: CHANNEL, FUNCTION, HIST, ... etc.
        """
        _types_key = [
            "CHAN",
            "CHANNEL",
            "DIFF",
            "COMM",
            "COMMONMODE",
            "FUNC",
            "FUNCTION",
            "HIST",
            "HISTOGRAM",
            "WMEM",
            "WMEMORY",
            "CLOC",
            "CLOCK" "MTR",
            "MTREND",
            "MSP",
            "MSPECTRUM",
            "EQU",
            "EQUALIZED",
            "XT",
        ]
        if key is not None:
            if key.upper() not in _types_key:
                raise ValueError("Invalid Argument. Expected one of: %s" % _types_key)
            if int(value) <= 16:  # For CHAN <=2, for FUNC <=16, ... etc.
                return int(self.query(f":STATus? {key}{value}"))
        else:
            return int(self.query(f":STATus? CHANnel1"))

    def stop(self) -> None:
        """
        Set the scope in stop mode.
        """
        self.write(":STOP")

    # =============================================================================
    # :CHANnel<N> Commands
    # =============================================================================

    def channel_display(
        self, channel: int, write: bool = False, value: int | str | None = None
    ) -> int:
        """The :CHANnel<N>:DISPlay command turns the display of the specified channel on
        or off.

            Parameters
            ----------
            channel : int
                An integer, analog input channel 1 or 2
            write : bool, optional
                write the channel display state, else query
            value : int, str, optional
                ON, 1, OFF, 0


            Returns
            -------
            int
                The :CHANnel<N>:DISPlay? query returns the current display condition for the
                specified channel

            Raises
            ------
            ValueError
                For Channel expected one of: num_channels
            ValueError
                For values expected one of: ON, 1, OFF, 0
        """
        _type_value = ["ON", 1, "OFF", 0]
        if int(channel) not in self._types_channel:
            raise ValueError(
                "Invalid Argument. Expected one of: %s" % self._types_channel
            )
        if write:
            if isinstance(value, str):
                value = value.upper()
            if value not in _type_value:
                raise ValueError("Invalid Argument. Expected one of: %s" % _type_value)
            self.write(f":CHANnel{channel}:DISPlay {value}")
        else:  # query
            return int(self.query(f":CHANnel{channel}:DISPlay?"))

    def channel_range(
        self, channel: int, write: bool = False, range_value: float | None = None
    ) -> float:
        """The :CHANnel<N>:RANGe command defines the full-scale vertical axis of the
        selected channel. The values represent the full-scale deflection
        factor of the vertical axis in volts. These values change as the probe attenuation
        factor is changed.

            Parameters
            ----------
            channel : int
                An integer, analog input channel 1 or 2
            write : bool, optional
                write else query, by default False
            range_value : float, optional
                A real number for the full-scale voltage of the specified channel number,
                by default None

            Returns
            -------
            float
                full-scale vertical axis of the selected channel

            Raises
            ------
            ValueError
                For Channel expected one of: num_channels
            ValueError
                For range_value expected to be < 2V
        """
        if int(channel) not in self._types_channel:
            raise ValueError(
                "Invalid Argument. Expected one of: %s" % self._types_channel
            )
        if write:
            if range_value <= 4:  # 2V Full Scale Range
                self.write(f":CHANnel{channel}:RANGe {range_value}")
            else:
                raise ValueError("Invalid Argument. Expected to be <= 4V")
        else:  # query
            return float(self.query(f":CHANnel{channel}:RANGe?"))

    def channel_scale(
        self, channel: int, write: bool = False, scale_value: float | None = None
    ) -> float:
        """The :CHANnel<N>:SCALe command sets the vertical scale, or units per division, of
        the selected channel. This command is the same as the front-panel channel scale.

            Parameters
            ----------
            channel : int
                An integer, analog input channel 1 or 2
            write : bool, optional
                write else query, by default False
            scale_value : float, optional
                A real number for the vertical scale of the channel in units per division,
                by default None

            Returns
            -------
            float
                A real number for the vertical scale of the channel in units per division

            Raises
            ------
            ValueError
                For Channel expected one of: num_channels
            ValueError
                For range_value expected to be < 500mV/div
        """
        if int(channel) not in self._types_channel:
            raise ValueError(
                "Invalid Argument. Expected one of: %s" % self._types_channel
            )
        if write:
            if scale_value <= 0.5:  # 500mV/div Scale
                self.write(f":CHANnel{channel}:SCALe {scale_value}")
            else:
                raise ValueError("Invalid Argument. Expected to be <= 500mV/div")
        else:  # query
            return float(self.query(f":CHANnel{channel}:SCALe?"))

    # =============================================================================
    # :SYSTem Commands
    # =============================================================================

    def system_header(self, value: int | str | None = None) -> int:
        """!!!! SHOULD BE OFF !!!!
        The :SYSTem:HEADer command specifies whether the instrument will output a
        header for query responses. When :SYSTem:HEADer is set to ON, the query
        responses include the command header.


            Parameters
            ----------
            value : int | str | None, optional
                {{ON | 1} | {OFF | 0}}, by default None

            Returns
            -------
            int
                {1 | 0}

            Raises
            ------
            ValueError
                Expected one of: {{ON | 1} | {OFF | 0}}
        """
        _type_value = ["ON", 1, "OFF", 0]
        if value is not None:
            if isinstance(value, str):
                value = value.upper()
            if value not in _type_value:
                raise ValueError("Invalid Argument. Expected one of: %s" % _type_value)
            self.write(f":SYSTem:HEADer {value}")
        else:  # query
            return int(self.query(":SYSTem:HEADer?"))

    # =============================================================================
    # :WAVeform Commands
    # =============================================================================

    def waveform_byteorder(self, value: str | None = None) -> str:
        """The :WAVeform:BYTeorder command selects the order in which bytes are
        transferred from (or to) the oscilloscope using WORD and LONG formats

            Parameters
            ----------
            value : str, optional
                byteorder {MSBF, LSBF}, by default None

            Returns
            -------
            str
                byteorder {MSBF, LSBF}

            Raises
            ------
            ValueError
                Expected one of: MSBFIRST, LSBFIRST
        """
        _types = ["MSBF", "MSBFIRST", "LSBF", "LSBFIRST"]
        if value is not None:
            if value.upper() not in _types:
                raise ValueError("Invalid Argument. Expected one of: %s" % _types)
            self.write(f":WAVeform:BYTeorder {value}")
        else:  # Query
            return self.query(":WAVeform:BYTeorder?")

    def waveform_data(
        self,
        start: int | None = None,
        size: int | None = None,
        datatype: str = "h",
        container: type = np.array,
        data_points: int = 0,
        **kwargs,
    ) -> np.ndarray:
        """
        The :WAVeform:DATA? query outputs waveform data to the computer over the
        remote interface. The data is copied from a waveform memory, function, or
        channel previously specified with the :WAVeform:SOURce command.

        Parameters
        ----------
        start : int, optional
            Starting point in the source memory for the first waveform point to transfer, by default None.
        size : int, optional
            Number of points in the source memory to transfer. If larger than available data,
            size is adjusted to the maximum available, by default None.
        datatype : str, optional
            Data type for binary values as defined in Python struct, by default "h" (short).
        container : type, optional
            Type of container to hold the data, by default np.array.
        data_points : int, optional
            Expected number of data points, by default 0.
        kwargs : dict, optional
            Additional arguments passed to the query_binary_values method.

        Returns
        -------
        np.ndarray
            Acquired data.

        Raises
        ------
        ValueError
            If `start` or `size` are invalid (non-integers or negative).
        NotImplementedError
            If the waveform format is not "WORD".
        """
        # Validate start and size
        if start is not None and (not isinstance(start, int) or start < 0):
            raise ValueError("`start` must be a non-negative integer.")
        if size is not None and (not isinstance(size, int) or size < 0):
            raise ValueError("`size` must be a non-negative integer.")

        # Construct the SCPI message
        if start is not None and size is not None:
            message = f":WAVeform:DATA? {start},{size}"
        elif start is not None:
            message = f":WAVeform:DATA? {start}"
        else:
            message = ":WAVeform:DATA?"

        # Query the waveform data
        if self._waveform_format == "WORD":
            try:
                return self.query_binary_values(
                message,
                datatype=datatype,
                container=container,
                data_points=data_points,
                **kwargs,
            )
            except Exception as e:
                print("Error:", e)
            
        else:
            raise NotImplementedError(
                f"Unsupported waveform format: {self._waveform_format}. "
                "Only 'WORD' format is currently supported."
            )

    def waveform_format(self, value: str | None = None) -> str:
        """The :WAVeform:FORMat command sets the data transmission mode for waveform
        data output. This command controls how the data is formatted when it is sent from
        the oscilloscope, and pertains to all waveforms.
        To Do: Only WORD is tested. There is a FLOAT type?

            Parameters
            ----------
            value : str, optional
                One of {ASCii | BINary | BYTE | WORD }, by default None

            Returns
            -------
            str
                {ASC | BIN | BYTE | WORD }

            Raises
            ------
            ValueError
                Expected one of: {ASCii | BINary | BYTE | WORD}
        """
        _types = ["ASC", "ASCII", "BIN", "BINARY", "BYTE", "WORD"]
        if value is not None:
            if value.upper() not in _types:
                raise ValueError("Invalid Argument. Expected one of: %s" % _types)
            self.write(f":WAVeform:FORMat {value}")
            self._waveform_format = value.upper()
        else:  # Query
            self._waveform_format = self.query(":WAVeform:FORMat?").upper()
            return self._waveform_format

    def waveform_points(self) -> int:
        """The :WAVeform:POINts? query returns the points value in the current waveform
        preamble.

            Returns
            -------
            int
                Number of points in the current waveform
        """
        return int(self.query(":WAVeform:POINts?"))

    def waveform_source(self, key: str | None = None, value: int | None = None) -> str:
        """The :WAVeform:SOURce command selects a channel, function, waveform
        memory, or histogram as the waveform source
        To Do: No checkes implemented

            Parameters
            ----------
            key : str | None, optional
                One of: {CHANnel<N> | DIFF<D> | COMMonmode<C> | FUNCtion<F> | HISTogram |
                WMEMory<R> | CLOCk | MTRend | MSPectrum | EQUalized | XT<X> | PNOise |
                INPut | CORRected | ERRor | LFPR | NREDuced}, by default None
            value : int | None, optional
                Number e.g. 1 for Channel1, by default None

            Returns
            -------
            str
                The :WAVeform:SOURce? query returns the currently selected waveform source.
        """
        if key is not None and value is not None:
            self.write(f":WAVeform:SOURce {key}{value}")
        else:
            return self.query(":WAVeform:SOURce?")

    def waveform_streaming(self, value: int | str | None = None) -> int:
        """When enabled, :WAVeform:STReaming allows more than 999,999,999 bytes of
        data to be transferred from the Infiniium oscilloscope to a PC when using the
        :WAVeform:DATA? query.

            Parameters
            ----------
            value : int | str | None, optional
                {{ON | 1} | {OFF | 0}}, by default None

            Returns
            -------
            int
                {1 | 0}

            Raises
            ------
            ValueError
                Expected one of: {{ON | 1} | {OFF | 0}}
        """
        _type_value = ["ON", 1, "OFF", 0]
        if value is not None:
            if isinstance(value, str):
                value = value.upper()
            if value not in _type_value:
                raise ValueError("Invalid Argument. Expected one of: %s" % _type_value)
            self.write(f":WAVeform:STReaming {value}")
        else:  # query
            return int(self.query(":WAVeform:STReaming?"))

    def waveform_x_increment(self) -> float:
        """The :WAVeform:XINCrement? query returns the duration between consecutive
        data points for the currently specified waveform source.

        Returns
        -------
        float
            A real number representing the duration between data points on the X axis.
        """
        return float(self.query(":WAVeform:XINCrement?"))

    def waveform_x_origin(self) -> float:
        """The :WAVeform:XORigin? query returns the X-axis value of the first data point in
        the data record.

        Returns
        -------
        float
            A real number representing the X-axis value of the first data point in the data
            record.
        """
        return float(self.query(":WAVeform:XORigin?"))

    def waveform_y_increment(self) -> float:
        """The :WAVeform:YINCrement? query returns the y-increment voltage value for the
        currently specified source.

        Returns
        -------
        float
            A real number in exponential format.
        """
        return float(self.query(":WAVeform:YINCrement?"))

    def waveform_y_origin(self) -> float:
        """The :WAVeform:YORigin? query returns the y-origin voltage value for the currently
        specified source. The voltage value returned is the voltage value represented by
        the waveform data digital code 00000.

        Returns
        -------
        float
            A real number in exponential format.
        """
        return float(self.query(":WAVeform:YORigin?"))
