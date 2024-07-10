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
        
        self.add_ent: customtkinter.CTkButton = None
        self.rm_ent: customtkinter.CTkButton = None
        self.entityes: customtkinter.CTkComboBox = None
                
        self.selected_entity = None
        
        self.entidades = customtkinter.CTkFrame(self.frame, fg_color=("#DEDEDE","#4A4A4A"))
        self.entidades.grid(row=0, column=0, padx = 0, pady=0, sticky='w')
        
        self.options_entidade = ["Robôs", "Mesas", "Esteiras"]
        
        self.botoes_robo: list[customtkinter.CTkButton] = []
        self.frames_robo: list[customtkinter.CTkFrame] = []
        self.lista_robos: list[list, list] = [self.botoes_robo, self.frames_robo]
        
        self.botoes_mesa: list[customtkinter.CTkButton] = []
        self.frames_mesas: list[customtkinter.CTkFrame] = []
        self.lista_mesas: list[list, list] = [self.botoes_mesa, self.frames_mesas]
        
        self.botoes_esteira: list[customtkinter.CTkButton] = []
        self.frames_esteira: list[customtkinter.CTkFrame] = []
        self.lista_esteiras: list[list, list] = [self.botoes_esteira, self.frames_esteira]
        
        self.lista_entidades = [self.lista_robos, self.lista_mesas, self.lista_esteiras]
        
        # Frame onde o conteudo da entidade será carregado
        self.conteudo = customtkinter.CTkFrame(self.frame, fg_color=("#DEDEDE","#4A4A4A"))
        self.conteudo.grid_columnconfigure(0, weight=1)
        self.conteudo.grid_rowconfigure(0, weight=1)
        self.conteudo.grid(row=1, column=0, columnspan=2, sticky='nsew')
        
        
        self.frame_entidades()
        
            
    def frame_entidades(self):
        self.entityes = customtkinter.CTkComboBox(self.entidades,
                                             values=self.options_entidade,
                                             variable=self.entity_type,
                                             width=90
                                             )
        
        self.entityes.grid(row=0, column=0, padx=3, pady=3, sticky='w')
        
        self.entityes.set("Robôs")
        
        self.add_ent = FakeTab(self.entidades, "+", self.new_entity)
        self.add_ent = self.add_ent.get_button()
        self.add_ent.configure(width = 10, hover_color="#696969")
        self.add_ent.grid(row=0, column=2, padx=3, pady=3, sticky='w')
        
        self.rm_ent = FakeTab(self.entidades, "-", self.pop_ent)
        self.rm_ent = self.rm_ent.get_button()
        self.rm_ent.configure(width = 10, hover_color="#696969")
        self.rm_ent.grid(row=0, column=3, padx=3, pady=3, sticky='w')
        
        self.aux_enity_type = "Robôs"
        self.rb_frame()
        
        self.entity_type.trace_add('write', self.on_entidades_selected)
            
    def rb_frame(self):
        if len(self.lista_robos[0]) == 0:
            new_ent = self.gera_entidade("RB1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
            
            if self.selected_entity is None:
                new_ent.invoke()      
        else:
            self.botoes_robo[0].invoke()
        
    def mesa_frame(self):
        if len(self.lista_mesas[0]) == 0:   
            new_ent = self.gera_entidade("MS1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
        
        else:
            self.botoes_mesa[0].invoke()
            
    def est_frame(self):
        if len(self.lista_esteiras[0]) == 0:
            new_ent = self.gera_entidade("ES1")
            new_ent.grid(row=0, column=1, padx=5, pady=0, sticky='w')
        else:
            self.botoes_esteira[0].invoke()
            
    def gera_entidade(self, nome) -> customtkinter.CTkButton:
        try:
            new_ent = FakeTab(self.entidades, nome)
                
            new_ent = new_ent.get_button()
                
            new_ent.configure(command=lambda btn=new_ent: self.load_entity_frame(btn))
            
            if self.aux_enity_type == "Robôs":
                self.botoes_robo.append(new_ent)
            elif self.aux_enity_type == "Mesas":
                self.botoes_mesa.append(new_ent)
            elif self.aux_enity_type == "Esteiras":
                self.botoes_esteira.append(new_ent)
                
            new_ent.invoke()
            
            if new_ent is None:
                raise Exception("Erro ao criar nova entidade")
            
            return new_ent
        except Exception as e:
            print(f"Erro na função 'gera_entidade': {e}")
            return
        
        ################### Utils ###################
        

    def on_entidades_selected(self, *args):
        try:
            selecionado = self.entityes.get()
            if selecionado == self.aux_enity_type or selecionado == "":
                self.entityes.update_idletasks() 
                return
            
            self.remove_entity()
            self.forget_widgets_self_conteudo()
            
            if selecionado == "Robôs":
                self.set_entidades(self.lista_robos[0])
                self.aux_enity_type = "Robôs"
                self.rb_frame()
                self.entityes.update_idletasks() 
                
            elif selecionado == "Mesas":
                self.set_entidades(self.lista_mesas[0])
                self.aux_enity_type = "Mesas"
                self.mesa_frame()
                self.entityes.update_idletasks() 
                
            elif selecionado == "Esteiras":
                self.set_entidades(self.lista_esteiras[0])
                self.aux_enity_type = "Esteiras"
                self.est_frame()
                self.entityes.update_idletasks() 
                
            else:
                raise Exception("Entidade não encontrada")
        
        except Exception as e:
            msg = f"Erro na função on_entidades_selected: {e}"
            print(msg)
            
    def remove_entity(self):
        """
        Remove todas as entidades do frame de entidades
        """
        for widget in self.entidades.winfo_children():
            if widget == self.add_ent or \
               widget == self.rm_ent or \
               isinstance(widget, customtkinter.CTkComboBox):
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
            n_entidades = len(self.lista_robos[0])
            if n_entidades >= 5:
                return
            nome = f"RB {n_entidades + 1}"
            self.append_ent(nome)
            
        elif entity_type == "Mesas":
            n_entidades = len(self.lista_mesas[0])
            if n_entidades >= 5:
                return
            nome = f"MG {n_entidades + 1}"
            self.append_ent(nome) 
               
        elif entity_type == "Esteiras":
            n_entidades = len(self.lista_esteiras[0])
            if n_entidades >= 5:
                return
            nome = f"ES {n_entidades + 1}"
            self.append_ent(nome)  
            
        
    def append_ent(self, nome):
        try:
            grid_info: dict = self.add_ent.grid_info()
            
            self.add_ent.grid_forget()
            
            self.rm_ent.grid_forget()
        
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
            
            self.rm_ent.grid(row=0,
                    column = grid_info.get('column') + 2,
                    padx = 3,
                    pady = 3,
                    sticky ='w')
            
            self.add_ent.update_idletasks()
            
            if new_ent is None:
                raise Exception("Erro ao criar nova entidade")
                
            return new_ent
        except Exception as e:
            print(f"Erro na função 'move_add_ent': {e}")
    
    def pop_ent(self):
        try:
            grid_info: dict = self.add_ent.grid_info()
            entity_type = self.entity_type.get()
            ent_list = None
            
            if entity_type == "Robôs":
                ent_list = self.lista_robos
            
            elif entity_type == "Mesas":
                ent_list = self.lista_mesas
                
            elif entity_type == "Esteiras":
                ent_list = self.lista_esteiras
                
            if len(ent_list[0]) == 1:
                return
            
            ent_list[0][-1].destroy()
            ent_list[1][-1].destroy()
            ent_list[0].pop()
            ent_list[1].pop()
            
            self.add_ent.grid_forget()
            self.rm_ent.grid_forget()
            self.add_ent.grid(row=0, column=grid_info.get('column'), padx=3, pady=3, sticky='w')
            self.rm_ent.grid(row=0, column=grid_info.get('column') + 1, padx=3, pady=3, sticky='w')
            
            ent_list[0][-1].invoke()
        
        except Exception as e:
            print(f"Erro na função 'pop_ent': {e}")
            
            
    def load_entity_frame(self, parent: customtkinter.CTkButton=None):
        if parent == self.selected_entity:
            return
        self.selected_entity = parent
        
        self.forget_widgets_self_conteudo()
        self.change_all_entities_fg_color()       
        
        if parent is not None:
            if parent in self.botoes_robo:
                btn_index = self.botoes_robo.index(parent)
                print(f"\nbtn_index:{btn_index}")
                if len(self.lista_robos[1]) > btn_index:
                    print(f"entrou para robo\nlen lista_robos: {len(self.lista_robos[1])}")
                    frame: customtkinter.CTkFrame = self.lista_robos[1][btn_index]
                    frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                else:
                    print("no else para robo\n")
                    n_frame = InputRobo(self.conteudo)
                    self.lista_robos[1].append(n_frame.frame)
                    n_frame.frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                    
            elif parent in self.botoes_mesa:
                btn_index = self.botoes_mesa.index(parent)
                print(f"\nbtn_index:{btn_index}")
                if len(self.lista_mesas[1]) > btn_index:
                    print(f"entrou para mesa\nlen lista_mesas: {len(self.lista_mesas[1])}")
                    frame: customtkinter.CTkFrame = self.lista_mesas[1][btn_index]
                    frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                else:
                    print("no else para mesa\n")
                    n_frame = InputMesa(self.conteudo)
                    self.lista_mesas[1].append(n_frame.frame)
                    n_frame.frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                    
            elif parent in self.botoes_esteira:
                btn_index = self.botoes_esteira.index(parent)
                print(f"\nbtn_index:{btn_index}")
                if len(self.lista_esteiras[1]) > btn_index:
                    print(f"entrou para esteira\nlen lista_esteiras: {len(self.lista_esteiras[1])}")
                    frame: customtkinter.CTkFrame = self.lista_esteiras[1][btn_index]
                    frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                else:
                    print("no else para esteira\n")
                    n_frame = InputConveyor(self.conteudo)
                    self.lista_esteiras[1].append(n_frame.frame)
                    n_frame.frame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky='nsew')
                    
            parent.configure(fg_color="#3B8ED0")
                
                
    def forget_widgets_self_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.grid_forget()
            
            
    def change_all_entities_fg_color(self):
        for i in self.lista_robos[0]:
            i.configure(fg_color="#4A4A4A")
        for i in self.lista_mesas[0]:
            i.configure(fg_color="#4A4A4A")
        for i in self.lista_esteiras[0]:
            i.configure(fg_color="#4A4A4A")