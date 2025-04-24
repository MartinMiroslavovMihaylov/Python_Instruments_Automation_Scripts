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
        Make a restart of the instrument in the beginning to get the instrument 
        to default settings.
        '''
        super().__init__(hostname)
        print(self.ask('*IDN?'))

    def query(self, message):
        return self.ask(message)

    def Close(self):
        print("Instrument Rohde&Schwarz SMA100B is closed!")
        return self.close()

    def reset(self):
        return self.write('*RST')
# =============================================================================
# Get Identication Command
# =============================================================================
    def getIdn(self):
        '''
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        return self.query('*IDN?')
    
# =============================================================================
# Ask Commands
# =============================================================================

    def ask_OutputImpedance(self):
        """
        

        Returns
        -------
        TYPE
            Queries the impedance of the RF outputs.

        """
        return float(self.query(":OUTPut1:IMP?"))


# =============================================================================
# Set Commands
# =============================================================================

    def set_rf_output_all(self, value):
        """Activates all Signal Genrator RF Outputs

        Parameters
        ----------
        value : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        
        OnsStates = ["On", "ON", "on", "oN", "1", 1]
        OffsStates = ["Off", "oFf", "ofF", "OFF", "off", "0", 0]
        if value in OnsStates:
            self.write(':OUTPut:ALL:STATe 1')
        elif value in OffsStates:
            self.write(':OUTPut:ALL:STATe 0')
        else:
            raise ValueError('Not a valid input. Valid: \'ON\', \'OFF\', 1, 0')
            
            

    def set_rf_output(self, value):
        """Activates the Signal Genrator RF Output

        Parameters
        ----------
        value : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        OnsStates = ["On", "ON", "on", "oN", "1", 1]
        OffsStates = ["Off", "oFf", "ofF", "OFF", "off", "0", 0]
        if value in OnsStates:
            self.write(':OUTPut' + ' 1')
        elif value in  OffsStates:
            self.write(':OUTPut' + ' 0')
        else:
            raise ValueError('Not a valid input. Valid: \'ON\', \'OFF\', 1, 0')


    def set_output(self,value):
        """Activates the Signal Genrator RF Output

        Parameters
        ----------
        value : str/int
            'ON' 1 or 'OFF' 0

        Raises
        ------
        ValueError
            Valid values are: \'ON\', \'OFF\', 1, 0
        """
        self.set_rf_output(value)

    def set_DCOffset(self, value):
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
            self.write(":CSYNthesis:OFFSet "+ str(value))
        else:
            raise ValueError("Allowed Offsets are numbers between -5 and 5!")


    def set_CMOS_Voltage(self, value):
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
            self.write(":CSYNthesis:VOLTage "+str(value))
        else:
            raise ValueError("Wrong Value. Allowed values are between o.8 and 2.7!")
            
    def set_ClockSigPhase(self, value):
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
            self.write(":CSYNthesis:PHASe "+ str(value))
        else:
            raise ValueError("Wrong value range! Allowed values between -36000 and 36000!")
        
        
# =============================================================================
# SOURce:FREQuency subsystem
# =============================================================================

    def set_frequency_mode(self, MODE):
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
        
        sStates = ["CW", "cw", "Cw", "cW", "FIXed", "SWEep", "LIST", "CIMBined"]
        if MODE in sStates:
            self.write(':FREQuency:MODE ' + MODE)
        else:
            raise ValueError("Not a valid input. Valid: CW | FIXed | SWEep | LIST | COMBined !")
            

    def set_freq_CW(self, value, unit):
        '''
        Parameters
        ----------
        value : int/float
            Parameter Frequency

        unit : str
            Frequency Unit: 'GHz' or 'MHz'

        Returns
        -------
        None.

        '''

        minFreq = 8e3 # 8 kHz
        maxFreq = 72e9  # 67 GHz calibrated, 72 GHz max
        stUnit = ['MHz', 'GHz']

        if unit == 'MHz':
            if value*1e6 <= maxFreq and value*1e6 >= minFreq:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError(
                    'Warning !! Minimum Frequency = 8 kHz and Maximum Frequency = 67 GHz')
        elif unit == 'GHz':
            if value*1e9 <= maxFreq and value*1e9 >= minFreq:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError(
                    'Warning !! Minimum Frequency = 8 kHz and Maximum Frequency = 67 GHz')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


# =============================================================================
# Activate Commands
# =============================================================================

    def act_DCOffset(self, state):
        '''
        

        Returns
        -------
        Activates a DC offset.

        '''
        sState = ["On", "oN", "on", "ON", "1", "Off", "OFF", "off", "0"]
        if state in sState:
            self.write(":CSYNthesis:OFFSet:STATe "+ state)
        else:
            raise ValueError("Wrong command! You can give 'ON', 'OFF', '0', '1'!")
        
    
    
# =============================================================================
# SOURce:POWer subsystem
# =============================================================================

    def set_rf_power(self, value):
        """Sets the Signal Generator Output Power in dBm

        Parameters
        ----------
        value : float
            Output Power in dBm
        """        ''''''
        minVal = -20.0
        maxVal = 30.0
        if value > maxVal or value < minVal:
            raise ValueError('Unknown input! See function description for more info.')
        else:
            self.write('SOURce:POWer:LEVel:IMMediate:AMPlitude ' + str(value))
  
    
    def set_OutputPowerLevel(self,value):
        """Sets the Signal Generator Output Power in dBm

        Parameters
        ----------
        value : float
            Output Power in dBm
        """        ''''''
        self.set_rf_power(value)
