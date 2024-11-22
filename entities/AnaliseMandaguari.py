import re
from datetime import datetime

def validarMandaguariPR(conteudo):
    if('MUNICIPIO DE MANDAGUARI' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CPF/CNPJ' in linha):
                linhaNova = re.split(',', linha)

                for linha2 in linhaNova:
                    if('CPF/CNPJ' in linha2):
                        cnpj = re.split(' nº ', linha2)[-1].strip()
                
            if('VALIDADE ATÉ' in linha):
                dataValidade = re.split('ATÉ ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'