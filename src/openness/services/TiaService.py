import os
from openness.services.Utils import Utils
from openness.services.HwFeaturesService import HwFeaturesService
from openness.services.CompilerService import CompilerService
from openness.services.LanguageService import LanguageService
from openness.services.XmlService import XmlService
from openness.services.RobotService import RobotService
from openness.services.IHMService import IHMService
import pygetwindow as gw
import pyautogui
from System import Int32, String # type: ignore


class TiaService:
    def __init__(self, tia, hwf, comp):
        self.tia = tia
        self.hwf: HwFeaturesService = HwFeaturesService(hwf)
        self.comp: CompilerService = CompilerService(comp)
        self.tia_instance = None
        self.myproject = None
        self.my_devices = []
        self.my_subnet = None
        
    def save_project(self):
        try:
            self.myproject.Save()
            RPA_status = 'Projeto salvo com sucesso!'
            print(RPA_status)
            return RPA_status
        except Exception as e:
            RPA_status = 'Falha ao salvar projeto: ', e
            print(RPA_status)
            return RPA_status
        
    def get_project(self):
        if self.myproject is None:
            raise "No project open"
        return self.myproject
        
    def open_tia_ui(self):
        # Create an instance of Tia Portal
        self.tia_instance = self.tia.TiaPortal(self.tia.TiaPortalMode.WithUserInterface)
        return self.tia_instance
    
    def open_project(self, project_path):
        file_info = Utils().get_file_info(project_path)
        
        if not file_info.Exists:
            return "Project file not found"
    
        if self.tia_instance is None:
            self.open_tia_ui()

        return self.tia_instance.Projects.OpenWithUpgrade(file_info)
    
    def create_project(self, proj_name, proj_path):
        proj_path = Utils().get_directory_info(proj_path)
        try:
            if self.tia_instance is None:
               self.mytia = self.open_tia_ui()
                
            self.myproject = self.tia_instance.Projects.Create(proj_path, proj_name)
            LanguageService().add_language(self.myproject, "pt-BR")
            if self.myproject == None:
                raise Exception("Error creating project")
            
        except Exception as e:
            result = "Falha ao gerar projeto: " + str(e)
            print(result)
            return result
        
    def get_all_devices(self):
        try:
            devices = []
            for device in self.myproject.Devices:
                devices.append(device)
            return devices
        except Exception as e:
            print('Error getting all devices:', e)
            
    def get_device_by_index(self, index):
        cpu_list = self.get_all_devices()
        cpu = cpu_list[index]
        return cpu
    
    def get_device_by_name(self, device_name):
        return next((d for d in self.myproject.Devices if d.Name == device_name), None)

    def add_hardware(self,  hardwware: list):
        try:
            plc_count = 0
            remota_count = 0
            for device in hardwware:
                deviceType = device['type']
                deviceName = device['name']
                deviceMlfb = device['mlfb']
                FirmVersion = device['firmware']
                Start_Adress = device ['Address']
                if self.myproject != None:
                    if deviceType == "CONTROLLERS":
                        if "F" in deviceMlfb:
                            print("é safety")
                        plc_count += 1
                        print('Creating CPU: ', deviceName)
                        config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                        deviceCPU = self.myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
                        count = self.myproject.Devices.Count
                        Count = count - 1
                        Device = self.myproject.Devices[Count]
                        networkIterface = self.hwf.get_network_interface_CPU(Device)
                        Node = networkIterface.Nodes[0]
                        address = Node.SetAttribute("Address", String(Start_Adress))
                        self.my_devices.append(deviceCPU)
                    elif deviceType == "REMOTAS":
                        remota_count += 1
                        print('Creating CPU: ', deviceName)
                        config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                        deviceREMOTA = self.myproject.UngroupedDevicesGroup.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
                        count = self.myproject.UngroupedDevicesGroup.Devices.Count
                        Count = count - 1
                        Device = self.myproject.UngroupedDevicesGroup.Devices[Count]
                        networkIterface = self.hwf.get_network_interface_REMOTAS(Device)
                        Node = networkIterface.Nodes[0]
                        address = Node.SetAttribute("Address", String(Start_Adress))
                        self.my_devices.append(deviceREMOTA)
                    elif deviceType == "IHM":
                        print("Creating IHM: ", deviceName)
                        config_Hmi = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                        deviceIHM = self.myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
                        count = self.myproject.Devices.Count
                        Count = count - 1
                        Device = self.myproject.Devices[Count]
                        networkIterface = self.hwf.get_network_interface_IHM(Device)
                        Node = networkIterface.Nodes[0]
                        address = Node.SetAttribute("Address", String(Start_Adress))
                        self.my_devices.append(deviceIHM)

                    elif deviceType == "DI" or deviceType == "DO":
                        Remota = self.myproject.UngroupedDevicesGroup.Devices.Count
                        if Remota  == 0: 
                            print('Creating IO Node: ', deviceName)
                            confing_IOnode = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                            Devices = self.myproject.Devices[plc_count]
                            typeName = Devices.GetAttribute("TypeName")
                            if typeName == "ET 200SP-Station":
                                countFINAL = Devices.DeviceItems.Count
                                count = countFINAL - 1 
                            elif typeName == "ET 200S station":
                                countFINAL = Devices.DeviceItems.Count
                                count = countFINAL + 2
                            else:
                                count = Devices.DeviceItems.Count
                            DeviceItemAssociation = Devices.GetAttribute("Items")
                            if DeviceItemAssociation[0].CanPlugNew(confing_IOnode, deviceName, count):
                                IONode = DeviceItemAssociation[0].PlugNew(confing_IOnode, deviceName, count)
                                if typeName == "ET 200SP-Station":
                                    Start_Adress_int = int(Start_Adress)
                                    addressController = Devices.DeviceItems[countFINAL].DeviceItems[0].Addresses[0]
                                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                                    GETStartAddress = addressController.GetAttribute("StartAddress")
                                elif typeName == "ET 200S station":
                                    addressController = Devices.DeviceItems[countFINAL].DeviceItems[0].Addresses[0]
                                    Start_Adress_int = int(Start_Adress)
                                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                                    GETStartAddress = addressController.GetAttribute("StartAddress")
                                else:
                                    addressController = Devices.DeviceItems[count].DeviceItems[0].Addresses[0]
                                    Start_Adress_int = int(Start_Adress)
                                    StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                                    GETStartAddress = addressController.GetAttribute("StartAddress")
                                    print("Address Start: " , GETStartAddress )
                                self.my_devices.append(IONode)
        except Exception as e:
            RPA_status = 'Unknown hardware type: ', deviceType
            print(RPA_status)
            RPA_status = 'Error creating hardware: ', e
            print(RPA_status)

    def addIORemota(self, hardware):
        deviceName = ''
        deviceMlfb = ''

        remot_count = 0
        for device in hardware:
            deviceType = device['type']
            deviceName = device['name']
            deviceMlfb = device['mlfb']
            FirmVersion = device['firmware']
            Start_Adress = device ['Address']
            
            if deviceType == "REMOTAS":
                remot_count += 1
            if remot_count > 0:
                     if deviceType == "DI" or deviceType == "DO":
                        print('Creating IO Node Remota: ', deviceName)
                        confing_IOnode = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                        remotaRef = remot_count - 1
                        Remota = self.myproject.UngroupedDevicesGroup.Devices.Count
                        if Remota  > 0: 
                            remotas = self.myproject.UngroupedDevicesGroup.Devices[remotaRef]
                            countFinal = remotas.DeviceItems.Count
                            count = countFinal - 2
                            DeviceItemAssociation = remotas.GetAttribute("Items")
                            if DeviceItemAssociation[0].CanPlugNew(confing_IOnode, deviceName, count):              
                                IONodeRemota = DeviceItemAssociation[0].PlugNew(confing_IOnode, deviceName, count)
                                addressController = remotas.DeviceItems[countFinal].DeviceItems[0].Addresses[0]
                                Start_Adress_int = int(Start_Adress)
                                StartAddress = addressController.SetAttribute("StartAddress", Int32(Start_Adress_int))
                                GETStartAddress = addressController.GetAttribute("StartAddress")
                                print("Address Start: " , GETStartAddress )
                            self.my_devices.append(IONodeRemota)

    def wire_profinet(self):
        ProfinetInterfaces = self.GetAllProfinetInterfaces()
        print("Nº de interfaces PROFINET: ", str(len(ProfinetInterfaces)))
        
        if len(ProfinetInterfaces) > 1:
            self.SetSubnetName("mySubnet")
            for port in ProfinetInterfaces:
                node = port.Nodes[0]
                self.ConnectToSubnet(node)
            
            RPA_status = "Rede PROFINET configurada com sucesso!"
            print(RPA_status)
            
        else:
            RPA_status = "Número de interfaces PROFINET menor que 2"
            print(RPA_status)

    def create_IO_System(self):
        redes = []
        Device = self.myproject.Devices[1]
        count = self.myproject.UngroupedDevicesGroup.Devices.Count
        if count >= 1:
            networkIterface = self.hwf.get_network_interface_CPU(Device)
            redeIO = networkIterface.IoControllers[0]
            nomerede = "PROFINET IO-System"
            rede = redeIO.CreateIoSystem(nomerede)
            RPA_status = "Rede IO Criada"
            print(RPA_status)
            redes.append(rede)
            return redes

    def connect_IO_System(self, hardware, redes):
        count = self.myproject.UngroupedDevicesGroup.Devices.Count
        if count >= 1:
            for rede in redes:  # Loop para cada rede na lista de redes
                for device in hardware:
                    deviceType = device ["type"]
                    if deviceType == "REMOTAS":
                        Devices = self.myproject.UngroupedDevicesGroup.Devices  # Referenciando a lista de dispositivos
                        for i, Device in enumerate(Devices):
                            networkInterface = self.hwf.get_network_interface_REMOTAS(Device)
                            Io_System = networkInterface.IoConnectors[0]
                            if Io_System.GetAttribute("ConnectedToIoSystem") == "" or Io_System.GetAttribute("ConnectedToIoSystem") == None:  # Verifica se o Io_System não está conectado
                                connect = Io_System.ConnectToIoSystem(rede)  # Usando a rede atual do loop externo
                                RPA_status = "Rede IO Conectada"
                                print(RPA_status)
            
    def SetSubnetName(self, subnet_name):
        RPA_status = 'Setting subnet name'
        print(RPA_status)
        if subnet_name == '':
            subnet_name = 'mySubnet'
        self.my_subnet = self.myproject.Subnets.Create("System:Subnet.Ethernet", subnet_name)

    def ConnectToSubnet(self, node):
        try:
            node.ConnectToSubnet(self.my_subnet)
        except Exception as e:
            RPA_status = 'Error connecting to subnet: ', e
            print(RPA_status)
            
    def GetAllProfinetInterfaces(self):
        try:
            network_ports = []
            for device in self.my_devices:      
                if (not self.is_gsd(device)):
                    hardware_type = self.getHardwareType(device)
                    
                    if (hardware_type == "CONTROLLERS"):
                        self.get_types(device)
                        network_interface_cpu = self.hwf.get_network_interface_CPU(device)
                        network_ports.append(network_interface_cpu)
                        
                    elif (hardware_type == "IHM"):
                        network_interface_ihm = self.hwf.get_network_interface_IHM(device)
                        network_ports.append(network_interface_ihm)

                    elif (hardware_type == "REMOTAS"):
                        network_interface_remota = self.hwf.get_network_interface_REMOTAS(device)
                        network_ports.append(network_interface_remota)
                else:
                    RPA_status = 'Device' + str(device.GetAttribute("Name")) + ' is GSD: '
                    print(RPA_status)
                    
            return network_ports
        
        except Exception as e:
            RPA_status = 'Error getting PROFINET interfaces: ', e
            print(RPA_status)
            
    def getHardwareType(self, device):
        try:
            device_item_impl = Utils().getCompositionPosition(device)
            if (self.is_cpu(device_item_impl)):
                return "CONTROLLERS"
            elif (self.is_hmi(device_item_impl)):
                return "IHM"
            elif (self.is_IO(device_item_impl)):
                return "IO Node"
            elif (self.is_remota(device_item_impl)):
                return "REMOTAS"
            
        except Exception as e:
            RPA_status = 'Error getting hardware type: ', e
            print(RPA_status)
    
    def is_gsd(self, device):
        try:
            if device.GetAttribute("IsGsd") == True:
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking GSD: ', e
            print(RPA_status)
            
    def is_cpu(self, device):
        try:
            device_item = device[1]
            if str(device_item.GetAttribute("Classification")) == "CPU":
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking CPU: ', e
            print(RPA_status)

    def is_hmi(self, device):
        try:
            device_item = device[0]
            type_identifier = str(device_item.GetAttribute("TypeIdentifier"))
            
            if (type_identifier.__contains__("OrderNumber:6AV")):
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking IHM: ', e
            print(RPA_status)
            
    def is_IO(self, device):
        try:
            device_item = device[0]
            type_identifier = str(device_item.GetAttribute("TypeIdentifier"))
            
            if (type_identifier.__contains__("OrderNumber:6ES7")):
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking IO: ', e
            print(RPA_status)

    def is_remota(self, device):
        try:
            device_item = device[1]
            if str(device_item.GetAttribute("Classification")) == "HM":
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking CPU: ', e
            print(RPA_status)

    def get_types(self, cpu):
        plc_software = self.hwf.get_software(cpu)
        type_group = plc_software.TypeGroup
        return type_group.Types
    
    def recursive_group_search(self, groups, group_name: str):
        try:
            if not groups:
                return
            found = groups.Find(group_name)
            if found:
                return found
            
            for group in groups.GetEnumerator():
                found = self.recursive_group_search(group.Groups, group_name)
                if found:
                    return found
        except Exception as e:
            print('Error searching group:', e)
    
    def recursive_folder_search(self, groups, group_name):
        try:
            found = groups.Find(group_name)
            if found:
                return found
            
            for group in groups.GetEnumerator():
                found = self.recursive_folder_search(group.Folders, group_name)
                if found:
                    return found
        except Exception as e:
            print('Error searching group:', e)


    def create_folder(self, device, group_name, parent_group):
        try:
            if device == 'IHM':
                device = self.my_devices[0]
            ihm = self.hwf.get_Software_IHM(device).Software
            groups = ihm.ScreenFolder.Folders
            if not parent_group:
                return groups.Create(group_name)
            else:
                return self.recursive_folder_search(groups, parent_group).Folders.Create(group_name)
                
        except Exception as e:
            print('Error creating group:', e)

    def create_folder_tag(self, device, group_name, parent_group):
        try:
            if device == 'IHM':
                device = self.my_devices[0]
            ihm = self.hwf.get_Software_IHM(device).Software
            groups = ihm.TagFolder.Folders
            if not parent_group:
                return groups.Create(group_name)
            else:
                return self.recursive_folder_search(groups, parent_group).Folders.Create(group_name)
                
        except Exception as e:
            print('Error creating group:', e)

    def create_group(self, device, group_name: str, parent_group: str):
        try:
            if device is None:
                device = self.my_devices[1]
            plc_software = self.hwf.get_software(device)
            groups = plc_software.BlockGroup.Groups
            
            if not parent_group:
                return groups.Create(group_name)
            else:
                mygroup = self.recursive_group_search(groups, parent_group)
                if mygroup:
                    return mygroup.Groups.Create(group_name)
                else:
                    raise Exception(f"Parent {parent_group} group not found")
                
        except Exception as e:
            print('Error creating group:', e)

    def import_data_type(self, cpu, data_type_path):
        try:
            udts_dependentes = XmlService().list_udt_from_xml(data_type_path)
            for udt in udts_dependentes:
                udt_path = data_type_path.rsplit(".xml", 1)[0] + "\\" + udt + ".xml"
                self.import_data_type(cpu, udt_path) 
            
            types = self.get_types(cpu)
            if type(data_type_path) == str:
                data_type_path = Utils().get_file_info(data_type_path)
            import_options = self.tia.ImportOptions.Override
            types.Import(data_type_path, import_options)
            
        except Exception as e:
            if str(e).__contains__("culture"):
                LanguageService().add_language(self.myproject, "pt-BR")
                self.import_data_type(cpu, data_type_path)
                
            else:
                print('Error importing data type from: ', data_type_path)
                print('Error message: ', e)
                
    def export_data_type(self, device, data_type_name : str, data_type_path : str):
        try:
            types = self.get_types(device)
            data_type_path = data_type_path + "\\" + data_type_name + ".xml"
            data_type_path = Utils().get_file_info(data_type_path)
            
            data_type = types.Find(str(data_type_name))
            
            if data_type is not None:
                attempts = 0
                while data_type.GetAttribute("IsConsistent") == False:
                    result = self.comp.compilate_item(data_type) != "Success"
                    if result == "Success":
                        break
                    attempts += 1
                    if attempts > 3:
                        raise Exception("Error compiling data type")
            
                data_type.Export(data_type_path, self.tia.ExportOptions.WithDefaults)
                RPA_status = 'Data type exported successfully!'
                print(RPA_status)
                return True
            
            else:
                RPA_status = 'Data type not found'
                print(RPA_status)
                return False
                
        except Exception as e:
            print('Error exporting data type while in service:', e)
            
            
    def import_blocks(self, block_list: dict):
        if not block_list:
            print('No blocks to import')
            return
        print('Importing blocks')
        for zona in block_list.keys():
            for block in block_list[zona]:
                if block == "robots":
                    RobotService(self).manage_robots(block_list[zona][block])
                else:
                    print(block, block_list[zona][block])

    def import_screens_IHM(self, hardware, project_path, project_name):
        self.create_connection(project_path, project_name)
        IHMService(self, self.tia).create_IHM_structure(hardware)       
            
    def import_block(self, object, file_path):
        try:
            import_options = self.tia.ImportOptions.Override
            xml_file_info = Utils().get_file_info(file_path)
            
            object_type = str(object.GetType())
            
            if object_type != "Siemens.Engineering.HW.DeviceImpl" and object_type != "Siemens.Engineering.SW.Blocks.PlcBlockComposition":
                raise Exception("Invalid object type: ", object_type)
        
            else:
                if object_type == "Siemens.Engineering.HW.DeviceImpl":
                    object = object.DeviceItems[1]
                    print(f"Importing block to CPU: {object}")
                    plc_software = self.hwf.get_software(object)
                    plc_software.BlockGroup.Blocks.Import(xml_file_info, import_options)
                    
                elif object_type == "Siemens.Engineering.SW.Blocks.PlcBlockComposition":
                    print(f"Importing block to group: {object}")
                    object.Import(xml_file_info, import_options)
                
            return True
        
        except Exception as e:
            print('Error importing block:', e)
            return False
        
        
    def export_block(self, device, block_name : str, block_path : str):
        global RPA_status
        try:
            RPA_status = 'Exporting block'
            print(RPA_status)
            
            block_path = Utils().get_file_info(block_path + "\\" + block_name + ".xml")
            
            plc_software = self.hwf.get_software(device)
            myblock = plc_software.BlockGroup.Blocks.Find(block_name)
        
            attempts = 0
            while myblock.GetAttribute("IsConsistent") == False:
                result = self.comp.compilate_item(myblock) != "Success"
                if result == "Success":
                    break
                attempts += 1
                if attempts > 3:
                    raise Exception("Error compiling data type")
            
            myblock.Export(block_path, self.tia.ExportOptions.WithDefaults)
            
        except Exception as e:
            RPA_status = 'Error exporting block: ', e
            print(RPA_status)
            return
        
    def verify_and_import(self, device_name, file_path, repetitions=0, tipo='' ):
        try:
            
            device = self.get_device_by_name(device_name)
            
            if not device:
                print(f"Device {device_name} not found in the project.")
                return

            # Extrair nome e número base do XML
            if tipo == 'robo':
                nome_base = "0070_robo"
                numero_base = 70
            else:
                nome_base = "0080_Grampo"
                numero_base = 80

            if not nome_base or not numero_base:
                print("Failed to extract base name or number from XML.")
                return

            # Executar a primeira importação
            self.import_block(device, file_path)

            # Executar importações adicionais conforme necessário
            for i in range(repetitions):
                print(f"Repetition {i+1} of {repetitions}")

                # Modificar o XML com novos valores de nome e número
                novo_nome = f"{int(nome_base.split('_')[0]) + i + 1:04d}_{nome_base.split('_')[1]}"
                novo_numero = numero_base + i + 1
                
                # Chamar a função para modificar o XML
                XmlService().editar_tags_xml(file_path, novo_nome, novo_numero)

                # Realizar a importação após modificar o XML
                self.import_block(device, file_path)

        except Exception as e:
            print('Error verifying or importing file:', e)

    def import_libraries(self):
        biblioteca = Utils().get_file_info(r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\Library")
        OpenGlobalLibrary = self.tia_instance.GlobalLibraries.Open(biblioteca, self.tia.OpenMode.ReadWrite)
        print("Open Library")
        enumLibrary =  OpenGlobalLibrary.TypeFolder.Folders
        projectLib = self.myproject.ProjectLibrary
        for folder in enumLibrary:
            # Verifica se 'Types' não está vazio antes de tentar acessar um índice
            try:
                updateLibrary = folder.Types[0].UpdateLibrary(projectLib)
                nameFolderEnum = Utils().get_attibutes(["Name"], folder)
                nameFolder = nameFolderEnum[0]
                print('update library:', nameFolder)
            except IndexError:
                # Ocorre se não houver itens em Types
                print('Erro: Não há tipos disponíveis em', folder)
            except Exception as e:
                # Captura outras exceções que podem ocorrer no processo
                print('Erro ao atualizar a biblioteca:', e)
        CloseGlobalLibrary = self.mytia.GlobalLibraries[0].Close()
        print("Close Library")

    def import_graphics(self):
        print("Import graphic start")
        # Define o caminho do diretório onde estão os arquivos .xml
        directory_path = r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\IHM\Graphic"
        # Lista todos os arquivos que terminam com '.xml' no diretório especificado
        arquivos_xml = [f for f in os.listdir(directory_path) if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            # Constrói o caminho completo para cada arquivo .xml
            full_path = os.path.join(directory_path, arquivo)
            # Obtém as informações do arquivo através do caminho completo
            arquivoFile = Utils().get_file_info(full_path)
            import_options = self.tia.ImportOptions.Override
            import_graph = self.myproject.Graphics.Import(arquivoFile, import_options)
        print("Import graphic done")
    
    def create_connection(self, project_path, project_name):
        network = self.tia.HW.View.Network
        self.myproject.ShowHwEditor(network)
        # Encontrar a janela pelo título
        direct_path = os.path.normpath(project_path)
        windows_path = os.path.join(direct_path, project_name, project_name)
        print('path:', windows_path)
        windows = gw.getWindowsWithTitle(windows_path)[0]

        if windows:
            window = windows
            # Ativar a janela e trazê-la para o foco
            window.activate()
            # Esperar um momento para garantir que a janela está ativa
            pyautogui.sleep(1)
            window.maximize()
            pyautogui.sleep(1)
            #Move o mouse para fechar aba lateral
            pyautogui.click(window.left + 9, window.top + 150)
            pyautogui.sleep(1)
            #Clica em Connections
            pyautogui.click(window.left + 150, window.top + 150)
            #Move o mouse para cima da IHM
            pyautogui.moveTo(window.left + 150, window.top + 230)
            pyautogui.sleep(1)
            #Arrasta o mouse para o PLC 1
            pyautogui.dragTo(window.left + 370, window.top + 230, 1 , button='left')
            pyautogui.sleep(1)
            pyautogui.click()
            pyautogui.sleep(1.5)
            #Clica em Network
            pyautogui.click(window.left + 90, window.top + 150)
            pyautogui.sleep(1)
            #Move o mouse para abrir aba lateral
            pyautogui.click(window.left + 9, window.top + 150)
            pyautogui.sleep(1)
            print("Automação de usuaria concluída.")
        else:
            print("Janela não encontrada.")

    def get_Software_IHM(self, deviceComposition):
        return self.hwf.get_Software_IHM(deviceComposition)