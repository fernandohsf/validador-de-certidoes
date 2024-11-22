import re
from datetime import datetime

def validarLapaPR(conteudo):
    if("MUNICÍPIO DA LAPA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('Contribuinte' in linha):
                cnpj = conteudo[i+3].strip()
                
            if("Válida até" in linha):
                dataValidade = linha.split(' ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'