#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:11:32 2021

@author: Martin.Mihaylov
"""

import numpy as np
import pyvisa as visa


    
class MS2760A:
    def __init__(self, resource_str):

        # self._resource = visa.ResourceManager().open_resource('TCPIP::' + str(resource_str) + '::9001::SOCKET',read_termination = '\n',query_delay  = 0.5)
        self._resource = visa.ResourceManager().open_resource(str(resource_str),read_termination = '\n',query_delay  = 0.5)
        print(self._resource.query('*IDN?'))

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        self._resource.close()
    

# =============================================================================
# Abort
# =============================================================================
    def abort(self):
        '''
        Description: Resets the trigger system. This has the effect of aborting the sweep or any measurement
        that is currently in progress.
        Additionally, any pending operation flags that were set by initiation of the trigger system
        will be set to false.
        If :INITiate:CONTinuous is OFF (i.e. the instrument is in single sweep mode), send the
        command :INITiate[:IMMediate] to trigger the next sweep.
        If :INITiate:CONTinuous is ON (i.e. the instrument is in continuous sweep mode) a new
        sweep will start immediately
        '''
        self.write(':ABORt')
        
    
    
# =============================================================================
# Start Measurment
# =============================================================================
 
    def Init(self):
        '''
        

        Returns
        -------
        None.
            Initialize meas

        '''
        
        self.write(':INITiate:IMMediate')
    
    
# =============================================================================
# OPC
# =============================================================================
    
    def OPC(self):
        '''
        

        Returns
        -------
        TYPE str
            Places a “1” into the output queue when all device
            operations have been completed
        '''
        
        
        return self.query('*OPC?')
    


# =============================================================================
# Ask Frequency
# =============================================================================
    def ask_freq_Start(self):
        '''
        

        Returns
        -------
        TYPE str
            Query return set start Frequency.
            Numeric (Hz)

        '''
        
        return self.query(':SENSe:FREQuency:STARt?')
        
    
    
    
    
    def ask_freq_Stop(self):
        '''
        

        Returns
        -------
        TYPE str 
            Query return set stop Frequency.
            Numeric (Hz)

        '''
        
        return self.query(':SENSe:FREQuency:STOP?')

    
    
    
    
    def ask_ResBwidth(self):
        '''
        

        Returns
        -------
        TYPE str
            Ask the resolution bandwidth.
            Query Return: Numeric (Hz)

        '''
        
        return float(self.query(':SENSe:BANDwidth:RESolution?'))
    
    
    
    
    
    def ask_SingleOrContinuesMeas(self):
        '''
        

        Returns
        -------
        data : str
            The query version of the command returns a 1 if the instrument is
            continuously sweeping/measuring and returns a 0 if the instrument is in single
            sweep/measurement mode.

        '''
        
        data = self.query(':INITiate:CONTinuous?')
        if data == '1':
            data = 'The instrument is continuously sweeping/measuring mode!'
        else:
            data = 'The instrument is in single sweep/measurement mode!'
        return data
    
    
    
    
    
    def ask_Configuration(self):
        '''
        

        Returns
        -------
        TYPE str
            Title: Option Configuration
            Description: This command returns a quoted string of characters readable only by Anritsu Customer
            Service. Only instrument configuration information is returned. No setup information is
            included.

        '''
        
        return self.query(':SYSTem:OPTions:CONFig?')
    
    
    
    
    
    def ask_sweepTime(self):
        '''
        

        Returns
        -------
        TYPE str
            Title: Measured Sweep Time
            Description: This command queries the measured sweep time, in number of milliseconds. This
            command will return "nan" if no measured sweep time is available, which happens if the
            sweep was reset and the instrument has not yet swept enough to measure a full sweep.

        '''
        
        return self.query(':DIAGnostic:SWEep:TIME?')
    
    
    
    
    
    def ask_TraceData(self,traceNumber):
        '''
        !!!!!DONT USE IT!!!!! 

        Parameters
        ----------
        traceNumber : int
            Description: This command transfers trace data from the instrument to the controller. Data are
            transferred from the instrument as an IEEE definite length arbitrary block response,
            which has the form <header><block>.

        Returns
        -------
        TYPE str
           Trace Data

        '''
        
        traceNumber = str(traceNumber)
        return self.query(':TRACe:DATA? ' + traceNumber)
        
    
    
    
    
    def ask_ResBwidthAuto(self):
        '''
        

        Returns
        -------
        val : str
            Query the resolution bandwidth.
            Defaoulf: ON

        '''
        
        val = self.query(':SENSe:BANDwidth:RESolution:AUTO?')
        if val == '0':
            val = 'OFF'
        else:
            val = 'ON'
        return val
    
    
    
    
    
    def ask_DataPointCount(self):
        '''
        
        Returns
        -------
        TYPE str
            Query the data point count.
            Title: Display Point Count
            Query Return: Numeric

        '''
        
        return self.query(':DISPlay:POINtcount?')
    
    
    
    
    def ask_MarkerExcursionState(self):
        '''
        

        Returns
        -------
        str
            Turn on/off excursion checking for marker max commands

        '''
        
        data = self.write(':CALCulate:MARKer:PEAK:EXCursion:STATe?')
        if data == '0':
            return 'OFF'
        else:
            return 'ON'
        
        
        
        
    
    def ask_MarkerExcursion(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the excursion for a marker. The excursion is the vertical distance from the peak to
            the next highest valley which must be exceeded for a peak to be considered a peak in
            marker max commands

        '''
        
        return self.query(':CALCulate:MARKer:DATA:ALL?')
        
    
    
    
    
    def ask_CHPowerState(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
        
            Channel Power State
            Sets the state of the channel power measurement, ON or OFF. When using
            :CONFigure:CHPower,the state is automatically set to ON
            state = ['ON','OFF',1,0]

        Returns
        -------
        str
            State ON or OFF

        '''
       
        data = self.query(':SENSe:CHPower:STATe?')
        if data == '0':
            return 'OFF'
        else:
            return 'ON'
        
        
        
        
    def ask_DataFormat(self):
        '''
        

        Returns
        -------
        TYPE str
             Query the data format

        '''
        
        return self.query(':FORMat:TRACe:DATA?')
    
    
    
    
    def ask_CenterFreq(self):
        '''
        

        Returns
        -------
        TYPE float
            Query the Central Frequency
            Numeric (Hz)
        '''
        
        return float(self.query(':SENSe:FREQuency:CENTer?'))
    
    
    

    def ask_TraceType(self,number):
        '''
        

        Parameters
        ----------
        number : int
            Specifies how successive sweeps are combined to produce the resulting display value.
            Setting the TYPE to NORMal will cause the displayed value for a point to be the current
            measured value for that point. Setting the TYPE to AVERage will cause the displayed
            value for a point to be the average of the last <integer> measured values where <integer>
            is set by [:SENSe]:AVERage:COUNt. Setting the TYPE to MAXimum will cause the
            displayed value for a point is the maximum measured value for that point over sweeps.
            Setting the TYPE to MINimum will cause the displayed value for a point is the minimum
            measured value for that point over sweeps.Setting the TYPE to RMAXimum will cause
            the displayed value for a point to be the maximum of the last <integer> measured values
            where <integer> is set by [:SENSe]:AVERage:COUNt.Setting the TYPE to RMINimum
            will cause the displayed value for a point to be the minimum of the last <integer>
            measured values where <integer> is set by [:SENSe]:AVERage:COUNt. This command
            will be ignored when spectrogram is disabled by DISPlay:VIEW.
            
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE str
            Query Return: NORM|MIN|MAX|AVER|RMAX|RMIN|RAV

        '''
        
        stNumber = [1,2,3,4,5,6]
        if number in stNumber:
            number = str(number)
            return self.query(':TRACe' + number+':TYPE?')
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
            
            
            
            
    def ask_TraceSelected(self):
        '''
        

        Returns
        -------
        TYPE str
            Query selected trace will be used by operations that use a single trace. The max number of
            traces available to select is model specific

        '''
        '''
        The selected trace will be used by operations that use a single trace. The max number of
        traces available to select is model specific
        '''
        return self.query(':TRACe:SELect?')
    
    
    
    def ask_TraceState(self,number):
        '''
        

        Parameters
        ----------
        number : int
                 Description: The trace visibility state. If it is OFF, the :TRAC:DATA? command will return nan.
                Trace Number:
                    int. [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        str
            State ON or OFF

        '''
       
        stNumber = [1,2,3,4,5,6]
        if number in stNumber:
            number = str(number)
            state = self.query(':TRACe'+number+':DISPlay:STATe?')
            if state == '0':
                return 'Trace is OFF'
            else:
                return 'Trace is ON'
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
        
        
        
        
        
    
    
# =============================================================================
# Get Data
# =============================================================================
   

        
    
    
# =============================================================================
#  Test param from MatLab Scripts
# =============================================================================
    def set_DataPointCount(self,value):
        '''
        

        Parameters
        ----------
        value : int
                Title: Display Point Count
                Description: Changes the number of display points the instrument currently measures. Increasing the
                number of display points can improve the resolution of measurements but will also
                increase sweep time.
                
               Default Value: 501
               Range: 10 to 10001

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if float(value) <=10 or float(value)>= 10001:
            value = str(value)
            self.write(':DISPlay:POINtcount ' + value)
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
    
    
    
    
    def set_freq_Start(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Description: Sets the start frequency. Note that in the spectrum analyzer, changing the value of the
            start frequency will change the value of the coupled parameters, Center Frequency and
            Span.
                
        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['HZ','KHZ','MHZ','GHZ']
        if unit in stUnit:
            self.write(':SENSe:FREQuency:STARt ' + str(value) + ' ' + unit)
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def set_freq_Stop(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
                Description: Sets the start frequency. Note that in the spectrum analyzer, changing the value of the
                start frequency will change the value of the coupled parameters, Center Frequency and
                Span.
            
        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['HZ','KHZ','MHZ','GHZ']
        if unit in stUnit:
            self.write(':SENSe:FREQuency:STOP ' + str(value) + ' ' + unit)
        else:
            raise ValueError('Unknown input! See function description for more info.')   
            
    
    
    
    
    def set_ResBwidth(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Description: Sets the resolution bandwidth.
            Note that using this command turns the automatic resolution bandwidth setting OFF.
            In Zero Span, the range will change to allow a mininum of 5 KHz to the maximum of 20
            MHz.
        unit : str
            Parameters: <numeric_value> {HZ | KHZ | MHZ | GHZ}
            Default Unit: Hz
                

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['HZ','KHZ','MHZ','GHZ']
        if unit in stUnit:
            self.write(':SENSe:BANDwidth:RESolution ' + str(value) + ' ' + unit)
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
    
    
    
    
    def set_ResBwidthAuto(self,state):
        '''
        

        Parameters
        ----------
        state : int/str
            Title:RBW AutoDescription:Sets the state of the coupling of the resolution bandwidth 
            to the frequency span. Setting the value to ON or 1 will result in the resolution
            bandwidth being coupled to the span. That is, when the span changes, the 
            resolution bandwidth changes. Setting the value to OFF or 0 will result in the 
            resolution bandwidth being decoupled from the span. That is, changing the span 
            will not change the resolution bandwidth. When this command is issued, the resolution 
            bandwidth setting itself will not change.
            Parameters:<1 | 0 | ON | OFF>
            Default Value:ON

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
        
        stList = ['ON','OFF',1,0]
        if state in stList:
            self.write(':SENSe:BANDwidth:RESolution:AUTO ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_CenterFreq(self,value,unit):
        '''
        

        Parameters
        ----------
        value : float 
            Sets the center frequency. Note that changing the value of the center frequency will
            change the value of the coupled parameters Start Frequency and Stop Frequency. It
            might also change the value of the span.
            
        unit : str
            Unit value. Can be ['HZ','KHZ','MHZ','GHZ']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sUnits = ['HZ','KHZ','MHZ','GHZ']
        
        if unit in sUnits:
            self.write(':SENSe:FREQuency:CENTer '+str(value) + ' '+ str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    def set_ContinuousMeas(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
            Title: Sweep Type
            Description: Specifies whether the sweep/measurement is triggered continuously. If the value is set to
            ON or 1, another sweep/measurement is triggered as soon as the current one completes.
            If continuous is set to OFF or 0, the instrument remains initiated until the current
            sweep/measurement completes, then enters the 'idle' state and waits for the
            :INITiate[:IMMediate] command or for :INITiate:CONTinuous ON.

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
        
        stList = ['ON','OFF',1,0]
        if state in stList:
            state = str(state)
            self.write(':INITiate:CONTinuous ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_DataFormat(self,status):
        '''
        

        Parameters
        ----------
        status : str
            Set Data Format status =  ['ASCii','INTeger','REAL']

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        statusLs = ['ASCii','INTeger','REAL']
        if status in statusLs:    
            self.write(':FORMat:TRACe:DATA ' + str(status))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            



    
    def set_Continuous(self,status):
        '''
        

        Parameters
        ----------
        status : str/int
            Stop/start Sweep. Can be ['ON', 'OFF', 1, 0]

        Raises
        ------
        ValueError
            Error message
            
            
        Returns
        -------
        None.

        '''

        satusLs = ['ON', 'OFF', 1, 0]
        if status in satusLs:
            self.write('INIT:CONT '+str(status))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
        
    def set_MarkerExcursionState(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
            Turn on/off excursion checking for marker max commands.
            Can be state = ['ON','OFF',1,0]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        if state in ['ON','OFF',1,0]:
            self.write(':CALCulate:MARKer:PEAK:EXCursion:STATe ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_MarkerExcursion(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the excursion for a marker. The excursion is the vertical distance from the peak to
            the next highest valley which must be exceeded for a peak to be considered a peak in
            marker max commands

        Returns
        -------
        None.

        '''
        self.write(':CALCulate:MARKer:PEAK:EXCursion ' + str(value)+' DB')
        
        
        
        
        
    def set_NextPeak(self):
        '''
        

        Returns
        -------
        None.
            Moves the marker X value to the point in the marker's assigned 
            trace that is the next highest peak

        '''
        self.write(':CALCulate:MARKer:MAXimum:NEXT')
        
        
        
        
        
    def set_MaxPeak(self):
        '''

        Returns
        -------
        None.
            Moves the marker X value to the point in the marker's assigned 
            trace that has the highest peak.

        '''
        self.write(':CALCulate:MARKer:MAXimum')
        
        
        
        
        
    def set_MarkerPreset(self):
        '''
        

        Returns
        -------
        None.
            Presets all markers to their preset values.

        '''
        self.write(':CALCulate:MARKer:APReset')
        
        
        
        
    def set_CHPowerState(self,state):
        '''
        

        Parameters
        ----------
        state :str
            Sets the state of the channel power measurement, ON or OFF. When using
            :CONFigure:CHPower,the state is automatically set to ON
            state = ['ON','OFF',1,0]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stList = ['ON','OFF',1,0]
        if state in stList:
            state = str(state)
            self.write(':SENSe:CHPower:STATe ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
        
    def set_TraceType(self,state,number):
        '''
        

        Parameters
        ----------
        state : str
             Sets Trace Type:
                            Normal - NORM
                            Hold the Minimmum - MIN
                            Hold the Maximum - MAX
                            Average - AVER
                            Rolling Max Hold - RMAX
                            Rolling Min Hold - RMIN
                            Rolling Avarage - RAV
        number : int
            Trace number:
                        Can be set to [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stList = ['NORM', 'MIN', 'MAX', 'AVER', 'RMAX', 'RMIN', 'RAV']
        stNumber = [1,2,3,4,5,6]
        if state in stList and number in stNumber:
            state = str(state)
            number = str(number)
            self.write(':TRACe'+number+':TYPE ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    
    def set_TraceSelected(self,number):
        '''
        

        Parameters
        ----------
        number : int
            The selected trace will be used by operations that use a single trace. The max number of
            traces available to select is model specific.
            Trace number:
                        Can be set to [1,2,3,4,5,6]

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stNumber = [1,2,3,4,5,6]

        if number in stNumber:
            number = str(number)
            self.write(':TRACe:SELect '+number)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
            
    def set_TraceState(self,state,number):
        '''
        

        Parameters
        ----------
        state : str
            The trace visibility state status. If it is OFF, the :TRAC:DATA? 
            command will return NaN.
            ['ON','OFF',0,1]
        number : int
            Trace Number:
                Can be set to  [1,2,3,4,5,6]

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
        
        stNumber = [1,2,3,4,5,6]
        stList = ['ON','OFF',0,1]
        if number in stNumber and state in stList:
            state = str(state)
            number = str(number)
            self.write(':TRACe'+number+':DISPlay:STATe '+state)
            
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
            
            
            
# =============================================================================
#   get/Save Data   
# =============================================================================



    def get_Data(self):
        '''
        
        This function will stop temporally set Continuous Measurment to OFF, extract 
        the max.peak value and frequency and restore the Continuous Measurment to ON.
        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured voltage and current.

        '''
        OutPut = {}
        self.set_ContinuousMeas('OFF')
        self.set_MarkerPreset()
        self.set_MaxPeak()
        Power = float(self.ask_MarkerExcursion().split(',')[1].split(')')[0])
        Freq = float(self.ask_MarkerExcursion().split(',')[0].split('(')[1])
        self.set_MarkerPreset()
        self.set_ContinuousMeas('ON')
        OutPut['Power/dBm'] = Power
        OutPut['Frequency/Hz'] = Freq
        return OutPut
        
    
    
    
    def ExtractTtraceData(self,value):
        '''
        

        Parameters
        ----------
        value : int
        
        !!!!!USE IT AT YOUR OWN RISK is not an official function, but a workaround!!!!! 
        
            Trace Number from which the data is taken:
                Can be set to  [1,2,3,4,5,6].
            1 - This Function will set the continues measurment to 'OFF'.
            2 - Will set the Data Format to ASCii. This is needed since
            :TREACE:DATA? <num> is defect!! 
            3 - Will write TRACE:DATA? <num>. Will return only 3 bits. The rest
            will be packed in the next command asked.
            4 - Will ask for the Data Format. This is dummy command that will 
            have the data and the Data Format.
            5 - Make manupulations to separate the actual data from the rest and
            return the data in Output np.array() form.

        Returns
        -------
        Output : TYPE
            DESCRIPTION.

        '''
        
        self.set_Continuous('OFF')
        self.set_DataFormat('ASCii')
        data = self.write(':TRACe:DATA? '+str(value))
        data = self.ask_DataFormat()
        new_str = data[6:-5]
        data_arr = new_str.split(',')
        Output = [float(item) for item in data_arr]
        Output = np.array(Output)
        self.set_Continuous('ON')
        return Output
