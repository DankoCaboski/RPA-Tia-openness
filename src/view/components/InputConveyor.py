from CustomTkinter import customtkinter

class InputConveyor:
    def __init__(self, frame):
        self.frame: customtkinter.CTkFrame = frame
        
        self.main_content()
        
        
    def main_content(self):
        lb_conveyor = customtkinter.CTkLabel(self.frame, text="Esteira")
        lb_conveyor.grid(row=0, column=0, padx=3, pady=3, sticky='ws') 