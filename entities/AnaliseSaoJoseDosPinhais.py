import re
import locale
from datetime import datetime, timedelta

def validarSaoJoseDosPinhaisPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPAL DE SÃO JOSÉ DOS PINHAIS' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)
        cnpj = '-'
        dataValidade = '-'

        for i, linha in enumerate(conteudo):
            if('CPF:' in linha):
                cnpj = conteudo[i+1].strip()
                
            if('São José dos Pinhais,' in linha or 'SÃO JOSÉ DOS PINHAIS,' in linha):
                dataValidade = linha.split(',')[-1].replace('.', '').strip()
                try:
                    dataValidade = datetime.strptime(dataValidade,'%d de %B de %Y') + timedelta(days=60)
                except:
                    dataValidade = '-'

        return cnpj, dataValidade
    return '-', '-'