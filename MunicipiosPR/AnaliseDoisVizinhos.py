import re
from datetime import datetime

def validarDoisVizinhosPR(conteudo):
    if("Dois Vizinhos," in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ' in linha):
                cnpj = conteudo[i+1].strip()
                
            if("Valida até:" in linha):
                dataValidade = linha.split(':')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except: 
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'