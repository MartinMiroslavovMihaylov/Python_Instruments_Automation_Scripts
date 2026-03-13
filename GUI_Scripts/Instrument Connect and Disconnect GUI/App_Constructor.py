import tkinter
import random
import customtkinter
from CTkListbox import CTkListbox
import os
from PIL import Image

from Instruments_Libraries.InstrumentSelect import (
    InstInit, SpecAnalyser, SigGen, VNA, PowerMeter,
    LU1000, OSA, SourceMeter, PowerSupply,
    Laser_CoBrite, PhaseNoiseAnalyzer_APPH,
    PowerSupply_GPP4323, RnS_SMA100B,
    UXR_1002A, RnS_FSWP50
)

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


ListInstruments = [
    "Anrtisu Spectrum Analyzer MS2760A",
    "Anritsu Signal Generator MG3694C",
    "Anritsu Vectro Analyzer MS4647B",
    "Power Meter ThorLabs PM100D",
    "Novoptel Laser LU1000",
    "Yokogawa Optical Spectrum Analyzer AQ6370D",
    "KEITHLEY Source Meter 2612",
    "Power Supply KA3005",
    "CoBrite Tunable Laser",
    "AnaPico AG,APPH20G",
    "4-Channels Power Suppy GPP4323",
    "Rohde and Schwarz SMA100B",
    "Rohde and Schwarz FSWP50",
    "Keysight UXR0702A"
]


# ======================================
# Main App Class
# ======================================
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.InstrumentSelected = []
        self.Instrument = []

        # window
        self.title("Instrument Controller")
        self.geometry("1100x580")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # image
        image_path = os.path.dirname(os.path.realpath(__file__))

        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "Pictures/HNI_Logo_RGB.jpg")),
            size=(200, 50)
        )

        # ======================================
        # Sidebar
        # ======================================

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            image=self.logo_image,
            text=""
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.logo_text = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Select and Connect",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_text.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Select Instrument",
            fg_color="blue",
            command=lambda: self.Add_Items(self.leftList, self.rightList)
        )
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Remove Instrument",
            fg_color="blue",
            command=lambda: self.Remove_Items(self.rightList)
        )
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Connect",
            fg_color="green",
            command=self.ConnectInst
        )
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_5 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Exit",
            fg_color="red",
            command=self.QuitWindow
        )
        self.sidebar_button_5.grid(row=7, column=0, padx=20, pady=(10, 10))

        # ======================================
        # Lists
        # ======================================

        self.ListLabel = customtkinter.CTkLabel(
            self,
            text="Selections Fields",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.ListLabel.grid(row=0, column=1, padx=20, pady=(10, 0))

        self.leftList = CTkListbox(self, height=200, width=400)
        self.leftList.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.rightList = CTkListbox(self, height=200, width=400)
        self.rightList.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # headers
        self.leftList.insert("END", "--- Available Devices ---")
        self.rightList.insert("END", "--- Selected Devices ---")

        for inst in ListInstruments:
            self.leftList.insert("END", inst)

        # ======================================
        # Textbox
        # ======================================

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", rowspan=2)
        self.textbox.tag_config("1", foreground="green")

    # ======================================
    # GUI Functions
    # ======================================

    def QuitWindow(self):
        self.quit()
        self.destroy()

    # --------------------------

    def Add_Items(self, fromList, toList):

        index = fromList.curselection()

        if not index:
            return

        val = fromList.get(index)

        if "Available Devices" in val:
            return

        toList.insert("END", val)

        base_val = val.strip()

        if base_val in ["4-Channels Power Suppy GPP4323", "Power Supply KA3005"]:
            rand_x = random.randint(1, 5)
            base_val = f"{base_val}_{rand_x}"

        self.InstrumentSelected.append(base_val)

    # --------------------------

    def Remove_Items(self, fromList):

        index = fromList.curselection()

        if not index:
            return

        val = fromList.get(index)

        if "Selected Devices" in val:
            return

        fromList.delete(index)

        if val in self.InstrumentSelected:
            self.InstrumentSelected.remove(val)

    # ======================================
    # Connect Instruments
    # ======================================

    def ConnectInst(self):

        import logging

        self.InstrumentsDict = {}
        self.Instrument = []

        map_func = {

            "Anrtisu Spectrum Analyzer MS2760A": SpecAnalyser,
            "Anritsu Signal Generator MG3694C": SigGen,
            "Anritsu Vectro Analyzer MS4647B": VNA,
            "Power Meter ThorLabs PM100D": PowerMeter,
            "Novoptel Laser LU1000": LU1000,
            "Yokogawa Optical Spectrum Analyzer AQ6370D": OSA,
            "KEITHLEY Source Meter 2612": SourceMeter,
            "Power Supply KA3005": PowerSupply,
            "CoBrite Tunable Laser": Laser_CoBrite,
            "AnaPico AG,APPH20G": PhaseNoiseAnalyzer_APPH,
            "4-Channels Power Suppy GPP4323": PowerSupply_GPP4323,
            "Rohde and Schwarz SMA100B": RnS_SMA100B,
            "Keysight UXR0702A": UXR_1002A,
            "Rohde and Schwarz FSWP50": RnS_FSWP50
        }

        for elem in self.InstrumentSelected:

            base_name = elem.split("_")[0].strip()

            if base_name not in map_func:
                self.textbox.insert("0.0", f"Invalid instrument selected: {base_name}\n", "1")
                continue

            try:

                obj = map_func[base_name]()

                self.Instrument.append(obj)

                self.InstrumentsDict.setdefault(base_name, []).append(obj)

                self.textbox.insert("0.0", f"{base_name} connected!\n", "1")

            except Exception as e:

                logging.warning(f"Failed to connect {base_name}: {e}")

                self.textbox.insert("0.0", f"Failed to connect {base_name}: {e}\n", "1")

        self.textbox.insert("0.0", "All connection attempts completed.\n", "1")
        self.textbox.see("0.0")

    # ======================================
    # Extract Instruments
    # ======================================

    def ExtractData_old(self):

        dict_Instr = {}

        for i, sel in enumerate(self.InstrumentSelected):

            instr = self.Instrument[i]

            if isinstance(instr, list):
                dict_Instr.setdefault(sel.strip(), []).extend(instr)

            else:
                dict_Instr.setdefault(sel.strip(), []).append(instr)

        return dict_Instr
    
    
    def ExtractData(self) -> dict[str, list]:
        """
        Attempt to connect to all selected instruments and return them in a dictionary.
        Handles connection failures gracefully.
        """
        import logging

        dict_Instr: dict[str, list] = {}
        logger = logging.getLogger(__name__)

        for i, sel in enumerate(self.InstrumentSelected):
            base_name = sel.strip()
            instr_instance: list | None = None

            try:
                # Attempt to get instrument object(s)
                instr_instance = self.Instrument[i]  # can be single or list
            except IndexError:
                instr_instance = None
                warning_msg = f"{base_name} not initialized in self.Instrument!"
                # GUI warning
                if hasattr(self, "textbox") and self.textbox:
                    try:
                        self.textbox.insert("0.0", f"Warning: {warning_msg}\n", "1")
                    except Exception:
                        logger.warning(warning_msg)
                else:
                    logger.warning(warning_msg)

            if instr_instance is None:
                dict_Instr[base_name] = []
                continue

            # If a list of instruments, keep as list
            if isinstance(instr_instance, list):
                valid_instrs = []
                for instr in instr_instance:
                    try:
                        # Attempt to query IDN to test connection
                        idn = instr.get_idn()
                        valid_instrs.append(instr)
                    except Exception as e:
                        logger.warning(f"Failed to connect {base_name}: {e}")
                dict_Instr[base_name] = valid_instrs
            else:
                # Single instrument
                try:
                    instr_instance.get_idn()
                    dict_Instr[base_name] = [instr_instance]
                except Exception as e:
                    dict_Instr[base_name] = []
                    logger.warning(f"Failed to connect {base_name}: {e}")
                    if hasattr(self, "textbox") and self.textbox:
                        try:
                            self.textbox.insert("0.0", f"Warning: {base_name} not connected!\n", "1")
                        except Exception:
                            pass

        return dict_Instr
        
   
   
# ======================================
# Disconnect App Class
# ======================================
class DisconnectApp(customtkinter.CTk):
    def __init__(self, DissDict):
        super().__init__()

        # Configure window
        self.title("Disconnect Instruments")
        self.geometry("900x750")
        self.DissDict = DissDict

        # Load Image
        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "Pictures/HNI_Logo_RGB.jpg")),
            size=(200, 50)
        )

        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Sidebar label
        self.logo_text = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="List of Instruments",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_text.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Textbox for messages
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", rowspan=2)
        self.textbox.tag_config("1", foreground="green")

        # Label for textbox
        self.ListLabel = customtkinter.CTkLabel(
            self,
            text="Disconnect Devices",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.ListLabel.grid(row=0, column=1, padx=20, pady=(10, 0))

        # Buttons for each device
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

        # Exit button
        self.exit_button = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Exit",
            fg_color="red",
            command=self.quit_window
        )
        self.exit_button.grid(row=row_counter, column=0, padx=20, pady=(10, 10))

        # Enable/disable buttons based on instruments
        self.update_button_states()

    def update_button_states(self):
        """Enable or disable buttons based on instruments in the DissDict."""
        for device_name, button in self.buttons.items():
            if device_name in self.DissDict and self.DissDict[device_name]:
                button.configure(state="enable")
            else:
                button.configure(state="disabled")

    def disconnect_device(self, device_name):
        """Disconnect the devices for a given key."""
        devices = self.DissDict.get(device_name, [])
        if not devices:
            return

        for dev in devices:
            try:
                if device_name.strip() == 'Anritsu Vectro Analyzer MS4647B':
                    # Only VNA needs RTL before closing
                    dev.rtl()

                dev.Close()

                self.textbox.insert("0.0", f"{device_name} is disconnected\n", "1")
                self.textbox.see("0.0")

            except Exception as e:
                self.textbox.insert("0.0", f"Error disconnecting {device_name}: {e}\n", "1")
                self.textbox.see("0.0")

        # Disable button after disconnect
        self.buttons[device_name].configure(state="disabled")

    def quit_window(self):
        """Quit the application."""
        self.quit()
        self.destroy()


class DisconnectApp_new(customtkinter.CTk):
    def __init__(self, DissDict):
        super().__init__()
        self.title("Disconnect Instruments")
        self.geometry("900x750")
        self.DissDict = DissDict

        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Pictures/HNI_Logo_RGB.jpg")), size=(200,50))

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.logo_text = customtkinter.CTkLabel(self.sidebar_frame, text="List of Instruments", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_text.grid(row=1, column=0, padx=20, pady=(20,10))

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20,0), pady=(20,0), sticky="nsew", rowspan=2)
        self.textbox.tag_config("1", foreground="green")

        self.ListLabel = customtkinter.CTkLabel(self, text="Disconnect Devices", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ListLabel.grid(row=0, column=1, padx=20, pady=(10,0))

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

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", fg_color="red", command=self.quit_window)
        self.exit_button.grid(row=row_counter, column=0, padx=20, pady=(10,10))

        self.update_button_states()

    def update_button_states(self):
        for device_name, button in self.buttons.items():
            if device_name in self.DissDict:
                button.configure(state="enable")
            else:
                button.configure(state="disabled")

    def disconnect_device(self, device_name):
        devices = self.DissDict.get(device_name)
        if devices:
            for dev in devices:
                try:
                    if hasattr(dev, "RTL"):
                        dev.RTL()
                    dev.Close()
                    self.textbox.insert("0.0", f"{device_name} disconnected.\n")
                    self.textbox.see("0.0")
                except Exception as e:
                    self.textbox.insert("0.0", f"Error disconnecting {device_name}: {e}\n")
                    self.textbox.see("0.0")
            self.buttons[device_name].configure(state="disabled")

    def quit_window(self):
        self.quit()
        self.destroy()