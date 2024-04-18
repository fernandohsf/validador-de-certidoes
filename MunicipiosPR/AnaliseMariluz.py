import re
import locale
from datetime import datetime, timedelta

def validarMariluzPR(conteudo):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if('MUNICIPAL DE MARILUZ' in conteudo and not('Documento Auxiliar da NFS-e' in conteudo)):
        conteudo = re.sub('\xa0', ' ', conteudo)
        conteudo = re.split('\n', conteudo)

        for i, linha in enumerate(conteudo):
            if('CPF/CNPJ:' in linha):
                cnpj = conteudo[i+2].strip()
            
            if('Exercício:' in linha):
                ano = linha.split(':')[-1].strip()
            if('Mariluz - PR,' in linha):
                dataValidade = linha.split(',')[-1].strip()
                dataValidade = f'{dataValidade} de {ano}'
                dataValidade = datetime.strptime(dataValidade,'%d %B de %Y') + timedelta(days=30)
                
        return cnpj, dataValidade
    return '-', '-'