from openness.services.Utils import Utils

class CompilerService:
    def __init__(self, comp):
        self.comp = comp
        
    def compilate_item(self, to_compile):
        try:
            print("Compiling item: ", to_compile)
            compiler_result = Utils().get_service(self.comp.ICompilable, to_compile).Compile()
            
            enumerable_attributes = Utils().get_attributes(["State"], compiler_result)
            state = enumerable_attributes[0]
            print("State: ", state)
            
            return state
            
            # get_compilation_error_description(compiler_result.Messages)
                
        except Exception as e:
            print('Error compiling device:', e)