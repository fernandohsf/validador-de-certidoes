import re
import locale
from datetime import datetime, timedelta

def validarIzabelDoOestePR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if("MUNICÍPIO DE SANTA IZABEL DO OESTE" in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CNPJ/CPF' in linha):
                cnpj = conteudo[i+1].strip()

            if('Emitida em ' in linha):
                dataValidade = linha.split('em ')[-1].replace('.', '').strip()
                dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=60)
                
        return cnpj, dataValidade
    return '-', '-'