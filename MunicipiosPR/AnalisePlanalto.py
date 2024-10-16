import re
from datetime import datetime

def validarPlanaltoPR(conteudo):
    if("Prefeitura Municipal de Planalto" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if 'CNPJ/CPF' in linha:
                cnpj = conteudo[i+4].strip()
                
            if("TEM VALIDADE" in linha):
                dataValidade = conteudo[i+3].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'                
        return cnpj, dataValidade
    return '-', '-'