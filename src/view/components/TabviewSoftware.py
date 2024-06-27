from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab


class TabviewSoftware:
    def __init__(self, sw_frame):
        
        robos = customtkinter.CTkFrame(sw_frame)
        label_1 = customtkinter.CTkLabel(robos, text="Robôs que deseja adicionar: ")
        label_1.grid(row=0, column=0, sticky="e", padx=(0,10), pady=10)
        
        global rb_entry
        rb_entry = customtkinter.CTkEntry(robos)
        rb_entry.insert(0, "0")
        rb_entry.grid(row=0, column=1, padx=(10,10), pady=10, sticky="w")
        
        ################### Mesa giratoria ###################
        
        mesas = customtkinter.CTkFrame(sw_frame)
        label_2 = customtkinter.CTkLabel(mesas, text="Mesas giratórias que deseja adicionar: ")
        label_2.grid(row=0, column=0, sticky="e", padx=(0,10), pady=10)
        
        global mg_entry
        mg_entry = customtkinter.CTkEntry(mesas)
        mg_entry.insert(0, "0")
        mg_entry.grid(row=0, column=1, padx=(10,10), pady=10, sticky="w")
        
        ################### gp ###################
        
        grampos = customtkinter.CTkFrame(sw_frame)
        label_3 = customtkinter.CTkLabel(grampos, text="Grampos que deseja adicionar: ")
        label_3.grid(row=0, column=0, sticky="e", padx=(0,10), pady=10)
        
        global gp_entry
        gp_entry = customtkinter.CTkEntry(grampos)
        gp_entry.insert(0, "0")
        gp_entry.grid(row=0, column=1, padx=(10,10), pady=10, sticky="w")
    
        
        self.frames = [robos, mesas, grampos]
        self.current_frame = 0
        
    def sw_content(self, index):
        if index == None:
            return self.frames[self.current_frame]
        else:
            return self.frames[index]
        
    def get_blocks_to_import(self):
        return {
            'robots': rb_entry.get(),
            'turntables': mg_entry.get(),
            'grippers': gp_entry.get()
        }