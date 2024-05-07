import re
from datetime import datetime

def validarMandiritubaPR(conteudo):

    if("MUNICIPAL DE MANDIRITUBA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

            if('Validade' in linha):
                dataValidade = conteudo[i+3].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade 
    return '-', '-'