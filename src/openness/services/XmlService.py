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

    def edit_tags_xml(self, arquivo, index):
        with open(arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.read()

        # Encontrar o valor atual dentro da tag <Name> e <Number>
        nome_atual = re.search(r'(?<=<Name>)[^<]+(?=</Name>)', conteudo)
        numero_atual = re.search(r'(?<=<Number>)[^<]+(?=</Number>)', conteudo)
        
        print(nome_atual)
        print(numero_atual)

        # Inicializar novo_nome e novo_numero
        novo_nome = ""
        novo_numero = ""

        if nome_atual:
            nome_atual = nome_atual.group()
            # Substituir o último número antes de _MG com o novo índice
            nome_part = re.search(r'(\d+)(?=_MG)', nome_atual)
            if nome_part:
                novo_nome = nome_atual[:nome_part.start()] + str(int(nome_part.group())) + f"_MG0{index+1}"
            else:
                novo_nome = nome_atual + f"_MG0{index+1}"
        else:
            novo_nome = f"Name_MG0{index+1}"

        if numero_atual:
            numero_atual = int(numero_atual.group())
            novo_numero = numero_atual + (index - 1 )
        else:
            novo_numero = "1"
        print(novo_nome)
        print(novo_numero)
        # Substituir o texto nas tags <Name> e <Number>
        conteudo = re.sub(r'(?<=<Name>)[^<]+(?=</Name>)', novo_nome, conteudo)
        conteudo = re.sub(r'(?<=<Number>)[^<]+(?=</Number>)', str(novo_numero), conteudo)

        with open(arquivo, 'w', encoding='utf-8') as file:
            file.write(conteudo)