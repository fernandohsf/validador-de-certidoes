import re
from datetime import datetime, timedelta

def validarGuarapuavaPR(conteudo):
    if('MUNICÍPIO DE GUARAPUAVA' in conteudo):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = conteudo[i+1].strip()
                
            if('DATA DE VALIDADE' in linha):
                dataValidade = conteudo[i+1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=90)

        return cnpj, dataValidade
    return '-', '-'