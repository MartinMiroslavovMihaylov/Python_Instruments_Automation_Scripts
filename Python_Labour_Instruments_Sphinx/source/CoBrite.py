# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 13:54:49 2022

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa


    
class CoBrite:
    def __init__(self, resource_str):

        self._resource = visa.ResourceManager().open_resource(str(resource_str),query_delay  = 0.5)
        print(self._resource.query('*IDN?'))

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def read(self):
        '''
        Returns
        -------
        None
            This function must be set after each set_() function. CoBrite 
            writes the set_() to register and returns ;/r/n to the user. The
            ;/r/n command will mess up the next data sent to CoBrite from the user.
            An empty read() is required after each set_() function sendet to the
            laser. 

        '''
        return self._resource.read_raw()
    
    def Close(self):
        self._resource.close()
        
        
# =============================================================================
# Identify       
# =============================================================================

    def Identification(self):
        '''
        

        Returns
        -------
        float
            Identification name and model of the instrument. 

        '''
        
        return self.query('*IDN?')
# =============================================================================
# ASK 
# =============================================================================
    

    def ask_FreqTHz(self,chan):
        
        '''
    
        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        float
            Queries the wavelength setting of a tunable laser port.
            Value format is in THz.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                freq = self.query('FREQ? 1,1,1')
            elif chan == 2:
                freq = self.query('FREQ? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
                
        return float(freq.split(';')[0])
    
    
    
    
    
    def ask_Wavelength(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        float
            Queries the wavelength setting of a tunable laser port. 
            Value format is in Nanometer.

        '''

        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                wav = self.query('WAV? 1,1,1')
            elif chan == 2:
                wav = self.query('WAV? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        return float(wav.split(';')[0])

    




    def ask_Offset(self,chan):
        
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        flaot
            Queries the frequency offset setting of a tunable laser port. 
            Value format is in GHz.

        '''
       
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                freq = self.query('OFF? 1,1,1')
            elif chan == 2:
                freq = self.query('OFF? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        return float(freq.split(';')[0])





    def ask_LaserOutput(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        str
            Query if laser is ON or OFF. 

        '''
        
        chanLs = [1,2]
        
        if chan in chanLs:
            if chan == 1:
                out =  float(self.query('STATe? 1,1,1').split(';')[0])
                if out == 0:
                    out = 'OFF'
                else:
                    out = 'ON'
            elif chan == 2:
                out = float(self.query('STATe? 1,1,2').split(';')[0])
                if out == 0:
                    out = 'OFF'
                else:
                    out = 'ON'
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        return out 
        
    
    
        
        

    def ask_Power(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.


        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        float
            Queries the optical output power target setting of a tunable laser
            port. Value format is in dBm.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                power =  self.query('POW? 1,1,1')
            elif chan == 2:
                power = self.query('POW? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        return float(power.split(';')[0])
    
    
    
    
    
    def ask_ActualPower(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        float
            Queries the current optical output power reading of a tunable laser
            port. Value format is in dBm.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                apow =  self.query('APOW? 1,1,1')
            elif chan == 2:
                apow = self.query('APOW? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        return float(apow.split(';')[0])





    def ask_LaserLim(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        DataDic : dictionary
            Query maximum tuning Parameters of Laser in location C-S-D in csv 
            format.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                lim =  self.query('LIM? 1,1,1')
            elif chan == 2:
                lim = self.query('LIM? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        datasep = lim.split(';')[0]
        datasep = datasep.split(',')
        DataDic =  {}
        labels = ['Minimum Frequency','Maximum Frequency','Fine tuning Range','Minimum Power','Maximum Power']
        for i in range(len(datasep)):
            DataDic[labels[i]] = float(datasep[i])
        return DataDic
    
    
    
    
    
    def ask_Configuration(self,chan):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        DataDic : dictionary
            Query current configuration of Laser in location C-S-D in csv format

        '''
       
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                config =  self.query(':SOURce:CONFiguration? 1,1,1')
            elif chan == 2:
                config = self.query(':SOURce:CONFiguration? 1,1,2')
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        datasep = config.split(';')[0]
        datasep = datasep.split(',')
        if datasep[-1] == '-1':  
            datasep[-1] = 'NO'
        else:
            datasep[-1] = 'YES'
        DataDic =  {}
        labels = ['Wavelength','Offset','Output Power','Output state','Busy state','Dither state']
        for i in range(int(len(datasep)-1)):
            DataDic[labels[i]] = float(datasep[i])
        DataDic['Dither supported'] = datasep[-1]
        return DataDic



# =============================================================================
# SET
# =============================================================================
    
    def set_Power(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        value : float
            Sets the optical output power target setting of a tunable laser port.
            Value format is in dBm.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                self.write('POW 1,1,1,'+str(value))
            elif chan == 2:
                self.write('POW 1,1,2,'+str(value))
            else:
                raise ValueError('Unknown input! See function description for more info.') 
     
        
     
        
     
    def set_Wavelength(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        value : float
            Sets the wavelength setting of a tunable laser port. Value format 
            is in Nanometer.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                self.write('WAV 1,1,1,'+str(value))
            elif chan == 2:
                self.write('WAV 1,1,2,'+str(value))
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        
        
        
        
      
    def set_FreqTHz(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        value : float
            Sets or queries the wavelength setting of a tunable laser port.
            Value format is in Tera Hertz.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                self.write('FREQ 1,1,1,'+str(value))
            elif chan == 2:
                self.write('FREQ 1,1,2,'+str(value))
            else:
                raise ValueError('Unknown input! See function description for more info.') 
                
        




        
    def set_LaserOutput(self,chan,state):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        state : float/int
            Set if laser is ON or OFF. Can be integer 0 or 1, but can be a str 
            ON and OFF.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        stateLs = ['ON','OFF',1,0,'1','0']
        if state == 'ON' or state == 1:
            state = '1'
        elif state == 'OFF' or state == 0:
            state = '0'
        if chan in chanLs and state in stateLs:
            if chan == 1:
                self.write('STATe 1,1,1,' + state)
            elif chan == 2:
                self.write('STATe 1,1,2,' + state)
            else:
                raise ValueError('Unknown input! See function description for more info.') 
                
              
                
              
                
              
                
    def set_Offset(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        value : float
            Sets the frequency offset setting of a tunable laser port. 
            Value format is in Giga Hertz.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                self.write('OFF 1,1,1,'+str(value))
            elif chan == 2:
                self.write('OFF 1,1,2,'+str(value))
            else:
                raise ValueError('Unknown input! See function description for more info.') 
         
         
         
         
         
        
    def set_Configuration(self,chan,freq,power,offset):
        '''
        

        Parameters
        ----------
        chan : int
            Channel number. Can be 1 or 2. CoBrite have only 2 channels!.
        freq : float
            Sets frequency in Thz format. For example freq = 192.2345
        power : float
            Sets the power to dBm. For example power = 9.8.
            min Power = 8.8 
            max Power = 17.8
            Check ask_LaserLim() for more info. 
        offset : float
            Sets offset Freq in range Ghz.

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        chanLs = [1,2]
        if chan in chanLs:
            if chan == 1:
                self.set_FreqTHz(chan, freq)
                self.set_Power(chan, power)
                self.set_Offset(chan, offset)
            elif chan == 2:
                self.set_FreqTHz(chan, freq)
                self.set_Power(chan, power)
                self.set_Offset(chan, offset)
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
            
        
        
