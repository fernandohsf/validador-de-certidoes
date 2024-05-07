import re
import locale
from datetime import datetime, timedelta

def validarLunardelliPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPAL DE LUNARDELLI' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('Contribuinte:' in linha):
                cnpj = conteudo[i+3].strip()
                cnpj = cnpj.split('\t')[0].strip()
            
            if('Lunardelli - PR,' in linha):
                dataValidade = linha.split(', ')
                dataValidade = dataValidade[-2] + dataValidade[-1]
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d %B%Y') + timedelta(days=60)
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'