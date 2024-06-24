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
    
    def create_project(self, proj_name, proj_path, tia_version):
        if self.tia_instance is None:
            self.open_tia_ui()
        proj_path = Utils().get_directory_info(proj_path+"\\"+proj_name)
        self.myproject = self.tia_instance.Projects.Create(proj_path, proj_name)
        
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