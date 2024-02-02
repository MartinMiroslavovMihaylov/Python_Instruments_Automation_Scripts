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
	- Anritsu Vectro Analyzer MS4647B
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
	pip install python-vxi11
	pip install PyVISA
	pip install sockets
	pip install pandas
	pip install matplotlib
	pip install numpy

How to use 
===================================================================

Python code example to how to connect to ThorLabs Power Meter PM100D
-------------------

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
