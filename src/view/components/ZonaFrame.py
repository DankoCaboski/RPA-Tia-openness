from CustomTkinter import customtkinter

from view.components.TabviewSoftware import TabviewSoftware

class Zonaframe:
    def __init__(self, frame):
        
        entidades = customtkinter.CTkComboBox(frame, values=["Robôs", "Mesas", "Esteiras"])
        entidades.grid(row=0, column=0, padx=(0,10), pady=10)