from CustomTkinter import customtkinter

from view.components.InputLado import InputLado


class InputMesa:
    def __init__(self, frame):
        self.frame: customtkinter.CTkFrame = frame
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        
        
        self.main_content()
        
    def main_content(self):
        driver_label = customtkinter.CTkLabel(self.frame, text="Driver")
        driver_label.grid(row=0, column=0, padx=3, pady=3, sticky='ws')
        
        driver_input = customtkinter.CTkComboBox(self.frame, width=90, values=["SWE", "Sinamics"])
        driver_input.grid(row=1, column=0, padx=3, pady=3, sticky='wn')
        
        ladoA = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        ladoA.grid(row=0, column=1, padx=3 , pady=3, sticky='e')
        InputLado(ladoA, "A")
        
        ladoB = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        ladoB.grid(row=0, column=2, padx=3, pady=3, sticky='w')
        InputLado(ladoB, "B")
        
        ladoC = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        ladoC.grid(row=1, column=1, padx=3 , pady=3, sticky='e')
        InputLado(ladoC, "C")
        
        ladoD = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        ladoD.grid(row=1, column=2, padx=3, pady=3, sticky='w')
        InputLado(ladoD, "D")
        
        