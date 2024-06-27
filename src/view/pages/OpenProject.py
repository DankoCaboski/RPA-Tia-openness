from CustomTkinter import customtkinter

from view.components.CustomButton import CustomButton
from view.functions.HomeIcon import HomeIcon


from openness.services.Utils import Utils

from view.functions.ButtonHandler import ButtonHandler

class OpenProject:
    
    def __init__(self,frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.button_handler: ButtonHandler = frame_management.button_handler
    
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_rowconfigure(3, weight=1)  # Row for expansion
        self.frame.grid_rowconfigure(4, weight=0)
        
        self.row_counter = 0
        
        self.create_project_page()
        
    def create_project_page(self):
        
        home_icon = HomeIcon().load_image()
        
        comp_home_page = CustomButton(self.frame, None, home_icon, command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=self.row_counter, column=0, sticky="w", padx=25, pady=25)
        self.row_counter += 1
        
        comp_export_bk = CustomButton(self.frame, "Exportar blocos", None, command=None)
        comp_export_bk = comp_export_bk.get_button()
        comp_export_bk.grid(row=self.row_counter, column=0, columnspan=2, sticky="e", padx=25)
        
        comp_home_udt = CustomButton(self.frame, "Exportar UDT", None, command=None)
        comp_home_udt = comp_home_udt.get_button()
        comp_home_udt.grid(row=self.row_counter, column=2, columnspan=2, sticky="w", padx=25)
        self.row_counter += 1
        
        open_tia = CustomButton(self.frame, "Abrir projeto", None, command=self.open_project)
        open_tia = open_tia.get_button()
        open_tia.grid(row=self.row_counter, column=0, columnspan=4, pady=10)
        self.row_counter += 1
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=self.row_counter+1, column=0, columnspan=4, pady=10, sticky="ew")
        self.row_counter += 1
        
    def call_home_page(self):
        self.button_handler.show_home_page()
        
    def open_tia_ui(self):
        self.button_handler.open_tia_ui()
        
    def open_project(self):
        project_path = Utils().open_file_dialog()
        self.button_handler.open_project(project_path)
    