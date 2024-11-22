import re
from datetime import datetime

def validarFranciscoBeltraoPR(conteudo):
    if("MUNICÍPIO DE FRANCISCO BELTRÃO" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ:' in linha):
                cnpj = conteudo[i-1].strip()
                
            if("E M I S S Ã O :" in linha):
                dataValidade = conteudo[i+2].replace(' ', '')
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'