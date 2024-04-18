import re
from datetime import datetime

def validarVirmondPR(conteudo):

    if("Município de Virmond" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF' in linha):
                cnpj = conteudo[i+4].strip()

            if('VALIDADE:' in linha):
                dataValidade = linha.split(': ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade 
    return '-', '-'