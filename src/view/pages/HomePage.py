import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class HomePage:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.button_handler = frame_management.button_handler
        self.home_page()
        
    def home_page(self):            
        label = customtkinter.CTkLabel(self.frame, text="Home page")
        label.grid(row=0, column=0)
        
        comp_create_proj = CustomButton(self.frame, "Criar novo projeto", command=self.call_create_project)  # Create an instance of CustomButton
        comp_create_proj = comp_create_proj.get_button()  # Call the instance to get the button
        comp_create_proj.grid(row=1, column=0)
        
        comp_open_proj = CustomButton(self.frame, "Abrir projeto", command=self.call_create_project)  # Create an instance of CustomButton
        comp_open_proj = comp_open_proj.get_button()  # Call the instance to get the button
        comp_open_proj.grid(row=2, column=0)

    def call_create_project(self):
        self.button_handler.create_project()
        
    def call_open_project(self):
        self.button_handler.open_project()