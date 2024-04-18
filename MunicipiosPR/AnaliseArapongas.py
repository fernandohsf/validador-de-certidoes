import re
import locale
from datetime import datetime, timedelta

def validarArapongasPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if("Municipal de Arapongas" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for linha in conteudo:
            if('CNPJ' in linha):
                cnpj = linha.split(': ')[-1].strip()
                
            if("Arapongas - PR," in linha):
                dataValidade = linha.split(', ')[-1]
                dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=90)
                
            if('COMPROVAÇÃO…' in linha):
                dataValidade = conteudo[-2].strip()
                dataValidade = dataValidade.split('Tributação ')[-1].replace('.', '')
                dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=90)

        return cnpj, dataValidade                  
    return '-', '-'