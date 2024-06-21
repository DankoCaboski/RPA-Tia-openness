from src.openness.services.OponessService import OpennessService
class OpennessController:
    def __init__(self):
        self.openness_service = OpennessService()
        
    def set_dll(self, dll):
        return self.openness_service.set_dll(dll)
