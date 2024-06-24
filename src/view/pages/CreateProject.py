import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class CreateProject:
    
    def __init__(self,frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.button_handler: ButtonHandler = frame_management.button_handler
        self.create_project_page()
        
    def create_project_page(self):
        label = customtkinter.CTkLabel(self.frame, text="Create Project")
        label.grid(row=0, column=0, padx=10)
        
        comp_home_page = CustomButton(self.frame, "Homepage", command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=1, column=0)
        
        set_tia_version = CustomButton(self.frame, "set_tia_version", command=self.set_tia_version)
        set_tia_version = set_tia_version.get_button()
        set_tia_version.grid(row=2, column=0)
        
        global tia_version
        tia_version = customtkinter.CTkEntry(self.frame)
        tia_version.grid(row=2, column=1, padx=10)
        
        comp_criar = CustomButton(self.frame, "Abrir tia", command=self.open_tia_ui)
        comp_criar = comp_criar.get_button()
        comp_criar.grid(row=3, column=0)
        
        
    def call_home_page(self):
        self.button_handler.home_page()
        
    def open_tia_ui(self):
        self.button_handler.open_tia_ui()
        
        
    def set_tia_version(self):
        self.button_handler.set_tia_version(tia_version.get())
    