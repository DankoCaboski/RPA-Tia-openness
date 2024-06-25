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