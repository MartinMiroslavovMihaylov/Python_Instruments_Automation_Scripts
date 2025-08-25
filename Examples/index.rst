Examples
========

Python code example how to connect to ThorLabs Power Meter PM100D.
Here's a simple Python code example how to connect and disconnect from an instrument:

.. code-block:: python

   from Instruments_Libraries.PM100D import PM100D
   PM = PM100D("Serial Number Of the ThorLabs Power Meter PM100D")
   PM.getIdn()
   PM.Close()


Full Code Examples:
-------------------

.. toctree::
   :maxdepth: 1

   Example_MS2760A
   Example_Powersupply_advanced
   Example_Powersupply_GPP4323
   Example_Powersupply_Keithly
   Example_Thorlabs_PM100D