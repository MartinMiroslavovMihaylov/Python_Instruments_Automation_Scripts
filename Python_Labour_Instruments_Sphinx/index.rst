.. Instruments Automatisation Libraries documentation master file, created by
   sphinx-quickstart on Thu Dec  9 12:15:13 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Instruments Automatisation Libraries's documentation!
===================================================================

This is a python Library that allow the users to controll the following 
Instruments:
	- Anrtisu Spectrum Analyzer MS2760A
	- Anritsu Signal Generator MG3694C
	- Rohde and Schwarz Signal Generator SMA100B 
	- Anritsu Vector Network Analyzer MS4647B
	- Yokogawa Optical Spectrum Analyzer AQ6370D
	- Power Meter ThorLabs PM100D
	- KEITHLEY Source Meter 2612
	- Novoptel Laser LU1000
	- CoBrite Tunable Laser
	- Power Supply RD3005
	- Power Supply KA3005
	- Power Supply KA3005p
	- 4 Channels Power Suppy GPP4323
	- AnaPico AG APPH20G
	
	
	
	
	
Python Libraries
===================================================================

This Python Librarys can be used with Python Version 3.10.0 or newr. 
For the Moment you will need the following python Libraries. ::

	pip install ftd2xx
	pip install oct2py
	pip install pyserial
	pip install serial-tool
	pip install python-vxi11
	pip install PyVISA
	pip install sockets
	pip install pandas
	pip install matplotlib
	pip install numpy
	pip install matplotlib
	

Programms needed when using the Novoptel Laser
===================================================================

To use the Novoptel Laser LU1000, the user must install octave. At the 
moment what the Novoptel documentation mentions, is that Octave version 
6.1.0 is required. Furthermore, the user must check in the path variables 
of the operating system whether the Octave path is set correctly...
Windows Path - 'C:\Program Files\GNU Octave\Octave-6.1.0\mingw64\bin'
For more information see: Python script by https://www.novoptel.de/Home/Downloads_en.php 


How to use the GUI 
===================================================================

In folder "GUI_Scripts/Instrument Connect and Disconnect GUI" you will find an customtkinter GUI write 
by me to help you faster connect and disconnect to different devices. You can copy the hole "Instrument Connect and Disconnect GUI"
folder to your prefered location. Inside you will see an main.py. You can open the main.py in your Python IDE. To use the GUI 
you will be needing two more extra library. ::
	pip install customtkinter
	pip install pillow

After installing it you can run the main.py. An GUI window will open with list of instruments. Choose your instrument 
and press select. You can choose more the one instrument! Afterwords press the green button Connect. This will automatically 
search your ports for the devices you selected. Please be shure to connect the devices to your PC/Laptop befor you connect otherwise you will 
be not able to find any devices! After some time you will see an green text in the box bewol your selected devices with "Instruments are Connected !". 
When you get this massage you can now close the GUI with Close and all the devices will be saved in your dictionary "dictTest" see main.py. 
You now can use the dictionary to call an device function for example 

Python code example to how to set frequency on R&S SMA100B
----------------------------------------------------------------------------

Here's a simple Python code example:

.. code-block:: python


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
	
	dictTest[' Rohde and Schwarz SMA100B '].set_freq_CW(FreqVec[i], "GHz")
	dictTest[' Rohde and Schwarz SMA100B '].Close()


How to use the code without the GUI
===================================================================

If you wann use the codes without the GUI, you can do it too. You can copy the library of the instrument 
you wanna use from "GUI_Scripts/Instrument Connect and Disconnect GUI/InstrumentControl". To connect 
to your instrument you will still need the python librarys given in the section "Python Libraries"!
Then you need to know what kind of connection your instrument have to your PC/Laptop Ethernet, USB-C,
USB-A, RS323 etc. After you find out you can connect to your instrument and use all the function from 
the choosen instrument library. See the code bewol for a short example on how to connect use some function 
and then close the connection to your instrument. 


Python code example to how to connect to ThorLabs Power Meter PM100D
----------------------------------------------------------------------------

Here's a simple Python code example how to connect and disconnect from an instrument:

.. code-block:: python

   from PM100D import PM100D
   PM = PM100D("Serial Number Of the ThorLabs Power Meter PM100D")
   PM.getIdn()
   PM.Close()

Instruments
===================================================================

.. include:: rst/MS2760A.rst
   

.. include:: rst/MG3694C.rst


.. include:: rst/SMA100B.rst


.. include:: rst/MS4647B.rst


.. include:: rst/AQ6370D.rst


.. include:: rst/PM100D.rst


.. include:: rst/KEITHLEY2612.rst


.. include:: rst/LU1000.rst


.. include:: rst/CoBrite.rst


.. include:: rst/KA3005.rst


.. include:: rst/KA3005p.rst


.. include:: rst/RD3005.rst


.. include:: rst/GPP4323.rst


.. include:: rst/APPH20G.rst

		

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
