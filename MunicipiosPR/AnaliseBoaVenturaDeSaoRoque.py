import re
from datetime import datetime

def validarBoaVenturaDeSaoRoquePR(conteudo):

    if('Municipal de Boa Ventura de São Roque' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF' in linha):
                cnpj = conteudo[i+4].strip()
            
            if('CERTIDÃO TEM VALIDADE' in linha):
                dataValidade = conteudo[i+3].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
        return cnpj, dataValidade

    return '-', '-'