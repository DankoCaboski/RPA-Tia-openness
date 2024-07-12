class MesaService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        
    def manage_turntables(self, mesa_association: list):
        try:
            print("\n", mesa_association)
            for i in enumerate(mesa_association):
                print(f"Manage robots: i == {i}")
                self.create_turntable_structure(i[0])
        except Exception as e:
            print("Error manage_robots: ", e)


    def create_turntable_structure(self, i):
        try:            
            group_name = f"03.4.{i+1}_RB{i+1}"
            robot_group = self.tia_service.create_group(None, group_name, "03.4_Robos")
            
            if not robot_group:
                raise Exception("Error creating robot group")
            
        except Exception as e:
            print("Error creating robot structure: ", e)