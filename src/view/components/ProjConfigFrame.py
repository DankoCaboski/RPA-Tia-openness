from CustomTkinter import customtkinter

from view.components.ZonaFrame import Zonaframe

import tkinter as tk
from openness.services.Utils import Utils

class ProjConfigFrame:
    def __init__(self, frame):
        self.tabview  = customtkinter.CTkTabview(frame, anchor="nw")
        
        self.tabview.add("Hardware")
        
        self.tabview.add("Software")
        
        self.tabview.set("Hardware")
        
        self.hw_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Hardware"))
        
        self.sw_options = ["Robôs", "Mesa", "Grampos"]
        
        self.zonas = []
        
        self.opcoes_Hardware = ["PLC", "IHM", "IO Node"]
        
        self.firm_versions = {}
        self.mlfb_List = [[], [], []]
        
        self.hardware_values = []
        
        self.row_counter = 1
        self.get_mlfb_by_hw_type()
        
        self.add_hw()
        self.configure_sw()
        
        ################### Hardware tab ###################
    
    def add_hw(self):
        self.hw_frame.pack(fill='both', expand=True)
        self.hw_frame.configure(fg_color="transparent")
        self.hw_frame.grid_columnconfigure(0, weight=1)
        self.hw_frame.grid_columnconfigure(1, weight=0)
        self.hw_frame.grid_columnconfigure(2, weight=0)
        self.hw_frame.grid_columnconfigure(3, weight=0)
        self.hw_frame.grid_columnconfigure(4, weight=1)
        
        global btn_add_hw
        btn_add_hw = customtkinter.CTkButton(self.hw_frame,
                                             text="Adicionar Hardware",
                                             command=self.add_hw_combobox
                                             )
        
        btn_add_hw.grid(row=0, column=1, columnspan=2, pady=10)
            
    def add_hw_combobox(self):                
        input = {
            "combobox": tk.StringVar(),
            "mlfb": tk.StringVar(),
            "firm_version": tk.StringVar(),
            "entry": tk.StringVar(),
            "Start_Adress": tk.StringVar()
            }
        
        self.hardware_values.append(input)
        
        def focus_next_widget(event):
            event.widget.tk_focusNext().focus()
            return "break"
        
        type_hw = customtkinter.CTkComboBox(self.hw_frame,
                                            width=120,
                                            variable=input["combobox"],
                                            values=self.opcoes_Hardware
                                            )
        
        type_hw.grid(row=self.row_counter, column=0, padx=(10,0), pady=10, sticky='e')
        
        hw_mlfb = customtkinter.CTkComboBox(self.hw_frame, variable=input["mlfb"])
        hw_mlfb.grid(row=self.row_counter, column=1, padx=(10,0), pady=10)
        
        hw_firmware = customtkinter.CTkComboBox(self.hw_frame, width=120, variable=input["firm_version"])
        hw_firmware.grid(row=self.row_counter, column=2, padx=(10,0), pady=10)
        
        hw_name = customtkinter.CTkEntry(self.hw_frame, width=120, textvariable=input["entry"])
        hw_name.grid(row=self.row_counter, column=3, padx=(10,0), pady=10)
        
        special_entry = customtkinter.CTkEntry(self.hw_frame, textvariable=input["Start_Adress"])
        special_entry.grid(row=self.row_counter, column=4, padx=(10,0), pady=10)
        
        special_entry.bind('<Return>', focus_next_widget)
        special_entry.grid_remove()  # Inicia sem aparecer
        
        def update_mlfb_combobox(*args):
            selected_option = input["combobox"].get()
            print(f"Selected hardware type: {selected_option}")
            
            if selected_option == "PLC":
                valueSource = self.mlfb_List[0]
                special_entry.grid_remove()
            elif selected_option == "IHM":
                valueSource = self.mlfb_List[1]
                special_entry.grid_remove()
            elif selected_option == "IO Node":
                valueSource = self.mlfb_List[2]
                special_entry.grid()
                btn_add_hw.grid(row=0, column=0, columnspan=5, pady=10)
            else:
                valueSource = []

            hw_mlfb.configure(values=valueSource)
            
        def update_firmware_combobox(*args):
            selected_mlfb = input["mlfb"].get()

            firmware_versions = self.firm_versions.get(selected_mlfb, [])
            print(f"Firmware versions for {selected_mlfb}: {firmware_versions}")
            hw_firmware.configure(values=firmware_versions)
            if firmware_versions:
                hw_firmware.set(firmware_versions[0])  # Define a primeira versão como padrão
        
        input["combobox"].trace_add('write', update_mlfb_combobox)
        input["mlfb"].trace_add('write', update_firmware_combobox)
        
        self.row_counter += 1
        
        
        ################### Software tab ###################
        
    def configure_sw(self):
        self.tabview.tab("Software").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Software").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Software").grid_columnconfigure(2, weight=1)
        self.tabview.tab("Software").grid_columnconfigure(3, weight=1)

        self.tabview.tab("Software").grid_rowconfigure(0, weight=1)
        
        global zonas_view
        zonas_view = customtkinter.CTkTabview(self.tabview.tab("Software"),
                                              anchor="nw",
                                              command=self.on_tab_change,
                                              fg_color="#3D3D3D"
                                              )


        zonas_view.add("+")

        self.add_zona(zonas_view)

        zonas_view.grid(row=0, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
          
                
        ################### Utils ###################
        
    def on_tab_change(self):
        current_tab = zonas_view.get()
        if current_tab == "+":
            if len(self.zonas) >= 5:
                return
            zona_name = self.add_zona(zonas_view)
            zonas_view.set(zona_name)
            
    def get_mlfb_by_hw_type(self):
        for i, hw_type in enumerate(self.opcoes_Hardware):
            mlfbs = Utils().get_mlfb_by_hw_type(hw_type)
            for mlfb in mlfbs:
                self.mlfb_List[i].append(mlfb[0])
            
            firmware_data = Utils().get_firmware_by_mlfb(hw_type)
            for mlfb, version in firmware_data:
                if mlfb in self.firm_versions:
                    self.firm_versions[mlfb].append(version)
                else:
                    self.firm_versions[mlfb] = [version]
        
        print("Firmware versions dictionary:", self.firm_versions)
    
    def get_hardware_values(self):
        result = []
        for hw_value in self.hardware_values:
            hw_dict = {
                'type': hw_value['combobox'].get(),
                'mlfb': hw_value['mlfb'].get(),
                'firmware': hw_value['firm_version'].get(),
                'name': hw_value['entry'].get()
            }
            result.append(hw_dict)
        return result
    
    def get_blocks_to_import(self):
        raise NotImplementedError("'get_blocks_to_import' method not implemented yet.")
        # return self.sw_content.get_blocks_to_import()

    def add_zona(self, zonas_view: customtkinter.CTkTabview):
        l_zonas = len(self.zonas)
        zona_name = f"Zona {l_zonas + 1}"
        new_tab = zonas_view.add(zona_name)
        self.zonas.append(new_tab)
        zonas_view.set(zona_name)
        
        zonas_view.move(l_zonas + 1, "+")
        
        Zonaframe(zonas_view.tab(zona_name))

        return zona_name     
            
