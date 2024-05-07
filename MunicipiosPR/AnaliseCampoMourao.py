import re
import locale
from datetime import datetime, timedelta

def validarCampoMouraoPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPAL DE CAMPO MOURÃO' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CPF:' in linha or 'CNPJ:' in linha):
                cnpj = re.split(': ', linha)[-1].strip()
                
            if('Validade:' in linha):
                dataValidade = re.split(': ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y')
                except:
                    dataValidade = '-'

            if('CAMPO MOURÃO,' in linha):
                dataValidade = re.split(', ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y.') + timedelta(days=30)
                except:
                    dataValidade = '-'
                
        return cnpj,dataValidade
    return '-', '-'