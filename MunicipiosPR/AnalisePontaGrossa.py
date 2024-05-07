import re
import locale
from datetime import datetime, timedelta

def validarPontaGrossaPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPAL DE PONTA GROSSA' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for linha in conteudo:
            if('CNPJ/CPF:' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if('PONTA GROSSA,' in linha):
                dataValidade = linha.split(', ')[-1].strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=60)
                except:
                    dataValidade = '-'
                
        return cnpj, dataValidade
    return '-', '-'