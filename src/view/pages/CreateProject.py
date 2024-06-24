import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class CreateProject:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1)
        self.button_handler = frame_management.button_handler
        self.create_project_page()
        
    def create_project_page(self):
        label = customtkinter.CTkLabel(self.frame, text="Create Project")
        label.grid(row=0, column=0, columnspan=4, padx=10)
        
        comp_home_page = CustomButton(self.frame, "Homepage", command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=1, column=0, columnspan=4, pady=10)
        
        button_set_tia_version = CustomButton(self.frame, "set_tia_version", command=self.set_tia_version)
        set_tia_version_button = button_set_tia_version.get_button()
        set_tia_version_button.grid(row=2, column=1, sticky="e", padx=(0, 10), pady=10)  # Alinhar à direita da coluna 1 com padding à direita
        
        global tia_version
        tia_version = customtkinter.CTkEntry(self.frame)
        tia_version.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=10)  # Alinhar à esquerda da coluna 2 com padding à esquerda
        
        comp_criar = CustomButton(self.frame, "Abrir tia", command=self.open_tia_ui)
        comp_criar = comp_criar.get_button()
        comp_criar.grid(row=3, column=0, columnspan=4)
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=4, column=0, columnspan=4, padx=10)
        
    def call_home_page(self):
        self.button_handler.home_page()
        
    def open_tia_ui(self):
        self.button_handler.open_tia_ui()
        
    def set_tia_version(self):
        self.status = self.button_handler.set_tia_version(tia_version.get())
        self.status_label.configure(text="Status: " + str(self.status))

