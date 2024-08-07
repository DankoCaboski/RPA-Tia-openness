from CustomTkinter import customtkinter


class InputMesa:
    def __init__(self, frame):
        self.frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.main_content()
        
        
    def main_content(self):
        driver_label = customtkinter.CTkLabel(self.frame, text="Driver")
        driver_label.grid(row=0, column=0, padx=6, pady=3, sticky='ws')
        
        driver_input = customtkinter.CTkComboBox(self.frame, width=90, values=["SEW", "Sinamics"])
        driver_input.grid(row=1, column=0, padx=3, pady=3, sticky='wn')
        
        ladoA = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        ladoA.grid(row=0, column=0, padx=6 , pady=3, sticky='es')
        self.frame_lado(ladoA, "A")
        
        ladoB = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        ladoB.grid(row=0, column=1, padx=6, pady=3, sticky='ws')
        self.frame_lado(ladoB, "B")
        
        ladoC = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        ladoC.grid(row=1, column=0, padx=6 , pady=3, sticky='en')
        self.frame_lado(ladoC, "C")
        
        ladoD = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        ladoD.grid(row=1, column=1, padx=6, pady=3, sticky='wn')
        self.frame_lado(ladoD, "D")
        
        
    def frame_lado(self, frame, lado):
        nome_lado = f"Lado {lado}"
        lado_label = customtkinter.CTkLabel(frame, text=nome_lado)
        lado_label.grid(row=0, column=0, padx=3, sticky='w')
        
        pro1 = customtkinter.CTkLabel(frame, text="Produto 1")
        pro1.grid(row=1, column=0, padx=3, sticky='w')
        
        prod2 = customtkinter.CTkLabel(frame, text="Produto 2")
        prod2.grid(row=2, column=0, padx=3, sticky='w')
        
        prod3 = customtkinter.CTkLabel(frame, text="Produto 3")
        prod3.grid(row=3, column=0, padx=3, sticky='w')
        
        
        cl = customtkinter.CTkLabel(frame, text="CL")
        cl.grid(row=0, column=1, padx=3, sticky='w')
        
        cl_p1 = customtkinter.CTkEntry(frame, width=40, height=15)
        cl_p1.grid(row=1, column=1, padx=3, sticky='w')
        
        cl_p2 = customtkinter.CTkEntry(frame, width=40, height=15)
        cl_p2.grid(row=2, column=1, padx=3, sticky='w')
        
        cl_p3 = customtkinter.CTkEntry(frame, width=40, height=15)
        cl_p3.grid(row=3, column=1, padx=3, sticky='w')
        
        
        pp = customtkinter.CTkLabel(frame, text="PP")
        pp.grid(row=0, column=2, padx=3, sticky='w')
        
        pp_p1 = customtkinter.CTkEntry(frame, width=40, height=15)
        pp_p1.grid(row=1, column=2, padx=3, sticky='w')
        
        pp_p2 = customtkinter.CTkEntry(frame, width=40, height=15)
        pp_p2.grid(row=2, column=2, padx=3, sticky='w')
        
        pp_p3 = customtkinter.CTkEntry(frame, width=40, height=15)
        pp_p3.grid(row=3, column=2, padx=3, sticky='w')