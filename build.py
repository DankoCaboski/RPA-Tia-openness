import subprocess
import os
from src.openness.repositories.DbManagement import DbManagement

current_path = os.path.abspath(__file__)
src_path = os.path.join(os.path.dirname(current_path), "src")

requirements_path = os.path.join(os.path.dirname(current_path), "requirements.txt")

def install_dependencies():
    subprocess.call(["pip", "install", "-r", requirements_path])

def build():
    DbManagement().validate_db()
    
    setup_file = os.path.join(src_path, "setup.py")
    subprocess.call(["python", setup_file, "build"])
        
install_dependencies()
build()
