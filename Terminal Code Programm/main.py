# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 08:48:51 2022

@author: Martin.Mihaylov
"""

import tkinter as tk
from tkinter import filedialog
from InstrumentControl.InstrumentSelect import InstInit
from InstrumentControl.FunctionCall import MeasFunctions



# =============================================================================
# Select Instruments and Load Instrument Libraries
# =============================================================================

print('''
      ######### How many instruments will be used ######## 
      
      ''')
numInstr = int(input('Number Instruments = '))
print('''
      
      ######### How many instruments will be used ######## 
      
      ''')

listInstruments = []


print('''
      ############ Select which instumnets will be used ########
      
             You will be ask to give the name of the instruments 
             manualy. For example Instrument name: MS4647B for
             Anrtisu Signal Analyzer.
             
             
              Table of instruments
              Anritsu spectrum Analyzer MS2760A = 1
              Anritsu Signal Generator MG3694C = 2
              Anritsu Vectro Analyzer MS4647B = 3
              Power Meter ThorLabs PM100D = 4
              Novoptel Laser LU1000 = 5
              Yokogawa Optical Spectrum Analyzer AQ6370D = 6
              KEITHLEY Source Meter 2612 = 7
              Power Supply KA3005 = 8 
              CoBrite Tunable Laser = 9
              AnaPico AG,APPH20G = 10
              4-Channels Power Suppy GPP4323 = 11
              
              
              
              
      ############ Select which instumnets will be used ########
      ''')
instrumenNameList = ['1','2','3','4','5','6','7','8','9','10', '11']
Instrument = []
for i in range(numInstr):
    instrumenName = input('Instrument name: ')
    if instrumenName in instrumenNameList:
        listInstruments.append(instrumenName)
    else:
        raise ValueError('Invalid Instrument Selected')
            
   
for elements in listInstruments:
    if elements == '1':
        SA = InstInit(elements)
        Instrument.append(SA)
        print('Anrtisu Spectrum Analyzer MS2760A is connected as SA')
       
    elif elements == '2':
        SG = InstInit(elements)
        Instrument.append(SG)
        print('Anrtisu Signal Generator MG3694C is connected as SG')
        
    elif elements == '3':
        VNA = InstInit(elements)
        Instrument.append(VNA)
        print('Anrtisu Vectro Network Analyzer MS4647B is connected as VNA')

    elif elements == '4':
        PM = InstInit(elements)
        Instrument.append(PM)
        print('Power Meter ThorLabs PM100D is connected as PM')
    
    elif elements == '5':
        LU = InstInit(elements)
        Instrument.append(LU)
        print('Novoptel Laser LU1000 is connected as LU')

    elif elements == '6':
        OSA = InstInit(elements)
        Instrument.append(OSA)
        print('Yokogawa AQ6370D is connected as OSA')
        
    elif elements == '7':
        KA = InstInit(elements)
        Instrument.append(KA)
        print('KEITHLEY Source Meter 2612 is connected as KA')
    
    elif elements == '8':
        SerialNum = ['KORAD KA3005P V5.8 SN:03379314' , 'KORAD KA3005P V5.8 SN:03379289' , 'RND 320-KA3005P V2.0']      
        PS = InstInit(elements)
        data = PS.getIdn()
        print(data)
        if data in SerialNum:
            if data == SerialNum[0]:
                PS1 = PS
                print('Power Supply KA3005P is connected as PS1')
                Instrument.append(PS1)
            elif data == SerialNum[1]:
                PS2 = PS
                print('Power Supply KA3005P is connected as PS2')
                Instrument.append(PS2)
            if data == SerialNum[2]:
                PS3 = PS
                print('Power Supply KA3005 is connected as PS3')
                Instrument.append(PS3)

        
    elif elements == '9':
        CO = InstInit(elements)
        Instrument.append(CO)
        print('CoBrite Tunable Laser is connected as CO')
    elif elements == '10':
        AP = InstInit(elements)
        Instrument.append(AP)
        print('AnaPico AG,APPH20G is connected as AP')
    elif elements == '11':
        GPP = InstInit(elements)
        Instrument.append(GPP)
        print('GW Instek,GPP4323 is connected as GPP')
    else:
        raise ValueError('Invalid Instrument Selected')
        

# =============================================================================
# Select Path for Save Data (pop up window)
# =============================================================================
root = tk.Tk()
path =  filedialog.askdirectory(parent = root)
root.destroy()




# =============================================================================
# Functions
# =============================================================================
#Main Function.Instrument is a list of selected instruments for the measurment
# MeasFunctions(Instrument,path)



#dont forget to close the instrument connection to the PC. (free the socket)

# # # SA.Close()
# # # SG.Close()
VNA.RTL()
VNA.Close()
# # # LU.Close()
PM.Close()
KA.Close()
PS.Close()
# # # PS1.Close()
PS2.Close()
PS3.Close()
# # # OSA.Close()
# # # CO.Close()
# # # AP.Close()
# # # GPP.Close()


# =============================================================================
# Custom Command Section
# =============================================================================

#
# import numpy as np
# import time as t
# import matplotlib.pyplot as plt

# PS.set_Volt(0)

# VthVec= np.linspace(0,1.3,20)
# WaveLength = 1310
# PowerVec_Vth = []

# Vth_Steps = round((1.5 - 0) / 0.02) + 1
# VthVec = np.linspace(0, 1.5, Vth_Steps)

# PS.set_Amp(0.15)
# PS.set_Out('ON')

# for p in range(len(VthVec)):
            
#             PS.set_Volt(VthVec[p])
#             PowerVec_Vth.append(PM.DefaultPowerMeas(WaveLength))

            
# # PS.set_Volt(0)
            
# plt.figure()
# plt.plot(VthVec, PowerVec_Vth)

# KA.set_OutputSourceFunction('a','volt')
# KA.set_OutputSourceFunction('b','amp')
# KA.Close()
# KA.set_OutputSourceFunction('b','volt')

# import vxi11
# rm = vxi11.list_devices()
# print(rm)

# import time as t
# VNA.set_SetAverageState(1,'ON')
# VNA.set_AverageCount(1,2)
# time = VNA.ask_SweepTime()
# t.sleep(time)
# VNA.SaveData('Test'+'_'+'Vvar_'+str(1)+'_'+'Isa_'+str(500),4)
# file = VNA.ask_TransferData('Test'+'_'+'Vvar_'+str(1)+'_'+'Isa_'+str(500),4)
# VNA.SaveTransferData(file,path,'Test'+'_'+'Vvar_'+str(1)+'_'+'Isa_'+str(500),4)
# VNA.DeleteData('Test'+'_'+'Vvar_'+str(1)+'_'+'Isa_'+str(500),4)
# with open("C:/Users/SCT-Labor/Desktop/Martins Meassurments/Test New Function for Tobias Meas/Test_Rename_S_Param/Test_Vvar_1_Isa_500.s4p", "r") as f:
#             lines = f.readlines()
        
# with open("C:/Users/SCT-Labor/Desktop/Martins Meassurments/Test New Function for Tobias Meas/Test_Rename_S_Param/Test_Vvar_1_Isa_500.s4p", "w") as f:
#     for i in range(1,len(lines)):
#         f.write(lines[i])


# import pandas as pd
# import numpy as np
# import time as t
# import matplotlib.pyplot as plt

# name = 'test'
# Vsa_max = 5
# Vsa_min = 0
# Vsa_step =2.5
# Vth_0 = 0.19
# Vth_max = 1
# Steps_Vth  = 0.01
# V_var = 0 
# I_th_max = 0.06
# WaveLength = 1310
# t_th = 5
# Average_points_VNA = 2



# name = name
# nameParam = name + '_Param'
# nameImage = name + '_Image'




# #Define arrays
# # StepnumVar = round((Vvar_max - Vvar_min) / Vvar_step) + 1
# StepnumVec = round((Vsa_max - Vsa_min) / Vsa_step) + 1
# # Vvar_vec = np.linspace(Vvar_min, Vvar_max, StepnumVar)
# Vsa_vec = np.linspace(Vsa_min, Vsa_max, StepnumVec)
# Vsa_vec = Vsa_vec[::-1]
# idx = 0

# #Define the Header and dectionarys to save the data
# df =  pd.DataFrame({'Idx':['idx'],'Var Voltage/V':['V_var'], 'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A':['I_DC_A_PS'], 'Ias_Channel_B/A':['I_DC_B_PS'], 'Power/dBm':['P_opt_static'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})
# data = pd.DataFrame({'Vas/V':['V_DC_PS'], 'Ias_Channel_A/A':['I_DC_A_PS'], 'Ias_Channel_B/A':['I_DC_B_PS'], 'Power/dBm':['P_opt_static']})
# Sdata = pd.DataFrame({'Idx':['idx'], 'name_S_Param':['name_S_Param'], 'path_S_Param':['path_S_Param']})




# #Find the Operation Point

# Vth_0 = Vth_0
# Vth_Steps = round((Vth_max - 0) / Steps_Vth) + 1
# VthVec = np.linspace(0,1,Vth_Steps)


# PowerVec_Vth = []
# Power_3db = []
# volt_3dB = []



# #Predefine some of the instruments 
# Channel1 = 'a' #Set Channel 1 as Channel A
# Channel2 = 'b' # Set Channel 2 as Channel B
# KA.set_OutputSourceFunction(Channel1,'volt')
# KA.set_OutputSourceFunction(Channel2,'volt')
# KA.set_AutoVoltageRange(Channel1, 'ON')
# KA.set_AutoVoltageRange(Channel2, 'ON')
# KA.set_Current(Channel1, 0)
# KA.set_Current(Channel2, 0)
# KA.set_Voltage(Channel1, 0)
# KA.set_Voltage(Channel2, 0)
# PS.set_Volt(0)
# PS.set_Out('ON')
# KA.set_SourceOutput(Channel1,'ON')
# KA.set_SourceOutput(Channel2,'ON')



# Dummy = np.ones(len(Vsa_vec))
# Vvar_vec = Dummy*V_var

# AmpVec1 = []
# AmpVec2 = []
# PowerVec = []
# volt_3dB = []
# Power_3db = []
# PowerVec_Vth = []
# S_Param_Names = []
# S_Param_Names_Path = []
# indexList = []
    
# for j in range(len(Vsa_vec)):
#     KA.set_Voltage(Channel1,Vsa_vec[j])
#     KA.set_Voltage(Channel2,Vsa_vec[j])

    
#     Headaer2 = ['Vth/V','Power/'+PM.ask_PowerUnits()]
#     Headaer3 = ['Power @ -3dB/'+PM.ask_PowerUnits(), 'Voltage @ -3dB/V']
    
#     # Const Value for the Term.elements
#     PS.set_Volt(Vth_0)
#     PS.set_Amp(I_th_max)


#     for p in range(len(VthVec)):
        
#         PS.set_Volt(VthVec[p])
#         PowerVec_Vth.append(PM.DefaultPowerMeas(WaveLength))
#     plt.figure()
#     plt.plot(VthVec, PowerVec_Vth, color = 'green')
#     plt.xlabel('$V_{th}$/V')
#     plt.ylabel('$P_{Out}$/' + PM.ask_PowerUnits())
#     plt.title('Power @ $V_{b}$ = ' + str(Vsa_vec[j]) + ', $V_{a}$ = '+ str(Vsa_vec[j]))
#     plt.grid()
#     figManager = plt.get_current_fig_manager()
#     figManager.window.showMaximized()
#     plt.show()  
#     plt.savefig(path +'/'+ nameImage + '_@_Voltage_psa,psb_'+ str(Vsa_vec[j]) +"_.svg") 
    
    
    
    
#     PowerVec_Vth = np.array(PowerVec_Vth, dtype=np.float32) 
#     data2 = {Headaer2[0]:VthVec, Headaer2[1]:PowerVec_Vth}
#     PG = pd.DataFrame(data2,columns = Headaer2)
#     PG.to_csv(path +'/'+'Vth_@_Voltage_psa_psb_'+str(Vsa_vec[j]) +'_.csv',sep = ',')
    
    

#     d = np.vstack((VthVec, PowerVec_Vth)).T    
#     Power_3db.append(max(PowerVec_Vth)-3)
#     volt_3dB.append(float(d[:,0][d[:,1] == max(d[:,1])] ))
#     Power_3db_array = np.array(Power_3db, dtype=np.float32)
#     volt_3dB_array = np.array(volt_3dB, dtype=np.float32)
#     PowerVec_Vth = []
    
#     #SET Vth @ V_3dB
#     PS.set_Volt(float(d[:,0][d[:,1] == max(d[:,1])] ))
#     t.sleep(t_th)

    
#     VNA.set_SetAverageState(1,'ON')
#     VNA.set_AverageCount(1,Average_points_VNA)
#     time = VNA.ask_SweepTime()
#     t.sleep(time)
#     AmpVec1.append(KA.ask_Current(Channel1))
#     AmpVec2.append(KA.ask_Current(Channel1))
#     PowerVec.append(PM.DefaultPowerMeas(WaveLength)) 
#     VNA.SaveData('S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]), 4)
#     file = VNA.ask_TransferData('S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)
#     VNA.SaveTransferData(file, path, 'S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)
#     VNA.DeleteData('S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j]),4)
    
#     # VNA.SaveData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
#     # file = VNA.ask_TransferData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
#     # VNA.SaveTransferData(file,path,name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
#     # VNA.DeleteData(name+'_'+'Vvar_'+str(Vvar_vec[i])+'_'+'Vsa_'+str(Vsa_vec[j]),4)
    
    
#     S_Param_Names.append('S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p')
#     S_Param_Names_Path.append('"'+path+'/'+'S_Parameters_V_Var_'+str(Vvar_vec[j])+'__V_DC_'+str(Vsa_vec[j])+'.s4p'+'"')
#     indexList.append(idx)
#     idx += 1
#     t.sleep(1)
# ValueVec = np.ones(len(Vsa_vec))*Vvar_vec[j]
# PowerVec = np.array(PowerVec, dtype=np.float32)
# df2 = pd.DataFrame({'Idx':indexList, 'Var Voltage/V': ValueVec, 'Vas/V': Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm': PowerVec, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
# data2 = pd.DataFrame({'Vas/V':Vsa_vec, 'Ias_Channel_A/A': AmpVec1, 'Ias_Channel_B/A': AmpVec2, 'Power/dBm':PowerVec})
# Sdata2 = pd.DataFrame({'Idx':indexList, 'name_S_Param':S_Param_Names, 'path_S_Param':S_Param_Names_Path})
# data = data.append(data2)
# df = df.append(df2)
# Sdata = Sdata.append(Sdata2)
# data3 = {Headaer3[0]:Power_3db_array, Headaer3[1]:volt_3dB_array}
# PJ = pd.DataFrame(data3,columns = Headaer3)
# PJ.to_csv(path +'/'+'Vth_3dB_@_V_psb_psa_'+str(Vsa_vec[j]) +'_.csv',sep = ',')




# fig, (ax1, ax2) = plt.subplots(2)
# ax1.plot(df2['Vas/V'],df2['Ias_Channel_A/A'],linewidth=3.0, color = 'red', label = 'Channel A')
# ax1.plot(df2['Vas/V'],df2['Ias_Channel_B/A'],linewidth=3.0, color = 'blue', label = 'Channel B')
# ax2.plot(df2['Vas/V'],df2['Power/dBm'],linewidth=3.0)
# ax1.set( ylabel = "$I_{Source Meter}$/A")
# ax1.legend(loc = 'best')
# ax2.set( ylabel = 'Power/dB')
# ax2.set( xlabel = "$V_{Source Meter}$/V")
# ax1.grid()
# ax2.grid()
# fig.suptitle("@ $V_{Var}$ = "+str(Vvar_vec[j])+" V")
# figManager = plt.get_current_fig_manager()
# figManager.window.showMaximized()
# plt.savefig(path +'/'+ nameImage +'_@'+ str(Vvar_vec[j]) +".svg")   
# plt.close()



# #Shut the instruments down and save the csv   
# PS.set_Volt(0)
# PS.set_Out('OFF')
# VNA.RTL()
# KA.set_Voltage(Channel1, 0)
# KA.set_Voltage(Channel2, 0)
# KA.set_SourceOutput(Channel1,'OFF')
# KA.set_SourceOutput(Channel2,'OFF')
