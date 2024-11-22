import re
from datetime import datetime

def validarPiraiDoSulPR(conteudo):
    if('MUNICÍPIO DE PIRAÍ DO SUL' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CNPJ/CPF:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = linha.split('ATÉ ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y.')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'