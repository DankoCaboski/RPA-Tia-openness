class ConveyorService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        
    def manage_conveyor(self, conveyor_association):
        print("Tipo conveyor: ", type(conveyor_association))
        pass