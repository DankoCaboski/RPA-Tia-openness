from openness.controllers.OpennessController import OpennessController
class ButtonHandler:
    def __init__(self, frame_management, database):
        self.frame_management = frame_management
        self.openness = OpennessController(database)
        
    def set_tia_version(self, tia_version):
        result = self.openness.set_dll(tia_version)
        return result

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
