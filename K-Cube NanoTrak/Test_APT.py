import numpy as np
import time
import clr

import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.PiezoCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.PiezoCLI import *
from System import Decimal  # necessary for real world units



def main():
    # serial_num = str("SerialNumberOfNanoTrak")



    # DeviceManagerCLI.BuildDeviceList()
    try:

        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "SerialNumberOfNanoTrak"

        # Connect, begin pulling and enable
        device = KCubePiezo.CreateKCubePiezo(serial_no)

        device.Connect(serial_no)

        # Get device inormation and display description
        device_info = device.GetDeviceInfo()
        print(device_info.Description)

        # Start polling anf enable
        device.StartPolling(250) # 250ms polling rate
        time.sleep(25)
        device.EnableDevie()
        time.sleep(0.25) # Wait for device to enablee


        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(10000) # 10 sec timeout
            assert device.IsSettingsInitialized() is True

        # Load the device configuration
        device_config = device.GetPiezoConfiguration(serial_no)

        # This shows how to obtaain the device settings
        device_setting = device.PiezoDeviceSettings


        # Set the Zero point of the device
        print("Setting Zero Point")
        device.SetZero()

        # Get maximum voltge output of the KPZ
        max_voltage = device.GetMaxOutputVoltage() #Stored as .NET Decimal

        # Go to a voltage
        dev_voltage = Decimal(15.0)
        print(f'Going to voltage {dev_voltage}')

        if dev_voltage != Decimal(0) and dev_voltage <= max_voltage:
            device.SetOutputVoltage(dev_voltage)
            time.sleep(1.0)
            print(f'Move to Voltage {device.GetOutputVoltage()}')
        else:
            print(f'Voltagee must be between 0 and {max_voltaage}')

        #Stop Polling and Disconnect
        device.StopPolling()
        device.Disconnect()
    except Exception as e:
        print(e)



        
if __name__ == "__main__":
    main()