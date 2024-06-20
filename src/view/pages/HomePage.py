import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class HomePage:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.button_handler = ButtonHandler(frame_management)
        self.home_page()
        
    def home_page(self):            
        label = customtkinter.CTkLabel(self.frame, text="Home page")
        label.grid(row=0, column=0)
        
        comp_create_proj = CustomButton(self.frame, "Criar novo projeto", command=self.call_create_project)  # Create an instance of CustomButton
        button_create_proj = comp_create_proj()  # Call the instance to create the button
        button_create_proj.grid(row=1, column=0)

    def call_create_project(self):
        self.button_handler.create_project()