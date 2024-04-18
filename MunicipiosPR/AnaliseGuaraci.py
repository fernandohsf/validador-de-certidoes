import re
from datetime import datetime

def validarGuaraciPR(conteudo):
    if("MUNICIPAL DE GUARACI" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CADASTRO' in linha):
                cnpj = conteudo[i+1].strip()
                
            if("VALIDADE ATÉ" in linha):
                dataValidade = linha.split(' ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade
    return '-', '-'