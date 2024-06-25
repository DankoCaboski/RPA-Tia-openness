import customtkinter
import tkinter as tk
from openness.services.Utils import Utils

class HwFrame:
    def __init__(self, frame):
        self.frame = customtkinter.CTkScrollableFrame(frame)    
           
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1) 
        
        self.opcoes_Hardware = ["PLC", "IHM", "IO Node"]
        
        self.mlfb_Plc = []
        self.mlfb_ihm = []
        self.mlfb_npde = []
        self.mlfb_List = [self.mlfb_Plc, self.mlfb_ihm, self.mlfb_npde]
        
        self.row_counter = 1
        self.get_mlfb_by_hw_type()
        self.add_hw()
    
    def add_hw(self):
        btn_add_hw = customtkinter.CTkButton(self.frame, text="Adicionar Hardware", command=self.add_hw_combobox)
        btn_add_hw.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        
    def add_hw_combobox(self):        
        tupla_Input = {"combobox": tk.StringVar(), "mlfb": tk.StringVar(), "firm_version": tk.StringVar(), "entry": tk.StringVar()}
        
        type_hw = customtkinter.CTkComboBox(self.frame, variable=tupla_Input["combobox"], values=self.opcoes_Hardware)
        type_hw.grid(row=self.row_counter, column=0, padx=10, pady=10)
        
        hw_mlfb = customtkinter.CTkComboBox(self.frame, variable=tupla_Input["mlfb"])
        hw_mlfb.grid(row=self.row_counter, column=1, padx=10, pady=10)
        
        hw_firmware = customtkinter.CTkComboBox(self.frame, values=["firmware1", "firmware2", "firmware3"])
        hw_firmware.grid(row=self.row_counter, column=2, padx=10, pady=10)
        
        hw_name = customtkinter.CTkEntry(self.frame, textvariable=tupla_Input["entry"])
        hw_name.grid(row=self.row_counter, column=3, padx=10, pady=10)
        
        def update_mlfb_combobox(*args):
            selected_option = tupla_Input["combobox"].get()
            
            if selected_option == "PLC":
                valueSource = self.mlfb_List[0]
            elif selected_option == "IHM":
                valueSource = self.mlfb_List[1]
            elif selected_option == "IO Node":
                valueSource = self.mlfb_List[2]
            else:
                valueSource = []

            hw_mlfb.configure(values=valueSource)
        
        tupla_Input["combobox"].trace_add('write', update_mlfb_combobox)
        
        self.row_counter += 1
        
    def get_mlfb_by_hw_type(self):
        i = 0
        for hw_type in self.opcoes_Hardware:
            mlfbs = Utils().get_mlfb_by_hw_type(hw_type)
            for mlfb in mlfbs:
                self.mlfb_List[i].append(mlfb[0])
            i += 1