# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:14:47 2022

@author: Martin.Mihaylov 
"""



'''
The script is take https://github.com/uberdaff/kd3005p/blob/master/kd3005p.py
and cosmetically preprocessed.
#  Copyright 2017 uberdaff
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
# Requirement: pyserial
#
# getIdn() - Get instrument identification
# set_Volt(tal) - Set the voltage on the output
# ask_Volt() - Get the 'set' voltage
# read_Volt() - Get a measurement of the voltage
# set_Amp(tal) - Set the current limit
# ask_Amp() - Get the 'set' current limit
# read_Amp() - Get a measurement of the output current
# set_Out(bool) - Set the state of the output
# set_Ocp(bool) - Set the state of the over current protection
# ask_Status() - Get the state of the output and CC/CV
'''

import sys
import time
import serial

class RD3005:
    isConnected = False
    psu_com = None
    status = {}
    
    def __init__(self, psu_com):
        '''
        

        Parameters
        ----------
        psu_com : str
            COM Port

        Returns
        -------
        None

        '''
        try:
            psu_com = serial.Serial(
                port=psu_com,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            psu_com.isOpen()
            self.psu_com = psu_com
            self.isConnected = True
            self.status=self.ask_Status()
        except:
            print("COM port failure:")
            print(sys.exc_info())
            self.psu_com = None
            self.isConnected = False
    
    def Close(self):
        self.psu_com.close()
        print('Instrument KD3005 is closed!')
    
    def serWriteAndRecieve(self, data, delay=0.05): 
        self.psu_com.write(data.encode())
        out = ''
        time.sleep(delay)
        while self.psu_com.inWaiting() > 0:
            out += self.psu_com.read(1).decode()
        if out != '':
            return out
        return None
    
    def getIdn(self):
        '''
        

        Returns
        -------
        TYPE  str
            Instrument identification 

        '''
        return self.serWriteAndRecieve("*IDN?", 0.3)
    
    def set_Volt(self, voltage, delay=0.01):
        '''
        

        Parameters
        ----------
        voltage : int/float
            Set the voltage on the Display
            
        delay : 0.01s Delay 
            

        Returns
        -------
        None

        '''
        self.serWriteAndRecieve("VSET1:"+"{:1.2f}".format(voltage))
        time.sleep(delay) 
    
    def ask_Volt(self):
        '''
        

        Returns
        -------
        TYPE float
            Voltage set.

        '''
        return float(self.serWriteAndRecieve("VSET1?"))
    
    def read_Volt(self):
        '''
        

        Returns
        -------
        TYPE float
            Voltage Measured

        '''
        return float(self.serWriteAndRecieve("VOUT1?"))
    
    
    def set_Amp(self, amp, delay=0.01):
        '''
        

        Parameters
        ----------
        voltage : int/float
            Set the current on the Display
            
        delay : 0.01s Delay 
            

        Returns
        -------
        None

        '''
        self.serWriteAndRecieve("ISET1:"+"{:1.3f}".format(amp))
        time.sleep(delay) 
    
    def ask_Amp(self):
        '''
        

        Returns
        -------
        TYPE float
            current set.

        '''
        return float(self.serWriteAndRecieve("ISET1?"))
    
    def read_Amp(self):
        '''
        

        Returns
        -------
        TYPE float
            Current Measured

        '''
        return float(self.serWriteAndRecieve("IOUT1?"))
    
    def set_Out(self, state):
        '''
        

        Parameters
        ----------
        state : str (ON/OFF)
            Turn Output ON and OFF

        Returns
        -------
        None.

        '''
        if(state == 'ON'):
            self.serWriteAndRecieve("OUT1")
        elif(state == 'OFF'):
            self.serWriteAndRecieve("OUT0")
    
    def set_Ocp(self, state):
        '''
        

        Parameters
        ----------
        state : str (ON/OFF)
            Set the state of the over current protection ON and OFF

        Returns
        -------
        None.

        '''
        if(state == 'ON'):
            self.serWriteAndRecieve("OCP1")
        elif(state == 'OFF'):
            self.serWriteAndRecieve("OCP0")
    
    def ask_Status(self):
        '''
        

        Returns
        -------
        TYPE
            Get the state of the output and CC/CV

        '''
        stat = ord(self.serWriteAndRecieve("STATUS?")[0])
        if (stat&(1 << 0))==0:
            self.status["Mode"]="CC"
        else:
            self.status["Mode"]="CV"
        if (stat&(1 << 6))==0:
            self.status["Output"]="Off"
        else:
            self.status["Output"]="On"
        return self.status

# =============================================================================
# Get/Save Data
# =============================================================================

    def get_data(self):
        '''
        

        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured voltage and current. 

        '''
        OutPut = {}
        Voltage = self.read_Volt()
        Current = self.read_Amp()
        OutPut['Voltage/V'] = Voltage
        OutPut['Current/A'] = Current
        
        return  OutPut       
        
    