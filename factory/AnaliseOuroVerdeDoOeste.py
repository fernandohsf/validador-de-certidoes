import re
from datetime import datetime, timedelta

def validarOuroVerdeDoOestePR(conteudo):
    if('MUNICÍPIO DE OURO VERDE DO OESTE' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = conteudo[i+1].strip()
            
            if('DATA DE EMISSÃO' in linha):
                dataValidade = conteudo[i+2].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=60)
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'