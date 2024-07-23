# Essa classe está focada em fazer o import dos blocos do robo,
# toda criação de pasta e subpastas do robo são feitas aqui

from openness.services.XmlService import XmlService
from openness.services.UDTService import UDTService

from openness.services.Utils import Utils


class RobotService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types"
        self.db_rb = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.4_Robos\3.4.1_RB01\34171_RB01.xml"
        
        
    def manage_robots(self, robots_associations: list, rbz_name: str):
        try:
            for i in enumerate(robots_associations):
                print(f"Manage robots: i == {i}")
                robot_group = self.create_robot_structure(i[0], rbz_name)
                self.import_robot_structure(robot_group, "ABB")
                
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


    def import_robot_structure(self, robot_group, robot_robot_brand : str):
        try:
            robot_robot_brand = robot_robot_brand.upper()
            
            generated_block_name = Utils().get_attributes(["Name"],robot_group)
            print(f'\nImporting {robot_robot_brand} robot block to {generated_block_name[0]}...')
            bk_path:str = ""
            if robot_robot_brand == 'ABB':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.4_Robos\3.4.1_RB01\34101_RB01.xml"
                
            elif robot_robot_brand == 'FANUC':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\03_Blocos Operacionais\robots\bk_fanuc.xml"
            
            self.import_rb_bk(robot_group, bk_path)
            self.import_rb_db(robot_group)
                
        except Exception as e:
            print("Error no estrutura do robô: ", e)
            
    def import_rb_bk(self, robot_group, bk_path):
        try:
            udts = UDTService().list_udt_from_bk(bk_path)
            if len(udts) >= 1:    
                device = self.tia_service.get_device_by_index(1)
                for udt in udts:
                    print("\nImportando dependencias da FC de robô...")
                    print(f"Importing UDT {udt}...")
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    imported = self.tia_service.import_data_type(device, udt_path)
                    if not imported:
                        raise Exception(f"Error importing UDT {udt}")
                    print(f"UDT {udt} imported")
                
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
        
    def import_rb_db(self, robot_group):
        udts = UDTService().list_udt_from_db(self.db_rb)
        if len(udts) >= 1:    
            device = self.tia_service.get_device_by_index(1)
            for udt_d in udts:
                udt_path: str = None
                print(f"\nImportando dependencias da DB de robô...")
                print(f"Importing UDT {udt_d}...")
                udt_path = f"{self.dependencies}\\{udt_d}.xml"
                if udt_path == r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types\06_Axis.RB.Memórias.xml":
                    self.tia_service.import_data_type(device, f"{self.dependencies}\\08_Axis.RB.MemóriasInternas.xml")
                    self.tia_service.import_data_type(device, f"{self.dependencies}\\07_Axis.RB.MemóriasExternas.xml")
                imported = self.tia_service.import_data_type(device, udt_path)
                if not imported:
                    raise Exception(f"Error importing UDT {udt_d}")
                print(f"UDT {udt_d} imported")
                
        self.tia_service.import_block(robot_group.Blocks, self.db_rb)