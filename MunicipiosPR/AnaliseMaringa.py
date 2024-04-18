import re
from datetime import datetime

def validarMaringaPR(conteudo):
    if('MUNICIPIO DE MARINGA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ' in linha):
                linhaNova = re.split(',', linha)
                for linha2 in linhaNova:
                    if('CPF/CNPJ' in linha2):
                        cnpj = linha2.split(' nº ')[-1].strip()
                if(cnpj == ''):
                    cnpj = conteudo[i+1]
                    cnpj = cnpj.split(',')[0].strip()
                
            if('Válida até:' in linha):
                dataValidade = conteudo[i+1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

        return cnpj, dataValidade
    return '-', '-'