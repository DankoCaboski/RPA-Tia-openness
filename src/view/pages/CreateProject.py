import customtkinter

class CreateProject:
    
    def __init__(self,parent):
        self.parent = parent
        self.frame = customtkinter.CTkFrame(self.parent)
        self.create_project()
        
    def create_project(self):
        label = customtkinter.CTkLabel(self.frame, text="Create Project")
        label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        return self.frame
    