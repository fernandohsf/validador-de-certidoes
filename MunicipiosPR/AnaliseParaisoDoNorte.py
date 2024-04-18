import re
from datetime import datetime

def validarParaisoDoNortePR(conteudo):
    if('MUNICIPIO DE PARAISO DO NORTE' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CPF/CNPJ' in linha):
                cnpj = linha.split(',')
                for linhaNova in cnpj:
                    if('nº' in linhaNova):
                        cnpj = linhaNova.split(' nº ')[-1].strip()
                        break
            
            if('VALIDADE ATÉ' in linha):
                dataValidade = linha.split(' ')[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade
    return '-', '-'