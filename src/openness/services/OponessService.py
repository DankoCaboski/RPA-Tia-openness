import clr

from openness.services.TiaService import TiaService
from openness.services.HardwareFeatures import HardwareFeatures
from openness.services.CompilerService import CompilerService

class OpennessService:
    def __init__(self):
        self.tia = None
        self.hwf = None
        self.comp = None
        print("OpennessService initialized")
    
    def set_dll(self, tia_Version):
        try:
            if project_dll is None:
                print(f"Não foi possível obter o caminho da DLL para a versão {tia_Version}.")
                return False
            
            clr.AddReference(project_dll)
            
            global tia, hwf, comp

            import Siemens.Engineering as tia # type: ignore
            self.tia = TiaService(tia)
            import Siemens.Engineering.HW.Features as hwf # type: ignore
            self.hwf = HardwareFeatures(hwf)
            import Siemens.Engineering.Compiler as comp # type: ignore
            self.comp = CompilerService(comp)

        except Exception as e:
            print("Error adding DLL reference: ", e)
            return False