from System.IO import DirectoryInfo, FileInfo # type: ignore
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