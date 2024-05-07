import re
from datetime import datetime

def validarAndiraPR(conteudo):

    if("MUNICIPAL DE ANDIRÁ" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ' in linha):
                cnpj = linha + conteudo[i+1]
                cnpj = cnpj.split('nº ')[-1].split(',')[0].strip()

            if('VALIDADE ATÉ' in linha):
                dataValidade = linha.split('ATÉ ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade 
    return '-', '-'