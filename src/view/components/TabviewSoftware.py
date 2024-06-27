from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab


class TabviewSoftware:
    def __init__(self, sw_frame):
        
        frame1 = customtkinter.CTkFrame(sw_frame)
        label_1 = customtkinter.CTkLabel(frame1, text="Robôs que deseja adicionar: ")
        label_1.grid(row=0, column=0, sticky="e", padx=(0,10), pady=10)
        
        rb_entry = customtkinter.CTkEntry(frame1)
        rb_entry.insert(0, "0")
        rb_entry.grid(row=0, column=1, padx=(10,10), pady=10, sticky="w")
        
        ################### Mesa giratoria ###################
        
        frame2 = customtkinter.CTkFrame(sw_frame)
        label_2 = customtkinter.CTkLabel(frame2, text="Mesas giratórias que deseja adicionar: ")
        label_2.grid(row=1, column=0, sticky="e", padx=(0,10), pady=10)
        
        mg_entry = customtkinter.CTkEntry(frame2)
        mg_entry.insert(0, "0")
        mg_entry.grid(row=1, column=1, padx=(10,10), pady=10, sticky="w")
        
        ################### gp ###################
        
        frame3 = customtkinter.CTkFrame(sw_frame)
        label_3 = customtkinter.CTkLabel(frame3, text="Grampos que deseja adicionar: ")
        label_3.grid(row=2, column=0, sticky="e", padx=(0,10), pady=10)
        
        gp_entry = customtkinter.CTkEntry(frame3)
        gp_entry.insert(0, "0")
        gp_entry.grid(row=2, column=1, padx=(10,10), pady=10, sticky="w")
    
        
        self.frames = [frame1, frame2, frame3]
        self.current_frame = 0
        
    def sw_content(self, index):
        if index == None:
            return self.frames[self.current_frame]
        else:
            return self.frames[index]