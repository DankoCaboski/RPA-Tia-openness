import os
import re
from openness.services.Utils import Utils
from openness.services.UDTService import UDTService
from openness.services.XmlService import XmlService
class MesaService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types"
        
        
    def manage_turntables(self, turntables_associations: list, turn_name: str):
        try:
            print("\n", turntables_associations)
            print("Manage turntables: ")
            for Index, turntable in enumerate(turntables_associations):
                driver = turntable['driver']
                self.turntable_group = self.create_turntables_structure(Index)
                std_group = self.tia_service.recursive_group_search(None, '02_Blocos Standard Axis')
                prodiag = self.tia_service.recursive_group_search(None, '01.3_Prodiag')
                if Index <= 1:
                    self.import_mg_std(std_group, driver, prodiag)
                # Process each side (ladoA, ladoB, ladoC, ladoD)
                for side, products in turntable.items():
                    if 'lado' in side:  # Filter out non-side keys like 'driver'
                        print(f"Processing {side} for driver {driver}")
                        # Process each product in the side
                        self.import_mg(self.turntable_group[0], side, Index)
                        for product_name, details in products.items():
                            cl_value = details['Cl']
                            pp_value = details['PP']
                            # Implement conditional logic based on 'Cl' and 'PP' values
                            if cl_value and pp_value:
                                print(f"{product_name} on {side} has 'Cl' = {cl_value} and 'PP' = {pp_value}.")
                                self.import_mg_mesa(self.turntable_group[1], side, Index)
                                self.import_mg_prod(side, product_name, Index)
                            else:
                                print(f"{product_name} on {side} is missing 'Cl' or 'PP' values.")                      
                        
        except Exception as e:
            print("Error manage_turntables: ", e)

    def create_turntables_structure(self, i):
        try:           
            print('VALOR DE i', i)
            group_name = f"3.1.{i+1}_MG0{i+1}"
            grupo_mesa_name = "z1_Mesas Giratórias"
            turntable_group = self.tia_service.create_group(None, group_name, grupo_mesa_name)
            grupo_mesa = self.tia_service.recursive_group_search(None, grupo_mesa_name)

            if i == 0: 
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
    def import_mg_std(self, std_group, turntable_turntable_brand, prodiag):
        try:         
            #IMPORT SEPARADO DE UDT 
            device = self.tia_service.get_device_by_index(1)
            IHMBypass = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types\02_Axis.Vlv.IHM.Status&Bypass.xml"
            self.tia_service.import_data_type(device, IHMBypass)

            # Lista de caminhos dos arquivos
            file_paths = [
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2006_FB Válvulas.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2008_FB Presença de Peça.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2014_FC Conversion_XY.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2011_FC SEW Movidrive Modulo Positioning.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2016_FB Mesa Giratoria Movidrive Sew.xml",
                r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2015_FB Mesa Giratoria Sinamics Siemens.xml"

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

            self.tia_service.import_block(std_group.Blocks, file_paths[0])
            self.tia_service.import_block(std_group.Blocks, file_paths[1])
            self.tia_service.import_block(std_group.Blocks, file_paths[2])
            self.tia_service.import_block(std_group.Blocks, file_paths[3])
            self.tia_service.import_block(std_group.Blocks, file_paths[4])
            self.tia_service.import_block(std_group.Blocks, file_paths[5])
            # self.tia_service.import_block(prodiag.Blocks, PP_path)
            
                
        except Exception as e:
            print("Error importing standard mesa block: ", e)

    #import do mesa MG
    def import_mg(self, turntable_mesa, turntable_brand, index):
        try:   
            if index == 0:

                if turntable_brand == 'ladoA':
                    generated_block_name = Utils().get_attributes(["Name"],turntable_mesa)
                    print(f'Importing {turntable_brand} mesa block to {generated_block_name[0]}...')
                    group_name = f'3.1.{index+1}.1_Mesa MG0{index+1}'
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
            else:
                
                if turntable_brand == 'ladoA':
                    generated_block_name = Utils().get_attributes(["Name"],turntable_mesa)
                    print(f'Importing {turntable_brand} mesa block to {generated_block_name[0]}...')
                    group_name = f'3.1.{index+1}.1_Mesa MG0{index+1}'
                    turntable_mesa = self.tia_service.recursive_group_search(None, group_name)
                    directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.2_MG02"
                    
                    # Lista todos os arquivos que terminam com '.xml' no diretório especificado
                    arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
                    for arquivo in arquivos_xml:
                        print('Arquivo', arquivo)
                        # Constrói o caminho completo para cada arquivo .xml
                        full_path = os.path.join(directory_path, arquivo)
                        udts = UDTService().list_udt_from_bk(full_path)
                        udtss = UDTService().list_udt_from_bk_data(full_path)
                        for udt in udts:
                            udt_path = self.dependencies + '\\' + udt + '.xml'
                            device = self.tia_service.get_device_by_index(1)
                            self.tia_service.import_data_type(device, udt_path)
                        for udt in udtss:
                            udt_path = self.dependencies + '\\' + udt + '.xml'
                            device = self.tia_service.get_device_by_index(1)
                            self.tia_service.import_data_type(device, udt_path)

                        if index > 1:
                                if index > 1:
                                    bk_file_info = Utils().get_file_info(full_path)
                                    aux = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls"
                                    temp_path = f"{aux}\\{Utils().generate_entropy_string()}.xml"
                                    print('arquivo novo', temp_path)
                                    bk_file_info.CopyTo(temp_path)

                                    with open(temp_path, 'r', encoding='utf-8') as file:
                                        conteudo = file.read()

                                    # Encontrar o valor atual dentro da tag <Name> e <Number>
                                    nome_atual = re.search(r'(?<=<Name>)[^<]+(?=</Name>)', conteudo)
                                    numero_atual = re.search(r'(?<=<Number>)[^<]+(?=</Number>)', conteudo)

                                    # Inicializar novo_nome e novo_numero
                                    novo_nome = ""
                                    novo_numero = ""

                                    if nome_atual:
                                        nome_atual = nome_atual.group()
                                        # Substituir o último número antes de _MG com o novo índice
                                        nome_part = re.search(r'(\d+)(?=_MG)', nome_atual)
                                        if nome_part:
                                            novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_MG0{index+1}"
                                        else:
                                            novo_nome = nome_atual + f"_MG0{index+1}"
                                    else:
                                        novo_nome = f"Name_MG0{index+1}"

                                    if numero_atual:
                                        numero_atual = int(numero_atual.group())
                                        novo_numero = numero_atual + (index - 1 )
                                    else:
                                        novo_numero = "1"
                                    XmlService().editar_tags_xml(temp_path, novo_nome, novo_numero )
                                    
                                    self.tia_service.import_block(turntable_mesa.Blocks, temp_path)
                                        
                                    Utils().get_file_info(temp_path).Delete()
                                    
                                else:
                                    self.tia_service.import_block(turntable_mesa.Blocks, full_path)
                        else:
                            self.tia_service.import_block(turntable_mesa.Blocks, full_path)
                    
        except Exception as e:
            print("Error importing mesa block: ", e)

    #Import dispositivo lado
    def import_mg_mesa(self,opera_group,  turntable_brand,index):
        try:
            if index == 0:
                
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
    def import_mg_prod(self, turntable_prod , produto, index):
        try:  
            if index == 0:     
                
                if turntable_prod == 'ladoA':
                    print("Produto name", produto)
                    if produto == 'Produto 1':
                        group_name = '3.1.1.2_'+produto
                        self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado A")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.2_Dispositivo Lado A\3.1.1.2_Produto 1"
                    elif produto == 'Produto 2':
                        group_name = '3.1.1.2_'+produto
                        self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado A")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.2_Dispositivo Lado A\3.1.1.2_Produto 2"
                    elif produto == 'Produto 3':
                        group_name = '3.1.1.2_'+produto
                        self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado A")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.2_Dispositivo Lado A\3.1.1.2_Produto 3"
                elif turntable_prod == 'ladoB':
                    if produto == 'Produto 1':
                        group_name = '3.1.1.3_Produto 1'
                        self.tia_service.create_group(None, group_name, "3.1.1.3_Dispositivo Lado B")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.3_Dispositivo Lado B\03.1.1.3.1_Produto 1"
                    elif produto == 'Produto 2':
                        group_name = '3.1.1.2_'+produto
                        self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado B")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.3_Dispositivo Lado B\03.1.1.3.1_Produto 2"
                    elif produto == 'Produto 3':
                        group_name = '3.1.1.2_'+produto
                        self.tia_service.create_group(None, group_name, "3.1.1.2_Dispositivo Lado B")
                        prod_group =self.tia_service.recursive_group_search(None, group_name)
                        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.1_Mesas Giratórias\3.1.1_MG01\3.1.1.3_Dispositivo Lado B\03.1.1.3.1_Produto 3"
                    

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