# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:40:31 2021

@author: Martin.Mihaylov
"""


import numpy as np
import pyvisa as visa



    
class MS4647B:
    def __init__(self, resource_str):
        '''
        Connect to Device and print the Identification Number.
        '''
        self._resource = visa.ResourceManager('@py').open_resource(resource_str)
        print(self._resource.query('*IDN?'))


    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        print('Instrument Anritsu MS4647B is closed!')
        return self._resource.close()
    


# =============================================================================
# Get the instrument Serial Number and Model 
# =============================================================================
    def getIdn(self):
        '''

        Returns
        -------
        TYPE str
                Device Serial Number and Model

        '''

        return self.query("*IDN?").split('\n')[0]

# =============================================================================
# Return to local 
# =============================================================================
        
    def RTL(self):
        '''
        

        Returns
        -------
        None.
        Description: Send all devices to local operation. No query

        '''
        self.write('RTL')
# =============================================================================
# Ask 
# =============================================================================

    def ask_SubSystem(self):
        '''
        

        Returns
        -------
        TYPE str
                The :SENSe:HOLD subsystem command sets the hold function for all 
                channels on a per-instrument basis

        '''
        
        return self.query(':SENSe:HOLD:FUNCtion?').split('\n')[0]
    
    
    
    
    
    def ask_SweepCount(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE
           Description: Query only. Outputs the averaging sweep count for the 
            indicated channel.

        '''
        
        if type(ChanNumber) == int: 
            return float(self.query(':SENS'+str(ChanNumber)+':AVER:SWE?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_TestSet(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Raises
        ------
        ValueError
           Error message

        Returns
        -------
        TYPE
            Query State of TS3739.

        '''
        
        if type(ChanNumber) == int: 
            return self.query(':SENS'+str(ChanNumber)+':TS3739:STATe?').split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def ask_SysErrors(self):
        '''
        

        Returns
        -------
        TYPE
            Description: Query only. Outputs the number of errors in the error queue.
        
        '''
       
        return self.query(':SYST:ERR:COUN?').split('\n')[0]
    
    
    
    
    
    def ask_StatOperation(self):
        '''
        

        Returns
        -------
        TYPE
                Description: Query only. Outputs the value of the operation status 
                condition reg.
                Range: 0 to 32767
                Default Value: 0

        '''
        
        return self.query(':STAT:OPER:COND?').split('\n')[0]
    
    
    
    
    
    def ask_StatOperationRegister(self):
        '''
        

        Returns
        -------
        TYPE    str
                Sets the value of the operation status enable register. 
                Outputs the value of the operation status enable register.

        '''
       
        return self.query(':STATus:OPERation:ENABle?').split('\n')[0]
    
    
    
    
    
    def ask_FreqSpan(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE  : float
                Optional query. Span is automatically calculated as Stop Frequency minus
                Start Frequency. The query returns the resulting span in Hertz.

        '''
        
        if type(ChanNumber) == int: 
            return float(self.query(':SENSe'+str(ChanNumber)+':FREQuency:SPAN?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def ask_CenterFreq(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : float
                Optional query. Center frequency is automatically calculated using Stop Frequency and Start
                Frequency as:
            
                    Fc = ((Fstop - Fstart)/2) + Fstart

        '''
        
        if type(ChanNumber) == int: 
            return float(self.query(':SENSe'+str(ChanNumber)+':FREQuency:CENTer?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def ask_CWFreq(self,ChanNumber):
        '''
        

         Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : float
                Sets the CW frequency of the indicated channel. Outputs the CW 
                frequency of the indicated channel.

                The output parameter is in Hertz.

        '''
        
        if type(ChanNumber) == int: 
            return float(self.query(':SENS'+str(ChanNumber)+':FREQ:CW?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def ask_DataFreq(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
           Error message

        Returns
        -------
        TYPE : str
            Outputs the frequency list for the indicated channel

        '''
        
        if type(ChanNumber) == int: 
            return self.query(':SENSe'+str(ChanNumber)+':FREQuency:DATA?').split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def ask_SweepChannelStatus(self):
        '''
        

        Returns
        -------
        TYPE : str
            The query outputs the On/Off state of the option to sweep only the active 
            channel

        '''
        
        return self.query(':DISP:ACT:CHAN:SWE:STAT?').split('\n')[0]
  
    
    
    
    
    def ask_AssignetDataPort(self,value):
        '''
        

        Parameters
        ----------
        value : int/float
            the N(ports number) for the .sNp data output.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : str
            Outputs the data port pair assigned to use when creating an sNp data 
            file on the indicated channel.

        '''
        
       
        value = str(value)
        if value in ['1','2','3','4']:
            return self.query('FORMat:S'+str(value)+'P:PORT?').split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
    
    
    
    
    def ask_ParamFormInFile(self):
        '''
        Outputs the parameter format displayed in an SNP data file.
        '''
        return self.query(':FORMat:SNP:PARameter?').split('\n')[0]
        
    
    
    
    
    def ask_RFState(self):
        '''
        

        Returns
        -------
        TYPE : str
            Outputs the RF on/off state in Hold

        '''
        
        return self.query(':SYST:HOLD:RF?').split('\n')[0]
    
    
    
    
    
    def ask_SetAverageState(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : str
            Outputs the averaging function on/off status on the indicated channel.

        '''
        
        if type(ChanNumber) == int: 
            return self.query(':SENS'+str(ChanNumber)+':AVER?').split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.')
          
    
    
    
    
    def ask_AverageFunctionType(self,ChanNumber):
        '''
        

         Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : str
            Outputs the averaging function type of point-by-point or sweep-by-sweep.

        '''
        
        if type(ChanNumber) == int: 
            return self.query(':SENS'+str(ChanNumber)+':AVER:TYP?').split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_AverageCount(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        TYPE : float
            Outputs the averaging count for the indicated channel.

        '''
        
        if type(ChanNumber) == int:
            return float(self.query(':SENS'+str(ChanNumber)+':AVER:COUN?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_TransferData(self,name,portNumb):
        '''
        

        Parameters
        ----------
        name : str
            File Name
        portNumb : int
            the N(ports number) for the .sNp data output.

        Returns
        -------
        TYPE : str
            The query outputs the disk file data to the
            GPIB. The file must exist
            
            
            
            Hard coded path on the VNA = 'C:/tmp/'

        '''
        
        path = 'C:/tmp/'
        path = str(path) + str(name)+'_.s' + str(portNumb) + 'p'
        return self.query(':MMEM:TRAN? '+'"' + path + '"')
    
    
    
    
    
    def ask_TransferDataCSV(self,name):
        '''
        

        Parameters
        ----------
        name : str
            File Name
        portNumb : int
            the N(ports number) for the .sNp data output.

        Returns
        -------
        TYPE : str
            The query outputs the disk file data to the
            GPIB. The file must exist
            
            
            
            Hard coded path on the VNA = 'C:/tmp/'

        '''
        
        path = 'C:/tmp/'
        path = str(path) + str(name)+'_.csv'
        return self.query(':MMEM:TRAN? '+'"' + path + '"')

    
    
    
    
    def ask_ResolutionBW(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...

        Returns
        -------
        TYPE : float
           The command sets the IF bandwidth for the indicated channel. The query outputs the IF
           bandwidth for the indicated channel.

        '''

        return float(self.query(':SENS'+str(ChanNumber)+':BAND?').split('\n')[0])
        
    
    
    
    
    def ask_PowerOnPort(self,segment,ChanNumber):
        '''
        

        Parameters
        ----------
        segment : int 
            Selected Source. Can be from 1-16
        ChanNumber : int
            Channel Number 1,2,3...

        Returns
        -------
        Value: flaot
             Outputs the power level of the indicated port on the indicated channel.

        '''
        
        
        stSegment = np.arange(1,17,1)
        stChanNumber = np.arange(1,5,1)
        if segment in stSegment and ChanNumber in stChanNumber:
            return float(self.query(':SOUR'+str(segment)+':POW:PORT'+str(ChanNumber)+'?').split('\n')[0])
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
            
            
            
            
    def ask_SmoothingState(self, ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Returns
        -------
        TYPE
            Query outputs the smoothing on/off status for the indicated channel and active trace.
            1 = ON
            2 = OFF

        '''
        return float(self.query(':CALC'+str(ChanNumber)+':SMO?').split('\n')[0])
    




    def ask_DisplayTrace(self):
        '''
        

        Returns
        -------
        TYPE
            Query only. Outputs the Active Channel number.

        '''
        return self.query(':DISPlay:WINDow:ACTivate?')
    
    
    
    
    
    def ask_DisplayCount(self):
        '''
        

        Returns
        -------
        TYPE
            Quuery the number of displayed channels.

        '''
        return float(self.query(':DISP:COUN?').split('\n')[0])
    
    
    
    
    
    def ask_DisplayTitle(self):
        '''
        

        Returns
        -------
        TYPE
            Outputs the user title for the channel
            indicated

        '''
        return self.query(':DISP:WIND1:TITL?')
    
    
    
    
    
    def ask_SelectParameter(self):
        '''
        

        Returns
        -------
           The query outputs only the selected parameter.

        '''
        
        return self.query(':CALC1:PAR1:DEF?').split('\n')[0]
    
    
    
    
    
    def ask_SweepDelay(self):
        '''
        

        Returns
        -------
            Outputs the sweep delay time of the indicated channel.

        '''
        
        return self.query(':SENS1:SWE:DEL?')
    
    
    
    
    
    
    
    def ask_SweepTime(self):
        '''
        

        Returns
        -------
            Outputs the Sweep Time of the indicated  channel.

        '''
        return float(self.query(':SENS1:SWE:TIM?'))
    
    
    
    
# =============================================================================
# Set
# =============================================================================

    def set_ClearAverage(self,ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
                     Description: Clears and restarts the averaging sweep count of the 
                     indicated channel.
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            self.write(':SENS'+str(ChanNumber)+':AVER:CLE')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_SubSystemHold(self):
        '''
        

        Returns
        -------
        None.
        Sets the hold function for all channels on a per-instrument basis.
        The sweep is stopped.

        '''
        
        self.write(':SENS:HOLD:FUNC HOLD')
        
    
    
    
    
    def set_SubSystemSing(self):
        '''
        

        Returns
        -------
        None.
        The sweep restarts and sweeps until the end of the
        sweep, at which point it sets the end of sweep status bit and
        stops.

        '''
        
        self.write(':SENS:HOLD:FUNC SING')
     
    
    
    
    
    def set_SubSystemCont(self):
        '''
        

        Returns
        -------
        None.
        The sweep is sweeping continuously

        '''
        
        self.write(':SENS:HOLD:FUNC CONT')    
        
    
    
    
    
    def set_DisplayScale(self):
        '''
        

        Returns
        -------
        None.
        Description: Auto scales all traces on all channels. 
        '''
        
        self.write(':DISPlay:Y:AUTO')
        
    
    
    
    
    def set_TS3739(self,ChanNumber,state):
        '''
        

       Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        state : str/int
                The :SENSe{1-16}:TS3739 subsystem commands are used to configure and 
                control the VectorStar ME7838x  Broadband/Millimeter-Wave 3738A Test Set.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            if state in ['ON','OFF',1,0]:
                self.write(':SENS'+str(ChanNumber)+':TS3739 '+ str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.') 
        else:
            raise ValueError('Unknown input! See function description for more info.') 
            
    
    
    
    
    def set_ClearError(self):
        '''
        

        Returns
        -------
        None.
        Description: Clears the contents of the error queue.

        '''
        
        self.write(':SYST:ERR:CLE')
        
    
    
    
    
    def set_DisplayColorReset(self):
        '''
        

        Returns
        -------
        None.
        Resets all colors and inverted colors to their normal default values.

        '''
        
        self.write(':DISP:COL:RES')
        
    
    
    
    
    def set_StatOperationRegister(self,value):
        '''
        

        Parameters
        ----------
        value : TYPE
            Sets the value of the operation status enable register. 
            Outputs the value of the operation status enable register.
            The input parameter is a unitless number.
            
            Range: 0 to 65535

        Returns
        -------
        None.

        '''
        
        value = int(value)
        self.write(':STAT:OPER:ENAB '+str(value))
        
    
    
    
    
    def set_StartFreq(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
                Sets the start value of the sweep range of the indicated channel. 
                The input parameter is in Hertz, Meters, or Seconds.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
       
        if type(ChanNumber) == int:
            self.write(':SENSe'+str(ChanNumber)+':FREQuency:STARt '+str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
    
    def set_StopFreq(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
                Sets the stop value of the sweep range of the indicated channel. 
                The input parameter is in Hertz, Meters, or Seconds.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            self.write(':SENSe'+str(ChanNumber)+':FREQuency:STOP '+str(value))
        else:
                raise ValueError('Unknown input! See function description for more info.') 
    
    
    
    
    
    def set_CenterFreq(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
                Sets the center value of the sweep range of the indicated channel. 
                Outputs the center value of the sweep range of the indicated channel

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            self.write(':SENS'+str(ChanNumber)+':FREQ:CENT '+str(value))
        else:
                raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_CWFreq(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int/str in form - 10E+9
               Sets the CW frequency of the indicated channel. Outputs the CW 
               frequency of the indicated channel.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            self.write(':SENS'+str(ChanNumber)+':FREQ:CW '+str(value))
        else:
                raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_SweepChannelStatus(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                The command turns On/Off the option to sweep only the active channel

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':DISP:ACT:CHAN:SWE:STAT  '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_AssignetDataPort(self,ChanNumber,value1,value2):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value1 : int
            
        value2 : int
            
            The command assigns the data port pair to use when creating an sNp 
            data file on the indicated channel. The use of Port 3 and/or Port 4 
            requires a 4-port VNA instrument
        
            PORT12 | PORT13 | PORT14 | PORT23 | PORT24 | PORT34
        
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        value1 = str(value1)
        value2 = str(value2)
        if type(ChanNumber) == int:
            if value1 in ['1','2','3','4']:
                self.write(':CALC'+str(ChanNumber)+':FORM:S'+str(value1)+'P:PORT PORT'+str(value1)+str(value2))
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
                raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_ParamFormInFile(self,unit):
        '''
        

        Parameters
        ----------
        unit : str
            Sets the parameter format displayed in an SNP data file. 
            Where:
                 • LINPH = Linear and Phase
                 • LOGPH = Log and Phase
                 • REIM = Real and Imaginary Numbers

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if unit in ['LINPH','LOGPH','REIM']:
            self.write(':FORM:SNP:PAR '+str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_RFState(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                Sets the RF on/off state in Hold.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':SYST:HOLD:RF '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
          
    
    
    
    
    def set_SetAverageState(self,ChanNumber,state):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        state : int/str
             Turns averaging on/off for the indicated channel (Turns on and Off the averaging for all channels).

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            if state in ['ON','OFF',1,0]:
                self.write(':SENS'+str(ChanNumber)+':AVER '+ str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            raise ValueError('Unknown input! See function description for more info.') 
           
    
    
    
    
    def set_AverageFunctionType(self,ChanNumber,state):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        state : str
            Sets the averaging function type to point-by-point or sweep-by-sweep.
            POIN | SWE
            Default Value: POIN

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if type(ChanNumber) == int:
            if state in ['SWE','POIN']:
                self.write(':SENS'+str(ChanNumber)+':AVER:TYP '+ str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
           raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
    
    def set_AverageCount(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int
            Sets the averaging count for the indicated channel. The channel must 
            be turned on.
            The input parameter is a unitless number.
            Range: 1 to 1024
            Default Value: 1

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        value = str(value)
        if type(ChanNumber) == int:
            self.write(':SENS'+str(ChanNumber)+':AVER:COUN '+str(value))
        else:
           raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
    
    def set_ResolutionBW(self,ChanNumber,value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
                     Channel Number 1,2,3...
        value : int/floa/str
           The command sets the IF bandwidth for the indicated channel. The query outputs the IF
           bandwidth for the indicated channel.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        
        value = str(value) 
        if type(ChanNumber) == int:
            self.write(':SENS'+str(ChanNumber)+':BAND '+str(value))        
        else:
           raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
    
    def set_PowerOnPort(self,segment,ChanNumber,value):
        '''
        

        Parameters
        ----------
        segment : int 
            Selected Source. Can be from 1-16
        ChanNumber : int
            Channel Number 1,2,3...
        value : int/floa/str
            Sets the power level of the indicated port on the indicated channel.

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
   
        stSegment = np.arange(1,17,1)
        stChanNumber = np.arange(1,5,1)
        if segment in stSegment and ChanNumber in stChanNumber:
            self.write(':SOUR'+str(segment)+':POW:PORT'+str(ChanNumber)+' '+str(value))
        else:
            raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
    
    def set_SmoothingState(self, ChanNumber, state):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...
        state : str/int
            can be int or str form the list ['ON','OFF',1,0]

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        The command sets the smoothing aperture for the indicated channel and active trace.

        '''
        if type(ChanNumber) == int:
            if state in ['ON','OFF',1,0]:
                self.write(':CALC'+str(ChanNumber)+':SMO '+ str(state))
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            raise ValueError('Unknown input! See function description for more info.') 
        
    
    
    
     
    def set_SmoothingAPERture(self, ChanNumber, value):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...
        value : int
            Procentge smoothing between 0 to 100
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        The command sets the smoothing aperture for the indicated channel and active trace.

        '''
        if type(ChanNumber) == int:
           
            self.write(':CALC'+str(ChanNumber)+'SMO:APER '+ str(float(value)))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_DisplayTrace(self, ChanNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        The command sets the active channel to the indicated number. When the VNA is set to
        100,000 point mode, the number of channels is

        '''
        if type(ChanNumber) == int:
           
            self.write(':DISP:WIND'+str(ChanNumber)+ ':ACT')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_DisplayCount(self,ChannelNumber):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns 
        -------
        None: Sets the number of displayed channels. When the VNA is in 25,000 point mode, the
        number of channels can only be 1 (one), 2, 3, 4, 6, 8, 9, 10, 12, or 16 channels. If the
        channel display is set to a non-listed number (5, 7, 11, 13, 14, 15), the instrument is set to
        the next higher channel number. If a number of greater than 16 is entered, the
        instrument is set to 16 channels. If the instrument is set to 100,000 points, any input
        results in 1 (one) channel. Outputs the number of displayed channels.

        '''
        if type(ChannelNumber) == int:
           
            self.write(':DISP:COUN ' + str(ChannelNumber))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_DisplayTitle(self, ChannelName):
        '''
        

        Parameters
        ----------
        ChanNumber : int
            Channel Number 1,2,3...

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None: Sets the user title for the channel indicated.

        '''

        if type(ChannelName) == str:
            self.write(':DISP:WIND1:TITL ' + ChannelName)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
    def set_SelectParameter(self, S_Param):
        '''
        

        Parameters
        ----------
        S_Param : str
            S-Parameter selected. 

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None: Select an S-Parameter. 16 S-Parameters for 4 Ports config can be selected.

        '''
        S_Paramls = ['S11','S12','S13','S14','S21','S22','S23','S24','S31','S32','S33','S34','S41','S42','S43','S44']
        if type(S_Param) == str:
            if S_Param in S_Paramls:
                self.write(':CALC1:PAR1:DEF ' + S_Param)
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    
    def set_SweepDelay(self, time):
        '''
    
        Parameters
        ----------
        time : float
            Sets the sweep delay time of the indicated channel.

        Returns
        -------
        None.

        '''
        self.write(':SENS1:SWE:DEL ' + str(time))
    
    
    
    
    
    
    def set_SweepTime(self, time):
        '''
        

        Parameters
        ----------
        time : float
            Sets the Sweep Time of the indicated channel. 

        Returns
        -------
        None.

        '''
        
        self.write(':SENS1:SWE:TIM ' + str(time))
    
    
# =============================================================================
# Save 
# =============================================================================
        
    def SaveData(self,name,portNumb):
        '''
        

        Parameters
        ----------
        name : str
            File Name
        portNumb : TYPE
                The N(ports number) for the .sNp data output.
                Description: Stores a data file of the type specified by the filename
                extension.No query.
                
                
                Hard coded path on the VNA = 'C:/tmp/'

        Returns
        -------
        None.

        '''
        
        path = 'C:/tmp/'
        path = str(path) +str(name) +'_.s' + str(portNumb) + 'p'
        self.write(':MMEM:STOR '+'"' + path + '"')
        
    
    
    
    
    def SaveDataCSV(self,name):
        '''
        

        Parameters
        ----------
        name : str
            File Name
        portNumb : TYPE
                The N(ports number) for the .sNp data output.
                Description: Stores a data file of the type specified by the filename
                extension.No query.
                
                
                Hard coded path on the VNA = 'C:/tmp/'

        Returns
        -------
        None.

        '''
        
        path = 'C:/tmp/'
        path = str(path) +str(name) +'_.csv'
        self.write(':MMEM:STOR '+'"' + path + '"')
        
    
    
    
    
    def SaveImage(self,name):
        '''
        

        Parameters
        ----------
        name : str
            File Name
        portNumb : TYPE
                The N(ports number) for the .sNp data output.
                Description: Stores a data file of the type specified by the filename
                extension.No query.
                
                
                Hard coded path on the VNA = 'C:/tmp/'

        Returns
        -------
        None.

        '''
        
        path = 'C:/tmp/Image/'
        path = str(path) +str(name) +'_.png'
        self.write(':MMEMory:STORe:IMAGe '+'"' + path + '"')
       
    
    
    
    
    def DeleteData(self,name,portNumb):
        '''
                

        Parameters
        ----------
        name : str
            File Name
        portNumb : TYPE
                The N(ports number) for the .sNp data output.
                Delete a disk, file, or directory. Use caution with this command as there is no recovery
                operation in case of a user mistake or error. No query
                
                
                Hard coded path on the VNA = 'C:/tmp/'

        Returns
        -------
        None.

        '''
        path = 'C:/tmp/'
        path = str(path) +str(name) +'_.s' + str(portNumb) + 'p'
        self.write(':MMEMory:DEL ' + '"' + path + '"')
       
    
    
    
    
    def DeleteDataCSV(self,name):
        '''
                

        Parameters
        ----------
        name : str
            File Name
        portNumb : TYPE
                The N(ports number) for the .sNp data output.
                Delete a disk, file, or directory. Use caution with this command as there is no recovery
                operation in case of a user mistake or error. No query
                
                
                Hard coded path on the VNA = 'C:/tmp/'

        Returns
        -------
        None.

        '''
        path = 'C:/tmp/'
        path = str(path) +str(name) +'_.csv'
        self.write(':MMEMory:DEL ' + '"' + path + '"')
    
    
    
    
    
    def SaveTransferData(self,file,path,name,portNumb):
        '''
        

        Parameters
        ----------
        file : str
                File data extracted from function ask_TransferData
        path : str
            Where on the PC to save the data
        name : str
            Name of the File
        portNumb : int/str
            The N(ports number) for the .sNp data output.
            
            Write a text File whit the transfered Data

        Returns
        -------
        None.

        '''
    
        readinglines = file.splitlines()
        with open(str(path) + '/'+str(name)+'.s'+str(portNumb)+'p', 'w') as f:
            for line in readinglines:
                f.write(line)
                f.write('\n')
                
    
    
    
    
    def SaveTransferDataCSV(self,file,path,name):
        '''
        

        Parameters
        ----------
        file : str
                File data extracted from function ask_TransferData
        path : str
            Where on the PC to save the data
        name : str
            Name of the File
        portNumb : int/str
            The N(ports number) for the .sNp data output.
            
            Write a text File whit the transfered Data

        Returns
        -------
        None.

        '''
    
        readinglines = file.splitlines()
        with open(str(path) + '/'+str(name)+'.csv', 'w') as f:
            for line in readinglines:
                f.write(line)
                f.write('\n')

    
    
    
    