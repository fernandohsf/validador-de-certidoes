import re
from datetime import datetime

def validarIbaitiPR(conteudo):
    if('Ibaiti,' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('ALVARÁ' in linha):
                cnpj = conteudo[i+2].strip()
                
            if('VALIDADE:' in linha):
                dataValidade = re.split(': ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'