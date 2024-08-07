from CustomTkinter import customtkinter


from view.components.CustomButton import CustomButton
from view.components.ProjConfigFrame import ProjConfigFrame

from view.functions.ButtonHandler import ButtonHandler
from view.functions.HomeIcon import HomeIcon

from openness.services.Utils import Utils
class CreateProject:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1)
        
        self.button_handler: ButtonHandler = frame_management.button_handler
        
        self.hw_frame: ProjConfigFrame = ProjConfigFrame(self.frame)
        
        self.hw_frame_index = 2  # Definindo o índice inicial da linha para self.hw_frame.frame
        
        self.frame.grid_rowconfigure(self.hw_frame_index, weight=1)  # Configurando a linha
        
        self.row_counter = 0
        
        
        self.proj_path = ""
        
        self.get_tia_versions()
        
        self.create_project_page()
        
    def create_project_page(self):
        
        home_icon = HomeIcon().load_image()
        
        comp_home_page = CustomButton(self.frame, None, home_icon, command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=self.row_counter, column=0, columnspan=4, sticky="w", padx=25, pady=25)
        
        button_proj_path = CustomButton(self.frame, "Local do Arquivo", None, command=self.set_proj_path)
        button_proj_path = button_proj_path.get_button()
        # button_proj_path.grid(row=self.row_counter, column=0, columnspan=4, pady=25)
        # self.row_counter += 1
        
        proj_name_label = customtkinter.CTkLabel(self.frame, text="Nome do projeto:")
        proj_name_label.grid(row=self.row_counter, column=1, sticky="e", padx=(0, 10), pady=(0, 10))
             
        global proj_name
        proj_name = customtkinter.CTkEntry(self.frame)
        proj_name.grid(row=self.row_counter, column=2, sticky="w", padx=(10, 0), pady=(0, 10))
        self.row_counter += 1
        
        label_tia = customtkinter.CTkLabel(self.frame, text="Versão do TIA:")
        label_tia.grid(row=self.row_counter, column=1, sticky="e", padx=(0, 10), pady=0)
        
        global tia_version
        tia_version = customtkinter.CTkComboBox(self.frame, values=versions)
        tia_version.grid(row=self.row_counter, column=2, sticky="w", padx=(10, 0), pady=0)
        self.row_counter += 1
        
        self.hw_frame.tabview.grid(row=self.hw_frame_index, column=0, columnspan=4, padx=25, pady=0, sticky='nsew')
        self.row_counter += 1
        
        btn_criar = CustomButton(self.frame, "Gerar Projeto", None, command=self.call_create_proj)
        btn_criar = btn_criar.get_button()
        btn_criar.grid(row=self.row_counter, column=0, columnspan=4, padx=10, pady=5)
        self.row_counter += 1
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=self.row_counter, column=0, columnspan=4, sticky="nsew")
        
    def call_home_page(self):
        self.button_handler.show_home_page()
        
    def call_create_proj(self):
        if self.proj_path == '' or self.proj_path is None:
            self.set_proj_path()
            if self.proj_path == '' or self.proj_path is None:
                self.status_label.configure(text="Status: Defina um local para salvar o projeto")
                return
        if proj_name.get() == '' or proj_name.get() is None:
            self.status_label.configure(text="Status: Defina um nome para o projeto")
            return
        self.status_label.configure(text=f"Status: Criando projeto...")
        self.status_label.update_idletasks() 
        
        hardware = self.hw_frame.get_hardware_values()
        blocks: dict = self.hw_frame.get_zonas()
        safaty: dict = self.hw_frame.get_safety_config()
        
        
        status = self.button_handler.create_project(
            proj_name.get(),
            self.proj_path,
            tia_version.get(),
            hardware,
            blocks,
            safaty
            )
        
        self.status_label.configure(text="Status: " + str(status))
        
    def set_proj_path(self):
        self.proj_path = Utils().open_directory_dialog()
        
    def get_tia_versions(self):
        global versions
        versions = Utils().get_tia_versions()
        
    def call_set_tia(self):
        self.status = self.button_handler.set_tia_version(tia_version.get())
        self.status_label.configure(text="Status: " + str(self.status))            
