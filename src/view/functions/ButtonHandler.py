from openness.controllers.OpennessController import OpennessController
class ButtonHandler:
    def __init__(self, frame_management):
        self.frame_management = frame_management
        self.openness = OpennessController()

    def create_project(self):
        self.frame_management.show_create_project_page()
        
    def home_page(self):
        self.frame_management.show_home_page()
        
    def open_project(self):
        self.frame_management.show_open_project_page()
        
    def open_tia_ui(self):
        self.openness.open_tia_ui()
        
    def open_tia_without_ui(self):
        raise NotImplementedError("Not implemented yet")
    
    def set_dll(self):
        self.frame_management.set_dll()
