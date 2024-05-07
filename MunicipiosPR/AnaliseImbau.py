import re
from datetime import datetime

def validarImbauPR(conteudo):
    if('MUNICIPIO DE IMBAU' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CNPJ' in linha):
                cnpj = re.split(',', linha)[1]
                cnpj = re.split(' ', cnpj)[-1]
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split(' ATÉ ', linha)[-1]
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'