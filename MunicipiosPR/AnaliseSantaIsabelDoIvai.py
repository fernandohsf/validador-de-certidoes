import re
from datetime import datetime

def validarSantaIsabelDoIvaiPR(conteudo):
    if('MUNICÍPIO DE SANTA ISABEL DO IVAÍ' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('ALVARÁ' in linha):
                cnpj = conteudo[i+5].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split('ATÉ ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y.')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'