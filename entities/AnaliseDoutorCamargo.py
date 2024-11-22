import re
from datetime import datetime

def validarDoutorCamargoPR(conteudo):
    if("Municipal de Doutor Camargo" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ' in linha):
                linhaNova = linha + conteudo[i+1]
                cnpj = linhaNova.split(' nº ')[-1]
                cnpj = cnpj.split(',')[0].strip()
                
            if("VALIDADE ATÉ" in linha):
                dataValidade = linha.split(' ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'