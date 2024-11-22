import re
from datetime import datetime, timedelta

def validarGuarapuavaPR(conteudo):
    if('MUNICÍPIO DE GUARAPUAVA' in conteudo):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = conteudo[i+1].strip()
                
            if('DATA DE VALIDADE' in linha):
                dataValidade = conteudo[i+1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=90)
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'