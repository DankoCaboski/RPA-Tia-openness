import customtkinter

from view.components.CustomButton import CustomButton
from view.functions.HomeIcon import HomeIcon


from openness.services.Utils import Utils

from view.functions.ButtonHandler import ButtonHandler

class OpenProject:
    
    def __init__(self,frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.button_handler: ButtonHandler = frame_management.button_handler
        
        self.row_counter = 0
        
        self.create_project_page()
        
    def create_project_page(self):
        
        home_icon = HomeIcon().load_image()
        
        comp_home_page = CustomButton(self.frame, None, home_icon, command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=self.row_counter, column=0, sticky="w", padx=25, pady=25)
        self.row_counter += 1
        
        open_tia = CustomButton(self.frame, "Abrir projeto", None, command=self.open_project)
        open_tia = open_tia.get_button()
        open_tia.grid(row=self.row_counter, column=0, pady=10)
        self.row_counter += 1
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=self.row_counter, column=0, pady=10)
        self.row_counter += 1
        
    def call_home_page(self):
        self.button_handler.show_home_page()
        
    def open_tia_ui(self):
        self.button_handler.open_tia_ui()
        
    def open_project(self):
        project_path = Utils().open_file_dialog()
        self.button_handler.open_project(project_path)
    