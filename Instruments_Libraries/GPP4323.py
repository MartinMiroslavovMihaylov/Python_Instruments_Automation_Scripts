# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:55:01 2023

@author: Martin.Mihaylov
"""



import io
import serial
import time

print(
'''
#####################################################################################
    To use the DC-Power Supply GW-Instek GPP4323 you need to install the USB Driver 
    from https://www.gwinstek.com/en-global/download/ - GPP USB Driver 
    Python Library needed: pip install pyserial
#####################################################################################
'''
)

class GPP4323:
    def __init__(self, resource_str):
        '''
        This class is using python serial, time and io libraries. Please be sure to install pyserial.
        Connect to Device and print the Identification Number.
        '''
        self._resource =  serial.Serial(resource_str,
                        baudrate = 115200,
                        bytesize=8,
                        timeout=1,
                        stopbits = serial.STOPBITS_ONE,
                        parity = serial.PARITY_NONE,
                        xonxoff = False)
        
        self.eol_char = '\n'
        self.timeout = 0.2
        self.sio = io.TextIOWrapper(io.BufferedReader(self._resource),newline= self.eol_char)
        self._ChannelLS = [1,2,3,4]
        self._mainChannelLS = [1,2]
        self._StateLS_mapping = { 'on': 'ON', 'off': 'OFF', 1: 'ON', 0: 'OFF', '1': 'ON', '0': 'OFF' }
        print(self.getIdn())
        

   
    
    def write(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
    

    def query_values(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
        time.sleep(self.timeout)
        data = self._resource.read_until().decode('utf-8').strip()
        return data
    
    
    def query_values_io(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
        time.sleep(self.timeout)
        data = self.sio.read()
        return data

    
    def Close(self):
        print('Instrument GPP4323 is closed!')
        return self._resource.close()
    

    def reset(self):
        self.write("*RST")
    

    def getIdn(self):
        '''
        

        Returns
        -------
        TYPE  str
            Instrument identification 

        '''
        return self.query_values("*IDN?")
    
    
# =============================================================================
# Set Values and Modes
# =============================================================================
    
    def set_Volt(self, channel: int, voltage: int|float) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        voltage : int/float.
            Set Voltage on Channel.

        Returns
        -------
        None.

        '''
        
        if channel in self._ChannelLS: 
            self.write("VSET"+str(channel)+":{:1.2f}".format(voltage))
        else:
            raise ValueError("Invalid channel number give! Channel Number can be [1,2,3,4].")   
    def set_Voltage(self, channel: int, voltage: int | float) -> None:
        '''Alias for set_Volt().'''
        self.set_Volt(channel, voltage)
        
        
        
    def set_Amp(self, channel: int, amp: int|float) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        amp : int/float
            Set Current on Channel.

        Returns
        -------
        None.

        '''
        if channel in self._ChannelLS: 
            self.write("ISET"+str(channel)+":{:1.4f}".format(amp))
        else:
            raise ValueError("Invalid channel number give! Channel number can be [1,2,3,4].")
    def set_Current(self, channel: int, amp: int | float) -> None:
        '''Alias for set_Amp().'''
        self.set_Amp(channel, amp)
    def set_CurrentLimit(self, channel: int, amp: int | float) -> None:
        '''Alias for set_Amp().'''
        self.set_Amp(channel, amp) 
        
        
        
    def set_ChannelToSerial(self, channel: int, status: str|int) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        status : str
            Sets CH1/CH2 as Tracking series mode.

        Returns
        -------
        None.

        '''
        if channel in self._mainChannelLS:
            state_normalized = self._StateLS_mapping.get(status.lower() if isinstance(status, str) else int(status))
            if state_normalized is not None:
                self.write(f":OUTPut:SERies {state_normalized}")
            else:
                raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2 !")
        
        
        
        
    def set_ChannelToParallel(self, channel: int, status: str|int) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        status : str
            Sets CH1/CH2 as Tracking parallel mode.

        Returns
        -------
        None.

        '''
        if channel in self._mainChannelLS:
            state_normalized = self._StateLS_mapping.get(status.lower() if isinstance(status, str) else int(status))
            if state_normalized is not None:
                self.write(f":OUTPut:PARallel {state_normalized}")
            else:
                raise ValueError("Invalid channel status. Possible arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2 !")
        
        
        
         
    def set_ChannelTracking(self, mode: int) -> None:
        '''
        

        Parameters
        ----------
        mode : int
            Selects the operation mode: independent, tracking series, or tracking parallel.
            GPP-1326 does not have this function. Series-parallel mode is not supported under LOAD.

        Returns
        -------
        None.

        '''
        modeLS = [0,1,2]
        if mode in modeLS:
            self.write("TRACK" + str(mode))
        else:
            raise ValueError("Invalid Mode Number. Select 0 - Independent, 1 - Series or 2 - Parallel")
        
        
        
        
    def set_ChannelLoadMode(self, channel: int, mode: str, status: str|int) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        mode : str
            Sets CH1/CH2 as Load CV, CC or CR mode.
        status : str
            Possible status ["ON", "OFF"].

        Returns
        -------
        None.

        '''
        modeLS = ['CC', 'CV', 'CR']
        state_normalized = self._StateLS_mapping.get(status.lower() if isinstance(status, str) else int(status))
        
        if channel in self._mainChannelLS and mode in modeLS:
            if state_normalized is not None:
                self.write(":LOAD"+str(channel)+":"+str(mode)+' '+str(state_normalized))
            else:
                raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2! Or invalid mode! Possible modes are 'CC', 'CV' or 'CR' !")
        
        
        
        
    def set_LoadResistor(self, channel: int, value: float) -> None:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].
        value : float
            Set resistance values from range 1-1000.

        Returns
        -------
        None.

        '''

        if channel in self._mainChannelLS:
            self.write(":LOAD"+str(channel) + ":RESistor " +str(value))
            # self.write("LOAD2: RESistor 100")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2! Or Invalid resistor Value. Valid Resistor Values are 1-1000!")
              
        
        
        
    def set_Out(self, channel: int, status: str|int) -> None:
        '''Enable/Disable Output
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        status : str
            Status of power Supple output. Could be ["ON", "OFF"]

        Returns
        -------
        None.

        '''
        
        state_normalized = self._StateLS_mapping.get(status.lower() if isinstance(status, str) else int(status))
        if channel in self._ChannelLS:
            if state_normalized is not None:
                self.write(":OUTPut"+str(channel) + ':STATe '+ str(state_normalized))
            else:
                raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number give! Channel Number can be [1,2,3,4].")
        
        
        
        
# =============================================================================
# Ask Commands
# =============================================================================


    def ask_VoltageSetting(self, channel: int) -> float:
        ''' Returns the voltage setting, NOT the measured voltage!!!
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Voltage Setting.

        '''
        
        if channel in self._ChannelLS:   
            return float(self.query_values("VSET"+str(channel)+"?"))
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
        
        
        
    def ask_CurrentSetting(self, channel: int) -> float:
        '''Returns the current setting, NOT the measured current!!!
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Current Setting.

        '''
    
        if channel in self._ChannelLS:   
            return float(self.query_values("ISET"+str(channel)+"?"))
        else:
            raise ValueError('Invalid channel number or type of measurement! Possible channel numbers are [1,2,3,4]')
       


       
    def read_Measurement(self, channel: int, type: str) -> float:
        '''Performs a measurement and returns the measured value.


        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2,3,4].
        Type : str
            Select measurement type: 
            'volt', 'amp' or 'watt'.
        
        Returns
        -------
        float
            Return float with the measured value on the channel.

        '''

        type_mapping = {'voltage': 'Voltage', 'volt': 'Voltage',
                'current': 'Current', 'amp': 'Current',
                'power': 'Power', 'watt': 'Power'
            }
        type = type_mapping.get(type.lower() if isinstance(type, str) else type)
        
        if channel in self._ChannelLS and type is not None:
            return float(self.query_values(":MEASure"+str(channel)+":"+str(type)+"?"))
        else:
            raise ValueError('Invalid channel number or type of measurment! Possible channel numbers are [1,2,3,4]. Possible tapes are ["Voltage", "Current", "Power"]')
             


    def ask_Current(self, channel: int) -> float:
        ''' Performs one current measurements and returns the value.
        

        Parameters
        ----------
        channel : int    
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Current.

        '''
        return self.read_Measurement(channel, 'amp')



    def ask_Voltage(self, channel: int) -> float:
        ''' Performs one voltage measurements and returns the value.
        

        Parameters
        ----------
        channel : int    
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Voltage.

        '''
        return self.read_Measurement(channel, 'volt')



    def ask_Power(self, channel: int) -> float:
        ''' Performs one power measurements and returns the value.
        

        Parameters
        ----------
        channel : int    
            Select channel from List of Channel Numbers [1,2,3,4].

        Returns
        -------
        float
            Measured Power.

        '''
        return self.read_Measurement(channel, 'watt')    
        
        
    def ask_ChannelLoadMode(self, channel: int) -> str:
        ''' Queries CH1 or CH2 work mode. 
        6 modes: SERies/PARallel/INDE pendent, CV Load/CC Load/CR Load
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].

        Returns
        -------
        str
            SERies/PARallel/INDependent, CV Load/CC Load/CR Load

        '''
        
        if channel in self._mainChannelLS:
           return self.query_values(":MODE"+str(channel)+"?")
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
        
        
        
        
    def ask_LoadResistor(self, channel: int) -> float:
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channel Numbers [1,2].

        Returns
        -------
        TYPE
            Set load Resistance Value for given channel.

        '''
  
        if channel in self._mainChannelLS:
            return float(self.query_values(":LOAD"+str(channel) + ":RESistor?"))
        else: 
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
                        

    
    # def ask_Status(self):
    #     '''
        

    #     Returns
    #     -------
    #     TYPE
    #         Get the state of the output and CC/CV

    #     '''
        
    #     return float(self.query_values("STATUS?"))
    

# =============================================================================
# Get/Save Data
# =============================================================================

    def get_data(self, channel: int) -> dict:
        '''
        

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured voltage and current.

        '''

        OutPut = {}
        if channel in self._ChannelLS:
            Voltage = self.read_Measurment(channel, 'Voltage')
            Current = self.read_Measurment(channel, 'Current')
            Power = self.read_Measurment(channel, 'Power')
            OutPut['Voltage/V'] = Voltage
            OutPut['Current/A'] = Current
            OutPut['Power/W'] = Power
            return OutPut
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')