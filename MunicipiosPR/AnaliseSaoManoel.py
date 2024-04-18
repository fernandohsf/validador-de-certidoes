import re
from datetime import datetime

def validarSaoManoelPR(conteudo):
    if('MUNICÍPIO DE SÃO MANOEL' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CNPJ:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if('Validade:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')

        return cnpj, dataValidade
    return '-', '-'