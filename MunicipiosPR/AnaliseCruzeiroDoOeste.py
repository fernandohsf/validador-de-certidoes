import re
from datetime import datetime

def validarCruzeiroDoOestePR(conteudo):
    if('MUNICIPIO DE CRUZEIRO DO OESTE' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ' in linha):
                cnpj = linha.split(' nº ')[-1].strip()

                if(len(cnpj) != 18):
                    linhaNova = linha + conteudo[i+1]
                    cnpj = linhaNova.split(' nº ')[-1]
                    cnpj = cnpj.split(',')[0].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split('ATÉ ', linha)[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                
        return cnpj, dataValidade
    return '-', '-'