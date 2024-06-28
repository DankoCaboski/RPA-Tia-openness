from openness.services.UDTService import UDTService



class RobotService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
        
        
    def manege_robot(self, robots_association: dict):
        try:
            brands = list(robots_association.keys())
            for robot_brand in brands:
                qtd = robots_association.get(robot_brand)
                if qtd is None or str(qtd) == '':
                    continue
                if int(qtd) > 1:
                    print("qtd > 1")
                    for i in range(robot_brand[1]):
                        self.create_robot_structure(robot_brand[0] + "_" + str(i), robot_brand)
                else:
                    self.create_robot_structure(robot_brand[0], robot_brand)
        except Exception as e:
            print("Error manege_robot: ", e)


    def create_robot_structure(self, robot_name, robot_brand):
        op_exist = self.tia_service.recursive_folder_search(None, "03_Blocos Operacionais")
        if not op_exist:
            self.tia_service.create_group(None, "03_Blocos Operacionais", None)
            
        group_name = robot_name + '_group'
        robot_group = self.tia_service.create_group(None, group_name, "03_Blocos Operacionais")
        self.import_robot_bk(robot_group, robot_brand)


    def import_robot_bk(self, robot_group, robot_robot_brand : str):
        try:
            robot_robot_brand = robot_robot_brand.upper()
            
            print(f'Importing {robot_robot_brand} robot block')
            if robot_robot_brand == 'ABB':
                abb_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\robots\bk_abb.xml"
                udts = UDTService().list_udt_from_bk(abb_bk_path)
                
                for udt in udts:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(0)
                    self.tia_service.import_data_type(device, udt_path)
                    
                self.tia_service.import_block(robot_group, abb_bk_path)
                
            elif robot_robot_brand == 'FANUC':
                self.tia_service.import_block(robot_group, 123, r"C:\Users\Willian\Desktop\exported_bk\bk_fanuc.xml")
        except Exception as e:
            print("Error importing robot block: ", e)