from openness.services.Utils import Utils

import re

class XmlService:
    def __init__(self):
        pass
    
    def list_udt_from_xml(self, xml_path):
        udts = []
        with open(xml_path, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            pattern = r'<Member[^>]+Datatype="&quot;([^&]+)&quot;"[^>]*>'

            matches = re.findall(pattern, conteudo)
            for match in matches:
                udts.append(match)
        return udts
    
    def editar_tags_xml(self, arquivo, novo_nome, novo_numero):
        
        with open(arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.read()

        # Substituir o texto nas tags <Name> e <Number>
        conteudo = re.sub(r'(?<=<Name>)[^<]+(?=</Name>)', novo_nome, conteudo)
        conteudo = re.sub(r'(?<=<Number>)[^<]+(?=</Number>)', str(novo_numero), conteudo)
        
        with open(arquivo, 'w', encoding='utf-8') as file:
            file.write(conteudo)
