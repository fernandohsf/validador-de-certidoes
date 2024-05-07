import re
from datetime import datetime

def validarPeabiruPR(conteudo):
    if('MUNICIPIO DE PEABIRU' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = re.split(' nº ', linha)[-1].replace(',', '').strip()
                if(len(cnpj) != 18):
                    cnpj = conteudo[i+1].split(',')[0].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split(' ATÉ ', linha)[-1]
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'