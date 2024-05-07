import re
from datetime import datetime

def validarIretamaPR(conteudo):

    if("MUNICIPIO DE IRETAMA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CPF / CNPJ' in linha):
                cnpj = linha.split(': ')[-1].strip()

            if('Validade:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade 
    return '-', '-'