import re
from datetime import datetime

def validarLaranjeirasDoSulPR(conteudo):
    if('Município de Laranjeiras do Sul' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ:' in linha):
                cnpj = re.split(': ', linha)[-1].strip()
                
            if('VÁLIDA ATÉ' in linha):
                dataValidade = conteudo[i-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

        return cnpj, dataValidade
    return '-', '-'