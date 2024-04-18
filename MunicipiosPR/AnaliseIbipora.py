import re
from datetime import datetime

def validarIbiporaPR(conteudo):
    if('MUNICIPIO DE IBIPORA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = re.split(',', linha)[1]
                cnpj = re.split(' ', cnpj)[-1]
                
                if(len(cnpj) != 18):
                    linhaNova = linha + conteudo[i+1]
                    cnpj = linhaNova.split(' nº ')[-1]
                    cnpj = cnpj.split(',')[0].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split(' ATÉ ', linha)[-1]
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

        return cnpj, dataValidade
    return '-', '-'