import customtkinter
from view.pages.CreateProject import CreateProject

class FrameManagement:
    def __init__(self, root):
        self.root = root
        self.frame: customtkinter.CTkFrame = None
        self.frame_manegement()
        
    def frame_manegement(self):
        if (self.frame == None):
            self.frame = CreateProject(self.root).frame 
            self.frame.pack()
            
            