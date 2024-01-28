# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 12:58:27 2021

@author: Martin.Mihaylov
"""

import numpy as np
import pandas as pd
import vxi11


class AQ6370D(vxi11.Instrument):
    '''
    A class thats uses vxi11 library to interface a Yokogawa AQ6370D.
    Need to have python 'vxi11', 'pandas' and 'numpy' librarys installed!
    
    
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
        self.close()
        print('Instrument Yokogawa AQ6370D is closed!')
    
# =============================================================================
# Start Sweep
# =============================================================================

    def StartSweep(self):
        '''
        Makes a sweep
        '''
        self.write(':INITIATE')
        
    
    
    
    
# =============================================================================
# Stop Measurment
# =============================================================================

    def Stop(self):
        '''
        

        Returns
        -------
        None.
            OSA.ask_SweepMode()

        '''
        
        self.write('ABORt')
        
    
    
    
    
# =============================================================================
# ASK 
# =============================================================================

    def ask_DisplayAutoY(self):
        '''
        

        Returns
        -------
        str
            Queries the automatic setting function of
            the sub scale of the level axis.
            Response 0 = OFF, 1 = ON

        '''
        
        data = self.query(':DISPLAY:TRACE:Y2:AUTO?')
        if data == '0':
            return 'OFF'
        else:
            return 'ON'
    
    
    
    
    
    def ask_DisplayYUnit(self):
        '''
        

        Returns
        -------
        str
            Queries the units of the main scale of the
            level axis.
            DBM = dBm
            W = W
            DBM/NM = dBm/nm or dBm/THz
            W/NM = W/nm or W/THz
            Response 0 = dBm
                1 = W
                2 = DBM/NM
                3 = W/NM

        '''
               
        data  = self.query(':DISPLAY:TRACE:Y1:UNIT?')
        if data == '0':
            return 'dBm'
        elif data == '1':
            return 'W'
        elif data == '2':
            return 'DBM/NM'
        elif data == '3':
            return 'W/NM'
       
    
    
    
    
    def ask_WavelengthStart(self):
        '''
        

        Returns
        -------
        float
            Queries the measurement condition
            measurement start wavelength

        '''

        return float(self.query(':SENSE:WAVELENGTH:START?'))
    
    
    
    
    
    def ask_WavelengthStop(self):
        '''
        

        Returns
        -------
        dloat
            Queries the measurement condition
            measurement start wavelength

        '''
        
        return float(self.query(':SENSE:WAVELENGTH:STOP?'))
    
    
    
    
    
    def ask_CenterWavelenght(self):
        '''
        
        Returns
        -------
        float
            Queries the synchronous sweep function.

        '''
        
        return float(self.query(':SENSe:WAVelength:CENTer?'))
    
    
    
    
    
    def ask_DataFormat(self):
        '''
        

        Returns
        -------
        str
            Queries the format used for data transfer
            via GP-IB.
            
            ASCii = ASCII format (default)
            REAL[,64] = REAL format (64bits)
            REAL,32 = REAL format (32bits)

        '''
        
        return self.query(':FORMat:DATA?')
    
    
    
    
    
    def ask_UnitX(self):
        '''
        
        Returns
        -------
        str
            Queries the units for the X axis.
            
            
            For AQ6370C, AQ6373 or AQ6373B
            WAVelength = Wavelength
            FREQuency = Frequency

        '''
        
        data =  self.query(':UNIT:X?')
        if data == '0':
            return 'WAVelength'
        elif data == '1':
            return 'FREQuency'
        elif data == '2':
            return 'WNUMber'
        
    
    
    
    
    def ask_TraceState(self):
        '''
        

        Returns
        -------
        str
            Queries the display status of the specified
            trace.

        '''
        
        data = self.query('TRACe:STATe?')
        if data == '0':
            return 'Trace is OFF'
        else:
            return 'Trace is ON'
   
    
    
    
    
    def ask_TraceActive(self):
        '''
        

        Returns
        -------
        str
            Queries the trace to be transferred.
            
            Outputs - (TRA|TRB|TRC|TRD|TRE|TRF|TRG)

        '''
        
        return self.query(':TRACe:ACTive?')
    
    
    
    
    
    def ask_CentralWavelenght(self):
        '''
        

        Returns
        -------
        str
            Queries the center wavelength of the
            X-axis of the display scale

        '''
        
        return float(self.query(':SENSE:WAVELENGTH:CENTER?'))
    
    
    
    
    
    def ask_Span(self):
        '''
        

        Returns
        -------
        float
            Queries the measurement condition
            measurement span.

        '''
        
        
        return float(self.query(':SENSE:WAVELENGTH:SPAN?'))
    
    
    
    
    
    def ask_TraceResolution(self,state):
        '''
        

        Parameters
        ----------
        state : str
           Trace selected - ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        list of floats
            Queries the actual resolution data of the
            specified trace.

        '''
    
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:
            data = self.query('CALCULATE:ARESOLUTION? '+str(state)).split(',')
            data = list(np.array(data,dtype=np.float32))
            return data
        
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_BWResolution(self):
        '''
        

        Returns
        -------
        float
            Queries the measurment resolution

        '''
        
        return float(self.query(':SENSE:BANDWIDTH?'))
    
    
    
    
    
    def ask_Sensitivity(self):
        '''
        

        Returns
        -------
        str
            Queries the measurement sensitivity.

        '''
        
        data  = self.query(':SENSE:SENSE?')
        if data == '0':
            return 'NHLD'
        elif data == '1':
            return 'NAUT'
        elif data == '2':
            return 'MID'
        elif data == '3':
            return 'HIGH1'
        elif data == '4':
            return 'HIGH2'
        elif data == '5':
            return 'HIGH3'
        else:
            return 'NORMAL'
       
    
    
    
    
    def ask_AverageCount(self):
        '''
        

        Returns
        -------
        float
            Queries the number of times averaging for
            each measured point.

        '''
        
        return float(self.query(':SENSE:AVERAGE:COUNT?'))
    
    
    
    
    
    def ask_SegmentPoints(self):
        '''
        

        Returns
        -------
        float
            Queries the number of sampling points
            to be measured at one time when performing
            SEGMENT MEASURE.

        '''
        
        return float(self.query(':SENSE:SWEEP:SEGMENT:POINTS?'))
    
    
    
    
    
    def ask_SamplePoints(self):
        '''
        

        Returns
        -------
        float
            Queries the number of samples measured

        '''
        
        return float(self.query(':SENSE:SWEEP:POINTS?'))
    
    
    
    
    
    def ask_SamplePointsAuto(self):
        '''
        

        Returns
        -------
        str
            Queries the function of automatically
            setting the sampling number to be measured
            
            Response 0 = OFF, 1 = ON

        '''
        
        data = self.query(':SENSE:SWEEP:POINTS:AUTO?')
        if data == '0':
            return 'OFF'
        else:
            return 'ON'
    
    
    
    
    
    def ask_SweepSpeed(self):
        '''
        

        Returns
        -------
        str
            Queries the sweep speed
            1x|0: Standard
            2x|1: Twice as fast as standard

        '''
        
        data = self.query(':SENSE:SWEEP:SPEED?')
        if data == '0':
            return 'Standard'
        else:
            return 'Twise as fast as standard'
    
    
    
    
    
    def ask_TraceDataX(self,state):
        '''
        

        Parameters
        ----------
        state : str
             Name of the trace that should be extractselected.          
            state = [TRA|TRB|TRC|TRD|TRE|TRF|TRG]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        list of floats
            Queries the wavelength axis data of the
            specified trace.

        '''
        
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:   
            data = self.query(':TRACE:X? '+str(state)).split(',')
            data = list(np.array(data,dtype=np.float32))
            return data
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_TraceDataY(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Name of the trace that should be extractselected.          
            state = [TRA|TRB|TRC|TRD|TRE|TRF|TRG]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        data : list of floats
            Queries the level axis data of specified trace.

        '''
        
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:   
            data = self.query(':TRACE:Y? '+str(state)).split(',')
            data = list(np.array(data,dtype=np.float32))
            return data
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_SweepMode(self):
        '''
        

        Returns
        -------
        str
            Queries the sweep mode
            ['SINGle','REPeat','AUTO','SEGMent']

        '''
        
        data  = self.query(':INITiate:SMODe?')
        if data == '1':
            return 'SINGle'
        elif data == '2':
            return 'REPeat'
        elif data == '3':
            return 'AUTO'
        elif data == '4':
            return 'SEGMent'
        
    
    
    
    
    def ask_TraceAttribute(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Name of the trace that should be extractselected. 
            sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        str
            Queries the attributes of the specified
            trace
            ['WRITe','FIX','MAX','MIN','RAVG','CALC']
            WRITe = WRITE
            FIX = FIX
            MAX = MAX HOLD
            MIN = MIN HOLD
            RAVG = ROLL AVG
            CALC = CALC


        '''
        
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:
            data  = self.query(':TRACE:ATTRIBUTE:'+str(state)+'?')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        if data == '0':
            return 'WRITE'
        elif data == '1':
            return 'FIX'
        elif data == '2':
            return 'MAX HOLD'
        elif data == '3':
            return 'MIN HOLD'
        elif data == '4':
            return 'ROLL AVG'
        else:
            return 'CALC'

    
    
    
    
# =============================================================================
# SET
# =============================================================================

    def set_DisplayYUnit(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Set the units of the main scale of the
            level axis
            ['dBm','W','DBM/NM','W/NM']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sState = ['dBm','W','DBM/NM','W/NM']
        if state in sState:
            self.write(':DISPLAY:TRACE:Y1:UNIT '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_WavelengthStart(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Set the measurement condition
        unit : str
            units - [M|HZ].

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['M','HZ']
        if unit in sUnit:    
            self.write(':SENSE:WAVELENGTH:START '+str(value)+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_WavelengthStop(self,value,unit):
        '''
        Set the measurement condition
        measurement stop wavelength
        
        [M|HZ]
        '''
        sUnit = ['M','HZ']
        if unit in sUnit:    
            self.write(':SENSE:WAVELENGTH:STOP '+str(value)+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_DataFormat(self,unit):
        '''
        

        Parameters
        ----------
        unit : str
            sUnit = ['ASCii', 'REAL[,64]', 'REAL,32']
            
            
            When the format is set to REAL (binary) using
            this command, the output data of the following
            commands are produced in the REAL format.
            :CALCulate:DATA:CGAin?
            :CALCulate:DATA:CNF?
            :CALCulate:DATA:CPOWers?
            :CALCulate:DATA:CSNR?
            :CALCulate:DATA:CWAVelengths?
            :TRACe[:DATA]:X?
            :TRACe[:DATA]:Y?
                • The default is ASCII mode.
                • When the *RST command is executed, the
                format is reset to the ASCII mode.
                • The ASCII format outputs a list of numerics
                each of which is delimited by a comma (,).
                Example: 12345,12345,....
                • By default, the REAL format outputs data in
                fixed length blocks of 64 bits, floating-point
                binary numerics.
                • If “REAL,32” is specified in the parameter,
                data is output in the 32-bit, floating-point
                binary form.
                • The fixed length block is defined by IEEE
                488.2 and consists of “#” (ASCII), one numeric
                (ASCII) indicating the number of bytes that
                specifies the length after #, length designation
                (ASCII), and binary data of a specified length
                in this order. Binary data consists of a floatingpoint data string of 8 bytes (64 bits) or 4 bytes
                (32 bits). Floating-point data consists of lowerorder bytes to higher-order bytes.
                E.g.: #18 [eight <byte data>]
                #280[80 <byte data>]
                #48008[8008 <byte data>]
                • For data output in the 32-bit floating-point
                binary form, cancellation of significant digits
                is more likely to occur in comparison with
                transfer of data in the 64-bit, floating-point
                binary form.
                • This is a sequential command

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['ASCii', 'REAL[,64]', 'REAL,32']
        if unit in sUnit:    
            self.write('FORMAT:DATA '+ str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_UnitX(self,unit):
        '''
        

        Parameters
        ----------
        unit : str
            Set the units for the X axis.
            sUnit = ['WAV','FREQ','WNUM']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['WAV','FREQ','WNUM']
        if unit in sUnit:
            self.write(':UNIT:X '+ unit)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_CenterWavelenght(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Set the center wavelength of the
            X-axis of the display scale
        unit : str
            sUnits = ['M','HZ']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['M','HZ']
        if unit in sUnit:
            self.write(':SENSE:WAVELENGTH:CENTER ' + str(value)+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_Span(self,value, unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Set the measurement condition
        measurement span.
        unit : str
            sUnits = ['M','HZ']

        Returns
        -------
        None.

        '''
        
        sUnit = ['M','HZ']
        if unit in sUnit:
            self.write(':SENSE:WAVELENGTH:SPAN '+str(value)+ str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_BWResolution(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Set the measurment resolution
        unit : str
            sUnit = ['M','HZ']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['M','HZ']
        if unit in sUnit:
            self.write(':SENSE:BANDWIDTH:RESOLUTION '+str(value)+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_Sensitivity(self,unit):
        '''
        

        Parameters
        ----------
        unit : str
            Set the measurement sensitivity.
                NHLD = NORMAL HOLD
                NAUT = NORMAL AUTO
                NORMal = NORMAL
                MID = MID
                HIGH1 = HIGH1 or HIGH1/CHOP
                HIGH2 = HIGH2 or HIGH2/CHOP
                HIGH3 = HIGH3 or HIGH3/CHOP

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnit = ['NHLD','NAUT','MID','HIGH1','HIGH2','HIGH3','NORMAL']
        if unit in sUnit:
            self.write(':SENSE:SENSE '+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_AverageCount(self,value):
        '''
        

        Parameters
        ----------
        value : int
            Set the number of times averaging for
            each measured point.

        Returns
        -------
        None.

        '''
        value = int(value)
        self.write(':SENSE:AVERAGE:COUNT '+str(value))
           
    
    
    
    
    def set_SegmentPoints(self,value):
        '''
        

        Parameters
        ----------
        value :int
            Set the number of sampling points
            to be measured at one time when performing
            SEGMENT MEASURE.

        Returns
        -------
        None.

        '''
        value = int(value)
        self.write(':SENSE:SWEEP:SEGMENT:POINTS '+str(value))
        
    
    
    
    
    def set_SamplePoints(self,value):
        '''
        

        Parameters
        ----------
        value : int
            Set the number of samples measured

        Returns
        -------
        None.

        '''
        
        value = int(value)
        self.write(':SENSE:SWEEP:POINTS '+str(value))
        
    
    
    
    
    def set_SweepSpeed(self,value):
        '''
        

        Parameters
        ----------
        value : int
            Set the sweep speed.
            1 - Standard
            2 - Twice as fast as standard

        Returns
        -------
        None.

        '''
        
        value = int(value)
        if value == 1: 
            self.write(':SENSE:SWEEP:SPEED 1x')
        elif value == 2:
            self.write(':SENSE:SWEEP:SPEED 2x')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_SamplePointsAuto(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Set the function of automatically
            setting the sampling number to be measured
            ['ON'|'OFF']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sState = ['ON'|'OFF']
        if state in sState:
            self.write(' :SENSE:SWEEP:POINTS:AUTO '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_TraceActive(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Sets the active trace.
            sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:    
            self.write(':TRACE:ACTIVE '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_SweepMode(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Set the sweep mode
            ['SINGle','REPeat','AUTO','SEGMent']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sState = ['SINGle','REPeat','AUTO','SEGMent']
        if state in sState:
            self.write('INITIATE:SMODE ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_TraceAttribute(self,trace,state):
        '''
        

        Parameters
        ----------
        trace : str
            Sets the active trace.
            sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
            
        state : str
            Set the attributes of the specified
            trace
            ['WRITe','FIX','MAX','MIN','RAVG','CALC']
            
            WRITe = WRITE
            FIX = FIX
            MAX = MAX HOLD
            MIN = MIN HOLD
            RAVG = ROLL AVG
            CALC = CALC


        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sState = ['WRITe','FIX','MAX','MIN','RAVG','CALC']
        sTrace = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        
        if state in sState and trace in sTrace:
            self.write(':TRACE:ATTRIBUTE:'+str(trace)+' '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
# =============================================================================
# get Data
# =============================================================================

    def get_Data(self,state):

        
        '''
        Get data on X and Y Traces from OSA.
        Data Output is CST File.
        Data is Saved in X Column and Y Column 
        state = 'TRA','TRB','TRC','TRD','TRE','TRF','TRG'
        '''
        sState = ['TRA','TRB','TRC','TRD','TRE','TRF','TRG']
        if state in sState:
            #Get Headers
            HeaderX = self.ask_UnitX()
            HeaderY = self.ask_DisplayYUnit()
            #Get Data
            dataX = self.ask_TraceDataX(state)
            dataY = self.ask_TraceDataY(state)
            
            #create CSV
            data = {str(HeaderX):dataX,str(HeaderY):dataY}
            Data = pd.DataFrame(data, columns=[str(HeaderX), str(HeaderY)])
            
            return Data
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def print_ParamsOSA(self):
        '''
        

        Returns
        -------
        srt 
            Parameters set on the Yokogawa AQ6370D

        '''
        
        print('################ OSA Parameters ################')
        print('Y-Axis units = ',self.ask_DisplayYUnit())
        print('X-Axis units = ',self.ask_UnitX())
        print('Start Wavelength = ',self.ask_WavelengthStart())
        print('Stop Wavelength = ',self.ask_WavelengthStop())
        print('Bandwidth Resolution = ',self.ask_BWResolution())
        print('Center Wavelenght = ',self.ask_CenterWavelenght())
        print('Span = ',self.ask_Span())
        print('Output data format = ',self.ask_DataFormat())
        print('Displayed trace = ',self.ask_TraceState())
        print('Selected Trace = ',self.ask_TraceActive())
        print('Averaging Points = ',self.ask_AverageCount())
        print('Sample Points = ',self.ask_SamplePoints())
        print('Sweep speed = ',self.ask_SweepSpeed())
        print('Sweep Mode = ',self.ask_SweepMode())
        print('################ OSA Parameters ################')
        
     
    
    def get_ParamsOSA(self):
        '''
        

        Returns
        -------
        srt 
            Parameters set on the Yokogawa AQ6370D

        '''
        Header = ['Y-Axis units','X-Axis units','Start Wavelength','Stop Wavelength',
                  'Bandwidth Resolution','Center Wavelenght','Span','Output data format',
                  'Displayed trace','Selected Trace','Averaging Points','Sample Points',
                  'Sweep speed','Sweep Mode']
        Data = []

        Data.append(self.ask_DisplayYUnit())
        Data.append(self.ask_UnitX())
        Data.append(self.ask_WavelengthStart())
        Data.append(self.ask_WavelengthStop())
        Data.append(self.ask_BWResolution())
        Data.append(self.ask_CenterWavelenght())
        Data.append(self.ask_Span())
        Data.append(self.ask_DataFormat())
        Data.append(self.ask_TraceState())
        Data.append(self.ask_TraceActive())
        Data.append(self.ask_AverageCount())
        Data.append(self.ask_SamplePoints())
        Data.append(self.ask_SweepSpeed())
        Data.append(self.ask_SweepMode())

        
        return Header,Data
        
        
        