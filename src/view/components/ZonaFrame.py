from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab


import tkinter as tk

class Zonaframe:
    def __init__(self, frame):
        self.frame: customtkinter.CTkComboBox = frame
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.actual_entity = tk.StringVar()
        
        self.entidades = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        self.entidades.grid(row=0, column=0, padx=0, pady=0, sticky='w')
        
        self.lista_entidades = []
        
        self.conteudo: customtkinter.CTkFrame = None
        
        self.frame_entidades()
        
            
    def frame_entidades(self):
        global entityes
        entityes = customtkinter.CTkComboBox(self.entidades,
                                             values=["Robôs", "Mesas", "Esteiras"],
                                             variable=self.actual_entity
                                             )
        entityes.grid(row=0, column=0, padx=0, pady=0, sticky='w')
        
        entityes.set("Robôs")
        
        if self.lista_entidades.__len__() == 0:
            new_ent = FakeTab(self.entidades, "rb1")
            new_ent = new_ent.get_button()
            new_ent.grid(row=0, column=1, padx=0, pady=0, sticky='w')
            self.lista_entidades.append(new_ent)
        
        global add_ent
        add_ent = FakeTab(self.entidades, "+", self.new_entity)
        add_ent = add_ent.get_button()
        add_ent.grid(row=0, column=2, padx=0, pady=0, sticky='w')
        
        self.rb_frame()
        
        self.actual_entity.trace_add('write', self.on_entidades_selected)
            
    def rb_frame(self):
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="green")
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
    def mesa_frame(self):
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="blue")
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
    
    def est_frame(self):
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="red")
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
        
        ################### Utils ###################
        

    def on_entidades_selected(self, *args):
        if entityes.get() == "Robôs":
            print("Robôs")
            self.rb_frame()
        elif entityes.get() == "Mesas":
            print("Mesas")
            self.mesa_frame()
        elif entityes.get() == "Esteiras":
            print("Esteiras")
            self.est_frame()
            
    def new_entity(self):
        
        n_entidades = self.lista_entidades.__len__()
        if n_entidades >= 5:
            return
        
        grid_info: dict = add_ent.grid_info()
        aux = add_ent
        add_ent.grid_forget()
        
        nome = f"rb{n_entidades + 1}"
        new_ent = FakeTab(self.entidades, nome)
        new_ent = new_ent.get_button()
        new_ent.grid(row = grid_info.get('row'),
                     column = grid_info.get('column'),
                     padx=0,
                     pady=0,
                     sticky='w')
        
        aux.grid(row = grid_info.get('row'),
                 column = grid_info.get('column') + 1,
                 padx=0,
                 pady=0,
                 sticky='w')
        
        self.lista_entidades.append(new_ent)