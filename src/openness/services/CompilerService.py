from openness.services.Utils import Utils

class CompilerService:
    def __init__(self, comp):
        self.comp = comp
        
    def compilate_item(self, to_compile):
        try:
            RPA_status = "Compiling..."
            print(RPA_status)
            print("Compiling item: ", to_compile)
            compiler_result = Utils().get_service(self.comp.ICompilable, to_compile).Compile()
            
            enumerable_attributes = Utils().get_attributes(["State"], compiler_result)
            state = enumerable_attributes[0]
            print("State: ", state)
            
            if state == "Success":
                RPA_status = "Compilation successful!"
                print(RPA_status)
                return RPA_status
            else:
                RPA_status = "Compilation failed!"
                print(RPA_status)
                return RPA_status
                # get_compilation_error_description(compiler_result.Messages)
                
        except Exception as e:
            print('Error compiling device:', e)