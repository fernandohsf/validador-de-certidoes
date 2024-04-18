import re
import locale
from datetime import datetime, timedelta

def validarItapejaraDoestePR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    if("MUNICIPIO.: Itapejara d'Oeste" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CNPJ/CPF.' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if("Emitida" in linha):
                dataValidade = linha.split(' ')[-1].replace('.', '').strip()
                dataValidade = datetime.strptime(dataValidade,'%d/%m/%Y') + timedelta(days=60)
                
        return cnpj, dataValidade
    return '-', '-'