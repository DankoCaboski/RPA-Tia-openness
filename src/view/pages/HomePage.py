import customtkinter

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class HomePage:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.button_handler: ButtonHandler = frame_management.button_handler
        self.home_page()
        
    def home_page(self):            
        label = customtkinter.CTkLabel(self.frame, text="Home page")
        label.grid(row=0, column=0)
        
        comp_create_proj = CustomButton(self.frame, "Criar novo projeto", command=self.call_create_project)  # Create an instance of CustomButton
        comp_create_proj = comp_create_proj.get_button()  # Call the instance to get the button
        comp_create_proj.grid(row=1, column=0, padx=(0, 10), pady=10)
        
        comp_open_proj = CustomButton(self.frame, "Abrir projeto", command=self.call_open_project)  # Create an instance of CustomButton
        comp_open_proj = comp_open_proj.get_button()  # Call the instance to get the button
        comp_open_proj.grid(row=2, column=0, padx=(0, 10), pady=10)
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=3, column=0, padx=(0, 10), pady=10)

    def call_create_project(self):
        self.button_handler.show_create_project_page()
        
    def call_open_project(self):
        self.button_handler.show_open_project_page()