# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 08:27:01 2021

@author: MartinMihaylov
"""



import time
import numpy as np
import pyvisa as visa


Serien_Nummer = ['P0024970','P0033858']



    
class PM100D:
    def __init__(self, resource_str):

        self._resource = visa.ResourceManager().open_resource('USB0::0x1313::0x8078::' + str(resource_str) + '::INSTR')
        print(self._resource.query('*IDN?'))

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        self._resource.close()
        print('Instrument PM100D is closed!')
    
       
    
    
    
    
    
# =============================================================================
#     Self Test
# =============================================================================
    
    def self_test(self):
        '''
        

        Returns
        -------
        TYPE
             Use this query command to perform the instrument self-test routine. The command
             places the coded result in the Output Queue. A returned value of zero (0) indicates
             that the test passed, other values indicate that the test failed.

        '''
        print('A returned value of zero (0) indicates that the test passed, other \
              values indicate that the test failed.')
              
        return self.query('*TST?')

# =============================================================================
# Configuration 
# =============================================================================
    def ReadConfig(self):
        '''
        

        Returns
        -------
        None
            Query the current measurement configuration

        '''
        
        return self.query('CONFigure?')

    
# =============================================================================
# Fetch last meassure Data 
# =============================================================================

    def fetchData(self):
        '''
        

        Returns
        -------
        TYPE float
            Read last measurement data. WILL NOT START THE MEASURMENT
        '''
        return float(self.query(':FETCh?').split('\n')[0])
    
    
# =============================================================================
# OPC Register
# =============================================================================

    def OPC(self):
        '''
        

        Returns
        -------
        TYPE str
            Query the OPC value

        '''
        return self.query('*OPC?').split('\n')[0]
    
# =============================================================================
# Initialize Commando
# =============================================================================

    def Init(self):
        '''
        

        Returns
        -------
        None.
            Start measurement

        '''
        self.write(':INITiate:IMMediate')
        
# =============================================================================
# Abort Measurement
# =============================================================================

    def Abort(self):
        '''
        

        Returns
        -------
        None. 
            Abort measurement

        '''
        
        self.write('ABORt')
        
# =============================================================================
# Adapter Settings
# =============================================================================


    def ask_AdapterType(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries default sensor adapter type

        '''
        return self.query('INPut:ADAPter:TYPE?')
    
    
    def set_AdapterType(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Sets default sensor adapter type:
                Allow senor types are: ['PHOTodiode','THERmal','PYRo']
        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        stState = ['PHOTodiode','THERmal','PYRo']
        if state in stState:
            self.write('INPut:ADAPter:TYPE ' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
# =============================================================================
# Photodiode parameters
# =============================================================================
    def set_PD(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
            Sets the bandwidth of the photodiode input stage. 
                Can be ['ON','OFF',1,0]
        Raises
        ------
        ValueError
            Error message.
            
        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
       
        stState = ['ON','OFF',1,0]
        if state in stState:
            self.write('INPut:PDIode:FILTer:LPASs:STATe ' + str(state))
        else:
            return ValueError('Unknown input! See function description for more info.')
        
# =============================================================================
# Ask Instrument 
# =============================================================================

    def ask_beeper(self):
        '''
        

        Returns
        -------
        Type print str
            Return the state of the the beeper

        '''
        status = self.query('SYSTem:BEEPer:STATe?').split('\n')[0]
        if status == '1':
            print('Beeper is ON')
        else:
            print('Beeper is OFF')



    def ask_calibration(self):
        '''
        

        Returns
        -------
        TYPE str
            Returns a human readable calibration string. This is a query
            only command. The response is formatted as string response
            data.

        '''
        
        return self.query('CALibration:STRing?').split('\n')[0]
    
    
    
    
    
    def ask_PDPower(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the photodiode response value.

        '''
        
        return self.query('CORRection:POWer:PDIOde:RESPonse?').split('\n')[0]
    
    
    
    
    def ask_Thermopile(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the thermopile response value

        '''
        
        return self.query('POWer:THERmopile:RESPonse?').split('\n')[0]
    
    
    
    
    def ask_Pyro(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the pyro-detectro response value

        '''
        
        return self.query('ENERgy:PYRO:RESPonse?').split('\n')[0]
    
    
    
    def ask_energyRange(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the energy range

        '''
        return self.query('ENERgy:RANGe:UPPer?').split('\n')[0]
    
    
    
    
    def ask_currentRange(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the current curent range

        '''
        return self.query('CURRent:DC:UPPer?').split('\n')[0]
    
    
    
    
    def ask_AutoCurrentRange(self):
        '''
        

        Returns
        -------
        TYPE str 
            Queries the auto-ranging function state

        '''
        return self.query('CURRent:DC:AUTO?').split('\n')[0]
    
    
    
    
    def ask_freqRange(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Queries the frequency range. 
            Can be  ['MAX','MIN']

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        TYPE
            Queries the frequency range

        '''
        stState = ['MAX','MIN']
        if state in stState:
            if state == 'MAX':
                state = 'UPPer?'
                return self.query('SENSe:FREQuency:Range:' + state).split('\n')[0]
            else:
                state = 'LOWer?'
                return self.query('SENSe:FREQuency:Range:' + state).split('\n')[0]
        else:
            raise ValueError('Unknown input! See function description for more info.')
 
    
 
    
    def ask_PowerUnits(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the power unit

        '''
        
        return self.query('SENSe:POWer:DC:UNIT?').split('\n')[0]
    
    
    
    def ask_AutoPowerRange(self):
        '''
        

        Returns
        -------
        status : print massage str
            Queries the auto-ranging function state

        '''
        
        status = self.query('POWer:DC:RANGe:AUTO?').split('\n')[0]
        if status == '1':
            print('Auto Range is ON')
        else:
            print('Auto Range is OFF')
        return status

    



    def ask_PowerRange(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the power range.

        '''
        
        return self.query('POWer:DC:RANGe:UPPer?').split('\n')[0]
    
    
    
    
    def ask_voltRange(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the current voltage range

        '''
        
        return self.query('VOLTage:DC:UPPer?').split('\n')[0]
    
    
    
    
    def ask_AutoVoltageRange(self):
        '''
        

        Returns
        -------
        TYPE str
           Queries the auto-ranging function state

        '''
        
        return self.query('VOLTage:DC:AUTO?').split('\n')[0]
    
    
    
    
    def ask_Wavelength(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the operation wavelength

        '''
        
        return self.query('CORRection:WAVelength?').split('\n')[0]
    
    
    
    
    def ask_BeamDiameter(self):
        '''
        

        Returns
        -------
        TYPE str 
            Queries the beam diameter

        '''
       
        return self.query('CORRection:BEAMdiameter?').split('\n')[0]
    
    
    
    
    def ask_Average(self):
        '''
        

        Returns
        -------
        TYPE str
            Queries the averaging rate

        '''
    
        return self.query('SENSe:AVERage:COUNt?').split('\n')[0]
    
    
    

# =============================================================================
# Set Power,Energy,Current,Voltage Measurment Values aand Wavelength
# =============================================================================

    def set_PowerUnits(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Sets the power unit W or dBm. Can be ['W','dBm'].

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        stState = ['W','dBm']
        if state in stState:
            self.write('POWer:DC:UNIT ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    
    def set_AutoPowerRange(self,state):
        '''
        

        Parameters
        ----------
        state : float/int
            Switches the auto-ranging function on and off. Can be set to ['ON','OFF',1,0].
        
        
         Raises
        ------
        ValueError
            Error message.
            
            
        Returns
        -------
        None.

        '''
        stState = ['ON','OFF',1,0]
        if state in stState:
            self.write('POWer:DC:RANGe:AUTO ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_PowerRange(self,value):
        '''
        

        Parameters
        ----------
        value : float
             Sets the current range in W

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        #unit = str(input('Give a power unit Value [W|dBm]: '))
        #self.set_PowerUnits(unit)
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('POWer:DC:RANGe:UPPer ' + value + ' W')  
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
        
    def set_AutoCurrentRange(self,state):
        '''
        

        Parameters
        ----------
        state : str
            Switches the auto-ranging function on and off. Can be set to ['ON','OFF',1,0].
        
        Raises
        ------
        ValueError
            Error message.
        
        Returns
        -------
        None.

        '''
        
        stState = ['ON','OFF',1,0]
        if state in stState:
            self.write('SENSe:CURRent:DC:RANGe:AUTO ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
            
    def set_currentRange(self,value):
        '''
        

        Parameters
        ----------
        value : float
           Sets the current range in A.
           
           
        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
       
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:CURRent:DC:RANGe:UPPer ' + value + ' A')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
     
    def set_AutoVoltageRange(self,state):
        '''
        

        Parameters
        ----------
        state : str/int
            witches the auto-ranging function on and off. Can be ['ON','OFF',1,0]
        
        
        Raises
        ------
        ValueError
            Error message.
            
            
        Returns
        -------
        None.

        '''
        
        stState = ['ON','OFF',1,0]
        if state in stState:
            self.write('SENSe:VOLTage:DC:RANGe:AUTO ' + str(state))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
         
    def set_voltageRange(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the voltage range in V

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:VOLTage:DC:RANGe:UPPer ' + value + ' V')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
        
    def set_energyRange(self,value):
        '''
        

        Parameters
        ----------
        value : float
             Sets the voltage range in J

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        None.

        '''
        
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:ENERgy:DC:RANGe:UPPer ' + value + ' J')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_WaveLength(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the operation wavelength in nm.

        Returns
        -------
        None.

        '''
        
        self.write('SENSe:CORRection:WAVelength ' + str(value) + ' nm')
        
        
        
    def set_Average(self,value):
        '''
        

        Parameters
        ----------
        value : float
            Sets the averaging rate (1 sample takes approx. 3ms)

        Returns
        -------
        None.

        '''
        self.write('SENSe:AVERage:COUNt ' + value)
        
        
        
        
# =============================================================================
# Configure
# =============================================================================


    def ConfigPower(self):
        '''
        

        Returns
        -------
        None.
            Configure for power measurement

        '''
        
        self.write(':CONFigure:POWer')
        
        
        
    def ConfigCurrent(self):
        '''
        

        Returns
        -------
        None.
             Configure for current measurement

        '''
        
        self.write(':CONFigure:CURRent:DC')
        
        
        
        
    def ConfigVoltage(self):
        '''
        

        Returns
        -------
        None.
            Configure for voltage measurement

        '''
        
        self.write(':CONFigure::VOLTage:DC')
        
        
        
        
    def ConfigEnergy(self):
        '''
        

        Returns
        -------
        None.
            Configure for energy measurement

        '''
        
        self.write(':CONFigure:ENERgy')
        
        
        
        
    def ConfigFreq(self):
        '''
        

        Returns
        -------
        None.
            Configure for frequency measuremen
        '''
        
        self.write(':CONFigure:FREQuency')
      
        
      
        
    def ConfigPowerDensity(self):
        '''
        

        Returns
        -------
        None.
            Configure for power density measuremen

        '''
        self.write(':CONFigure:PDENsity')
        
        
        
    def ConfigEnergyDensity(self):
        '''
        

        Returns
        -------
        None.
            Configure for energy density measurement

        '''
        self.write(':CONFigure:EDENsity')
        
        
        
    def ConfigResistance(self):
        '''
        

        Returns
        -------
        None.
            Configure for sensor presence resistance measurement

        '''
        self.write(':CONFigure:RESistance')
        
        
        
    def ConfigTemp(self):
        '''
        

        Returns
        -------
        None.
            Configure for sensor temperature measurement

        '''
        self.write(':CONFigure:TEMPerature')
        
        
        
# =============================================================================
# Perform Measurment    
# =============================================================================

    def MeasPower(self):
        '''
        

        Returns
        -------
        None.
            Perform Power meas

        '''
        self.write('MEASure:POWer')
        
        
        
    def MeasCurrent(self):
        '''
        

        Returns
        -------
        None.
            Performs a current measurement

        '''
        
        self.write('MEASure:CURRent:DC ')
        
        
        
        
    def MeasVoltage(self):
        '''
        

        Returns
        -------
        None.
            Performs a voltage measurement

        '''
       
        self.write('MEASure:VOLTage:DC')
        
        
        
        
        
    def MeasEnergy(self):
        '''
        

        Returns
        -------
        None.
            Performs a energy measuremen

        '''
        self.write('MEASure:ENERgy')
        
        
        
        
    def MeasPowerDensity(self):
        '''
        

        Returns
        -------
        None.
            Performs a power density measurement

        '''
        self.write('MEASure:PDENsity')
        
        
        
        
    def MeasEnergyDensity(self):
        '''
        

        Returns
        -------
        None.
            Performs a energy density measuremen

        '''
        self.write('MEASure:EDENsity')
        
        
        
        
    def MeasResistance(self):
        '''
        

        Returns
        -------
        None.
             Performs a sensor presence resistance measurement

        '''
        self.write('MEASure:RESistance')
        
        
        
        
        
    def MeasTemp(self):
        '''
        

        Returns
        -------
        None.
             Performs a sensor temperature measuremen

        '''
        self.write('MEASure:TEMPerature')
        
        
        
    def MeasFreq(self):
        '''
        

        Returns
        -------
        None.
            Performs a frequency measurement

        '''
        self.write('MEASure:FREQuency')
        
        
    
# =============================================================================
# Measurment Test 
# =============================================================================
    
    def adjustPowerMeas(self):
        '''
        

        Returns
        -------
        None.
            Adjust the Power Measurments

        '''
        un = input('Set Power unit W/dBm: ')
        self.set_PowerUnits(un)
        dis = input('Set Power Measurment Range auto/manual: ')
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoPowerRange('ON')
            else:
                self.set_AutoPowerRange('OFF')
                val = float(input('Sets the upper Power range in W to: '))
                self.set_PowerRange(val)
        else:
            print('Invalid input! adjustPowerMeas() is stoped!')
      
            
      
        
    def adjustEnergyMeas(self):
        '''
        

        Returns
        -------
        None.
           Adjust the Energy Measurment.

        '''
        print('Energy is measured in J')
        value = float(input('Set Energy range in J: '))
        self.set_energyRange(value)
        
        
        
        
        
        
    def adjustVoltageRange(self):
        '''
        

        Returns
        -------
        None.
            Adjust the Voltage Measurments.

        '''
        dis = input('Set Voltage Measurment Range auto/manual: ')
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoVoltageRange('ON')
            else:
                self.set_AutoVoltageRange('OFF')
                value = float(input('Sets the upper range to: '))
                self.set_voltageRange(value)
        else:
            print('Invalid input! adjustVoltageRange() is stoped!')
        
    
    
    
    
    
    def adjustCurrentRange(self):
        '''
        

        Returns
        -------
        None.
            Adjust the Voltage Measurment.

        '''
        dis = input('Set Current Measurment Range auto/manual: ')
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoCurrentRange('ON')
            else:
                self.set_AutoVoltageRange('OFF')
                value = float(input('Sets the upper range to: '))
                self.set_currentRange(value)
        else:
            print('Invalid input! adjustVoltageRange() is stoped!')
        
      
           

        
    def set_Parameters(self,Type):
        '''
        

        Parameters
        ----------
        Type : str
            This function will set the measurments parameters.
            Can be set to Type = ['Power','Energy','Current','Voltage']

        Returns
        -------
        None.

        '''
        
        
        waveL = float(input('Sets the operation wavelength in nm: '))
        self.set_WaveLength(waveL)
        diss = Type
        dissList = ['Power','Energy','Current','Voltage']
        if diss in dissList:
            if diss == 'Power':
                self.adjustPowerMeas()
            elif diss == 'Energy':
                self.adjustEnergyMeas()
            elif diss == 'Voltage':
                self.adjustVoltageRange()
            else:
                self.adjustCurrentRange()
        else:
            print('Invalid input! Function will be stoped!')
            
        
        
        
        
        
        
    def DisplayParam(self,Type):
        '''
        

        Parameters
        ----------
        Type : str
            This function will print all the adjusted parameters.
            Can be set to Type = ['Power','Energy','Current','Voltage']

        Returns
        -------
        None.

        '''
        
        print('Adapter Type: ',self.ask_AdapterType())
        print('Max Frequency range: ',self.ask_freqRange('MAX'))
        print('Min Frequency range: ',self.ask_freqRange('MIN'))
        print('Waveelength: ',self.ask_Wavelength())
        
        meas = Type
        measList = ['Power','Energy','Current','Voltage']
        if meas in measList:
            if meas == 'Power': 
                print('Power Unit set: ',self.ask_PowerUnits())
                print('Power range auto: ',self.ask_AutoPowerRange())
                print('Power Range set: ',self.ask_PowerRange())
                
            elif meas == 'Energy':
                print('Energy range auto: ',self.ask_energyRange())
            elif meas == 'Voltage':
                print('Voltage range auto: ',self.ask_AutoVoltageRange())
                print('Voltage range: ',self.ask_voltRange())
            elif meas == 'Current':
                print('Current range auto: ',self.ask_AutoCurrentRange())
                print('Current range: ',self.ask_currentRange())
        else:
            print('Invalid Value! Function will be terminated.')
        
        
        
        
        
    def DisplayParamDict(self,Type):
        '''
        

        Parameters
        ----------
        Type : str
            This function will print all the adjusted parameters.
            Can be set to Type = ['Power','Energy','Current','Voltage']

        Returns
        -------
        Headers : str
            String with ['Power','Energy','Current','Voltage']
        Data : lidt
            Data from the instrument.
        Params : list
            List with str for different data that are extractet from the instrument.

        '''
        '''
        This function will print all the adjusted parameters.
        '''
        Headers = ['Power','Energy','Current','Voltage']
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
        
        
                
                

                
    def PowerMeas(self):
        '''
        

        Returns
        -------
        data : Data from the measurment 
            Performs a power measurement

        '''
        '''
        Performs a power measurement
        '''
        print('This Function prtforme Power measurments.')
        #print('To go on whit the measurments please check again the parameters set!')
        self.set_Parameters('Power')
        print('#####################################')
        self.DisplayParam('Power')
        print('#####################################')

        com = input('Should the measurment proceed yes/no: ')
        if com == 'yes':
            
            self.Init()
            complite = 0
            while complite == '1':
                complite = self.OPC()
                self.timeout = 0.1
            self.ConfigPower()
            self.MeasPower()
            data = self.fetchData()
            
            return data
        else:
            print('Measurment is canceled!')

             

    def DefaultPowerMeas(self, WaveLength):
        '''
        

        Returns
        -------
        TYPE Data from the measurment 
            Performs a power measurement whit hard codded parameter!.

        '''
        
        self.set_PowerUnits('dBm')
        self.set_WaveLength(WaveLength)
        self.set_AutoPowerRange('ON')
        
        #print('#####################################')
        #self.DisplayParam('Power')
        #print('#####################################')
        self.Init()
        complite = 0
        while complite == '1':
            complite = self.OPC()
            self.timeout = 0.1
        self.ConfigPower()
        self.MeasPower()
        return self.fetchData()   




    def PowerSpecifications(self):
        '''
        

        Returns
        -------
        None.
            Return Instrument parameters

        '''
        
        self.DisplayParam('Power')
        
        

        

