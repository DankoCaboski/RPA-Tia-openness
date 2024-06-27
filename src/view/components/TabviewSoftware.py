from CustomTkinter import customtkinter

class TabviewSoftware:
    def __init__(self, sw_frame):
        
        robos = customtkinter.CTkFrame(sw_frame)
        robos.grid_columnconfigure(0, weight=1)
        robos.grid_columnconfigure(1, weight=1)
        robos.grid_columnconfigure(2, weight=1)
        robos.grid_columnconfigure(3, weight=1)
        
        label_1 = customtkinter.CTkLabel(robos, text="Quais robôs deseja adicionar:")
        label_1.grid(row=0, column=0, columnspan=4, padx=(0,80), sticky="wens")
        
        lb_manuf = customtkinter.CTkLabel(robos, text="Fabricante")
        lb_qtd_abb = customtkinter.CTkLabel(robos, text="ABB")
        lbqtd_kuka = customtkinter.CTkLabel(robos, text="KUKA")
        lb_qtd_fanuc = customtkinter.CTkLabel(robos, text="FANUC")
        
        lb_manuf.grid(row=1, column=1, padx=(23,0), pady=10, sticky="wens")
        lb_qtd_abb.grid(row=2, column=1, padx=(20,0), pady=10, sticky="wens")
        lbqtd_kuka.grid(row=3, column=1, padx=(20,0), pady=10, sticky="wens")
        lb_qtd_fanuc.grid(row=4, column=1, padx=(20,0), pady=10, sticky="wens")
        
        lb_qtd = customtkinter.CTkLabel(robos, text="Quantidade")
        global en_qtd_abb, en_qtd_kuka, en_qtd_fanuc
        en_qtd_abb = customtkinter.CTkEntry(robos, width=50)
        en_qtd_kuka = customtkinter.CTkEntry(robos, width=50)
        en_qtd_fanuc = customtkinter.CTkEntry(robos, width=50)
        
        lb_qtd.grid(row=1, column=2, padx=(0,105),  pady=10, sticky="wens")
        en_qtd_abb.grid(row=2, column=2, padx=(0,105), pady=10)
        en_qtd_kuka.grid(row=3, column=2, padx=(0,105), pady=10)
        en_qtd_fanuc.grid(row=4, column=2, padx=(0,105), pady=10)
        
        
        
        ################### Mesa giratoria ###################
        
        mesas = customtkinter.CTkFrame(sw_frame)
        label_2 = customtkinter.CTkLabel(mesas, text="Mesas giratórias que deseja adicionar: ")
        label_2.grid(row=0, column=0, sticky="e", padx=(7,10), pady=10)
        
        global mg_entry
        mg_entry = customtkinter.CTkEntry(mesas)
        mg_entry.insert(0, "0")
        mg_entry.grid(row=0, column=1, padx=(10,10), pady=10, sticky="w")
        
        ################### gp ###################
        
        grampos = customtkinter.CTkFrame(sw_frame)
        label_3 = customtkinter.CTkLabel(grampos, text="Grampos que deseja adicionar: ")
        label_3.grid(row=0, column=0, sticky="e", padx=(7,10), pady=10)
        
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
            'robots': self.get_robots(),
            'turntables': mg_entry.get(),
            'grippers': gp_entry.get()
        }
        
    def get_robots(self):
        return {
            'abb': en_qtd_abb.get(),
            'kuka': en_qtd_kuka.get(),
            'fanuc': en_qtd_fanuc.get()
        }