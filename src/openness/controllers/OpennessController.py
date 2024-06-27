from openness.services.OponessService import OpennessService
from openness.services.Utils import Utils

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
        
    def create_project(
        self,
        proj_name: str,
        proj_path: str,
        tia_version: str,
        hardwware: list,
        blocks_to_import: dict
        ):
        
        try:
            if self.curent_tia_version is None:
                self.openness_service.set_dll(tia_version)
            error_creating = self.openness_service.tia.create_project(proj_name, proj_path)
            if error_creating:
                raise Exception(error_creating)
            self.openness_service.tia.add_hardware(hardwware)
            self.openness_service.tia.wire_profinet()
            self.openness_service.tia.import_blocks(blocks_to_import)
            self.openness_service.tia.save_project()
            return "Projeto criado com sucesso!"
        except Exception as e:
            return "Erro ao gerar projeto: " + str(e)


    def open_project(self, project_path):
        if self.curent_tia_version is None:
            extension = project_path.split(".")[-1]
            self.set_dll(extension)
        my_proj = self.openness_service.tia.open_project(project_path)
        proj_name = Utils().get_attibutes(["Name"], my_proj)
        return proj_name[0]