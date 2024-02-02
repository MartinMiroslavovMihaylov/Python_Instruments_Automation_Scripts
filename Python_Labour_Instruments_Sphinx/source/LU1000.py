# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:04:21 2021

@author: Martin.Mihaylov
"""
from __future__ import print_function
import os       
import numpy as np                          
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" 
import oct2py
from oct2py import Oct2Py
oc = Oct2Py()
import os 






def Paths():
    import tkinter as tk 
    from tkinter import filedialog


    # =============================================================================
    # Select the Paths to COM and OCT6
    # =============================================================================
    print('''
          Paths of the COM Folder and OCT6 Folder cant be found in the directory 
          where LU1000.py is saved. Please select the right directory.
          
          1) - Select COM directory
          2) - Select OCT6 directory
    
          ''')

    #Path COM
    root = tk.Tk()
    COM = filedialog.askdirectory(parent = root,title = 'Select COM Diretory: ')
    root.destroy()
    #COM = 'C:/Users/marti/OneDrive/Desktop/WHK Martin/Auto_Measurement/InstrumentControl/COM'
    
    
    
    #Path OCT6
    root = tk.Tk()
    OCT6 = filedialog.askdirectory(parent = root,title = 'Select COM Diretory: ')
    root.destroy()
    #OCT6 = 'C:/Users/marti/OneDrive/Desktop/WHK Martin/Auto_Measurement/InstrumentControl/OCT6'
    
    return COM, OCT6
    


path = os.getcwd()
nameCOM = '\COM'
nameOCT6 = '\OCT6'



if os.path.exists(path+nameCOM) == True:
    PathCOM = path+nameCOM
    PathOCT6 = path+nameOCT6
else:
    PathCOM , PathOCT6 = Paths()
    

'''
Initialize Connection to the Instrument whit the Octave engine.
Selected COM and OCT6 Paths are needed!!!
'''
oc.addpath(PathCOM); 
oc.addpath(PathOCT6);  

class LU1000:


    
    print(
        '''
        ################ ATTENTION ################
        
        Befor using the Librarys you need to:

           1 - Octave 6.1.0 needed!!!
           2 - PATH env to 'C:\Program Files\GNU Octave\Octave-6.1.0\mingw64\bin'
           3 - pip install ftd2xx , pip install pypiwin32
           
       For more information see: Python script by https://www.novoptel.de/Home/Downloads_en.php 
         
        ################ ATTENTION ################
        '''
            )
    
    print(
            '''
            
            In the Class Lib ypu need to give the Paths to COM and OCT6 folders.
            The folders are comming together whit the lib. If not download them from:
                https://www.novoptel.de/Home/Downloads_en.php 
                
            '''
            )
            
    def __init__(self):

        

# =============================================================================
#         stri = input('Select LU1000 device (0) or look it up in LastDevLU.mat (1 or "enter"):')
#         if stri=='0':
#             oc.initlu(0)
#         else:
# =============================================================================
        oc.initlu()
        DevDescrLU  = oc.load('LastDevLU.mat',  'LastDevDescr')['LastDevDescr']
        
        print(DevDescrLU) 
        
    
    
    
    
    def Close(self):
        '''
        

        Returns
        -------
        str
            Close connection 

        '''
        
        ok = oc.closelu()
        print(ok, sep='\n')
        
    
    
    
    
# =============================================================================
# ASK 
# =============================================================================
    def ask_Power(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Ask Sets or returns the laser module’s current optical power
            in dBm*100

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+49, nout=2)
            return float(res/100)
        elif laser == 2:
            res, ok = oc.readlu(256+49, nout=2)
            return float(res/100)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_LaserOutput(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        str 
            Laser emable('ON') or laser diseble('OFF') 

        '''
        if laser == 1:
            res, ok = oc.readlu(128+50, nout=2)
            if res == 0.0:
                print('OFF')
            else:
                print('ON')
        elif laser == 2:
            res, ok = oc.readlu(256+50, nout=2)
            if res == 0.0:
                print('OFF')
            else:
                print('ON')
        else: 
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_ControllerTemp(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Controller module temperature in Celsiusx16

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+51, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+51, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def ask_Gridspacing(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Grid spacing in GHz*10

        '''
        
        
        if laser == 1:
            res, ok = oc.readlu(128+52, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+52, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_FirstChannFreqTHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message
            

        Returns
        -------
        res : float
            First channel’s frequency, THz

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+53, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+53, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_FirstChannFreqGHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            First channel’s frequency, GHz*10

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+54, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+54, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_ChannelFreqTHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Ask channel Frequency in THz

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+64, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+64, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def ask_ChannelFreqGHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Returns channel’s frequency as GHZ*10

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+65, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+65, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_OpticalPower(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Returns the optical power encoded as dBm*100

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+66, nout=2)
            return float(res/100)
        elif laser == 2:
            res, ok = oc.readlu(256+66, nout=2)
            return float(res/100)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_Temperature(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Returns the current temperature encoded as °C*100.

        '''
       
        if laser == 1:
            res, ok = oc.readlu(128+67, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+67, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_MinOpticalOutputPower(self):
        '''
        

        Returns
        -------
        res : float
            Ask minimum possible optical power setting

        '''
        res, ok = oc.readlu(128+80, nout=2)
        return res

    
    
    
    
    def ask_MaxOpticalOutputPower(self):
        '''
        

        Returns
        -------
        res : float
            Maximum possible optical power setting

        '''
    
        res, ok = oc.readlu(128+81, nout=2)
        return res
   
    
    
    
    
    def ask_LaserFirstFreqTHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser’s first frequency, THz

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+82, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+82, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
      
    
    
    
    
    def ask_LaserFirstFreqGHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser’s first frequency, GHz*10

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+83, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+83, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    def ask_minFreqLaser(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            min possible frequency.

        '''
        
        
        if laser in [1,2]:
            THz = self.ask_LaserFirstFreqTHz(laser)
            GHz = self.ask_LaserFirstFreqGHz(laser)
            Freq = THz + GHz*1e-4
            return Freq
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    def ask_LaserLastFreqTHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
           Laser’s last frequency, THz

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+84, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+84, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def ask_LaserLastFreqGHz(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2


        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Laser’s last frequency, GHz*10

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+85, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+85, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
        
        
    def ask_maxFreqLaser(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float 
            max possible frequency

        '''
        
        
        if laser in [1,2]:
            THz = self.ask_LaserLastFreqTHz(laser)
            GHz = self.ask_LaserLastFreqTHz(laser)
            Freq = THz + GHz*1e-4
            return float(Freq)
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    def ask_LaserMinGridFreq(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            Laser’s minimum supported grid spacing, GHz*10

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+86, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+86, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
    def ask_Frequency(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message
            
        Returns
        -------
        Freq : float
            Calculate and return Frequency on the selected channel

        '''
        
        sLaser = [1,2]
        if laser in sLaser:
            THz = float(self.ask_ChannelFreqTHz(laser))
            GHz = float(self.ask_ChannelFreqGHz(laser))
            Freq = THz + GHz*1e-4
            return Freq
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    def ask_LaserChannel(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2


        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : foat
            Selected Channel Number

        '''
        
        if laser == 1:
            res, ok = oc.readlu(128+48, nout=2)
            return float(res)
        elif laser == 2:
            res, ok = oc.readlu(256+48, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
        

    def ask_Whispermode(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : foat
            Whispermode Status


        '''
        if laser == 1:
            res, ok = oc.readlu(128+108, nout=2)
            data = float(res)
            if data == 0:     
                return 'OFF'
            else:
                return 'ON'
        elif laser == 2:
            res, ok = oc.readlu(256+108, nout=2)
            return float(res)
        else:
            raise ValueError('Unknown input! See function description for more info.')
    

    
    
# =============================================================================
# SET
# =============================================================================

    def set_Power(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : float
            Sets the laser module’s current optical power
            in dBm

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        
        value = float(value)
        if laser == 1:
            if value>10:
                print('''
                      ################# Worning #################
                      
                      More then 10dBm is critical for some devices!
                      ''')
                comf = input('Are you sure you wanna continue (yes/no)? ')
                comf = comf.lower()
                if comf == 'yes':
                    value = value*100
                    ok = oc.writelu(128+49, int(value))
                    print('Power = '+str(float(value/100))+'dBm')
                else:
                    pass
            elif value <= 10 and value >= 6:
                value = value*100
                ok = oc.writelu(128+49, int(value))
                print('Power = '+str(float(value/100))+'dBm')
            else:
                raise ValueError('Unknown input! See function description for more info.')
        elif laser == 2:
            if value>10:
                print('''
                      ################# Worning #################
                      
                      More then 10dBm is critical for some devices!
                      ''')
                comf = input('Are you sure you wanna continue (yes/no)? ')
                comf = comf.lower()
                if comf == 'yes':
                    value = value*100
                    ok = oc.writelu(256+49, int(value))
                    print('Power = '+str(float(value/100))+'dBm')
                else:
                    pass
            elif value <= 10 and value >= 6:
                value = value*100
                ok = oc.writelu(256+49, int(value))
                print('Power = '+str(float(value/100))+'dBm')
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
    
    
    
    
    def set_LaserChannel(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : int
            Sets or returns the laser module’s current channel
             value = select channel value

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
    
        if laser == 1:
            oc.writelu(128+48, value)
             
        elif laser == 2:
            oc.writelu(256+48, value) 
        else:
            raise ValueError('Unknown input! See function description for more info.')

    
    
    
    
    def set_LaserOutput(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : int/str
            Turn Laser N output ON/OFF
            value = 'ON'|'OFF'|1|0

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
        
        sValue = ['ON','OFF',1,0]
        if value in sValue:
            if laser == 1:
                if value == 1 or value == 'ON':
                    oc.writelu(128+50, 8)
                    print('### Laser 1 is ON ###')
                else:
                    oc.writelu(128+50, 0)
                    print('### Laser 1 is OFF')
            elif laser == 2:
                if value == 1 or value == 'ON':
                    oc.writelu(256+50, 8) 
                    print('### Laser 2 is ON ###')
                else:
                    oc.writelu(256+50, 0)   
                    print('### Laser 2 is OFF ###')
        else:
            raise ValueError('Unknown input! See function description for more info.')
        
    
    
    
    
# =============================================================================
# Test Write Grid
# =============================================================================
    
    def set_Gridspacing(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : int
            Set Grid spacing. Smalles possible value = 1

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        None.

        '''
    
        if value >= 1:
            if laser == 1:
                oc.writelu(128+52, value )
    
            elif laser == 2:
                oc.writelu(256+52, value )
                
            else:
                raise ValueError('Unknown input! See function description for more info.')
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    
    def set_FirstChannFreqTHz(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message
            

        Returns
        -------
        res : float
            First channel’s frequency, THz

        '''
        
        if laser == 1:
            oc.writelu(128+53, int(value) )
        elif laser == 2:
            oc.writelu(256+53, value )
        else:
            raise ValueError('Unknown input! See function description for more info.')
    
    
    def set_FirstChannFreqGHz(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            First channel’s frequency, GHz*10

        '''
        
        if laser == 1:
            oc.writelu(128+54, value )
        elif laser == 2:
            oc.writelu(256+54, value )
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
            
    def set_Frequency(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : float
            Set Laser Frequency.
            value in form value = 192.876

        Returns
        -------
        None.

        '''
        
        if laser == 1:
            
            GHz = int((value%1)*1e4)
            THz = int(value // 1)
            self.set_FirstChannFreqTHz(1,THz)
            self.set_FirstChannFreqGHz(1,GHz)
            
        elif laser == 2:
            GHz = int((value%1)*1e4)
            THz = int(value // 1)
            self.set_FirstChannFreqTHz(2,THz)
            self.set_FirstChannFreqGHz(2,GHz)
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
            
        
    def set_Whispermode(self,laser,state):
        
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        state : str
            ['ON','OFF']

        Returns
        -------
        None.

        '''
        stState = ['ON','OFF']
        if state in stState:
            if state == 'ON':
                if laser == 1:
                    oc.writelu(128+108, 2 )
                    data = self.ask_Whispermode(1)
                    while data != 'ON': 
                        oc.writelu(128+108, 2 )
                        data = self.ask_Whispermode(1)
                        
                elif laser == 2:
                    oc.writelu(256+108, 2 )
                    data = self.ask_Whispermode(2)
                    while data != 'ON': 
                        oc.writelu(128+108, 2 )
                        data = self.ask_Whispermode(2)
                else:
                    raise ValueError('Unknown input! See function description for more info.')
            elif state == 'OFF':
                if laser == 1:
                    oc.writelu(128+108, 0 )
                    data = self.ask_Whispermode(1)
                    while data != 'OFF': 
                        oc.writelu(128+108, 0 )
                        data = self.ask_Whispermode(1)
                elif laser == 2:
                    oc.writelu(256+108, 0 )
                    data = self.ask_Whispermode(2)
                    while data != 'OFF': 
                        oc.writelu(128+108, 0 )
                        data = self.ask_Whispermode(2)
                else:
                    raise ValueError('Unknown input! See function description for more info.')
            else:
                raise ValueError('Unknown input! See function description for more info.')
                
        
    def set_FineTune(self,laser,value):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2
        value : int
            Fine tunning set the frequency in MHz steps

        Returns
        -------
        None.

        '''
        if laser == 1:
            oc.writelu(128+98, int(value))
        elif laser == 2:
            oc.writelu(256+98, int(value))
        else:
            raise ValueError('Unknown input! See function description for more info.')
            
            
# =============================================================================
# Get/Save Data
# =============================================================================
    def get_Data(self,laser):
        '''
        

        Parameters
        ----------
        laser : int
            Laser seleected. 1 or 2

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        OutPut : dict
            Return a dictionary whit the measured power and set frequency.

        '''
        
        OutPut = {}
        if laser == 1:
            Power = self.ask_Power(laser)
            Freq = self.ask_Frequency(laser)
            OutPut['Power/dBm'] = Power
            OutPut['Set Frequency/THz'] = Freq
        elif laser == 2:
            Power = self.ask_Power(laser)
            Freq = self.ask_Frequency(laser)
            OutPut['Power/dBm'] = Power
            OutPut['Set Frequency/THz'] = Freq
        else:
            raise ValueError('Unknown input! See function description for more info.')
        return OutPut





