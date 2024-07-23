# Essa classe está focada em fazer todas manipulações da IHM, tanto como template,telas e graphic list
# toda criação de pasta e subpastas da IHM são feitas aqui

import os
from openness.services.Utils import Utils
dependencies = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\dependence"


class IHMService:
    def __init__(self, tia_service, tia) -> None:
        self.tia_service = tia_service
        self.tia = tia
        
    def create_IHM_structure(self, hardware):
        for device in hardware:
            deviceType = device['type']
            deviceName = device['name']
            if deviceType == 'IHM':
                device = self.tia_service.get_device_by_name(deviceName)
                ihm = self.tia_service.get_Software_IHM(device).Software
                
                #Criação dos Grupos da telas Sistemas
                Sistemas =  '01_Sistemas'
                system_group = self.tia_service.create_folder(device, Sistemas, None).Screens
                group_name_axis =  '01.1_Axis Template'
                Axis_group = self.tia_service.create_folder(device, group_name_axis, Sistemas).Screens
                group_name_celula =  '01.2_Célula'
                Celula_group = self.tia_service.create_folder(device, group_name_celula, Sistemas).Screens
                group_name_prod =  '1.2.1_Contagem de Produção'
                prod_group = self.tia_service.create_folder(device, group_name_prod, group_name_celula).Screens
                group_name_prod_temp =  '1.2.2_Tempo de Ciclo'
                temp_group = self.tia_service.create_folder(device, group_name_prod_temp, group_name_celula).Screens
                group_name_alarm =  '01.3_Alarmes'
                alarm_group = self.tia_service.create_folder(device, group_name_alarm, Sistemas).Screens
                
                #Criação dos Grupos da telas Operacionais
                opera =  '03_Telas Operacionais'
                system_group = self.tia_service.create_folder(device, opera, None).Screens
                robos = '3.4_Robôs'
                robos_group = self.tia_service.create_folder(device, robos, opera).Screens
                robo1 = '3.4.1_RB01'
                rb1_group = self.tia_service.create_folder(device, robo1, robos).Screens

                #Criação dos grupos das tags
                Sistemas_tag =  '01_Sistemas'
                system_group_tag = self.tia_service.create_folder_tag(device, Sistemas_tag, None).TagTables

                #Chamadas
                self.import_graphicList(ihm)
                self.import_template(ihm)
                self.import_Screens(Axis_group, 'sistema')
                self.import_Screens(prod_group, 'prod')
                self.import_Screens(temp_group, 'ciclo')
                self.import_Screens(alarm_group, 'alarm')
                self.import_Screens(rb1_group, 'RB1')
                self.import_tags(system_group_tag)

    def import_Screens(self, group, screen_type):
        screen_paths = {
            'sistema': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\01_Sistema\01-1_Axis",
            'prod': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\01_Sistema\01-2_Ciclo\Contagem Produção",
            'ciclo': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\01_Sistema\01-2_Ciclo\Templo Ciclo",
            'alarm': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\01_Sistema\01-3-Alarm",
            'RB1': r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Screens\03_Telas Operacionais\3.4_Robos\3.4.1_RB01"
        }
        
        if screen_type in screen_paths:
            Screen_bk_path = screen_paths[screen_type]
            arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
            for arquivo in arquivos_xml:
                arquivo_caminho_completo = Utils().get_file_info(os.path.join(Screen_bk_path, arquivo))
                import_options = self.tia.ImportOptions.Override
                group.Import(arquivo_caminho_completo, import_options)
        else:
            raise ValueError(f"Tipo de tela '{screen_type}' não é válido. Use 'sistema', 'prod' ou 'alarm'.")

    def import_tags(self, group):
        Screen_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Tags\01_Sistemas"
        arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            arquivo_caminho_completo = Utils().get_file_info(os.path.join(Screen_bk_path, arquivo))
            import_options = self.tia.ImportOptions.Override
            ScreensSystem = group.Import(arquivo_caminho_completo, import_options)

    def import_template(self, device):
        template = device.ScreenTemplateFolder.ScreenTemplates
        Screen_bk_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Template"
        arquivos_xml = [f for f in os.listdir(Screen_bk_path) if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            arquivo_caminho_completo = Utils().get_file_info(os.path.join(Screen_bk_path, arquivo))
            import_options = self.tia.ImportOptions.Override
            importTemplate = template.Import(arquivo_caminho_completo, import_options)

    def import_graphicList(self, device):
        print("Import graphic start")
        # Define o caminho do diretório onde estão os arquivos .xml
        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\GraphicList"
        # Lista todos os arquivos que terminam com '.xml' no diretório especificado
        arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            # Constrói o caminho completo para cada arquivo .xml
            full_path = os.path.join(directory_path, arquivo)
            # Obtém as informações do arquivo através do caminho completo
            arquivoFile = Utils().get_file_info(full_path)
            import_options = self.tia.ImportOptions.Override
            import_graph = device.GraphicLists.Import(arquivoFile, import_options)
        print("Import graphic done")
    