# version: 1.0.0 2024/11/28 #Downloaded from https://www.novoptel.de/Home/Downloads_de.php
# version: 1.1.0 2025/02/07 modified by Maxim.Weizel for LU1000 CBand+OBand (partially tested)


from Instruments_Libraries.NovoptelUSB import NovoptelUSB
from Instruments_Libraries.NovoptelTCP import NovoptelTCP
from time import time, sleep

print(
'''
#####################################################################################
    To use the LU1000 Laser you need to install the FTDI D2XX Driver e.g.
    from https://www.novoptel.de/Home/Downloads_de.php - USB Driver for USB2.0
    or https://ftdichip.com/drivers/d2xx-drivers/ - 2.12.36.4 (accessed on 08.02.2025)
    Python Library needed: pip install ftd2xx 
#####################################################################################
'''
)

##################################
    # LU1000 Laser Base Class #
##################################
class LU1000_Base:
    def __init__(self, target='USB', port=5025):
        if target == 'USB':
            self.n = NovoptelUSB('LU1000')
            if self.n.DEVNO < 0:
                raise ConnectionError("Could not open USB connection")
        else:
            self.n = NovoptelTCP(target, port=port)
        self._available_lasers = [1, 2]

    def Close(self):
        self.n.close()
        self.n = None

    def _read(self, addr: int) -> int:
        return self.n.read(addr)

    def _write(self, addr: int, data: int) -> None:
        self.n.write(addr, data)

    def _validate_laser(self, laser: int) -> None:
        if laser not in self._available_lasers:
            raise ValueError(f"Laser {laser} is not in available lasers {self._available_lasers}")

    def _calc_address(self, laser: int, offset: int) -> int:
        if laser not in self._available_lasers:
            raise ValueError("Invalid laser number. Must be one of: " + str(self._available_lasers))
        return int(128 * laser + offset)

# =============================================================================
# Base Class - General instrument data
# =============================================================================

    def get_controller_temp(self) -> float:
        '''Controller module temperature in Celsius

        Parameters
        ----------

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Controller module temperature in Celsius

        '''
        CONTROLLER_TEMP_ADDR = 51  
        raw = self._read(CONTROLLER_TEMP_ADDR)  # Celsius * 16
        return float(raw / 16.0)
    
    def get_firmware(self): # as string
        return hex(self.n.read(64)) #4 Digit BCD

    def get_serial_number(self): # as integer
        return self.n.read(65)

    def get_module_type(self) -> str:
        module_type = []
        for ii in range(16):
            dummy = self._read(68 + ii)
            module_type.append(chr(dummy >> 8))
            module_type.append(chr(dummy & 0xFF))
        return "".join(module_type).strip()

# =============================================================================
# Base Class - GET functions
# =============================================================================
    def get_laser_output(self, laser: int) -> int:
        '''Returns the Laser output state. Enabled = 1 , Disabled = 0

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        int 
            Laser enabled = 1 or laser disabled = 0

        '''

        addr = self._calc_address(laser, 50)
        res = self._read(addr)
        return 1 if int(res) == 8 else 0
    
# =============================================================================
# Base Class - SET functions
# =============================================================================
    def set_laser_output(self, laser: int, value: str|int) -> None:
            '''Turn Laser N output ON/OFF

            Parameters
            ----------
            laser : int
                Laser output selected -  1 or 2
            value : int/str
                value = 'ON'|'OFF'|1|0

            Raises
            ------
            ValueError
                Error message

            Returns
            -------
            None.

            '''

            state_mapping = { 'on': 8, 'off': 0, 1: 8, 0: 0}
            state_normalized = state_mapping.get(value.lower() if isinstance(value, str) else int(value))
            if state_normalized is None:
                raise ValueError("Invalid state. Expected 'ON', 'OFF', 1, or 0.")
            addr = self._calc_address(laser, 50)
            self._write(addr, state_normalized)  

####################################################################################
####################################################################################

##################################
    # C-Band Tuable Laser Class #
##################################
class LU1000_Cband(LU1000_Base):    
    def __init__(self, target='192.168.1.100'):
        super().__init__(target)
        # implement LU1000_Cband specific initializations here
        self._max_freq = {
            1: self.get_max_freq(1),
            2: self.get_max_freq(2)
        }

        self._min_freq = {
            1: self.get_min_freq(1),
            2: self.get_min_freq(2)
        }

        self._grid_spacing = {
            1: self.get_grid_spacing(1),
            2: self.get_grid_spacing(2)
        }

        self._max_channel_number = {
            1: self._update_max_channel_number(1),
            2: self._update_max_channel_number(2)
        }
        
# =============================================================================
# C-Band Laser - General instrument data
# =============================================================================

# Inherit from parent class

# =============================================================================
# C-Band Laser - GET functions
# =============================================================================        
    def _update_max_channel_number(self, laser: int) -> int:
        '''_internal function: Update max channel number
        
        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        int 
            max channel number
        '''

        self._validate_laser(laser)
        max_f = self._max_freq[laser]
        min_f = self._min_freq[laser]
        sleep(0.1)
        grid_spacing = self.get_grid_spacing(laser)
        return int( (max_f-min_f)/(grid_spacing/1e4) + 1)

    def get_channel(self, laser: int) -> int:
        '''Returns the Laser module's current channel.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : int
            Laser module's current channel number

        '''

        addr = self._calc_address(laser, 48)
        res = self._read(addr)
        return int(res)



    def get_target_power(self, laser: int) -> float:
        '''Returns the laser module's current Optical Power in dBm

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Returns the laser module's current optical power in dBm

        '''

        addr = self._calc_address(laser, 49)
        res = self._read(addr)
        return float(res/100)


    def get_grid_spacing(self, laser: int) -> int:
        '''Grid spacing in GHz*10


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        int
            Grid spacing in GHz*10

        '''

        addr = self._calc_address(laser, 52)
        res = self._read(addr)
        return int(res)    


    def _get_first_chann_freq_THz(self, laser: int) -> float:
        '''_internal function: First channel's frequency, THz
        Bit unclear what this is. Is this the minimum Frequency?

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        res : float
            First channel's frequency, THz

        '''

        addr = self._calc_address(laser, 53)
        res = self._read(addr)
        return float(res)
    

    def _get_first_chann_freq_GHz(self, laser: int) -> float:
        '''_internal function: First channel's frequency, GHz*10
        Bit unclear what this is. Is this the minimum Frequency?

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            First channel's frequency, GHz*10

        '''

        addr = self._calc_address(laser, 54)
        res = self._read(addr)
        return float(res)


    def _get_channel_freq_THz(self, laser: int) -> float:
        '''Retrun channel Frequency in THz


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Retrun channel Frequency in THz

        '''

        addr = self._calc_address(laser, 64)
        res = self._read(addr)
        return float(res)
    

    def _get_channel_freq_GHz(self, laser: int) -> float:
        '''Returns channel's frequency as GHZ*10

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Returns channel's frequency as GHZ*10

        '''

        addr = self._calc_address(laser, 65)
        res = self._read(addr)
        return float(res)


    def get_measured_power(self, laser: int) -> float:
        '''Returns the current optical power encoded as dBm

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Returns the current optical power encoded as dBm

        '''

        addr = self._calc_address(laser, 66)
        res = self._read(addr) # dBm * 100
        return float(res/100.0)


    def get_temperature(self, laser: int) -> float:
        '''Returns the current temperature encoded as °C.

        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Returns the current temperature encoded as °C.

        '''

        addr = self._calc_address(laser, 67)
        res = self._read(addr) # Celsius * 100
        return float(res/100)

    def get_min_optical_power(self, laser: int) -> float:
        '''Get minimum possible optical power setting

        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

        Raises
        ------
        ValueError
            Error message
        
        Returns
        -------
        res : float
            Get minimum possible optical power setting

        '''
        addr = self._calc_address(laser, 80)
        res = self._read(addr)
        return float(res)
    

    def get_max_optical_power(self, laser: int) -> float:
        '''Get maximum possible optical power setting

        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

        Raises
        ------
        ValueError
            Error message
        
        Returns
        -------
        res : float
            Get maximum possible optical power setting

        '''
        addr = self._calc_address(laser, 81)
        res = self._read(addr)
        return float(res)

    def _get_min_freq_THz(self, laser: int) -> float:
        '''_internal function:  Laser's minimum (first) Frequency, THz

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser's minimum frequency, THz

        '''

        addr = self._calc_address(laser, 82)
        res = self._read(addr)
        return float(res)

    def _get_min_freq_GHz(self, laser: int) -> float:
        '''_internal function: Laser's minimum (first) Frequency, GHz*10

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser's minimum frequency, GHz*10

        '''

        addr = self._calc_address(laser, 83)
        res = self._read(addr)
        return float(res)



    def _get_max_freq_THz(self, laser: int) -> float:
        '''_internal function: Laser's maximum Frequency, THz


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
           Laser's maximum Frequency, THz

        '''

        addr = self._calc_address(laser, 84)
        res = self._read(addr)
        return float(res)

    def _get_max_freq_GHz(self, laser: int) -> float:
        '''_internal function: Laser's maximum Frequency, GHz*10

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser's maximum Frequency, GHz*10

        '''

        addr = self._calc_address(laser, 85)
        res = self._read(addr)
        return float(res)


    def get_min_grid_freq(self, laser: int) -> float:
        '''Laser's minimum supported grid spacing, GHz*10

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Laser's minimum supported grid spacing, GHz*10

        '''

        addr = self._calc_address(laser, 86)
        res = self._read(addr)
        return float(res)


    def get_whispermode(self, laser: int) -> int:
        '''Whispermode Status, ON = 2, OFF = 0

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : int
            Whispermode Status. ON = 2, OFF = 0

        '''

        addr = self._calc_address(laser, 108)
        res = self._read(addr)
        return int(res)


# =============================================================================
# GET Function Wrappers implemented by SCT-Group
# =============================================================================

    def get_min_freq(self, laser: int) -> float:
        '''Laser's minimum possible frequency

        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            min possible frequency.

        '''

        self._validate_laser(laser)
        THz = self._get_min_freq_THz(laser)
        GHz = self._get_min_freq_GHz(laser)
        Freq = THz + GHz*1e-4
        return Freq


    def get_max_freq(self, laser: int) -> float:
        '''Lasers's maximum possible Frequency.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float 
            max possible frequency

        '''

        self._validate_laser(laser)
        THz = self._get_max_freq_THz(laser)
        GHz = self._get_max_freq_GHz(laser)
        Freq = THz + GHz*1e-4
        return float(Freq)


    def get_frequency(self, laser: int) -> float:
        '''Calculate and return Frequency on the selected channel

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Freq : float
            Calculate and return Frequency on the selected channel

        '''

        self._validate_laser(laser)
        THz = float(self._get_channel_freq_THz(laser))
        GHz = float(self._get_channel_freq_GHz(laser))
        Freq = THz + GHz*1e-4
        return Freq


# =============================================================================
# SET
# =============================================================================

    def set_target_power(self, laser: int, value: int|float, ignore_warning: bool = False) -> None:
        '''Sets the laser module's optical power in dBm

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : float
            optical power in dBm
        ignore_warning : bool
            When True, no warning for power > 10dBm is displayed

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        self._validate_laser(laser)
        if 10 < value <= 16 and not ignore_warning:
            raise ValueError("Power value above 10dBm requires explicit confirmation.")
        elif  6 <= value <= 16:
            addr = self._calc_address(laser, 49)
            self._write(addr, int(value * 100))
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


    def set_channel(self, laser: int, value: int) -> None:
        '''Sets the laser module's current channel

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int
            Sets the laser module's current channel
            value = select channel value

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''

        addr = self._calc_address(laser, 48)
        if 1 <= value <= self._max_channel_number[laser]:
            self._write(addr, int(value))
        else:
            raise ValueError(
                f'Channel number: {value} out of range!')


    def set_grid_spacing(self, laser: int, value: int) -> None:
        '''Set Grid spacing in GHz*10.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int
            Set Grid spacing. Smallest possible value = 1

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        addr = self._calc_address(laser, 52)
        if value >= 1:
            for ii in range(5): # try 5 times
                self._write(addr, int(value))
                self._max_channel_number[laser] = self._update_max_channel_number(laser)
                sleep(0.1)
                if self.get_grid_spacing(laser) == value:
                    break
            else:
                raise ValueError('Failed to set grid spacing.')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def _set_first_chann_freq_THz(self, laser: int, value: int|float) -> None:
        '''_internal function: Channel's frequency, THz

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int | float
            Channel's frequency, THz

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''

        addr = self._calc_address(laser, 53)
        self._write(addr, int(value))


    def _set_first_chann_freq_GHz(self, laser: int, value: int|float) -> None:
        '''_internal function:Channel's frequency, GHz*10

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int | float
            Channel's frequency, GHz*10

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''

        addr = self._calc_address(laser, 54)
        self._write(addr, int(value))


    def set_fine_tune(self, laser: int, value: int) -> None:
        '''Fine-tuning set the frequency in MHz steps

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int
            Fine-tuning set the frequency in MHz steps

        Returns
        -------
        None.

        '''

        addr = self._calc_address(laser, 98)
        self._write(addr, int(value))

    def set_whispermode(self, laser: int, state: str|int, timeout: int = 30) -> None:
        '''Activates/Deactivates Whispermode

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        state : str | int
            ['ON','OFF', 1, 0]
        timeout : int
            Timeout in seconds

        Returns
        -------
        None.

        '''

        state_mapping = { 'on': 2, 'off': 0, 1: 2, 0: 0}
        state_write = state_mapping.get(state.lower() if isinstance(state, str) else int(state))

        if  state_write is not None:
            addr = self._calc_address(laser, 108)
            self._write(addr, state_write)
            timeout = int(timeout) if isinstance(timeout, (int, float)) else 30  # Timeout in seconds
            start_time = time()

            while time() - start_time < timeout:
                temp_read = self.get_whispermode(laser)
                if temp_read == state_write:
                    break
                self._write(addr, state_write)
                sleep(0.5) 
            else:
                raise TimeoutError(f"Failed to set Whispermode for laser {laser} within {timeout} seconds.")
        else:
            raise ValueError('Unknown input! See function description for more info.')


# =============================================================================
# SET Wrapper Functions implemented by SCT-Group
# =============================================================================
    def set_frequency(self, laser: int, value: float) -> None:
        '''Set Laser Frequency value in  value


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : float
            Set Laser Frequency in THz
            e.g value = 192.876

        Returns
        -------
        None.

        '''

        self._validate_laser(laser)
        GHz = int((value % 1)*1e4)
        THz = int(value // 1)
        self._set_first_chann_freq_THz(laser, THz)
        sleep(0.1)
        self._set_first_chann_freq_GHz(laser, GHz)




# =============================================================================
# Get/Save Data
# =============================================================================


    def get_data(self, laser: int) -> dict:
        '''Return a dictionary with the measured power and set frequency.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured power and set frequency.

        '''

        OutPut = {}
        self._validate_laser(laser)
        Power = self.get_measured_power(laser)
        Freq = self.get_frequency(laser)
        OutPut['Power/dBm'] = Power
        OutPut['Set Frequency/THz'] = Freq
        return OutPut



##################################
    # O-Band DFB Laser Class #
##################################
class LU1000_Oband(LU1000_Base):
    
    def __init__(self, target='192.168.1.100'):
        super().__init__(target)
        # Implement O-Band Laser specific initializations here        
        
# =============================================================================
# Basic communication
# =============================================================================
        # Inherit from LU1000_Base

# =============================================================================
# General instrument data
# =============================================================================
        # Inherit from LU1000_Base

# =============================================================================
# Get
# =============================================================================
    def get_temperature(self, laser: int) -> float:
        '''Returns the laser module temperature in °C.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Temperature in °C

        '''
        addr = self._calc_address(laser, 23)
        return float(self._read(addr) / 1000.0)


    def get_target_current(self, laser: int) -> float:
        '''Retruns the laser module's current in mA

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Current in mA.

        '''
        addr = self._calc_address(laser, 24)
        return float(self._read(addr) / 100.0)
    
    def get_measured_power_dBm(self, laser: int) -> float:
        '''Retruns the laser module's measured power in dBm

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Measured power in dBm or 'nan' if laser is off

        '''
        addr = self._calc_address(laser, 31)  # Adjust the offset if needed
        raw_value = self._read(addr)
        
        # Check for the "laser off" magic value.
        if raw_value == 45535:
            return float('nan') #laser is off -inf dBm
        
        # Convert raw_value to a signed 16-bit integer (two's complement)
        if raw_value >= 32768:
            raw_value -= 65536

        # Scale the value to dBm.
        return raw_value / 1000.0
    
    def get_measured_power_mW(self, laser: int) -> float:
        '''Retruns the laser module's measured power in mW

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Measured power in mW or 10 if laser is off

        '''
        addr = self._calc_address(laser, 29)  # Adjust the offset if needed
        raw_value = self._read(addr)

        # Scale the value to mW.
        return raw_value / 1000.0
    
    def get_measured_current_1(self, laser: int) -> float:
        '''Experimental! 
        Retruns the laser module's measured current in mA

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Measured current in mA

        '''
        addr = self._calc_address(laser, 28)
        return self._read(addr) *6.35647/1000
    
    def get_measured_current_2(self, laser: int) -> float:
        '''Experimental! 
        Retruns the laser module's measured current in mA

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Measured current in mA

        '''
        addr = self._calc_address(laser, 26)
        return (self._read(addr) + 4957)/589.9
    
# =============================================================================
# Set
# =============================================================================
    def set_temperature(self, laser: int, temperature: float) -> None:
        '''Sets the laser module's temperature in °C.

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        temperature : float
            9°C <= temperature <= 45°C

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        addr = self._calc_address(laser, 23)
        if  9.0 <= temperature <= 45.0: #temperature in °C
            self._write(addr, int(temperature * 1000))
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


    def set_target_current(self, laser: int, current: float, ignore_warning: bool = False) -> None:
        '''Sets the laser module's current in mA

        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : float
            0mA <= value <= 100mA

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''

        addr = self._calc_address(laser, 24)
        if 45 <= current <= 100.0 and not ignore_warning:
            raise ValueError("Power value above 10dBm requires explicit confirmation.")
        elif  0.0 <= current < 100.0:
            addr = self._calc_address(laser, 24)
            self._write(addr, int(current * 100))
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')
          