# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:57:49 2022

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa


    
class APPH:
    def __init__(self, resource_str):

        self._resource = visa.ResourceManager().open_resource(str(resource_str),query_delay  = 0.5,read_termination = '\n')
        print(self._resource.query('*IDN?'))

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        print('AnaPico AG,APPH20G is closed!')
        self._resource.close()
        
        
# =============================================================================
# Initiate System
# =============================================================================
    def Init(self):
        '''
        

        Returns
        -------
        None.
            Initialize the measurement

        '''
        self.write(':INITiate:IMMediate')
        
# =============================================================================
# Abort
# =============================================================================

    def Abort(self):
        '''
        

        Returns
        -------
        None.
            Abort measurement

        '''
        
        self.write(':ABORt')
        
# =============================================================================
# ASK
# =============================================================================

    def ask_CalcFreq(self):
        '''
        

        Returns
        -------
        TYPE float 
            Reads back the detected frequency from a frequency search.

        '''
        return float(self.query(':CALCulate:FREQuency?').split('\n')[0])




    def ask_CalcPower(self):
        '''
        

        Returns
        -------
        TYPE float
            Reads back the detected power level from a frequency search.

        '''
        
        return float(self.query(':CALCulate:POWer?').split('\n')[0])  
    


    
    def ask_DUTPortVoltage(self):
        '''
        

        Returns
        -------
        TYPE float
           Sets/gets the voltage at the DUT TUNE püort. Returns the configured value. If the output is
           turned off, it doesn’t necessarily return 0, as an internal voltage may be configured.

        '''
        return float(self.query(':SOURce:TUNE:DUT:VOLT?').split('\n')[0])
    
    
    
    
    def ask_DUTPortStatus(self):
        '''
        

        Returns
        -------
        stat : str
           Query the status of the DUT TUNE port.

        '''
        
        stat = self.query('SOURce:TUNE:DUT:STAT?').split('\n')[0]
        if stat == '0':
            stat = 'OFF'
        else:
            stat = 'ON'
        return stat
    
    
    
    
    def ask_SysMeasMode(self):
        '''
        

        Returns
        -------
        TYPE str
            Gets the active measurement mode.

        '''
        return self.query('SENSe:MODE?')
    
    
    
    
    def ask_SystemError(self):
        '''
        

        Returns
        -------
        TYPE list
            Return parameters: List of integer error numbers. This query is a request for all 
            entries in the instrument’s error queue. Error messages in the queue contain an 
            integer in the range [-32768,32768] denoting an error code and associated descriptive
            text. This query clears the instrument’s error queue.

        '''
        
        return self.query(':SYSTem:ERRor:ALL?')
    
    
# =============================================================================
# Ask Phase Noise
# =============================================================================

    def ask_PMTraceJitter(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns the RMS jitter of the current trace.

        '''
            
        return self.query(':CALCulate:PN:TRACE:SPURious:JITTer?')
        
        
        
        
        
    def ask_PMTraceNoise(self):
        '''
        

        Returns
        -------
        TYPE list
            Returns a list of phase noise points of the most recent measurement as block data.

        '''
        return self.query(':CALCulate:PN:TRACe:NOISe?')  
    
    
    
    
    
    def ask_PN_IFGain(self):
        '''
        

        Returns
        -------
        TYPE float
            Range: 0-60
            Query the IF gain for the measurement.

        '''
        return float(self.query(':SENSe:PN:IFGain?'))
    
    
    
    
    def ask_PN_StartFreq(self):
        '''
        

        Returns
        -------
        TYPE float
            Query the start offset frequency

        '''
        return float(self.query(':SENSe:PN:FREQuency:STARt?').split('\n')[0])
    
    
    
    
    
    def ask_PN_StopFreq(self):
        '''
        

        Returns
        -------
        TYPE float
            Query the stop offset frequency

        '''
        return float(self.query(':SENSe:PN:FREQuency:STOP?').split('\n')[0])
    
    
    
    def ask_PNSpot(self,value):
        '''
        

        Parameters
        ----------
        value : float 
            The parameter is given as offset frequency in [Hz]
            Unit Hz
            Value - float

        Returns
        -------
        TYPE str
            Returns the phase noise value of the last measurement at the offset frequency 
            defined in <value>. The parameter is given as offset frequency in [Hz]
            Unit Hz
            Value - float

        '''
        
        return self.query('CALCulate:PN:TRACE:SPOT? '+str(value))
    
    
# =============================================================================
# Ask Amplitude Noise
# =============================================================================

    
    def ask_ANTraceFreq(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns a list of offset frequency values of the current measurement as block data.
            Hz

        '''
        
        return self.query(':CALCulate:AN:TRACe:FREQuency?')
    
    
    
    def ask_ANTraceNoise(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns a list of amplitude noise spectrum values of the current measurement as block data
            Unit dBc/Hz

        '''
       
        return self.query('CALCulate:AN:TRACe:NOISe?')
    
    
    
    
    def ask_ANTraceSpurFreq(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns a list of offset frequencies of the spurs in the active trace as block data.
            Unit Hz

        '''
        
        return self.query(':CALCulate:AN:TRACe:SPURious:FREQuency?')
    
    
    
    
    def ask_ANTraceSpurPower(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns a list of power values of the spurs in the active trace as block data.
            Unit dBc

        '''
        
        return self.query(':CALCulate:AN:TRACe:SPURious:POWer?')
    
    
    
    
    def ask_ANSpot(self,value):
        '''
        

        Parameters
        ----------
        value : TYPE
            The parameter is given as offset frequency in [Hz]
                Unit Hz
                Value - float

        Returns
        -------
        TYPE str
            Returns the phase noise value of the last measurement at the offset frequency 
            defined in <value>. The parameter is given as offset frequency in [Hz]
            Unit Hz
            Value - float

        '''
       
        return self.query('CALCulate:AN:TRACE:SPOT? '+str(value))
    
    
# =============================================================================
# Ask Frequency Noise
# =============================================================================


    def ask_FNTraceFreq(self):
        '''
        

        Returns
        -------
        TYPE lisz
            Returns a list of offset frequency values of the current measurement as block data.
            Unit Hz

        '''
       
        return self.query(':CALCulate:FN:TRACe:FREQuency?')
    
    
    
    def ask_FNTraceNoise(self):
        '''
        

        Returns
        -------
        TYPE list
             Returns a list of phase noise spectrum values of the current measurement as block data.
             Unit Hz
        '''
        
        return self.query(':CALCulate:FN:TRACe:NOISe?')
    
    
    
    def ask_FNTraceSpurFreq(self):
        '''
        

        Returns
        -------
        TYPE list
            Returns a list of offset frequencies of the spurs in the active trace as block data.
            Unit Hz
        '''
        
        return self.query(':CALCulate:FN:TRACe:SPURious:FREQuency?')
    
    
    
    def ask_FNTraceSpurPower(self):
        '''
        

        Returns
        -------
        TYPE list
               Returns a list of power values of the spurs in the active trace as block data.
               Unit Hz

        '''
        
        return self.query(':CALCulate:FN:TRACe:SPURious:POWer?')
    
    
    
    def ask_FNSpot(self,value):
        '''
        

        Parameters
        ----------
        value : float
            The parameters defines the spot noise offset frequency in [Hz].
                Unit Hz
                Value - float

        Returns
        -------
        TYPE str
            Returns the spot noise value at the specified offset frequency. 

        '''
        
        return self.query('CALCulate:FN:TRACE:SPOT? '+str(value))
    
    
    
# =============================================================================
# Ask Voltage controlled Oscillator
# =============================================================================

    def ask_VCOTraceFreq(self):
        '''
        

        Returns
        -------
        TYPE list
            Returns a list of frequency values measured at each tune voltage point of the 
            current measurement as block data2.

        '''
       
        return self.query('CALCulate:VCO:TRACE:FREQuency?')
    
    
    
    def ask_VCOTracePNoise(self,chan):
        '''
        

        Parameters
        ----------
        chan : ist
            Can be set to [1,2,3,4]

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        TYPE list
            Returns a list of phase noise values measured at each tune voltage point of 
            the current measurement as block data. The parameter 1-4 selects the offset 
            frequency from the set defined by the SENS:VCO:TEST:PN:OFFS <list> command

        '''
        chanLS = [1,2,3,4]
        if chan in chanLS:
            return self.query('CALCulate:VCO:TRACE:PNoise? '+str(chan))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def ask_VCOTracePower(self):
        '''
        

        Returns
        -------
        TYPE list 
            Returns a list of power values measured at each tune voltage point of the current 
            measurement as block data.

        '''
       
        return self.query('CALCulate:VCO:TRACE:POWer?')
    
    
    
    def ask_VCOTraceVoltage(self):
        '''
        

        Returns
        -------
        TYPE list
            Returns a list of tune voltage values measured at each tune voltage point of the 
            current measurement as block data.

        '''
        
        return self.query('CALCulate:VCO:TRACE:VOLTage?')
    
    
    
    
    def ask_VSOTestFreq(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the frequency parameter for the measurement.

        '''
        return self.query(':SENSe:VCO:TEST:FREQuency?')   
    
    
    
    
    def ask_VSOTestNoise(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the the phase noise parameter for the measurement.

        '''
       
        return self.query(':SENSe:VCO:TEST:PNoise?')   
    
    
    
    
    def ask_VCOTestPower(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the power parameter for the measurement.

        '''

        return self.query(':SENSe:VCO:TEST:POWer?')   
    
    
    
    
    def ask_VCOTestStart(self):
        '''
        

        Returns
        -------
        TYPE str
             Query the start tuning voltage for the measurement.
             Unit V

        '''
        
        return self.query(':SENSe:VCO:VOLTage:STARt?')
    
    
    
    
    def ask_VCOTestStop(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the stop tuning voltage for the measurement.
            Unit V

        '''
        
        return self.query(':SENSe:VCO:VOLTage:STOP?')
    
    
    
    
    def ask_VCOTestISupply(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the supply current parameter for the measurement

        '''
        
        return self.query(':SENSe:VCO:TEST:ISUPply?')
    
    
    
    def ask_VCOKPuShing(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the pushing parameter for the measurement

        '''
        
        return self.query(':SENSe:VCO:TEST:KPUShing?')
    
    
    
    
    def ask_VCOKVCO(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the tune sensitivity parameter for the measurement.

        '''
       
        return self.query(':SENSe:VCO:TEST:KVCO?')
        
    
    
        
    def ask_VCOTYPE(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the DUT type for the measurement.

        '''
        
        return self.query(':SENSe:VCO:TYPE?')
    
    
    
    def ask_VCOTestPNoise(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the phase noise parameter for the measurement.

        '''
        
        return self.query(':SENSe:VCO:TEST:PNoise?')
    
    
    
    def ask_VCOTestPnoiseOFFSet(self,state):
        '''
        

        Parameters
        ----------
        state : int
            Can be set to [1,2,3,4]

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        TYPE str
            Query the 4 offset frequencies at which the phase noise is measured

        '''
        
    
        stateLs = [1,2,3,4]
        if state in stateLs:
            return self.query(':SENSe:VCO:TEST:Pnoise:OFFSet'+str(state)+'?')
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    def ask_VCOTestPoint(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the number rof voltage points to use in the measurement

        '''
        return self.query(':SENSe:VCO:VOLTage:POINts?')
        
        
# =============================================================================
# SET
# =============================================================================

    def set_Output(self,status):
        '''
        

        Parameters
        ----------
        status : str
            Set Output ON and OFF.  CAn be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        statusLs = ['ON','OFF']
        if status in statusLs:
            self.write(':OUTput '+status)
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    def set_SysMeasMode(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Sets/gets the active measurement mode. Can be ['PN','AN','FN','BB','TRAN','VCO']
                • PN: phase noise measurement
                • AN: amplitude noise measurement
                • FN: frequency noise measurement (results are converted to phase noise)
                • BB: base band measurement (not yet available)
                • TRAN: transient analysis (not yet available)
                • VCO: voltage controlled oscillator characterization

        Raises
        ------
        ValueError
            Error massage


        Returns
        -------
        None.

        '''
        
        stateLs = ['PN','AN','FN','BB','TRAN','VCO']
        if state in stateLs:
            self.write('SENSe:MODE '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_FreqExecute(self):
        '''
        

        Returns
        -------
        None.
            Starts the frequency search. See the CALCulate subsystem on how to read out the result.

        '''
        
        self.write('SENSe:FREQuency:EXECute?')
        
        
        
        
    def set_PowerExecute(self):
        '''
        

        Returns
        -------
        None.
            Starts the power measurement. When performing SENS:FREQ:EXEC, this measurement 
            will be automatically run at the end (if a signal is detected

        '''
        
        self.write('SENSe:POWer:EXECute?')
        
        
        
    def set_CalcAverage(self,event):
        '''
        
        
        Parameters
        ----------
        event : str
                Waits for the defined event 
                NEXT: next iteration complete 
                ALL: measurement complete
                <value>: specified iteration complete 
                Optionally, a timeout in milliseconds can be specified as a second parameter. 
                This command will block further SCPI requests until the specified event or the
                specified timeout has occurred. If no timeout is specified, the timeout will be 
                ininite.

        Returns
        -------
        None.

        '''
        self.write('CALCulate:WAIT:AVERage '+str(event))
        


    def set_DUTPortVoltage(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the voltage at the DUT TUNE püort. Returns the configured value. 
            If the output is turned off, it doesn’t necessarily return 0, as an internal
            voltage may be configured
            
            
        Returns
        -------
        None.

        '''
        
        self.write(':SOURce:TUNE:DUT:VOLT '+str(value))
        
    
    def set_DUTPortStatus(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the DUT TUNE port. Can be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SOURce:TUNE:DUT:STAT '+str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
        
            
    
# =============================================================================
# Set Phase Noise
# =============================================================================

    def set_PNIFGain(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Range: 0-60
            Sets the IF gain for the measurement.

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        if value>60.0:
            raise ValueError('Unknown input! See function description for more info.')
        else:
            self.write(':SENSe:PN:IFGain '+str(value))
            
            
            
            
    def set_PNStartFreq(self,value):
        '''
        

        Parameters
        ----------
        value : float
                    Unit HZ
                    Sets the start offset frequency.

        Returns
        -------
        None.

        '''
        
        self.write(':SENSe:PN:FREQuency:STARt '+str(value))
        
        
    def set_PNStopFreq(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Unit HZ
            Sets the stop offset frequency.

        Returns
        -------
        None.

        '''
       
        self.write(':SENSe:PN:FREQuency:STOP '+str(value))
        
        
        
# =============================================================================
# Set Voltage controlled Oscillators
# =============================================================================
        

    def set_VCOWait(self,state,value):
        '''
        

        Parameters
        ----------
        state : str
            Can be ['ALL','NEXT']
        value : float
            This command requests a preliminary result during the measurement and blocks until 
            the resultis ready. The first parameter (required) specifies the target iteration 
            to be saved. NEXT specifies the next possible iteration, ALL specifies the last 
            iteration of the measurement (i.e. waits for the measurement to finish) and an 
            iteger specifies the specific iteration requested.The second parameter (optional) 
            defines a timeout in milliseconds. If the command terminates without generating a 
            preliminary result. It will produce an error. This error can be queried with
            SYST:ERR? or SYST:ERR:ALL?.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        
        
        stateLs = ['ALL','NEXT']
        if state in stateLs:
            return self.query('CALCulate:VCO:WAIT '+str(state)+' '+str(value))
        
        
        
        
    def set_VCOTestFreq(self,state):
        '''
        

        Parameters
        ----------
        state : str 
            Enables/disables the frequency parameter for the measurement.
            Can be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:FREQuency ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_VCOTestNoise(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the phase noise parameter for the measurement
            Can be  ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:PNoise ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_VCOTestPower(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the power parameter for the measurement.
            Can be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
    
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:POWer ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
            
    
    def set_VCOTestStart(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the start tuning voltage for the measurement.
            Unit V

        Returns
        -------
        None.

        '''
        
        self.write(':SENSe:VCO:VOLTage:STARt '+ str(value))
        
        
        
    
    def set_VCOTestStop(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the stop tuning voltage for the measurement.
            Unit V

        Returns
        -------
        None.

        '''
        
        self.write(':SENSe:VCO:VOLTage:STOP '+ str(value))
        
        
        
        
    def set_VCOTestISupply(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the supply current parameter for the measurement.
            Can be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:ISUPply ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
    
    def set_VCOKPuShing(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the pushing parameter for the measurement.
            Can be ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:KPUShing ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_VCOKVCO(self,state):
        '''
        

        Parameters
        ----------
        state : str
           Enables/disables the tune sensitivity parameter for the measurement
           Can be ['ON','OFF']
           
        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:KVCO ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_VCOTYPE(self,typ):
        '''
        

        Parameters
        ----------
        typ : str
            Select the DUT type for the measurement. Distinguish between slow (VCXO) and fast
            (VCO) tuning sensitivities. Can be ['VCO','VCXO']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        typLs = ['VCO','VCXO']
        if typ in typLs:
            self.write(':SENSe:VCO:TYPE ' +str(typ))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
        
    def set_VCOTestPNoise(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Enables/disables the phase noise parameter for the measurement.
            CAn be set to ['ON','OFF']

        Raises
        ------
        ValueError
            Error massage

        Returns
        -------
        None.

        '''
        
        stateLs = ['ON','OFF']
        if state in stateLs:
            self.write(':SENSe:VCO:TEST:PNoise ' +str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_VCOTestPnoiseOFFSet(self,value1,value2,value3,value4):
        '''
        

        Parameters
        ----------
        value1 : float
            freq val 1
        value2 : float
            freq val 2
        value3 : float
            freq val 3
        value4 : float
            freq val 4


        Sets up to 4 offset frequencies at which the phase noise is measured. 
        At least 1 parameter is required. Blank parameters are set to 0 
        (disabled). The query returns the set frequency for the specified 
        offset. The offset can be specified with the <sel> parameter and can 
        be chosen from 1|2|3|4
        
        Unit HZ
        
        Returns
        -------
        None.

        '''
        
        self.write(':SENSe:VCO:TEST:Pnoise:OFFSet ' +str(value1)+','+str(value3)+','\
                   +str(value4)+','+str(value4))
        
            
            
    def set_VCOTestPoint(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the number rof voltage points to use in the measurement

        Returns
        -------
        None.

        '''
        
        self.write(':SENSe:VCO:VOLTage:POINts '+str(value))


# =============================================================================
# Get Functions
# =============================================================================
        
        
    def getIdn(self):
        '''
        

        Returns
        -------
        TYPE Str
            Queries the device serial number and name

        '''
        
        return self.query('*IDN?')
        
        
            
# =============================================================================
# Measurments Examples 
# =============================================================================
    
    def PNMeasExample(self,value):
        '''
        This is a small example how to make a Phase Noise measurment.
        '''
        
        self.set_SysMeasMode('PN') # select phase noise measurement
        self.Init()                # start measurement
        self.set_CalcAverage('ALL') # wait for the measurement to finish
        err = self.ask_SystemError()     # check if measurement was successful
        val = self.ask_PNSpot(value) #request spot noise value at 1MHz offset
        ResultDic = {}
        ResultDic['Erro Value'] = err #Write Error status if 0 no errors!
        ResultDic['Spot Phase Noise @ ' +str(value)] = val
        return ResultDic
    
    
    
    def ANMeasExample(self,value):
        '''
        This is a small example how to make a Phase Noise measurment.
        '''
        self.set_SysMeasMode('AN') # select amplitude noise measurement
        self.Init()                # start measurement
        err = self.ask_SystemError()     # check if measurement was successful
        val = self.ask_ANSpot(value) #request spot noise value at 1MHz offset
        ResultDic = {}
        ResultDic['Erro Value'] = err #Write Error status if 0 no errors!
        ResultDic['Spot Amplitude Noise @ ' +str(value)] = val
        return ResultDic




    def FNMeasExample(self,value):
        '''
        This is a small example how to make a Frequency Noise measurment.
        '''
        self.set_SysMeasMode('FN') # select amplitude noise measurement
        self.Init()                # start measurement
        err = self.ask_SystemError()     # check if measurement was successful
        val = self.ask_FNSpot(value) #request spot noise value at 1MHz offset
        ResultDic = {}
        ResultDic['Erro Value'] = err #Write Error status if 0 no errors!
        ResultDic['Spot Frequency Noise @ ' +str(value)] = val
        return ResultDic
    
    
    
    def VCOMeasExample(self,NoieseOffset1,NoieseOffset2,measPoints,tunRangeMin,tunRangeMax,SupplyVoltage,delay):
        '''
        This is a small example how to make a Voltage controlled oscillator Noise measurment.
        '''
        
        #Config 
        self.set_SysMeasMode('VCO') #select VCO characterization
        self.set_VCOTestFreq('ON') #enable frequency parameter
        self.set_VCOTestISupply('ON') #enable supply current parameter
        self.set_VCOKPuShing('ON') #enable pushing parameter
        self.set_VCOKVCO('ON') #enable Kvco parameter
        self.set_VCOTestPNoise('ON') #enable spot noise parameter
        self.set_VCOTestPnoiseOFFSet(NoieseOffset1,NoieseOffset2) #set two spot noise offsets: 1.2kHz, 100kHz
        self.set_VCOTestPower('ON') #enable power parameter
        
        
        #measurment
        self.set_VCOTYPE('VCO') #set DUT Type (VCO or VCXO)
        self.set_VCOTestPoint(measPoints) #set 11 measurement points
        self.set_VCOTestStart(tunRangeMin) #set tuning range minimum to 0.5V
        self.set_VCOTestStop(tunRangeMax) #set tuning range maximum to 10V
        self.set_DUTPortVoltage(SupplyVoltage) #set supply voltage to 6V
        self.set_DUTPortStatus('ON') # enable supply voltage 
        self.Init()                # start measurement
        
        
        #loop
        self.set_VCOWait('ALL',delay) #wait for the measurement to finish
        err = self.ask_SystemError() #check if measurement was successful
        ResultDic = {}
        
        
        #read results
        ResultDic['control voltage'] = self.ask_VCOTraceVoltage() #request control voltage data array
        ResultDic['frequency data'] = self.ask_VCOTraceFreq() #request frequency data array
        ResultDic['Kvco data'] = self.ask_VCOKVCO() # request Kvco data array
        ResultDic['pushing data'] = self.ask_VCOKPuShing() #request pushing data array
        ResultDic['supply current data'] = self.ask_VCOTestISupply() #request supply current data array
        ResultDic['power level'] = self.ask_VCOTracePower() #request power level data array
        ResultDic['spot noise data array @offset #1 (1.2kHz)'] = self.ask_VCOTestPnoiseOFFSet(1) #request spot noise data array @offset #1 (1.2kHz)
        ResultDic['Error Value'] = err #Write Error status if 0 no errors!
        
        
        
        
        

        