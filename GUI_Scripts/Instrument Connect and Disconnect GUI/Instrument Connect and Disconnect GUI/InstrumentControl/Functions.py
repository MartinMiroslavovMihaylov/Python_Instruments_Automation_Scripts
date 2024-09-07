# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 10:26:28 2022

@author: Martin.Mihaylov
"""

import numpy as np 
import pandas as pd
import tkinter as tk 
from tkinter import filedialog
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':22})
plt.rcParams["figure.figsize"] = (22,20)
import time as t
import sys
import pyvisa as visa
import os
from datetime import datetime 



# =============================================================================
# Loading Bar
# =============================================================================

def loadingBar(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+
                     str(int(total)).rjust(3,'0') +' [' + '='*int(percent/10)*
                     size + ' '*(10-int(percent/10))*size + ']')
    
def loadingBarTwo(count,total,size):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+
                     str(int(total)).rjust(3,'0') +' [' + '*'*int(percent/10)*
                     size + ' '*(10-int(percent/10))*size + ']')

# =============================================================================
# Definitions
# =============================================================================


def Coupling_Stability(Instrument,Time, WaveLength, path,name):
    '''
    

    Parameters
    ----------
    Time : int
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

    '''
    for i in range(len(Instrument)):
        if 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Meter
                                 """)
    
    name = 'Coupling_Stability_' + name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    secs = Time*60
    TimeVec = np.arange(1,int(secs+1),1)
    PowerVec = []
    Headaer = ['Time/s','Power/'+PM.ask_PowerUnits()]
    for i in range(secs):
        loadingBar(i,int(secs+1),1)
        t.sleep(1)
        PowerVec.append(PM.DefaultPowerMeas(WaveLength))
    PowerVec = np.array(PowerVec, dtype=np.float32)
    print('Max Power = ',max(PowerVec))
    print('Min Power = ',min(PowerVec))
    data = {Headaer[0]:TimeVec,Headaer[1]:PowerVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")
            
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")      

    
    
    
    
    
 
def MZM_transfer(Instrument ,Voltage ,Steps ,WaveLength ,wait ,path ,name ,Current):
    '''
    

    Parameters
    ----------
    Voltage : int/float
        Voltage in V
    Steps : int/float
        Voltage step in V
    wait : int
        Delay time between the sweeps
    WaveLength : int
        Wavelenght for the Power Meter. It is give in nm. For example WaveLength = 1310, WaveLength = 1550
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

    '''
    for i in range(len(Instrument)):
        if 'KA3005' in str(Instrument[i]).split('.'):
            PS = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Supply KA3005
                                     - Power Meter
                                 """)
    

    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    # VoltVec = np.arange(0,int(Voltage+Steps),Steps)
    StepnumVec = round((Voltage - 0) / Steps) + 1
    VoltVec = np.linspace(0, Voltage, StepnumVec)
    PowerVec = []
    if Current == False:
        Headaer = ['Voltage/V','Power/'+PM.ask_PowerUnits()]
        for i in range(len(VoltVec)):
            loadingBar(i+1,int(len(VoltVec)),1)
            PS.set_Volt(VoltVec[i])
            PS.set_Out('ON')
            t.sleep(wait)
            PowerVec.append(PM.DefaultPowerMeas(WaveLength))  
        PS.set_Volt(0)
        PS.set_Out('OFF')
        PowerVec = np.array(PowerVec, dtype=np.float32)
        data = {Headaer[0]:VoltVec,Headaer[1]:PowerVec}
        PD = pd.DataFrame(data,columns = Headaer)
        PD.to_csv(path +'/'+ name +'.csv',sep = ',')
        Headers,Data,Param = PM.DisplayParamDict('Power')
        ParamsInst = {}
        for i in range(len(Param)):
            ParamsInst[Param[i]] = Data[i]
        with open(path +'/'+ nameParam +'.txt', 'w') as file:
            for key, value in ParamsInst.items():
                file.write(key+"\t"+value+"\n")       
        plt.figure()
        plt.plot(PD[Headaer[0]],PD[Headaer[1]])
        plt.xlabel(Headaer[0])
        plt.ylabel(Headaer[1])
        plt.title(name)
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()  
        plt.savefig(path +'/'+ nameImage +".svg")           
    elif Current ==  True:
        Headaer = ['Voltage/V','Power/'+PM.ask_PowerUnits(),'Current/A']
        CurrentVec = []
        for i in range(len(VoltVec)):
            loadingBar(i+1,int(len(VoltVec)),1)
            PS.set_Volt(VoltVec[i])
            PS.set_Out('ON')
            t.sleep(wait)
            PowerVec.append(PM.DefaultPowerMeas(WaveLength))
            CurrentVec.append(PS.read_Amp())
        PS.set_Volt(0)
        PS.set_Out('OFF')
        PowerVec = np.array(PowerVec, dtype=np.float32)
        CurrentVec = np.array(CurrentVec, dtype=np.float32)
        data = {Headaer[0]:VoltVec,Headaer[1]:PowerVec,Headaer[2]:CurrentVec}
        PD = pd.DataFrame(data,columns = Headaer)
        PD.to_csv(path +'/'+ name +'.csv',sep = ',')
        Headers,Data,Param = PM.DisplayParamDict('Power')
        ParamsInst = {}
        for i in range(len(Param)):
            ParamsInst[Param[i]] = Data[i]
        with open(path +'/'+ nameParam +'.txt', 'w') as file:
            for key, value in ParamsInst.items():
                file.write(key+"\t"+value+"\n") 
        plt.figure()
        plt.plot(PD[Headaer[0]],PD[Headaer[1]])
        plt.xlabel(Headaer[0])
        plt.ylabel(Headaer[1])
        plt.title(name)
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()  
        plt.savefig(path +'/'+ nameImage +".svg") 

        plt.figure()
        plt.plot(PD[Headaer[0]],PD[Headaer[2]])
        plt.xlabel(Headaer[0])
        plt.ylabel(Headaer[2])
        plt.title(name)
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()  
        plt.savefig(path +'/'+ nameImage+'_Current' +".svg")

    




def GC_transfer(Instrument ,wmax ,wmin ,wstep ,LaserChannel ,LaserPower ,WaveLength ,wait ,path ,name):
    '''
    

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

    '''
    for i in range(len(Instrument)):
        if 'LU1000' in str(Instrument[i]).split('.'):
            LU = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Laser LU1000
                                     - Power Meter
                                 """)
    
    LU = Instrument[0]
    PM = Instrument[0]
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    LU.set_Power(LaserChannel,LaserPower)
    LU.set_LaserChannel(LaserChannel,0)
    LU.set_Gridspacing(LaserChannel,1)
    GridSpacing = LU.ask_Gridspacing(LaserChannel)
    fmin = 299792458/(wmax*1e-9)
    fmax =299792458/(wmin*1e-9)
    fmin = float('%.4f' % (fmin*1e-12))
    fmax = float('%.4f' % (fmax*1e-12))
    Vec = np.arange(fmin,fmax,GridSpacing*1e-4)
    FreqVec = []
    for i in range(len(Vec)):
        FreqVec.append(float('%.4f' % Vec[i]))
    WavelengeSweep = np.arange(wmin,wmax,wstep)
    StepVec = []
    for i in range(len(WavelengeSweep)):
        StepVec.append(float('%.4f' % ((299792458/(WavelengeSweep[i]*1e-9))*1e-12)))
    LU.set_Gridspacing(LaserChannel,1)
    PowerVec = []
    WaveVec = []
    Headaer = ['Wavelenght/m','Power/'+PM.ask_PowerUnits()]
    LU.set_LaserOutput(LaserChannel,'ON')
    t.sleep(wait)
    for i in range(len(StepVec)):
        loadingBar(i+1,int(len(StepVec)),1)
        if StepVec[i] in FreqVec:
            print(FreqVec.index(StepVec[i]))
            LU.set_LaserChannel(LaserChannel,FreqVec.index(StepVec[i]))
            print('Channel = ',LU.ask_LaserChannel(LaserChannel))
            print('Frequqency = ',LU.ask_Frequency(LaserChannel))
            print('Wavelenght = ',299792458/(LU.ask_Frequency(LaserChannel)*1e12),' m')
            WaveVec.append(299792458/(LU.ask_Frequency(LaserChannel)*1e12))
            print('#####################')
            t.sleep(10)
            PowerVec.append(PM.DefaultPowerMeas(WaveLength)) 
    LU.set_LaserOutput(LaserChannel,'OFF')
    PowerVec = np.array(PowerVec, dtype=np.float32)
    WaveVec = np.array(WaveVec, dtype = np.float32)
    data = {Headaer[0]:WaveVec,Headaer[1]:PowerVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['Laser Channel'] = str(LaserChannel)
    ParamsInst['Laser Power']  = str(LaserPower) 
    ParamsInst['Laser Power Unit'] =  str(LU.ask_Power(LaserChannel)) +' dBm'
    ParamsInst['Laser Grid spacing'] = str(LU.ask_Gridspacing(LaserChannel)*1e-4) + ' THz'
    ParamsInst['Laser min Wavelength'] = str(wmin) + ' nm'
    ParamsInst['Laser max Wavelength'] = str(wmax) + ' nm'
    ParamsInst['Laser step Wavelength'] = str(wstep) + ' nm'
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")       
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")      





        
    
def SG_SA_transfer(Instrument,fmin,fmax,Schritte,Pec,unit,path,name):
    
    for i in range(len(Instrument)):
        if 'MG3694C' in str(Instrument[i]).split('.'):
            SG = Instrument[i]
        elif 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Signal Generator
                                     - Spectrum Analyzer
                                     - Power Meter
                                 """)
    
  
    name = 'SG_SA_transfer_' + name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    SG.set_OutputPowerLevel(Pec)
    FreqVec = np.arange(fmin,fmax+Schritte,Schritte)
    #unitsSA = SA.DataY() #not ready waiting for Anritsu
    PowerVec = []
    Headaer = ['Frequency/'+unit,'Power/']#+unitsSA
    for i in range(0,len(FreqVec)):
        loadingBar(i,len(FreqVec),1)
        t.sleep(1)
        SG.set_output('ON')
        SG.set_freq_CW(FreqVec[i],unit)
        #PowerVec.append(SA.ExtractTtraceData()) #not ready waiting for anritsu
    SG.set_output('OFF')
    SG.set_OutputPowerLevel(0)
    PowerVec = np.array(PowerVec, dtype=np.float32)
    data = {Headaer[0]:FreqVec,Headaer[1]:PowerVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")       
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")      
    
    



def SG_SA_Linearing(Instrument,fin,Pmin,Pmax,Steps,unit,path,name):
    '''
    

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

    '''
    for i in range(len(Instrument)):
        if 'MG3694C' in str(Instrument[i]).split('.'):
            SG = Instrument[i]
        elif 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Signal Generator
                                     - Spectrum Analyzer
                                 """)

    
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    PowerVec = np.arange(Pmin,Pmax+Steps,Steps)
    FreqVec = np.arange(fin,fin*len(PowerVec),fin)
    PowerOverFreq = []
    SAFreqVec = []
    Headaer = ['Power Input/W','THD/%']
    SG.set_output('ON')
    SG.set_freq_CW(fin,unit)
    SA.set_freq_Stop(fin*4,unit.upper())
    SA.set_freq_Start(fin/2,unit.upper())
    for i in range(len(PowerVec)):
        SG.set_OutputPowerLevel(PowerVec[i])
        loadingBar(i,len(FreqVec),1)
        t.sleep(1)
        SA.set_ContinuousMeas('OFF')
        SA.set_MarkerPreset()
        SA.set_MaxPeak()
        PowerOverFreq.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_NextPeak()
        PowerOverFreq.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_NextPeak()
        PowerOverFreq.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_NextPeak()
        PowerOverFreq.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_MarkerPreset()
        SA.set_ContinuousMeas('ON')
    SG.set_output('OFF')
    SG.set_OutputPowerLevel(0)
    PowerOverFreq = np.array(PowerOverFreq, dtype=np.float32)
    SAFreqVec = np.array(SAFreqVec, dtype=np.float32)
    PowerVecWatt = (10**((PowerVec-30)/(10)))
    PowerWatt = (10**((PowerOverFreq-30)/(10)))


    #Calculation THD in %
    THD = []
    FreqDetected = []
    CompressVec = []
    for i in range(0,len(PowerWatt),4):
        THD.append(100*np.sqrt((PowerWatt[i+1]+PowerWatt[i+2]+PowerWatt[i+3])/PowerWatt[i]))
        FreqDetected.append(SAFreqVec[i])
        CompressVec.append(PowerWatt[i])
    
    
    #Calculate 1dB Copression 
    PowerdB = 10*np.log10(PowerVecWatt)
    PowerVecdB = 10*np.log10(CompressVec)
    OnedBCompOut = []
    OnedBCompIn = []
    OnrdBVec = []
    for i in range(len(CompressVec)):
        if (PowerdB[i] - PowerVecdB[i]) >= 1:
            OnrdBVec.append(PowerdB[i] - PowerVecdB[i])
        else:
            OnedBCompOut.append(PowerVecdB[i])
            OnedBCompIn.append(PowerdB[i]) 
            OnrdBVec.append(PowerdB[i] - PowerVecdB[i])
   

    #Write Data THB
    dataTHB = {Headaer[0]:CompressVec,Headaer[1]:THD}
    PD = pd.DataFrame(dataTHB,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")      
    
    plt.figure()
    plt.plot(OnedBCompOut,OnedBCompOut)
    plt.plot(OnedBCompIn,OnedBCompIn)
    plt.xlabel('Power Output/dB')
    plt.ylabel('Power Input/dB')
    plt.title('1dB Compression Point')
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage+ '_1dBComp' +".svg")      
    
    






def Laserbeating_RF_Response(Instrument, f_opt, f_min, f_max, f_step ,LaserChannel ,LaserPower , WaveLength ,Loops ,path,name):
    '''
    

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

    '''
    for i in range(len(Instrument)):
        if 'LU1000' in str(Instrument[i]).split('.'):
            LU = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Laser LU1000
                                     - Power Meter
                                     - Spectrum Analyzer
                                 """)
    

    
    #Choose which laser will be swept and which one will be const on f_opt.
    stLasers = [1,2]
    if LaserChannel in stLasers:
        if LaserChannel == 1: 
            LaserActive = 1
            LaserPassive = 2
        elif LaserChannel == 2:
             LaserActive = 2
             LaserPassive = 1
    else:
        raise ValueError('Not a Valid Laser Channel!!')
   
    
   
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    #Check the frquency for mod 100MHz
    if f_step%100e6 == 0 and f_min%100e6 == 0 and f_max%100e6 == 0:
        print('Frequency is a multiple of 100Hz')
    else:
        raise ValueError('Frequency is not multiple of 100Hz')

    #Convert the values in floats from GHz in THz to give to the lasers.
    f_min = float('%.4f' % (f_min*1e-12))
    f_max = float('%.4f' % (f_max*1e-12))
    f_opt = float('%.4f' % (f_opt*1e-12))
    f_step = float('%.4f' % (f_step*1e-12))
    minf = LU.ask_minFreqLaser(LaserActive)
    maxf = LU.ask_maxFreqLaser(LaserActive)
    if f_opt+f_max > maxf:
        raise ValueError('Max Frequency of the laser is '+str(LU.ask_maxFreqLaser(1)) + 'THz'+'.Given Max Frequqnecy is '+ str(f_opt+f_max)+'THz')
    else:
        pass
    
    #Set Laser Power,Grid to min and Channel to min freq
    LU.set_Power(LaserActive,LaserPower)
    LU.set_Power(LaserPassive,LaserPower)
    LU.set_Gridspacing(LaserActive,1)
    LU.set_Gridspacing(LaserPassive,1)
    LU.set_LaserChannel(LaserActive,1)
    LU.set_LaserChannel(LaserPassive,1)
    LU.set_Frequency(LaserActive,minf)
    LU.set_Frequency(LaserPassive,minf)
    
    #Move laser frequency to wanted freqe
    LU.set_Frequency(LaserActive,f_opt)
    LU.set_Frequency(LaserPassive,f_opt)
    
    
    FreqVec = np.arange(f_opt,f_opt+f_max,1*1e-4)
    
    Headaer = ['Frequency / Hz','Power/'+ PM.ask_PowerUnits()]
    PowerVec = []
    
    SA.set_freq_Stop(f_opt+f_max,'HZ')
    SA.set_freq_Start(f_opt,'HZ')
    PowerOverFreq = []
    SAFreqVec = []
    
    LU.set_Whispermode(LaserActive,'ON')
    LU.set_Whispermode(LaserPassive,'ON')
    LU.set_LaserOutput(LaserActive,'ON')
    LU.set_LaserOutput(LaserPassive,'ON')
    
    for i in range(len(FreqVec)):
        LU.set_Frequency(LaserActive,FreqVec[i])
        t.sleep(10)
        DummyPower = []
        DummyFreq = []
        for j in range(Loops):
            
            SA.set_MarkerPreset()
            SA.set_MaxPeak()
            DummyPower.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
            DummyFreq.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
            SA.set_ContinuousMeas('ON')
            t.sleep(1)
        SAFreqVec.append(float(DummyFreq[DummyPower.index(max(DummyPower))]))
        PowerOverFreq.append(float(max(DummyPower)))
        PowerVec.append(PM.DefaultPowerMeas(WaveLength))
    
    LU.set_Whispermode(LaserActive,'OFF')
    LU.set_Whispermode(LaserPassive,'OFF')
    LU.set_LaserOutput(LaserActive,'OFF')
    LU.set_LaserOutput(LaserPassive,'OFF')
    PowerVec = np.array(PowerVec, dtype=np.float32)
    PowerOverFreq = np.array(PowerOverFreq, dtype = np.float32)
    data = {Headaer[0]:FreqVec,Headaer[1]:PowerVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['Active Laser Channel'] = str(LaserActive)
    ParamsInst['Passive Laser Channel'] = str(LaserPassive)
    ParamsInst['Laser Power']  = str(LaserPower) 
    ParamsInst['Active and Passive Laser Power Unit'] =  str(LU.ask_Power(LaserActive)) +' dBm'
    ParamsInst['ActiveLaser Grid spacing'] = str(LU.ask_Gridspacing(LaserActive)*1e-4) + ' THz'
    ParamsInst['Passive Laser Grid spacing'] = str(LU.ask_Gridspacing(LaserPassive)*1e-4) + ' THz'
    ParamsInst['Laser min Wavelength'] = str(299792458/f_opt*1e12) + ' m'
    ParamsInst['Laser max Wavelength'] = str(299792458/(f_max+f_opt)*1e12) + ' m'
    ParamsInst['Laser step Wavelength'] = str(299792458/f_step*1e12) + ' m'
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n") 
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")      

    

    

    
    

def Device_characterization(Instrument ,V_min , V_max , V_step ,WaveLength, Channel ,path ,name):
    '''
    

    Parameters
    ----------
    V_min : int/float
        Minimal voltage in V
    V_max : int/float
        Maximum voltage in V
    V_step : int/float
        Step voltage in V
    Channel : str
        Source Meter Channel 'A','a' or 'B','b'
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
    be created, CSV file whit  data will be created and saved in the given in 'path' folder.

    '''
    for i in range(len(Instrument)):
        if 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Source Meter
                                     - Power Meter
                                     - Vector Network Analyzer
                                 """)
    

    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    PowerVec = []
    AmpVec = []
    Headaer = ['Voltage/V','Power/'+PM.ask_PowerUnits(),'Current/A']
    Vec = np.arange(V_min,V_max+V_step,V_step)
    KA.set_OutputSourceFunction(Channel,'volt')
    for i in range(len(Vec)):
        loadingBar(i+1,len(Vec),1)
        KA.set_Voltage(Channel,Vec[i])
        KA.set_SourceOutput(Channel,'ON')
        t.sleep(5)
        AmpVec.append(KA.ask_Current(Channel))
        PowerVec.append(PM.DefaultPowerMeas(WaveLength)) 
        VNA.SaveData(name+'_'+str(i),2)
        file = VNA.ask_TransferData(name+'_'+str(i),2)
        VNA.SaveTransferData(file,path,name+'_'+str(i),2)
        VNA.DeleteData(name+'_'+str(i),2)
        t.sleep(1)
    
    KA.set_SourceOutput(Channel,'OFF')
    PowerVec = np.array(PowerVec, dtype=np.float32)
    AmpVec = np.array(AmpVec, dtype=np.float32)
    VoltVec = np.array(Vec, dtype=np.float32)
    data = {Headaer[0]:VoltVec,Headaer[1]:PowerVec, Headaer[2]:AmpVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")   
    
   
    
    
    
    
    
    
def MZM_transfer_Keithley(Instrument ,Voltage ,Steps ,WaveLength, wait ,Channel ,path ,name):
    '''
    

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

    '''
    
    for i in range(len(Instrument)):
        if 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Source Meter
                                     - Power Meter
                                 """)


    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    VoltVec = np.arange(0,Voltage+Steps,Steps)
    PowerVec = []
    AmpVec = []
    Headaer = ['Voltage/V','Power/'+PM.ask_PowerUnits(),'Current/A']
    for i in range(len(VoltVec)):
        loadingBar(i+1,int(len(VoltVec)),1)
        KA.set_Voltage(Channel,VoltVec[i])
        KA.set_SourceOutput(Channel,'ON')
        t.sleep(wait)
        AmpVec.append(KA.ask_Current(Channel))
        PowerVec.append(PM.DefaultPowerMeas(WaveLength))
    
    KA.set_SourceOutput(Channel,'OFF')
    PowerVec = np.array(PowerVec, dtype=np.float32)
    AmpVec = np.array(AmpVec, dtype=np.float32)
    VoltVec = np.array(VoltVec, dtype=np.float32)
    data = {Headaer[0]:VoltVec,Headaer[1]:PowerVec,Headaer[2]:AmpVec}
    PD = pd.DataFrame(data,columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")      
           
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[1]])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")           
    
    plt.figure()
    plt.plot(PD[Headaer[2]],PD[Headaer[1]])
    plt.xlabel(Headaer[2])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage+ '_Current' +".svg") 






    
def Voltage_OSA(Instrument, V_min, V_max, V_step,wait,Trace,path,name):
    '''
    

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

    '''
    
    for i in range(len(Instrument)):
        if 'AQ6370D' in str(Instrument[i]).split('.'):
            OSA = Instrument[i]
        elif 'KA3005' in str(Instrument[i]).split('.'):
            PS = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Yokogawa Optical Spectrum Analyzer
                                     - Power Supply KA3005                
                                 """)

    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    VoltVec = np.arange(V_min,V_max+V_step,V_step)
    Headaer = ['Voltage/V','Power/'+OSA.ask_DisplayYUnit(),'Current/A']
    OSA.set_TraceActive('TRA')
    OSA.set_SweepMode('AUTO')
    OSA.StartSweep()
    t.sleep(10)
    OSA.set_SweepMode('REPeat')
    OSA.StartSweep()
    for i in range(len(VoltVec)):
        loadingBar(i+1,int(len(VoltVec)),1)
        PS.set_Volt(VoltVec[i])
        PS.set_Out('ON')
        t.sleep(wait)
        OSA.get_Data(Trace).to_csv(path +'/'+ name + '_Sweep_'+str(i)+'.csv')
        data = OSA.get_Data(Trace)
        fig = plt.figure()
        plt.plot(data[OSA.ask_UnitX()],data[OSA.ask_DisplayYUnit()])
        plt.xlabel('Wavelength/m')
        plt.ylabel(Headaer[1])
        plt.title(name)
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()  
        plt.savefig(path +'/'+ nameImage + '_'+str(i) +".svg") 
        plt.close(fig)
    PS.set_Out('OFF')
    PS.set_Volt(0)
    Headers,Data = OSA.get_ParamsOSA()
    ParamsInst = {}
    for i in range(len(Headers)):
        ParamsInst[Headers[i]] = Data[i]
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+str(value)+"\n")   
            








def Sweep_CWF_VNA(Instrument, fmin, fmax, fstep, Power, unit, path, name):
    '''
    

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

    '''

    for i in range(len(Instrument)):
        if 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        elif 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Vector Network Analyzer
                                     - Spectrum Analyzer                
                                 """)
    

    
    #Unit Correction for VNA
    corrFac = 1e0
    if unit.upper() == 'GHZ':
        corrFac = 1e9
        figUnit = 'GHz'
    elif unit.upper() == 'MHZ':
        corrFac = 1e6
        figUnit = 'MHz'
    elif unit.upper() == 'KHZ':
        corrFac = 1e3
        figUnit = 'kHz'
    else:
        figUnit = 'Hz'
        pass

    
    #define Variables and Names for data extraction later
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    PowerVec = []
    SAFreqVec = []
    Headaer = ['Frequency/Hz','Signal Analyzer Frequency/'+str(figUnit),'Power/dBm']
    
    #Main Loop
    FreqVec = np.arange(fmin,fmax+fstep,fstep)
    VNA.set_PowerOnPort(1,1,Power)
    SA.set_freq_Stop(fmax,unit.upper())
    SA.set_freq_Start(fmin,unit.upper())
    for i in range(len(FreqVec)):
        VNA.set_CWFreq(1,FreqVec[i]*corrFac)
        loadingBar(i,len(FreqVec),1)
        t.sleep(3)
        SA.set_ContinuousMeas('OFF')
        SA.set_MarkerPreset()
        SA.set_MaxPeak()
        PowerVec.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_ContinuousMeas('ON')
    VNA.RTL()      
    PowerVec = np.array(PowerVec, dtype=np.float32)
    SAFreqVec = np.array(SAFreqVec, dtype=np.float32)
    FreqVec = FreqVec*corrFac
    
    
    #Parameters for the Meas from SA and VNA in txt File 
    ParamsInst = {}
    ParamsInst['Min Frequency'] = str(fmin)
    ParamsInst['Max Frequency'] = str(fmax)
    ParamsInst['Step Frequency'] = str(fstep)
    ParamsInst['Output Power/dBm'] = str(Power)
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")
    
    
    
    
    #Write data 
    data = {Headaer[0]:SAFreqVec,Headaer[1]:FreqVec,Headaer[2]:PowerVec,}
    PD = pd.DataFrame(data, columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    
    
    #Plot Data
    plt.figure()
    plt.plot(PD[Headaer[0]],PD[Headaer[2]],label = 'Linear Curve')
    plt.plot(PD[Headaer[1]],PD[Headaer[2]],label = 'Measure Curve')
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.legend(loc = 'best')
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")   
    


def Sweep_Power_VNA(Instrument, fin, Pmin, Pmax, Pstep, unit, path, name):
    '''
    

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

    '''
    for i in range(len(Instrument)):
        if 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        elif 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Vector Network Analyzer
                                     - Spectrum Analyzer                
                                 """)

    
    
    #Unit Correction for VNA
    corrFac = 1e0
    figUnit = 'Hz'
    if unit.upper() == 'GHZ':
        corrFac = 1e9
        figUnit = 'GHz'
    elif unit.upper() == 'MHZ':
        corrFac = 1e6
        figUnit = 'MHz'
    elif unit.upper() == 'KHZ':
        corrFac = 1e3
        figUnit = 'kHz'
    else:
        pass
    
    #define Variables and Names for data extraction later
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    Headaer = ['Frequency/Hz','Signal Analyzer Power/dBm']
    
    #Main Loop
    PowerVec = np.arange(Pmin,Pmax,Pstep)
    SAFreqVec = []
    PowerMeasurment = []
    VNA.set_CWFreq(1,fin*corrFac)
    SA.set_CenterFreq(fin,unit.upper())
    for i in range(len(PowerVec)):
        VNA.set_PowerOnPort(1,1,PowerVec[i])
        loadingBar(i,len(PowerVec),1)
        t.sleep(3)
        SA.set_ContinuousMeas('OFF')
        SA.set_MarkerPreset()
        SA.set_MaxPeak()
        PowerMeasurment.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_ContinuousMeas('ON')
    PowerMeasurment = np.array(PowerMeasurment, dtype=np.float32)
    SAFreqVec = np.array(SAFreqVec, dtype=np.float32)
    VNA.RTL()
    
    #Parameters for the Meas from SA and VNA in txt File 
    ParamsInst = {}
    ParamsInst['Min Power/dBm'] = str(Pmin)
    ParamsInst['Max Power/dBm'] = str(Pmax)
    ParamsInst['Step Power/dBm'] = str(Pstep)
    ParamsInst['CW Frequency/Hz'] = str(fin)
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")
    
    
    
    
    #Write data 
    data = {Headaer[0]:SAFreqVec,Headaer[1]:PowerMeasurment,}
    PD = pd.DataFrame(data, columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    
    
    #Plot Data
    plt.figure()
    plt.plot(PD[Headaer[1]],PD[Headaer[1]],label = 'Measured Curve')
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.legend(loc = 'best')
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")   
    
    
def Laserbeating_RF_Response_CoBrite(Instrument, SA_f_min, SA_f_max, Laser_f_opt, Laser_f_max, Step, resBW, LaserChannel, LaserPower, path, name, SA_TraceNum = 1):
    '''
    

    Parameters
    ----------
    Instrument : list
        List of Instruments
    SA_f_min : float
        Spectrum Analyzer minimal frequency in Hz
    SA_f_max : float
        Spectrum Analyzer minimal frequency in Hz
    Laser_f_opt : float
        Optical frequency of the laser in THz. For Example:
            Laser_f_opt = 192.3421
    Laser_f_max : float
        Maximal frequency of the laser in THz. For Example:
            Laser_f_max = 192.3421
    Step : int
        Steps from Laser_f_opt to Laser_f_max. For Example:
            Steps = 2 , Laser_f_opt = 192.3000 Laser_f_max = 192.3400 ->
            -> (Laser_f_max- Laser_f_opt)/Steps
    resBW : float
        Resolution bandwidth in Hz
    LaserChannel : int
        Laser channel selected. It can be only 1 and 2 for CoBrite Laser Unit
    LaserPower : int
        Laser output power in dB.
    SA_TraceNum : int
        Spectrum Analyzer Active Trace. Per Defoult = 1
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


    '''
    for i in range(len(Instrument)):
        if 'MS2760A' in str(Instrument[i]).split('.'):
            SA = Instrument[i]
        elif 'CoBrite' in str(Instrument[i]).split('.'):
            CO = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - CoBrite Laser
                                     - Spectrum Analyzer                
                                 """)
    
    SA = Instrument[0]
    CO = Instrument[1]
    
    #Choose which laser will be swept and which one will be const on f_opt.
    stLasers = [1,2]
    if LaserChannel in stLasers:
        if LaserChannel == 1: 
            LaserActive = 1
            LaserPassive = 2
        elif LaserChannel == 2:
             LaserActive = 2
             LaserPassive = 1
    else:
        raise ValueError('Not a Valid Laser Channel!!')
   
    
   
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    #Set SA Range
    SA.set_freq_Stop(SA_f_max,'HZ')
    SA.set_freq_Start(SA_f_min,'HZ')
    SA.set_ResBwidth(resBW,'HZ')
    
    #Set Laser Powe to min and Channel to min freq. Calc Freq.
    LimDict = CO.ask_LaserLim(LaserActive)
    minFreqL = LimDict['Maximum Frequency']*1e12 
    
    
# =============================================================================
#     fSet = minFreqL + f_opt
#     GHz = int(str(fSet)[3:7])*1e-4
#     THz = int(str(fSet)[:3])
#     f_optTHz = THz+ GHz
#     
#     fSetM = minFreqL + f_max
#     MaxGHz = int(str(fSetM)[3:7])*1e-4
#     MaxTHz = int(str(fSetM)[:3])
#     f_maxTHz = MaxTHz+ MaxGHz
#     
#     fStep =  minFreqL + f_step
#     StepGHz = int(str(fStep)[3:7])*1e-4
#     StepTHz = int(str(fStep)[:3])
#     f_stepTHz = StepTHz + StepGHz
# =============================================================================

    CO.set_FreqTHz(LaserActive,Laser_f_opt)
    Dumpster = CO.read()
    CO.set_FreqTHz(LaserPassive,Laser_f_opt)
    Dumpster = CO.read()
    CO.set_Power(LaserActive,LaserPower)
    Dumpster = CO.read()
    CO.set_Power(LaserPassive,LaserPower)
    Dumpster = CO.read()
    
    



    FreqVec = np.linspace(SA_f_min,SA_f_max,int(SA.ask_DataPointCount())) # Frequency from Spectrum analyzer
    SetFreq = np.arange(Laser_f_opt,Laser_f_max ,(Laser_f_max-Laser_f_opt)/Step)        # Frequency for the Lasers
    
    
    Headaer = ['Frequency / Hz','Signal Analyzer Power/dBm']
    OutDict = {}
    OutDict[Headaer[0]] = FreqVec
    PowerMeasurment = []
    SAFreqVec = []
    
    #Activate the Laser Channels!!!
    CO.set_LaserOutput(LaserActive,'ON')
    Dumpster = CO.read()
    CO.set_LaserOutput(LaserPassive,'ON')
    Dumpster = CO.read()    
# =============================================================================
#     
#     for i in range(len(SetFreq)):
#         CO.set_FreqTHz(LaserActive,SetFreq[i])
#         Dumpster = CO.read()
#         loadingBar(i,len(SetFreq),1)
#         t.sleep(3)
#         data  = SA.ExtractTtraceData(SA_TraceNum)
#         Headaer.append('Power @ Freq = '+str(SetFreq[i]) + ' THz')
#         OutDict['Power @ Freq = '+str(SetFreq[i]) + ' THz'] = data
# 
# =============================================================================
    for i in range(len(SetFreq)):
        CO.set_FreqTHz(LaserActive,SetFreq[i])
        Dumpster = CO.read()
        loadingBar(i,len(SetFreq),1)
        t.sleep(3)
        SA.set_TraceType('MAX',SA_TraceNum)
        t.sleep(10)
        SA.set_ContinuousMeas('OFF')
        SA.set_MarkerPreset()
        SA.set_MaxPeak()
        PowerMeasurment.append(float(SA.ask_MarkerExcursion().split(',')[1].split(')')[0]))
        SAFreqVec.append(float(SA.ask_MarkerExcursion().split(',')[0].split('(')[1]))
        SA.set_ContinuousMeas('ON')
        SA.set_TraceType('NORM',SA_TraceNum)
        

    #Disable the Laser Channels!!!
    CO.set_LaserOutput(LaserActive,'OFF')
    Dumpster = CO.read()
    CO.set_LaserOutput(LaserPassive,'OFF')
    Dumpster = CO.read()
    
    PowerMeasurment = np.array(PowerMeasurment, dtype=np.float32)
    SAFreqVec = np.array(SAFreqVec, dtype=np.float32)
    

# =============================================================================
#     #Save data in txt and CSV
#     data = OutDict
#     PD = pd.DataFrame(data,columns = Headaer)
#     PD.to_csv(path +'/'+ name +'.csv',sep = ',')
# =============================================================================
    
    #Save data in txt and CSV
    data = {Headaer[0]:SAFreqVec,Headaer[1]:PowerMeasurment,}
    PD = pd.DataFrame(data, columns = Headaer)
    PD.to_csv(path +'/'+ name +'.csv',sep = ',')
    
    
    Laser_Config_Active_Chan = CO.ask_Configuration(LaserActive)
    Laser_Config_Passive_Chan = CO.ask_Configuration(LaserPassive)
    Spacer = {}
    Spacer['########################'] = ['########################']
    Laser_Config_Active_Chan.update(Spacer)
    Laser_Config_Active_Chan.update(Laser_Config_Passive_Chan)
    Laser_Config_Active_Chan.update(Spacer)
    Laser_Config_Active_Chan['Spectrum Analyzer max Frequency = '] = SA.ask_freq_Stop()
    Laser_Config_Active_Chan['Spectrum Analyzer min Frequency = '] = SA.ask_freq_Start()
    Laser_Config_Active_Chan['Spectrum Analyzer data Points = '] = float(SA.ask_DataPointCount())
    
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in Laser_Config_Active_Chan.items():
            file.write(key+"\t"+str(value)+"\n") 
            
            
    #Optional Plot Figure
    plt.figure()
    for i in range(len(SetFreq)):
       plt.plot(PD[Headaer[0]],PD['Power @ Freq = '+str(SetFreq[i]) + ' THz'])
    plt.xlabel(Headaer[0])
    plt.ylabel(Headaer[1])
    plt.title(name)
    plt.grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()  
    plt.savefig(path +'/'+ nameImage +".svg")   
    
    
    
    
    
def Tobias_MZM_passive_Equalizer(Instrument, V_var, Vsa_min, Vsa_max, Vsa_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, Average_points_VNA, path, name):
    """
    

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

        """
    for i in range(len(Instrument)):
        if 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        # elif 'KA3005' in str(Instrument[i]).split('.'):
        #     PS1 = Instrument[i]
        # elif 'KA3005p' in str(Instrument[i]).split('.'):
        #     PS2 = Instrument[i]
        # elif 'RD3005' in str(Instrument[i]).split('.'):
        #     PS3 = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Supply 
                                     - Source Meter
                                     - Power Meter
                                     - Vector Network Analyzer
       
                                    """)


    
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    
    
    #Define arrays
    # StepnumVar = round((Vvar_max - Vvar_min) / Vvar_step) + 1
    StepnumVec = round((Vsa_max - Vsa_min) / Vsa_step) + 1
    # Vvar_vec = np.linspace(Vvar_min, Vvar_max, StepnumVar)
    Vsa_vec = np.linspace(Vsa_min, Vsa_max, StepnumVec)
    Vsa_vec = Vsa_vec[::-1]
    idx = 0
    
    #Define the Header and dectionarys to save the data
    df =  pd.DataFrame({'Idx':['idx'],'Var Voltage/V':['V_var'], 'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A':['I_DC_A_PS'], 'Ias_Channel_B/A':['I_DC_B_PS'], 'Power/dBm':['P_opt_static'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
    data = pd.DataFrame({'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A':['I_DC_A_PS'], 'Ias_Channel_B/A':['I_DC_B_PS'], 'Power/dBm':['P_opt_static']})
    Sdata = pd.DataFrame({'Idx':['idx'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
    
    
    
    
    #Set Vth Vec
    Vth_Steps = round((Vth_max - Vth_min) / Steps_Vth) + 1
    VthVec = np.linspace(Vth_min, Vth_max, Vth_Steps)
    
    
    PowerVec_Vth = []
    Power_3db = []
    volt_3dB = []
    
    
    
    #Predefine some of the instruments 
    Channel1 = 'a' #Set Channel 1 as Channel A
    Channel2 = 'b' # Set Channel 2 as Channel B
    KA.set_OutputSourceFunction(Channel1,'volt')
    KA.set_OutputSourceFunction(Channel2,'volt')
    KA.set_AutoVoltageRange(Channel1, 'ON')
    KA.set_AutoVoltageRange(Channel2, 'ON')
    KA.set_Current(Channel1, 0)
    KA.set_Current(Channel2, 0)
    KA.set_Voltage(Channel1, 0)
    KA.set_Voltage(Channel2, 0)
    PS.set_Volt(0)
    PS.set_Out('ON')
    KA.set_SourceOutput(Channel1,'ON')
    KA.set_SourceOutput(Channel2,'ON')
    
    
    
    Dummy = np.ones(len(Vsa_vec))
    Vvar_vec = Dummy*V_var
    
    AmpVec1 = []
    AmpVec2 = []
    PowerVec = []
    volt_3dB = []
    Power_3db = []
    PowerVec_Vth = []
    S_Param_Names = []
    S_Param_Names_Path = []
    indexList = []
    PowerVec_Vth0 = []
    PowerVec_max = []
    Vth_max_vec_array = []
    Vth_0_vec = []
    idx_2 = 0 
    indexList2 = []
    
    for j in range(len(Vsa_vec)):
        loadingBar(j+1,int(len(Vsa_vec)),1)
        
        KA.set_Voltage(Channel1,Vsa_vec[j])
        KA.set_Voltage(Channel2,Vsa_vec[j])
        
        VthPopt = pd.DataFrame({'idx2':['idx2'],'Vth/V':['Vth/V'],'P_opt_@_Vth':['P_opt_@_Vth/'+PM.ask_PowerUnits()]})
        Vth3dB_Popt3dB = pd.DataFrame({'Idx':['Idx'],'Vth/V':['Vth/V'],'Power @ -3dB':['P_opt @ -3dB/'+PM.ask_PowerUnits()]})
        
        
        # Const Value for the Term.elements
        PS.set_Volt(Vth_min)
        PS.set_Amp(I_th_max)
        
        # save Popt @ Vth0
        PowerVec_Vth0.append(PM.DefaultPowerMeas(WaveLength))   # added by Tobias
        Vth_0_vec.append(Vth_min)                               # added by Tobias 
        
        
          
        idx_2 = 0 
        indexList2 = []
        for p in range(len(VthVec)):
            
            PS.set_Volt(VthVec[p])
            PowerVec_Vth.append(PM.DefaultPowerMeas(WaveLength))
            indexList2.append(idx_2)
            idx_2 += 1
        plt.figure()
        plt.plot(VthVec, PowerVec_Vth, color = 'green')
        plt.xlabel('$V_{th}$/V')
        plt.ylabel('$P_{Out}$/' + PM.ask_PowerUnits())
        plt.title('Power @ $V_{b}$ = ' + str(Vsa_vec[j]) + ', $V_{a}$ = '+ str(Vsa_vec[j]))
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()  
        plt.savefig(path +'/'+ nameImage + '_@_Voltage_psa,psb_'+ str(Vsa_vec[j]) +"_.svg") 
        plt.close()
        
        
        
        
        #Save data in dict and then in .txt File in ADS-txt Format
        PowerVec_Vth = np.array(PowerVec_Vth, dtype=np.float32) 
        data3 = pd.DataFrame({'idx2':indexList2, 'Vth/V':VthVec, 'P_opt_@_Vth':PowerVec_Vth})
        VthPopt = VthPopt.append(data3)
        
        with open(path + '/'+ 'Vth_@_Voltage_psa_'+ str(Vsa_vec[j])+'.txt', 'a') as f:
            f.write('begin dscrdata')
            f.write(" \n")
            f.write("% ")
            dfAsString = VthPopt.to_string(header=False, index=False)
            f.write(dfAsString)
            f.write(" \n")
            f.write("END dscrdata")
        
        
        
        #Find Vth and Popt @ -3dB
        d = np.vstack((VthVec, PowerVec_Vth)).T    
        Power_3db.append(max(PowerVec_Vth)-3)
        def find_Vth_at_Popt_3dB(array, value):
            array = np.asarray(array)
            idx_1 = (np.abs(array - value)).argmin()    # edited by Tobias
            idx_2 = idx_1.argmin()                      # added by Tobias
            return array[idx_2]                         # edited by Tobias
                
        k = find_Vth_at_Popt_3dB(PowerVec_Vth,Power_3db[j]) # find vth@ Popt-3db
        PowerVec_max.append(max(PowerVec_Vth)) #Save Popt max for ADS txt file
        
        # new code:
        Vth_max_vec_array_arbitrary_size = (d[:,0][d[:,1] == max(d[:,1])])      # added by Tobias
        Vth_max_vec_array.append(float(Vth_max_vec_array_arbitrary_size[0]))    # Save Vth@ Popt max for ADS txt file
        volt_3dB_arbitrary_size = (d[:,0][d[:,1] == k])                         # added by Tobias
        volt_3dB.append(float(volt_3dB_arbitrary_size[0]))                      # Find the nearest value of Vth@Popt-3dB
        
        Power_3db_array = np.array(Power_3db, dtype=np.float32)
        volt_3dB_array = np.array(volt_3dB, dtype=np.float32)
        Vth_max_vec = np.array(Vth_max_vec_array, dtype=np.float32)
        PowerVec_Vth = []
        
        #SET Vth @ V_3dB
        Vth_3dB = float(volt_3dB[j])
        PS.set_Volt(Vth_3dB)
        t.sleep(t_th)
        
        VNA.set_SetAverageState(1,'ON')
        VNA.set_AverageCount(1,Average_points_VNA)
        time = VNA.ask_SweepTime()
        t.sleep(time*5)
        AmpVec1.append(KA.ask_Current(Channel1))
        AmpVec2.append(KA.ask_Current(Channel2))
        PowerVec.append(PM.DefaultPowerMeas(WaveLength)) 
        VNA.SaveData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]), 4)
        file = VNA.ask_TransferData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)
        VNA.SaveTransferData(file, path, name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)
        VNA.DeleteData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)

        with open(path+'/'+name +'_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p', "r") as f:
            lines = f.readlines()
        
        with open(path+'/'+name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p', "w") as f:
            for i in range(1,len(lines)):
                f.write(lines[i])
        
    
        S_Param_Names.append(name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p')
        S_Param_Names_Path.append('"'+path+'/'+ name + '_S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p'+'"')
        indexList.append(idx)
        idx += 1
        t.sleep(1)
        
        
        # d = np.vstack((VthVec, PowerVec_Vth)).T    
        # Power_3db.append(max(PowerVec_Vth)-3)
        # volt_3dB.append(float(d[:,0][d[:,1] == max(d[:,1])] ))
        # Power_3db_array = np.array(Power_3db, dtype=np.float32)
        # volt_3dB_array = np.array(volt_3dB, dtype=np.float32)
        # PowerVec_Vth = []
        
        # #SET Vth @ V_3dB
        # PS.set_Volt(float(d[:,0][d[:,1] == max(d[:,1])] ))
        # t.sleep(t_th)
    

    
        
        
        # VNA.SaveData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
        # file = VNA.ask_TransferData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
        # VNA.SaveTransferData(file,path,name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
        # VNA.DeleteData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
        

    ValueVec = np.ones(len(Vsa_vec))*Vvar_vec[j]
    PowerVec = np.array(PowerVec, dtype=np.float32)
    df2 = pd.DataFrame({'Idx':indexList, 'Var Voltage/V': ValueVec, 'Vas/V': Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm': PowerVec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    data2 = pd.DataFrame({'Vas/V':Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm':PowerVec})
    Sdata2 = pd.DataFrame({'Idx':indexList, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    data = data.append(data2)
    df = df.append(df2)
    Sdata = Sdata.append(Sdata2)
    data4 = pd.DataFrame({'Idx':indexList,'Vth/V': volt_3dB_array, 'Power @ -3dB':Power_3db_array})
    Vth3dB_Popt3dB = Vth3dB_Popt3dB.append(data4)
    # data3 = {Headaer3[0]:Power_3db_array, Headaer3[1]:volt_3dB_array}
    # PJ = pd.DataFrame(data3,columns = Headaer3)
    # PJ.to_csv(path +'/'+'Vth_3dB_@_V_psb_psa_'+str(Vsa_vec[j]) +'_.csv',sep = ',')
        
        
        
        
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(df2['Vas/V'],df2['Ias_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax1.plot(df2['Vas/V'],df2['Ias_Channel_B/A'],linewidth=3.0, color = 'blue', label = 'Channel B')
    ax2.plot(df2['Vas/V'],df2['Power/dBm'],linewidth=3.0)
    ax1.set( ylabel = "$I_{Source Meter}$/A")
    ax1.legend(loc = 'best')
    ax2.set( ylabel = 'Power/dB')
    ax2.set( xlabel = "$V_{Source Meter}$/V")
    ax1.grid()
    ax2.grid()
    fig.suptitle("@ $V_{Var}$ = "+str(Vvar_vec[j])+" V")
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.savefig(path +'/'+ nameImage +'_@'+ str(Vvar_vec[j]) +".svg")   
    plt.close()
        
        
        
        

    #Main Loop
    # for i in range(len(Vvar_vec)):
    #     loadingBar(i+1,len(Vvar_vec),1)
    #     PS.set_Volt(Vvar_vec[i])
    #     AmpVec1 = []
    #     AmpVec2 = []
    #     PowerVec = []
    #     S_Param_Names = []
    #     S_Param_Names_Path = []
    #     indexList = []
        
    #     for j in range(len(Vsa_vec)):
    #         KA.set_Voltage(Channel1,Vsa_vec[j])
    #         KA.set_Voltage(Channel2,Vsa_vec[j])
            
    #         #Make the Vth adjustment
    #         PS.set_Volt(0)
    #         PS.set_Out('ON')
            
            
    #         Headaer2 = ['Vth/V','Power/'+PM.ask_PowerUnits()]
    #         Headaer3 = ['Power @ -3dB/'+PM.ask_PowerUnits(), 'Voltage @ -3dB/V']
            
    #         # Const Value for the Term.elements
    #         PS.set_Volt(Vth_0)
    #         PS.set_Amp(0.06)
        
        
    #         for p in range(len(VthVec)):
    #             loadingBar(p+1,int(len(VthVec)),1)
    #             PS.set_Volt(VthVec[p])
    #             t.sleep(5)
    #             PowerVec_Vth.append(PM.DefaultPowerMeas(WaveLength))
    #         PS.set_Volt(Vth_0)
    #         plt.figure()
    #         plt.plot(VthVec, d = np.vstack((VthVec, PowerVec_Vth)).T, color = 'green')
    #         plt.xlabel('$V_{th}$/V')
    #         plt.ylabel('$P_{Out}$/' + PM.ask_PowerUnits())
    #         plt.title('Power @ $V_{b}$ = ' + str(Vsa_vec[j]) + ', $V_{a}$ = '+ str(Vsa_vec[j]))
    #         plt.grid()
    #         figManager = plt.get_current_fig_manager()
    #         figManager.window.showMaximized()
    #         plt.show()  
    #         plt.savefig(path +'/'+ nameImage + '_@_Voltage_A,B_'+ str(Vsa_vec[j]) +"_.svg") 
            
            
            
    #         PowerVec_Vth = np.array(PowerVec_Vth, dtype=np.float32) 
    #         data2 = {Headaer2[0]:VthVec, Headaer2[1]:PowerVec_Vth}
    #         PG = pd.DataFrame(data2,columns = Headaer2)
    #         PG.to_csv(path +'/'+'Vth_@_Vb_und_Va_'+str(Vsa_vec[j]) +'_.csv',sep = ',')
            
            
        
    #         d = np.vstack((VthVec, PowerVec_Vth)).T    
    #         Power_3db.append(max(PowerVec_Vth)-3)
    #         volt_3dB.append(float(d[:,0][d[:,1] == max(d[:,1])] ))
    #         Power_3db = np.array(Power_3db, dtype=np.float32)
    #         volt_3dB = np.array(volt_3dB, dtype=np.float32)
    #         PowerVec_Vth = []
            
            
    
    #         PS.set_Volt(float(volt_3dB))
            
    #         VNA.set_SetAverageState(1,'ON')
    #         VNA.set_AverageCount(1,6)
    #         time = VNA.ask_SweepTime()
    #         t.sleep(time)
    #         AmpVec1.append(KA.ask_Current(Channel1))
    #         AmpVec2.append(KA.ask_Current(Channel1))
    #         PowerVec.append(PM.DefaultPowerMeas(WaveLength)) 
    #         VNA.SaveData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j]), 4)
    #         file = VNA.ask_TransferData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j]),4)
    #         VNA.SaveTransferData(file, path, name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j]),4)
    #         VNA.DeleteData(name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j]),4)
            
    #         # VNA.SaveData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
    #         # file = VNA.ask_TransferData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
    #         # VNA.SaveTransferData(file,path,name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
    #         # VNA.DeleteData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
            
            
    #         S_Param_Names.append(name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j])+'.s4p')
    #         S_Param_Names_Path.append('"'+path+'/'+name + '_S_Parameters_V_Var_'+str(Vvar_vec[i])+'__V_DC_'+str(Vsa_vec[j])+'.s4p'+'"')
    #         indexList.append(idx)
    #         idx += 1
    #         t.sleep(1)
    #     ValueVec = np.ones(len(Vsa_vec))*Vvar_vec[i]
    #     PowerVec = np.array(PowerVec, dtype=np.float32)
    #     df2 = pd.DataFrame({'Idx':indexList, 'Var Voltage/V': ValueVec, 'Vas/V': Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm': PowerVec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    #     data2 = pd.DataFrame({'Vas/V':Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm':PowerVec})
    #     Sdata2 = pd.DataFrame({'Idx':indexList, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    #     data = data.append(data2)
    #     df = df.append(df2)
    #     Sdata = Sdata.append(Sdata2)
    #     data3 = {Headaer3[0]:Power_3db, Headaer3[1]:volt_3dB}
    #     PJ = pd.DataFrame(data3,columns = Headaer3)
    #     PJ.to_csv(path +'/'+'Vth_3dB_@_Vb_und_Va_'+str(Vsa_vec[j]) +'_.csv',sep = ',')
        
        
        
        
    #     fig, (ax1, ax2) = plt.subplots(2)
    #     ax1.plot(df2['Vas/V'],df2['Ias_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
    #     ax1.plot(df2['Vas/V'],df2['Ias_Channel_B/A'],linewidth=3.0, color = 'blue', label = 'Channel B')
    #     ax2.plot(df2['Vas/V'],df2['Power/dBm'],linewidth=3.0)
    #     ax1.set( ylabel = "$I_{Source Meter}$/A")
    #     ax1.legend(loc = 'best')
    #     ax2.set( ylabel = 'Power/dB')
    #     ax2.set( xlabel = "$V_{Source Meter}$/V")
    #     ax1.grid()
    #     ax2.grid()
    #     fig.suptitle("@ $V_{Var}$ = "+str(Vvar_vec[i])+" V")
    #     figManager = plt.get_current_fig_manager()
    #     figManager.window.showMaximized()
    #     plt.savefig(path +'/'+ nameImage +'_@'+ str(Vvar_vec[i]) +".svg")   
    #     plt.close()
    
    

    #Shut the instruments down and save the csv   
    PS.set_Volt(0)
    PS.set_Out('OFF')
    VNA.RTL()
    KA.set_Voltage(Channel1, 0)
    KA.set_Voltage(Channel2, 0)
    KA.set_SourceOutput(Channel1,'OFF')
    KA.set_SourceOutput(Channel2,'OFF')
    df.to_csv(path +'/'+ name +'.csv',sep = ',', index=False)
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    ParamsInst['PowerSupply Current'] = 'A'
    ParamsInst['PowerSupply Voltage'] = 'V'
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")   
            
    with open(path + '/'+name+ '_tabula_voltage_current_power_path'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path + '/'+name+ '_tabula__V_Var_voltage_current_powers'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = data.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path + '/'+name+ '_tabula__V_Var_S_Parameters_names_path'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Sdata.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
        
    with open( path +'/'+'P_opt@3dB_Vth@3dB'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Vth3dB_Popt3dB.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
            
            
    
    
def Tobias_MZM_wo_Equalizer(Instrument, Vsa_min, Vsa_max, Vsa_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, Average_points_VNA, path, name):
    """
    

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

    """
    

    for i in range(len(Instrument)):
        if 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        elif 'KA3005p' in str(Instrument[i]).split('.'):
            PS = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Supply 
                                     - Source Meter
                                     - Power Meter
                                     - Vector Network Analyzer
                                 """)





    
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    
    
    #Define arrays
    StepnumVec = round((Vsa_max - Vsa_min) / Vsa_step) + 1
    Vsa_vec = np.linspace(Vsa_min, Vsa_max, StepnumVec)
    idx = 0
    idx_2 = 0                       # added by Tobias
    
    #Define the Header and dectionarys to save the data
    df =  pd.DataFrame({'Idx':['idx'],'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A': ['I_DC_A_PS'], 'P_opt_0/dBm':['P_opt_@_Vth_min'], 'P_opt_meas/dBm':['P_opt_meas'], 'P_opt_max/dBm':['P_opt_max'], 'P_opt_min/dBm':['P_opt_min'], 'V_th_0/V':['Vth_@_V_th_min'], 'V_th_meas/V':['Vth_meas'], 'V_th_maxP/V': ['Vth_max_@_Popt_max'], 'V_th_minP/V': ['Vth_@_Popt_min'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param'], 'path_P_opt_over_V_th':['path_Popt_over_Vth']}) # edited by Tobias
    data = pd.DataFrame({'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A':['I_DC_A_PS'], 'P_opt_meas/dBm':['P_opt_meas']}) # edited by Tobias
    Sdata = pd.DataFrame({'Idx':['idx'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
    
    
    
    
    #Find the Operation Point
    Vth_Steps = round((Vth_max - Vth_min) / Steps_Vth) + 1
    VthVec = np.linspace(Vth_min, Vth_max, Vth_Steps)
      
    
    
    #Predefine some of the instruments 
    Channel1 = 'a' #Set Channel 1 as Channel A
    KA.set_OutputSourceFunction(Channel1,'volt')
    KA.set_AutoVoltageRange(Channel1, 'ON')
    KA.set_Current(Channel1, 0)
    KA.set_Voltage(Channel1, 0)
    PS.set_Volt(0)
    PS.set_Out('ON')
    KA.set_SourceOutput(Channel1,'ON')
    
    
    
    AmpVec1 = []
    PowerVec_meas = []
    #volt_3dB_arbitrary_size = []                # added by Tobias 
    volt_3dB = []
    Vth_meas = []
    Vth_max_vec = []
    Vth_min_vec = [] 
    Vth_0_vec = []                              # added by Tobias                            # edited by Tobias
    #Vth_max_vec_array_arbitrary_size = []       # added by Tobias 
    #Vth_max_vec_array = []
    #Power_3db = []
    PowerVec_Vth = []
    PowerVec_max = []
    PowerVec_min = []
    PowerVec_Vth0 = []                          # added by Tobias
    S_Param_Names = []
    S_Param_Names_Path = []
    Vth_Popt_Names_PAth = []
    indexList = []
    indexList2 = []
    
    
    for j in range(len(Vsa_vec)):
        loadingBar(j+1,int(len(Vsa_vec)),1)
        KA.set_Voltage(Channel1,Vsa_vec[j])
       
        VthPopt = pd.DataFrame({'idx2':['idx2'],'Vth/V':['Vth/V'],'P_opt_@_Vth':['P_opt_@_Vth/'+PM.ask_PowerUnits()]})
        Vth3dB_Popt3dB = pd.DataFrame({'Idx':['Idx'],'Vth/V':['Vth/V'],'Power @ -3dB':['P_opt @ -3dB/'+PM.ask_PowerUnits()]})
        
        
        # Const Value for the Term.elements
        PS.set_Volt(Vth_min)
        PS.set_Amp(I_th_max)
        
        #TEMP: V_th0 & P_opt@V_th0 output
        # print("\n")
        # print("Vth_0")
        # print(Vth_min)
        # print("P_opt@V_th0")
        # print(PM.DefaultPowerMeas(WaveLength))
        
        
        # save Popt @ Vth0
        PowerVec_Vth0.append(PM.DefaultPowerMeas(WaveLength))   # added by Tobias
        Vth_0_vec.append(Vth_min)                               # added by Tobias 
        
        
        
        
        idx_2 = 0 
        indexList2 = []
        for p in range(len(VthVec)):
            # loadingBarTwo(p+1,int(len(VthVec)),1)
            PS.set_Volt(VthVec[p])
            t.sleep(t_th)                                       # edited by Tobias (pause before saving)
            PowerVec_Vth.append(PM.DefaultPowerMeas(WaveLength))
            indexList2.append(idx_2)
            idx_2 += 1
        plt.figure()
        plt.plot(VthVec, PowerVec_Vth, color = 'green')
        plt.xlabel('$V_{th}$/V')
        plt.ylabel('$P_{Out}$/' + PM.ask_PowerUnits())
        plt.title('Power @ $V_{b}$ = ' + str(Vsa_vec[j]) + ', $V_{a}$ = '+ str(Vsa_vec[j]))
        plt.grid()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()  
        plt.savefig(path +'/'+ nameImage + '_@_Voltage_psa'+ str(Vsa_vec[j]) +"_.svg") 
        plt.close()
        
        #TEMP: Plot all measured values for V_th & P_opt@V_th
        # print("VthVec")
        # print(VthVec)
        # print("PowerVec_Vth")
        # print(PowerVec_Vth)
        
        
        #Save data in dict and then in .txt File in ADS-txt Format
        PowerVec_Vth = np.array(PowerVec_Vth, dtype=np.float32) 
        data3 = pd.DataFrame({'idx2':indexList2, 'Vth/V':VthVec, 'P_opt_@_Vth':PowerVec_Vth})
        VthPopt = VthPopt.append(data3)
        
        with open(path + '/'+ 'Vth_@_Voltage_psa_'+ str(Vsa_vec[j])+'.txt', 'a') as f:
            f.write('begin dscrdata')
            f.write(" \n")
            f.write("% ")
            dfAsString = VthPopt.to_string(header=False, index=False)
            f.write(dfAsString)
            f.write(" \n")
            f.write("END dscrdata")
        
        #Define function to find Vth for a given P_opt value
        def find_nearest_Vth_and_P_opt_for_given_Popt_value(Vth_vec, Popt_vec, Popt_value):
            power_array = np.asarray(Popt_vec)
            voltage_array = np.asarray(Vth_vec)
            index = (np.abs(power_array - Popt_value)).argmin()                   
            V_th = voltage_array[index]  
            P_opt = power_array[index]                
            return [index, V_th, P_opt]
        
        # ### test environment ###
        # # Here a fixed vector is given to the "find_nearest_Vth_and_P_opt_for_given_Popt_value" function
        # # the vector contain two exactly same values which could be identified as the QP
        # # Thus, this test can be used to check correct functionlity of the "find_nearest_Vth_and_P_opt_for_given_Popt_value" function
        # VthVec_test = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1]
        # print("VthVec_test")
        # print(VthVec_test)
        # PowerVec_Vth_test = [-34.2821236, -34, -33, -34.2585678, -34.2530594, -33, -34.2272758, -34.1936111, -34.1745224, -34.1389275, -34.1242599, -34.0865402, -34.0559998, -34.0014305, -33.9488792, -33.9073334, -33.8489151, -33.7964401, -33.7437401, -33.694622, -33.6427193, -33.5910187, -33.5421638, -33.472393, -33.4169388, -33.3559494, -33.2971458, -33.272625, -33.185997, -33.1242638, -33.0659447, -33.0019341, -32.9487724, -32.9023857, -32.8681374, -32.8083305, -32.7595062, -32.7112274, -32.6671333, -32.6256218, -32.5869484, -32.5471611, -32.5155907, -32.485527, -32.464222, -32.4469719, -32.4286842, -32.40625, -32.3954659, -32.3777046, -30]
        # print("PowerVec_Vth_test")
        # print(PowerVec_Vth_test)
        # P_opt_max_test = max(PowerVec_Vth_test)
        # print("P_opt_max_test")
        # print(P_opt_max_test)
        # Power_3dB_ideal_test = P_opt_max_test-3
        # print("Power_3dB_ideal_test")
        # print(Power_3dB_ideal_test)
        # [idx_3dB_test, V_th_3dB_test, P_opt_3dB_test] = find_nearest_Vth_and_P_opt_for_given_Popt_value(VthVec_test, PowerVec_Vth_test, Power_3dB_ideal_test)
        # print("Test: index for Power_3dB")
        # print(idx_3dB_test)
        # print("Test: V_th @ Power_3dB found")
        # print(V_th_3dB_test)
        # print("Test: Power_3dB found")
        # print(P_opt_3dB_test)
        
        
        #Find P_opt_max
        P_opt_max = max(PowerVec_Vth)              #Save temporal Popt max for QP search
        
        #TEMP: Plot P_opt_max
        # print("P_opt_max")
        # print(P_opt_max)
        
        #Calculate V_th @ P_opt_max 
        [idx_max, V_th_maxP, P_opt_max] = find_nearest_Vth_and_P_opt_for_given_Popt_value(VthVec, PowerVec_Vth, P_opt_max)
        
        #TEMP: Plot V_th @ P_opt_max
        # print("V_th @ P_opt_max")
        # print(V_th_maxP)
        
        #Find P_opt_min
        P_opt_min = min(PowerVec_Vth)              #Save temporal Popt max for QP search
        
        #TEMP: Plot P_opt_min
        # print("P_opt_min")
        # print(P_opt_min)
        
        #Calculate V_th @ P_opt_max 
        [idx_min, V_th_minP, P_opt_min] = find_nearest_Vth_and_P_opt_for_given_Popt_value(VthVec, PowerVec_Vth, P_opt_min)
        
        #TEMP: Plot V_th @ P_opt_min
        # print("V_th @ P_opt_min")
        # print(V_th_minP)
        
        #Popt @ -3dB ideal
        Power_3dB_ideal_temp = P_opt_max-3
        
        #TEMP: Plot ideal Power_3dB
        # print("Power_3dB ideal")
        # print(Power_3dB_ideal_temp)
        
        #Calculate P_opt_3dB and V_th@P_opt_3dB
        [idx_3dB, V_th_3dB_found, P_opt_3db_found] = find_nearest_Vth_and_P_opt_for_given_Popt_value(VthVec, PowerVec_Vth, Power_3dB_ideal_temp)
        
        #TEMP: Plot found Power_3dB
        # print("index for Power_3dB")
        # print(idx_3dB)
        # print("V_th @ Power_3dB found")
        # print(V_th_3dB_found)
        # print("Power_3dB found")
        # print(P_opt_3db_found)
           
        
        Vth_meas = V_th_3dB_found
        
        
        #save results into the corresponding arrays (in correct data format)
        volt_3dB.append(float(V_th_3dB_found))
        volt_3dB_array = np.array(volt_3dB, dtype=np.float32)
        Vth_max_vec.append(float(V_th_maxP))
        Vth_max_vec = np.array(Vth_max_vec, dtype=np.float32)
        PowerVec_max.append(P_opt_max)
        PowerVec_max = np.array(PowerVec_max, dtype=np.float32)
        Vth_min_vec.append(float(V_th_minP))
        Vth_min_vec = np.array(Vth_min_vec, dtype=np.float32)
        PowerVec_min.append(P_opt_min)
        PowerVec_min = np.array(PowerVec_min, dtype=np.float32)                                   
        PowerVec_Vth = []
        
        #TEMP: debugging
        # print("length Vth_max_vec")
        # print(len(Vth_max_vec))
        # print("length PowerVec_max")
        # print(len(PowerVec_max))
        # print("length Vth_min_vec")
        # print(len(Vth_min_vec))
        # print("length PowerVec_min")
        # print(len(PowerVec_min))
        
        
        #SET Vth @ V_3dB
        #Vth_3dB = float(volt_3dB[j])
        #PS.set_Volt(Vth_3dB)
        PS.set_Volt(float(Vth_meas))
        
        # Wait for t_th seconds to let the thermal PS heat up and set teh phaseshift
        t.sleep(t_th)
        
        
        # Core measurements
        VNA.set_SetAverageState(1,'ON')
        VNA.set_AverageCount(1,Average_points_VNA)
        time = VNA.ask_SweepTime()
        t.sleep(time*5)
        AmpVec1.append(KA.ask_Current(Channel1))
        PowerVec_meas.append(PM.DefaultPowerMeas(WaveLength)) 
        VNA.SaveData(name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j]), 4)
        file = VNA.ask_TransferData(name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j]),4)
        VNA.SaveTransferData(file, path, name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j]),4)
        VNA.DeleteData(name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j]),4)

        with open(path+'/'+name +'_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j])+'.s4p', "r") as f:
            lines = f.readlines()
        
        with open(path+'/'+name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j])+'.s4p', "w") as f:
            for i in range(1,len(lines)):
                f.write(lines[i])
        
    
        S_Param_Names.append(name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j])+'.s4p')
        S_Param_Names_Path.append('"'+path+'/'+ name + '_S_Parameters_V_Var_'+'_Van_'+str(Vsa_vec[j])+'.s4p'+'"')
        Vth_Popt_Names_PAth.append('"'+path + '/'+ 'Vth_@_Voltage_psa_'+ str(Vsa_vec[j])+'.txt'+'"')
        indexList.append(idx)
        idx += 1
        t.sleep(1)
    PowerVec_Vth0 = np.array(PowerVec_Vth0, dtype=np.float32)  # added by Tobias
    Vth_0_vec = np.array(Vth_0_vec, dtype=np.float32)  # added by Tobias
    PowerVec_meas = np.array(PowerVec_meas, dtype=np.float32)
    
    # df2 = pd.DataFrame({'Idx':indexList,'Vas/V': Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'P_opt_meas/dBm': PowerVec_meas, 'P_opt_max/dBm': PowerVec_max, 'V_th_3db/V': Vth_3dB, 'V_th_maxP/V': Vth_max_vec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path, 'path_P_opt_over_V_th':Vth_Popt_Names_PAth})
    df2 = pd.DataFrame({'Idx':indexList,'Vas/V': Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'P_opt_0/dBm': PowerVec_Vth0, 'P_opt_meas/dBm': PowerVec_meas, 'P_opt_max/dBm': PowerVec_max, 'P_opt_min/dBm': PowerVec_min, 'V_th_0/V': Vth_0_vec, 'V_th_meas/V': Vth_meas, 'V_th_maxP/V': Vth_max_vec, 'V_th_minP/V': Vth_min_vec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path, 'path_P_opt_over_V_th':Vth_Popt_Names_PAth}) # edited by Tobias
    data2 = pd.DataFrame({'Vas/V':Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'P_opt_meas/dBm':PowerVec_meas})
    Sdata2 = pd.DataFrame({'Idx':indexList, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    data = data.append(data2)
    df = df.append(df2)
    Sdata = Sdata.append(Sdata2) 
    data4 = pd.DataFrame({'Idx':indexList,'Vth/V': volt_3dB_array, 'Power @ -3dB':PowerVec_meas})
    Vth3dB_Popt3dB = Vth3dB_Popt3dB.append(data4)
   
        
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(df2['Vas/V'],df2['Ias_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax2.plot(df2['Vas/V'],df2['P_opt_meas/dBm'],linewidth=3.0)
    ax1.set( ylabel = "$I_{Source Meter}$/A")
    ax1.legend(loc = 'best')
    ax2.set( ylabel = 'P_opt_meas/dBm')
    ax2.set( xlabel = "$V_{Source Meter}$/V")
    ax1.grid()
    ax2.grid()
    # fig.suptitle("@ $V_{TH}$ = "+str(Vth_3dB)+" V")
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.savefig(path +'/'+ nameImage +'_'+ str(j) +".svg")   
    plt.close()
        
        
    

    #Shut the instruments down and save the csv   
    PS.set_Volt(0)
    PS.set_Out('OFF')
    VNA.RTL()
    KA.set_Voltage(Channel1, 0)
    KA.set_SourceOutput(Channel1,'OFF')
    df.to_csv(path +'/'+ name +'.csv',sep = ',', index=False)
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    ParamsInst['PowerSupply Current'] = 'A'
    ParamsInst['PowerSupply Voltage'] = 'V'
    ParamsInst['VNA Center frequency Hz'] = str(VNA.ask_CenterFreq(1))
    ParamsInst['VNA CW frequency Hz'] = str(VNA.ask_CWFreq(1))
    ParamsInst['VNA CW averaging count'] = str(VNA.ask_AverageCount(1))
    ParamsInst['VNA IF bandwidth Hz'] = str(VNA.ask_ResolutionBW(1))
    with open(path +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")   
            
            
    #Save Results in ADS-txt Format        
    with open(path + '/'+name+ '_tabula_voltage_current_power_path'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path + '/'+name+ '_tabula__V_Var_voltage_current_powers'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = data.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path + '/'+name+ '_tabula__V_Var_S_Parameters_names_path'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Sdata.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open( path +'/'+'P_opt@3dB_Vth@3dB'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Vth3dB_Popt3dB.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
            
########################################################
##################### new function #####################
########################################################  
def Tobias_MZM_measurement(Instrument, V_or_I_sweep, SystemSourcemeter_const_or_sweep, V_I_channel_A_const, V_I_channel_B_const, V_I_min, V_I_max, V_I_step, th_PS_source_const_or_sweep, V_th_p_const, V_th_n_const, Vth_min, Vth_max, Steps_Vth, t_th, I_th_max, WaveLength, V_Var, V_Peltier, Average_points_VNA, path, name):
    """
    

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

    """
    
    temp = 1
    
    #print("len(Instrument)")
    #print(len(Instrument)) 
    
    # working_directory = os.getcwd
    # print("Current working directory: {0}".format(working_directory))
    # print("Current working directory:")
    # print(working_directory)
    
    now = datetime.now()
    date_and_time_start_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Measurement started at:", date_and_time_start_string)
    
    
    # Create folders in which the files are to be saved
    path_Backup_tabular = path + '/Backup_tabular'
    if not os.path.exists(path_Backup_tabular):
        os.makedirs(path_Backup_tabular)
    path_CSV_summary = path + '/CSV_summary'
    if not os.path.exists(path_CSV_summary):
        os.makedirs(path_CSV_summary)
    path_Parameters = path + '/Parameters'
    if not os.path.exists(path_Parameters):
        os.makedirs(path_Parameters)
    path_Quadrature_points = path + '/Quadrature_points'
    if not os.path.exists(path_Quadrature_points):
        os.makedirs(path_Quadrature_points)
    path_S_Param = path + '/S_Param'
    if not os.path.exists(path_S_Param):
        os.makedirs(path_S_Param)
    path_SVG_V_th_sweep = path + '/SVG_V_th_sweep'
    if not os.path.exists(path_SVG_V_th_sweep):
        os.makedirs(path_SVG_V_th_sweep)
    path_Tabular_idx_voltages_currents_powers_paths = path + '/Tabular_idx_voltages_currents_powers_paths'
    if not os.path.exists(path_Tabular_idx_voltages_currents_powers_paths):
        os.makedirs(path_Tabular_idx_voltages_currents_powers_paths)
    path_TXT_V_th_sweep = path + '/TXT_V_th_sweep'
    if not os.path.exists(path_TXT_V_th_sweep):
        os.makedirs(path_TXT_V_th_sweep)
    path_plot_SystemSourceMeter = path + '/plot_SystemSourceMeter'
    if not os.path.exists(path_plot_SystemSourceMeter):
        os.makedirs(path_plot_SystemSourceMeter)    
    path_TXT_measurement_step = path + '/TXT_measurement_step'
    if not os.path.exists(path_TXT_measurement_step):
        os.makedirs(path_TXT_measurement_step) 
       

    for i in range(len(Instrument)):
        # print("i")
        # print(i)
        # print("str(Instrument[i]).split('.')")
        # print(str(Instrument[i]).split('.'))
        if 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        elif 'KA3005p' in str(Instrument[i]).split('.'):
            # print("temp")
            # print(temp) 
            if temp == 1:
                # print("set PS_1")
                PS_1 = Instrument[i]
                # print("set temp = 2")
                temp = 2
            else:
                print("set PS_2")
                PS_2 = Instrument[i]
        elif 'RD3005' in str(Instrument[i]).split('.'):
            # print("temp")
            # print(temp) 
            if temp == 1:
                # print("set PS_1")
                PS_1 = Instrument[i]
                # print("set temp = 2")
                temp = 2
            else:
                # print("set PS_2")
                PS_2 = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Supply 
                                     - Source Meter
                                     - Power Meter
                                     - Vector Network Analyzer
                                 """)
                                

    time_vec = []
    V_Var_vec = []
    V_Peltier_vec = []
    V_th_p_3dB_vec = []
    V_th_n_3dB_vec = []
    V_th_p_meas = []
    V_th_p_minP_vec = []
    V_th_n_minP_vec = []
    V_th_p_maxP_vec = []
    V_th_n_maxP_vec = []
    V_th_min_vec = []
    V_th_max_vec = []
    PowerVec_meas = []
    PowerVec_max = []
    PowerVec_min = []
    PowerVec_Vthmin = []
    S_Param_Names = []
    S_Param_Names_Path = []
    Vth_Popt_Names_Path = []
    indexList = []
    SystemSourceMeter_Current_A = []
    SystemSourceMeter_Voltage_A = []
    SystemSourceMeter_Current_B = []
    SystemSourceMeter_Voltage_B = []
    
    
    
    
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    
    #Define vector to set the SystemSourceMeter (PS biasing)
    if SystemSourcemeter_const_or_sweep == 0:
        # create an one element vector (required for sweep)
        StepnumVec = 1
        SystemSourceMeter_vec = []
        SystemSourceMeter_vec.append(0)
    elif SystemSourcemeter_const_or_sweep == 1:
        StepnumVec = round((V_I_max - V_I_min) / V_I_step) + 1
        SystemSourceMeter_vec  = np.linspace(V_I_min, V_I_max, StepnumVec)
    else:
        print("An error occured: SystemSourcemeter_const_or_sweep was not set to 0 or 1, SystemSourceMeter is set to be constant \n")
        # create an one element vector (required for sweep)
        StepnumVec = 1
        SystemSourceMeter_vec = []
        SystemSourceMeter_vec.append(0)
        
    
    #Define vector to set the power supplies (setting th. PS/ sweeping th. PS and finding QP)
    if th_PS_source_const_or_sweep == 0:
        Vth_Steps = 1
        VthVec  = 0
    elif th_PS_source_const_or_sweep == 1:
        Vth_Steps = round((Vth_max - Vth_min) / Steps_Vth) + 1
        VthVec = np.linspace(Vth_min, Vth_max, Vth_Steps)
    else:
        print("An error occured: th_PS_source_const_or_sweep was not set to 0 or 1 \n")
        Vth_Steps = 1
        VthVec  = 0
      
    
    
    
    idx = 0
    idx_2 = 0 
    indexList2 = []                     
  
    
    #Define the Header and dectionarys to save the data
    df =  pd.DataFrame({'Idx':['idx'], 'V_Peltier':['V_Peltier'], 'V_Var':['V_Var'], 'V_SSM_Channel_A/V':['V_DC_PS_A'], 'I_SSM_Channel_A/A': ['I_DC_PS_A'], 'V_SSM_Channel_B/V':['V_DC_PS_B'], 'I_SSM_Channel_B/A': ['I_DC_PS_B'], 'P_opt_0/dBm':['P_opt_@_Vth_min'], 'P_opt_meas/dBm':['P_opt_meas'], 'P_opt_max/dBm':['P_opt_max'], 'P_opt_min/dBm':['P_opt_min'], 'V_th_min/V':['V_th_min'], 'V_th_max/V':['V_th_max'], 'V_th_p_meas/V':['Vth_p_meas'], 'V_th_n_meas/V':['Vth_n_meas'], 'V_th_p_maxP/V': ['Vth_p_@_Popt_max'], 'V_th_n_maxP/V': ['Vth_n_@_Popt_max'], 'V_th_p_minP/V': ['Vth_p_@_Popt_min'], 'V_th_n_minP/V': ['Vth_n_@_Popt_min'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param'], 'path_P_opt_over_V_th':['path_Popt_over_Vth']})
    #data = pd.DataFrame({'V_SSM_Channel_A/V':['V_DC_PS_A'], 'I_SSM_Channel_A/A': ['I_DC_PS_A'], 'V_SSM_Channel_B/V':['V_DC_PS_B'], 'I_SSM_Channel_B/A': ['I_DC_PS_B'], 'P_opt_meas/dBm':['P_opt_meas']})
    data = pd.DataFrame({'V_SSM_Channel_A/V':['V_DC_PS_A'], 'I_SSM_Channel_A/A': ['I_DC_PS_A'], 'V_SSM_Channel_B/V':['V_DC_PS_B'], 'I_SSM_Channel_B/A': ['I_DC_PS_B'], 'P_opt_meas/dBm':['P_opt_meas'], 'time':['time_meas']})
    Sdata = pd.DataFrame({'Idx':['idx'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
    
    
    

    
    
    #Predefine the SystemSourcemeter 
    Channel1 = 'a' #Set Channel 1 as Channel A
    Channel2 = 'b' #Set Channel 2 as Channel B
    if V_or_I_sweep == 0:
        KA.set_OutputSourceFunction(Channel1,'volt')
        KA.set_OutputSourceFunction(Channel2,'volt')
        KA.set_AutoVoltageRange(Channel1, 'ON')
        KA.set_AutoVoltageRange(Channel2, 'ON')
    elif   V_or_I_sweep == 1:  
        KA.set_OutputSourceFunction(Channel1,'amp')
        KA.set_OutputSourceFunction(Channel2,'amp')
        KA.set_AutoCurrentRange(Channel1, 'ON')
        KA.set_AutoCurrentRange(Channel2, 'ON')
    else:
        print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
        KA.set_OutputSourceFunction(Channel1,'volt')
        KA.set_OutputSourceFunction(Channel2,'volt')
        KA.set_AutoVoltageRange(Channel1, 'ON')
        KA.set_AutoVoltageRange(Channel2, 'ON')
    KA.set_Current(Channel1, 0)
    KA.set_Voltage(Channel1, 0)
    KA.set_Current(Channel2, 0)
    KA.set_Voltage(Channel2, 0)
    KA.set_SourceOutput(Channel1,'ON')
    KA.set_SourceOutput(Channel2,'ON')
    
    #Predefine the power sources 
    PS_1.set_Volt(0)
    PS_1.set_Out('ON')
    PS_2.set_Volt(0)
    PS_2.set_Out('ON')
    
    # set SystemSourceMeter either to current or voltage sweep (according to user input)
    if SystemSourcemeter_const_or_sweep == 0:
        if V_or_I_sweep == 0:
            # set to constant voltage
            SystemSourceMeter_Voltage_A.append(V_I_channel_A_const)
            SystemSourceMeter_Voltage_B.append(V_I_channel_B_const)
        elif   V_or_I_sweep == 1:
            # set to constant current
            SystemSourceMeter_Voltage_A.append(0.001*V_I_channel_A_const)   # conversion to mA
            SystemSourceMeter_Current_B.append(0.001*V_I_channel_B_const)   # conversion to mA
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            SystemSourceMeter_Voltage_A.append(V_I_channel_A_const)
            SystemSourceMeter_Voltage_B.append(V_I_channel_B_const)
    elif SystemSourcemeter_const_or_sweep == 1:
        if V_or_I_sweep == 0:
            # set to voltage sweep
            SystemSourceMeter_Voltage_A = SystemSourceMeter_vec
            SystemSourceMeter_Voltage_B = SystemSourceMeter_vec
        elif   V_or_I_sweep == 1:  
            # set to current sweep
            SystemSourceMeter_Current_A = 0.001*SystemSourceMeter_vec   # conversion to mA
            SystemSourceMeter_Current_B = 0.001*SystemSourceMeter_vec   # conversion to mA
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            SystemSourceMeter_Voltage_A = SystemSourceMeter_vec
            SystemSourceMeter_Voltage_B = SystemSourceMeter_vec
    else:
        print("An error occured: SystemSourcemeter_const_or_sweep was not set to 0 or 1, SystemSourceMeter is set to be constant \n")
        
    

    
    
    
    #################################################
    ############# start measurement #################
    ################################################# 
    for j in range(len(SystemSourceMeter_vec)):
        loadingBar(j+1,int(len(SystemSourceMeter_vec)),1)
        
        
        # set SystemSourceMeter
        if V_or_I_sweep == 0:
            KA.set_Voltage(Channel1,SystemSourceMeter_Voltage_A[j])
            KA.set_Voltage(Channel2,SystemSourceMeter_Voltage_B[j])
        elif   V_or_I_sweep == 1:  
            KA.set_Current(Channel1,SystemSourceMeter_Current_A[j])
            KA.set_Current(Channel2,SystemSourceMeter_Current_B[j])
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            KA.set_Voltage(Channel1,SystemSourceMeter_Voltage_A[j])
            KA.set_Voltage(Channel2,SystemSourceMeter_Voltage_B[j])
        
        
            
        # files are given different names, depending on type of sweeping (voltage or current sweep)
        if V_or_I_sweep == 0:
            # voltage set, current measured
            file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_Voltage_A[j])+'V__V_B_'+str(SystemSourceMeter_Voltage_B[j])+'V'
        elif   V_or_I_sweep == 1:
            # current set, voltage measured
            file_name_V_or_I = '_I_A_'+str(SystemSourceMeter_Current_A[j])+'mA__I_B_'+str(SystemSourceMeter_Current_B[j])+'mA'
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            # voltage set, current measured
            file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_Voltage_A[j])+'V__V_B_'+str(SystemSourceMeter_Voltage_B[j])+'V'
        
               
        
       
         
        V_th_Popt = pd.DataFrame({'idx2':['idx2'],'V_Peltier':['V_Peltier'],'V_Var':['V_Var'],'V_th_p/V':['V_th_p/V'],'V_th_n/V':['V_th_n/V'],'P_opt_@_Vth':['P_opt_@_Vth/'+PM.ask_PowerUnits()]})
        Vth3dB_Popt3dB = pd.DataFrame({'Idx':['Idx'],'V_th_p/V':['V_th_p/V'],'V_th_n/V':['V_th_n/V'],'Power @ -3dB':['P_opt @ -3dB/'+PM.ask_PowerUnits()]})
        
        # Const Value for the th.PS
        PS_1.set_Volt(Vth_min)
        PS_1.set_Amp(I_th_max)
        PS_2.set_Volt(Vth_min)
        PS_2.set_Amp(I_th_max)
        
        # save Popt @ Vth0
        PowerVec_Vthmin.append(PM.DefaultPowerMeas(WaveLength))
        
        # save minimum and maximum V_th (for ADS export later)
        V_th_min_vec.append(Vth_min) 
        V_th_max_vec.append(Vth_max)
        
        # save Varactor and Peltier element voltage (for ADS export later)
        V_Var_vec.append(V_Var)
        V_Peltier_vec.append(V_Peltier)
        
        # save the current time
        now = datetime.now()
        time_vec.append(now)
        
        
        
        
        if th_PS_source_const_or_sweep == 0:
            # set voltages
            PS_1.set_Volt(float(V_th_p_const))
            PS_2.set_Volt(float(V_th_n_const))
            # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
            t.sleep(t_th)
            # Measure static optical power
            measured_P_opt = PM.DefaultPowerMeas(WaveLength)
            
            # save values that have to be saved in .txt files
            V_th_p_3dB_vec.append(float(V_th_p_const))
            V_th_p_3dB_vec_np = np.array(V_th_p_3dB_vec, dtype=np.float32)
            V_th_n_3dB_vec.append(float(V_th_n_const))
            V_th_n_3dB_vec_np = np.array(V_th_n_3dB_vec, dtype=np.float32)
            V_th_p_minP_vec.append(float(V_th_p_const))
            V_th_p_minP_vec_np = np.array(V_th_p_minP_vec, dtype=np.float32)
            V_th_n_minP_vec.append(float(V_th_n_const))
            V_th_n_minP_vec_np = np.array(V_th_n_minP_vec, dtype=np.float32)
            V_th_p_maxP_vec.append(float(V_th_p_const))
            V_th_p_maxP_vec_np = np.array(V_th_p_maxP_vec, dtype=np.float32)
            V_th_n_maxP_vec.append(float(V_th_n_const))
            V_th_n_maxP_vec_np = np.array(V_th_n_maxP_vec, dtype=np.float32)            
            PowerVec_min.append(measured_P_opt)
            PowerVec_min_np = np.array(PowerVec_min, dtype=np.float32) 
            PowerVec_max.append(measured_P_opt)
            PowerVec_max_np = np.array(PowerVec_max, dtype=np.float32)
            
        elif th_PS_source_const_or_sweep == 1:
            
            # initialize all vectors which are rewritten in every V_th sweep
            indexList2 = []                 # used for txt file
            V_th_p_Vec = []                 # will be set to VthVec followed by Vth_Steps zeros, used for txt file
            V_th_n_Vec = []                 # will be set to Vth_Steps zeros followed by VthVec, used for txt file
            PowerVec_Vth = []               # used for txt file
            PowerVec_Vth_p = []             # only used for plotting, deleted and rewritten in each step of the loop
            PowerVec_Vth_n = []             # only used for plotting, deleted and rewritten in each step of the loop
            V_Var_vec_Vth_sweep = []        # used for txt file
            V_Peltier_vec_Vth_sweep = []    # used for txt file
        
            # sweep th. PS
            p=0
            PS_1.set_Volt(0)
            PS_2.set_Volt(0)
            for p in range(len(VthVec)):
                # loadingBarTwo(p+1,int(len(VthVec)),1)
                PS_1.set_Volt(VthVec[p])
                V_th_p_Vec.append(VthVec[p])
                V_th_n_Vec.append(0)
                # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
                t.sleep(t_th)
                # Measure static optical power
                measured_P_opt = PM.DefaultPowerMeas(WaveLength)
                PowerVec_Vth.append(measured_P_opt)                                          
                #PowerVec_Vth_mem.append(measured_P_opt)                # given to PowerVec_Vth (which has another data format)
                PowerVec_Vth_p.append(measured_P_opt)                   # used for plotting
                V_Var_vec_Vth_sweep.append(float(V_Var))                # used for txt file
                V_Peltier_vec_Vth_sweep.append(float(V_Peltier))        # used for txt file
                indexList2.append(idx_2)
                idx_2 += 1
    
            p=0
            PS_1.set_Volt(0)
            PS_2.set_Volt(0)
            for p in range(len(VthVec)):
                # loadingBarTwo(p+1,int(len(VthVec)),1)
                PS_2.set_Volt(VthVec[p])
                V_th_p_Vec.append(0)
                V_th_n_Vec.append(VthVec[p])
                # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
                t.sleep(t_th)
                # Measure static optical power
                measured_P_opt = PM.DefaultPowerMeas(WaveLength)
                PowerVec_Vth.append(measured_P_opt)                                          
                #PowerVec_Vth_mem.append(measured_P_opt)                # given to PowerVec_Vth (which has another data format)
                PowerVec_Vth_n.append(measured_P_opt)                   # used for plotting
                V_Var_vec_Vth_sweep.append(float(V_Var))                # used for txt file
                V_Peltier_vec_Vth_sweep.append(float(V_Peltier))        # used for txt file
                indexList2.append(idx_2)
                idx_2 += 1
            
            
            
            # Plot P_opt over V_th_n and V_th_p
            P_opt_max = max(PowerVec_Vth)       #required for same scaling in subplot and calculating V_th_max and QP 
            P_opt_min = min(PowerVec_Vth)       #required for same scaling in subplot and calculating V_th_max and QP
            
            figure_Vth, (plot_left, plot_right) = plt.subplots(1, 2)
            plot_left.plot(VthVec, PowerVec_Vth_n, color = 'red')
            plot_left.invert_xaxis()
            plot_right.plot(VthVec, PowerVec_Vth_p, color = 'green')
            plot_left.set( ylabel = '$P_{Out}$/' + PM.ask_PowerUnits())
            plot_right.set( ylabel = '$P_{Out}$/' + PM.ask_PowerUnits())
            plot_left.set( xlabel = "$V_{th,n}$/V")
            plot_right.set( xlabel = "$V_{th,p}$/V")
            plot_right.grid()
            plot_left.grid()
            plot_left.set_ylim([P_opt_max,P_opt_min])
            plot_right.set_ylim([P_opt_max,P_opt_min])
            #plot_left.ylim((P_opt_max,P_opt_min))
            # fig.suptitle("@ $V_{TH}$ = "+str(Vth_3dB)+" V")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.savefig(path_SVG_V_th_sweep +'/'+ nameImage + '_V_th_sweep'+ str(SystemSourceMeter_vec[j]) + "_.svg")   
            plt.close()
            
            
            
            #Save data in dict and then in .txt File in ADS-txt Format
            PowerVec_Vth = np.array(PowerVec_Vth, dtype=np.float32) 
            data3 = pd.DataFrame({'idx2':indexList2, 'V_Peltier':V_Peltier_vec_Vth_sweep, 'V_Var':V_Var_vec_Vth_sweep, 'V_th_p/V':V_th_p_Vec, 'V_th_n/V':V_th_n_Vec, 'P_opt_@_Vth':PowerVec_Vth})
            V_th_Popt = V_th_Popt.append(data3)
            with open(path_TXT_V_th_sweep + '/'+ 'P_opt_over_Vth_with_' + file_name_V_or_I +'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]) +'.txt', 'a') as f:
                f.write('begin dscrdata')
                f.write(" \n")
                f.write("% ")
                dfAsString = V_th_Popt.to_string(header=False, index=False)
                f.write(dfAsString)
                f.write(" \n")
                f.write("END dscrdata")
           
            
            #Define function to find Vth for a given P_opt value
            def find_nearest_Vth_and_P_opt_for_given_Popt_value(V_th_p_Vec, V_th_n_Vec, Popt_vec, Popt_value):
                power_array = np.asarray(Popt_vec)
                V_th_p_array = np.asarray(V_th_p_Vec) 
                V_th_n_array = np.asarray(V_th_n_Vec)
                index = (np.abs(power_array - Popt_value)).argmin()
                V_th_p = V_th_p_array[index] 
                V_th_n = V_th_n_array[index] 
                P_opt = power_array[index]                
                return [index, V_th_p, V_th_n, P_opt]
            
            # ### test environment ###
            # # Here a fixed vector is given to the "find_nearest_Vth_and_P_opt_for_given_Popt_value" function
            # # the vector contain two exactly same values which could be identified as the QP
            # # Thus, this test can be used to check correct functionlity of the "find_nearest_Vth_and_P_opt_for_given_Popt_value" function
            # VthVec_test = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1]
            # print("VthVec_test")
            # print(VthVec_test)
            # PowerVec_Vth_test = [-34.2821236, -34, -33, -34.2585678, -34.2530594, -33, -34.2272758, -34.1936111, -34.1745224, -34.1389275, -34.1242599, -34.0865402, -34.0559998, -34.0014305, -33.9488792, -33.9073334, -33.8489151, -33.7964401, -33.7437401, -33.694622, -33.6427193, -33.5910187, -33.5421638, -33.472393, -33.4169388, -33.3559494, -33.2971458, -33.272625, -33.185997, -33.1242638, -33.0659447, -33.0019341, -32.9487724, -32.9023857, -32.8681374, -32.8083305, -32.7595062, -32.7112274, -32.6671333, -32.6256218, -32.5869484, -32.5471611, -32.5155907, -32.485527, -32.464222, -32.4469719, -32.4286842, -32.40625, -32.3954659, -32.3777046, -30]
            # print("PowerVec_Vth_test")
            # print(PowerVec_Vth_test)
            # P_opt_max_test = max(PowerVec_Vth_test)
            # print("P_opt_max_test")
            # print(P_opt_max_test)
            # Power_3dB_ideal_test = P_opt_max_test-3
            # print("Power_3dB_ideal_test")
            # print(Power_3dB_ideal_test)
            # [idx_3dB_test, V_th_3dB_test, P_opt_3dB_test] = find_nearest_Vth_and_P_opt_for_given_Popt_value(VthVec_test, PowerVec_Vth_test, Power_3dB_ideal_test)
            # print("Test: index for Power_3dB")
            # print(idx_3dB_test)
            # print("Test: V_th @ Power_3dB found")
            # print(V_th_3dB_test)
            # print("Test: Power_3dB found")
            # print(P_opt_3dB_test)
            
            
        
            
            #Calculate V_th @ P_opt_max 
            [idx_max, V_th_p_maxP, V_th_n_maxP, P_opt_max] = find_nearest_Vth_and_P_opt_for_given_Popt_value(V_th_p_Vec, V_th_n_Vec, PowerVec_Vth, P_opt_max)
            
            #Calculate V_th @ P_opt_max 
            [idx_min, V_th_p_minP, V_th_n_minP, P_opt_min] = find_nearest_Vth_and_P_opt_for_given_Popt_value(V_th_p_Vec, V_th_n_Vec, PowerVec_Vth, P_opt_min)
            
            #Popt @ -3dB ideal
            Power_3dB_ideal_temp = P_opt_max-3

            #Calculate P_opt_3dB and V_th@P_opt_3dB
            [idx_3dB, V_th_p_3dB_found, V_th_n_3dB_found, P_opt_3db_found] = find_nearest_Vth_and_P_opt_for_given_Popt_value(V_th_p_Vec, V_th_n_Vec, PowerVec_Vth, Power_3dB_ideal_temp)
            
            
            V_th_p_meas = V_th_p_3dB_found
            V_th_n_meas = V_th_n_3dB_found
            
            #save results into the corresponding arrays (in correct data format)
            V_th_p_3dB_vec.append(float(V_th_p_3dB_found))
            V_th_p_3dB_vec_np = np.array(V_th_p_3dB_vec, dtype=np.float32)
            V_th_n_3dB_vec.append(float(V_th_n_3dB_found))
            V_th_n_3dB_vec_np = np.array(V_th_n_3dB_vec, dtype=np.float32)
            V_th_p_minP_vec.append(float(V_th_p_minP))
            V_th_p_minP_vec_np = np.array(V_th_p_minP_vec, dtype=np.float32)
            V_th_n_minP_vec.append(float(V_th_n_minP))
            V_th_n_minP_vec_np = np.array(V_th_n_minP_vec, dtype=np.float32)
            V_th_p_maxP_vec.append(float(V_th_p_maxP))
            V_th_p_maxP_vec_np = np.array(V_th_p_maxP_vec, dtype=np.float32)
            V_th_n_maxP_vec.append(float(V_th_n_maxP))
            V_th_n_maxP_vec_np = np.array(V_th_n_maxP_vec, dtype=np.float32)            
            PowerVec_min.append(P_opt_min)
            PowerVec_min_np = np.array(PowerVec_min, dtype=np.float32) 
            PowerVec_max.append(P_opt_max)
            PowerVec_max_np = np.array(PowerVec_max, dtype=np.float32)        
            
            
            # delete vectors which are initialized and rewritten in every V_th sweep
            del(indexList2)
            del(V_th_p_Vec) 
            del(V_th_n_Vec)
            del(V_Var_vec_Vth_sweep)
            del(V_Peltier_vec_Vth_sweep)
            del(PowerVec_Vth_p) 
            del(PowerVec_Vth_n)
            del(PowerVec_Vth)
              
            #SET Vth @ V_3dB
            PS_1.set_Volt(float(V_th_p_meas))
            PS_2.set_Volt(float(V_th_n_meas))
        
        else:
            print("an error occured: th_PS_source_const_or_sweep was not set to 0 or 1")
        
        
        
        # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
        t.sleep(t_th)
        
        #################################################
        ############### Core measurements ###############
        ################################################# 
        VNA.set_SetAverageState(1,'ON')
        VNA.set_AverageCount(1,Average_points_VNA)
        time = VNA.ask_SweepTime()
        #t.sleep(time*5)
        t.sleep(time*8)
        
        if V_or_I_sweep == 0:
            # voltage set, current measured
            SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
            SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))
        elif   V_or_I_sweep == 1:
            # current set, voltage measured
            SystemSourceMeter_Voltage_A.append(KA.ask_Voltage(Channel1))
            SystemSourceMeter_Voltage_B.append(KA.ask_Voltage(Channel2))
            print("\n SystemSourceMeter voltage channel A =")
            print(SystemSourceMeter_Voltage_A[j])
            print("\n SystemSourceMeter voltage channel B =")
            print(SystemSourceMeter_Voltage_B[j])
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            # voltage set, current measured
            SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
            SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))    
        
        
        
        
        
        PowerVec_meas.append(PM.DefaultPowerMeas(WaveLength)) 
        VNA.SaveData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]), 4)
        file = VNA.ask_TransferData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
        VNA.SaveTransferData(file, path_S_Param, 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
        VNA.DeleteData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)

        with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "r") as f:
            lines = f.readlines()
        
        with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "w") as f:
            for i in range(1,len(lines)):
                f.write(lines[i])
        
    
        S_Param_Names.append('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p')
        S_Param_Names_Path.append('"'+path_S_Param+'/'+ 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p'+'"')
             
        Vth_Popt_Names_Path.append('"'+path_TXT_V_th_sweep + '/'+ 'P_opt_over_Vth_with_' + file_name_V_or_I +'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]) +'.txt'+'"')
        indexList.append(idx)
        idx += 1
        t.sleep(1)
        
        
        
        # Save results of this measurement step into TXT file (see be able to observe the measurement during measurement process)
        path_to_save_current_measurement_results = path_TXT_measurement_step + '/' + 'step_' + str(j+1) + '.txt'
        with open(path_to_save_current_measurement_results, 'a') as file_measurement_step:
            file_measurement_step.write("SystemSourceMeter voltage channel A = " + str(SystemSourceMeter_Voltage_A[j]) + "\n")
            file_measurement_step.write("SystemSourceMeter voltage channel B = " + str(SystemSourceMeter_Voltage_B[j]) + "\n")
            file_measurement_step.write("SystemSourceMeter current channel A = " + str(SystemSourceMeter_Current_A[j]) + "\n")
            file_measurement_step.write("SystemSourceMeter current channel B = " + str(SystemSourceMeter_Current_B[j]) + "\n")
            file_measurement_step.write("P_opt_@V_th_0/dBm = " + str(PowerVec_Vthmin[j]) + "\n")
            file_measurement_step.write("P_opt_max/dBm = " + str(PowerVec_max_np[j]) + "\n")
            file_measurement_step.write("P_opt_min/dBm = " + str(PowerVec_min_np[j]) + "\n")
            file_measurement_step.write("P_opt_meas/dBm = " + str(PowerVec_meas[j]) + "\n")
            file_measurement_step.write("V_th_p_meas/V = " + str(V_th_p_3dB_vec[j]) + "\n")
            file_measurement_step.write("V_th_n_meas/V = " + str(V_th_n_3dB_vec[j]) + "\n")
            file_measurement_step.write("time = " + str(time_vec[j]) + "\n")
            
            
                        
   


    #################################################
    ################## data frame ###################
    #################################################    

    V_th_min_vec = np.array(V_th_min_vec, dtype=np.float32)
    V_th_max_vec = np.array(V_th_max_vec, dtype=np.float32)
    V_Var_vec = np.array(V_Var_vec, dtype=np.float32)
    V_Peltier_vec = np.array(V_Peltier_vec, dtype=np.float32)
    PowerVec_Vthmin = np.array(PowerVec_Vthmin, dtype=np.float32)
    PowerVec_meas = np.array(PowerVec_meas, dtype=np.float32)
         
    df2 = pd.DataFrame({'Idx':indexList, 'V_Peltier':V_Peltier_vec, 'V_Var':V_Var_vec, 'V_SSM_Channel_A/V': SystemSourceMeter_Voltage_A, 'I_SSM_Channel_A/A': SystemSourceMeter_Current_A, 'V_SSM_Channel_B/V': SystemSourceMeter_Voltage_B, 'I_SSM_Channel_B/A': SystemSourceMeter_Current_B, 'P_opt_0/dBm': PowerVec_Vthmin, 'P_opt_meas/dBm': PowerVec_meas, 'P_opt_max/dBm': PowerVec_max_np, 'P_opt_min/dBm': PowerVec_min_np, 'V_th_min/V': V_th_min_vec, 'V_th_max/V': V_th_max_vec, 'V_th_p_meas/V': V_th_p_3dB_vec, 'V_th_n_meas/V': V_th_n_3dB_vec, 'V_th_p_maxP/V': V_th_p_maxP_vec_np, 'V_th_n_maxP/V': V_th_n_maxP_vec_np, 'V_th_p_minP/V': V_th_p_minP_vec_np, 'V_th_n_minP/V': V_th_n_minP_vec_np, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path, 'path_P_opt_over_V_th':Vth_Popt_Names_Path}) # edited by Tobias
    #data2 = pd.DataFrame({'V_SSM_Channel_A/V': SystemSourceMeter_Voltage_A, 'I_SSM_Channel_A/A': SystemSourceMeter_Current_A, 'V_SSM_Channel_B/V': SystemSourceMeter_Voltage_B, 'I_SSM_Channel_B/A': SystemSourceMeter_Current_B, 'P_opt_meas/dBm':PowerVec_meas})
    data2 = pd.DataFrame({'V_SSM_Channel_A/V': SystemSourceMeter_Voltage_A, 'I_SSM_Channel_A/A': SystemSourceMeter_Current_A, 'V_SSM_Channel_B/V': SystemSourceMeter_Voltage_B, 'I_SSM_Channel_B/A': SystemSourceMeter_Current_B, 'P_opt_meas/dBm':PowerVec_meas, 'time':time_vec})
    Sdata2 = pd.DataFrame({'Idx':indexList, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    data = data.append(data2)
    df = df.append(df2)
    Sdata = Sdata.append(Sdata2) 
    data4 = pd.DataFrame({'Idx':indexList,'V_th_p/V': V_th_p_3dB_vec_np, 'V_th_n/V': V_th_n_3dB_vec_np, 'Power @ -3dB':PowerVec_meas})
    Vth3dB_Popt3dB = Vth3dB_Popt3dB.append(data4)
   
    
    # Plot all results regarding SystemSourceMeter sweep
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    # subplot 1
    ax1.plot(df2['V_SSM_Channel_A/V'],df2['I_SSM_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax1.plot(df2['V_SSM_Channel_B/V'],df2['I_SSM_Channel_B/A'],linewidth=3.0, color = 'blue', label = 'Channel B')
    ax1.set( ylabel = "$I_{Source Meter}$/A")
    ax1.set( xlabel = "$V_{Source Meter}$/V")
    ax1.legend(loc = 'best')
    ax1.grid()
    # subplot 2
    ax2.plot(df2['V_SSM_Channel_A/V'],df2['P_opt_meas/dBm'],linewidth=3.0, color = 'blue', label = 'Channel A')
    ax2.set( ylabel = 'P_{opt,meas}/dBm')
    ax2.set( xlabel = "$V_{Source Meter A}$/V")
    ax2.grid()
    # subplot 3
    ax3.plot(df2['I_SSM_Channel_A/A'],df2['P_opt_meas/dBm'],linewidth=3.0, color = 'blue', label = 'Channel A')
    ax3.set( ylabel = 'P_{opt,meas}/dBm')
    ax3.set( xlabel = "$I_{Source Meter A}$/A")
    ax3.grid()
    # fig Manager
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    # save plot
    plt.savefig(path_plot_SystemSourceMeter +'/'+ nameImage +'_meas' +'_'+ str(j) +".svg")   
    plt.close()
 
    
 
    # Plot all results regarding SystemSourceMeter sweep
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    # subplot 1
    ax1.plot(df2['V_SSM_Channel_A/V'],df2['I_SSM_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax1.plot(df2['V_SSM_Channel_B/V'],df2['I_SSM_Channel_B/A'],linewidth=3.0, color = 'blue', label = 'Channel B')
    ax1.set( ylabel = "$I_{Source Meter}$/A")
    ax1.set( xlabel = "$V_{Source Meter}$/V")
    ax1.legend(loc = 'best')
    ax1.grid()
    # subplot 2
    ax2.plot(df2['V_SSM_Channel_A/V'],df2['P_opt_max/dBm'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax2.set( ylabel = 'P_{opt,max}/dBm')
    ax2.set( xlabel = "$V_{Source Meter A}$/V")
    ax2.grid()
    # subplot 3
    ax3.plot(df2['I_SSM_Channel_A/A'],df2['P_opt_max/dBm'],linewidth=3.0, color = 'red', label = 'Channel A')
    ax3.set( ylabel = 'P_{opt,max}/dBm')
    ax3.set( xlabel = "$I_{Source Meter A}$/A")
    ax3.grid()
    # fig Manager
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    # save plot
    plt.savefig(path_plot_SystemSourceMeter +'/'+ nameImage +'_max' +'_'+ str(j) +".svg")   
    plt.close()
    

    #Shut the instruments down and save the csv   
    PS_1.set_Volt(0)
    PS_1.set_Out('OFF')
    PS_2.set_Volt(0)
    PS_2.set_Out('OFF')
    VNA.RTL()
    KA.set_Voltage(Channel1, 0)
    KA.set_SourceOutput(Channel1,'OFF')
    KA.set_Voltage(Channel2, 0)
    KA.set_SourceOutput(Channel2,'OFF')
    df.to_csv(path_CSV_summary +'/'+ name +'.csv',sep = ',', index=False)
    
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    ParamsInst['PowerSupply Current'] = 'A'
    ParamsInst['PowerSupply Voltage'] = 'V'
    ParamsInst['VNA Center frequency Hz'] = str(VNA.ask_CenterFreq(1))
    ParamsInst['VNA CW frequency Hz'] = str(VNA.ask_CWFreq(1))
    ParamsInst['VNA CW averaging count'] = str(VNA.ask_AverageCount(1))
    ParamsInst['VNA IF bandwidth Hz'] = str(VNA.ask_ResolutionBW(1))
    with open(path_Parameters +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")   
            
            
    #Save Results in ADS-txt Format        
    with open(path_Tabular_idx_voltages_currents_powers_paths + '/'+name+ '_tabular_idx_voltages_currents_powers_paths'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path_Backup_tabular + '/'+name+ '_tabula__V_A__I_A__V_B__I_B__P_opt'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = data.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path_Backup_tabular + '/'+name+ '_tabula__idx_S_Parameters_names__SParameters_path'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Sdata.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        
    with open(path_Quadrature_points +'/'+name+ '_tabula__idx__V_th_3dB_found__P_opt_at_Vth_3dB'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = Vth3dB_Popt3dB.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")    
    
    
    now = datetime.now()
    date_and_time_end_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Measurement ended at:", date_and_time_end_string)
    
    
########################################################
##################### new function #####################
########################################################  
def Tobias_MZM_characteristic_in_dependency_of_thermal_biasing(Instrument, V_or_I_sweep, V_I_min, V_I_max, V_I_step, WaveLength, Vth_min, Vth_max, Steps_Vth, I_th_max, t_th, V_Var, V_Peltier, Average_points_VNA, path, name):
    """
    

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

    """
    
    temp = 1
    print("len(Instrument)")
    print(len(Instrument)) 
    
    # working_directory = os.getcwd
    # print("Current working directory: {0}".format(working_directory))
    # print("Current working directory:")
    # print(working_directory)
    
    
    # Create folders in which the files are to be saved
    path_SVG_V_th_sweep = path + '/SVG_V_th_sweep'
    if not os.path.exists(path_SVG_V_th_sweep):
        os.makedirs(path_SVG_V_th_sweep)
    path_Tabular_idx_voltages_currents_powers_paths = path + '/Tabular_idx_voltages_currents_powers_paths'
    if not os.path.exists(path_Tabular_idx_voltages_currents_powers_paths):
        os.makedirs(path_Tabular_idx_voltages_currents_powers_paths)
    path_S_Param = path + '/S_Param'
    if not os.path.exists(path_S_Param):
        os.makedirs(path_S_Param)
    path_Parameters = path + '/Parameters'
    if not os.path.exists(path_Parameters):
        os.makedirs(path_Parameters)
    
       

    for i in range(len(Instrument)):
        # print("i")
        # print(i)
        # print("str(Instrument[i]).split('.')")
        # print(str(Instrument[i]).split('.'))
        if 'MS4647B' in str(Instrument[i]).split('.'):
            VNA = Instrument[i]
        elif 'PM100D' in str(Instrument[i]).split('.'):
            PM = Instrument[i]
        elif 'KEITHLEY2612' in str(Instrument[i]).split('.'):
            KA = Instrument[i]
        elif 'KA3005p' in str(Instrument[i]).split('.'):
            # print("temp")
            # print(temp) 
            if temp == 1:
                # print("set PS_1")
                PS_1 = Instrument[i]
                # print("set temp = 2")
                temp = 2
            else:
                print("set PS_2")
                PS_2 = Instrument[i]
        elif 'RD3005' in str(Instrument[i]).split('.'):
            # print("temp")
            # print(temp) 
            if temp == 1:
                # print("set PS_1")
                PS_1 = Instrument[i]
                # print("set temp = 2")
                temp = 2
            else:
                # print("set PS_2")
                PS_2 = Instrument[i]
        else:
            raise Exception("""
                                 The Instrument that you select is not one of: 
                                     - Power Supply 
                                     - Source Meter
                                     - Power Meter
                                     - Vector Network Analyzer
                                 """)


    
    name = name
    nameParam = name + '_Param'
    nameImage = name + '_Image'
    
    
    
    #Define arrays
    
    StepnumVec = round((V_I_max - V_I_min) / V_I_step) + 1
    SystemSourceMeter_vec  = np.linspace(V_I_min, V_I_max, StepnumVec)
    idx = 0                 
    
    #Define the Header and dectionarys to save the data
    df =  pd.DataFrame({'Idx':['idx'], 'V_Peltier':['V_Peltier'], 'V_Var':['V_Var'], 'V_SSM_Channel_A/V':['V_DC_PS_A'], 'I_SSM_Channel_A/A': ['I_DC_PS_A'], 'V_SSM_Channel_B/V':['V_DC_PS_B'], 'I_SSM_Channel_B/A': ['I_DC_PS_B'], 'P_opt_meas/dBm':['P_opt_meas'], 'V_th_min/V':['V_th_min'], 'V_th_max/V':['V_th_max'], 'V_th_p_meas/V':['Vth_p_meas'], 'V_th_n_meas/V':['Vth_n_meas'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
    
    
    
    #Define vector to sweep the power supplies (sweeping th. PS and finding QP)
    Vth_Steps = round((Vth_max - Vth_min) / Steps_Vth) + 1
    VthVec = np.linspace(Vth_min, Vth_max, Vth_Steps)
    V_th_p_Vec = []         # will be set to VthVec followed by Vth_Steps zeros
    V_th_n_Vec = []         # will be set to Vth_Steps zeros followed by VthVec
    V_th_p_Vec_float = []   # required to save the data
    V_th_n_Vec_float = []   # required to save the data
    
    
    #Predefine the SystemSourcemeter 
    Channel1 = 'a' #Set Channel 1 as Channel A
    Channel2 = 'b' #Set Channel 2 as Channel B
    if V_or_I_sweep == 0:
        KA.set_OutputSourceFunction(Channel1,'volt')
        KA.set_OutputSourceFunction(Channel2,'volt')
        KA.set_AutoVoltageRange(Channel1, 'ON')
        KA.set_AutoVoltageRange(Channel2, 'ON')
    elif   V_or_I_sweep == 1:  
        KA.set_OutputSourceFunction(Channel1,'amp')
        KA.set_OutputSourceFunction(Channel2,'amp')
        KA.set_AutoCurrentRange(Channel1, 'ON')
        KA.set_AutoCurrentRange(Channel2, 'ON')
    else:
        print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
        KA.set_OutputSourceFunction(Channel1,'volt')
        KA.set_OutputSourceFunction(Channel2,'volt')
        KA.set_AutoVoltageRange(Channel1, 'ON')
        KA.set_AutoVoltageRange(Channel2, 'ON')
    KA.set_Current(Channel1, 0)
    KA.set_Voltage(Channel1, 0)
    KA.set_Current(Channel2, 0)
    KA.set_Voltage(Channel2, 0)
    KA.set_SourceOutput(Channel1,'ON')
    KA.set_SourceOutput(Channel2,'ON')
    
    #Predefine the power sources 
    PS_1.set_Volt(0)
    PS_1.set_Out('ON')
    PS_2.set_Volt(0)
    PS_2.set_Out('ON')
    
    
    
    V_Var_vec = []
    V_Peltier_vec = []
    V_th_min_vec = []
    V_th_max_vec = []
    PowerVec_meas = []
    S_Param_Names = []
    S_Param_Names_Path = []
    Vth_Popt_Names_PAth = []
    indexList = []
    SystemSourceMeter_Current_A = []
    SystemSourceMeter_Voltage_A = []
    SystemSourceMeter_Current_B = []
    SystemSourceMeter_Voltage_B = []
    
    
    
    
    
    # Const Value for the th.PS
    PS_1.set_Volt(Vth_min)
    PS_1.set_Amp(I_th_max)
    PS_2.set_Volt(Vth_min)
    PS_2.set_Amp(I_th_max)
    
    
    # Start PS voltage/ current sweep (SystemSourceMeter sweep)
    for j in range(len(SystemSourceMeter_vec)):
        loadingBar(j+1,int(len(SystemSourceMeter_vec)),1)
        #KA.set_Voltage(Channel1,SystemSourceMeter_vec[j])
        
        # set SystemSourceMeter either to current or voltage sweep (according to user input)
        if V_or_I_sweep == 0:
            KA.set_Voltage(Channel1,SystemSourceMeter_vec[j])
            KA.set_Voltage(Channel2,SystemSourceMeter_vec[j])
        elif   V_or_I_sweep == 1:  
            KA.set_Current(Channel1,0.001*SystemSourceMeter_vec[j])     # conversion to mA
            KA.set_Current(Channel2,0.001*SystemSourceMeter_vec[j])     # conversion to mA
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            KA.set_Voltage(Channel1,SystemSourceMeter_vec[j])
            KA.set_Voltage(Channel2,SystemSourceMeter_vec[j])
        
        
        # initialize variables for P_opt over V_th plot
        V_th_p_Vec_plot = []         
        V_th_n_Vec_plot = [] 
        PowerVec_Vth_p_plot = []
        PowerVec_Vth_n_plot = []        
        
        
        # Start thermal PS p voltage sweep (powersource 1 sweep)    
        p=0
        PS_1.set_Volt(0)
        PS_2.set_Volt(0)
        
        for p in range(len(VthVec)):
            # loadingBarTwo(p+1,int(len(VthVec)),1)
            
            # save SystemSourceMeter source voltage/current
            if V_or_I_sweep == 0:
                SystemSourceMeter_Voltage_A.append(float(SystemSourceMeter_vec[j]))
                SystemSourceMeter_Voltage_B.append(float(SystemSourceMeter_vec[j]))
            elif   V_or_I_sweep == 1:
                SystemSourceMeter_Current_A.append(float(0.001*SystemSourceMeter_vec[j]))   # conversion to mA
                SystemSourceMeter_Current_B.append(float(0.001*SystemSourceMeter_vec[j]))   # conversion to mA
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                SystemSourceMeter_Voltage_A.append(float(SystemSourceMeter_vec[j]))
                SystemSourceMeter_Voltage_B.append(float(SystemSourceMeter_vec[j]))
            
            
            # set the thermal voltages and save them
            PS_1.set_Volt(VthVec[p])
            t.sleep(t_th)
            V_th_p_Vec.append(VthVec[p])
            V_th_n_Vec.append(0)
            V_th_p_Vec_float.append(float(VthVec[p]))
            V_th_n_Vec_float.append(float(0))
            
            # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
            t.sleep(t_th)
            
            # save minimum and maximum V_th (for ADS export later)
            V_th_min_vec.append(Vth_min) 
            V_th_max_vec.append(Vth_max)
            
            # save Varactor and Peltier element voltage (for ADS export later)
            V_Var_vec.append(V_Var)
            V_Peltier_vec.append(V_Peltier)
            
            
            ### start core measurements ###
            
            # measure the optical power and save it                                       
            measured_P_opt = PM.DefaultPowerMeas(WaveLength)                                          
            PowerVec_meas.append(measured_P_opt)         # given to PowerVec_Vth (which has another data format)
            
            # save data for P_opt over V_th plot
            V_th_p_Vec_plot.append(VthVec[p])
            PowerVec_Vth_p_plot.append(measured_P_opt)
            
            
            VNA.set_SetAverageState(1,'ON')
            VNA.set_AverageCount(1,Average_points_VNA)
            time = VNA.ask_SweepTime()
            #t.sleep(time*5)
            t.sleep(time*8)
            
            # measure phaseshifter voltage or current
            if V_or_I_sweep == 0:
                # voltage set, current measured
                SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
                SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))
            elif   V_or_I_sweep == 1:
                # current set, voltage measured
                SystemSourceMeter_Voltage_A.append(KA.ask_Voltage(Channel1))
                SystemSourceMeter_Voltage_B.append(KA.ask_Voltage(Channel2))
                print(SystemSourceMeter_Voltage_A)
                print(SystemSourceMeter_Voltage_B)
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                # voltage set, current measured
                SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
                SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))    
            
            # files are given different names, depending on type of sweeping (voltage or current sweep)
            if V_or_I_sweep == 0:
                # voltage set, current measured
                file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_vec[j])+'V__V_B_'+str(SystemSourceMeter_vec[j])+'V__Vth_p_'+str(VthVec[p])+'V__V_th_n_0V'
            elif   V_or_I_sweep == 1:
                # current set, voltage measured
                file_name_V_or_I = '_I_A_'+str(SystemSourceMeter_vec[j])+'mA__I_B_'+str(SystemSourceMeter_vec[j])+'mA__Vth_p_'+str(VthVec[p])+'V__V_th_n_0V'
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                # voltage set, current measured
                file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_vec[j])+'V__V_B_'+str(SystemSourceMeter_vec[j])+'V__Vth_p_'+str(VthVec[p])+'V__V_th_n_0V'
            
            
            VNA.SaveData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]), 4)
            file = VNA.ask_TransferData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
            VNA.SaveTransferData(file, path_S_Param, 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
            VNA.DeleteData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
    
            with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "r") as f:
                lines = f.readlines()
            
            with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "w") as f:
                for i in range(1,len(lines)):
                    f.write(lines[i])
            
        
            S_Param_Names.append('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p')
            S_Param_Names_Path.append('"'+path_S_Param+'/'+ 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p'+'"')
            Vth_Popt_Names_PAth.append('"'+path_S_Param + '/'+ 'Vth_@_Voltage_psa_'+ str(SystemSourceMeter_vec[j])+'.txt'+'"')
            ### end core measurements ###
            
            

            # save index for txt file (required for ADS import)
            indexList.append(idx)
            idx += 1
            
            # wait
            t.sleep(1)
        
        
        # Start thermal PS n voltage sweep (powersource 2 sweep)    
        p=0
        PS_1.set_Volt(0)
        PS_2.set_Volt(0)
        
        for p in range(len(VthVec)):
            # loadingBarTwo(p+1,int(len(VthVec)),1)
            
            # save SystemSourceMeter source voltage/current
            if V_or_I_sweep == 0:
                SystemSourceMeter_Voltage_A.append(float(SystemSourceMeter_vec[j]))
                SystemSourceMeter_Voltage_B.append(float(SystemSourceMeter_vec[j]))
            elif   V_or_I_sweep == 1:
                SystemSourceMeter_Current_A.append(float(0.001*SystemSourceMeter_vec[j]))   # conversion to mA
                SystemSourceMeter_Current_B.append(float(0.001*SystemSourceMeter_vec[j]))   # conversion to mA
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                SystemSourceMeter_Voltage_A.append(float(SystemSourceMeter_vec[j]))
                SystemSourceMeter_Voltage_B.append(float(SystemSourceMeter_vec[j]))
            
            # set the thermal voltages and save them
            PS_2.set_Volt(VthVec[p])
            t.sleep(t_th)
            V_th_p_Vec.append(0)
            V_th_n_Vec.append(VthVec[p])
            V_th_p_Vec_float.append(float(0))
            V_th_n_Vec_float.append(float(VthVec[p]))
            
            # Wait for t_th seconds to let the thermal PS heat up and set the phaseshift
            t.sleep(t_th)
            
            # save minimum and maximum V_th (for ADS export later)
            V_th_min_vec.append(Vth_min) 
            V_th_max_vec.append(Vth_max)
            
            # save Varactor and Peltier element voltage (for ADS export later)
            V_Var_vec.append(V_Var)
            V_Peltier_vec.append(V_Peltier)
            
            
            ### start core measurements ###
            
            # measure the optical power and save it                                       
            measured_P_opt = PM.DefaultPowerMeas(WaveLength)                                          
            PowerVec_meas.append(measured_P_opt)         # given to PowerVec_Vth (which has another data format)
            
            # save data for P_opt over V_th plot
            V_th_n_Vec_plot.append(VthVec[p])
            PowerVec_Vth_n_plot.append(measured_P_opt)
            
            VNA.set_SetAverageState(1,'ON')
            VNA.set_AverageCount(1,Average_points_VNA)
            time = VNA.ask_SweepTime()
            #t.sleep(time*5)
            t.sleep(time*8)
            
            # measure phaseshifter voltage or current
            if V_or_I_sweep == 0:
                # voltage set, current measured
                SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
                SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))
            elif   V_or_I_sweep == 1:
                # current set, voltage measured
                SystemSourceMeter_Voltage_A.append(KA.ask_Voltage(Channel1))
                SystemSourceMeter_Voltage_B.append(KA.ask_Voltage(Channel2))
                print(SystemSourceMeter_Voltage_A)
                print(SystemSourceMeter_Voltage_B)
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                # voltage set, current measured
                SystemSourceMeter_Current_A.append(KA.ask_Current(Channel1))
                SystemSourceMeter_Current_B.append(KA.ask_Current(Channel2))    
            
            # files are given different names, depending on type of sweeping (voltage or current sweep)
            if V_or_I_sweep == 0:
                # voltage set, current measured
                file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_vec[j])+'V__V_B_'+str(SystemSourceMeter_vec[j])+'V__Vth_p_0V__V_th_n_'+str(VthVec[p])+'V'
            elif   V_or_I_sweep == 1:
                # current set, voltage measured
                file_name_V_or_I = '_I_A_'+str(SystemSourceMeter_vec[j])+'mA__I_B_'+str(SystemSourceMeter_vec[j])+'mA__Vth_p_0V__V_th_n_'+str(VthVec[p])+'V'
            else:
                print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
                # voltage set, current measured
                file_name_V_or_I = '_V_A_'+str(SystemSourceMeter_vec[j])+'V__V_B_'+str(SystemSourceMeter_vec[j])+'V__Vth_p_0V__V_th_n_'+str(VthVec[p])+'V'
            
            
            VNA.SaveData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]), 4)
            file = VNA.ask_TransferData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
            VNA.SaveTransferData(file, path_S_Param, 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
            VNA.DeleteData('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j]),4)
    
            with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "r") as f:
                lines = f.readlines()
            
            with open(path_S_Param+'/'+'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p', "w") as f:
                for i in range(1,len(lines)):
                    f.write(lines[i])
            
        
            S_Param_Names.append('S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p')
            S_Param_Names_Path.append('"'+path_S_Param+'/'+ 'S_Parameters'+file_name_V_or_I+'_V_Var_'+str(V_Var_vec[j])+'_V_Peltier_'+str(V_Peltier_vec[j])+'.s4p'+'"')
            Vth_Popt_Names_PAth.append('"'+path_S_Param + '/'+ 'Vth_@_Voltage_psa_'+ str(SystemSourceMeter_vec[j])+'.txt'+'"')
            ### end core measurements ###
            
            

            # save index for txt file (required for ADS import)
            indexList.append(idx)
            idx += 1
            
            # wait
            t.sleep(1)        
        
        P_opt_max = max(PowerVec_meas)
        P_opt_min = min(PowerVec_meas)
        
        # print('\n')
        # print('V_th_n_Vec_plot')
        # print(V_th_n_Vec_plot)
        # print('PowerVec_Vth_n_plot')
        # print(PowerVec_Vth_n_plot)
        
        figure_Vth, (plot_left, plot_right) = plt.subplots(1, 2)
        plot_left.plot(V_th_n_Vec_plot, PowerVec_Vth_n_plot, color = 'red')
        plot_left.invert_xaxis()
        plot_right.plot(V_th_p_Vec_plot, PowerVec_Vth_p_plot, color = 'green')
        plot_left.set( ylabel = '$P_{Out}$/' + PM.ask_PowerUnits())
        plot_right.set( ylabel = '$P_{Out}$/' + PM.ask_PowerUnits())
        plot_left.set( xlabel = "$V_{th,n}$/V")
        plot_right.set( xlabel = "$V_{th,p}$/V")
        plot_right.grid()
        plot_left.grid()
        plot_left.set_ylim([P_opt_max,P_opt_min])
        plot_right.set_ylim([P_opt_max,P_opt_min])
        #plot_left.ylim((P_opt_max,P_opt_min))
        # fig.suptitle("@ $V_{TH}$ = "+str(Vth_3dB)+" V")
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        if V_or_I_sweep == 0:
            plt.savefig(path_SVG_V_th_sweep +'/'+ nameImage + '_V_th_sweep__V_PS_'+ str(SystemSourceMeter_vec[j]) + "V_.svg")   
        elif   V_or_I_sweep == 1:
            plt.savefig(path_SVG_V_th_sweep +'/'+ nameImage + '_V_th_sweep__I_PS_'+ str(SystemSourceMeter_vec[j]) + "mA_.svg")   
        else:
            print("Warning: SystemSourceMeter voltage is swept because V_or_I_sweep is not 0 or 1")
            plt.savefig(path_SVG_V_th_sweep +'/'+ nameImage + '_V_th_sweep__V_PS_'+ str(SystemSourceMeter_vec[j]) + "V_.svg")   
        plt.close()
        
        del(V_th_p_Vec_plot) 
        del(V_th_n_Vec_plot)
        del(PowerVec_Vth_p_plot) 
        del(PowerVec_Vth_n_plot)
        
        
    #save parameters and results into the corresponding arrays (in correct data format)
    V_th_min_vec = np.array(V_th_min_vec, dtype=np.float32)
    V_th_max_vec = np.array(V_th_max_vec, dtype=np.float32)
    V_Var_vec = np.array(V_Var_vec, dtype=np.float32)
    V_Peltier_vec = np.array(V_Peltier_vec, dtype=np.float32)
    V_th_p_Vec = np.array(V_th_p_Vec, dtype=np.float32)
    V_th_n_Vec = np.array(V_th_n_Vec, dtype=np.float32)
    PowerVec_meas = np.array(PowerVec_meas, dtype=np.float32)   
    
    
    #################################################
    ################## data frame ###################
    #################################################
    # print('\n')
    # print('indexList')
    # print(indexList)
    # print('V_Peltier_vec')
    # print(V_Peltier_vec) 
    # print('V_Var_vec')
    # print(V_Var_vec)
    # print('SystemSourceMeter_Voltage_A')
    # print(SystemSourceMeter_Voltage_A)
    # print('SystemSourceMeter_Current_A')
    # print(SystemSourceMeter_Current_A)
    # print('SystemSourceMeter_Voltage_B')
    # print(SystemSourceMeter_Voltage_B)
    # print('SystemSourceMeter_Current_B')
    # print(SystemSourceMeter_Current_B)
    # print('PowerVec_meas')
    # print(PowerVec_meas)
    # print('V_th_min_vec')
    # print(V_th_min_vec) 
    # print('V_th_max_vec')
    # print(V_th_max_vec) 
    # print('V_th_p_Vec')
    # print(V_th_p_Vec)
    # print('V_th_n_Vec')
    # print(V_th_n_Vec) 
    # print('S_Param_Names')
    # print(S_Param_Names)
    # print('V_Var_vecS_Param_Names_Path')
    # print(S_Param_Names_Path)
    
    
    df2 = pd.DataFrame({'Idx':indexList, 'V_Peltier':V_Peltier_vec, 'V_Var':V_Var_vec, 'V_SSM_Channel_A/V': SystemSourceMeter_Voltage_A, 'I_SSM_Channel_A/A': SystemSourceMeter_Current_A, 'V_SSM_Channel_B/V': SystemSourceMeter_Voltage_B, 'I_SSM_Channel_B/A': SystemSourceMeter_Current_B, 'P_opt_meas/dBm': PowerVec_meas, 'V_th_min/V': V_th_min_vec, 'V_th_max/V': V_th_max_vec, 'V_th_p_meas/V': V_th_p_Vec, 'V_th_n_meas/V': V_th_n_Vec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
    df = df.append(df2)
 
    
    #Shut the instruments down
    PS_1.set_Volt(0)
    PS_1.set_Out('OFF')
    PS_2.set_Volt(0)
    PS_2.set_Out('OFF')
    VNA.RTL()
    KA.set_Voltage(Channel1, 0)
    KA.set_SourceOutput(Channel1,'OFF')
    KA.set_Voltage(Channel2, 0)
    KA.set_SourceOutput(Channel2,'OFF')


    
    Headers,Data,Param = PM.DisplayParamDict('Power')
    ParamsInst = {}
    for i in range(len(Param)):
        ParamsInst[Param[i]] = Data[i]
    ParamsInst['SourceMeter Current'] = 'A'
    ParamsInst['SourceMeter Voltage'] = 'V'
    ParamsInst['PowerSupply Current'] = 'A'
    ParamsInst['PowerSupply Voltage'] = 'V'
    ParamsInst['VNA Center frequency Hz'] = str(VNA.ask_CenterFreq(1))
    ParamsInst['VNA CW frequency Hz'] = str(VNA.ask_CWFreq(1))
    ParamsInst['VNA CW averaging count'] = str(VNA.ask_AverageCount(1))
    ParamsInst['VNA IF bandwidth Hz'] = str(VNA.ask_ResolutionBW(1))
    with open(path_Parameters +'/'+ nameParam +'.txt', 'w') as file:
        for key, value in ParamsInst.items():
            file.write(key+"\t"+value+"\n")   
            
            
    #Save Results in ADS-txt Format        
    with open(path_Tabular_idx_voltages_currents_powers_paths + '/'+name+ '_tabular_idx_voltages_currents_powers_paths'+'.txt', 'a') as f:
        f.write('begin dscrdata')
        f.write(" \n")
        f.write("% ")
        dfAsString = df.to_string(header=False, index=False)
        f.write(dfAsString)
        f.write(" \n")
        f.write("END dscrdata")
        