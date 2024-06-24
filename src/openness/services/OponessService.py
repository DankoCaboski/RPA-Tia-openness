import clr

from openness.services.TiaService import TiaService
from openness.services.HwFeaturesService import HwFeaturesService
from openness.services.CompilerService import CompilerService

from openness.repositories.DbManagement import DbManagement

class OpennessService:
    def __init__(self, database):
        self.database: DbManagement = database
        self.tia: TiaService = None
        self.hwf: HwFeaturesService = None
        self.comp: CompilerService = None
        print("OpennessService initialized")
    
    def set_dll(self, tia_Version):
        try:
            project_dll = self.database.getDllPath(tia_Version)
            if project_dll is None:
                result = f"Não foi possível obter o caminho da DLL para a versão {tia_Version}."
                return result
            
            clr.AddReference(project_dll[0])
            
            global tia, hwf, comp

            import Siemens.Engineering as tia # type: ignore
            self.tia = TiaService(tia)
            import Siemens.Engineering.HW.Features as hwf # type: ignore
            self.hwf = HwFeaturesService(hwf)
            import Siemens.Engineering.Compiler as comp # type: ignore
            self.comp = CompilerService(comp)
        
            result = "Versãod o tia configurada com sucesso!"
            return result

        except Exception as e:
            result = "Error adding DLL reference: " + str(e)
            return result
    
    def create_project(self, proj_name, proj_path, tia_version):
        try:
            self.tia.create_project(proj_name, proj_path, tia_version)
            return "Projeto criado com sucesso!"
        except Exception as e:
            return "Falha ao criar projeto: " + str(e)