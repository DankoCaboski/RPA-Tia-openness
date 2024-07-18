import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pyautogui","pygetwindow", "CustomTkinter", "darkdetect", "tkinter", "sqlite3"],
    "include_files": [
        
        os.path.join("src", "view", "assets", "favico.ico"),
        os.path.join("src", "view", "assets", "homeIcoDark.png"),
        os.path.join("src", "view", "assets", "axix-solution-logo.png"),
        
        # os.path.join("src", "view", "components", "CustomButton.py"),
        # os.path.join("src", "view", "components", "CustomCheckbox.py"),
        # os.path.join("src", "view", "components", "HwFrame.py"),
        
        # os.path.join("src", "view", "functions", "ButtonHandler.py"),
        # os.path.join("src", "view", "functions", "FrameManagement.py"),
        # os.path.join("src", "view", "functions", "HomeIcon.py"),
        
        # os.path.join("src", "view", "pages", "CreateProject.py"),
        # os.path.join("src", "view", "pages", "HomePage.py"),
        # os.path.join("src", "view", "pages", "OpenProject.py"),
        
        # os.path.join("src", "openness", "controllers", "OpennessController.py"),
        
        os.path.join("src", "openness", "database", "Openness.db"),
        
        # os.path.join("src", "openness", "repositories", "DbManagement.py"),
        
        # os.path.join("src", "openness", "services", "CompilerService.py"),
        # os.path.join("src", "openness", "services", "HwFeaturesService.py"),
        # os.path.join("src", "openness", "services", "LanguageService.py"),
        # os.path.join("src", "openness", "services", "OponessService.py"),
        # os.path.join("src", "openness", "services", "TiaService.py"),
        # os.path.join("src", "openness", "services", "Utils.py"),
        # os.path.join("src", "openness", "services", "XmlService.py"),
   
    ]
}

if sys.platform == "win32":
    base = "Win32GUI"
    
target = Executable(
    base=base,
    script="src/App.py",
    icon="src/view/assets/favico.ico",
    target_name="RPA Tia Openness"
    )

setup(
    version="1.1.0",
    description="Interface for automated creation of TIA Portal projects using Openness API",
    options={"build_exe": build_exe_options},
    executables=[target],
    include_msvcr=True
)
