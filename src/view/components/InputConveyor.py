from CustomTkinter import customtkinter
from tkinter import BooleanVar

class InputConveyor:
    def __init__(self, frame):
        self.frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        self.inversor = BooleanVar()
        self.sensor_presenca = BooleanVar()
        self.sensor_posicao = BooleanVar()
        
        self.main_content()
        
        
    def main_content(self):
        
        lb_inversor = customtkinter.CTkLabel(self.frame, text="Inversor?")
        lb_inversor.grid(row=0, column=0, padx=3, pady=(3, 10), sticky='ws')
        ck_inversor = customtkinter.CTkCheckBox(self.frame, text="", variable=self.inversor, border_color=("#4A4A4A", "#949A9F"))
        ck_inversor.grid(row=1, column=0, padx=3, pady=(3, 10), sticky='nsew')
        
        lb_s_presenca = customtkinter.CTkLabel(self.frame, text="Sensor de presença?")
        lb_s_presenca.grid(row=0, column=1, padx=3, pady=(3, 10), sticky='ws')
        s_presenca = customtkinter.CTkCheckBox(self.frame, text="", variable=self.sensor_presenca)
        s_presenca.grid(row=1, column=1, padx=3, pady=(3, 10), sticky='nsew')
        
        lb_s_pos = customtkinter.CTkLabel(self.frame, text="Sensor de posição?")
        lb_s_pos.grid(row=0, column=2, padx=3, pady=(3, 10), sticky='ws')
        s_pos = customtkinter.CTkCheckBox(self.frame, text="", variable=self.sensor_posicao)
        s_pos.grid(row=1, column=2, padx=3, pady=(3, 10), sticky='nsew')