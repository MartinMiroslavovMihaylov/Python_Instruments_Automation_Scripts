from App_Constructor import App, DissconnectApp



app = App()
app.mainloop()

# Inst, ListDissconnect =  app.ExtractData()

dictTest = {}
dictTest =  app.ExtractData()


# path = os.getcwd()
# nameCOM = '\COM'
# nameOCT6 = '\OCT6'


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




# # Loop data live update monitor with ThorLabs PowerMeter and LU1000 Laser 
# import pandas as pd 
# import numpy as np
# import matplotlib.pyplot as plt 
# import time
# import csv

# # LU = dictTest[" Novoptel Laser LU1000 "]
# PM = dictTest[" Power Meter ThorLabs PM100D "]

# DataDic = {}
# fieldnames = ["DataX", "DataY"]
# DataDic[fieldnames[0]] = [0]
# DataDic[fieldnames[1]] = [0]
# df = pd.DataFrame.from_dict(DataDic)


# # LU.set_Power(1,6.5)
# # LU.set_LaserChannel(1,0)
# # LU.set_Gridspacing(1,1)
# # GridSpacing = LU.ask_Gridspacing(1)
# # LU.set_Frequency(1,193.87)
# # LU.set_LaserOutput(1,'ON')
# Power = PM.DefaultPowerMeas(1550)
# # pd.DataFrame.from_dict(DataDic)
# # df = pd.DataFrame.from_dict(DataDic)
# # df.to_csv('my_csv.csv', mode='a', header=True)

# with open('File.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()



# for i in range(60):
#     # DataDic[fieldnames[1]].append(PM.DefaultPowerMeas(1550))
#     # DataDic[fieldnames[0]].append(LU.ask_Power(1))
#     # DataDic[fieldnames[0]].append(i)
#     with open('File.csv', 'a') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#         info = {
#             "DataX": i,
#             "DataY": PM.DefaultPowerMeas(1550)
#                 }
#         csv_writer.writerow(info)
    
#     time.sleep(3)
    

# # LU.set_LaserOutput(1,'OFF')
# # DissApp = DissconnectApp(app.ExtractData())
# # DissApp.mainloop()








# # Inst[0].set_Out(1, 'OFF')
# # .Close()
                    
# # PM[0].ask_AdapterType()

# # DissApp = DissconnectApp(app.ExtractData())
# # DissApp.mainloop()

# # print(app.ExtractData())


# # if ' 4-Channels Power Suppy GPP4323 ' in dictTest.keys():
# #     print("ja")
# # else:
# #     raise ValueError("Nothing to see here")



# # ListInstruments = ["Anrtisu Spectrum Analyzer MS2760A", "Anritsu Signal Generator MG3694C", "Anritsu Vectro Analyzer MS4647B", "Power Meter ThorLabs PM100D", "Novoptel Laser LU1000", "Yokogawa Optical Spectrum Analyzer AQ6370D", "KEITHLEY Source Meter 2612", "Power Supply KA3005", "CoBrite Tunable Laser", "AnaPico AG,APPH20G", "4-Channels Power Suppy GPP4323" ]

# # for i in range(len(ListInstruments)):
# #     match ListInstruments[i]:
# #         case "Anrtisu Spectrum Analyzer MS2760A":
# #             print("ja")
# #         case "Anritsu Signal Generator MG3694C":
# #             print("2")
# # for idx, element in enumerate(ListInstruments):
# #     print(idx,element)