from App_Constructor import App, DisconnectApp



#######################################################
# How to use the GUI Automation Controll
# Call the GUI App and select your instruments 
# The selected instruments will be connected and you will see an
# green Massage in the GUI Massage Box.
# After you see the massage you can Close the app with the Close button
#######################################################

# Call GUI App
app = App()
app.mainloop()

# The devices will be given back in a dictionary
dictTest = {} # Create empty dictionary to store the devices
dictTest =  app.ExtractData() # Call the app ExtractData Function to give you the Connected Devices back


# # Some Test function to all the Instruments IDs to check if you connect them propperly 
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



#######################################################
# How to use the GUI Automation Controll DisconnectApp
# Call the GUI App, the instruments the you have store in 
# your Dictionry will be listed as seperate buttons on the side.
# Click on the buttons one by one to disconnect the Instrument 
# After Disconnecting, close the App with the Close button
#######################################################

DissApp = DisconnectApp(app.ExtractData()) # Call Disconnect App and give the list of instruments as arg
DissApp.mainloop()
