class OperationalService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
    
    def create_operational_structure(self):
        try:
            op_gp = self.tia_service.recursive_group_search(None, "03_Blocos Operacionais")
            if not op_gp:
                op_gp = self.tia_service.create_group(None, "03_Blocos Operacionais", None)
        except Exception as e:
            print("Error creating operational structure: ", e)
            
    def create_robot_structure(self):
        try:
            op_gp = self.tia_service.recursive_group_search(None, "03_Blocos Operacionais")
            if not op_gp:
                self.create_operational_structure()
                
            rb_gp = self.tia_service.recursive_group_search(op_gp.Groups, "03.4_Robos")
            if not rb_gp:
                rb_gp = self.tia_service.create_group(None, "03.4_Robos", "03_Blocos Operacionais")
        except Exception as e:
            print("Error creating operational structure: ", e)