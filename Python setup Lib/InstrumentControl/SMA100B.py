#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""
Created on Fir Feb 02 13:00:00 2024

@author: mweizel
"""

import numpy as np
import vxi11


print(
    '''

#####################################################################################

Befor using the SMA100B you need to:
    1) Install python-vxi11. E.g. pip install python-vxi11
    2) Check the IP Adress of the SMA100B. Setup-> Remote Access -> Network
    
#####################################################################################

'''
)


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
        self.write('*RST')

    def query(self, message):
        return self.ask(message)

    def Close(self):
        return self.close()

    def reset(self):
        return self.write('*RST')
# =============================================================================
# Abort Command
# =============================================================================

# =============================================================================
# OUTPut subsystem
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
        if value == 1 or value == 'ON':
            self.write(':OUTPut:ALL:STATe 1')
        elif value == 0 or value == 'OFF':
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
        if value == 1 or value == 'ON':
            self.write(':OUTPut' + ' 1')
        elif value == 0 or value == 'OFF':
            self.write(':OUTPut' + ' 0')
        else:
            raise ValueError('Not a valid input. Valid: \'ON\', \'OFF\', 1, 0')

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
        self.write(':FREQuency:MODE ' + MODE)

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

        minFreq = 10
        maxFreq = 67
        stUnit = ['MHz', 'GHz']

        if unit == 'MHz':
            if value <= maxFreq*1e9 and value >= 10:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError(
                    'Warning !! Minimum Frequency = 10 MHz and Maximum Frequency = 67*1e9 MHz')
        elif unit == 'GHz':
            if value <= maxFreq and value >= 0.01:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError(
                    'Warning !! Minimum Frequency = 0.01 GHz and Maximum Frequency = 67 GHz')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


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
        self.write('SOURce:POWer:LEVel:IMMediate:AMPlitude ' + str(value))
