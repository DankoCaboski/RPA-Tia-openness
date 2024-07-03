from CustomTkinter import customtkinter

class InputLado:
    def __init__(self, frame, lado):
        self.frame: customtkinter.CTkFrame = frame
        self.main_content(lado)    
    
    def main_content(self, lado):
        nome_lado = f"Lado {lado}"
        lado_label = customtkinter.CTkLabel(self.frame, text=nome_lado)
        lado_label.grid(row=0, column=0, padx=3, sticky='w')
        
        pro1 = customtkinter.CTkLabel(self.frame, text="Produto 1")
        pro1.grid(row=1, column=0, padx=3, sticky='w')
        
        prod2 = customtkinter.CTkLabel(self.frame, text="Produto 2")
        prod2.grid(row=2, column=0, padx=3, sticky='w')
        
        prod3 = customtkinter.CTkLabel(self.frame, text="Produto 3")
        prod3.grid(row=3, column=0, padx=3, sticky='w')
        
        
        
        cl = customtkinter.CTkLabel(self.frame, text="CL")
        cl.grid(row=0, column=1, padx=3, sticky='w')
        
        lc_p1 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        lc_p1.grid(row=1, column=1, padx=3, sticky='w')
        
        lc_p2 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        lc_p2.grid(row=2, column=1, padx=3, sticky='w')
        
        lc_p3 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        lc_p3.grid(row=3, column=1, padx=3, sticky='w')
        
        
        pp = customtkinter.CTkLabel(self.frame, text="PP")
        pp.grid(row=0, column=2, padx=3, sticky='w')
        
        pp_p1 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        pp_p1.grid(row=1, column=2, padx=3, sticky='w')
        
        pp_p2 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        pp_p2.grid(row=2, column=2, padx=3, sticky='w')
        
        pp_p3 = customtkinter.CTkEntry(self.frame, width=40, height=15)
        pp_p3.grid(row=3, column=2, padx=3, sticky='w')
        