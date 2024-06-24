import customtkinter
import tkinter as tk
from view.pages.CreateProject import CreateProject
from view.pages.OpenProject import OpenProject
from view.pages.HomePage import HomePage
from view.functions.ButtonHandler import ButtonHandler

class FrameManagement:
    def __init__(self, root, database):
        self.root = root
        self.current_frame = None
        
        self.database = database
        
        self.button_handler = ButtonHandler(self, database)
        self.show_home_page()
        
    def show_home_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = HomePage(self).frame
        self.current_frame.grid(row=0, column=0)

    def show_create_project_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = CreateProject(self).frame
        self.current_frame.grid(row=0, column=0)
        
    def show_open_project_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = OpenProject(self).frame
        self.current_frame.grid(row=0, column=0)
