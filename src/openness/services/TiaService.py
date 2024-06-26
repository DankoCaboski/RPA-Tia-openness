from openness.services.Utils import Utils
from openness.services.HwFeaturesService import HwFeaturesService
from openness.services.CompilerService import CompilerService
from openness.services.LanguageService import LanguageService
from openness.services.XmlService import XmlService

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
            if self.myproject != None:
                result = "Projeto criado com sucesso!"
                print(result)
                return result
            
        except Exception as e:
            result = "Falha ao criar projeto: " + str(e)
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
        cpu_list = self.get_all_devices(self.myproject)
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
                        config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
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

    def import_data_type(self, cpu, data_type_path):
        try:
            udts_dependentes = XmlService().list_udt_from_xml(data_type_path)
            for udt in udts_dependentes:
                udt_path = data_type_path.rsplit(".xml", 1)[0] + "\\" + udt + ".xml"
                self.import_data_type(self.myproject, cpu, udt_path) 
            
            types = self.get_types(cpu)
            if type(data_type_path) == str:
                data_type_path = Utils().get_file_info(data_type_path)
            import_options = self.tia.ImportOptions.Override
            types.Import(data_type_path, import_options)
            
        except Exception as e:
            if str(e).__contains__("culture"):
                LanguageService().add_language(self.myproject, "pt-BR")
                self.import_data_type(self.myproject, cpu, data_type_path)
                
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