# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 08:27:01 2021

@author: MartinMihaylov
"""



import time
import numpy as np
import pyvisa as visa


    
class PM100D:
    """
    Thorlabs PM100-series power meter wrapper using PyVISA.

    You can construct either with:
      - resource_str="P00XXXXX"       # serial only (legacy behavior)
      - resource_str="USB0::...::INSTR"  # full VISA resource (also works)
      - resource_name="USB0::...::INSTR" # explicit VISA resource

    Parameters
    ----------
    resource_str : str | None
        Either the device serial (e.g., 'P00XXXXX') or a full VISA string. Kept
        for backward compatibility.
    resource_name : str | None
        Explicit VISA resource name to open. If given, resource_str is ignored.
    backend : str | None
        Optional PyVISA backend string, e.g., '@py' for pyvisa-py.
    timeout_ms : int
        VISA I/O timeout in milliseconds.
    """
    def __init__(self,
                 resource_str: str | None = None,
                 *,
                 resource_name: str | None = None,
                 backend: str | None = None,
                 timeout_ms: int = 1000):

        
        if resource_str is None and resource_name is None:
            raise ValueError("Provide either 'resource_str' or 'resource_name'.")

        # Choose the effective VISA resource name
        if resource_name is not None:
            rn = str(resource_name)
        else:
            s = str(resource_str)
            if "::" in s or s.startswith("USB"):
                # Caller passed a full VISA string in resource_str
                rn = s
            else:
                # Caller passed a bare serial; build a PM100D VISA address
                # Vendor ID 0x1313 = Thorlabs; Product ID 0x8078 = PM100D USBTMC
                rn = f"USB0::0x1313::0x8078::{s}::INSTR"

        self._backend = backend
        self._rm = visa.ResourceManager(backend) if backend else visa.ResourceManager()
        self._resource_name = rn
        self._resource = self._rm.open_resource(rn)
        self._resource.timeout = int(timeout_ms)
        self._resource.read_termination = '\n'

        # Query *IDN? to verify connectivity (Thorlabs PM100* expected)
        self.idn = self.getIdn()
        print(self.idn)

        # Predefine Lists
        self._ON_OFF_StateLS_mapping = {
            "on": "ON",
            "off": "OFF",
            1: "ON",
            0: "OFF",
            "1": "ON",
            "0": "OFF",
            True: "ON",
            False: "OFF",
        }

        
    def query(self, message):
        return self._resource.query(message)
    
    def write(self, message):
        return self._resource.write(message)
    
    def Close(self):
        self._resource.close()
        print('Instrument PM100D is closed!')
    
    def getIdn(self) -> str:
        """Returns the Instrument Identification: Thorlabs,PM100D"""
        return self.query("*IDN?")
    
       
# =============================================================================
#     Checks and Validations
# =============================================================================

    def _validate_on_off_state(self, state: int | str) -> str:
        state_normalized = self._ON_OFF_StateLS_mapping.get(
            state.lower() if isinstance(state, str) else int(state)
        )
        if state_normalized is None:
            raise ValueError("Invalid state given! State can be [on,off,1,0,True,False].")
        return state_normalized
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
    def ReadConfig(self) -> str:
        '''
        

        Returns
        -------
        str
            Query the current measurement configuration

        '''
        
        return self.query('CONFigure?')

    
# =============================================================================
# Fetch last meassure Data 
# =============================================================================

    def fetchData(self, allow_NaN: bool = False, delay: float|None = None) -> float:
        '''Reads last measurement data. WILL NOT START THE MEASUREMENT!
        Use readData() instead. Returns 'nan' if no data is available.
        

        Returns
        -------
        float
            last measurement data or 'nan' if no data is available.
        '''
        val = float(self.query(':FETCh?'))
        if abs(val) >= 9.0e37:
            delay = 1 if delay is None else delay
            val = self.readData(delay=delay, allow_NaN=allow_NaN)
        return val
    
    def readData(self, allow_NaN: bool = False, delay: float|None = 1) -> float:
        '''Starts a measurement and reads last measurement data.

        Returns
        -------
        float
            last measurement data or 'nan' if no data is available.
        '''
        s = self.query(':READ?', delay=delay)  # triggers, waits, returns result
        val = float(s)
        if abs(val) >= 9.0e37:
            if allow_NaN:
                return float('nan')
            else:
                raise OverflowError(f"READ? returned sentinel {val}")
        return val
    
    
# =============================================================================
# OPC Register
# =============================================================================

    def OPC(self) -> str:
        '''
        

        Returns
        -------
        str
            Query the OPC value

        '''
        return self.query('*OPC?')
    
# =============================================================================
# Initialize Commando
# =============================================================================

    def Init(self) -> None:
        '''Start measurement.
        

        Returns
        -------
        None.

        '''
        self.write(':INITiate:IMMediate')
        
# =============================================================================
# Abort Measurement
# =============================================================================

    def Abort(self) -> None:
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


    def ask_AdapterType(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries default sensor adapter type

        '''
        return self.query('INPut:ADAPter:TYPE?')
    
    
    def set_AdapterType(self, state : str) -> None:
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
    def set_PD(self,state: str|int) -> None:
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

        '''
        state = self._validate_on_off_state(state)
        self.write(f'INPut:PDIode:FILTer:LPASs:STATe {state}')

        
# =============================================================================
# Ask Instrument 
# =============================================================================

    def ask_beeper(self) -> int:
        '''
        

        Returns
        -------
        int
            Return the state of the beeper.

        '''
        return int(self.query('SYSTem:BEEPer:STATe?'))



    def ask_calibration(self) -> str:
        '''
        

        Returns
        -------
        str
            Returns a human readable calibration string.

        '''
        
        return self.query('CALibration:STRing?')
    
    
    
    
    
    def ask_PDPower(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the photodiode response value.

        '''
        
        return self.query('CORRection:POWer:PDIOde:RESPonse?')
    
    
    
    
    def ask_Thermopile(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the thermopile response value.

        '''
        
        return self.query('POWer:THERmopile:RESPonse?')
    
    
    
    
    def ask_Pyro(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the pyro-detectr response value.

        '''
        
        return self.query('ENERgy:PYRO:RESPonse?')
    
    
    
    def ask_energyRange(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the energy range.

        '''
        return self.query('ENERgy:RANGe:UPPer?')
    
    
    
    
    def ask_currentRange(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the actual current range.

        '''
        return self.query('CURRent:DC:UPPer?')
    
    
    
    
    def ask_AutoCurrentRange(self) -> str:
        '''
        

        Returns
        -------
        str 
            Queries the auto-ranging function state.

        '''
        return self.query('CURRent:DC:AUTO?')
    
    
    
    
    def ask_freqRange(self,state: str) -> str:
        '''Queries the frequency range.
        

        Parameters
        ----------
        state : str
            Can be  ['MAX','MIN']

        Raises
        ------
        ValueError
            Error message.

        Returns
        -------
        str
            Queries the frequency range.

        '''
        stState = ['MAX','MIN']
        if state in stState:
            if state == 'MAX':
                state = 'UPPer?'
                return self.query('SENSe:FREQuency:Range:' + state)
            else:
                state = 'LOWer?'
                return self.query('SENSe:FREQuency:Range:' + state)
        else:
            raise ValueError('Unknown input! See function description for more info.')
 
    
 
    
    def ask_PowerUnits(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the power unit.

        '''
        
        return self.query('SENSe:POWer:DC:UNIT?')
    
    
    
    def ask_AutoPowerRange(self) -> str:
        '''
        

        Returns
        -------
        str
            Queries the auto-ranging function state.

        '''
        
        return self.query('POWer:DC:RANGe:AUTO?')

    



    def ask_PowerRange(self):
        '''
        

        Returns
        -------
        str
            Queries the power range.

        '''
        
        return self.query('POWer:DC:RANGe:UPPer?')
    
    
    
    
    def ask_voltRange(self):
        '''
        

        Returns
        -------
        str
            Queries the current voltage range.

        '''
        
        return self.query('VOLTage:DC:UPPer?')
    
    
    
    
    def ask_AutoVoltageRange(self):
        '''
        

        Returns
        -------
        str
           Queries the auto-ranging function state.

        '''
        
        return self.query('VOLTage:DC:AUTO?')
    
    
    
    
    def ask_Wavelength(self):
        '''
        

        Returns
        -------
        str
            Queries the operation wavelength.

        '''
        
        return self.query('CORRection:WAVelength?')
    
    
    
    
    def ask_BeamDiameter(self):
        '''
        

        Returns
        -------
        str 
            Queries the beam diameter.

        '''
       
        return self.query('CORRection:BEAMdiameter?')
    
    
    
    
    def ask_Average(self):
        '''
        

        Returns
        -------
        str
            Queries the averaging rate.

        '''
    
        return self.query('SENSe:AVERage:COUNt?')
    
    
    

# =============================================================================
# Set Power,Energy,Current,Voltage Measurment Values aand Wavelength
# =============================================================================

    def set_PowerUnits(self,state: str) -> None:
        '''
        

        Parameters
        ----------
        state : str
            Sets the power unit W or dBm. Can be ['W','dBm'].

        Raises
        ------
        ValueError
            Error message.

        '''
        
        stState = ['W','dBm']
        if state in stState:
            self.write('POWer:DC:UNIT ' + str(state))
        else:
            raise ValueError(f'Unknown input! You selected {state}. Allowed inputs are {stState}')
    
    
    
    
    def set_AutoPowerRange(self,state: str|int) -> None:
        '''Switches the auto-ranging function on and off.
        

        Parameters
        ----------
        state : str/int
             Can be set to ['ON','OFF',1,0].
        
        
         Raises
        ------
        ValueError
            Error message.

        '''
        state = self._validate_on_off_state(state)
        self.write(f'POWer:DC:RANGe:AUTO {state}')
         
            
            
            
    def set_PowerRange(self,value: float|int) -> None:
        '''
        

        Parameters
        ----------
        value : float/int
             Sets the current range in W

        Raises
        ------
        ValueError
            Error message.

        '''
        
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('POWer:DC:RANGe:UPPer ' + value + ' W')  
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
        
    def set_AutoCurrentRange(self,state: str|int) -> None:
        '''Switches the auto-ranging function on and off.
        

        Parameters
        ----------
        state : str/int
            Can be set to ['ON','OFF',1,0].
        
        Raises
        ------
        ValueError
            Error message.

        '''
        
        state = self._validate_on_off_state(state)
        self.write(f'SENSe:CURRent:DC:RANGe:AUTO {state}')          
            
            
            
            
    def set_currentRange(self,value: float|int) -> None:
        '''
        

        Parameters
        ----------
        value : float/int
           Sets the current range in A.
           
           
        Raises
        ------
        ValueError
            Error message.

        '''
       
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:CURRent:DC:RANGe:UPPer ' + value + ' A')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
     
    def set_AutoVoltageRange(self,state: str|int) -> None:
        '''Switches the auto-ranging function on and off.
        

        Parameters
        ----------
        state : str/int
            Can be ['ON','OFF',1,0]
        
        
        Raises
        ------
        ValueError
            Error message.

        '''
        
        state = self._validate_on_off_state(state)
        self.write(f'SENSe:VOLTage:DC:RANGe:AUTO {state}')
         
            
         
    def set_voltageRange(self,value: float) -> None:
        '''
        

        Parameters
        ----------
        value : float
            Sets the voltage range in V

        Raises
        ------
        ValueError
            Error message.

        '''
        
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:VOLTage:DC:RANGe:UPPer ' + value + ' V')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
        
        
    def set_energyRange(self,value: float|int) -> None:
        '''
        

        Parameters
        ----------
        value : float
             Sets the energy range in J

        Raises
        ------
        ValueError
            Error message.

        '''
        
        if type(value) == int  or type(value) == float:
            value = str(value)
            self.write('SENSe:ENERgy:DC:RANGe:UPPer ' + value + ' J')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_WaveLength(self,value: float|int) -> None:
        '''
        

        Parameters
        ----------
        value : float/int
            Sets the operation wavelength in nm.

        '''
        
        self.write(f'SENSe:CORRection:WAVelength {value} nm')
        
        
        
    def set_Average(self,value: float|int) -> None:
        '''
        

        Parameters
        ----------
        value : float/int
            Sets the averaging rate (1 sample takes approx. 3ms)

        '''
        self.write(f'SENSe:AVERage:COUNt {value}')
        
        
        
        
# =============================================================================
# Configure
# =============================================================================


    def ConfigPower(self) -> None:
        '''
        Configure for power measurement.            

        '''
        self.write(':CONFigure:POWer')
        
        
        
    def ConfigCurrent(self) -> None:
        '''
        Configure for current measurement.

        '''
        self.write(':CONFigure:CURRent:DC')
        
        
        
        
    def ConfigVoltage(self) -> None:
        '''
        Configure for voltage measurement.

        '''
        self.write(':CONFigure::VOLTage:DC')
        
        
        
        
    def ConfigEnergy(self) -> None:
        '''
        Configure for energy measurement.

        '''
        self.write(':CONFigure:ENERgy')
        
        
        
        
    def ConfigFreq(self) -> None:
        '''
         Configure for frequency measurement.
        '''
        self.write(':CONFigure:FREQuency')
      
        
      
        
    def ConfigPowerDensity(self) -> None:
        '''
        Configure for power density measurement.

        '''
        self.write(':CONFigure:PDENsity')
        
        
        
    def ConfigEnergyDensity(self) -> None:
        '''
        Configure for energy density measurement.

        '''
        self.write(':CONFigure:EDENsity')
        
        
        
    def ConfigResistance(self) -> None:
        '''
        Configure for sensor presence resistance measurement.

        '''
        self.write(':CONFigure:RESistance')
        
        
        
    def ConfigTemp(self) -> None:
        '''
        Configure for sensor temperature measurement.

        '''
        self.write(':CONFigure:TEMPerature')
        
        
        
# =============================================================================
# Perform Measurment    
# =============================================================================

    def MeasPower(self) -> None:
        '''
        Performs a Power measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:POWer')
        
        
        
    def MeasCurrent(self) -> None:
        '''
        Performs a current measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:CURRent:DC ')
        
        
        
        
    def MeasVoltage(self) -> None:
        '''
        Performs a voltage measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:VOLTage:DC')
        
        
        
        
        
    def MeasEnergy(self) -> None:
        '''
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:ENERgy')
        
        
        
        
    def MeasPowerDensity(self) -> None:
        '''
        Performs a power density measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:PDENsity')
        
        
        
        
    def MeasEnergyDensity(self) -> None:
        '''
        Performs an energy density measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:EDENsity')
        
        
        
        
    def MeasResistance(self) -> None:
        '''
        Performs a sensor presence resistance measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:RESistance')
        
        
        
        
    def MeasTemp(self) -> None:
        '''
        Performs a sensor temperature measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:TEMPerature')
        
        
        
    def MeasFreq(self) -> None:
        '''
        Performs a frequency measurement.
        Maxim: Does nothing? Measure with Init() or readData() instead!
        '''
        self.write('MEASure:FREQuency')
        
        
    
# =============================================================================
# Measurment Test 
# =============================================================================
    
    def adjustPowerMeas(self) -> None:
        '''Legacy function. Do not use.
        Adjust the power measurement interactively. 

        '''
        un = input("Set Power unit 'W' or 'dBm': ")
        self.set_PowerUnits(un)
        dis = input("Set Power Measurement Range 'auto' or 'manual': ")
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoPowerRange('ON')
            else:
                self.set_AutoPowerRange('OFF')
                val = float(input('Sets the upper Power range in W to: '))
                self.set_PowerRange(val)
        else:
            print('Invalid input! adjustPowerMeas() is stopped!')
      
            
      
        
    def adjustEnergyMeas(self):
        '''Legacy function. Do not use.
        Adjust the Energy Measurement interactively.

        '''
        print('Energy is measured in J')
        value = float(input('Set Energy range in J: '))
        self.set_energyRange(value)
        
        
        

    def adjustVoltageRange(self):
        '''Legacy function. Do not use.
        Adjust the Voltage Measurement interactively.

        '''
        dis = input("Set Voltage Measurement Range 'auto' or 'manual': ")
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoVoltageRange('ON')
            else:
                self.set_AutoVoltageRange('OFF')
                value = float(input('Sets the upper range to: '))
                self.set_voltageRange(value)
        else:
            print('Invalid input! adjustVoltageRange() is stopped!')
        
    
    
        
    def adjustCurrentRange(self):
        '''Legacy function. Do not use.
        Adjust the Current Measurement interactively.

        '''
        dis = input("Set Current Measurement Range 'auto' or 'manual': ")
        disList = ['auto','manual']
        if dis in disList:
            if dis == 'auto':
                self.set_AutoCurrentRange('ON')
            else:
                self.set_AutoVoltageRange('OFF')
                value = float(input('Sets the upper range to: '))
                self.set_currentRange(value)
        else:
            print('Invalid input! adjustVoltageRange() is stopped!')
        
      
           
     
    def set_Parameters(self,Type:str) -> None:
        '''Legacy function. Do not use. 
        This function will set the measurement parameters interactively.
        

        Parameters
        ----------
        Type : str 
            Can be set to Type = ['Power','Energy','Current','Voltage']

        '''
        
        
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
            print('Invalid input! Function will be stopped!')
            
        
        
        
    def DisplayParam(self,Type:str) -> None:
        '''Legacy function. Do not use.
        This function will print all the adjusted parameters.
        

        Parameters
        ----------
        Type : str
            Can be set to Type = ['Power','Energy','Current','Voltage']


        '''
        
        print('Adapter Type: ',self.ask_AdapterType())
        print('Max Frequency range: ',self.ask_freqRange('MAX'))
        print('Min Frequency range: ',self.ask_freqRange('MIN'))
        print('Wavelength: ',self.ask_Wavelength())
        
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
        
        
        
        
    def DisplayParamDict(self,Type:str) -> None:
        '''This function will print all the adjusted parameters.
        

        Parameters
        ----------
        Type : str
            Can be set to Type = ['Power','Energy','Current','Voltage']

        Returns
        -------
        Headers : str
            String with ['Power','Energy','Current','Voltage']
        Data : list
            Data from the instrument.
        Params : list
            List with str for different data that are extracted from the instrument.

        '''

        Headers = ['Power','Energy','Current','Voltage']
        Params = ['Adapter Type','Max Frequency range','Min Frequency range','Wavelength']
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
        
        
                

    def PowerMeas(self) -> float:
        '''Legacy function. Do not use! Use get_Power instead.
        Performs a power measurement interactively.
        

        Returns
        -------
        float
            Data from the power measurement.

        '''

        print('This Function performs Power measurements.')
        #print('To go on whit the measurments please check again the parameters set!')
        self.set_Parameters('Power')
        print('#####################################')
        self.DisplayParam('Power')
        print('#####################################')

        com = input('Should the measurement proceed yes/no: ')
        if com == 'yes':
            
            self.Init()
            complete = '0'
            while complete != '1':
                complete = self.OPC()
                time.sleep(0.1)
            self.ConfigPower()
            self.MeasPower()
            return self.fetchData()
        else:
            print('Measurement is canceled!')

             

    def DefaultPowerMeas(self, WaveLength: float|int) -> float:
        '''Legacy function. Do not use! Use get_Power instead.
        Performs a power measurement with hard coded parameters! 
        PowerRange is set to auto.

        Parameters
        ----------
        WaveLength : float
            Wavelength in nm.
        
        Returns
        -------
        float 
            Power in dBm.

        '''
        
        self.set_PowerUnits('dBm')
        self.set_WaveLength(WaveLength)
        self.set_AutoPowerRange('ON')
        
        #print('#####################################')
        #self.DisplayParam('Power')
        #print('#####################################')
        self.Init()
        complete = '0'
        while complete != '1':
            complete = self.OPC()
            time.sleep(0.1)
        self.ConfigPower()
        self.MeasPower()
        return self.fetchData()   
        
        
        
    def DefaultPowerMeas_W(self, WaveLength: float|int) -> float:
        '''Legacy function. Do not use! Use get_Power instead.
        Performs a power measurement with hard coded parameters!
        PowerRange is set to auto.

        Parameters
        ----------
        WaveLength : float
            Wavelength in nm.
        
        Returns
        -------
        float
            Power in W.

        '''
        
        self.set_PowerUnits('W')
        self.set_WaveLength(WaveLength)
        self.set_AutoPowerRange('ON')
        
        #print('#####################################')
        #self.DisplayParam('Power')
        #print('#####################################')
        self.Init()
        complete = '0'
        while complete != '1':
            complete = self.OPC()
            time.sleep(0.1)
        self.ConfigPower()
        self.MeasPower()
        return self.fetchData()




    def PowerSpecifications(self) -> None:
        '''Legacy function. Do not use.
        This function will print all the adjusted parameters for the power measurement.

        '''
        
        self.DisplayParam('Power')

    
    def get_Power(self, 
                  unit: str = None, 
                  waveLength: float = None, 
                  allow_NaN: bool = False,
                  delay: float|None = None) -> float:
        '''Performs a Power measurement.

        Parameters
        ----------
        unit : str, optional
            Power unit ['W','dBm']. The default is None.
        waveLength : float, optional
            Wavelength in nm. The default is None.

        Returns
        -------
        float
            Power in dBm or W.

        '''
        
        if unit != None:
            self.set_PowerUnits(unit)
        if waveLength != None:
            self.set_WaveLength(waveLength)
        if self.ReadConfig() == 'POW':
            pass
        else:
            self.ConfigPower()

        self.Init()
        complete = '0'
        while complete != '1': # From Maxim: This does not work.
            complete = self.OPC()
            time.sleep(0.1)
        return self.fetchData(allow_NaN=allow_NaN, delay=delay)
    
    def ask_Power(self, 
                  unit: str = None, 
                  waveLength: float = None, 
                  allow_NaN: bool = False,
                  delay: float|None = None) -> float:
        '''Calls get_Power().

        Parameters
        ----------
        unit : str, optional
            Power unit ['W','dBm']. The default is None.
        waveLength : float, optional
            Wavelength in nm. The default is None.

        Returns
        -------
        float
            Power in dBm or W.

        '''
        return self.get_Power(unit,waveLength,allow_NaN,delay)
        
        

        

