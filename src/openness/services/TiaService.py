from openness.services.Utils import Utils

class TiaService:
    def __init__(self, tia):
        self.tia = tia
        self.tia_instance = None
        self.myproject = None
        
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
    
    def create_project(self, proj_name, proj_path, tia_version):
        try:
            if self.tia_instance is None:
                self.open_tia_ui()
                
            self.tia_instance.Projects.Create(proj_name, proj_path, tia_version)
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

    def addHardware(self, deviceType, deviceName, deviceMlfb, FirmVersion, plc_count):
        try:
            if deviceType == "PLC":
                print('Creating CPU: ', deviceName)
                config_Plc = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                deviceCPU = self.myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
                return deviceCPU
                
            elif deviceType == "IHM":
                print("Creating IHM: ", deviceName)
                config_Hmi = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                deviceIHM = self.myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
                return deviceIHM

            elif deviceType == "IO Node":
                print('Creating IO Node: ', deviceName)
                confing_IOnode = "OrderNumber:"+deviceMlfb+"/"+FirmVersion
                plcRef = plc_count - 1
                Devices = self.myproject.Devices[plcRef]
                count = Devices.DeviceItems.Count
                DeviceItemAssociation = Devices.GetAttribute("Items")
                if DeviceItemAssociation[0].CanPlugNew(confing_IOnode, deviceName, count):
                    IONode = DeviceItemAssociation[0].PlugNew(confing_IOnode, deviceName, count)
                    return IONode
                
        except Exception as e:
            RPA_status = 'Unknown hardware type: ', deviceType
            print(RPA_status)
            RPA_status = 'Error creating hardware: ', e
            print(RPA_status)