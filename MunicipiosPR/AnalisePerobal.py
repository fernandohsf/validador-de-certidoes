import re
import locale
from datetime import datetime, timedelta

def validarPerobalPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    if('MUNICÍPIO DE PEROBAL' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('Proprietário' in linha):
                cnpj = conteudo[i+1].strip()
                
            if('Perobal,' in linha):
                dataValidade = re.split(', ', linha)[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y.') + timedelta(days=30)
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'