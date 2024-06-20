import customtkinter
from view.pages.CreateProject import CreateProject
from view.pages.HomePage import HomePage

class FrameManagement:
    def __init__(self, root):
        self.root = root
        self.frame: customtkinter.CTkFrame = None
        self.frame_manegement()
        
    def frame_manegement(self):
        if (self.frame == None):
            self.frame = HomePage(self.root).frame 
            self.frame.pack(anchor="center", fill="both", expand=True)
