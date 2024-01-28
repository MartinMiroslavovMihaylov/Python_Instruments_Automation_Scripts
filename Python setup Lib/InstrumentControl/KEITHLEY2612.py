# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 08:39:48 2021

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa


    
class KEITHLEY2612:
    def __init__(self, resource_str):
        '''
        Connect to Device and print the Identification Number.
        '''
        self._resource = visa.ResourceManager().open_resource(resource_str)
        print(self._resource.query('*IDN?'))
        


    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        self._resource.close()
        print('Instrument Keithley Instruments Inc., Model 2612, 1152698, 1.4.2 is closed!')
    
# =============================================================================
# Reset to Defoult
# =============================================================================
    
    def Reset(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B and restore to defaults channel settings.

        Raises
        ------
        ValueError
             Error message 

        Returns
        -------
        None.

        '''
       
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            self.write('smu'+str(chan)+'.reset()')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
            
    
    
    
    
# =============================================================================
# ASK
# =============================================================================
    def Identification(self):
        return str(self.query('*IDN?'))



    def ask_LimitReached(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            This output indicates that a configured limit has been reached.
            (voltage, current, or power limit)

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            v = self.write('smua.source.compliance')
            return print(v)
    
    
    
    
    
    def ask_Current(self,chan):
        '''
        

        Parameters
        ----------
        chan : str 
            Select channel A or B

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        TYPE  float
            Return float whit the measured value on the channel

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            return float(self.query('print(smu'+str(chan)+'.measure.i())'))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_Voltage(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message 


        Returns
        -------
        TYPE : float
            Return float whit the measured value on the channel

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            return float(self.query('print(smu'+str(chan)+'.measure.v())'))
        else:
            raise ValueError('Unknown input! See function description for more info.')
                
    
    
    
    
    def ask_Power(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message 


        Returns
        -------
        TYPE : float
            Return float whit the measured value on the channel

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            return float(self.query('print(smu'+str(chan)+'.measure.p())'))
        else:
            raise ValueError('Unknown input! See function description for more info.')
                
    
    
    
    
    def ask_Resistance(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B

        Raises
        ------
        ValueError
            Error message 


        Returns
        -------
        TYPE : float
            Return float whit the measured value on the channel

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            return print(self.query('print(smu'+str(chan)+'.measure.r())'))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_readBuffer(self,chan,start,stop):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        start : int
            select start value
        stop : int
            select stop value

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        Print the source function used
        for 'start' - 'stop' readings stored in
        source-measure unit (SMU)
        channel A, buffer 1.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            self.query('printbuffer('+str(start)+','+str(stop)+',smu'+str(chan)+')')
        else:
            raise ValueError('Unknown input! See function description for more info.')
                    
    
    
    
    
# =============================================================================
#SET 
# =============================================================================

    def set_SourceOutput(self,chan,state):
        
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        state : str 
            Set source output (CHAN A) ON and OF

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        chan = chan.lower()
        stList = ['ON','OFF']
        chList = ['a','b']
        if chan in chList:
            if state in stList:
                self.write('smu'+str(chan)+'.source.output = smu'+str(chan)+'.OUTPUT_'+str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_AutoVoltageRange(self,chan,state):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        state : str
           ON/OFF voltage source autorange

        Raises
        ------
        ValueError
           Error message 

        Returns
        -------
        None.

        '''
        chan = chan.lower()
        stList = ['ON','OFF']
        chList = ['a','b']
        if chan in chList:
            if state in stList:
                self.write('smu'+str(chan)+'.source.autorangev = smu'+str(chan)+'.AUTORANGE_' + str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
                
    
    
    
    
    def set_AutoCurrentRange(self,chan,state):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        state : str
           ON/OFF current source autorange

        Raises
        ------
        ValueError
           Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        stList = ['ON','OFF']
        chList = ['a','b']
        if chan in chList:
            if state in stList:
                self.write('smu'+str(chan)+'.source.autorangei = smu'+str(chan)+'.AUTORANGE_' + str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_VoltageRange(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Set voltage source voltage limit

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
  
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.0e}'.format(value)
            self.write('smu'+str(chan) + '.measure.rangev = ' + value)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_CurrentRange(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Set current source voltage limit

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.0e}'.format(value)
            self.write('smu'+str(chan)+'.measure.rangei = ' + str(value))
            
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_VoltageLimit(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Sets the voltage limitof channel X to V.

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.0e}'.format(value)
            self.write('smu'+str(chan)+'.source.limitv = ' + str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_CurrentLimit(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Sets the current limitof channel X to V.

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.0e}'.format(value)
            self.write('smu'+str(chan)+'.source.limiti = ' + str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_Voltage(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Set voltage on channels A and B

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.4e}'.format(value)
            self.write('smu'+str(chan)+'.source.levelv = '+str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_Current(self,chan,value):
        '''
        

        Parameters
        ----------
        chan : str
            Select Channel A or B
        value : int/float
            Set Current on channels A and B

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            value = '{:.4e}'.format(value)
            self.write('smu'+str(chan)+'.source.leveli = '+str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_ChannelDisplay(self,chan,double=True):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        double : boolen, optional
            Displays source-measure for SMU A and SMU B.
            double = None per defould.
            if double = True:
                Display Chan A and B 
            else:
                Display only Chan selected

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if double == True:
            if chan in chList:
                self.write('display.screen = display.SMUA_SMUB')
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            if chan in chList:
                self.write('display.screen = display.SMU'+str(chan.upper()))
            else:
                raise ValueError('Unknown input! See function description for more info.')
                   
    
    
    
    
    def set_OutputSourceFunction(self,chan,typ):
        '''
        

        Parameters
        ----------
        chan : str
            Select channl A or B
        typ : str
            The source function. Set to one of the following values:
            typ = 'volt' for Selects voltage source function
            typ = 'amp' for Selects voltage source function

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        typ = typ.lower()
        tList = ['volt','amp']
        chList = ['a','b']
        if chan in chList and typ in tList:
            if typ == 'volt':
                self.write('smu'+str(chan)+'.source.func = smu'+str(chan)+'.OUTPUT_DCVOLTS')
            elif typ == 'amp':
                self.write('smu'+str(chan)+'.source.func = smu'+str(chan)+'.OUTPUT_DCAMPS')
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
                raise ValueError('Unknown input! See function description for more info.')
              
    
    
    
    
    def set_DisplayMeasurementFunction(self,chan,typ):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B
        typ : str
            Selects the displayed measurement function: 
            Amperes, volts, ohms, or watts.
            SMU A and SMU B can be set for different measurement functions!

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        typ = typ.lower()
        tList = ['volt','amp','ohm','watt']
        chList = ['a','b']
        if chan in chList and typ in tList:
            if typ == 'volt':
                self.write('display.smu'+str(chan)+'.measure.func = display.MEASURE_DCVOLTS')
            elif typ == 'amp':
                self.write('display.smu'+str(chan)+'.measure.func = display.MEASURE_DCAMPS')
            elif typ == 'ohm':
                self.write('display.smu'+str(chan)+'.measure.func = display.MEASURE_OHMS')
            elif typ == 'watt':
                self.write('display.smu'+str(chan)+'.measure.func = display.MEASURE_WATTS')
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
                raise ValueError('Unknown input! See function description for more info.')
              
    
    
    
    
    def set_PulseMeasured(self,chan,value,ton,toff):
        '''

        Parameters
        ----------
        chan : str
            Select channel A or B
        value : int/float or list with curly braces for example {1,2,3....}.
        ton : int/float
             X ms pulse on
        toff : int/float
            X ms pulse off

        Raises
        ------
        ValueError
            Error message 

        Returns
        -------
        None.

        '''
        
        chan = chan.lower()
        chList = ['a','b']
        if chan in chList:
            self.write('ConfigPulseIMeasureV(smu'+str(chan)+','+str(value)+','+str(ton)+','+str(toff)+')')
        else:
            raise ValueError('Unknown input! See function description for more info.')
                   
    
    
    
# =============================================================================
# Get/Save Data
# =============================================================================
    def get_Data(self,chan):
        '''
        

        Parameters
        ----------
        chan : str
            Select channel A or B

        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured voltage and current.

        '''
        chan = chan.lower()
        chList = ['a','b']
        OutPut = {}
        if chan in chList:
            Current = self.ask_Current(chan)
            Voltage = self.ask_Voltage(chan)
        OutPut['Voltage/V'] = Voltage
        OutPut['Current/A'] = Current
        return OutPut