from openness.services.XmlService import XmlService
from openness.services.UDTService import UDTService

from openness.services.Utils import Utils


class RobotService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"
        
        
    def manage_robots(self, robots_associations: list, rbz_name: str):
        try:
            print("\n", robots_associations)
            for i in enumerate(robots_associations):
                print(f"Manage robots: i == {i}")
                robot_group = self.create_robot_structure(i[0], rbz_name)
                self.import_robot_bk(robot_group, "ABB")
                
        except Exception as e:
            print("Error manage_robots: ", e)


    def create_robot_structure(self, i: int, rbz_name: str):
        try:            
            group_name = f"03.4.{i+1}_RB{i+1}"
            robot_group = self.tia_service.create_group(None, group_name, rbz_name)
            
            if not robot_group:
                raise Exception("Error creating robot group")
            
            return robot_group
            
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
                
            bk_file_info = Utils().get_file_info(bk_path)
            aux = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls"
            temp_path = f"{aux}\\{Utils().generate_entropy_string()}.xml"
            bk_file_info.CopyTo(temp_path)
            
            random_number = Utils().get_random_number()
            XmlService().editar_tags_xml(temp_path, f"ABB{Utils().generate_entropy_string()}", random_number)
            
            self.tia_service.import_block(robot_group.Blocks, temp_path)
                
            Utils().get_file_info(temp_path).Delete()   
                
        except Exception as e:
            print("Error importing robot block: ", e)