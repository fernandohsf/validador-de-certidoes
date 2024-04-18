import re
import locale
from datetime import datetime, timedelta

def validarLondrinaPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICÍPIO DE LONDRINA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ:' in linha):
                cnpj = re.split(': ', linha)[-1].strip()
                
            if('Londrina,' in linha):
                dataValidade = re.split(', ', linha)[-1].strip()
                dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=120)

        return cnpj, dataValidade
    return '-', '-'

    