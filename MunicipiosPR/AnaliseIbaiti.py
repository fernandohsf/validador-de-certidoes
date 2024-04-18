import re
from datetime import datetime

def validarIbaitiPR(conteudo):
    if('Ibaiti,' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('ALVARÁ' in linha):
                cnpj = conteudo[i+2].strip()
                
            if('VALIDADE:' in linha):
                dataValidade = re.split(': ', linha)[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

        return cnpj, dataValidade
    return '-', '-'