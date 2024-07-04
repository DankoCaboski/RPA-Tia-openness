from CustomTkinter import customtkinter
from view.components.FakeTab import FakeTab
from view.components.InputRobo import InputRobo
from view.components.InputMesa import InputMesa
from view.components.InputConveyor import InputConveyor


import tkinter as tk

class Zonaframe:
    def __init__(self, frame):
        self.frame: customtkinter.CTkFrame = frame
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.entity_type = tk.StringVar()
        self.aux_enity_type = tk.StringVar()
        
        self.add_ent = None
                
        self.selected_entity = None
        
        self.entidades = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        self.entidades.grid(row=0, column=0, padx = 0, pady=0, sticky='w')
        
        self.options_entidade = ["Robôs", "Mesas", "Esteiras"]
        self.lista_robos = []
        self.lista_mesas = []
        self.lista_esteiras = []
        
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color="#4A4A4A")
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
        
        self.frame_entidades()
        
            
    def frame_entidades(self):
        global entityes
        entityes = customtkinter.CTkComboBox(self.entidades,
                                             values=self.options_entidade,
                                             variable=self.entity_type,
                                             width=90
                                             )
        
        entityes.grid(row=0, column=0, padx=3, pady=3, sticky='w')
        
        entityes.set("Robôs")
        
        self.add_ent = FakeTab(self.entidades, "+", self.new_entity)
        self.add_ent = self.add_ent.get_button()
        self.add_ent.grid(row=0, column=2, padx=3, pady=3, sticky='w')
        
        self.aux_enity_type = "Robôs"
        self.rb_frame()
        
        self.entity_type.trace_add('write', self.on_entidades_selected)
            
    def rb_frame(self):
        if self.lista_robos.__len__() == 0:
            new_ent = self.gera_entidade("rb1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_robos.append(new_ent)
            
            if self.selected_entity is None:
                new_ent.invoke()
        
    def mesa_frame(self):
        if self.lista_mesas.__len__() == 0:   
            new_ent = self.gera_entidade("ms1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_mesas.append(new_ent)
            
    def est_frame(self):
        if self.lista_esteiras.__len__() == 0:
            new_ent = self.gera_entidade("es1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            self.lista_esteiras.append(new_ent)
            
    def gera_entidade(self, nome):
        try:
            new_ent = FakeTab(self.entidades, nome)
                
            new_ent = new_ent.get_button()
                
            new_ent.configure(command=lambda btn=new_ent: self.load_entity_frame(btn))
            new_ent.invoke()
            
            if new_ent is None:
                raise Exception("Erro ao criar nova entidade")
            
            return new_ent
        except Exception as e:
            print(f"Erro na função 'gera_entidade': {e}")
            return
        
        ################### Utils ###################
        

    def on_entidades_selected(self, *args):
        entityes.update_idletasks() 
        try:
            selecionado = entityes.get()
            if selecionado == self.aux_enity_type or selecionado == "":
                print("retornou")
                return
            print(f"Selecionado: {selecionado}")
            self.remove_entity()
            self.remove_widgets()
            
            if selecionado == "Robôs":
                self.set_entidades(self.lista_robos)
                self.aux_enity_type = "Robôs"
                self.rb_frame()
                
            elif selecionado == "Mesas":
                self.set_entidades(self.lista_mesas)
                self.aux_enity_type = "Mesas"
                self.mesa_frame()
                
            elif selecionado == "Esteiras":
                self.set_entidades(self.lista_esteiras)
                self.aux_enity_type = "Esteiras"
                self.est_frame()
                
            else:
                return
                
                
        
        except Exception as e:
            msg = f"Erro na função on_entidades_selected: {e}"
            print(msg)
            
    def remove_entity(self):
        """
        Remove todas as entidades do frame de entidades
        """
        for widget in self.entidades.winfo_children():
            if type(widget) == customtkinter.CTkComboBox:
                continue
            if widget == self.add_ent:
                continue
            widget.grid_forget()
                
    def set_entidades(self, entidades: list):
        """
        Popula o frame de entidades com os botões da entidade selecionada
        """
        for i in entidades:
            i.grid(row=0, column=entidades.index(i) + 1, padx=5, pady=0, sticky='w')
            i.update_idletasks() 
            
    def new_entity(self):
        entity_type = self.entity_type.get()
        
        if entity_type == "Robôs":
            n_entidades = self.lista_robos.__len__()
            if n_entidades >= 5:
                return
            nome = f"rb {n_entidades + 1}"
            new_ent = self.move_add_ent(nome)
            self.lista_robos.append(new_ent) 
            
        elif entity_type == "Mesas":
            n_entidades = self.lista_mesas.__len__()
            if n_entidades >= 5:
                return
            nome = f"mg {n_entidades + 1}"
            new_ent = self.move_add_ent(nome) 
            self.lista_mesas.append(new_ent)
               
        elif entity_type == "Esteiras":
            n_entidades = self.lista_esteiras.__len__()
            if n_entidades >= 5:
                return
            nome = f"es {n_entidades + 1}"
            new_ent = self.move_add_ent(nome)
            self.lista_esteiras.append(new_ent)     
            
        
    def move_add_ent(self, nome):
        try:
            grid_info: dict = self.add_ent.grid_info()
            
            self.add_ent.grid_forget()
        
            new_ent = self.gera_entidade(nome)
            
            new_ent.grid(row=0,
                        column = grid_info.get('column'),
                        padx = 3,
                        pady = 3,
                        sticky ='w')
            
            self.add_ent.grid(row=0,
                    column = grid_info.get('column') + 1,
                    padx = 3,
                    pady = 3,
                    sticky ='w')
            
            self.add_ent.update_idletasks()
            
            if new_ent is None:
                raise Exception("Erro ao criar nova entidade")
                
            return new_ent
        except Exception as e:
            print(f"Erro na função 'move_add_ent': {e}")
            
    def load_entity_frame(self, parent: customtkinter.CTkButton=None):
        # TODO: revisar a função que remove os widgets, com ela descomentada a aplicação cracha ao trocar de monitor
        # Att: Subistituir "widget.destroy()" por "widget.grid_forget()" aparentemente resolve o problema
        # Rever o retrive do widget que está sendo ocultado para evitar memory leak
        self.remove_widgets()
        self.change_all_entities_fg_color()
        
        self.selected_entity = parent
        if parent is not None:
            parent.configure(fg_color="#1F6AA5")
            if self.aux_enity_type == "Robôs":
                self.aux_enity_type
                InputRobo(self.conteudo)
            elif self.aux_enity_type == "Mesas":
                InputMesa(self.conteudo)
            elif self.aux_enity_type == "Esteiras":
                InputConveyor(self.conteudo)
        
    def remove_widgets(self):
        for widget in self.conteudo.winfo_children():
            widget.grid_forget()
            
    def change_all_entities_fg_color(self):
        for i in self.lista_robos:
            i.configure(fg_color="#4A4A4A")
        for i in self.lista_mesas:
            i.configure(fg_color="#4A4A4A")
        for i in self.lista_esteiras:
            i.configure(fg_color="#4A4A4A")