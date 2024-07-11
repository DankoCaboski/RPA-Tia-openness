class MesaService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        
    def manage_turntables(self, mesa_association):
        print("Tipo mesa: ", type(mesa_association))
        pass