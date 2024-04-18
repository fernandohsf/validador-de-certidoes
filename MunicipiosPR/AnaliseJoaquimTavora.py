import re
from datetime import datetime, timedelta

def validarJoaquimTavoraPR(conteudo):
    if('Municipal de Joaquim Távora' in conteudo):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CNPJ:' in linha):
                cnpj = re.split(': ', linha)[-1].strip()
                
            if('Municipal de Joaquim Távora' in linha):
                linha = linha.replace('.', '')
                dataValidade = re.split(', ', linha)[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=30)

        return cnpj, dataValidade
    return '-', '-'