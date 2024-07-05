from CustomTkinter import customtkinter

class InputRobo:
    def __init__(self, frame) -> None:
        self.frame: customtkinter.CTkFrame = frame
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        self.fabricantes = ["ABB", "Kuka", "Fanuc"]
        self.operacoes = ["Solda", "Manipulação"]
        
        self.input_robo()
        
        self.lista_robos = []
        
    def input_robo(self):
        lb_fabricante = customtkinter.CTkLabel(self.frame, text="Fabricante")
        lb_fabricante.grid(row=0, column=0, padx=3, pady=3, sticky='ws')
        fabricante = customtkinter.CTkComboBox(self.frame,
                                               width=90,
                                               values=self.fabricantes)
        fabricante.grid(row=1, column=0, padx=3, pady=3, sticky='wn')
        
        lb_aplicacao = customtkinter.CTkLabel(self.frame, text="Aplicação")
        lb_aplicacao.grid(row=0, column=1, padx=3, pady=3, sticky='ws')
        aplicacao = customtkinter.CTkComboBox(self.frame,
                                              width=90,
                                              values=self.operacoes)
        aplicacao.grid(row=1, column=1, padx=3, pady=3, sticky='wn')
        
        lb_nome = customtkinter.CTkLabel(self.frame, text="Nome")
        lb_nome.grid(row=0, column=2, padx=3, pady=3, sticky='ws')
        nome = customtkinter.CTkEntry(self.frame, width=90)
        nome.grid(row=1, column=2, padx=3, pady=3, sticky='wn')