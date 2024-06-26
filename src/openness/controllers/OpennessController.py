from openness.services.OponessService import OpennessService
class OpennessController:
    def __init__(self, database):
        self.database = database
        
        self.openness_service: OpennessService = OpennessService(self.database)
        self.curent_tia_version = None
        
        
    def set_dll(self, dll: str):
        dll = ''.join(filter(str.isdigit, dll))
        result = self.openness_service.set_dll(dll)
        return result

    def open_tia_ui(self):
        self.openness_service.tia.open_tia_ui()
        
    def create_project(self, proj_name, proj_path, tia_version: str, hardwware: list, blocks_to_import: dict):
        if self.curent_tia_version is None:
            self.openness_service.set_dll(tia_version)
        self.openness_service.tia.create_project(proj_name, proj_path)
        self.openness_service.tia.add_hardware(hardwware)
        self.openness_service.tia.wire_profinet()
        self.openness_service.tia.save_project()


    def open_project(self, project_path):
        if self.curent_tia_version is None:
            extension = project_path.split(".")[-1]
            print(extension)
            self.set_dll(extension)
        self.openness_service.tia.open_project(project_path)