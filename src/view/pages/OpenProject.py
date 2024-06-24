import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class OpenProject:
    
    def __init__(self,frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.button_handler: ButtonHandler = frame_management.button_handler
        self.create_project_page()
        
    def create_project_page(self):
        label = customtkinter.CTkLabel(self.frame, text="Open Project")
        label.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        comp_home_page = CustomButton(self.frame, "Homepage", command=self.call_home_page)
        comp_home_page = comp_home_page.get_button()
        comp_home_page.grid(row=1, column=0)
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=2, column=0, padx=(0, 10), pady=10)
        
    def call_home_page(self):
        self.button_handler.home_page()
    