import re
from datetime import datetime

def validarGuairaPR(conteudo):
    if('MUNICIPIO DE GUAIRA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = conteudo[i+1].strip()
            
            if('Validade até:' in linha):
                dataValidade = conteudo[i+1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade
    return '-', '-'