# version: 1.0.0 2024/11/28 #Downloaded from https://www.novoptel.de/Home/Downloads_de.php
# verison: 1.0.1 modified by Maxim.Weizel for LU1000_Cband (untested)

from NovoptelUSB import NovoptelUSB
from NovoptelTCP import NovoptelTCP

print(
'''
#####################################################################################
    To use the LU1000 Laser you need to install the FTDI D2XX Driver e.g.
    from https://www.novoptel.de/Home/Downloads_de.php - USB Driver for USB2.0
    or https://ftdichip.com/drivers/d2xx-drivers/ - 2.12.36.4 (accessed on 08.02.2025)
    Python Library needed: pip install ftd2xx 
#####################################################################################
'''
)

class LU1000_Cband():
    
    n = None
    
    def __init__(self, target='192.168.1.100'):
        if (target=='USB'):
            self.n = NovoptelUSB('LU1000')
            if self.n.DEVNO<0:
                self.n = None
        else:
            self.n = NovoptelTCP(target, port=5025)
        

    def close(self):
        self.n.close()
        del(self.n)
        
        
    #######################    
    # Basic communication #
    #######################
        
    def read(self, addr: int):
        res = self.n.read(addr)
        return res
    
    def readram(self, startaddr: int, numaddr: int):
        res = self.n.readbuffer(startaddr, numaddr)
        return res
        
    def write(self, addr: int, data: int):
        self.n.write(addr, data)
        
        
     
    ###########################    
    # General instrument data #
    ###########################
    # TODO:has to be implemented

    # def getfirmware(self): # as string
    #     return hex(self.n.read(84))

    # def getserialnumber(self): # as integer
    #     return self.n.read(91)

    # def getmoduletype(self): # as string
    #      str="";
    #      for ii in range(16):
    #         dummy = self.n.read(96+ii)
    #         str += chr(dummy >> 8)
    #         str += chr(dummy & 0xFF)

    #      return str

# =============================================================================
# ASK
# =============================================================================


    def ask_Power(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+49)
            return float(res/100)
        elif laser == 2:
            res = self.read(256+49)
            return float(res/100)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


    def ask_LaserOutput(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        str 
            Laser enable('ON') or laser disable('OFF')

        '''
        if laser == 1:
            res = self.read(128+50 )
            if res == 0.0:
                print('OFF')
            else:
                print('ON')
        elif laser == 2:
            res = self.read(256+50 )
            if res == 0.0:
                print('OFF')
            else:
                print('ON')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_ControllerTemp(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+51 )
            return float(res)
        elif laser == 2:
            res = self.read(256+51 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_Gridspacing(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+52 )
            return float(res)
        elif laser == 2:
            res = self.read(256+52 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_FirstChannFreqTHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+53 )
            return float(res)
        elif laser == 2:
            res = self.read(256+53 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_FirstChannFreqGHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+54 )
            return float(res)
        elif laser == 2:
            res = self.read(256+54 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_ChannelFreqTHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+64 )
            return float(res)
        elif laser == 2:
            res = self.read(256+64 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_ChannelFreqGHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+65 )
            return float(res)
        elif laser == 2:
            res = self.read(256+65 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_OpticalPower(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+66 )
            return float(res/100)
        elif laser == 2:
            res = self.read(256+66 )
            return float(res/100)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_Temperature(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

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
            res = self.read(128+67 )
            return float(res)
        elif laser == 2:
            res = self.read(256+67 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_MinOpticalOutputPower(self):
        '''


        Returns
        -------
        res : float
            Ask minimum possible optical power setting

        '''
        res = self.read(128+80 )
        return res

    def ask_MaxOpticalOutputPower(self):
        '''


        Returns
        -------
        res : float
            Maximum possible optical power setting

        '''

        res = self.read(128+81 )
        return res

    def ask_LaserFirstFreqTHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+82 )
            return float(res)
        elif laser == 2:
            res = self.read(256+82 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_LaserFirstFreqGHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+83 )
            return float(res)
        elif laser == 2:
            res = self.read(256+83 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_minFreqLaser(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser out selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float
            min possible frequency.

        '''

        if laser in [1, 2]:
            THz = self.ask_LaserFirstFreqTHz(laser)
            GHz = self.ask_LaserFirstFreqGHz(laser)
            Freq = THz + GHz*1e-4
            return Freq
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_LaserLastFreqTHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+84 )
            return float(res)
        elif laser == 2:
            res = self.read(256+84 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_LaserLastFreqGHz(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2


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
            res = self.read(128+85 )
            return float(res)
        elif laser == 2:
            res = self.read(256+85 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_maxFreqLaser(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        float 
            max possible frequency

        '''

        if laser in [1, 2]:
            THz = self.ask_LaserLastFreqTHz(laser)
            GHz = self.ask_LaserLastFreqTHz(laser)
            Freq = THz + GHz*1e-4
            return float(Freq)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_LaserMinGridFreq(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            res = self.read(128+86 )
            return float(res)
        elif laser == 2:
            res = self.read(256+86 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_Frequency(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        Freq : float
            Calculate and return Frequency on the selected channel

        '''

        sLaser = [1, 2]
        if laser in sLaser:
            THz = float(self.ask_ChannelFreqTHz(laser))
            GHz = float(self.ask_ChannelFreqGHz(laser))
            Freq = THz + GHz*1e-4
            return Freq
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_LaserChannel(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2


        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Selected Channel Number

        '''

        if laser == 1:
            res = self.read(128+48 )
            return float(res)
        elif laser == 2:
            res = self.read(256+48 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def ask_Whispermode(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            Error message

        Returns
        -------
        res : float
            Whispermode Status


        '''
        if laser == 1:
            res = self.read(128+108 )
            data = float(res)
            if data == 0:
                return 'OFF'
            else:
                return 'ON'
        elif laser == 2:
            res = self.read(256+108 )
            return float(res)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


# =============================================================================
# SET
# =============================================================================


    def set_Power(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
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
            if value > 10:
                print('''
                      ################# Warning #################
                      
                      More then 10dBm is critical for some devices!
                      ''')
                comf = input('Are you sure you wanna continue (yes/no)? ')
                comf = comf.lower()
                if comf == 'yes':
                    value = value*100
                    self.write(128+49, int(value))
                    print('Power = '+str(float(value/100))+'dBm')
                else:
                    pass
            elif value <= 10 and value >= 6:
                value = value*100
                self.write(128+49, int(value))
                print('Power = '+str(float(value/100))+'dBm')
            else:
                raise ValueError(
                    'Unknown input! See function description for more info.')
        elif laser == 2:
            if value > 10:
                print('''
                      ################# Warning #################
                      
                      More then 10dBm is critical for some devices!
                      ''')
                comf = input('Are you sure you wanna continue (yes/no)? ')
                comf = comf.lower()
                if comf == 'yes':
                    value = value*100
                    self.write(256+49, int(value))
                    print('Power = '+str(float(value/100))+'dBm')
                else:
                    pass
            elif value <= 10 and value >= 6:
                value = value*100
                self.write(256+49, int(value))
                print('Power = '+str(float(value/100))+'dBm')
            else:
                raise ValueError(
                    'Unknown input! See function description for more info.')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_LaserChannel(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
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
            self.write(128+48, value)

        elif laser == 2:
            self.write(256+48, value)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_LaserOutput(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected -  1 or 2
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

        sValue = ['ON', 'OFF', 1, 0]
        if value in sValue:
            if laser == 1:
                if value == 1 or value == 'ON':
                    self.write(128+50, 8)
                    print('### Laser 1 is ON ###')
                else:
                    self.write(128+50, 0)
                    print('### Laser 1 is OFF')
            elif laser == 2:
                if value == 1 or value == 'ON':
                    self.write(256+50, 8)
                    print('### Laser 2 is ON ###')
                else:
                    self.write(256+50, 0)
                    print('### Laser 2 is OFF ###')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


# =============================================================================
# Test Write Grid
# =============================================================================


    def set_Gridspacing(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int
            Set Grid spacing. Smallest possible value = 1

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
                self.write(128+52, value)

            elif laser == 2:
                self.write(256+52, value)

            else:
                raise ValueError(
                    'Unknown input! See function description for more info.')
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_FirstChannFreqTHz(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            self.write(128+53, int(value))
        elif laser == 2:
            self.write(256+53, value)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_FirstChannFreqGHz(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

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
            self.write(128+54, value)
        elif laser == 2:
            self.write(256+54, value)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_Frequency(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : float
            Set Laser Frequency.
            value in form value = 192.876

        Returns
        -------
        None.

        '''

        if laser == 1:

            GHz = int((value % 1)*1e4)
            THz = int(value // 1)
            self.set_FirstChannFreqTHz(1, THz)
            self.set_FirstChannFreqGHz(1, GHz)

        elif laser == 2:
            GHz = int((value % 1)*1e4)
            THz = int(value // 1)
            self.set_FirstChannFreqTHz(2, THz)
            self.set_FirstChannFreqGHz(2, GHz)
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')

    def set_Whispermode(self, laser, state):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        state : str
            ['ON','OFF']

        Returns
        -------
        None.

        '''
        stState = ['ON', 'OFF']
        if state in stState:
            if state == 'ON':
                if laser == 1:
                    self.write(128+108, 2)
                    data = self.ask_Whispermode(1)
                    while data != 'ON':
                        self.write(128+108, 2)
                        data = self.ask_Whispermode(1)

                elif laser == 2:
                    self.write(256+108, 2)
                    data = self.ask_Whispermode(2)
                    while data != 'ON':
                        self.write(128+108, 2)
                        data = self.ask_Whispermode(2)
                else:
                    raise ValueError(
                        'Unknown input! See function description for more info.')
            elif state == 'OFF':
                if laser == 1:
                    self.write(128+108, 0)
                    data = self.ask_Whispermode(1)
                    while data != 'OFF':
                        self.write(128+108, 0)
                        data = self.ask_Whispermode(1)
                elif laser == 2:
                    self.write(256+108, 0)
                    data = self.ask_Whispermode(2)
                    while data != 'OFF':
                        self.write(128+108, 0)
                        data = self.ask_Whispermode(2)
                else:
                    raise ValueError(
                        'Unknown input! See function description for more info.')
            else:
                raise ValueError(
                    'Unknown input! See function description for more info.')

    def set_FineTune(self, laser, value):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2
        value : int
            Fine-tuning set the frequency in MHz steps

        Returns
        -------
        None.

        '''
        if laser == 1:
            self.write(128+98, int(value))
        elif laser == 2:
            self.write(256+98, int(value))
        else:
            raise ValueError(
                'Unknown input! See function description for more info.')


# =============================================================================
# Get/Save Data
# =============================================================================


    def get_Data(self, laser):
        '''


        Parameters
        ----------
        laser : int
            Laser output selected - 1 or 2

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        OutPut : dict
            Return a dictionary with the measured power and set frequency.

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
            raise ValueError(
                'Unknown input! See function description for more info.')
        return OutPut
