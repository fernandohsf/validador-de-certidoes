import re
from datetime import datetime

def validarCampinaGrandeDoSulPR(conteudo):

    if('MUNICIPAL DE CAMPINA GRANDE DO SUL' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CPF/CNPJ' in linha):
                cnpj = re.split(',', linha)[1]
                cnpj = cnpj.split(' nº ')[-1].strip()
            
            if('Válida até:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
        
        return cnpj, dataValidade
    return '-', '-'