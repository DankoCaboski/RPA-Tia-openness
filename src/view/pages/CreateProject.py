import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

from openness.services.Utils import Utils

class CreateProject:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1)
        
        self.button_handler: ButtonHandler = frame_management.button_handler
        
        self.row_counter = 0
        
        self.create_project_page()
        
    def create_project_page(self):
        label = customtkinter.CTkLabel(self.frame, text="Create Project")
        label.grid(row=self.row_counter, column=0, columnspan=4, padx=10)
        self.row_counter += 1
        
        comp_home_page = CustomButton(self.frame, "Homepage", command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=self.row_counter, column=0, columnspan=4, pady=10)
        self.row_counter += 1
        
        button_proj_path = CustomButton(self.frame, "Project Path",  command=self.set_proj_path)
        button_proj_path = button_proj_path.get_button()
        button_proj_path.grid(row=self.row_counter, column=0, columnspan=4, padx=(0, 10), pady=10)
        self.row_counter += 1
        
        proj_name_label = customtkinter.CTkLabel(self.frame, text="Nome do projeto:")
        proj_name_label.grid(row=self.row_counter, column=1, sticky="e", padx=(0, 10), pady=10)
             
        global proj_name
        proj_name = customtkinter.CTkEntry(self.frame)
        proj_name.grid(row=self.row_counter, column=2, sticky="w", padx=(10, 0), pady=10)
        self.row_counter += 1
        
        button_set_tia_version = CustomButton(self.frame, "set_tia_version", command=self.call_set_tia)
        set_tia_version_button = button_set_tia_version.get_button()
        set_tia_version_button.grid(row=self.row_counter, column=1, sticky="e", padx=(0, 10), pady=10)  # Alinhar à direita da coluna 1 com padding à direita
        
        global tia_version
        tia_version = customtkinter.CTkEntry(self.frame)
        tia_version.grid(row=self.row_counter, column=2, sticky="w", padx=(10, 0), pady=10)  # Alinhar à esquerda da coluna 2 com padding à esquerda
        self.row_counter += 1
        
        comp_criar = CustomButton(self.frame, "Criar projeto", command=self.call_create_proj)
        comp_criar = comp_criar.get_button()
        comp_criar.grid(row=self.row_counter, column=0, columnspan=4, padx=(0, 10), pady=10)
        self.row_counter += 1
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=self.row_counter, column=0, columnspan=4, padx=10)
        
    def call_home_page(self):
        self.button_handler.show_home_page()
        
    def call_create_proj(self):
        self.button_handler.create_project(proj_name.get(), proj_path, tia_version)
        
    def set_proj_path(self):
        global proj_path
        proj_path = Utils().open_directory_dialog()
        
    def call_set_tia(self):
        self.status = self.button_handler.set_tia_version(tia_version.get())
        self.status_label.configure(text="Status: " + str(self.status)) 

