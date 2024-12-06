import numpy as np 
import pandas as pd 
import pyvisa as visa





class InfoClass:
    def __init__(self):

        self.Instructions()
        self.Devices()

    def Devices(self):

        List = ["MS2760A (Anritsu spectrum Analyzer MS2760A)", 
                "MG3694C (Anritsu Signal Generator MG3694C)", 
                "MS4647B (Anritsu Vectro Analyzer MS4647B)", 
                "AQ6370D (Yokogawa AQ6370D)", 
                "LU1000 (Novoptel Laser LU1000)", 
                "CoBrite (CoBrite Tunable Laser)", 
                "PM100D (Power Meter ThorLabs PM100D)", 
                "KEITHLEY (KEITHLEY Source Meter 2612)", 
                "GPP4323 (4-Channels Power Suppy GPP4323)",
                "KA3005 (Power Supply KA3005)", 
                "KA3005p (Power Supply KA3005p)", 
                "RD3005 (Power Supply RD3005)", 
                "APPH20G (AnaPico AG APPH20G)"              
                ]

        return print(List)
    
    def Instructions(self):
        return print("To Call an instrument use th Instrument serial number printed below!")
        

InfoClass()




class Instruments:

    def __init__(self, InstrumentSerialNumber):
        self.InstrumentSerialNumber = InstrumentSerialNumber
        self.Inst = None
        print("I am In the Class")

        self.Inst = self.Select()
        print(self.Inst)

    def Select(self):
        if self.InstrumentSerialNumber == 'MS2760A':
            return self.SpecAnalyser()
        elif self.InstrumentSerialNumber == 'MG3694C':
            return self.SigGen()
        elif self.InstrumentSerialNumber == 'MS4647B':
            return self.VNA()
        elif self.InstrumentSerialNumber == 'PM100D':
            return self.PowerMeter()
        elif self.InstrumentSerialNumber == 'LU1000':
            return self.LU1000()
        elif self.InstrumentSerialNumber == 'AQ6370D':
            return self.OSA()
        elif self.InstrumentSerialNumber == 'KEITHLEY':
            return self.SourceMeter()
        elif self.InstrumentSerialNumber == 'KA3005':
            return self.PowerSupply_KA3005()
        elif self.InstrumentSerialNumber == 'KA3005p':
            return self.PowerSupply_KA3005p()
        elif self.InstrumentSerialNumber == 'RD3005':
            return self.PowerSupply_RD3005()
        elif self.InstrumentSerialNumber == 'CoBrite':
            return self.CoBrite()
        elif self.InstrumentSerialNumber == 'APPH20G':
            return self.APPH()
        elif self.InstrumentSerialNumber == 'GPP4323':
            return self.PowerSupply_GPP4323()
        else:
            raise ValueError('Invalid Instrument Selected')
        
    
    def OSA(self):
        from InstrumentControl.AQ6370D import AQ6370D
        # import vxi11
        # rm = vxi11.list_devices()
        # for _ in rm:
        #     try:
        #          OSA = AQ6370D(str(_))
        #          InstrOSA = _
        #          OSA.Close()
        #     except (visa.VisaIOError): 
        #         print('Serial Number dont match!')
        # return AQ6370D(InstrOSA)
        return AQ6370D('169.254.58.101')



    def CoBrite(self):
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


    def SourceMeter(self):
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




    def PowerSupply_RD3005(self):
        from InstrumentControl.RD3005 import RD3005

        SerialNum = [ 'RND 320-KA3005P V2.0']      
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
        

    
    def PowerSupply_KA3005(self):
        from InstrumentControl.KA3005 import KA3005

        SerialNum = ['KORAD KA3005P V5.8 SN:03379314']      
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
                    PS = KA3005(data)
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
            return KA3005(Port_)
        else:
            raise ValueError("Instrument is not Valid Power Supply!")
    


    def PowerSupply_KA3005p(self):
        from InstrumentControl.KA3005p import KA3005p

        SerialNum = ['KORAD KA3005P V5.8 SN:03379289']      
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
                    PS = KA3005p(data)
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
            return KA3005p(Port_)
        else:
            raise ValueError("Instrument is not Valid Power Supply!")


        



    def PowerMeter(self):
        from InstrumentControl.PM100D import PM100D
        Serien_Nummer = ['P0024970','P0033858','P0037385']
        for _ in Serien_Nummer:
            try:
                PM100D(_)
                InstrPM = _
                break
            except (visa.VisaIOError): 
                print('Serial Number dont match!')
        return PM100D(InstrPM)



    def LU1000(self):
        from InstrumentControl.LU1000 import LU1000
        return LU1000()


    def SpecAnalyser(self):
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


    def SigGen(self):
        from InstrumentControl.MG3694C import MG3694C
        print('''
            ########### Set the correct network settings ###########
            
                Follow the instructions to set the network
                adapter and ip. After you are done confirm 
                to continue!
                
            ########### Set the correct network settings ###########
            ''')
            
        print('\n')
        conf = input('Are you finish yes/no: ')
        if conf == 'yes':
            print('Instrument Connected as SG')
            return MG3694C('192.168.0.254')
        else:
            pass


    def VNA(self):
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


            
    def APPH(self):
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

        
        
        
        
        
    def PowerSupply_GPP4323(self):
        from InstrumentControl.GPP4323 import GPP4323
        import serial.tools.list_ports
    
        SerialNum = ['GW INSTEK,GPP-4323,SN:GEW840790,V1.17', 'GW Instek,GPP-4323,SN:GEW866095,V1.19','GW Instek,GPP-4323,SN:GEW866095,V1.02']
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




# obj = Instruments("APPH20G")