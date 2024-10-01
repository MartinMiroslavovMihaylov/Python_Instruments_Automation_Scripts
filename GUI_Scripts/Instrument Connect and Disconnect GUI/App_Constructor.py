import tkinter
import random 
import tkinter.messagebox
import customtkinter
from CTkListbox import *
import os
from PIL import Image,ImageTk
import sys
from InstrumentControl.InstrumentSelect import InstInit


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



ListInstruments = ["Anrtisu Spectrum Analyzer MS2760A", "Anritsu Signal Generator MG3694C", "Anritsu Vectro Analyzer MS4647B", "Power Meter ThorLabs PM100D", "Novoptel Laser LU1000", "Yokogawa Optical Spectrum Analyzer AQ6370D", "KEITHLEY Source Meter 2612", "Power Supply KA3005", "CoBrite Tunable Laser", "AnaPico AG,APPH20G", "4-Channels Power Suppy GPP4323", "Rohde and Schwarz SMA100B" ]




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Def empty Lists 
        self.InstrumentSelected = []
        self.Instrument = []
        self.rand_x = 0
        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # Load Image
        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Pictures/HNI_Logo_RGB.jpg")), size=(200, 50))


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)




        # Image Logo HNI
        self.sidebar_frame = customtkinter.CTkLabel(self.sidebar_frame,   image=self.logo_image,  text="",)
        self.sidebar_frame.grid(row=0, column=0, padx=20, pady=20)
        # Create Label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Select and Connect", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "Select Instrument", fg_color ="blue",  command = lambda: self.Add_Items(self.leftList, self.rightList))
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text = "Remove Instrument", fg_color ="blue", command = lambda: self.Remove_Items(self.rightList, self.leftList))
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, fg_color = "green",text = "Connect", command= self.ConnectInst)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text = "Exit", fg_color = "red",  command= self.QuitWindow)
        self.sidebar_button_5.grid(row=7, column=0, padx=20, pady=(10, 10))




        # create Listboxs
        self.ListLabel = customtkinter.CTkLabel(self, text="Selections Fields", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ListLabel.grid(row=0, column=1, padx=20, pady=(10, 0))

        self.leftList = CTkListbox(self, height=200, width=400)
        self.leftList.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.rightList = CTkListbox(self,  height=200, width=400)
        self.rightList.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.leftList.insert("END", "List of instruemnts")
        self.rightList.insert("END", "List of instruemnts")
        for i in ListInstruments:
            self.leftList.insert("END", " "+ i + " ")


        
        

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", rowspan=2)
        self.textbox.tag_config("1", foreground="green")



    def QuitWindow(self):
        self.quit()
        self.destroy()



    def Add_Items(self,fromList, toList):
        indexList = fromList.curselection()
        if indexList:
            val = fromList.get(indexList)
            # fromList.delete(indexList)
            toList.insert("END",val)
            if val == " 4-Channels Power Suppy GPP4323 ":
                self.rand_x = random.randint(1, 5)
                val =  " 4-Channels Power Suppy GPP4323_" + str(self.rand_x)
                self.InstrumentSelected.append(val)
            elif val == " Power Supply KA3005 ":
                self.rand_x = random.randint(1, 5)
                val =  " Power Supply KA3005_" + str(self.rand_x)
                self.InstrumentSelected.append(val)
            else:
                self.InstrumentSelected.append(val)



    def Remove_Items(self,fromList, toList):
        indexList = fromList.curselection()
        if indexList:
            # index = indexList[0]
            val = fromList.get(indexList)
            fromList.delete(indexList)
            #toList.insert("END",val)
            self.InstrumentSelected.remove(val)



    # def ConnectInst(self):
    #     Ist_List = []
    #     # self.textbox.insert("0.0",self.InstrumentSelected)
    #     # self.textbox.see('0.0')
    #     # self.textbox.insert("0.0","\n")
    #     # self.textbox.see('0.0')
    #     for elements in self.InstrumentSelected:    
    #         base_element  = elements.split('_')[0] + " "
    #         print(base_element)
            # if base_element == " Anrtisu Spectrum Analyzer MS2760A  ":
            #     print(base_element)
            #     SA = InstInit(base_element)
            #     self.Instrument.append(SA)
            #     print('Anrtisu Spectrum Analyzer MS2760A is connected as SA')
            #     Ist_List.append(SA)
            #     # return SA
            # elif base_element == " Anritsu Signal Generator MG3694C  ":
            #     print(base_element)
            #     SG = InstInit(base_element)
            #     self.Instrument.append(SG)
            #     print('Anritsu Signal Generator MG3694C is connected as PM')
            #     Ist_List.append(SG)
            #     # return SG
            # elif base_element == " Anritsu Vectro Analyzer MS4647B  ":
            #     print(base_element)
            #     VNA = InstInit(base_element)
            #     self.Instrument.append(VNA)
            #     print('Anritsu Vectro Analyzer MS4647B is connected as PM')
            #     Ist_List.append(VNA)
            #     # return VNA
            # elif base_element == ' Power Meter ThorLabs PM100D  ':
            #     print(base_element)
            #     PM = InstInit(base_element)
            #     self.Instrument.append(PM)
            #     print('Power Meter ThorLabs PM100D is connected as PM')
            #     Ist_List.append(PM)
            #     # return PM
            # elif base_element == " Novoptel Laser LU1000  ":
            #     print(base_element)
            #     LU = InstInit(base_element)
            #     self.Instrument.append(LU)
            #     print('Novoptel Laser LU1000 is connected as LU')
            #     Ist_List.append(LU)
            #     # return LU
            # elif base_element == " Yokogawa Optical Spectrum Analyzer AQ6370D  ":
            #     print(base_element)
            #     OSA = InstInit(base_element)
            #     self.Instrument.append(OSA)
            #     print('Yokogawa Optical Spectrum Analyzer AQ6370D is connected as OSA')
            #     Ist_List.append(OSA)
            #     # return OSA
            # elif base_element == " KEITHLEY Source Meter 2612  ":
            #     print(base_element)
            #     KA = InstInit(base_element)
            #     self.Instrument.append(KA)
            #     print('KEITHLEY Source Meter 2612 is connected as KA')
            #     Ist_List.append(KA)
            #     # return KA
            # elif base_element == " Power Supply KA3005 ":
            #     print(base_element)
            #     PS = InstInit(base_element)
            #     self.Instrument.append(PS)
            #     print('Power Supply KA3005 is connected as PS')
            #     Ist_List.append(PS)
            #     # return PS
            # elif base_element == " CoBrite Tunable Laser  ":
            #     print(base_element)
            #     CO = InstInit(base_element)
            #     self.Instrument.append(CO)
            #     print('CoBrite Tunable Laser is connected as PS')
            #     Ist_List.append(CO)
            #     # return CO
            # elif base_element == " AnaPico AG,APPH20G  ":
            #     print(base_element)
            #     APP = InstInit(base_element)
            #     self.Instrument.append(APP)
            #     print('AnaPico AG,APPH20G is connected as PS')
            #     Ist_List.append(APP)
            #     # return APP
            # elif base_element == " 4-Channels Power Suppy GPP4323 ":
            #     print(base_element)
            #     Var = 0
            #     GPP = InstInit(base_element)
            #     Var = GPP
            #     GPP = 0
            #     self.Instrument.append(Var)
            #     print('4-Channels Power Suppy GPP4323 is connected as PS')
            #     Ist_List.append(Var)
            #     # return GPP
            # else:
            #     raise ValueError("Wrong instrument")
    #     return Ist_List
    def ConnectInst(self):
        Ist_List = []
        success_message = ""  # To store success messages
        for elements in self.InstrumentSelected:    
            base_element = elements.split('_')[0] + " "
            if base_element == " Anrtisu Spectrum Analyzer MS2760A  ":
                print(base_element)
                SA = InstInit(base_element)
                self.Instrument.append(SA)
                print('Anrtisu Spectrum Analyzer MS2760A is connected as SA')
                Ist_List.append(SA)
                # return SA
            elif base_element == " Anritsu Signal Generator MG3694C  ":
                print(base_element)
                SG = InstInit(base_element)
                self.Instrument.append(SG)
                print('Anritsu Signal Generator MG3694C is connected as PM')
                Ist_List.append(SG)
                # return SG
            elif base_element == " Anritsu Vectro Analyzer MS4647B  ":
                print(base_element)
                VNA = InstInit(base_element)
                self.Instrument.append(VNA)
                print('Anritsu Vectro Analyzer MS4647B is connected as PM')
                Ist_List.append(VNA)
                # return VNA
            elif base_element == ' Power Meter ThorLabs PM100D  ':
                print(base_element)
                PM = InstInit(base_element)
                self.Instrument.append(PM)
                print('Power Meter ThorLabs PM100D is connected as PM')
                Ist_List.append(PM)
                # return PM
            elif base_element == " Novoptel Laser LU1000  ":
                print(base_element)
                LU = InstInit(base_element)
                self.Instrument.append(LU)
                print('Novoptel Laser LU1000 is connected as LU')
                Ist_List.append(LU)
                # return LU
            elif base_element == " Yokogawa Optical Spectrum Analyzer AQ6370D  ":
                print(base_element)
                OSA = InstInit(base_element)
                self.Instrument.append(OSA)
                print('Yokogawa Optical Spectrum Analyzer AQ6370D is connected as OSA')
                Ist_List.append(OSA)
                # return OSA
            elif base_element == " Rohde and Schwarz SMA100B  ":
                print(base_element)
                SMA = InstInit(base_element)
                self.Instrument.append(SMA)
                print('Rohde&Schwarz Signal Generator SMA100 is connected as SMA')
                Ist_List.append(SMA)
            elif base_element == " KEITHLEY Source Meter 2612  ":
                print(base_element)
                KA = InstInit(base_element)
                self.Instrument.append(KA)
                print('KEITHLEY Source Meter 2612 is connected as KA')
                Ist_List.append(KA)
                # return KA
            elif base_element == " Power Supply KA3005 ":
                print(base_element)
                PS = InstInit(base_element)
                self.Instrument.append(PS)
                print('Power Supply KA3005 is connected as PS')
                Ist_List.append(PS)
                # return PS
            elif base_element == " CoBrite Tunable Laser  ":
                print(base_element)
                CO = InstInit(base_element)
                self.Instrument.append(CO)
                print('CoBrite Tunable Laser is connected as PS')
                Ist_List.append(CO)
                # return CO
            elif base_element == " AnaPico AG,APPH20G  ":
                print(base_element)
                APP = InstInit(base_element)
                self.Instrument.append(APP)
                print('AnaPico AG,APPH20G is connected as PS')
                Ist_List.append(APP)
                # return APP
            elif base_element == " 4-Channels Power Suppy GPP4323 ":
                print(base_element)
                Var = 0
                GPP = InstInit(base_element)
                Var = GPP
                GPP = 0
                self.Instrument.append(Var)
                print('4-Channels Power Suppy GPP4323 is connected as PS')
                Ist_List.append(Var)
                # return GPP
            else:
                raise ValueError("Wrong instrument")
        if Ist_List:
            self.textbox.insert("0.0", success_message, "1")
            self.textbox.insert("0.0", "Instruments are Connected!\n", "1")
            self.textbox.see('0.0')
        else:
            self.textbox.insert("0.0", "No instruments selected to connect.\n", "1")
            self.textbox.see('0.0')

        return Ist_List
        self.textbox.insert("0.0","Instruments are Connected !", "1")
        self.textbox.see('0.0')
    
    def ExtractData(self):
        dict_Instr = {}
        for i in range(len(self.InstrumentSelected)):
            dict_Instr[self.InstrumentSelected[i]] = self.Instrument[i]
        # return InstrumentSelected
        # return Instrument, InstrumentSelected
        return dict_Instr






class DisconnectApp(customtkinter.CTk):
    def __init__(self, DissDict):
        super().__init__()

        # Configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{900}x{750}")
        self.DissDict = DissDict

        # Load Image
        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Pictures/HNI_Logo_RGB.jpg")), size=(200, 50))

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Image Logo HNI
        self.sidebar_frame = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.sidebar_frame.grid(row=0, column=0, padx=20, pady=20)

        # Create Label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="List of Instruments", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Textbox for disconnected messages
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", rowspan=2)
        self.textbox.tag_config("1", foreground="green")

        # Label for Textbox
        self.ListLabel = customtkinter.CTkLabel(self, text="Disconnect Devices", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ListLabel.grid(row=0, column=1, padx=20, pady=(10, 0))

        # Dynamically create buttons based on DissDict
        self.buttons = {}
        row_counter = 2
        for device_name in self.DissDict.keys():
            btn = customtkinter.CTkButton(
                self.sidebar_frame,
                text=device_name.strip(),
                command=lambda name=device_name: self.disconnect_device(name)
            )
            btn.grid(row=row_counter, column=0, padx=20, pady=10)
            self.buttons[device_name] = btn
            row_counter += 1

        # Add exit button
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", fg_color="red", command=self.quit_window)
        self.exit_button.grid(row=row_counter, column=0, padx=20, pady=(10, 10))

        # Enable or disable buttons based on available instruments in DissDict
        self.update_button_states()

    def update_button_states(self):
        """Enable or disable buttons based on instruments in the DissDict."""
        for device_name, button in self.buttons.items():
            if device_name in self.DissDict:
                button.configure(state="enable")
            else:
                button.configure(state="disabled")

    def disconnect_device(self, device_name):
        """Disconnect a specific device."""
        self.DissDict[device_name].Close()  # Disconnect the device
        self.buttons[device_name].configure(state="disabled")
        self.textbox.insert("0.0", f"{device_name} is Disconnected\n")
        self.textbox.see('0.0')

    def quit_window(self):
        """Quit the application."""
        self.quit()
        self.destroy()







# class DisconnectApp(customtkinter.CTk):
#     def __init__(self, DissDict):
#         super().__init__()

#         # configure window
#         self.title("CustomTkinter complex_example.py")
#         self.geometry(f"{900}x{750}")

#         # configure grid layout (4x4)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure((2, 3), weight=0)
#         # self.grid_rowconfigure((0, 1, 2), weight=1)

#         self.DissDict = DissDict
#         # self.DissconnectList = DissList
#         # print(self.DissDict)

#         # Load Image
#         image_path = os.path.dirname(os.path.realpath(__file__))
#         self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "HNI_Logo_RGB.jpg")), size=(200, 50))


#         # create sidebar frame with widgets
#         self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
#         self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
#         self.sidebar_frame.grid_rowconfigure(4, weight=1)

#         # Image Logo HNI
#         self.sidebar_frame = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="", )
#         self.sidebar_frame.grid(row=0, column=0, padx=20, pady=20)

#         # Create Label
#         self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="List of Instruments", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))




#         self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "Anrtisu Spectrum Analyzer", command= self.SA_Dissconnect)
#         self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
#         self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text = "Anritsu Signal Generator", command= self.SG_Dissconnect)
#         self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
#         self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text = "Anritsu VNA", command= self.VNA_Dissconnect)
#         self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
#         self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text = "Novoptel Laser", command= self.LU_Dissconnect)
#         self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
#         self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text = "Power Meter ThorLabs", command= self.PM_Dissconnect)
#         self.sidebar_button_5.grid(row=6, column=0, padx=20, pady=10)
#         self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text = "KEITHLEY Source Meter", command= self.KA_Dissconnect)
#         self.sidebar_button_6.grid(row=7, column=0, padx=20, pady=10)
#         self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, text = "Power Supply 1-Channel", command= self.PS_Dissconnect)
#         self.sidebar_button_7.grid(row=8, column=0, padx=20, pady=10)
#         self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, text = "Yokogawa OSA", command= self.OSA_Dissconnect)
#         self.sidebar_button_8.grid(row=9, column=0, padx=20, pady=10)
#         self.sidebar_button_9 = customtkinter.CTkButton(self.sidebar_frame, text = "CoBrite Laser", command= self.CO_Dissconnect)
#         self.sidebar_button_9.grid(row=10, column=0, padx=20, pady=10)
#         self.sidebar_button_10 = customtkinter.CTkButton(self.sidebar_frame, text = "AnaPico", command= self.AP_Dissconnect)
#         self.sidebar_button_10.grid(row=11, column=0, padx=20, pady=10)
#         self.sidebar_button_11 = customtkinter.CTkButton(self.sidebar_frame, text = "Power Supply 4-Channel", command= self.GPP_Dissconnect)
#         self.sidebar_button_11.grid(row=12, column=0, padx=20, pady=10)
#         self.sidebar_button_12 = customtkinter.CTkButton(self.sidebar_frame, text = "Exit", fg_color = "red",  command= self.QuitWindow)
#         self.sidebar_button_12.grid(row=13, column=0, padx=20, pady=(10, 10))



#         # create textbox
#         self.textbox = customtkinter.CTkTextbox(self, width=250)
#         self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", rowspan=2)
#         self.textbox.tag_config("1", foreground="green")

#         #Label TextBox
#         self.ListLabel = customtkinter.CTkLabel(self, text="Disconnect Devices", font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.ListLabel.grid(row=0, column=1, padx=20, pady=(10, 0))

#         # check list of instruments and only activate the buttons if the instrument is presented in the list 
#         if " Anrtisu Spectrum Analyzer MS2760A " in self.DissDict.keys():
#             self.sidebar_button_1.configure(state="enable", text="Anrtisu Spectrum Analyzer")
#             self.sidebar_button_1.configure(state="enable")
#         else:
#             self.sidebar_button_1.configure(state="disabled", text="Anrtisu Spectrum Analyzer")
#             self.sidebar_button_1.configure(state="disabled")


#         if " Anritsu Signal Generator MG3694C " in self.DissDict.keys():
#             self.sidebar_button_2.configure(state="enable", text="Anritsu Signal Generator")
#             self.sidebar_button_2.configure(state="enable")
#         else:
#             self.sidebar_button_2.configure(state="disabled", text="Anritsu Signal Generator")
#             self.sidebar_button_2.configure(state="disabled")


#         if " Anritsu Vectro Analyzer MS4647B " in self.DissDict.keys():
#             self.sidebar_button_3.configure(state="enable", text="Anritsu VNA")
#             self.sidebar_button_3.configure(state="enable")
#         else:
#             self.sidebar_button_3.configure(state="disabled", text="Anritsu VNA")
#             self.sidebar_button_3.configure(state="disabled")


#         if " Novoptel Laser LU1000 " in self.DissDict.keys():
#             self.sidebar_button_4.configure(state="enable", text="Novoptel Laser")
#             self.sidebar_button_4.configure(state="enable")
#         else:
#             self.sidebar_button_4.configure(state="disabled", text="Novoptel Laser")
#             self.sidebar_button_4.configure(state="disabled")


#         if " Power Meter ThorLabs PM100D " in self.DissDict.keys():
#             self.sidebar_button_5.configure(state="enable", text="Power Meter ThorLabs")
#             self.sidebar_button_5.configure(state="enable")
#         else:
#             self.sidebar_button_5.configure(state="disabled", text="Power Meter ThorLabs")
#             self.sidebar_button_5.configure(state="disabled")

            
#         if " KEITHLEY Source Meter 2612 " in self.DissDict.keys():
#             self.sidebar_button_6.configure(state="enable", text="KEITHLEY Source Meter")
#             self.sidebar_button_6.configure(state="enable")
#         else:
#             self.sidebar_button_6.configure(state="disabled", text="KEITHLEY Source Meter")
#             self.sidebar_button_6.configure(state="disabled")


#         if " Power Supply KA3005 " in self.DissDict.keys():
#             self.sidebar_button_7.configure(state="enable", text="Power Supply 1-Channel")
#             self.sidebar_button_7.configure(state="enable")
#         else:
#             self.sidebar_button_7.configure(state="disabled", text="Power Supply 1-Channel")
#             self.sidebar_button_7.configure(state="disabled")


#         if " Yokogawa Optical Spectrum Analyzer AQ6370D " in self.DissDict.keys():
#             self.sidebar_button_8.configure(state="enable", text="Yokogawa OSA")
#             self.sidebar_button_8.configure(state="enable")
#         else:
#             self.sidebar_button_8.configure(state="disabled", text="Yokogawa OSA")
#             self.sidebar_button_8.configure(state="disabled")


#         if " CoBrite Tunable Laser " in self.DissDict.keys():
#             self.sidebar_button_9.configure(state="enable", text="CoBrite Laser")
#             self.sidebar_button_9.configure(state="enable")
#         else:
#             self.sidebar_button_9.configure(state="disabled", text="CoBrite Laser")
#             self.sidebar_button_9.configure(state="disabled")


#         if " AnaPico AG,APPH20G " in self.DissDict.keys():
#             self.sidebar_button_10.configure(state="enable", text="AnaPico")
#             self.sidebar_button_10.configure(state="enable")
#         else:
#             self.sidebar_button_10.configure(state="disabled", text="AnaPico")
#             self.sidebar_button_10.configure(state="disabled")


#         if " 4-Channels Power Suppy GPP4323 " in self.DissDict.keys():
#             self.sidebar_button_11.configure(state="enable", text="Power Supply 4-Channel")
#             self.sidebar_button_11.configure(state="enable")
#         else:
#             self.sidebar_button_11.configure(state="disabled", text="Power Supply 4-Channel")
#             self.sidebar_button_11.configure(state="disabled")
        





#     def QuitWindow(self):
#         self.quit()
#         self.destroy()


#     def DisconnectInst(self):
#         print("Instruments are Disconnected")

#     def SA_Dissconnect(self):
#         self.DissDict[" Anrtisu Spectrum Analyzer MS2760A "].Close()
#         self.sidebar_button_1.configure(state="disabled", text="Anrtisu Spectrum Analyzer")
#         self.sidebar_button_1.configure(state="disabled")
#         self.textbox.insert("0.0","Anrtisu Spectrum Analyzer MS2760A is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def SG_Dissconnect(self):
#         self.DissDict[" Anritsu Signal Generator MG3694C "].Close()
#         self.sidebar_button_2.configure(state="disabled", text="Anritsu Signal Generator")
#         self.sidebar_button_2.configure(state="disabled")
#         self.textbox.insert("0.0", "Anritsu Signal Generator MG3694C is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def VNA_Dissconnect(self):
#         self.DissDict[" Anritsu Vectro Analyzer MS4647B "].RTL()
#         self.DissDict[" Anritsu Vectro Analyzer MS4647B "].Close()
#         self.sidebar_button_3.configure(state="disabled", text="Anritsu VNA")
#         self.sidebar_button_3.configure(state="disabled")
#         self.textbox.insert("0.0", "Anritsu Vectro Analyzer MS4647B is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def LU_Dissconnect(self):
#         self.DissDict[" Novoptel Laser LU1000 "].Close()
#         self.sidebar_button_4.configure(state="disabled", text="Novoptel Laser")
#         self.sidebar_button_4.configure(state="disabled")
#         self.textbox.insert("0.0", "Novoptel Laser LU1000 is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')
        
#     def PM_Dissconnect(self):
#         self.DissDict[" Power Meter ThorLabs PM100D "].Close()
#         self.sidebar_button_5.configure(state="disabled", text="Power Meter ThorLabs")
#         self.sidebar_button_5.configure(state="disabled")
#         self.textbox.insert("0.0", "Power Meter ThorLabs PM100D is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def KA_Dissconnect(self):
#         self.DissDict[" KEITHLEY Source Meter 2612 "].Close()
#         self.sidebar_button_6.configure(state="disabled", text="KEITHLEY Source Meter")
#         self.sidebar_button_6.configure(state="disabled")
#         self.textbox.insert("0.0", "KEITHLEY Source Meter 2612 is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def PS_Dissconnect(self):
#         self.DissDict[" Power Supply KA3005 "].Close()
#         # PS1.Close()
#         # PS2.Close()
#         # PS3.Close()
#         self.sidebar_button_7.configure(state="disabled", text="Power Supply 1-Channel")
#         self.sidebar_button_7.configure(state="disabled")
#         self.textbox.insert("0.0", "Power Supply KA3005 is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def OSA_Dissconnect(self):
#         self.DissDict[" Yokogawa Optical Spectrum Analyzer AQ6370D "].Close()
#         self.sidebar_button_8.configure(state="disabled", text="Yokogawa OSA")
#         self.sidebar_button_8.configure(state="disabled")
#         self.textbox.insert("0.0", "Yokogawa Optical Spectrum Analyzer AQ6370D is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def CO_Dissconnect(self):
#         self.DissDict[" CoBrite Tunable Laser "].Close()
#         self.sidebar_button_9.configure(state="disabled", text="CoBrite Laser")
#         self.sidebar_button_9.configure(state="disabled")
#         self.textbox.insert("0.0", "CoBrite Tunable Laser is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')
        
#     def AP_Dissconnect(self):
#         self.DissDict[' AnaPico AG,APPH20G '].Close()
#         self.sidebar_button_10.configure(state="disabled", text="AnaPico")
#         self.sidebar_button_10.configure(state="disabled")
#         self.textbox.insert("0.0", "AnaPico AG,APPH20G is Disconnected")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')

#     def GPP_Dissconnect(self):
#         self.DissDict[" 4-Channels Power Suppy GPP4323 "].Close()
#         self.sidebar_button_11.configure(state="disabled", text="Power Supply 4-Channel")
#         self.sidebar_button_11.configure(state="disabled")
#         self.textbox.insert("0.0", "4-Channels Power Suppy GPP4323")
#         self.textbox.see('0.0')
#         self.textbox.insert("0.0","\n")
#         self.textbox.see('0.0')




# # ListInstruments = ["Anrtisu Spectrum Analyzer MS2760A"]


# # if __name__ == "__main__":
# #     app = App()
# #     app.mainloop()

# # data = {}
# # data[" 4-Channels Power Supply GPP4323 "] = 10

# # if __name__ == "__main__":
# #     DissApp = DissconnectApp(data)
# #     DissApp.mainloop()