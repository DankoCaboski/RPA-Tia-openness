import os
import time
from openness.services.Utils import Utils
from openness.services.UDTService import UDTService
class MesaService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types"
        
        
    def manage_turntables(self, turntables_associations: list):
        try:
            print("\n", turntables_associations)
            print("Manage turntables: ")
            for turntable in turntables_associations:
                driver = turntable['driver']
                self.turntable_group = self.create_turntables_structure(turntables_associations.index(turntable))
                opera_grupo = self.tia_service.recursive_group_search(None, '02_Blocos Standard Axis')
                prodiag = self.tia_service.recursive_group_search(None, '01.3_Prodiag')
                self.import_mg_std(opera_grupo, driver, prodiag)    
                time.sleep(60)
                # Process each side (ladoA, ladoB, ladoC, ladoD)
                for side, products in turntable.items():
                    if 'lado' in side:  # Filter out non-side keys like 'driver'
                        print(f"Processing {side} for driver {driver}")
                        # Process each product in the side
                        self.import_mg(self.turntable_group[0], side)
                        for product_name, details in products.items():
                            cl_value = details['Cl']
                            pp_value = details['PP']
                            # Implement conditional logic based on 'Cl' and 'PP' values
                            if cl_value and pp_value:
                                print(f"{product_name} on {side} has 'Cl' = {cl_value} and 'PP' = {pp_value}.")
                                self.import_mg_mesa(self.turntable_group[1],side )
                                self.import_mg_prod(side, product_name)
                            else:
                                print(f"{product_name} on {side} is missing 'Cl' or 'PP' values.")
                        
                        
        except Exception as e:
            print("Error manage_turntables: ", e)

    def create_turntables_structure(self, i):
        try:           
            group_name = f"3.1.{i+1}_MG0{i+1}"
            grupo_mesa_name = "z1_Mesas Giratórias"
            turntable_group = self.tia_service.create_group(None, group_name, grupo_mesa_name)
            grupo_mesa = self.tia_service.recursive_group_search(None, grupo_mesa_name)
            path_ob = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\Main_Mesas.xml"
            self.tia_service.import_block(grupo_mesa.Blocks, path_ob)
            
            group_name_mesa = f"3.1.{i+1}.1_Mesa MG0{i+1}"
            turntable_group_mesa = self.tia_service.create_group(None, group_name_mesa, group_name)

            if not turntable_group:
                raise Exception("Error creating mesa group")
            return turntable_group, turntable_group_mesa
        except Exception as e:
            print("Error creating mesa structure: ", e)

    #Import do bloco padrão da mesa no standard 
    def import_mg_std(self, opera_grupo, turntable_turntable_brand, prodiag):
        try:         
            if turntable_turntable_brand == 'Sinamics':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2015_FB Mesa Giratoria Sinamics Siemens.xml"
                udts = UDTService().list_udt_from_bk(bk_path)
                udtss = UDTService().list_udt_from_bk_data(bk_path)
                for udt in udts:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)
                for udt in udtss:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)

            elif turntable_turntable_brand == 'SEW':
                bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2016_FB Mesa Giratoria Movidrive Sew.xml"
                udts = UDTService().list_udt_from_bk(bk_path)
                udtss = UDTService().list_udt_from_bk_data(bk_path)
                for udt in udts:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)
                for udt in udtss:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)

            #IMPORT SEPARADO DE UDT 
            device = self.tia_service.get_device_by_index(1)
            IHMBypass = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types\02_Axis.Vlv.IHM.Status&Bypass.xml"
            self.tia_service.import_data_type(device, IHMBypass)

            # Lista de caminhos dos arquivos
            file_paths = [
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2006_FB Válvulas.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2008_FB Presença de Peça.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2014_FC Conversion_XY.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2011_FC SEW Movidrive Modulo Positioning.xml"
            ]
            
            # Iterar sobre cada caminho de arquivo
            for bk_files_path in file_paths:
                udts = UDTService().list_udt_from_bk(bk_files_path)
                udtss = UDTService().list_udt_from_bk_data(bk_files_path)
                for udt in udts:
                    print("UDT FILES", udt)
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)
                for udt in udtss:
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)

            self.tia_service.import_block(opera_grupo.Blocks, bk_path)
            self.tia_service.import_block(opera_grupo.Blocks, file_paths[0])
            self.tia_service.import_block(opera_grupo.Blocks, file_paths[1])
            self.tia_service.import_block(opera_grupo.Blocks, file_paths[2])
            self.tia_service.import_block(opera_grupo.Blocks, file_paths[3])
            # self.tia_service.import_block(prodiag.Blocks, PP_path)
            
                
        except Exception as e:
            print("Error importing standard mesa block: ", e)

    #import do mesa MG
    def import_mg(self, turntable_mesa, turntable_brand):
        try:   
            if turntable_brand == 'ladoA':
                generated_block_name = Utils().get_attributes(["Name"],turntable_mesa)
                print(f'Importing {turntable_brand} mesa block to {generated_block_name[0]}...')
                group_name = '3.1.1.1_Mesa MG01'
                turntable_mesa = self.tia_service.recursive_group_search(None, group_name)
                directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.1_Mesa MG01"
                
                # Lista todos os arquivos que terminam com '.xml' no diretório especificado
                arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
                for arquivo in arquivos_xml:
                    print('Arquivo', arquivo)
                    # Constrói o caminho completo para cada arquivo .xml
                    full_path = os.path.join(directory_path, arquivo)
                    udts = UDTService().list_udt_from_bk(full_path)
                    udtss = UDTService().list_udt_from_bk_data(full_path)
                    for udt in udts:
                        print("UDT FILES", udt)
                        udt_path = self.dependencies + '\\' + udt + '.xml'
                        device = self.tia_service.get_device_by_index(1)
                        self.tia_service.import_data_type(device, udt_path)
                    for udt in udtss:
                        print("UDT FILES", udt)
                        udt_path = self.dependencies + '\\' + udt + '.xml'
                        device = self.tia_service.get_device_by_index(1)
                        self.tia_service.import_data_type(device, udt_path)

                        
                    self.tia_service.import_block(turntable_mesa.Blocks, full_path)
                
        except Exception as e:
            print("Error importing mesa block: ", e)

    #Import dispositivo lado
    def import_mg_mesa(self,opera_group,  turntable_brand):
        try:
            bk_path:str = ""
            if turntable_brand == 'ladoA':
                generated_block_name = Utils().get_attributes(["Name"],opera_group)
                print(f'Importing {turntable_brand} dispositivo block to {generated_block_name[0]}...')
                group_name = '3.1.1.2_Dispositivo Lado A'
                group_exist = self.tia_service.recursive_group_search(None, group_name)
                if group_exist is None:
                    self.tia_service.create_group(None, group_name, "3.1.1.1_Mesa MG01")
                    group_exist = self.tia_service.recursive_group_search(None, group_name)
                directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.2_Dispositivo Lado A"
            elif turntable_brand == 'ladoB':
                group_name = '3.1.1.3_Dispositivo Lado B'
                group_exist = self.tia_service.recursive_group_search(None, group_name)
                if group_exist is None:
                    self.tia_service.create_group(None, group_name, "3.1.1.1_Mesa MG01")
                    group_exist = self.tia_service.recursive_group_search(None, group_name)
                directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.3_Dispositivo Lado B"

            # Lista todos os arquivos que terminam com '.xml' no diretório especificado
            arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
            for arquivo in arquivos_xml:
                # Constrói o caminho completo para cada arquivo .xml
                full_path = os.path.join(directory_path, arquivo)
                udts = UDTService().list_udt_from_bk(full_path)
                udtss = UDTService().list_udt_from_bk_data(full_path)
                for udt in udts:
                    print("UDT FILES", udt)
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)
                for udt in udtss:
                    print("UDT FILES", udt)
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)

                # Obtém as informações do arquivo através do caminho completo
                self.tia_service.import_block(group_exist.Blocks, full_path)
                
        except Exception as e:
            print("Error importing dispositivo mesa block: ", e)

    #Import produto lado
    def import_mg_prod(self, turntable_prod , produto):
        try:       
            bk_path:str = ""
            if turntable_prod == 'ladoA':
                print("Produto name", produto)
                if produto == 'Produto 1':
                    group_name = '3.1.1.2_Produto 1'
                    self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado A")
                    prod_group =self.tia_service.recursive_group_search(None, group_name)
                    directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.2_Dispositivo Lado A\3.1.1.2_Produto 1"
            elif turntable_prod == 'ladoB':
                 if produto == 'Produto 1':
                    group_name = '3.1.1.3_Produto 1'
                    self.tia_service.create_group(None, group_name, "3.1.1.3_Dispositivo Lado B")
                    prod_group =self.tia_service.recursive_group_search(None, group_name)
                    directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.3_Dispositivo Lado B\03.1.1.3.1_Produto 1"
                

            # Lista todos os arquivos que terminam com '.xml' no diretório especificado
            arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
            for arquivo in arquivos_xml:
                # Constrói o caminho completo para cada arquivo .xml
                full_path = os.path.join(directory_path, arquivo)
                udts = UDTService().list_udt_from_bk(full_path)
                udtss = UDTService().list_udt_from_bk_data(full_path)
                for udt in udts:
                    print("UDT FILES", udt)
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)
                for udt in udtss:
                    print("UDT FILES", udt)
                    udt_path = self.dependencies + '\\' + udt + '.xml'
                    device = self.tia_service.get_device_by_index(1)
                    self.tia_service.import_data_type(device, udt_path)

                # Obtém as informações do arquivo através do caminho completo
                self.tia_service.import_block(prod_group.Blocks, full_path)
                
        except Exception as e:
            print("Error importing produto mesa block: ", e)