import re
from datetime import datetime

def validarArapotiPR(conteudo):
    
    if("Municipal de Arapoti" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CNPJ/CPF:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if("VALIDADE:" in linha):
                dataValidade = linha.split(': ')[1]
                dataValidade = dataValidade.split('.')[0].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
        return cnpj, dataValidade

    return '-', '-'