# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 10:24:58 2022

@author: Martin.Mihaylov
"""

import pandas as pd
from InstrumentControl.Functions import Coupling_Stability
from InstrumentControl.Functions import MZM_transfer
from InstrumentControl.Functions import GC_transfer
from InstrumentControl.Functions import SG_SA_transfer
from InstrumentControl.Functions import SG_SA_Linearing
from InstrumentControl.Functions import Laserbeating_RF_Response
from InstrumentControl.Functions import Device_characterization
from InstrumentControl.Functions import MZM_transfer_Keithley
from InstrumentControl.Functions import Voltage_OSA
from InstrumentControl.Functions import Sweep_CWF_VNA
from InstrumentControl.Functions import Sweep_Power_VNA
from InstrumentControl.Functions import Laserbeating_RF_Response_CoBrite
from InstrumentControl.Functions import Tobias_MZM_passive_Equalizer
from InstrumentControl.Functions import Tobias_MZM_wo_Equalizer
from InstrumentControl.Functions import Tobias_MZM_measurement
from InstrumentControl.Functions import Tobias_MZM_characteristic_in_dependency_of_thermal_biasing
import os 




def __init__():
    print('''
          ########## Short Function Description ##########
              1) Coupling_Stability: 
                    In this function the coupling stability over time will be
                    measured. The Power Meter is used.
                    
              2) MZM_transfer:
                    In this function the transfer characteristic of a MZM Interferometer 
                    will be measured. For the purpase the MZM will be connected 
                    to a Power Supply that will sleep the Voltage from 0V to a 
                    given voltage. The Output of the MZM will be measured whit 
                    the Power Meter.
                    
              3) MZM_transfer_Keithley:
                    In this function the transfer characteristic of a MZM Interferometer 
                    will be measured. Same as function 2) but with the helpt of 
                    KEITHLEY Source Meter.
                    
              4) GC_transfer:
                    In this function the LU1000 from Novoptel will be sweept. The 
                    user will be askt to set a min and max wavelenght for the sweep. 
                    The Power Meter will measure the output of the Laser. It can be used 
                    to characterise different optical DUTs.
                    
              5) SG_SA_transfer:
                    In this function the CW Frequency of the Signal Generator will be 
                    sweept and the Spectrum will be measured with the Spectrum Analyzer.
                    The Spectrum Analyser is still not working properly so this function 
                    is still under construction!
                    
              6) SG_SA_Linearing:
                    This function will be used to measure and characterize non-linearitys
                    from the system(DUT). The Signal Generator will be set at fixed CW 
                    frequency. The power of the Signal Generator will be sweeped. The 
                    Spectrum Analyser will measure the first, secound thurd and forth 
                    peaks in a given frequency range. Afterwords a Total Harminic Distrotion
                    calculation will be done and the results will be saved. 
                    
             7) Laserbeating_RF_Response:
                    Durch die Schwebung zweier Laser kann man sehr hohe elektrische 
                    Frequenzen erzeugen. Zusätzlich ist die Schwebung sehr stabil in 
                    der optischen Amplitude über das komplette C-Band. Allerdings ist 
                    die Schwebungsfrequenz nicht so stabil. Deshalb sollten die Laser auf 
                    „Whispermode“ gestellt werden. Mit dieser Messroutine kann man schnell 
                    die Tranfercharakteristik von opto-elektrischen Empfängern bestimmen.
                    
             8) Device_characterization:
                    This function will use the Power Meter, Vectro Network Analyzer and
                    Source Meter to produce a dataset that will be used for further 
                    characterisation ot better understanding of a DUT.
                    Durch diese Routine können wir die Modellierung von Komponenten mit 
                    Daten füttern und bessere Simulationsmodelle bekommen.
                    
             9) Voltage_OSA:
                    This function will use the Optical Spectrum Analyzer and the Source Meter 
                    to sweep a given voltage and observe the optical signal spectrum. 
                    
            10) Sweep_CWF_VNA:
                    Sweep the continuous waveform(CW) Frequency from the Vectro analyzer Port 
                    by constant outpput Power. Spectrum Analyzer will detect the 
                    Signal and save the data in CSV, param and svg files.
                    
            11) Sweep_Power_VNA:
                    Sweep the Power from the Vectro Analyzer Port by constant continuous
                    waveform(CW) Frequency. Spectrum Analyzer will detect the 
                    Signal and save the data in CSV, param and svg files.
                    
            12) Laserbeating_RF_Response_CoBrite:
                    Same as Laserbeating_RF_Response! Will use the CoBrite Laser 
                    and the spectrum analyzer. No pewer meter needet. 
                    
            13) Tobias_MZM_passive_Equalizer:
                    A Function that is used to measure Tobias Chip(MZM passive Equalizer). The instruments needed are
                    VNA, Power Mether ThorLabs, Source Meter and Power Supply. The Voltage from 
                    the Power Supply will be sweeped. At each iteration, the source meter voltage 
                    is swept and for each voltage swept, a voltage measurement is made by the source 
                    meter, a power measurement is made by the power meter, and an S-parameter 4-port 
                    measurement is made. The information will be saved in .csv , .svg Files and additional 
                    .txt Files with speacial synthax suited for ADS. 
                    
            14) Tobias_MZM_wo_Equalizer:
                    A Function that is used to measure Tobias Chip(MZM wo Equalizer). The instruments needed are
                    VNA, Power Mether ThorLabs, Source Meter and Power Supply. The Voltage from 
                    the Power Supply will be sweeped. At each iteration, the source meter voltage 
                    is swept and for each voltage swept, a voltage measurement is made by the source 
                    meter, a power measurement is made by the power meter, and an S-parameter 4-port 
                    measurement is made. The information will be saved in .csv , .svg Files and additional 
                    .txt Files with speacial synthax suited for ADS. 
            
            15) Tobias_MZM_measurement:
                    A function which is used to measure an MZM. The instruments needed are
                    VNA (Anritsu MS4647B with extension), optical powermeter (ThorLabs S155C), 
                    SystemSourceMeter (Keithley 2612) and 2x Power Supply (RND Labs 320-KA3005P). 
                    In a first step, the voltage from the first power supply (connected to th.PS p) 
                    is swept, while the other power supply (connected to th.PS n) is turned off 
                    and the optical power is measured by means of the powermeter.
                    This process is repeated the other way around.
                    Afterwards, the maximum, minimum and the quadrature points are determined and saved,
                    and the MZM is biased to quadrature point.
                    Then, either the voltage or the current of the SystemSourceMeter is swept.
                    Both channels are swept with same voltage or current, 
                    and the corresponding current or voltage of both channels is measured.
                    For each voltage or current step, S-parameters are measured by means of the VNA.
                    All measurement results are saved in .snp, .csv, .txt and .svg files.
                    The syntax of the .txt files is adapted to ADS.
            
            16) Tobias_MZM_characteristic_in_dependency_of_thermal_biasing:
                    A function which is used to measure an MZM. The instruments needed are
                    VNA (Anritsu MS4647B with extension), optical powermeter (ThorLabs S155C), 
                    SystemSourceMeter (Keithley 2612) and 2x Power Supply (RND Labs 320-KA3005P).
                    The power supplies deliver the voltages fed to the thermal phaseshifters.
                    These voltages are swept and in each step the MZM characteristic is measured via the 
                    the VNA and the SystemSourceMeter.
                    This is repeated for multiple biasing voltages/currents 
                    of the regular Si phaseshifters in the MZM.
                    All measurement results are saved in .snp, .csv, .txt and .svg files.
                    The syntax of the .txt files is adapted to ADS.

          ''')
          

def MeasFunctions(Instrument,path):
    print('''
          ########## Functions  Menu ##########
              0) For short function description = 0
              1) Coupling_Stability = 1
              2) MZM_transfer = 2
              3) MZM_transfer_Keithley = 3 
              4) GC_transfer = 4
              5) SG_SA_transfer = 5
              6) SG_SA_Linearing = 6
              7) Laserbeating_RF_Response = 7
              8) Device_characterization = 8
              9) Voltage_OSA = 9
              10) Sweep_CWF_VNA = 10
              11) Sweep_Power_VNA = 11
              12) Laserbeating_RF_Response_CoBrite = 12
              13) Tobias_MZM_passive_Equalizer = 13
              14) Tobias_MZM_wo_Equalizer = 14
              15) Tobias_MZM_measurement = 15
              16) Tobias_MZM_characteristic_in_dependency_of_thermal_biasing = 16
              17) Exit
    
         ########## Functions  Menu ##########

          ''')
          
    FunctNameList = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
    FunctName = input('Function name: ')
    if FunctName in FunctNameList:
        while FunctName != '17':
            
            
            if FunctName == '1':
                print('''
                        Parameters
                        ----------
                        Time : int/float
                            Time in minutes. How many Min the Power Detector will measure the 
                            Power. 
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                            
                    
                        Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.
                      ''') 
                print('\n')
                Time = float(input('Time = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                name = input('name = ')
                
                Coupling_Stability(Instrument ,Time, WaveLength ,path ,name)
                break
            
            
        
            elif FunctName == '2':
                print(
                    '''

                        Parameters
                        ----------
                        Voltage : int/float
                            Voltage in V
                        Steps : int/float
                            Voltage step in V
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        Time : int
                            Delay time between the sweeps
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                        Current : boolen, optional
                            DESCRIPTION. The default is False. If curent need to be meassure 
                            set the Current = True. 
                    
                        Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.

                    ''')
                print('\n')
                Voltage = float(input('Voltage = '))
                Steps = float(input('Step = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Time = float(input('Time = '))
                name = input('name = ')
                Current = input('Current Meas (True/False) = ')
                if Current == 'True':
                    Current = True
                else:
                    Current = False
                MZM_transfer(Instrument ,Voltage ,Steps ,WaveLength ,Time ,path ,name ,Current)
                break
            
            
            
            elif FunctName == '3':
                print('''
    

                        Parameters
                        ----------
                        wmax : int/float
                            Maximal wavelength in nm
                        wmin : int/float
                            Minimal wavelength in nm
                        wstep : int/float
                            Step of the Wavelenth in nm
                        LaserChannel : int
                            Laser channel selected. It can be only 1 and 2 for LU1000 Laser Unit
                        LaserPower : int
                            Laser output power in dB.
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        wait : int
                            Delay time between the sweeps
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                    
                        Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.

                    ''')
                wmax = float(input('wmax = '))
                wmin = float(input('wmin = '))
                wstep = float(input('wstep = '))
                LaserChannel = int(input('LaserChannel = '))
                LaserPower = int(input('LaserPower = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Time = float(input('Time = '))
                name = input('name = ')
                GC_transfer(Instrument ,wmax ,wmin ,wstep ,LaserChannel ,LaserPower ,WaveLength ,Time ,path ,name)
                break
            
            
            
            
            elif FunctName == '4':
                
                print('''
                      
                      Not Working!!!!!
                      ''')
                      
                fmin = float(input('wmax = '))
                fmax = float(input('wmin = '))
                Schritte = float(input('wstep = '))
                Pec = int(input('LaserPower = '))
                unit = (input('Frequency Unit = '))
                name = input('name = ')
                SG_SA_transfer(Instrument,fmin,fmax,Schritte,Pec,unit,path,name)
                break
            
            
            
            elif FunctName == '5':
                print('''
    

                        Parameters
                        ----------
                        fin : int/float
                            Frequency. Depend on given 'unit' Parameter.
                        Pmin : int/float
                            Minimal Power in dBm
                        Pmax : int/float
                            Maximal Power in dBm
                        Steps : int/float
                            Power steps in dBm.
                        unit : str
                            Frequency Unit. It can be:
                                                        HZ - Herz
                                                        MHZ - Mega Herz
                                                        GHZ - Giga Herz
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                    
                        Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.

                        ''')
                        
                print('\n')
                fin = float(input('fin = '))
                Pmin = float(input('Pmin = '))
                Pmax = float(input('Pmax = '))
                Steps = float(input('Steps = '))
                unit = (input('Frequency Unit = '))
                name = input('name = ')
                SG_SA_Linearing(Instrument,fin,Pmin,Pmax,Steps,unit,path,name)
                break
            
            
            
            
            
            
            
            elif FunctName == '6':
                print('''
                    
                
                    Parameters
                    ----------
                    f_opt : TYPE
                        Frequency in Hz
                    f_min : TYPE
                        Minimal frequency in Hz
                    f_max : TYPE
                        Maximal freqeuncy in Hz
                    f_step : TYPE
                        Step frequency in Hz
                   LaserChannel : int
                        Laser channel selected. It can be only 1 and 2 for LU1000 Laser Unit
                    LaserPower : int
                        Laser output power in dB.
                    WaveLength : int
                        Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                    Loops : int
                        How many measurments should be done befor taken the max value from 
                        the Signal Generator.
                    path : str
                        Where to save the file.
                    name : str
                        Name of the File. The name is Combinationof the function name and 
                        name that you give.
                        For Example: Coupling_Stability_Test.csv
                
                    Raises
                    ------
                    ValueError
                        DESCRIPTION.
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and SVG plot
                    of the measurmend will be created and saved in the given in 'path' folder.

                    ''')
                print('\n')
                f_opt = float(input('f_opt = '))
                f_min = float(input('f_min = '))
                f_max = float(input('f_max = '))
                f_step = float(input('f_step = '))
                LaserChannel = int(input('LaserChannel = '))
                LaserPower = int(input('LaserPower = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Loops = int(input('Loops = '))
                name = input('name = ')
                Laserbeating_RF_Response(Instrument, f_opt, f_min, f_max, f_step ,LaserChannel ,LaserPower , WaveLength ,Loops ,path,name)
                break
            
            
            
            
            elif FunctName == '7':
                print('''
    
                
                    Parameters
                    ----------
                    V_min : int/float
                        Minimal voltage in V
                    V_max : int/float
                        Maximum voltage in V
                    V_step : int/float
                        Step voltage in V
                    WaveLength : int
                        Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                    Channel : str
                        Source Meter Channel 'A','a' or 'B','b'
                    path : str
                        Where to save the file.
                    name : str
                        Name of the File. The name is Combinationof the function name and 
                        name that you give.
                        For Example: Coupling_Stability_Test.csv
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and saved in the given in 'path' folder.

                    ''')
                print('\n')
                V_min = float(input('V_min = '))
                V_max = float(input('V_max = '))
                V_step = float(input('V_step = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Channel = input('Channel = ')
                name = input('name = ')
                Device_characterization(Instrument ,V_min , V_max , V_step ,WaveLength, Channel ,path ,name)
                break
            
            
            
            
            elif FunctName == '8':
                print('''
    

                    Parameters
                    ----------
                    Voltage : int/float
                        Voltage in V
                    Steps : int/float
                        Voltage steps in V
                    WaveLength : int
                        Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                    wait : int
                        Delay time between measurments
                    Channel : str
                        Source Meter Channel 'A','a' or 'B','b'
                    path : str
                        Where to save the file.
                    name : str
                        Name of the File. The name is Combinationof the function name and 
                        name that you give.
                        For Example: Coupling_Stability_Test.csv
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and SVG plot
                    of the measurmend will be created and saved in the given in 'path' folder.

                        ''')
                print('\n')
                Voltage = float(input('Voltage = '))
                Steps = float(input('Steps = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Time = float(input('Time = '))
                Channel = input('Channel = ')
                name = input('name = ')
                MZM_transfer_Keithley(Instrument ,Voltage ,Steps ,WaveLength, Time ,Channel ,path ,name)
                break
            
            
            
            elif FunctName == '9':
                print('''
    

                    Parameters
                    ----------
                    V_min : int/float
                        Minimal voltage in V
                    V_max : int/float
                        Maximal voltage
                    V_step : int/float
                        Voltage steps in V
                    wait : int
                        Deley time between measurments
                    Trace : str
                        Trace name from the Yokogawa. Could be: 
                                                                    Trace 1 = TRA
                                                                    Trace 2 = TRB
                                                                    Trace 3 = TRC
                                                                    Trace 4 = TRD
                                                                    Trace 5 = TRE
                                                                    Trace 6 = TRF
                                                                    Trace 7 = TRG
                    path : TYPE
                        DESCRIPTION.
                    name : TYPE
                        DESCRIPTION.
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and SVG plot
                    of the measurmend will be created and saved in the given in 'path' folder.
                
                    ''')
                print('\n')
                V_min = float(input('V_min = '))
                V_max = float(input('V_max = '))
                V_step = float(input('V_step = '))
                Time = float(input('Time = '))
                Trace = input('Trace = ')
                name = input('name = ')
                Voltage_OSA(Instrument, V_min, V_max, V_step,Time,Trace,path,name)
                break
            
            
            
            elif FunctName == '10':
                print('''
                    
                
                    Parameters
                    ----------
                    Instrument : list
                        List of Instruments
                    fmin : int/float
                        min CW frequency
                    fmax : int/float
                        min CW frequency
                    fstep : int/float
                        step CW frequency.
                    Power : int/float
                        Power in dBm.
                    unit : str
                        Frequency unit. 'HZ','kHz','MHz','GHz'
                    path : str
                        Path to where to save the data
                    name : str
                        Name of the data, parameter and svg files.
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and SVG plot
                    of the measurmend will be created and saved in the given in 'path' folder.
                
                    ''')
                print('\n')
                fmin = float(input('fmin = '))
                fmax = float(input('fmax = '))
                fstep = float(input('fstep = '))
                Power = float(input('Power = '))
                unit = (input('Frequency Unit = '))
                name = input('name = ')
                Sweep_CWF_VNA(Instrument, fmin, fmax, fstep, Power, unit, path, name)
                break
            
            
            elif FunctName == '11':
                print('''
                    
                
                    Parameters
                    ----------
                    Instrument : list
                        List of Instruments
                    fin : int/float
                        CW frequency.
                    Pmin : int/float
                        min Power in dBm.
                    Pmax : int/float
                        max Power in dBm.
                    Pstep : int/step
                        step Power in dBm.
                    unit : str
                        Frequency unit. 'HZ','kHz','MHz','GHz'
                    path : str
                        Path to where to save the data
                    name : str
                        Name of the data, parameter and svg files.
                
                    Returns
                    -------
                    None data will be returned. A TXT File with the Power Detector data will 
                    be created, CSV file whit  data will be created and SVG plot
                    of the measurmend will be created and saved in the given in 'path' folder.
                
                    ''')
                print('\n')
                fin = float(input('fin = '))
                Pmin = float(input('Pmin = '))
                Pmax = float(input('Pmax = '))
                Pstep = float(input('Pstep = '))
                unit = (input('Frequency Unit = '))
                name = input('name = ')
                Sweep_Power_VNA(Instrument, fin, Pmin, Pmax, Pstep, unit, path, name)
                break
            
            elif FunctName == '12':
                print('''
                      Parameters
                        ----------
                        Instrument : list
                            List of Instruments
                        f_opt : float
                            Frequency in Hz
                        f_min : float
                            Minimal frequency in GHz
                        f_max : float
                            Maximal freqeuncy in GHz
                        f_step : float
                            Step frequency in GHz
                        resBW : float
                            Resolution bandwidth in GHz
                        LaserChannel : int
                            Laser channel selected. It can be only 1 and 2 for LU1000 Laser Unit
                        LaserPower : int
                            Laser output power in dB.
            
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                    
                        Raises
                        ------
                        ValueError
                            DESCRIPTION.
                    
                        Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.
                      ''')
                print('\n')
                SA_f_min = float(input('Spectrum Analyzer min Freq [HZ] = '))
                SA_f_max = float(input('Spectrum Analyzer max Freq [HZ] = '))
                resBW = float(input('Freq Resolution bandwidth [HZ] = '))
                print('\n')
                print('Minimal Frequency = 191.1200 THz')
                print('Maximal Frequency = 196.2500 THz')
                print('\n')
                Laser_f_opt = float(input('Optical Freq of the laser [THz] = '))
                Laser_f_max = float(input('Max Freq of the laser [THz] = '))
                Step = int(input('Number of steps = '))
                LaserChannel = int(input('LaserChannel that will be moved  = '))
                print('\n')
                print('Minimal Laser Power = 8.8dBm')
                print('Maximal Laser Power = 17.8dBm')
                print('\n')
                LaserPower = float(input('LaserPower[dBm] = '))
                # SA_TraceNum = input('Speectral analyzer Trace selected for data extraction  = ')
                name = input('name = ')
                #Laserbeating_RF_Response_CoBrite(Instrument, f_min, f_max, f_opt, f_step, resBW, LaserChannel,LaserPower,SA_TraceNum,path,name)
                Laserbeating_RF_Response_CoBrite(Instrument, SA_f_min, SA_f_max, Laser_f_opt, Laser_f_max, Step, resBW, LaserChannel, LaserPower, path, name, SA_TraceNum = 1)
                break
            
            
            
            
            
            elif FunctName == '13':
                print('''
                      Parameters
                        ----------
                        Instrument : TYPE
                            DESCRIPTION.
                        Vvar_step : int/float
                            Step size Voltage for the array. (Vvar_min, Vvar_max, Vvar_step)
                        Vsa_min : int/float
                            Min voltage for source Meter
                        Vsa_max : int/float
                            Max voltage for the Source Meter
                        Vsa_step : int/float
                            Step size Voltage for the array. (Vsa_min, Vsa_max, Vsa_step)
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        Vth_min : int/float
                            Min Vth value to sweep the termal phase shifters
                        Vth_max : float/int
                            Max Vth value to sweep the termal phase shifters
                        Steps_Vth : float/int
                            Vth steps for the sweep. If Vth_max = 1 and Stteps_Vth = 0.1 => Vth = 0.1,0.2,0.3,...1
                        I_th_max : int/float
                            Max current that the Power supply can provide for the simulation. 
                        t_th : int/float
                            Sleep time between Vth Sweep steps. 1 or 2 secounds is ok 
                        Average_points_VNA : int
                            VNA Average points.
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                    
                    
                         Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.
                      ''')
                print('\n')
                # Vvar_min = float(input('Power Supply minimal voltage [V] = '))
                # Vvar_max = float(input('Power Supply maximal voltage [V] = '))
                # Vvar_step = float(input('Power Supply step voltage [V] = '))
                V_var = float(input('Varactor voltage [V] = '))
                Vsa_min = float(input('Source Meter minimal voltage [V] = '))
                Vsa_max = float(input('Source Meter maximal voltage [V] = '))
                Vsa_step = float(input('Source Meter step voltage [V] = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Vth_min = float(input('Min Vth for the Qadrature Point sweep [V] = '))
                Vth_max = float(input('Max Vth for the Qadrature Point sweep [V] = '))
                Steps_Vth = float(input('Vth steps [V] = '))
                I_th_max = float(input('I_th limit [A] = '))
                t_th = int(input('t_th [s] = '))
                Average_points_VNA = int(input('Average Points VNA = '))
                Channel = print('''
                                Power  Meter Channel A and Channel B are 
                                set as Channel A = Channel 1 and Channel 
                                B = Channel 2. So connect them as you wish
                                ''')
                name = input('name = ')
                LaserPower = float(input('Laser Power Signal IN= '))
                PowerCopIN = float(input('Laser Coupling Power IN = '))
                PowerCopOUT = float(input('Laser Coupling Power OUT = '))
                IL_GC = (PowerCopIN - PowerCopOUT) /2
                df =   pd.DataFrame({'Laser_Power_Signal_IN':[LaserPower], 'Laser_Coupling_Power_IN': [PowerCopIN], 'Laser_Coupling_Power_OUT': [PowerCopOUT], 'Inserion_Loss_per_GC':[IL_GC]})
                print(""""
                      #################### !!!! ####################
                          
                      Turn DeEmbeding on the VNA on!
                      Turn the Photodiode on! 
                      
                      
                      
                      #################### !!!! ####################
                      """)
                      
                Ask = input('Are the DeEmbeding and the Photodiode ON (Yes/No) = ')
                YesVec = ['Yes','yes','y','Y']
                NoVec = ['No','no','n','N']
                if Ask in YesVec:
                    with open(path + '/'+name+ '_Coupling'+'.txt', 'a') as f:
                        f.write('begin dscrdata')
                        f.write(" \n")
                        f.write("% ")
                        dfAsString = df.to_string(header=True, index=False)
                        f.write(dfAsString)
                        f.write(" \n")
                        f.write("END dscrdata")
                    Tobias_MZM_passive_Equalizer(Instrument, V_var, Vsa_min, Vsa_max, Vsa_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, Average_points_VNA, path, name)
                elif Ask in NoVec:
                    print("Check the Option again, and run the function one more time")
                else:
                    raise ValueError('Incorect Input. Try again later!')
                break
            
            
            
            
            
            
            
            elif FunctName == '14':
                print('''
                       Parameters
                        ----------
                        Instrument : TYPE
                            DESCRIPTION.
                        Vsa_min : int/float
                            Min voltage for source Meter
                        Vsa_max : int/float
                            Max voltage for the Source Meter
                        Vsa_step : int/float
                            Step size Voltage for the array. (Vsa_min, Vsa_max, Vsa_step)
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        Vth_min : int/float
                            Min Vth value to sweep the termal phase shifters
                        Vth_max : float/int
                            Max Vth value to sweep the termal phase shifters
                        Steps_Vth : float/int
                            Vth steps for the sweep. If Vth_max = 1 and Stteps_Vth = 0.1 => Vth = 0.1,0.2,0.3,...1
                        I_th_max : int/float
                            Max current that the Power supply can provide for the simulation. 
                        t_th : int/float
                            Sleep time between Vth Sweep steps. 1 or 2 secounds is ok 
                        Average_points_VNA : int
                            VNA Average points.
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                    
                    
                         Returns
                        -------
                        None data will be returned. A TXT File with the Power Detector data will 
                        be created, CSV file whit  data will be created and SVG plot
                        of the measurmend will be created and saved in the given in 'path' folder.
                      ''')
                print('\n')
                Vsa_min = float(input('Source Meter minimal voltage [V] = '))
                Vsa_max = float(input('Source Meter maximal voltage [V] = '))
                Vsa_step = float(input('Source Meter step voltage [V] = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Vth_min = float(input('Min Vth for the Qadrature Point Sweep [V] = '))
                Vth_max = float(input('Max Vth for the Qadrature Point Sweep [V] = '))
                Steps_Vth = float(input('Vth steps [V] = '))
                I_th_max = float(input('I_th limit [A] = '))
                t_th = int(input('t_th [s] = '))
                Average_points_VNA = int(input('Average Points VNA = '))
                name = input('name = ')
                LaserPower = float(input('Laser Power Signal IN = '))
                PowerCopIN = float(input('Laser Coupling Power IN = '))
                PowerCopOUT = float(input('Laser Coupling Power OUT = '))
                IL_GC = (PowerCopIN - PowerCopOUT) /2
                df2 =   pd.DataFrame({'Laser_Power_Signal_IN':[LaserPower], 'Laser_Coupling_Power_IN': [PowerCopIN], 'Laser_Coupling_Power_OUT': [PowerCopOUT], 'Inserion_Loss_per_GC':[IL_GC]})
                print(""""
                      #################### !!!! ####################
                          
                      Turn DeEmbeding on the VNA on!
                      Turn the Photodiode on! 
                      Source Meter Channel a is used! Please be sure 
                      that you connect the source Meter properly !
                      
                      
                      #################### !!!! ####################
                      """)
                      
                Ask = input('Are The DeEmbeding and the Photodiode ON (Yes/No) = ')
                
                YesVec = ['Yes','yes','YES','y','Y']
                NoVec = ['No','no','NO','n','N']
                if Ask in YesVec:
                    with open(path + '/'+name+ '_Coupling'+'.txt', 'a') as f:
                        f.write('begin dscrdata')
                        f.write(" \n")
                        f.write("% ")
                        dfAsString = df2.to_string(header=True, index=False)
                        f.write(dfAsString)
                        f.write(" \n")
                        f.write("END dscrdata")
                    Tobias_MZM_wo_Equalizer(Instrument, Vsa_min, Vsa_max, Vsa_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, Average_points_VNA, path, name)
                elif Ask in NoVec:
                    print("Check the Option again, and run the function one more time")
                else:
                    raise ValueError('Incorect Input. Try again later!')
                break
            
            
            elif FunctName == '15':
                print('''
                       Parameters
                        ----------
                        Instrument : TYPE
                            DESCRIPTION.
                        V_or_I_sweep: int/float
                            Define if voltage or current is swept in the SystemSourceMeter (V or I)
                        V_I_min : int/float
                            Min voltage [V] or current [mA] of the SystemSourceMeter
                        V_I_max : int/float
                            Max voltage [V] or current [mA] of the SystemSourceMeter
                        V_I_step : int/float
                            Step size voltage [V] or current [mA] of the array. (V_I_min, V_I_max, V_I_step)
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        Vth_min : int/float
                            Min Vth value to sweep the termal phase shifters
                        Vth_max : float/int
                            Max Vth value to sweep the termal phase shifters
                        Steps_Vth : float/int
                            Vth steps for the sweep. If Vth_max = 1 and Stteps_Vth = 0.1 => Vth = 0.1,0.2,0.3,...1
                        I_th_max : int/float
                            Max current that the Power supply can provide for the simulation. 
                        t_th : int/float
                            Sleep time between Vth Sweep steps. 1 or 2 secounds is ok 
                        V_Var : int/float
                            Voltage applied to the varactor (passive equalizer tuning) 
                        V_Peltier : int/float
                            Voltage applied to the Peltier element below the PCB and chip (cooling of the chip)
                        Average_points_VNA : int
                            VNA Average points.
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                        LaserPower : int/float
                            Power of the laser which is fed to the input signal grating coupler
                        PowerCopIN : int/float
                            Power of the laser which is fed to the input coupling grating coupler
                        PowerCopOUT : int/float
                            Power measured after the output coupling grating coupler
                         Returns
                        -------
                        None data will be returned. Measurement results (.txt, .csv, .svg, .snp) 
                        are saved in the given 'path' folder.
                      ''')
                print('\n')
                
                # Define vectors for possible answers
                YesVec = ['Yes','yes','YES','y','Y']
                NoVec = ['No','no','NO','n','N']
                Voltage_Ans_Vec = ['V','v','voltage','Voltage','0','Volt', 'volt', 'Vol', 'vol', 'U','u']
                Current_Ans_Vec = ['I','i','current','Current','1','Ampere','ampere','Amp','amp','C','c']
                Constant_Ans_vec = ['C','c','Constant','constant','Const','const', 'Const.', 'const.', 'Con', 'con', 'Con.', 'con.', '0']
                Sweep_Ans_vec = ['S','s','Sweep','sweep','Swe','swe', 'Swept', 'swept', 'Var', 'var', 'Variable', 'variable', 'Var.', 'var.', '1']
                
                
                # Define th PS source parameter
                Ask_V_or_I_sweep = input('voltage or current set/sweep in the SystemSourceMeter? (V/I) = ')                
                if Ask_V_or_I_sweep in Voltage_Ans_Vec:
                    V_or_I_sweep = float(0)
                elif Ask_V_or_I_sweep in Current_Ans_Vec:
                    V_or_I_sweep = float(1)
                else: 
                    print("Check the Option again, and run the function one more time")
                    break
                
                Ask_SystemSourcemeter_const_or_sweep = input('constant voltage/current or sweep in the SystemSourceMeter? (c/s) =')
                if Ask_SystemSourcemeter_const_or_sweep in Constant_Ans_vec:
                    SystemSourcemeter_const_or_sweep = float(0)
                elif Ask_SystemSourcemeter_const_or_sweep in Sweep_Ans_vec:
                    SystemSourcemeter_const_or_sweep = float(1)
                else: 
                    print("Check the Option again, and run the function one more time")
                    break
                
                if SystemSourcemeter_const_or_sweep == 0:
                    V_I_channel_A_const = float(input('SystemSourceMeter channel A voltage [V] or current [mA] = '))
                    V_I_channel_B_const = float(input('SystemSourceMeter channel B voltage [V] or current [mA] = '))
                    V_I_min = float(0)
                    V_I_max = float(0)
                    V_I_step = float(0)
                elif SystemSourcemeter_const_or_sweep == 1:
                    V_I_channel_A_const = float(0)
                    V_I_channel_B_const = float(0)
                    V_I_min = float(input('SystemSourceMeter minimal voltage [V] or current [mA] = '))
                    V_I_max = float(input('SystemSourceMeter maximal voltage [V] or current [mA] = '))
                    V_I_step = float(input('Source Meter step voltage [V] or current [mA] = '))
                else:
                    print("An error occured, please try again")
                    break
                
                # Define th PS source parameter
                Ask_th_PS_source_const_or_sweep = input('constant voltage/current or sweep in the phaseshifter power source? (c/s) =')
                
                if Ask_th_PS_source_const_or_sweep in Constant_Ans_vec:
                    th_PS_source_const_or_sweep = float(0)
                elif Ask_th_PS_source_const_or_sweep in Sweep_Ans_vec:
                    th_PS_source_const_or_sweep = float(1)
                else: 
                    print("Check the Option again, and run the function one more time")
                    break
                
                if th_PS_source_const_or_sweep == 0:
                    V_th_p_const = float(input('constant voltage at PS p [V] = '))
                    V_th_n_const = float(input('constant volatge at PS n [V] = '))
                    Vth_min = float(0)
                    Vth_max = float(0)
                    Steps_Vth = float(0)
                    t_th = int(input('t_th [s] = '))
                elif th_PS_source_const_or_sweep == 1:
                    V_th_p_const = float(0)
                    V_th_n_const = float(0)
                    Vth_min = float(input('Min Vth for the Qadrature Point Sweep [V] = '))
                    Vth_max = float(input('Max Vth for the Qadrature Point Sweep [V] = '))
                    Steps_Vth = float(input('Vth steps [V] = '))
                    t_th = int(input('t_th [s] = '))
                else:
                    print("An error occured, please try again")
                    break
                
                I_th_max = float(input('I_th limit [A] = '))
                
                
                
                
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                V_Var = float(input('Enter the varactor voltage [V] (manually set) = '))
                V_Peltier = float(input('Enter the Peltier element voltage [V] (manually set) = '))
                Average_points_VNA = int(input('Average Points VNA = '))
                name = input('name = ')
                LaserPower = float(input('Laser Power Signal IN = '))
                PowerCopIN = float(input('Laser Coupling Power IN = '))
                PowerCopOUT = float(input('Laser Coupling Power OUT = '))
                IL_GC = (PowerCopIN - PowerCopOUT) /2
                df2 =   pd.DataFrame({'Laser_Power_Signal_IN':[LaserPower], 'Laser_Coupling_Power_IN': [PowerCopIN], 'Laser_Coupling_Power_OUT': [PowerCopOUT], 'Inserion_Loss_per_GC':[IL_GC]})
                print(""""
                      #################### !!!! ####################
                          
                      Turn DeEmbeding on the VNA on!
                      Turn the Photodiode on! 
                      Source Meter is used! Please be sure 
                      that you connect the source Meter properly !
                      
                      
                      #################### !!!! ####################
                      """)
                Ask_PD = input('Is the Photodiode ON (Yes/No) = ')
                Ask_PD_deEmbedding = input('Is the Photodiode deembedded in the VNA (Yes/No) = ')
                Ask_Probes_deEmbedding = input('Are the probes deembedded in the VNA (Yes/No) = ')
                Ask_Layout_deEmbedding = input('Is the chip layout deembedded in the VNA (Yes/No) = ')
                Ask_electrical_gain = input('What is the gain of the electrical amplifier (if used)? ')
                Ask_optical_gain = input('What is the gain of the optical amplifier (if used)? ')
                Ask_comments = input('Are there any other comments that have to be saved? ')
                Ask_start = input('Start the measurement? (Yes/No) = ')
               
                path_Insertion_Loss_two_GC_in_dBm = path + '/Insertion_Loss_two_GC_in_dBm'
                if not os.path.exists(path_Insertion_Loss_two_GC_in_dBm):
                    os.makedirs(path_Insertion_Loss_two_GC_in_dBm)
                path_user_inputs = path + '/user_inputs'
                if not os.path.exists(path_user_inputs):
                    os.makedirs(path_user_inputs)
                    
                #save inputs into txt file    
                with open(path_user_inputs + '/'+name+ '_user_inputs'+'.txt', 'a') as file_1:
                        file_1.write("voltage or current sweep in the SystemSourceMeter? (V/I) = " + Ask_V_or_I_sweep + "\n")
                        file_1.write("constant voltage/current or sweep in the SystemSourceMeter? (c/s) = " + Ask_SystemSourcemeter_const_or_sweep + "\n")
                        file_1.write("SystemSourceMeter channel A voltage [V] or current [mA] = " + str(V_I_channel_A_const) + "\n")
                        file_1.write("SystemSourceMeter channel B voltage [V] or current [mA] = " + str(V_I_channel_B_const) + "\n") 
                        file_1.write("SystemSourceMeter minimal voltage [V] or current [mA] = " + str(V_I_min) + "\n")
                        file_1.write("SystemSourceMeter maximal voltage [V] or current [mA] = " + str(V_I_max) + "\n")
                        file_1.write("Source Meter step voltage [V] or current [mA] = " + str(V_I_step) + "\n")
                        file_1.write("constant voltage/current or sweep in the SystemSourceMeter? (c/s) = " + Ask_th_PS_source_const_or_sweep + "\n")
                        file_1.write("constant voltage at PS p [V] = " + str(V_th_p_const) + "\n")
                        file_1.write("constant voltage at PS n [V] = " + str(V_th_n_const) + "\n")
                        file_1.write("Min Vth for the Qadrature Point Sweep [V] = " + str(Vth_min) + "\n")
                        file_1.write("Max Vth for the Qadrature Point Sweep [V] = " + str(Vth_max) + "\n")
                        file_1.write("Vth steps [V] = " + str(Steps_Vth) + "\n")
                        file_1.write("t_th [s] = " + str(t_th) + "\n")
                        file_1.write("I_th limit [A] = " + str(I_th_max) + "\n")
                        file_1.write("Power Meter Wavelenth [nm] = " + str(WaveLength) + "\n")
                        file_1.write("Enter the varactor voltage [V] (manually set) = " + str(V_Var) + "\n")
                        file_1.write("Enter the Peltier element voltage [V] (manually set) = " + str(V_Peltier) + "\n")
                        file_1.write("Average Points VNA = " + str(Average_points_VNA) + "\n")
                        file_1.write("name = " + str(name) + "\n")
                        file_1.write("Laser Power Signal IN = " + str(LaserPower) + "\n")
                        file_1.write("Laser Coupling Power IN = " + str(PowerCopIN) + "\n")
                        file_1.write("Laser Coupling Power OUT = " + str(PowerCopOUT) + "\n")
                        file_1.write("Is the Photodiode ON (Yes/No) = " + str(Ask_PD) + "\n")
                        file_1.write("Is the Photodiode deembedded in the VNA (Yes/No) = " + str(Ask_PD_deEmbedding) + "\n")
                        file_1.write("Are the probes deembedded in the VNA (Yes/No) = " + str(Ask_Probes_deEmbedding) + "\n")
                        file_1.write("Is the chip layout deembedded in the VNA (Yes/No) = " + str(Ask_Layout_deEmbedding) + "\n")
                        file_1.write("What is the gain of the electrical amplifier (if used)? " + str(Ask_electrical_gain) + "\n")
                        file_1.write("What is the gain of the optical amplifier (if used)? " + str(Ask_optical_gain) + "\n")
                        file_1.write("Are there any other comments that have to be saved? " + str(Ask_comments) + "\n")
                        file_1.write("Start the measurement? (Yes/No) =  " + str(Ask_start) + "\n")
                        
                        
                
                if Ask_start in YesVec:
                    with open(path_Insertion_Loss_two_GC_in_dBm + '/'+name+ '_Coupling'+'.txt', 'a') as f:
                        f.write('begin dscrdata')
                        f.write(" \n")
                        f.write("% ")
                        dfAsString = df2.to_string(header=True, index=False)
                        f.write(dfAsString)
                        f.write(" \n")
                        f.write("END dscrdata")
                    Tobias_MZM_measurement(Instrument, V_or_I_sweep, SystemSourcemeter_const_or_sweep, V_I_channel_A_const, V_I_channel_B_const, V_I_min, V_I_max, V_I_step, th_PS_source_const_or_sweep, V_th_p_const, V_th_n_const, Vth_min, Vth_max, Steps_Vth, t_th, I_th_max, WaveLength, V_Var, V_Peltier, Average_points_VNA, path, name)
                elif Ask in NoVec:
                    print("Check the Option again, and run the function one more time")
                else:
                    raise ValueError('Incorect Input. Try again later!')
                break
            
            elif FunctName == '16':
                print('''
                       Parameters
                        ----------
                        Instrument : TYPE
                            DESCRIPTION.
                        V_or_I_sweep: int/float
                            Define if voltage or current is swept in the SystemSourceMeter (V or I)
                        V_I_min : int/float
                            Min voltage [V] or current [mA] of the SystemSourceMeter
                        V_I_max : int/float
                            Max voltage [V] or current [mA] of the SystemSourceMeter
                        V_I_step : int/float
                            Step size voltage [V] or current [mA] of the array. (V_I_min, V_I_max, V_I_step)
                        WaveLength : int
                            Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
                        Vth_min : int/float
                            Min Vth value to sweep the termal phase shifters
                        Vth_max : float/int
                            Max Vth value to sweep the termal phase shifters
                        Steps_Vth : float/int
                            Vth steps for the sweep. If Vth_max = 1 and Stteps_Vth = 0.1 => Vth = 0.1,0.2,0.3,...1
                        I_th_max : int/float
                            Max current that the Power supply can provide for the simulation. 
                        t_th : int/float
                            Sleep time between Vth Sweep steps. 1 or 2 secounds is ok 
                        V_Var : int/float
                            Voltage applied to the varactor (passive equalizer tuning) 
                        V_Peltier : int/float
                            Voltage applied to the Peltier element below the PCB and chip (cooling of the chip)
                        Average_points_VNA : int
                            VNA Average points.
                        path : str
                            Where to save the file.
                        name : str
                            Name of the File. The name is Combinationof the function name and 
                            name that you give.
                            For Example: Coupling_Stability_Test.csv
                        LaserPower : int/float
                            Power of the laser which is fed to the input signal grating coupler
                        PowerCopIN : int/float
                            Power of the laser which is fed to the input coupling grating coupler
                        PowerCopOUT : int/float
                            Power measured after the output coupling grating coupler
                         Returns
                        -------
                        None data will be returned. Measurement results (.txt, .csv, .svg, .snp) 
                        are saved in the given 'path' folder.
                      ''')
                print('\n')
                #V_or_I_sweep = float(input('voltage or current sweep in the SystemSourceMeter? (enter 0 for V or 1 for I) '))
                Ask_V_or_I_sweep = input('voltage or current sweep in the SystemSourceMeter? (V/I) = ')
                Voltage_Ans_Vec = ['V','v','voltage','Voltage','0','Volt', 'volt', 'Vol', 'vol']
                Current_Ans_Vec = ['I','i','current','Current','1','Ampere','ampere','Amp','amp']
                
                if Ask_V_or_I_sweep in Voltage_Ans_Vec:
                    V_or_I_sweep = float(0)
                elif Ask_V_or_I_sweep in Current_Ans_Vec:
                    V_or_I_sweep = float(1)
                else: 
                    print("Check the Option again, and run the function one more time")
                    break

                V_I_min = float(input('SystemSourceMeter minimal voltage [V] or current [mA] = '))
                V_I_max = float(input('SystemSourceMeter maximal voltage [V] or current [mA] = '))
                V_I_step = float(input('Source Meter step voltage [V] or current [mA] = '))
                WaveLength = float(input('Power Meter Wavelenth [nm] = '))
                Vth_min = float(input('Min Vth for the Qadrature Point Sweep [V] = '))
                Vth_max = float(input('Max Vth for the Qadrature Point Sweep [V] = '))
                Steps_Vth = float(input('Vth steps [V] = '))
                I_th_max = float(input('I_th limit [A] = '))
                t_th = int(input('t_th [s] = '))
                V_Var = float(input('Enter the varactor voltage [V] (manually set) = '))
                V_Peltier = float(input('Enter the Peltier element voltage [V] (manually set) = '))
                Average_points_VNA = int(input('Average Points VNA = '))
                name = input('name = ')
                LaserPower = float(input('Laser Power Signal IN = '))
                PowerCopIN = float(input('Laser Coupling Power IN = '))
                PowerCopOUT = float(input('Laser Coupling Power OUT = '))
                IL_GC = (PowerCopIN - PowerCopOUT) /2
                df2 =   pd.DataFrame({'Laser_Power_Signal_IN':[LaserPower], 'Laser_Coupling_Power_IN': [PowerCopIN], 'Laser_Coupling_Power_OUT': [PowerCopOUT], 'Inserion_Loss_per_GC':[IL_GC]})
                print(""""
                      #################### !!!! ####################
                          
                      Turn DeEmbeding on the VNA on!
                      Turn the Photodiode on! 
                      Source Meter is used! Please be sure 
                      that you connect the source Meter properly !
                      
                      
                      #################### !!!! ####################
                      """)
                Ask_PD = input('Is the Photodiode ON (Yes/No) = ')
                Ask_PD_deEmbedding = input('Is the Photodiode deembedded in the VNA (Yes/No) = ')
                Ask_Probes_deEmbedding = input('Are the probes deembedded in the VNA (Yes/No) = ')
                Ask_Layout_deEmbedding = input('Is the chip layout deembedded in the VNA (Yes/No) = ')
                Ask_electrical_gain = input('What is the gain of the electrical amplifier (if used)? ')
                Ask_optical_gain = input('What is the gain of the optical amplifier (if used)? ')
                Ask_comments = input('Are there any other comments that have to be saved? ')
                Ask_start = input('Start the measurement? (Yes/No) = ')
               
                path_Insertion_Loss_two_GC_in_dBm = path + '/Insertion_Loss_two_GC_in_dBm'
                if not os.path.exists(path_Insertion_Loss_two_GC_in_dBm):
                    os.makedirs(path_Insertion_Loss_two_GC_in_dBm)
                path_user_inputs = path + '/user_inputs'
                if not os.path.exists(path_user_inputs):
                    os.makedirs(path_user_inputs)
                    
                #save inputs into txt file    
                with open(path_user_inputs + '/'+name+ '_user_inputs'+'.txt', 'a') as file_1:
                        file_1.write("voltage or current sweep in the SystemSourceMeter? (V/I) = " + Ask_V_or_I_sweep + "\n")
                        file_1.write("SystemSourceMeter minimal voltage [V] or current [mA] = " + str(V_I_min) + "\n")
                        file_1.write("SystemSourceMeter maximal voltage [V] or current [mA] = " + str(V_I_max) + "\n")
                        file_1.write("Source Meter step voltage [V] or current [mA] = " + str(V_I_step) + "\n")
                        file_1.write("Power Meter Wavelenth [nm] = " + str(WaveLength) + "\n")
                        file_1.write("Min Vth for the Qadrature Point Sweep [V] = " + str(Vth_min) + "\n")
                        file_1.write("Max Vth for the Qadrature Point Sweep [V] = " + str(Vth_max) + "\n")
                        file_1.write("Vth steps [V] = " + str(Steps_Vth) + "\n")
                        file_1.write("I_th limit [A] = " + str(I_th_max) + "\n")
                        file_1.write("t_th [s] = " + str(t_th) + "\n")
                        file_1.write("Enter the varactor voltage [V] (manually set) = " + str(V_Var) + "\n")
                        file_1.write("Enter the Peltier element voltage [V] (manually set) = " + str(V_Peltier) + "\n")
                        file_1.write("Average Points VNA = " + str(Average_points_VNA) + "\n")
                        file_1.write("name = " + str(name) + "\n")
                        file_1.write("Laser Power Signal IN = " + str(LaserPower) + "\n")
                        file_1.write("Laser Coupling Power IN = " + str(PowerCopIN) + "\n")
                        file_1.write("Laser Coupling Power OUT = " + str(PowerCopOUT) + "\n")
                        file_1.write("Is the Photodiode ON (Yes/No) = " + str(Ask_PD) + "\n")
                        file_1.write("Is the Photodiode deembedded in the VNA (Yes/No) = " + str(Ask_PD_deEmbedding) + "\n")
                        file_1.write("Are the probes deembedded in the VNA (Yes/No) = " + str(Ask_Probes_deEmbedding) + "\n")
                        file_1.write("Is the chip layout deembedded in the VNA (Yes/No) = " + str(Ask_Layout_deEmbedding) + "\n")
                        file_1.write("What is the gain of the electrical amplifier (if used)? " + str(Ask_electrical_gain) + "\n")
                        file_1.write("What is the gain of the optical amplifier (if used)? " + str(Ask_optical_gain) + "\n")
                        file_1.write("Are there any other comments that have to be saved? " + str(Ask_comments) + "\n")
                        file_1.write("Start the measurement? (Yes/No) =  " + str(Ask_start) + "\n")
                        
                YesVec = ['Yes','yes','YES','y','Y']
                NoVec = ['No','no','NO','n','N']        
                
                if Ask_start in YesVec:
                    with open(path_Insertion_Loss_two_GC_in_dBm + '/'+name+ '_Coupling'+'.txt', 'a') as f:
                        f.write('begin dscrdata')
                        f.write(" \n")
                        f.write("% ")
                        dfAsString = df2.to_string(header=True, index=False)
                        f.write(dfAsString)
                        f.write(" \n")
                        f.write("END dscrdata")
                    Tobias_MZM_characteristic_in_dependency_of_thermal_biasing(Instrument, V_or_I_sweep, V_I_min, V_I_max, V_I_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, V_Var, V_Peltier, Average_points_VNA, path, name)
                elif Ask in NoVec:
                    print("Check the Option again, and run the function one more time")
                else:
                    raise ValueError('Incorect Input. Try again later!')
                break
            
                        
            elif FunctName == '0':
                __init__()
                FunctName = input('Function name: ')
            
    else:
        raise ValueError('Invalid Instrument Selected')
            
    
    