from CustomTkinter import customtkinter

class TabviewSoftware:
    def __init__(self, frame):
        self.tabview  = customtkinter.CTkTabview(frame, anchor="nw")
        
        self.tabview.add("Robô")
        self.tabview.add("Mesa")
        self.tabview.add("Grampo")
    
        self.tabview.set("Robô")