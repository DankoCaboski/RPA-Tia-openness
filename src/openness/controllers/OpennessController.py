from openness.services.OponessService import OpennessService
class OpennessController:
    def __init__(self, database):
        self.database = database
        
        self.openness_service = OpennessService(self.database)
        self.curent_tia_version = None
        
        
    def set_dll(self, dll):
        self.openness_service.set_dll(dll)

    def open_tia_ui(self):
        self.openness_service.tia.open_tia_ui()