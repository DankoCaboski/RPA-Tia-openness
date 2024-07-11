from openness.services.Utils import Utils
from openness.services.HwFeaturesService import HwFeaturesService
from openness.services.CompilerService import CompilerService
from openness.services.LanguageService import LanguageService
from openness.services.XmlService import XmlService
from openness.services.RobotService import RobotService


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
                self.open_tia_ui()
                
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
            for device in hardwware:
                deviceType = device['type']
                deviceName = device['name']
                deviceMlfb = device['mlfb']
                FirmVersion = device['firmware']
                
                if self.myproject != None:
                    if deviceType == "PLC":
                        print('Creating CPU: ', deviceName)
                        config_Plc = "OrderNumber:6ES7 512-1SK01-0AB0/V2.5"
                        # config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion  #
                        deviceCPU = self.myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)  
                        self.my_devices.append(deviceCPU)
                        
                    elif deviceType == "IHM":
                        print("Creating IHM: ", deviceName)
                        config_Hmi = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                        deviceIHM = self.myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
                        self.my_devices.append(deviceIHM)

                    # elif deviceType == "IO Node":
                    #     print('Creating IO Node: ', deviceName)
                    #     confing_IOnode = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                    #     plcRef = hardwware.index() - 1
                    #     Devices = self.myproject.Devices[plcRef]
                    #     count = Devices.DeviceItems.Count
                    #     DeviceItemAssociation = Devices.GetAttribute("Items")
                    #     if DeviceItemAssociation[0].CanPlugNew(confing_IOnode, deviceName, count):
                    #         IONode = DeviceItemAssociation[0].PlugNew(confing_IOnode, deviceName, count)
                    #         self.my_devices.append(deviceIHM)
                
        except Exception as e:
            RPA_status = 'Unknown hardware type: ', deviceType
            print(RPA_status)
            RPA_status = 'Error creating hardware: ', e
            print(RPA_status)
            
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
                    
                    if (hardware_type == "CPU"):
                        self.get_types(device)
                        network_interface_cpu = self.hwf.get_network_interface_CPU(device)
                        network_ports.append(network_interface_cpu)
                        
                    elif (hardware_type == "IHM"):
                        network_interface_ihm = self.hwf.get_network_interface_IHM(device)
                        network_ports.append(network_interface_ihm)
                        
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
                return "CPU"
            elif (self.is_hmi(device_item_impl)):
                return "IHM"
            elif (self.is_IO(device_item_impl)):
                return "IO Node"
            
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
                print("###################################################IO###################################################") 
                return True
            return False
        
        except Exception as e:
            RPA_status = 'Error checking IO: ', e
            print(RPA_status)
            
    def get_types(self, cpu):
        plc_software = self.hwf.get_software(cpu)
        type_group = plc_software.TypeGroup
        return type_group.Types
    
    def recursive_group_search(self, groups, group_name):
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


    def create_group(self, device, group_name: str, parent_group: str):
        try:
            if device is None:
                device = self.my_devices[0]
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