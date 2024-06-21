from typing import Any

class TiaService:
    def __init__(self, tia : Any):
        self.tia = tia
        
    def open_tia_ui(self):
        # Create an instance of Tia Portal
        return self.tia.TiaPortal(self.tia.TiaPortalMode.WithUserInterface)