import re
from datetime import datetime

def validarBorrazopolisPR(conteudo):
    
    if('MUNICIPAL DE BORRAZOPOLIS' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = re.split(', ', linha)[0]
                cnpj = re.split('nº ', cnpj)[-1].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split(' ', linha)[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
        return cnpj, dataValidade

    return '-', '-'