import re
import os

class UDTService:
    def __init__(self) -> None:
        pass
    
    def list_udt_from_bk(self, bk_path):
        is_valid_path = bk_path and isinstance(bk_path, str) and bk_path.endswith('.xml') and os.path.exists(bk_path) and os.path.isfile(bk_path)
        if not is_valid_path:
            raise Exception(f"\nbk_path is not valid\nbk_path: {bk_path}")
        
        print(f"\nListing UDTs from {bk_path}")
        udts = []
        with open(bk_path, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            # Expressão regular para capturar o valor do atributo Type dentro da tag Parameter
            pattern = r'<Parameter[^>]+Type="&quot;([^&]+)&quot;"[^>]*>'
            matches = re.findall(pattern, conteudo)
            for match in matches:
                udts.append(match)
        print(f"UDTs: {udts}")
        return udts