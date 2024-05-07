import re
from datetime import datetime

def validarTerraBoaPR(conteudo):
    if("MUNICIPIO DE TERRA BOA" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF' in linha):
                cnpj = conteudo[i+6].strip()
                
            if("VALIDADE ATÉ" in linha):
                dataValidade = linha.split(' ')[-1].replace('.', '').strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'