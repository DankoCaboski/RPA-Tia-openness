from src.openness.services.OponessService import OpennessService
class OpennessController:
    def __init__(self):
        self.openness_service = OpennessService()
        self.tia = None
        self.hwf = None
        self.comp = None