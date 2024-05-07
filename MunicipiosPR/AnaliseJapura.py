import re
from datetime import datetime

def validarJapuraPR(conteudo):
    if("MUNICÍPIO DE JAPURÁ" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ' in linha):
                cnpj = linha.split(' nº ')[-1].split(',')[0].strip()
                
            if("valida até" in linha):
                dataValidade = linha.strip().split(' ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'