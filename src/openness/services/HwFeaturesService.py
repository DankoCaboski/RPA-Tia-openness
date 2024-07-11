from openness.services.Utils import Utils

class HwFeaturesService:
    def __init__(self, hwf):
        self.hwf = hwf
        
    def get_software(self, parent):
        try:
            parent = parent.DeviceItems[1]
            software_container = Utils().get_service(self.hwf.SoftwareContainer, parent)
            if not software_container:
                raise Exception("No SoftwareContainer found for device.")
            else:
                plc_software = software_container.Software
                if not plc_software:
                    raise Exception("No PLC software found for device.")
                return software_container.Software
            
        except Exception as e:
            RPA_status = 'Error getting software container: ', e
            print(RPA_status)
            print("Name: ", str(parent.GetAttribute("Name")))
            print("Type: ", parent.GetType())
            
    def get_network_interface_CPU(self, deviceComposition):
        cpu = Utils().getCompositionPosition(deviceComposition)[1].DeviceItems
        for option in cpu:
            optionName = option.GetAttribute("Name")
            if optionName == "PROFINET interface_1":
                return Utils().get_service(self.hwf.NetworkInterface, option)
            
    def get_network_interface_IHM(self, deviceComposition):
        hmiItems = Utils().getCompositionPosition(deviceComposition)
        for items in hmiItems:
            hmi = items.DeviceItems
            for option in hmi:
                optionName = option.GetAttribute("Name")
                if optionName == "PROFINET Interface_1":
                    return Utils().get_service(self.hwf.NetworkInterface, option)
    
    def get_network_interface_REMOTAS(self, deviceComposition):
        remota = Utils().getCompositionPosition(deviceComposition)[1].DeviceItems
        for option in remota:
            optionName = option.GetAttribute("Name")
            if optionName == "PROFINET interface":
                return Utils().get_service(self.hwf.NetworkInterface, option)