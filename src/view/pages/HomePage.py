from CustomTkinter import customtkinter

from view.functions.WaterMark import WaterMark

from view.components.CustomButton import CustomButton

from view.functions.ButtonHandler import ButtonHandler

class HomePage:
    
    def __init__(self, frame_management):
        self.frame = customtkinter.CTkFrame(frame_management.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.button_handler: ButtonHandler = frame_management.button_handler
        
        self.row_counter = 0  # Contador de linhas para posicionar elementos na grade
        
        self.home_page()
        
    def home_page(self):            
        label = customtkinter.CTkLabel(self.frame, text="Home page")
        # label.grid(row=self.row_counter, column=0)
        self.row_counter += 1
        
        
        comp_open_proj = CustomButton(self.frame, "Abrir projeto", None,  command=self.call_open_project)  # Create an instance of CustomButton
        comp_open_proj = comp_open_proj.get_button()  # Call the instance to get the button
        # comp_open_proj.grid(row=self.row_counter, column=0, pady=10)
        self.row_counter += 1
        
        water_mark = WaterMark().load_image()
        
        water_mark_lb = customtkinter.CTkLabel(self.frame, text="", image=water_mark)
        water_mark_lb.grid(row=self.row_counter, column=0, columnspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(self.row_counter, weight=1)
        self.row_counter += 1
              
        comp_create_proj = CustomButton(self.frame, "Novo projeto", None, command=self.call_create_project)  # Create an instance of CustomButton
        comp_create_proj = comp_create_proj.get_button()  # Call the instance to get the button
        comp_create_proj.grid(row=self.row_counter, column=0, pady=10)
        self.row_counter += 1
        
        self.status_label = customtkinter.CTkLabel(self.frame, text="Status: Idle")
        self.status_label.grid(row=self.row_counter, column=0, columnspan=4, sticky="nsew")
        self.row_counter += 1

    def call_create_project(self):
        self.button_handler.show_create_project_page()
        
    def call_open_project(self):
        self.button_handler.show_open_project_page()