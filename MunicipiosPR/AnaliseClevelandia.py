import re
from datetime import datetime, timedelta

def validarClevelandiaPR(conteudo):
    if('MUNICÍPIO DE CLEVELÂNDIA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = conteudo[i+1].strip()
            
            if('DATA DE EMISSÃO' in linha):
                dataValidade = conteudo[i+2].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=90)
        return cnpj, dataValidade
    return '-', '-'