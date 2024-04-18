import re
from datetime import datetime

def validarIvaiporaPR(conteudo):
    if('MUNICIPAL DE IVAIPORA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('RAZÃO SOCIAL/NOME' in linha):
                cnpj = conteudo[i+9].strip()
            
            if('VALIDADE ATÉ' in linha):
                dataValidade = linha.split(' ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade
    return '-', '-'