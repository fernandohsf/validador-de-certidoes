import re
from datetime import datetime

def validarArapotiPR(conteudo):
    
    if("Municipal de Arapoti" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CNPJ/CPF:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if("VALIDADE:" in linha):
                dataValidade = linha.split(': ')[1]
                dataValidade = dataValidade.split('.')[0].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                    
        return cnpj, dataValidade

    return '-', '-'