from CustomTkinter import customtkinter

class InputRobo:
    def __init__(self, frame) -> None:
        self.frame: customtkinter.CTkFrame = frame
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        self.operacoes = ["Solda", "Manipulação"]
        
        self.input_robo()
        
        self.lista_robos = []
        
    def input_robo(self):
        fabricante = customtkinter.CTkComboBox(self.frame,
                                               width=90,
                                               values=self.operacoes)
        fabricante.grid(row=0, column=0, padx=3, pady=3, sticky='w')
        
        aplicacao = customtkinter.CTkComboBox(self.frame, width=90)
        aplicacao.grid(row=0, column=1, padx=3, pady=3, sticky='w')
        
        nome = customtkinter.CTkEntry(self.frame, width=90)
        nome.grid(row=0, column=2, padx=3, pady=3, sticky='w')