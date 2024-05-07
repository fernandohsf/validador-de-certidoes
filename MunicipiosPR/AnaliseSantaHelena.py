import re
import locale
from datetime import datetime, timedelta

def validarSanteHelenaPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPIO DE SANTA HELENA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF:' in linha):
                cnpj = conteudo[i+1].strip()
                
            if('SANTA HELENA - PR,' in linha):
                dataValidade = re.split(',', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=60)
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'