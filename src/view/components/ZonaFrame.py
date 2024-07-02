from CustomTkinter import customtkinter

from view.components.TabviewSoftware import TabviewSoftware

class Zonaframe:
    def __init__(self, frame):
        self.frame = customtkinter.CTkFrame(frame)
        
        button = customtkinter.CTkButton(self.frame, text="ZonaFrame")
        button.pack()