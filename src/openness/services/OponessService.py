import clr

class OpennessService:
    def __init__(self):
        self.tia = None
        self.hwf = None
        self.comp = None
    
    def set_dll(self, project_dll):
        try:
            if tuple is None:
                pass
                print(f"Não foi possível obter o caminho da DLL para a versão {tia_Version}.")
                return False
            
            clr.AddReference(project_dll)
            
            global tia, hwf, comp

            import Siemens.Engineering as tia # type: ignore
            self.tia = tia
            import Siemens.Engineering.HW.Features as hwf # type: ignore
            self.hwf = hwf
            import Siemens.Engineering.Compiler as comp # type: ignore
            self.comp = comp

        except Exception as e:
            print("Error adding DLL reference: ", e)
            return False