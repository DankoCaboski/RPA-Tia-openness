from openness.services.OperationalService import OperationalService
from openness.services.UDTService import UDTService

from openness.services.Utils import Utils


class RobotService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
        
        
    def manage_robots(self, robots_associations: list):
        try:
            print("\n", robots_associations)
            print("Manage robots: ")
            for robot in robots_associations:
                print(robot)
                self.create_robot_structure(robots_associations.index(robot))
        except Exception as e:
            print("Error manage_robots: ", e)


    def create_robot_structure(self, i):
        try:
            operational_service = OperationalService(self.tia_service)
            operational_service.create_robot_structure()
            
            group_name = f"03.4.{i+1}_RB{i+1}"
            robot_group = self.tia_service.create_group(None, group_name, "03.4_Robos")
            
            if not robot_group:
                raise Exception("Error creating robot group")
            
        except Exception as e:
            print("Error creating robot structure: ", e)


    def import_robot_bk(self, robot_group, robot_robot_brand : str):
        try:
            robot_robot_brand = robot_robot_brand.upper()
            
            generated_block_name = Utils().get_attributes(["Name"],robot_group)
            print(f'Importing {robot_robot_brand} robot block to {generated_block_name[0]}...')
            bk_path:str = ""
            if robot_robot_brand == 'ABB':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.4_Robos\3.4.1_RB01\34101_RB01.xml"
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