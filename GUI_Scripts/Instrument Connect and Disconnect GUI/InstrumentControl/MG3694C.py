#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 07:00:19 2021

@author: Martin.Mihylov
"""

import numpy as np
import vxi11



print(
'''

#####################################################################################

Befor using the MG3694C you need to:
    1) Make sure Instrument and PC are connected vie ethernet  cable.
    2) Hold Windows + R keys and type ncpa.cpl
    3) Search for your Ethernet  Adapter and go to Properties
    4) Go to 'Internetprotocoll, Version 4(TCP/IPv4)'
    5) Chnage the IP-Address from 'automatic' to 'static' and give the IP:192.168.0.1
    6) DNS will be filled automatically! Press 'OK' and leave. 
    7) After your measurement dont forget to change the IP back to 'automatic'!
    
#####################################################################################

'''
 )

class MG3694C(vxi11.Instrument):
    '''
    A class thats uses vxi11 library to interface a Anritsu MG3694C.
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
# =============================================================================
# Abort Command
# =============================================================================
    def abort(self):
        '''
        Description: Forces the trigger system to the idle state. Any sweep in 
        progress is aborted as soon as possible
        
        Parameters: None
        '''
        return self.write(':ABORt')
    
# =============================================================================
# Ask Instrument about Stats and Parameters
# =============================================================================
    def ask_output_protection(self):
        '''
        
        Returns
        -------
        TYPE Query str
            Requests the currently programmed state of the MG369xC RF output during 
            frequency changes in CW or step sweep mode.

        '''
        return self.query(':OUTPut:PROTection?')
    
    
    
    
    
    def ask_output_retrace(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed state of the MG369xC RF output during 
            sweep retrace
            

        '''
        
        return self.query(':OUTPut:PROTection:RETRace?')
    
    
    
    
    
    def ask_output_impedance(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Description: Queries the MG369xC RF output impedance. The impedance is 
            nominally 50 ohms and is not settable.

        '''
        
        return self.query(':OUTPut:IMPedance?')
    
    
    
    
    
    def ask_OutputPowerLevel(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the value currently programmed for the RF output power level

        '''

        return float(self.query(':SOURce:POWer:LEVel:IMMediate:AMPLitude?'))
    
    
    
    
    
    def ask_MaximalPowerLevel(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the maximum RF output power level value that can be programmed for the
            particular MG369xC model

        '''
        
        return self.query(':SOURce:POWer? MAX')
# =============================================================================
# Ask Source Amplitude Modulation
# =============================================================================
    def ask_am_logsens(self):
        '''
        

        Returns
        -------
        TYPE Query
            Requests the currently programmed AM sensitivity value for the external AM Log mode.

        '''
       
        return self.query(':SOURce:AM:LOGSens?')
    
    
    
    
    
    def ask_am_logDepth(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed modulation depth value for the internal 
            AM Log mode.

        '''
        
        return self.query(':SOURce:AM:LOGDepth?')
    
    
    
    
    
    def ask_am_internalWave(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently selected modulating waveform for the internal AM function.

        '''
        
        return self.query(':SOURce:AM:INTernal:WAVE?')
    
    
    
    
    
    def ask_am_internalFreq(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed modulating waveform frequency value for the
            internal AM function.

        '''
        
        return self.query(':SOURce:AM:INTernal:FREQuency?')
    
    
    
    
    
    def ask_am_state(self):
        '''
        

        Returns
        -------
        TYPE Query str
           Requests currently programmed amplitude modulation state (on/off)

        '''
        
        return self.query(':SOURce:AM:STATe?')
    
    
    
    
    
    def ask_am_type(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed AM operating mode.

        '''
        
        return self.query(':SOURce:AM:TYPE?')
        
# =============================================================================
# Frequency Modulation
# =============================================================================
    def ask_fm_internalWave(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently selected modulating waveform for the internal FM function.

        '''
        
        return self.query(':SOURce:FM:INTernal:WAVE?')
    
    
    
    
    
    def ask_fm_internalFreq(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed modulating waveform frequency value for the
            internal FM function.

        '''
        return self.query(':SOURce:FM:INTernal:FREQuency?')
    
    
    
    
    
    def ask_fm_mode(self):
        '''
        

        Returns
        -------
        TYPE Query str
             Requests the currently programmed synthesis mode used to generate the FM signal.

        '''
        
        return self.query(':SOURce:FM:MODE?')
    
    
    
    
    
    def ask_fm_Bwidth(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed Unlocked FM synthesis mode of operation
            (narrow or wide)

        '''
        
        return self.query(':SOURce:FM:BWIDth?')
    
    
    
    
    
    def ask_fm_state(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed frequency modulation state (on/off).

        '''
        
        return self.query(':SOURce:FM:STATe?')

# =============================================================================
# Frequency Commands
# =============================================================================
    def ask_freq_CW(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the current value of the frequency parameter.

        '''
        
        return float(self.query(':SOURce:FREQuency:CW?'))
    
    
    
    
    
    def ask_freq_step(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the current step increment value of the frequency parameter.

        '''
        
        return self.query(':SOURce:FREQuency:CW:STEP:INCRement?')
    
    
    
    
    
    def ask_freq_centerFreq(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the current value of the RF output center frequency.

        '''
        
        return self.query(':SOURce:FREQuency:CENTer?')
    
    
    
    
    
    def ask_freq_mode(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently selected programming mode for frequency control.

        '''
      
        return self.query(':SOURce:FREQuency:MODE?')
    
    
    
    
    
    def ask_freq_span(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the current value for SWEep[1] sweep span

        '''
        
        return self.query(':SOURce:FREQuencySPAN:?')
    
    
    
    
    
    def ask_freq_start(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the current value for SWEep[1] start frequency.

        '''
       
        return self.query(':SOURce:FREQuency:STARt?')
    
    
    
    
    
    def ask_freq_stop(self):
        '''
        

        Returns
        -------
         Query str
            Requests the current value for SWEep[1] stop frequency.

        '''
        
        return self.query(':SOURce:FREQuency:STOP?')
    
    
    
    
    
    def ask_freq_unit(self):
        '''
        

        Returns
        -------
        Query str
            Requests the currently selected frequency unit.

        '''
        return self.query('UNIT:FREQuency?')
    
# =============================================================================
# Pulse Modulation
# =============================================================================
    def ask_pm_Bwidth(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed phase modulation operating mode.

        '''
        
        return self.query(':SOURce:PM:BWIDth?')

    
    
    
    
    def ask_pm_internalWave(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently selected modulating waveform for the internal phase modulation
            function.

        '''
        
        return self.query(':SOURce:PM:INTernal:WAVE?')
    
    
    
    
    
    def ask_pm_internalFreq(self):
        '''
        

        Returns
        -------
        TYPE Query str
             Requests the currently programmed modulating waveform frequency value for the
             internal phase modulation function.

        '''
        
        return self.query(':SOURce:PM:INTernal:FREQuency?')
    
    
    
    
    
    def ask_pm_state(self):
        '''
        

        Returns
        -------
        TYPE Query str
            Requests the currently programmed phase modulation state (on/off).

        '''
       
        return self.query(':SOURce:PM:STATe?')
    
    
    
    
    
# =============================================================================
# Set Output
# =============================================================================
    def set_output(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                Description: Turns MG369xC RF output power on/off.
                Parameters: ON | OFF | 1 | 0
                Default: OFF 
                
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
   
        if state in ['ON','OFF',1,0]:
            self.write(':OUTPut:STATe '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
      
    
    
    
    
    def set_output_protection(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
               Description: ON causes the MG369xC RF output to be turned off (blanked) 
               during frequency changes in CW or step sweep mode.
               OFF leaves RF output turned on (unblanked).
               Parameters: ON | OFF | 1 | 0
               Default: ON
               
        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':OUTPut:PROTection '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_output_retrace(self,state):
        '''
        

        Parameters
        ----------
        state :  str/int
                Description: ON causes the MG369xC RF output to be turned off during 
                sweep retrace. 
                OFF leaves RF output turned on
                Parameters: ON | OFF | 1 | 0
                Default: OFF

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':OUTPut:PROTection:RETRace '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
     
    
    
    
    
    def set_OutputPowerLevel(self,value):
        '''
        

        Parameters
        ----------
        value : float/int
                Description: Sets the power level of the unswept RF output signal.
                Parameters: Power level (in dBm) | UP | DOWN | MIN | MAX
                Range: MIN to MAX (see notes below)
                Default: 0 dBm
                
        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        
        unit  = 'dBm'
        minVal = -20.0
        maxVal = 30.0
        if value > maxVal or value < minVal:
            raise ValueError('Unknown input! See function description for more info.')
        else:
            self.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude ' + str(value) + ' ' + unit)
     
    
    
    
    
# =============================================================================
# Set Control system commands:
#            Amplitude Modulation
#            Correction Commands
#            Frequency Modulation
#            Frequency Commands
#            Pulse Modulation
#            
# =============================================================================
    # =============================================================================
    #   Source - AM
    # =============================================================================
    def set_am_logsens(self,value):
        '''
        

        Parameters
        ----------
        value : int/float
                Description: Sets the AM sensitivity for the external AM Log mode.
                Parameters: Sensitivity (in dB/V)
                Range: 0 to 25 dB/V
                Default: 3 dB/V

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if int(value) in np.arange(0,26,1):
            self.write(':SOURce:AM:LOGSens ' + str(value) + ' dB/V')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_am_logDepth(self,value):
        '''
        

        Parameters
        ----------
        value : int/float
                Description: Sets the modulation depth of the AM signal in the internal AM Log mode.
                Parameters: Modulation depth (in dB)
                Range: 0 to 25 dB
                Default: 3 dB

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
        
        if int(value) in np.arange(0,26,1):
            self.write(':SOURce:AM:LOGDepth ' + str(value) + ' dB')
        else:
            raise ValueError('Unknown input! See function description for more info.')
          
    
    
    
    
    def set_am_internalWave(self,state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Selects the modulating waveform (from the internal AM generator) for the internal AM
                function, as follows:
                SINE = Sine wave
                GAUSsian = Guassian noise
                RDOWn = Negative ramp
                RUP = Positive ramp
                SQUare = Square wave
                TRIangle = Triangle wave
                UNIForm = Uniform noiseParameters:
                Parameters: SINE | GAUSsian | RDOWn | RUP | SQUare | TRIangle | UNIForm
                Default: SINE

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''

        stList = ['SINE','GAUSsian','RDOWn','RUP','SQUare','TRIangle','UNIForm']
        if state in stList:
            self.write(':SOURce:AM:INTernal:WAVE ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
         
    
    
    
    
    def set_am_internalFreq(self,value,unit):
        '''
        

        Parameters
        ----------
        value : str
            Description: Sets the frequency of the modulating waveform for the internal AM function
            (see :AM:INTernal:WAVE).
            Parameters: Frequency
        unit : int/float
            Range: 0.1 Hz to 1 MHz for sine wave
            0.1 Hz to 100 kHz for square, triangle, and ramp waveforms
            Default: 1 kHz

         Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        state = self.ask_am_internalFreq()
        sinUnit = ['Hz','kHz','MHz']
        if state == 'SINE':
            if value >=0.1 or value <= 1 and unit in sinUnit:
                self.write(':SOURce:AM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
            
        else:
            if value >=0.1 or value<=100 and unit in sinUnit[:-1]:
                self.write(':SOURce:AM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
          
    
    
    
    
    def set_am_state(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                Description: Enable/disable amplitude modulation of MG369xC RF output signal.
                Parameters: ON | OFF | 1 | 0
                Default: OFF

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':SOURce:AM:STATe ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_am_type(self,state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Selects the AM operating mode.
                Parameters: LINear | LOGarithmic
                Default: LINear

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['LINear','LOGarithmic']:
            self.wrtie(':SOURce:AM:TYPE ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
# =============================================================================
#     Correction Commands
# =============================================================================
    def set_correctionCommands(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                Description: Turns the selected user level flatness correction power-offset table on/off.
                Parameters: ON | OFF | 1 | 0
                Default: OFF

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':SOURce:CORRection:STATe ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
# =============================================================================
# Frequency Modulation
# =============================================================================
    def set_fm_internalWave(self,state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Selects the modulating waveform (from the internal FM generator) for the internal
                FM function, as follows:
                SINE = Sine wave
                GAUSsian = Guassian noise
                RDOWn = Negative ramp
                RUP =Positive ramp
                SQUare = Square wave
                TRIangle = Triangle wave
                UNIForm = Uniform noise
                Parameters: SINE | GAUSsian | RDOWn | RUP | SQUare | TRIangle | UNIForm
                Default: SINE

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stList = ['SINE','GAUSsian','RDOWn','RUP','SQUare','TRIangle','UNIForm']
        if state in stList:
            self.write(':SOURce:FM:INTernal:WAVE '+ state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
         
    
    
    
    
    def set_fm_internalFreq(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Range: 0.1 Hz to 1 MHz for sine wave
        unit : str
            Parameters: Frequency
            Description: Sets the frequency of the modulating waveform for the internal FM function
            (see :FM:INTernal:WAVE).
            Default: 1 kHz

       Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        state = self.ask_fm_internalFreq()
        sinUnit = ['Hz','kHz','MHz']
        if state == 'SINE':
            if value >=0.1 or value <= 1 and unit in sinUnit:
                self.write(':SOURce:FM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
            
        else:
            if value >=0.1 or value<=100 and unit in sinUnit[:-1]:
                self.write(':SOURce:FM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
           
    
    
    
    
    def set_fm_mode(self,state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Sets the synthesis mode employed in generating the FM signal, as follows:
                LOCKed[1] = Locked Narrow FM
                LOCKed2 = Locked Narrow Low-Noise FM
                UNLocked = Unlocked FM
                If LOCKed[1] or LOCKed2 is set, the YIG phase-locked loop is used in synthesizing the
                FM signal. If UNLocked is set, the YIG phase-lock loop is disabled and the FM signal is
                obtained by applying the modulating signal to the tuning coils of the YIG-tuned
                oscillator.
                Parameters: LOCKed[1] | LOCKed2 | UNLocked
                Default: UNLocked

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        modList = ['LOCKed[1]','LOCKed2','UNLocked']
        if state in modList:
            self.write(':SOURce:FM:MODE ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_fm_Bwidth(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Description: Sets the Unlocked FM synthesis mode to wide or narrow mode of operation.
            The Unlocked Wide FM synthesis mode allows maximum deviations of ±100 MHz for
            DC to 100 Hz rates.
            The Unlocked Narrow FM synthesis mode allows maximum deviations of ±10 MHz for
            DC to 8 MHz rates.
            Parameters: MIN | MAX
            Range: MIN = narrow mode; MAX = wide mode
            Default: MIN

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['MIN','MAX']:
            self.write(':SOURce:FM:BWIDth ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
         
    
    
    
    
    def set_fm_steta(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
                Description: Enable/disable frequency modulation of MG369xC RF output signal.
                Parameters: ON | OFF | 1 | 0
                Default: OFF

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':SOURce:FM:STATe ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
           
    
    
    
    
# =============================================================================
# Frequency Commands 
# =============================================================================
    def set_freq_CW(self,value ,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Description: Sets the RF output frequency of the MG369xC to the value entered.
            Parameters UP | DOWN increment/decrement the frequency by the value set by
            [:SOURce]:FREQuency:STEP:INCRement command.
            Parameters: Frequency (in Hz) | UP | DOWN | MIN | MAX
            Range: MIN to MAX (see note below)
            Default: (MIN + MAX) / 2
            
            Model   Minimum Frequency*      Maximum Frequency
            MG3691C 10 MHz                  10 GHz
            MG3692C 10 MHz                  20 GHz
            MG3693C 10 MHz                  31.8 GHz
            MG3694C 10 MHz                  40 GHz
            MG3695C 10 MHz                  50 GHz
            MG3697C 10 MHz                  70 GHz
        unit : str
            Parameter Frequency.

        Returns
        -------
        None.

        '''
        
        
        minFreq = 10
        maxFreq = 40 
        stUnit = ['MHz','GHz']

        if unit == 'MHz':
            if value <= 40*1e9 and value >= 10:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Warning !! Minimum Frequency = 10 MHz and Maximum Frequency = 40*1e9 MHz')
        elif unit == 'GHz':
            if value <= 40 and value >= 0.01:
                self.write(':SOURce:FREQuency:CW ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Warning !! Minimum Frequency = 0.01 GHz and Maximum Frequency = 40 GHz')
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def set_freq_step(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
                 Description: Sets the step increment size used with the :FREQuency:CW command.
                 Range: 0.01 Hz to (MAX  MIN) 
                 Default: 0.1 GHz
        unit : str
                Parameters: Frequency (in Hz)

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['Hz','kHz','MHz','GHz']
        if unit in stUnit and value>0.01:
            self.write(':SOURce:FREQuency:CW:STEP:INCRement ' + str(value) + ' ' + unit)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_freq_cent(self,value,unit):
        '''
        

        Parameters
        ----------
        value :  int/float
                   Description: Sets the MG369xC RF output center frequency to the value entered. :CENTER and :SPAN
                   frequencies are coupled values. Entering the value for one will cause the other to be
                   recalculated. (See notes under :FREQuency:SPAN)
        unit : str
            Parameters: Frequency (in Hz)

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['Hz','kHz','MHz','GHz']
        if unit in stUnit and value>0.01:
            self.write(':SOURce:FREQuency:CENTer ' + str(value) + ' ' + unit)
        else:
            raise ValueError('Unknown input! See function description for more info.')
      
    
    
    
     
    def set_freq_mode(self,state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Specifies which command subsystem controls the MG369xC frequency, as follows:
                CW|FIXed = [:SOURce]:FREQuency:CW|FIXed
                SWEep[1] = [:SOURce]:SWEep[1] (see Datasheet)
                SWCW = (see notes)
                ALSW = (see notes)
                LIST<n> = [:SOURce]:LIST<n> (see DataSheet)
                :SWEep and :SWEep1may be used interchangeably
                
                Parameters: CW | FIXed | SWEep[1] | SWCW | ALSW | LIST[1] | LIST2 | LIST3 | LIST4
                Default: CW

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stState = ['CW','FIXed','SWEep[1]','SWCW','ALSW','LIST[1]','LIST2','LIST3','LIST4']
        if state in stState:
            self.write(':SOURce:FREQuency:MODE '+ str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    
    def set_freq_span(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Description: Sets sweep span for SWEep[1] to value entered. :SPAN and :CENTer are coupled values
            Range: 1 kHz to (MAX  MIN)
            Default: MAX  MIN
        unit : str
            Parameters: Frequency (in Hz)

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        '''
        Description: Sets sweep span for SWEep[1] to value entered. :SPAN and :CENTer are coupled values
        Parameters: Frequency (in Hz)
        Range: 1 kHz to (MAX  MIN)
        Default: MAX  MIN
        '''
        
        stUnit = ['Hz','kHz','MHz','GHz']
        if unit in stUnit:
            self.write(':SOURce:FREQuency:SPAN ' + str(value) + ' ' + str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
         
    
    
    
    
    def set_freq_start(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
            Description: Sets start frequency for SWEep[1] to the value entered. (MIN is defined in the notes
             Range: MIN to MAX
             Default: MIN
        unit : str
            Parameters: Frequency (in Hz) | MIN

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        stUnit = ['Hz','kHz','MHz','GHz']
        if unit in stUnit:
            self.write(':SOURce:FREQuency:STARt ' + str(value) + ' ' + str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
          
    
    
    
    
    def set_freq_stop(self,value,unit):
        '''
        

        Parameters
        ----------
        value : int/float
                Description: Sets stop frequency for SWEep[1] to the value entered. (MAX is defined in the notes
                under [:SOURce]:FREQuency:CW|FIXed).
                Range: MIN to MAX 
                Default: MAX
        unit : str
            Parameters: Frequency (in Hz) | MAX

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        None.

        '''
        
        stUnit = ['Hz','kHz','MHz','GHz']
        if unit in stUnit:
            self.write(':SOURce:FREQuency:STOP ' + str(value) + ' ' + str(unit))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
# =============================================================================
# Pulse Modulation
# =============================================================================
    def set_pm_Bwidth(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Description: Selects the phase modulation (ΦM) operating mode.
            The Narrow ΦM mode allows maximum deviations of ±3 radians for DC to 8 MHz rates.
            The Wide ΦM mode allows maximum deviations of ±400 radians for DC to 1 MHz rates.
            Parameters: MIN | MAX
            Range: MIN = narrow mode
            MAX = wide mode
            Default: MIN

        Raises
        ------
        ValueError
            Error message


        Returns
        -------
        None.

        '''
        
        stList = ['MIN','MAX']
        if state in stList:
            self.write(':SOURce:PM:BWIDth ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
           
    
    
    
    
    def set_pm_internalWave(self, state):
        '''
        

        Parameters
        ----------
        state : str
                Description: Selects the modulating waveform (from the internal ΦM generator) for the internal phase
                modulation function, as follows:
                SINE = Sine wave
                GAUSsian = Gaussian noise
                RDOWn = Negative ramp
                RUP = Positive ramp
                SQUare = Square wave
                TRIangle = Triangle wave
                UNIForm = Uniform noise
                Parameters: SINE | GAUSsian | RDOWn | RUP | SQUare | TRIangle | UNIForm
                Default: SINE

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
        
        stList = ['SINE','GAUSsian','RDOWn','RUP','SQUare','TRIangle','UNIForm']
        if state in stList:
            self.write(':SOURce:PM:INTernal:WAVE '+ state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
           
    
    
    
    
    def set_pm_internalFreq(self,value, unit):
        '''
        

        Parameters
        ----------
        value : str
            Parameter: Frequency (in Hz)
        unit : int/float
            Description: Sets the frequency of the modulating waveform for the internal phase modulation
            (see :PM:INTernal:WAVE)
            Range: 0.1 Hz to 1 MHz for sine wave;
            0.1 Hz to 100 kHz for square, triangle, and ramp waveforms.
            Default: 1 kHz

        Raises
        ------
        ValueError
             Error message

        Returns
        -------
        None.

        '''
       
        state = self.ask_pm_internalFreq()
        sinUnit = ['Hz','kHz','MHz']
        if state == 'SINE':
            if value >=0.1 or value <= 1 and unit in sinUnit:
                self.write(':SOURce:PM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
            
        else:
            if value >=0.1 or value<=100 and unit in sinUnit[:-1]:
                self.write(':SOURce:PM:INTernal:FREQuency ' + str(value) + ' ' + unit)
            else:
                raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def set_pm_state(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
            Description: Enable/disable phase modulation of the MG369xC RF output signal.
            Parameters: ON | OFF | 1 | 0
            Default: OFF

        Raises
        ------
        ValueError
            v

        Returns
        -------
        None.

        '''
        
        if state in ['ON','OFF',1,0]:
            self.write(':SOURce:PM:STATe ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    def DisplayParamDict(self,Type):
        '''
        This function will print all the adjusted parameters.
        '''
        Headers = ['Params','Vaue/Type/Info']
        Params = ['Adapter Type','Max Frequency range','Min Frequency range','Waveelength']
        Data = [self.ask_AdapterType(),self.ask_freqRange('MAX'),self.ask_freqRange('MIN'),self.ask_Wavelength()]
    
        meas = Type
        measList = ['Power','Energy','Current','Voltage']
        if meas in measList:
            if meas == 'Power': 
                Params.append('Power Unit set')
                Data.append(self.ask_PowerUnits())
                Params.append('Power range auto')
                Data.append(self.ask_AutoPowerRange())
                Params.append('Power Range set')
                Data.append(self.ask_PowerRange()) 
             
            elif meas == 'Energy':
                Params.append('Energy range auto')
                Data.append(self.ask_energyRange())
                
            elif meas == 'Voltage':
                Params.append('Voltage range auto')
                Data.append(self.ask_AutoVoltageRange())
                Params.append('Voltage range')
                Data.append(self.ask_voltRange())
            elif meas == 'Current':
                Params.append('Current range auto')
                Data.append(self.ask_AutoCurrentRange())
                Params.append('Current range')
                Data.append(self.ask_currentRange())
            
        else:
            print('Invalid Value! Function will be terminated.')
            
        return Headers,Data,Params
        
    
# =============================================================================
# Get/Save Data
# =============================================================================
    def get_Data(self):
        '''
        

        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured Power and CW Frequency.

        '''
        OutPut = {}
        Freq = self.ask_freq_CW()
        Power = self.ask_OutputPowerLevel()
        OutPut['Power/dBm'] = Power
        OutPut['CW Frequency/'+self.ask_freq_unit()] = Freq
        return OutPut