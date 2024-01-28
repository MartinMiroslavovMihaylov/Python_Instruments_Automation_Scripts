# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:55:01 2023

@author: Martin.Mihaylov
"""



import io
import serial
import time


    
class GPP4323:
    def __init__(self, resource_str):
        '''
        Connect to Device and print the Identification Number.
        '''
        self._resource =  serial.Serial(resource_str,
                        baudrate = 115200,
                        bytesize=8,
                        timeout=1,
                        stopbits = serial.STOPBITS_ONE,
                        parity = serial.PARITY_NONE,
                        xonxoff = False)
        
        self.eol_char = '\r\n'
        self.sio = io.TextIOWrapper(io.BufferedReader(self._resource),newline= self.eol_char)
        self._resource.write(('*IDN?' + self.eol_char).encode('utf-8'))
        self.timeout_STR = time.sleep(0.2)
        self.timeout_STR
        self.timeout_STR = time.sleep(0.2)
        print(self.sio.read())
        

   
    
    def write(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
        self.timeout_STR



    def query_IND(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
        data = self.sio.read()
        return data
    
    def query_values(self, message):
        self._resource.write((message + self.eol_char).encode('utf-8'))
        self.timeout_STR
        data = self.sio.read()
        return data

    
    
    def Close(self):
        print('Instrument GPP4323 is closed!')
        return self._resource.close()
    
    
    
    
    
    
    def getIdn(self):
        '''
        

        Returns
        -------
        TYPE  str
            Instrument identification 

        '''
        return self.query_IND("*IDN?")
    
    
    
# =============================================================================
# Set Values and Modes
# =============================================================================
    
    def set_Volt(self, channel, voltage):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2,3,4].
        voltage : int/float.
            Set Voltage on Channel.

        Returns
        -------
        None.

        '''
        ChannelLS = [1,2,3,4]
        if channel in ChannelLS: 
            self.write("VSET"+str(channel)+":{:1.2f}".format(voltage))
        else:
            raise ValueError("Invalid channel number give! Channel Number can be [1,2,3,4].")
        
        
        
        
    def set_Amp(self, channel, amp):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2,3,4].
        amp : int/float
            Set Current on Channel.

        Returns
        -------
        None.

        '''
        ChannelLS = [1,2,3,4]
        if channel in ChannelLS: 
            self.write("ISET"+str(channel)+":{:1.4f}".format(amp))
        else:
            raise ValueError("Invalid channel number give! Channel number can be [1,2,3,4].")
        
        
        
        
    def set_ChannelToSerial(self, channel, status):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].
        status : str
            Sets CH1/CH2 as Tracking series mode.

        Returns
        -------
        None.

        '''
        ChannelLS = [1,2]
        if channel in ChannelLS:
            if status == 'ON':
                self.write(":OUTPut:SERies ON")
            elif status == 'OFF':   
                self.write(":OUTPut:SERies OFF")
            else:
                raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2 !")
        
        
        
        
    def set_ChannelToParallel(self, channel, status):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].
        status : str
            Sets CH1/CH2 as Tracking parallel mode.

        Returns
        -------
        None.

        '''
        ChannelLS = [1,2]
        if channel in ChannelLS:
            if status == 'ON':
                self.write(":OUTPut:PARallel ON")
            elif status == 'OFF':   
                self.write(":OUTPut:PARallel OFF")
            else:
                raise ValueError("Invalid channel status. Possible arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2 !")
        
        
        
         
    def set_ChannelTracking(self, mode):
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
        
        
        
        
    def set_ChannelLoadMode(self, channel, mode, status):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].
        mode : str
            Sets CH1/CH2 as Load CV, CC or CR mode.
        status : str
            Possible status ["ON", "OFF"].

        Returns
        -------
        None.

        '''
        ChannelLS  =[1,2]
        modeLS = ['CC', 'CV', 'CR']
        
        
        if channel in ChannelLS and mode in modeLS:
            if status == 'ON':
                self.write(":LOAD"+str(channel)+":"+str(mode)+' ON')
            elif status == 'OFF':
                self.write(":LOAD"+str(channel)+":"+str(mode)+' OFF')
            else:
                raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2! Or invalid mode! Possible modes are 'CC', 'CV' or 'CR' !")
        
        
        
        
    def set_LoadResistor(self, channel, value):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].
        value : float
            Set resistance values from range 1-1000.

        Returns
        -------
        None.

        '''
        ChannelLS = [1,2]
        if channel in ChannelLS:
            self.write(":LOAD"+str(channel) + ":RESistor " +str(value))
            # self.write("LOAD2: RESistor 100")
        else:
            raise ValueError("Invalid channel number! Possible channel numbers are 1 or 2! Or Invalid resistor Value. Valid Resistor Values are 1-1000!")
              
        
        
        
    def set_Out(self, channel, state):
            '''
            

            Parameters
            ----------
            channel : int
                Select channel from List of Channal Numbers [1,2,3,4].
            state : str
                Status of power Supple output. Could be ["ON", "OFF"]

            Returns
            -------
            None.

            '''
            
            ChannelLS = [1,2,3,4]
            StateLS = ['ON', 'OFF']
            if channel in ChannelLS and state in StateLS:
                if(state == 'ON'):
                    self.write(":OUTPut"+str(channel) + ':STATe '+ str(state))
                elif(state == 'OFF'):
                    self.write(":OUTPut"+str(channel) + ':STATe '+ str(state))
                else:
                    raise ValueError("Invalid channel Status. Valid arguments are 'ON' or 'OFF'! ")
            else:
                raise ValueError("Invalid channel number give! Channel Number can be [1,2,3,4].")
        
        
        
        
# =============================================================================
# Ask Commands
# =============================================================================


    def ask_Volt(self,channel):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2,3,4].

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        
        ChannelLS = [1,2,3,4]
        if channel in ChannelLS:   
            return float(self.query_values("VSET"+str(channel)+"?").split('\n')[0])
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
        
        
        
        
    def read_Measurment(self, channel, Type):
        '''
        

        Returns
        -------
        TYPE float
            Voltage Measured

        '''
        TypeLS = ['Voltage', 'Current', 'Power']
        ChannelLS = [1,2,3,4]
        if channel in ChannelLS and Type in TypeLS:
            return float(self.query_values(":MEASure"+str(channel)+":"+str(Type)+"?").split('\n')[0])
        else:
            raise ValueError('Invalid channel number or type of measurment! Possible channel numbers are [1,2,3,4]. Possible tapes are ["Voltage", "Current", "Power"]')
        
        
        
        
    def ask_Amp(self,channel):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2,3,4].

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
       
        ChannelLS = [1,2,3,4]
        if channel in ChannelLS:   
            return float(self.query_values("ISET"+str(channel)+"?").split('\n')[0])
        else:
            raise ValueError('Invalid channel number or type of measurment! Possible channel numbers are [1,2,3,4]')
        
        
        
        
    def ask_ChannelLoadMode(self, channel):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].

        Returns
        -------
        TYPE
            Queries CH1 or CH2 work mode. 6 modes below: SERies，PARallel，INDE pendent, CV Load，CC Load，CR Load

        '''
        ChannelLS = [1,2]
        
        if channel in ChannelLS:
           return self.query_values(":MODE"+str(channel)+"?").split('\n')[0]
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
        
        
        
        
    def ask_LoadResistor(self,channel):
        '''
        

        Parameters
        ----------
        channel : int
            Select channel from List of Channal Numbers [1,2].

        Returns
        -------
        TYPE
            Set Laod Resistance Value for given channel. 

        '''
        ChannelLs = [1,2]   
        if channel in ChannelLs:
            return float(self.query_values(":LOAD"+str(channel) + ":RESistor?").split('\n')[0])
        else: 
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')
                        

    
    # def ask_Status(self):
    #     '''
        

    #     Returns
    #     -------
    #     TYPE
    #         Get the state of the output and CC/CV

    #     '''
        
    #     return float(self.query_values("STATUS?").split('\n')[0])
    

# =============================================================================
# Get/Save Data
# =============================================================================

    def get_data(self, channel):
        '''
        

        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured voltage and current. 

        '''
        ChannelLS = [1,2,3,4]
        OutPut = {}
        if channel in ChannelLS:
            Voltage = self.read_Measurment(channel, 'Voltage')
            Current = self.read_Measurment(channel, 'Current')
            Power = self.read_Measurment(channel, 'Power')
            OutPut['Voltage/V'] = Voltage
            OutPut['Current/A'] = Current
            OutPut['Power/W'] = Power
            return  OutPut   
        else:
            raise ValueError('Invalid channel number! Possible channel numbers are [1,2,3,4]')