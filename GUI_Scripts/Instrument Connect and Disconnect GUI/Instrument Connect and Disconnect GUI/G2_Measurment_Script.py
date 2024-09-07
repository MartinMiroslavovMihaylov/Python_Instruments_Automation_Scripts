from App_Constructor import App, DisconnectApp



app = App()
app.mainloop()
# Inst, ListDissconnect =  app.ExtractData()

dictTest = {}
dictTest =  app.ExtractData()


# dictTest[' Power Supply KA3005 '].getIdn()
# dictTest[' Power Supply KA3005 '].getIdn()
# dictTest[' CoBrite Tunable Laser '].Identification()
# dictTest[' 4-Channels Power Suppy GPP4323 '].getIdn()
# dictTest[' 4-Channels Power Suppy GPP4323 '].Close()
# dictTest[' Anritsu Signal Generator MG3694C '].ask('*IDN?')
# dictTest[" Anrtisu Spectrum Analyzer MS2760A "].ask_MarkerExcursionState()
# dictTest[' Power Meter ThorLabs PM100D '].ask_PowerUnits()
# dictTest[" Yokogawa Optical Spectrum Analyzer AQ6370D "].ask_CenterWavelenght()
# dictTest[" Novoptel Laser LU1000 "].ask_Power(1)
# dictTest[' Anritsu Vectro Analyzer MS4647B '].getIdn()
# dictTest[' AnaPico AG,APPH20G '].getIdn()



# DissApp = DisconnectApp(app.ExtractData())
# DissApp.mainloop()



# Names of Power Sources_

PowerSource_3Vcc = ' 4-Channels Power Suppy GPP4323_5'
PowerSource_2Vcc = ' 4-Channels Power Suppy GPP4323_1'

# Set GPP4 channel Power Supply for Vcc2, Vcc3 and Vcc4
dictTest[PowerSource_3Vcc].set_Volt(1, 0)
dictTest[PowerSource_3Vcc].set_Amp(1,0.1)
dictTest[PowerSource_3Vcc].set_Out(1, "OFF")

dictTest[PowerSource_3Vcc].set_Volt(2, 0)
dictTest[PowerSource_3Vcc].set_Amp(2,0.1)
dictTest[PowerSource_3Vcc].set_Out(2, "OFF")

dictTest[PowerSource_3Vcc].set_Volt(3, 0)
dictTest[PowerSource_3Vcc].set_Amp(3,0.1)
dictTest[PowerSource_3Vcc].set_Out(3, "OFF")



# Set GPP4 channel Power Supply for Vcc and Vdc
dictTest[PowerSource_2Vcc].set_Volt(1, 0)
dictTest[PowerSource_2Vcc].set_Amp(1,0.1)
dictTest[PowerSource_2Vcc].set_Out(1, "OFF")

dictTest[PowerSource_2Vcc].set_Volt(2, 0)
dictTest[PowerSource_2Vcc].set_Amp(2,0.1)
dictTest[PowerSource_2Vcc].set_Out(2, "OFF")



dictTest[PowerSource_3Vcc].Close()
dictTest[PowerSource_2Vcc].Close()



# # Set VNA Anritsu
# # dictTest[' Anritsu Vectro Analyzer MS4647B '].getIdn()
# # dictTest[' Anritsu Vectro Analyzer MS4647B '].getIdn()
# # dictTest[' Anritsu Vectro Analyzer MS4647B '].RTL()
# # dictTest[' Anritsu Vectro Analyzer MS4647B '].Close()



# import keyboard
# import pandas as pd


# dataDic = {}
# # # dataDic["Laser Data"] = []
# # dataDic["Power Meter Data dBm"] = []q
# # dataDic["Power Meter Data W"] = []
# # dataDic["Source Meter Current"] = []
# # dataDic["Source Meter Voltage"] = []
# dataDic["Steps"] = []


 

# # # dictTest[' 4-Channels Power Suppy GPP4323 '].set_Out(1, "ON")

# # Initial Conditions
# dictTest[PowerSource_3Vcc].set_Volt(1, 2.3)
# dictTest[PowerSource_3Vcc].set_Volt(2, 2)
# dictTest[PowerSource_3Vcc].set_Volt(3, 2)

# dictTest[PowerSource_2Vcc].set_Volt(1, 2)
# dictTest[PowerSource_2Vcc].set_Volt(2, 2)


# count = 1
# val = 0.1
# while True:
#     dictTest[PowerSource_3Vcc].set_Out(1, "ON")
#     dictTest[PowerSource_3Vcc].set_Out(2, "ON")
#     dictTest[PowerSource_3Vcc].set_Out(3, "ON")

#     dictTest[PowerSource_2Vcc].set_Out(1, "ON")
#     dictTest[PowerSource_2Vcc].set_Out(2, "ON")

    

#     # Read the key press once
#     key = keyboard.read_key()

    
#     if key == "n": 

#         # dictTest[PowerSource_3Vcc].set_Volt(1, dictTest[PowerSource_3Vcc].ask_Volt(1) + 0.5)
#         dictTest[PowerSource_3Vcc].set_Volt(2, dictTest[PowerSource_3Vcc].ask_Volt(2) + 0.5)
#         dictTest[PowerSource_3Vcc].set_Volt(3, dictTest[PowerSource_3Vcc].ask_Volt(3) + 0.5)

#         dictTest[PowerSource_2Vcc].set_Volt(1, dictTest[PowerSource_2Vcc].ask_Volt(1) + 0.5)
#         dictTest[PowerSource_2Vcc].set_Volt(2, dictTest[PowerSource_2Vcc].ask_Volt(2) + 0.5)

#         dataDic["Steps"].append(count)
#         count = count + 1 
#         val = val + 0.5
#         print(val)
        
#     elif key == "q":

        
#         # Set GPP4 channel Power Supply for Vcc2, Vcc3 and Vcc4
#         dictTest[PowerSource_3Vcc].set_Volt(1, 0)
#         dictTest[PowerSource_3Vcc].set_Amp(1,0.1)
#         dictTest[PowerSource_3Vcc].set_Out(1, "OFF")

#         dictTest[PowerSource_3Vcc].set_Volt(2, 0)
#         dictTest[PowerSource_3Vcc].set_Amp(2,0.1)
#         dictTest[PowerSource_3Vcc].set_Out(2, "OFF")

#         dictTest[PowerSource_3Vcc].set_Volt(3, 0)
#         dictTest[PowerSource_3Vcc].set_Amp(3,0.1)
#         dictTest[PowerSource_3Vcc].set_Out(3, "OFF")



#         # Set GPP4 channel Power Supply for Vcc and Vdc
#         dictTest[PowerSource_2Vcc].set_Volt(1, 0)
#         dictTest[PowerSource_2Vcc].set_Amp(1,0.1)
#         dictTest[PowerSource_2Vcc].set_Out(1, "OFF")

#         dictTest[PowerSource_2Vcc].set_Volt(2, 0)
#         dictTest[PowerSource_2Vcc].set_Amp(2,0.1)
#         dictTest[PowerSource_2Vcc].set_Out(2, "OFF")

#         print("Quit")
#         break


# # dictTest[PowerSource_3Vcc].Close()
# # dictTest[PowerSource_2Vcc].Close()
# # csv = pd.DataFrame.from_dict(dataDic)

# # csv.to_csv('100724_MeasurmentData_Struc1.csv', index=False, sep = ";")  

# # dictTest[PowerSource_3Vcc].set_Out(1, "ON")
# # dictTest[PowerSource_3Vcc].set_Out(2, "ON")
# # dictTest[PowerSource_3Vcc].set_Out(3, "ON")

# # dictTest[PowerSource_2Vcc].set_Out(1, "ON")
# # dictTest[PowerSource_2Vcc].set_Out(2, "ON")

# # dictTest[PowerSource_3Vcc].set_Volt(1, 2.3)
# # dictTest[PowerSource_3Vcc].set_Volt(2, 4)
# # dictTest[PowerSource_3Vcc].set_Volt(3, 3.3)

# # dictTest[PowerSource_2Vcc].set_Volt(1, 3)
# # dictTest[PowerSource_2Vcc].set_Volt(2, 5)

# # dictTest[PowerSource_2Vcc].Close()
# # dictTest[PowerSource_3Vcc].Close()