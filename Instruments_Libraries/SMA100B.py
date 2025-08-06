#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""
Created on Fir Feb 02 13:00:00 2024

@author: mweizel
"""

import numpy as np
import vxi11



class SMA100B(vxi11.Instrument):
    '''
    A class thats uses vxi11 library to interface a SMA100B
    Need to have python 'vxi11' library installed!

    '''

    def __init__(self, hostname):
        '''
        Get name and identification.
        Execute the reset() command if you want to get the instrument 
        to default settings.
        '''
        super().__init__(hostname)

        # Predefine Lists
        self._StateLS_mapping = {
            "on": 1,
            "off": 0,
            1: 1,
            0: 0,
            "1": 1,
            "0": 0,
            True: 1,
            False: 0,
        }

        # Get name and identification
        print(self.getIdn())

    def query(self, message):
        return self.ask(message)

    def Close(self):
        print("Instrument Rohde&Schwarz SMA100B is closed!")
        return self.close()

    def reset(self):
        return self.write('*RST')
    
# =============================================================================
# Validate Variables
# =============================================================================

    def _validate_state(self, state: int | str) -> int:
        state_normalized = self._StateLS_mapping.get(
            state.lower() if isinstance(state, str) else int(state)
        )
        if state_normalized is None:
            raise ValueError("Invalid state given! State can be [on,off,1,0,True,False].")
        return state_normalized
    
# =============================================================================
# Get Identication Command
# =============================================================================
    def getIdn(self) -> str:
        '''
        
        Returns
        -------
        str
            Instrument identification.

        '''
        return self.query('*IDN?')
    
# =============================================================================
# Ask Commands
# =============================================================================

    def ask_OutputImpedance(self) -> float:
        """
        
        Returns
        -------
        float
            Queries the impedance of the RF output.

        """
        return float(self.query(":OUTPut1:IMP?"))


# =============================================================================
# Set Commands
# =============================================================================

    def set_rf_output_all(self, state: int | str) -> None:
        """Activates all Signal Genrator RF Outputs

        Parameters
        ----------
        state : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        state = self._validate_state(state)
        self.write(f':OUTPut:ALL:STATe {state}')


    def set_rf_output(self, state: int | str) -> None:
        """Activates the Signal Genrator RF Output

        Parameters
        ----------
        state : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        state = self._validate_state(state)
        self.write(f':OUTPut {state}')


    def set_output(self,state: int | str) -> None:
        """Activates the Signal Genrator RF Output

        Parameters
        ----------
        state : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        self.set_rf_output(state)

    def set_DCOffset(self, value: int | float) -> None:
        """
        

        Parameters
        ----------
        value : int/float
            Sets the value of the DC offset.
            Range: -5 to 5
            Increment: 0.001

        Returns
        -------
        None.

        """
        if value >= -5 and value <= 5:
            self.write(f":CSYNthesis:OFFSet {value}")
        else:
            raise ValueError("Allowed Offsets are numbers between -5 and 5!")


    def set_CMOS_Voltage(self, value: int | float) -> None:
        """
        

        Parameters
        ----------
        value : int/float
            Sets the voltage for the CMOS signal.
            Range: 0.8 to 2.7
            Increment: 0.001

        Raises
        ------
        ValueError
            Wrong range Error.

        Returns
        -------
        None.

        """
        if value >= 0.8 and value <= 2.7:
            self.write(f":CSYNthesis:VOLTage {value}")
        else:
            raise ValueError("Wrong Value. Allowed values are between o.8 and 2.7!")
            
    def set_ClockSigPhase(self, value: int | float) -> None:
        """
        

        Parameters
        ----------
        value : int/float
            Shifts the phase of the generated clock signal.
            Range: -36000 to 36000
            Increment: 0.1


        Raises
        ------
        ValueError
            Wrong Value Error.

        Returns
        -------
        None.

        """
        if value >= -36000 and value <= 36000:
            self.write(f":CSYNthesis:PHASe {value}")
        else:
            raise ValueError("Wrong value range! Allowed values between -36000 and 36000!")
        
        
# =============================================================================
# SOURce:FREQuency subsystem
# =============================================================================

    def set_frequency_mode(self, MODE: str) -> None:
        '''
        Parameters
        ----------
        MODE : str
            <Mode> CW | FIXed | SWEep | LIST | COMBined

            CW|FIXed
                Sets the fixed frequency mode. CW and FIXed are synonyms.
                The instrument operates at a defined frequency.

            SWEep
                Sets sweep mode.
                The instrument processes frequency (and level) settings in
                defined sweep steps.

            LIST
                Sets list mode.
                The instrument processes frequency and level settings by
                means of values loaded from a list.

            COMBined
                Sets the combined RF frequency / level sweep mode.
                The instrument processes frequency and level settings in
                defined sweep steps.
        '''
        
        sStates = ["CW", "FIXed", "FIX", "SWEep", "SWE", "LIST", "COMBined", "COMB"]
        MODE = MODE.upper()
        if MODE in sStates:
            self.write(f':FREQuency:MODE {MODE}')
        else:
            raise ValueError("Not a valid input. Valid: CW | FIXed | SWEep | LIST | COMBined !")
            

    def set_freq_CW(self, value: int | float, unit: str = None) -> None:
        '''
        Parameters
        ----------
        value : int/float
            Parameter Frequency

        unit : str (optional)
            Frequency Unit: 'GHz' or 'MHz' or 'Hz'

        Returns
        -------
        None.

        '''

        minFreq = 8e3 # 8 kHz
        maxFreq = 72e9  # 67 GHz calibrated, 72 GHz max

        if unit == 'Hz' or unit is None:
            unit = 'Hz'
            if value <= maxFreq and value >= minFreq:
                self.write(f':SOURce:FREQuency:CW {value} {unit}')
            else:
                raise ValueError('Minimum Frequency = 8 kHz and Maximum Frequency = 67 GHz')
        elif unit == 'MHz':
            if value*1e6 <= maxFreq and value*1e6 >= minFreq:
                self.write(f':SOURce:FREQuency:CW {value} {unit}')
            else:
                raise ValueError('Minimum Frequency = 8 kHz and Maximum Frequency = 67 GHz')
        elif unit == 'GHz':
            if value*1e9 <= maxFreq and value*1e9 >= minFreq:
                self.write(f':SOURce:FREQuency:CW {value} {unit}')
            else:
                raise ValueError('Minimum Frequency = 8 kHz and Maximum Frequency = 67 GHz')
        else:
            raise ValueError(
                'Unknown input! Unit must be None or "MHz" or "GHz"!')


# =============================================================================
# Activate Commands
# =============================================================================

    def activate_DCOffset(self, state) -> None:
        '''Activates a DC offset.
        
        Parameters
        ----------
        state : str
            'ON' 1 or 'OFF' 0
        '''
        state = self._validate_state(state)
        self.write(f":CSYNthesis:OFFSet:STATe {state}")
        
    
    
# =============================================================================
# SOURce:POWer subsystem
# =============================================================================

    def set_rf_power(self, value: int | float) -> None:
        """Sets the Signal Generator Output Power in dBm.

        Parameters
        ----------
        value : int/float
            Output Power in dBm
        """
        minVal = -20.0
        maxVal = 30.0
        if value > maxVal or value < minVal:
            raise ValueError(f'Power out of range! You can set power between {minVal} and {maxVal} dBm!')

        self.write(f'SOURce:POWer:LEVel:IMMediate:AMPlitude {value}')
  
    
    def set_OutputPowerLevel(self,value: int | float) -> None:
        """Sets the Signal Generator Output Power in dBm. Alias for set_rf_power().

        Parameters
        ----------
        value : int/float
            Output Power in dBm
        """
        self.set_rf_power(value)
