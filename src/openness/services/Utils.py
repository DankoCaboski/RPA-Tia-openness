from System.IO import DirectoryInfo, FileInfo # type: ignore
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