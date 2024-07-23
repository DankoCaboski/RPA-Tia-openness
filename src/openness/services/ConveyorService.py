# Essa classe está focada em fazer o import dos blocos das esteiras,
# toda criação de pasta e subpastas das esterias são feitas aqui

import os
import re
from openness.services.XmlService import XmlService
from openness.services.UDTService import UDTService

from openness.services.Utils import Utils
class ConveyorService:
    def __init__(self, tia_service) -> None:
        self.tia_service = tia_service
        self.dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\PLC data types"
        
    def manage_conveyor(self, conveyor_associations: list, conve_name: str):
        try:
            print('COnveyor', conveyor_associations)
            for i, association in enumerate(conveyor_associations):
                print(f"Manage conveyor: i == {i}")
                inversor = association['Inversor']
                presenca = association['Presença']
                posicao = association['Posição']
                if inversor or presenca or posicao:
                    conveyor_group = self.create_conveyor_structure(i)
                    self.import_conveyor_structure(conveyor_group, i )
                
        except Exception as e:
            print("Error manage_robots: ", e)


    def create_conveyor_structure(self, i: int):
        try:            
            group_name = f"03.3.{i+1}_ES0{i+1}"
            parente_name = 'z1_Esteiras'
            conveyor_group = self.tia_service.create_group(None, group_name, parente_name )
            grupo_esteira = self.tia_service.recursive_group_search(None, parente_name)
            std_group = self.tia_service.recursive_group_search(None, '02_Blocos Standard Axis')
            
            if i == 0: 
                path_ob = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.3_Esteiras\Main_Esteiras.xml"
                self.tia_service.import_block(grupo_esteira.Blocks, path_ob)
                path_fb = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\02_Blocos Standard Axis\2013_FB Mesa Descarga de Peça.xml"
                self.tia_service.import_block(std_group.Blocks, path_fb)


            if not conveyor_group:
                raise Exception("Error creating  group")
            
            return conveyor_group
            
        except Exception as e:
            print("Error creating conveyor structure: ", e)


    def import_conveyor_structure(self, conveyor_group, index):
        try:
            bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Program blocks\03_Blocos Operacionais\3.3_Esteiras\3.3.1_ES01"
                    
            # Lista todos os arquivos que terminam com '.xml' no diretório especificado
            arquivos_xml = [f for f in os.listdir(bk_path) if f.endswith('.xml')]
            for arquivo in arquivos_xml:
                print('Arquivo', arquivo)
                # Constrói o caminho completo para cada arquivo .xml
                full_path = os.path.join(bk_path, arquivo)
                self.import_cv_bk(conveyor_group, full_path, index)
                
        except Exception as e:
            print("Error no estrutura do robô: ", e)
            
    def import_cv_bk(self, conveyor_group, bk_path, index):
        try:

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

            if index > 0:
                bk_file_info = Utils().get_file_info(bk_path)
                aux = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls"
                temp_path = f"{aux}\\{Utils().generate_entropy_string()}.xml"
                print('arquivo novo', temp_path)
                bk_file_info.CopyTo(temp_path)

                with open(temp_path, 'r', encoding='utf-8') as file:
                    conteudo = file.read()

                # Encontrar o valor atual dentro da tag <Name> e <Number>
                nome_atual = re.search(r'(?<=<Name>)[^<]+(?=</Name>)', conteudo).group()
                numero_atual = re.search(r'(?<=<Number>)[^<]+(?=</Number>)', conteudo)

                if nome_atual == '33101_ES01':
                    # Inicializar novo_nome e novo_numero da FC da esteira
                    novo_nome = ""
                    novo_numero = ""

                    if nome_atual:
                        # Substituir o último número antes de _MG com o novo índice
                        nome_part = re.search(r'(\d+)(?=_ES)', nome_atual)
                        if nome_part:
                            novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_ES0{index+1}"
                        else:
                            novo_nome = nome_atual + f"_ES0{index+1}"
                    else:
                        novo_nome = f"Name_ES0{index+1}"

                elif nome_atual == '33110_Presença de Peça':
                    # Inicializar novo_nome e novo_numero da FC PP
                    novo_nome = ""
                    novo_numero = ""

                    if nome_atual:
                        nome_atual = nome_atual
                        # Substituir o último número antes de _MG com o novo índice
                        nome_part = re.search(r'(\d+)(?=_Pre)', nome_atual)
                        if nome_part:
                            novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_Presença de Peça 0{index+1}"
                        else:
                            novo_nome = nome_atual + f"_Presença de Peça{index+1}"
                    else:
                        novo_nome = f"Name_Presença0{index+1}" 

                elif nome_atual == '33110_ES01_ Presença de Peça_DB' :
                    # Inicializar novo_nome e novo_numero da FC da esteira
                    novo_nome = ""
                    novo_numero = ""

                    if nome_atual:
                        # Substituir o último número antes de _MG com o novo índice
                        nome_part = re.search(r'(\d+)(?=_ES)', nome_atual)
                        if nome_part:
                            novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_ Presença de Peça_DB 0{index+1}"
                        else:
                            novo_nome = nome_atual + f"_ Presença de Peça_DB{index+1}"
                    else:
                        novo_nome = f"Name_Presença de Peça_DB{index+1}"
                elif nome_atual == '33111_FB Mesa Descarga de Peça_DB':
                    # Inicializar novo_nome e novo_numero da FC PP
                    novo_nome = ""
                    novo_numero = ""

                    if nome_atual:
                        nome_atual = nome_atual
                        # Substituir o último número antes de _MG com o novo índice
                        nome_part = re.search(r'(\d+)(?=_FB)', nome_atual)
                        if nome_part:
                            novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_FB Mesa Descarga de Peça_DB 0{index+1}"
                        else:
                            novo_nome = nome_atual + f"Descarga de Peça_DB0{index+1}"
                    else:
                        novo_nome = f"Name_Descarga de Peça_DB0{index+1}"

                if numero_atual:
                    if nome_atual == '33110_ES01_ Presença de Peça_DB':
                        numero_atual = int(numero_atual.group())
                        novo_numero = numero_atual + index
                    elif nome_atual == '33111_FB Mesa Descarga de Peça_DB':
                        numero_atual = int(numero_atual.group())
                        novo_numero = numero_atual + (index + 3 )
                    else:
                        numero_atual = int(numero_atual.group())
                        novo_numero = numero_atual + index
                else:
                    novo_numero = "1"
                XmlService().editar_tags_xml(temp_path, novo_nome, novo_numero )            
                self.tia_service.import_block(conveyor_group.Blocks, temp_path)
                    
                Utils().get_file_info(temp_path).Delete() 
            else:
                self.tia_service.import_block(conveyor_group.Blocks, bk_path)
            
        except Exception as e:
            print("Error importing robot block: ", e)