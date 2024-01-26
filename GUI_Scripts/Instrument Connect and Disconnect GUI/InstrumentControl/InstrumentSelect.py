# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 08:55:42 2022

@author: Martin.Mihaylov
"""

import sys
import pyvisa as visa




def OSA():
    from InstrumentControl.AQ6370D import AQ6370D
    # import vxi11
    # rm = vxi11.list_devices()
    # for _ in rm:
    #     try:
    #          OSA = AQ6370D(str(_))
    #         #  InstrOSA = _
    #          OSA.Close()
    #     except (visa.VisaIOError): 
    #         print('Serial Number dont match!')
    # return AQ6370D(_)
    return AQ6370D('169.254.58.101')



def CoBrite():
    from InstrumentControl.CoBrite import CoBrite
    rm = visa.ResourceManager()
    CP = 0
    dataInst = []
    for data in list(rm.list_resources()):
        while CP == 0:
            try:
                CO = CoBrite(str(data))
                CP = CO.Identification().split(';')[0]
                if CP == 'COBRITE CBDX-SC-SC-NN-NN-FA, SN 22060011, F/W Ver 1.2.1(160), HW Ver 1.20':
                   CP = 1
                   dataInst = str(data)
                else:
                   CP = 0
            except (visa.VisaIOError): 
                print('Wrong Instrument!')
            else:
                break
            break
    return CoBrite(str(dataInst))


def SourceMeter():
    from InstrumentControl.KEITHLEY2612 import KEITHLEY2612
    rm = visa.ResourceManager()
    KM = 0
    dataInst = []
    for data in list(rm.list_resources()):
        while KM == 0:
            try:
                KA = KEITHLEY2612(str(data))
                KM = KA.Identification().split('\n')[0]
                if KM == 'Keithley Instruments Inc., Model 2612, 1152698, 1.4.2':
                   KM = 1
                   dataInst = str(data)
                else:
                   KM = 0
            except (visa.VisaIOError): 
                print('Wrong Instrument!')
            else:
                break
            break
    return KEITHLEY2612(str(dataInst))




def PowerSupply():
    from InstrumentControl.RD3005 import RD3005
    from InstrumentControl.KA3005 import KA3005
    from InstrumentControl.KA3005p import KA3005p
    
    SerialNum = ['KORAD KA3005P V5.8 SN:03379314' , 'KORAD KA3005P V5.8 SN:03379289' , 'RND 320-KA3005P V2.0']      
    #Prnt all instruments connected to the COM-Ports.
    #Needed to set later
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    COM_List = []
    Port_ = None
    for port, desc, hwid in sorted(ports):
            # print("{}: {} [{}]".format(port, desc, hwid))
            COM_List.append(port)


    PowerInstr = 0
    for data in list(COM_List):
        while PowerInstr == 0:
            try:
                PS = RD3005(data)
                PowerInstr = PS.getIdn().split("\n")[0]
                if PowerInstr in SerialNum:
                    PowerInstr = 1
                    Port_ = data
                    break
                else:
                    PowerInstr = 0
                    print("Scanning COM Ports for Instrument !")
            except serial.SerialException as e:
            #There is no new data from serial port
                print("Scanning COM Ports for Instrument !")
            except TypeError as e:
                #Disconnect of USB->UART occured
                print("Scanning COM Ports for Instrument !")
            except visa.VisaIOError as e:
                print("Scanning COM Ports for Instrument !")
            except AttributeError:
                pass
            else:
                break
            break
    CheckInstrName = None
    CheckInstrName = PS.getIdn().split("\n")[0]
    PS.Close()
    
    
    if CheckInstrName in SerialNum:
        return RD3005(Port_)
    else:
        raise ValueError("Instrument is not Valid Power Supply!")
 
    # if CheckInstrName in SerialNum:
    #     if data == SerialNum[0]:
    #         PS.Close()
    #         return KA3005(Port_)
    #     elif data == SerialNum[1]:
    #         PS.Close()
    #         return KA3005p(Port_)
    #     elif data == SerialNum[2]:
    #         PS.Close()
    #         return RD3005(Port_)
        
        
# =============================================================================
#         Old Power Supply Connect Function
# =============================================================================
        
# def PowerSupply():
#     from InstrumentControl.RD3005 import RD3005
#     from InstrumentControl.KA3005 import KA3005
#     from InstrumentControl.KA3005p import KA3005p
    
#     SerialNum = ['KORAD KA3005P V5.8 SN:03379314' , 'KORAD KA3005P V5.8 SN:03379289' , 'RND 320-KA3005P V2.0', 'GW INSTEK,GPP-4323,SN:GEW840790,V1.17']      
#     #Prnt all instruments connected to the COM-Ports.
#     #Needed to set later
#     import serial.tools.list_ports
#     ports = serial.tools.list_ports.comports()
#     for port, desc, hwid in sorted(ports):
#             print("{}: {} [{}]".format(port, desc, hwid))
#     print(' ')
#     print('Check See the COM Port #####')
#     Com = input('Give COM number from the Power Supply: ')
#     # PS = kd3005pInstrument('COM'+Com)
#     PS = RD3005('COM'+Com)
#     data = PS.getIdn()
    

    
#     if data in SerialNum:
#         if data == SerialNum[0]:
#             PS.Close()
#             return KA3005('COM'+Com)
#         elif data == SerialNum[1]:
#             PS.Close()
#             return KA3005p('COM'+Com)
#         elif data == SerialNum[2]:
#             PS.Close()
#             return RD3005('COM'+Com)
    



def PowerMeter():
    from InstrumentControl.PM100D import PM100D
    Serien_Nummer = ['P0024970','P0033858', 'P0037385']
    for _ in Serien_Nummer:
        try:
            PM100D(_)
            InstrPM = _
            break
        except (visa.VisaIOError): 
           print('Serial Number dont match!')
    return PM100D(InstrPM)


def LU1000():
    from InstrumentControl.LU1000 import LU1000
    return LU1000()


def SpecAnalyser():
    from InstrumentControl.MS2760A import MS2760A
    Source = '127.0.0.1'
    Ports = visa.ResourceManager().list_resources(query='TCP?*')
    for i in range(len(Ports)):
        if Ports[i].split("::")[1] == Source:
            _ = Ports[i]
        else:
            pass
    # return MS2760A('127.0.0.1')
    return MS2760A(_)


def SigGen():
    from InstrumentControl.MG3694C import MG3694C
    print('''
          ########### Set the correct network settings ###########
          
              Follow the instrictions to set the network
              addapter and ip. After you are done confurm 
              to continuen!
              
         ########### Set the correct network settings ###########
          ''')
          
    print('\n')
    conf = input('Are you finish yes/no: ')
    if conf == 'yes':
        return MG3694C('192.168.0.254')
        print('Instrument Connected as SG')
    else:
        pass


def VNA():
    from InstrumentControl.MS4647B import MS4647B
    # import vxi11
    # rm = vxi11.list_devices()
    rm = visa.ResourceManager('@py')
    list_rm = rm.list_resources()
        
    IP = '169.254.100.85'
    Str_IP = None
    Set = 0

    for _ in range(len(list_rm)):
        test_ip = list_rm[_].split('::')[1]
        if test_ip == IP:
            while Set == 0:
                try:
                    Str_IP = list_rm[_].split('::')[0] + '::' +list_rm[_].split('::')[1]
                    VNA = MS4647B(Str_IP)
                    data = VNA.getIdn()
                    if data == 'ANRITSU,MS4647B,1416530,V2023.9.1':
                        Set = 1
                        VNA.RTL()
                        VNA.Close()
                        break
                    else:
                        print('Connecting')
                except (visa.VisaIOError): 
                    print('Serial Number dont match!')
            
        else:
            print('No matching Device detected !!')

    # for _ in rm:
    #     try:
    #          VNA = MS4647B('TCPIP::'+str(_))
    #          InstrVNA = _
    #          VNA.RTL()
    #          VNA.Close()
    #     except (visa.VisaIOError): 
    #         print('Serial Number dont match!')
    return MS4647B(Str_IP) 
    #return MS4647B('TCPIP0::169.254.100.85')
    #return MS4647B('TCPIP0::131.234.87.205')

           
def APPH():
    from InstrumentControl.APPH import APPH
    # import vxi11
    # rm = vxi11.list_devices()
    import pyvisa as visa
    rm = visa.ResourceManager()
    list_rm = rm.list_resources()
    for i in range(len(list_rm)):
        if list_rm[i].split('::')[0] == 'USB0':
            inst = list_rm[i]
        else: 
            pass
    try:
        AP = APPH(inst)
        InstrAPPH = inst
        AP.Close()
    except (visa.VisaIOError): 
        print('Serial Number dont match!')

    # for _ in rm:
    #     try:
    #          AP = APPH('TCPIP0::'+str(_)+'::inst0::INSTR')
    #          InstrAPPH = _
    #          AP.Close()
    #     except (visa.VisaIOError): 
    #         print('Serial Number dont match!')
    return APPH(InstrAPPH)
    # return APPH('TCPIP0::131.234.87.204::inst0::INSTR')
    
    
    
    
    
def PowerSupply_GPP4323():
    from InstrumentControl.GPP4323 import GPP4323
    import serial.tools.list_ports
    
    SerialNum = ['GW INSTEK,GPP-4323,SN:GEW840790,V1.17', 'GW Instek,GPP-4323,SN:GEW866095,V1.19', 'GW Instek,GPP-4323,SN:GEW866085,V1.19', 'GW Instek,GPP-4323,SN:GEW866095,V1.02']
    ports = serial.tools.list_ports.comports()
    COM_List = []
    Port_ = None
    for port, desc, hwid in sorted(ports):
            # print("{}: {} [{}]".format(port, desc, hwid))
            COM_List.append(port)


    PowerInstr = 0
    for data in list(COM_List):
        while PowerInstr == 0:
            try:
                GPP = GPP4323(data)
                PowerInstr = GPP.getIdn().split("\n")[0]
                if PowerInstr in SerialNum:
                    PowerInstr = 1
                    Port_ = data
                    break
                else:
                    PowerInstr = 0
                    print("Scanning COM Ports for Instrument !")
            except serial.SerialException as e:
                #There is no new data from serial port
                print("Scanning COM Ports for Instrument !")
            except TypeError as e:
                #Disconnect of USB->UART occured
                GPP = GPP4323()
            else:
                break
            break    
    GPP.Close()
    return GPP4323(Port_)
          
    
# =============================================================================
#     Old GPP Function
# =============================================================================
# def PowerSupply_GPP4323():
#     from InstrumentControl.GPP4323 import GPP4323
#     import serial.tools.list_ports
#     ports = serial.tools.list_ports.comports()
#     for port, desc, hwid in sorted(ports):
#             print("{}: {} [{}]".format(port, desc, hwid))
#     print(' ')
#     print('Check See the COM Port #####')
#     Com = input('Give COM number from the Power Supply: ')
#     GPP = GPP4323('COM'+Com)
#     GPP.Close()
#     return GPP4323('COM'+Com)
        


# =============================================================================
# Load Instrument Librarys
# =============================================================================


def InstInit(Num):
    if Num == " Anrtisu Spectrum Analyzer MS2760A ":
        return SpecAnalyser()
    elif Num ==  " Anritsu Signal Generator MG3694C ":
        return SigGen()
    elif Num == " Anritsu Vectro Analyzer MS4647B ":
        return VNA()
    elif Num ==  " Power Meter ThorLabs PM100D ":
        return PowerMeter()
    elif Num == " Novoptel Laser LU1000 ":
        return LU1000()
    elif Num == " Yokogawa Optical Spectrum Analyzer AQ6370D ":
        return OSA()
    elif Num == " KEITHLEY Source Meter 2612 ":
        return SourceMeter()
    elif Num == " Power Supply KA3005 ":
        return PowerSupply()
    elif Num == " CoBrite Tunable Laser ":
        return CoBrite()
    elif Num == " AnaPico AG,APPH20G ":
        return APPH()
    elif Num == " 4-Channels Power Suppy GPP4323 ":
        return PowerSupply_GPP4323()
    else:
        raise ValueError('Invalid Instrument Selected')
    
    
    
    
    
    
    
    
    
    
    
    

    