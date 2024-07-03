from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab
from view.components.InputRobo import InputRobo
from view.components.InputMesa import InputMesa


import tkinter as tk

class Zonaframe:
    def __init__(self, frame):
        self.frame: customtkinter.CTkComboBox = frame
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.actual_entity = tk.StringVar()
        
        self.entidades = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        self.entidades.grid(row=0, column=0, padx = 3, pady=0, sticky='w')
        
        self.options_entidade = ["Robôs", "Mesas", "Esteiras"]
        self.lista_robos = []
        self.lista_mesas = []
        self.lista_esteiras = []
        
        self.conteudo: customtkinter.CTkFrame = None
        
        self.frame_entidades()
        
            
    def frame_entidades(self):
        global entityes
        entityes = customtkinter.CTkComboBox(self.entidades,
                                             values=self.options_entidade,
                                             variable=self.actual_entity,
                                             width=90
                                             )
        
        entityes.grid(row=0, column=0, padx=3, pady=3, sticky='w')
        
        entityes.set("Robôs")
        
        global add_ent
        add_ent = FakeTab(self.entidades, "+", self.new_entity)
        add_ent = add_ent.get_button()
        add_ent.grid(row=0, column=2, padx=3, pady=3, sticky='w')
        
        self.rb_frame()
        
        self.actual_entity.trace_add('write', self.on_entidades_selected)
            
    def rb_frame(self):
        if self.lista_robos.__len__() == 0:
            new_ent = FakeTab(self.entidades, "rb1")
            new_ent = new_ent.get_button()
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_robos.append(new_ent)
            
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="green")
        InputRobo(self.conteudo)
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
    def mesa_frame(self):
        if self.lista_mesas.__len__() == 0:
            new_ent = FakeTab(self.entidades, "ms1")
            new_ent = new_ent.get_button()
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_mesas.append(new_ent)
            
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="blue")
        InputMesa(self.conteudo)
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
    
    def est_frame(self):
        if self.lista_esteiras.__len__() == 0:
            new_ent = FakeTab(self.entidades, "es1")
            new_ent = new_ent.get_button()
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_esteiras.append(new_ent)
            
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="red")
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
        
        ################### Utils ###################
        

    def on_entidades_selected(self, *args):
        if entityes.get() == "Robôs":
            print("Robôs")
            self.remove_entity()
            self.set_entidades(self.lista_robos)
            
            self.rb_frame()
        elif entityes.get() == "Mesas":
            print("Mesas")
            self.remove_entity()
            self.set_entidades(self.lista_mesas)
            
            self.mesa_frame()
        elif entityes.get() == "Esteiras":
            print("Esteiras")
            self.remove_entity()
            self.set_entidades(self.lista_esteiras)
            
            self.est_frame()
            
    def remove_entity(self):
        for widget in self.entidades.winfo_children():
            if type(widget) == customtkinter.CTkComboBox:
                continue
            text = widget.cget("text")
            if text == "+":
                continue
            print(text)
            widget.grid_forget()
                
    def set_entidades(self, entidades: list):
        for i in entidades:
            i.grid(row=0, column=entidades.index(i) + 1, padx=5, pady=0, sticky='w')
            
    def new_entity(self):
        if self.actual_entity.get() == "Robôs":
            n_entidades = self.lista_robos.__len__()
            nome = "rb"
            if n_entidades >= 5:
                return
            
        elif self.actual_entity.get() == "Mesas":
            n_entidades = self.lista_mesas.__len__()
            nome = "ms"
            if n_entidades >= 5:
                return
            
        elif self.actual_entity.get() == "Esteiras":
            n_entidades = self.lista_esteiras.__len__()
            nome = "es"
            if n_entidades >= 5:
                return
        
        grid_info: dict = add_ent.grid_info()
        aux = add_ent
        add_ent.grid_forget()
        
        nome = f"{nome} {n_entidades + 1}"
        new_ent = FakeTab(self.entidades, nome)
        new_ent = new_ent.get_button()
        new_ent.grid(row = grid_info.get('row'),
                     column = grid_info.get('column'),
                     padx = 3,
                     pady = 3,
                     sticky ='w')
        
        aux.grid(row = grid_info.get('row'),
                 column = grid_info.get('column') + 1,
                 padx = 3,
                 pady = 3,
                 sticky ='w')
        
        if self.actual_entity.get() == "Robôs":
            self.lista_robos.append(new_ent)
            
        elif self.actual_entity.get() == "Mesas":
            self.lista_mesas.append(new_ent)
            
        elif self.actual_entity.get() == "Esteiras":
            self.lista_esteiras.append(new_ent)
        