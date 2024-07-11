class OperationalService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.op_gp = None
        self.rb_gp = None
    
    def create_operational_structure(self):
        try:
            
            if self.op_gp is None:
                op_gp = self.tia_service.recursive_group_search(None, "03_Blocos Operacionais")
                if not op_gp:
                    self.op_gp = self.tia_service.create_group(None, "03_Blocos Operacionais", None)
                    print(self.op_gp)
                    
        except Exception as e:
            print("Error creating operational structure: ", e)
            
    def create_robot_structure(self):
        try:
            self.create_operational_structure()
            
            if self.rb_gp is None:
                rb_gp = self.tia_service.recursive_group_search(None, "03.4_Robos")
                if not rb_gp:
                    self.rb_gp = self.tia_service.create_group(None, "03.4_Robos", "03_Blocos Operacionais")
                    print(self.rb_gp)
                    
        except Exception as e:
            print("Error creating operational structure: ", e)