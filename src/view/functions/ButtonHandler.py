from openness.controllers.OpennessController import OpennessController
class ButtonHandler:
    def __init__(self, frame_management, database):
        self.frame_management = frame_management
        self.openness: OpennessController = OpennessController(database)
        
    def set_tia_version(self, tia_version):
        result = self.openness.set_dll(tia_version)
        return result

    def show_create_project_page(self):
        self.frame_management.show_create_project_page()
        
    def create_project(
        self,
        proj_name: str,
        proj_path: str,
        tia_version: str,
        hardwware: list,
        blocks_to_import: dict,
        safaty: dict
        ):
        
        status = self.openness.create_project(
            proj_name,
            proj_path,
            tia_version,
            hardwware,
            blocks_to_import,
            safaty
            )
        return status
        
    def open_project(self, project_path):
        return self.openness.open_project(project_path)
        
    def show_home_page(self):
        self.frame_management.show_home_page()
        
    def show_open_project_page(self):
        self.frame_management.show_open_project_page()
        
    def open_tia_ui(self):
        self.openness.open_tia_ui()
        
    def open_tia_without_ui(self):
        raise NotImplementedError("Not implemented yet")
    
    def set_dll(self):
        self.frame_management.set_dll()