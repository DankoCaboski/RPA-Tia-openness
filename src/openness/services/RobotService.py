from openness.services.UDTService import UDTService
from openness.services.Utils import Utils

import random


class RobotService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
        
        
    def manage_robots(self, robots_associations: list):
        try:
            print("Manage robots: ")
            for robot in robots_associations:
                print(robot)
                self.create_robot_structure(robot["name"], robot["brand"])
        except Exception as e:
            print("Error manage_robots: ", e)


    def create_robot_structure(self, robot_name, robot_brand):
        try:
            op_gp = self.tia_service.recursive_folder_search(None, "03_Blocos Operacionais")
            if not op_gp:
                op_gp = self.tia_service.create_group(None, "03_Blocos Operacionais", None)
                
            rb_gp = self.tia_service.recursive_folder_search(op_gp.Groups, "03.5_Robos")
            if not rb_gp:
                rb_gp = self.tia_service.create_group(None, "03.5_Robos", "03_Blocos Operacionais")
            
            if robot_name == "":
                robot_name = f"rb{str(random.randint(0, 11))}"
                
            group_name = f"{robot_name}_group"
            robot_group = self.tia_service.create_group(None, group_name, "03.5_Robos")
            
            if not robot_group:
                raise Exception("Error creating robot group")
            
            self.import_robot_bk(robot_group, robot_brand)
        except Exception as e:
            print("Error creating robot structure: ", e)


    def import_robot_bk(self, robot_group, robot_robot_brand : str):
        try:
            robot_robot_brand = robot_robot_brand.upper()
            
            generated_block_name = Utils().get_attibutes(["Name"],robot_group)
            print(f'Importing {robot_robot_brand} robot block to {generated_block_name[0]}...')
            bk_path:str = ""
            if robot_robot_brand == 'ABB':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\robots\bk_abb.xml"
            elif robot_robot_brand == 'FANUC':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\robots\bk_fanuc.xml"
                
            udts = UDTService().list_udt_from_bk(bk_path)
                
            for udt in udts:
                udt_path = self.dependencies + '\\' + udt + '.xml'
                device = self.tia_service.get_device_by_index(0)
                self.tia_service.import_data_type(device, udt_path)
                
            self.tia_service.import_block(robot_group.Blocks, bk_path)
                
        except Exception as e:
            print("Error importing robot block: ", e)