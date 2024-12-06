import tkinter
import tkinter.messagebox
import customtkinter
from CTkListbox import *
import os
from PIL import Image,ImageTk
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from itertools import count
import pandas as pd
import keyboard 
plt.rcParams.update({'font.size':22})



customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


fig, ax = plt.subplots()
fig.set_size_inches(11,5.3)

# index = count()

def animate(i):
    # data = pd.read_csv('data.csv')
    # x = data['x_value']
    # y1 = data['total_1']
    # y2 = data['total_2']
    data = pd.read_csv(nSTR)
    x = data[xSTR]
    y1 = data[ySTR]

    ax.cla()
    ax.plot(x, y1, label = "Signal", linewidth=3.0, color = "red")
    # ax.plot(x, y2, label = "Chanel 2")

    ax.legend(loc = "upper left")
    plt.grid()
    # ax.tight_layout()



class LiveUpdate(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.Path = None
        self.xVal = None
        self.yVal = None
        self.hPos = 0

        # # Start the Moving
        # f = self.Move(self.hPos) 
            
        # configure window
        self.title("Live Data Tracking")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
    

        # Load Image
        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "HNI_Logo_RGB.png")), size=(300, 50))


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)



        # Image Logo HNI
        self.sidebar_frame = customtkinter.CTkLabel(self.sidebar_frame,   image=self.logo_image,  text="",)
        self.sidebar_frame.grid(row=0, column=0, padx=20, pady=20)

        
        # Create Label for Motor Sliders X and Y Position adjustments
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Horitontal Position Adjustment", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Slider 1
        self.sidebar_button_1 = customtkinter.CTkSlider(self.sidebar_frame, width=300,height=20,from_=0,to=7, number_of_steps=100, command = self.slider_hPos)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        # Entry Box 1
        self.Entry_hPos = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Entry Hporizontal Position")
        self.Entry_hPos.grid(row=3, column=0, padx=20, pady=10)

        # Enter Button 1
        self.Button_hPos = customtkinter.CTkButton(self.sidebar_frame, text = "Enter", fg_color = "green")
        self.Button_hPos.grid(row=3, column=2, padx=20, pady=(10, 10))

        

        
        # Create Label for Motor Sliders X and Y Position adjustments
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vertical Position Adjustment", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=4, column=0, padx=20, pady=(20, 10))
    
        # slider 2
        self.sidebar_button_2 = customtkinter.CTkSlider(self.sidebar_frame, width=300,height=20,from_=0,to=7, number_of_steps=100, command = self.slider_vPos)
        self.sidebar_button_2.grid(row=5, column=0, padx=20, pady=10)

        # Entry Box 2
        self.Entry_vPos = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Entry Vertical Position", command = self.Enter_hValue)
        self.Entry_vPos.grid(row=6, column=0, padx=20, pady=10)

        # Enter Button 2
        self.Button_vPos = customtkinter.CTkButton(self.sidebar_frame, text = "Enter", fg_color = "green")
        self.Button_vPos.grid(row=6, column=2, padx=20, pady=(10, 10))



        # Exit Buttons 
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text = "Exit", fg_color = "red",  command= self.QuitWindow)
        self.sidebar_button_5.grid(row=9, column=0, padx=20, pady=(10, 10))

        canvas = FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)



    def QuitWindow(self):
        self.quit()
        self.destroy()

    def slider_hPos(self, value):
        # value = self.sidebar_button_1.get()
        print(value)
        self.sidebar_button_2.set(value)
        # self.sidebar_button_1.config(command=self.Move(self.hPos))

    def slider_vPos(self, value):
        # value = self.sidebar_button_1.get()
        print(value)
        self.sidebar_button_1.set(value)

    def Enter_hValue(self):
        




    def update_label(value):
        label.config(text=f"Slider Value: {value}")




    
    





class Input_Information_Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.Path = None
        self.xVal = None
        self.yVal = None
        self.Accuracy = None
            
        # configure window
        self.title("Tracking File Data")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
    

        # Load Image
        image_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "HNI_Logo_RGB.png")), size=(300, 50))


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)



        # Image Logo HNI
        self.sidebar_frame = customtkinter.CTkLabel(self.sidebar_frame,   image=self.logo_image,  text="",)
        self.sidebar_frame.grid(row=1, column=0, padx=410, pady=20)


        # Create Label for Path , file Name and Axis Names
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Input data", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=4, column=0, padx=20, pady=(20, 10))

        # Entry Box for Path
        self.entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Path to File C:\....")
        self.entry.grid(row=5, column=0, padx=20, pady=(20, 10))

        #Entry Box for X Axis
        self.entry_xVal = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="X Axis Name")
        self.entry_xVal.grid(row=6, column=0, padx=20, pady=(20, 10))

        #Entry Box for Y Value
        self.entry_yVal = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Y Axis Name")
        self.entry_yVal.grid(row=7, column=0, padx=20, pady=(20, 10))

        # Entry Box for Acciracy
        self.entry_Accuracy = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Accuracy 0.1, 0.01, 0.001 ...")
        self.entry_Accuracy.grid(row=8, column=0, padx=20, pady=(20, 10))


        # Buttons 
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text = "Submit", fg_color = "green",  command= self.PassEntrys)
        self.sidebar_button_5.grid(row=9, column=0, padx=20, pady=(10, 10))



    def PassEntrys(self):
        self.Path = self.entry.get()
        self.xVal = self.entry_xVal.get()
        self.yVal = self.entry_yVal.get()
        self.Accuracy = self.entry_Accuracy.get()
        print(self.Path, self.xVal, self.yVal, self.Accuracy)
        self.quit()
        self.destroy()

    
    def Data(self):
        return self.Path, self.xVal, self.yVal, self.Accuracy 


        


if __name__ == "__main__":
    AppSelect = Input_Information_Window()
    nSTR = None
    xSTR = None
    ySTR = None
    AppSelect.mainloop()
    nSTR,xSTR,ySTR,Accuracy = AppSelect.Data()
    app = LiveUpdate()
    ani = FuncAnimation(fig, animate, interval = 2000)
    app.mainloop()


