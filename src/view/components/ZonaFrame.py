from CustomTkinter import customtkinter

import tkinter as tk

class Zonaframe:
    def __init__(self, frame):
        self.frame: customtkinter.CTkComboBox = frame
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.actual_entity = tk.StringVar()
        
        self.entidades = customtkinter.CTkComboBox(self.frame,
                                                   values=["Robôs", "Mesas", "Esteiras"],
                                                   variable=self.actual_entity
                                                   )
        
        self.entidades.grid(row=0, column=0, padx=(0, 10), pady=10, sticky='w')
        self.entidades.set("Robôs")
        self.rb_frame()
        
        self.actual_entity.trace_add('write', self.on_entidades_selected)
        
    def on_entidades_selected(self, *args):
        if self.entidades.get() == "Robôs":
            print("Robôs")
            self.rb_frame()
        elif self.entidades.get() == "Mesas":
            print("Mesas")
            self.mesa_frame()
        elif self.entidades.get() == "Esteiras":
            print("Esteiras")
            self.est_frame()
        else:
            self.tabview_software = None
            
    def rb_frame(self):
        self.robo_frame = customtkinter.CTkFrame(self.frame, fg_color="green")
        self.robo_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
        
    def mesa_frame(self):
        self.tt_frame = customtkinter.CTkFrame(self.frame, fg_color="blue")
        self.tt_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
    
    def est_frame(self):
        self.esteira_frame = customtkinter.CTkFrame(self.frame, fg_color="red")
        self.esteira_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
        
