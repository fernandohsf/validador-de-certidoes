import re
from datetime import datetime

def validarIretamaPR(conteudo):

    if("MUNICIPIO DE IRETAMA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CPF / CNPJ' in linha):
                cnpj = linha.split(': ')[-1].strip()

            if('Validade:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade 
    return '-', '-'