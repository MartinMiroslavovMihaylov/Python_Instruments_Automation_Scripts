# #######################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!! The following code is an example code provided by Keysight !!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #######################################################################
# #######################################################################

import struct
import sys
import pyvisa as visa


class UXR_keysight:
    # Global variables (booleans: 0 = False, 1 = True).
    # ---------------------------------------------------------
    def __init__(self, resource_str):
        rm = visa.ResourceManager("C:\\Windows\\System32\\visa64.dll")
        instrument = rm.open_resource(resource_str)
        instrument.timeout = 20000
        instrument.clear()
        self.debug = 0

    # =========================================================
    # Initialize:
    # =========================================================
    def initialize(self):
        # Clear status.
        self.do_cooamnd("*CLS")
        # Get and display the device's *IDN? string.
        idn_string = self.do_query_string("*IDN?")
        print("Identification string: '%s'" % idn_string)
        # Load the default setup.
        self.do_cooamnd("*RST")

    # =========================================================
    # Capture:
    # =========================================================
    def capture(self):
        # Set probe attenuation factor.
        # self.do_cooamnd(":CHANnel1:PROBe 1.0")
        qresult = self.do_query_string(":CHANnel1:PROBe?")
        print("Channel 1 probe attenuation factor: %s" % qresult)
        # Use auto-scale to automatically set up oscilloscope.
        print("Autoscale.")
        self.do_cooamnd(":AUToscale")
        # Set trigger mode.
        self.do_cooamnd(":TRIGger:MODE EDGE")
        qresult = self.do_query_string(":TRIGger:MODE?")
        print("Trigger mode: %s" % qresult)
        # Set EDGE trigger parameters.
        self.do_cooamnd(":TRIGger:EDGE:SOURce CHANnel1")
        qresult = self.do_query_string(":TRIGger:EDGE:SOURce?")
        print("Trigger edge source: %s" % qresult)
        self.do_cooamnd(":TRIGger:LEVel CHANnel1,150E-3")
        qresult = self.do_query_string(":TRIGger:LEVel? CHANnel1")
        print("Trigger level, channel 1: %s" % qresult)
        self.do_cooamnd(":TRIGger:EDGE:SLOPe POSitive")
        qresult = self.do_query_string(":TRIGger:EDGE:SLOPe?")
        print("Trigger edge slope: %s" % qresult)
        # Save oscilloscope setup.
        setup_bytes = self.do_query_ieee_block(":SYSTem:SETup?")
        f = open("setup.set", "wb")
        f.write(setup_bytes)
        f.close()
        print("Setup bytes saved: %d" % len(setup_bytes))
        # Change oscilloscope settings with individual commands:
        # Set vertical scale and offset.
        self.do_cooamnd(":CHANnel1:SCALe 0.1")
        qresult = self.do_query_number(":CHANnel1:SCALe?")
        print("Channel 1 vertical scale: %f" % qresult)
        self.do_cooamnd(":CHANnel1:OFFSet 0.0")
        qresult = self.do_query_number(":CHANnel1:OFFSet?")
        print("Channel 1 offset: %f" % qresult)
        # Set horizontal scale and offset.
        self.do_cooamnd(":TIMebase:SCALe 200e-6")
        qresult = self.do_query_string(":TIMebase:SCALe?")
        print("Timebase scale: %s" % qresult)
        self.do_cooamnd(":TIMebase:POSition 0.0")
        qresult = self.do_query_string(":TIMebase:POSition?")
        print("Timebase position: %s" % qresult)
        # Set the acquisition mode.
        self.do_cooamnd(":ACQuire:MODE RTIMe")
        qresult = self.do_query_string(":ACQuire:MODE?")
        print("Acquire mode: %s" % qresult)
        # Or, set up oscilloscope by loading a previously saved setup.
        setup_bytes = ""
        f = open("setup.set", "rb")
        setup_bytes = f.read()
        f.close()
        self.do_cooamnd_ieee_block(":SYSTem:SETup", setup_bytes)
        print("Setup bytes restored: %d" % len(setup_bytes))
        # Set the desired number of waveform points,
        # and capture an acquisition.
        self.do_cooamnd(":ACQuire:POINts 32000")
        self.do_cooamnd(":DIGitize")

    # =========================================================
    # Analyze:
    # =========================================================
    def analyze(self):
        # Make measurements.
        # --------------------------------------------------------
        self.do_cooamnd(":MEASure:SOURce CHANnel1")
        qresult = self.do_query_string(":MEASure:SOURce?")
        print("Measure source: %s" % qresult)
        self.do_cooamnd(":MEASure:FREQuency")
        qresult = self.do_query_string(":MEASure:FREQuency?")
        print("Measured frequency on channel 1: %s" % qresult)
        self.do_cooamnd(":MEASure:VAMPlitude")
        qresult = self.do_query_string(":MEASure:VAMPlitude?")
        print("Measured vertical amplitude on channel 1: %s" % qresult)
        # Download the screen image.
        # --------------------------------------------------------
        screen_bytes = self.do_query_ieee_block(":DISPlay:DATA? PNG")
        # Save display data values to file.
        f = open("screen_image.png", "wb")
        f.write(screen_bytes)
        f.close()
        print("Screen image written to screen_image.png.")
        # Download waveform data.
        # --------------------------------------------------------
        # Get the waveform type.
        qresult = self.do_query_string(":WAVeform:TYPE?")
        print("Waveform type: %s" % qresult)
        # Get the number of waveform points.
        qresult = self.do_query_string(":WAVeform:POINts?")
        print("Waveform points: %s" % qresult)
        # Set the waveform source.
        self.do_cooamnd(":WAVeform:SOURce CHANnel1")
        qresult = self.do_query_string(":WAVeform:SOURce?")
        print("Waveform source: %s" % qresult)
        # Choose the format of the data returned:
        self.do_cooamnd(":WAVeform:FORMat BYTE")
        print("Waveform format: %s" % self.do_query_string(":WAVeform:FORMat?"))
        # Display the waveform settings from preamble:
        wav_form_dict = {
            0: "ASCii",
            1: "BYTE",
            2: "WORD",
            3: "LONG",
            4: "LONGLONG",
        }
        acq_type_dict = {
            1: "RAW",
            2: "AVERage",
            3: "VHIStogram",
            4: "HHIStogram",
            6: "INTerpolate",
            10: "PDETect",
        }
        acq_mode_dict = {
            0: "RTIMe",
            1: "ETIMe",
            3: "PDETect",
        }
        coupling_dict = {
            0: "AC",
            1: "DC",
            2: "DCFIFTY",
            3: "LFREJECT",
        }
        units_dict = {
            0: "UNKNOWN",
            1: "VOLT",
            2: "SECOND",
            3: "CONSTANT",
            4: "AMP",
            5: "DECIBEL",
        }
        preamble_string = self.do_query_string(":WAVeform:PREamble?")
        (
            wav_form,
            acq_type,
            wfmpts,
            avgcnt,
            x_increment,
            x_origin,
            x_reference,
            y_increment,
            y_origin,
            y_reference,
            coupling,
            x_display_range,
            x_display_origin,
            y_display_range,
            y_display_origin,
            date,
            time,
            frame_model,
            acq_mode,
            completion,
            x_units,
            y_units,
            max_bw_limit,
            min_bw_limit,
        ) = preamble_string.split(",")
        print("Waveform format: %s" % wav_form_dict[int(wav_form)])
        print("Acquire type: %s" % acq_type_dict[int(acq_type)])
        print("Waveform points desired: %s" % wfmpts)
        print("Waveform average count: %s" % avgcnt)
        print("Waveform X increment: %s" % x_increment)
        print("Waveform X origin: %s" % x_origin)
        print("Waveform X reference: %s" % x_reference)  # Always 0.
        print("Waveform Y increment: %s" % y_increment)
        print("Waveform Y origin: %s" % y_origin)
        print("Waveform Y reference: %s" % y_reference)  # Always 0.
        print("Coupling: %s" % coupling_dict[int(coupling)])
        print("Waveform X display range: %s" % x_display_range)
        print("Waveform X display origin: %s" % x_display_origin)
        print("Waveform Y display range: %s" % y_display_range)
        print("Waveform Y display origin: %s" % y_display_origin)
        print("Date: %s" % date)
        print("Time: %s" % time)
        print("Frame model #: %s" % frame_model)
        print("Acquire mode: %s" % acq_mode_dict[int(acq_mode)])
        print("Completion pct: %s" % completion)
        print("Waveform X units: %s" % units_dict[int(x_units)])
        print("Waveform Y units: %s" % units_dict[int(y_units)])
        print("Max BW limit: %s" % max_bw_limit)
        print("Min BW limit: %s" % min_bw_limit)
        # Get numeric values for later calculations.
        x_increment = self.do_query_number(":WAVeform:XINCrement?")
        x_origin = self.do_query_number(":WAVeform:XORigin?")
        y_increment = self.do_query_number(":WAVeform:YINCrement?")
        y_origin = self.do_query_number(":WAVeform:YORigin?")
        # Get the waveform data.
        self.do_cooamnd(":WAVeform:STReaming OFF")
        sData = self.do_query_ieee_block(":WAVeform:DATA?")
        # Unpack signed byte data.
        values = struct.unpack("%db" % len(sData), sData)
        print("Number of data values: %d" % len(values))
        # Save waveform data values to CSV file.
        f = open("waveform_data.csv", "w")
        for i in range(0, len(values) - 1):
            time_val = x_origin + (i * x_increment)
            voltage = (values[i] * y_increment) + y_origin
            f.write("%E, %f\n" % (time_val, voltage))
        f.close()
        print("Waveform format BYTE data written to waveform_data.csv.")

    # =========================================================
    # Send a command and check for errors:
    # =========================================================
    def do_cooamnd(self, command, hide_params=False):
        if hide_params:
            (header, data) = command.split(" ", 1)
            if self.debug:
                print("\nCmd = '%s'" % header)
        else:
            if self.debug:
                print("\nCmd = '%s'" % command)
        self.instrument.write("%s" % command)
        if hide_params:
            self.check_instrument_errors(header)
        else:
            self.check_instrument_errors(command)

    # =========================================================
    # Send a command and binary values and check for errors:
    # =========================================================
    def do_cooamnd_ieee_block(self, command, values):
        if self.debug:
            print("Cmb = '%s'" % command)
        self.instrument.write_binary_values("%s " % command, values, datatype="B")
        self.check_instrument_errors(command)

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
    def do_query_string(self, query):
        if self.debug:
            print("Qys = '%s'" % query)
        result = self.instrument.query("%s" % query)
        self.check_instrument_errors(query)
        return result

    # =========================================================
    # Send a query, check for errors, return floating-point value:
    # =========================================================
    def do_query_number(self, query):
        if self.debug:
            print("Qyn = '%s'" % query)
        results = self.instrument.query("%s" % query)
        self.check_instrument_errors(query)
        return float(results)

    # =========================================================
    # Send a query, check for errors, return binary values:
    # =========================================================
    def do_query_ieee_block(self, query):
        if self.debug:
            print("Qyb = '%s'" % query)
        result = self.instrument.query_binary_values(
            "%s" % query, datatype="s", container=bytes
        )
        self.check_instrument_errors(query, exit_on_error=False)
        return result

    # =========================================================
    # Check for instrument errors:
    # =========================================================
    def check_instrument_errors(self, command, exit_on_error=True):
        while True:
            error_string = self.instrument.query(":SYSTem:ERRor? STRing")
            if error_string:  # If there is an error string value.
                if error_string.find("0,", 0, 2) == -1:  # Not "No error".
                    print("ERROR: %s, command: '%s'" % (error_string, command))
                    if exit_on_error:
                        print("Exited because of error.")
                        sys.exit(1)
                else:  # "No error"
                    break
            else:  # :SYSTem:ERRor? STRing should always return string.
                print(
                    "ERROR: :SYSTem:ERRor? STRing returned nothing, command: '%s'"
                    % command
                )
                print("Exited because of error.")
                sys.exit(1)


# =========================================================
# Main program:
# =========================================================
myUXR = UXR_keysight("TCPIP0::141.121.231.13::hislip0::INSTR")
# Initialize the oscilloscope, capture data, and analyze.
myUXR.initialize()
myUXR.capture()
myUXR.analyze()
myUXR.instrument.close()
print("End of program.")
