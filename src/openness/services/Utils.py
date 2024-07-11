import clr

from System.IO import DirectoryInfo, FileInfo # type: ignore
from System.Collections.Generic import List # type: ignore
from openness.repositories.DbManagement import DbManagement
from tkinter import filedialog

class Utils:
    def __init__(self) -> None:
        pass
    
    def configurePath(self, path: str):
        return path.replace("/", "\\")

    def get_directory_info(self, path: str):
        path = self.configurePath(path)
        return DirectoryInfo(path)

    def get_file_info(self, path: str):
        path = self.configurePath(path)
        return FileInfo(path)
    
    def open_directory_dialog(self):
        return filedialog.askdirectory()
    
    def open_file_dialog(self):
        return filedialog.askopenfilename()
    
    def get_tia_versions(self):
        versions = DbManagement().get_tia_versions()
        mylist = []
        
        for version in versions:
            if str(version[0]) == "151":
                mylist.append("15.1")
            else:
                mylist.append(str(version[0]))
        return mylist
    
    def get_attributes(
        self,
        attribute_names: list[str],
        item
        ):
        
        cs_attribute_names = List[str]()
        for i in attribute_names:
            cs_attribute_names.Add(i)
        return item.GetAttributes(cs_attribute_names)

    def get_mlfb_by_hw_type(self, hw_type: str):
        return DbManagement().get_mlfb_by_hw_type(hw_type)
    
    def get_firmware_by_mlfb(self, hw_type: str):
        return DbManagement().getMlfbByVersion(hw_type)
    
    def get_service(self, tipo, parent):
        try:
            network_interface_type = tipo
            getServiceMethod = parent.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
            return getServiceMethod.Invoke(parent, None)
        except Exception as e:
            RPA_status = 'Error getting service: ', e
            print(RPA_status)
            
    def getCompositionPosition(self, deviceComposition):
        return deviceComposition.DeviceItems